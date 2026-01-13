"""
Unit tests for Crawler.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from vnewsapi.core.crawler import Crawler
from vnewsapi.exceptions import CrawlerError, ConfigurationError


class TestCrawler:
    """Test cases for Crawler."""
    
    def test_crawler_init_valid_site(self):
        """Test crawler initialization with valid site."""
        crawler = Crawler('cafef')
        assert crawler.site_name == 'cafef'
        assert crawler.config is not None
        assert 'name' in crawler.config
    
    def test_crawler_init_invalid_site(self):
        """Test crawler initialization with invalid site."""
        with pytest.raises(ConfigurationError):
            Crawler('invalid_site')
    
    def test_crawler_init_custom_config(self):
        """Test crawler initialization with custom config."""
        custom_config = {
            'name': 'Custom Site',
            'base_url': 'https://custom.com',
            'rss': {'urls': ['https://custom.com/rss']},
            'selectors': {}
        }
        crawler = Crawler('cafef', custom_config=custom_config)
        assert crawler.config['name'] == 'Custom Site'
    
    @patch('vnewsapi.core.crawler.RSS')
    def test_get_articles_from_rss(self, mock_rss_class):
        """Test getting articles from RSS."""
        mock_rss = Mock()
        mock_rss.fetch.return_value = [
            {'title': 'Test', 'link': 'https://example.com', 'pubDate': '2024-01-01', 'description': 'Test'}
        ]
        mock_rss_class.return_value = mock_rss
        
        crawler = Crawler('cafef')
        df = crawler.get_articles(limit=10, prefer_rss=True)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
    
    @patch('vnewsapi.core.crawler.Sitemap')
    def test_get_articles_from_sitemap(self, mock_sitemap_class):
        """Test getting articles from sitemap."""
        mock_sitemap = Mock()
        mock_sitemap.run.return_value = pd.DataFrame({
            'loc': ['https://example.com'],
            'lastmod': ['2024-01-01']
        })
        mock_sitemap_class.return_value = mock_sitemap
        
        crawler = Crawler('cafef')
        # Mock RSS to fail so it falls back to sitemap
        crawler.rss_parser.fetch = Mock(side_effect=Exception("RSS failed"))
        
        df = crawler.get_articles(limit=10, prefer_rss=True)
        
        assert isinstance(df, pd.DataFrame)
    
    @patch('vnewsapi.core.crawler.send_request')
    @patch('vnewsapi.core.crawler.get_headers')
    def test_get_article_details(self, mock_headers, mock_send_request):
        """Test getting article details."""
        mock_send_request.return_value = """<!DOCTYPE html>
<html>
<body>
    <h1 class="title">Test Title</h1>
    <div class="detail-content"><p>Test content</p></div>
    <div class="sapo">Test summary</div>
    <span class="time">2024-01-01</span>
    <span class="author">Test Author</span>
</body>
</html>"""
        mock_headers.return_value = {'User-Agent': 'test'}
        
        crawler = Crawler('cafef')
        details = crawler.get_article_details('https://example.com/article')
        
        assert details['url'] == 'https://example.com/article'
        assert 'title' in details
        assert 'content' in details

