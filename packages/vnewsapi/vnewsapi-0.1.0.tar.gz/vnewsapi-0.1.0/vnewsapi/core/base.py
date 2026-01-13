"""
Base classes and interfaces for vnewsapi core modules.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Protocol
from datetime import datetime
import pandas as pd


class IParser(Protocol):
    """Interface for RSS and Sitemap parsers."""
    
    @abstractmethod
    def parse(self, source: str) -> List[Dict[str, Any]]:
        """
        Parse source (RSS feed or Sitemap) and return list of articles.
        
        Args:
            source (str): RSS feed URL or Sitemap URL
            
        Returns:
            List[Dict[str, Any]]: List of article dictionaries
        """
        pass


class IContentExtractor(Protocol):
    """Interface for content extraction from HTML."""
    
    @abstractmethod
    def extract(self, html: str, selectors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract content from HTML using selectors.
        
        Args:
            html (str): HTML content
            selectors (Dict[str, Any]): Selector configuration
            
        Returns:
            Dict[str, Any]: Extracted content dictionary
        """
        pass


class BaseParser(ABC):
    """Abstract base class for RSS and Sitemap parsers."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize parser.
        
        Args:
            timeout (int): Request timeout in seconds
        """
        self.timeout = timeout
    
    @abstractmethod
    def parse(self, source: str) -> List[Dict[str, Any]]:
        """
        Parse source and return list of articles.
        
        Args:
            source (str): Source URL
            
        Returns:
            List[Dict[str, Any]]: List of article dictionaries
        """
        pass
    
    def _normalize_date(self, date_str: Optional[str]) -> Optional[str]:
        """
        Normalize date string to ISO format.
        
        Args:
            date_str (Optional[str]): Date string to normalize
            
        Returns:
            Optional[str]: Normalized date string in ISO format
        """
        if not date_str:
            return None
        
        try:
            from dateutil import parser as date_parser
            dt = date_parser.parse(date_str)
            return dt.isoformat()
        except Exception:
            return date_str


class BaseContentExtractor(ABC):
    """Abstract base class for content extraction."""
    
    @abstractmethod
    def extract(self, html: str, selectors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract content from HTML using selectors.
        
        Args:
            html (str): HTML content
            selectors (Dict[str, Any]): Selector configuration
            
        Returns:
            Dict[str, Any]: Extracted content dictionary
        """
        pass


class BaseCrawler(ABC):
    """Abstract base class for crawlers."""
    
    def __init__(self, site_name: str, custom_config: Optional[Dict[str, Any]] = None):
        """
        Initialize crawler.
        
        Args:
            site_name (str): Name of the news site
            custom_config (Optional[Dict[str, Any]]): Custom configuration override
        """
        self.site_name = site_name
        self.custom_config = custom_config
    
    @abstractmethod
    def get_articles(self, limit: Optional[int] = None, **kwargs) -> pd.DataFrame:
        """
        Get list of articles.
        
        Args:
            limit (Optional[int]): Maximum number of articles to fetch
            
        Returns:
            pd.DataFrame: DataFrame with article list
        """
        pass
    
    @abstractmethod
    def get_article_details(self, url: str) -> Dict[str, Any]:
        """
        Get detailed content of a single article.
        
        Args:
            url (str): Article URL
            
        Returns:
            Dict[str, Any]: Article details dictionary
        """
        pass

