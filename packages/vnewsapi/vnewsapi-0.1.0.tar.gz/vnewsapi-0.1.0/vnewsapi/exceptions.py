"""
Custom exceptions for vnewsapi library.
"""


class VNewsAPIError(Exception):
    """Base exception for all vnewsapi errors."""
    pass


class CrawlerError(VNewsAPIError):
    """Base exception for crawler-related errors."""
    pass


class RSSParseError(CrawlerError):
    """Raised when RSS parsing fails."""
    pass


class SitemapParseError(CrawlerError):
    """Raised when Sitemap parsing fails."""
    pass


class ContentExtractionError(CrawlerError):
    """Raised when content extraction fails."""
    pass


class NetworkError(VNewsAPIError):
    """Raised when network/HTTP requests fail."""
    pass


class ConfigurationError(VNewsAPIError):
    """Raised when configuration is invalid."""
    pass

