"""
vnewsapi - Vietnamese News API
A Python library for crawling Vietnamese financial news from major news websites.

Features:
- RSS feed parsing
- Sitemap parsing
- Content extraction with CSS selectors
- Batch crawling support
- Multiple news sources support
"""

__version__ = "0.1.0"

# Core modules
from vnewsapi.core.crawler import Crawler
from vnewsapi.core.batch import BatchCrawler
from vnewsapi.core.rss import RSS
from vnewsapi.core.sitemap import Sitemap

# High-level API (optional)
try:
    from vnewsapi.api.enhanced import EnhancedNewsCrawler
    __all__ = [
        "Crawler",
        "BatchCrawler",
        "RSS",
        "Sitemap",
        "EnhancedNewsCrawler",
    ]
except ImportError:
    __all__ = [
        "Crawler",
        "BatchCrawler",
        "RSS",
        "Sitemap",
    ]

