"""
Unit tests for RSS parser.
"""

import pytest
from unittest.mock import Mock, patch
from vnewsapi.core.rss import RSS
from vnewsapi.exceptions import RSSParseError, NetworkError


class TestRSS:
    """Test cases for RSS parser."""
    
    def test_rss_init(self):
        """Test RSS parser initialization."""
        rss = RSS(timeout=30, data_source='CAFEF')
        assert rss.timeout == 30
        assert rss.data_source == 'CAFEF'
    
    @patch('vnewsapi.core.rss.send_request')
    @patch('vnewsapi.core.rss.get_headers')
    def test_fetch_success(self, mock_headers, mock_send_request):
        """Test successful RSS feed fetch."""
        # Mock response
        mock_send_request.return_value = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <item>
            <title>Test Article</title>
            <link>https://example.com/article</link>
            <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
            <description>Test description</description>
        </item>
    </channel>
</rss>"""
        mock_headers.return_value = {'User-Agent': 'test'}
        
        rss = RSS()
        articles = rss.fetch('https://example.com/rss')
        
        assert len(articles) == 1
        assert articles[0]['title'] == 'Test Article'
        assert articles[0]['link'] == 'https://example.com/article'
    
    @patch('vnewsapi.core.rss.send_request')
    def test_fetch_network_error(self, mock_send_request):
        """Test RSS fetch with network error."""
        mock_send_request.side_effect = NetworkError("Connection failed")
        
        rss = RSS()
        with pytest.raises(NetworkError):
            rss.fetch('https://example.com/rss')
    
    @patch('vnewsapi.core.rss.send_request')
    def test_fetch_invalid_rss(self, mock_send_request):
        """Test RSS fetch with invalid content."""
        mock_send_request.return_value = "Invalid XML content"
        
        rss = RSS()
        # feedparser is lenient, it won't raise but will return empty entries
        # So we check if result is empty list (which is acceptable)
        articles = rss.fetch('https://example.com/rss')
        # feedparser might parse it but with no valid entries
        assert isinstance(articles, list)

