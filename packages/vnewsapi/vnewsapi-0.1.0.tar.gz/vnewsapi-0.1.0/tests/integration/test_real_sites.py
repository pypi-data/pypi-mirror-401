"""
Integration tests for real news websites.

These tests make actual HTTP requests to news websites.
Mark with @pytest.mark.integration and @pytest.mark.slow.
"""

import pytest
from vnewsapi.core.crawler import Crawler
from vnewsapi.core.rss import RSS
from vnewsapi.core.sitemap import Sitemap


@pytest.mark.integration
@pytest.mark.slow
class TestRealSites:
    """Integration tests with real news websites."""
    
    @pytest.mark.parametrize("site_name", ["cafef", "vietstock"])
    def test_crawler_get_articles(self, site_name):
        """Test getting articles from real sites."""
        crawler = Crawler(site_name, timeout=30)
        df = crawler.get_articles(limit=5)
        
        assert not df.empty
        assert 'link' in df.columns
        assert len(df) <= 5
    
    @pytest.mark.parametrize("site_name", ["cafef"])
    def test_crawler_get_article_details(self, site_name):
        """Test getting article details from real site."""
        crawler = Crawler(site_name, timeout=30)
        
        # First get article list
        articles_df = crawler.get_articles(limit=1)
        if articles_df.empty:
            pytest.skip("No articles available")
        
        # Get details for first article
        article_url = articles_df.iloc[0]['link']
        details = crawler.get_article_details(article_url)
        
        assert details['url'] == article_url
        assert 'title' in details
        assert 'content' in details
    
    def test_rss_fetch_real(self):
        """Test RSS fetch from real feed."""
        rss = RSS(timeout=30)
        # Use a known RSS feed
        articles = rss.fetch('https://cafef.vn/rss/tin-moi-nhat.rss')
        
        assert len(articles) > 0
        assert 'title' in articles[0]
        assert 'link' in articles[0]

