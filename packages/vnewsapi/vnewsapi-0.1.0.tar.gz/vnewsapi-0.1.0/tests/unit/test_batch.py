"""
Unit tests for BatchCrawler.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from vnewsapi.core.batch import BatchCrawler
from vnewsapi.exceptions import CrawlerError


class TestBatchCrawler:
    """Test cases for BatchCrawler."""
    
    def test_batch_crawler_init(self):
        """Test batch crawler initialization."""
        batch = BatchCrawler('cafef', request_delay=1.0)
        assert batch.site_name == 'cafef'
        assert batch.request_delay == 1.0
        assert batch.crawler is not None
    
    @patch('vnewsapi.core.batch.time.sleep')
    @patch('vnewsapi.core.batch.Crawler')
    def test_fetch_details_for_urls_success(self, mock_crawler_class, mock_sleep):
        """Test successful batch fetch."""
        mock_crawler = Mock()
        mock_crawler.get_article_details.return_value = {
            'url': 'https://example.com',
            'title': 'Test',
            'content': 'Test content'
        }
        mock_crawler_class.return_value = mock_crawler
        
        batch = BatchCrawler('cafef', request_delay=0.1)
        batch.crawler = mock_crawler
        
        urls = ['https://example.com/1', 'https://example.com/2']
        df = batch.fetch_details_for_urls(urls, show_progress=False)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert mock_crawler.get_article_details.call_count == 2
    
    @patch('vnewsapi.core.batch.time.sleep')
    @patch('vnewsapi.core.batch.Crawler')
    def test_fetch_details_for_urls_with_errors(self, mock_crawler_class, mock_sleep):
        """Test batch fetch with some errors."""
        mock_crawler = Mock()
        mock_crawler.get_article_details.side_effect = [
            {'url': 'https://example.com/1', 'title': 'Test'},
            Exception("Error"),
        ]
        mock_crawler_class.return_value = mock_crawler
        
        batch = BatchCrawler('cafef', request_delay=0.1)
        batch.crawler = mock_crawler
        
        urls = ['https://example.com/1', 'https://example.com/2']
        df = batch.fetch_details_for_urls(urls, show_progress=False)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.iloc[1]['error'] is not None
    
    def test_fetch_details_from_dataframe(self):
        """Test fetching details from DataFrame."""
        df_input = pd.DataFrame({
            'link': ['https://example.com/1', 'https://example.com/2'],
            'title': ['Title 1', 'Title 2']
        })
        
        batch = BatchCrawler('cafef', request_delay=0.1)
        batch.fetch_details_for_urls = Mock(return_value=pd.DataFrame({
            'url': ['https://example.com/1', 'https://example.com/2'],
            'content': ['Content 1', 'Content 2']
        }))
        
        result_df = batch.fetch_details_from_dataframe(df_input, url_column='link')
        
        assert isinstance(result_df, pd.DataFrame)
        assert 'content' in result_df.columns

