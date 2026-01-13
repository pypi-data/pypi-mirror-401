"""
Pytest configuration and fixtures for vnewsapi tests.
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_rss_feed() -> str:
    """Sample RSS feed XML for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test News Feed</title>
        <link>https://example.com</link>
        <description>Test feed description</description>
        <item>
            <title>Test Article 1</title>
            <link>https://example.com/article1</link>
            <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
            <description>Test article description 1</description>
        </item>
        <item>
            <title>Test Article 2</title>
            <link>https://example.com/article2</link>
            <pubDate>Tue, 02 Jan 2024 12:00:00 +0000</pubDate>
            <description>Test article description 2</description>
        </item>
    </channel>
</rss>"""


@pytest.fixture
def sample_sitemap() -> str:
    """Sample sitemap XML for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
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


@pytest.fixture
def sample_html() -> str:
    """Sample HTML page for testing."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Test Article</title>
</head>
<body>
    <h1 class="title">Test Article Title</h1>
    <div class="sapo">Test article summary</div>
    <div class="detail-content">
        <p>Test article content paragraph 1.</p>
        <p>Test article content paragraph 2.</p>
    </div>
    <span class="time">2024-01-01 12:00:00</span>
    <span class="author">Test Author</span>
</body>
</html>"""


@pytest.fixture
def sample_site_config() -> Dict[str, Any]:
    """Sample site configuration for testing."""
    return {
        "name": "Test Site",
        "base_url": "https://example.com",
        "rss": {
            "urls": ["https://example.com/rss"]
        },
        "sitemap": {
            "url": "https://example.com/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    }

