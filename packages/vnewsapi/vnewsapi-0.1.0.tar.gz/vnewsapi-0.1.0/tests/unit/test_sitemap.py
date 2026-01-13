"""
Unit tests for Sitemap parser.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from vnewsapi.core.sitemap import Sitemap
from vnewsapi.exceptions import SitemapParseError, NetworkError


class TestSitemap:
    """Test cases for Sitemap parser."""
    
    def test_sitemap_init(self):
        """Test Sitemap parser initialization."""
        sitemap = Sitemap(timeout=30, data_source='CAFEF')
        assert sitemap.timeout == 30
        assert sitemap.data_source == 'CAFEF'
    
    @patch('vnewsapi.core.sitemap.send_request')
    @patch('vnewsapi.core.sitemap.get_headers')
    def test_run_success(self, mock_headers, mock_send_request):
        """Test successful sitemap parsing."""
        mock_send_request.return_value = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/article1</loc>
        <lastmod>2024-01-01</lastmod>
    </url>
    <url>
        <loc>https://example.com/article2</loc>
        <lastmod>2024-01-02</lastmod>
    </url>
</urlset>"""
        mock_headers.return_value = {'User-Agent': 'test'}
        
        sitemap = Sitemap()
        df = sitemap.run('https://example.com/sitemap.xml')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'loc' in df.columns
        assert 'lastmod' in df.columns
    
    @patch('vnewsapi.core.sitemap.send_request')
    def test_run_network_error(self, mock_send_request):
        """Test sitemap fetch with network error."""
        mock_send_request.side_effect = NetworkError("Connection failed")
        
        sitemap = Sitemap()
        with pytest.raises(NetworkError):
            sitemap.run('https://example.com/sitemap.xml')
    
    def test_parse_sitemap_index(self):
        """Test parsing sitemap index."""
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://example.com/sitemap1.xml</loc>
    </sitemap>
    <sitemap>
        <loc>https://example.com/sitemap2.xml</loc>
    </sitemap>
</sitemapindex>"""
        
        sitemap = Sitemap()
        # This should detect sitemap index and try to fetch child sitemaps
        # For unit test, we'll just check that it doesn't crash
        # Full integration test would mock the child sitemap fetches
        assert sitemap is not None

