"""
High-level API modules for vnewsapi.
"""

try:
    from vnewsapi.api.enhanced import EnhancedNewsCrawler
    __all__ = ["EnhancedNewsCrawler"]
except ImportError:
    __all__ = []

