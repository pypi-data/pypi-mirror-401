"""
Unit tests for utility modules.
"""

import pytest
from unittest.mock import Mock, patch
from vnewsapi.utils.parser import parse_html, extract_text, html_to_markdown
from vnewsapi.utils.user_agent import get_headers
from vnewsapi.utils.cleaner import clean_content, normalize_whitespace


class TestParser:
    """Test cases for HTML parser utilities."""
    
    def test_parse_html(self):
        """Test HTML parsing."""
        html = "<html><body><h1>Test</h1></body></html>"
        soup = parse_html(html)
        assert soup is not None
        h1_element = soup.find('h1')
        assert h1_element is not None
        assert h1_element.text == 'Test'
    
    def test_extract_text_with_selector(self):
        """Test text extraction with CSS selector."""
        html = "<html><body><h1 class='title'>Test Title</h1></body></html>"
        soup = parse_html(html)
        selector = {'tag': 'h1', 'class': 'title'}
        text = extract_text(soup, selector)
        assert text == 'Test Title'
    
    def test_html_to_markdown(self):
        """Test HTML to Markdown conversion."""
        html = "<h1>Title</h1><p>Content</p>"
        markdown = html_to_markdown(html)
        assert 'Title' in markdown
        assert 'Content' in markdown


class TestUserAgent:
    """Test cases for user agent utilities."""
    
    def test_get_headers_default(self):
        """Test getting default headers."""
        headers = get_headers()
        assert 'User-Agent' in headers
        assert 'Accept' in headers
    
    def test_get_headers_custom_source(self):
        """Test getting headers for custom source."""
        headers = get_headers(data_source='CAFEF')
        assert 'User-Agent' in headers


class TestCleaner:
    """Test cases for content cleaner utilities."""
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "  Test    text  \n\n  with   spaces  "
        normalized = normalize_whitespace(text)
        assert '  ' not in normalized
        assert normalized.strip() == normalized
    
    def test_clean_content(self):
        """Test content cleaning."""
        html = "<html><body><script>alert('test')</script><p>Content</p></body></html>"
        cleaned = clean_content(html)
        assert 'script' not in cleaned.lower()
        assert 'Content' in cleaned

