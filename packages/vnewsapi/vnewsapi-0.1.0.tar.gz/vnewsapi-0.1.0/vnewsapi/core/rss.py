"""
RSS feed parser for vnewsapi.
"""

import feedparser
from typing import List, Dict, Any, Optional
from datetime import datetime
from vnewsapi.core.base import BaseParser
from vnewsapi.utils.client import send_request
from vnewsapi.utils.user_agent import get_headers
from vnewsapi.utils.logger import get_logger
from vnewsapi.exceptions import RSSParseError, NetworkError

logger = get_logger(__name__)


class RSS(BaseParser):
    """
    RSS feed parser.
    
    Fetches and parses RSS feeds to extract article information.
    """
    
    def __init__(self, timeout: int = 30, data_source: str = 'CAFEF'):
        """
        Initialize RSS parser.
        
        Args:
            timeout (int): Request timeout in seconds
            data_source (str): Data source name for headers
        """
        super().__init__(timeout)
        self.data_source = data_source
    
    def fetch(self, rss_url: str) -> List[Dict[str, Any]]:
        """
        Fetch and parse RSS feed.
        
        Args:
            rss_url (str): RSS feed URL
            
        Returns:
            List[Dict[str, Any]]: List of article dictionaries with keys:
                - title: Article title
                - link: Article URL
                - pubDate: Publication date (ISO format)
                - description: Article description/summary
                
        Raises:
            RSSParseError: If RSS parsing fails
            NetworkError: If network request fails
        """
        try:
            logger.info(f"Fetching RSS feed: {rss_url}")
            
            # Get headers
            headers = get_headers(data_source=self.data_source)
            
            # Fetch RSS feed
            try:
                response = send_request(
                    url=rss_url,
                    headers=headers,
                    method="GET",
                    timeout=self.timeout,
                    request_mode="direct"
                )
                
                # If response is bytes, decode to string
                if isinstance(response, bytes):
                    rss_content = response.decode('utf-8')
                elif isinstance(response, str):
                    rss_content = response
                else:
                    raise RSSParseError(f"Unexpected response type: {type(response)}")
                    
            except NetworkError as e:
                logger.error(f"Network error fetching RSS: {e}")
                raise
            except Exception as e:
                logger.error(f"Error fetching RSS feed: {e}")
                raise NetworkError(f"Failed to fetch RSS feed: {e}")
            
            # Parse RSS with feedparser
            try:
                feed = feedparser.parse(rss_content)
            except Exception as e:
                logger.error(f"Error parsing RSS content: {e}")
                raise RSSParseError(f"Failed to parse RSS feed: {e}")
            
            # Check for parsing errors
            if feed.bozo and feed.bozo_exception:
                logger.warning(f"RSS parsing warning: {feed.bozo_exception}")
                # Continue anyway if we have entries
            
            # Extract articles
            articles = []
            for entry in feed.entries:
                try:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'pubDate': self._normalize_date(entry.get('published', entry.get('updated', ''))),
                        'description': entry.get('description', entry.get('summary', '')),
                    }
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Error processing RSS entry: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(articles)} articles from RSS feed")
            return articles
            
        except (RSSParseError, NetworkError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in RSS.fetch: {e}")
            raise RSSParseError(f"Unexpected error: {e}")
    
    def parse(self, source: str) -> List[Dict[str, Any]]:
        """
        Parse RSS feed (alias for fetch).
        
        Args:
            source (str): RSS feed URL
            
        Returns:
            List[Dict[str, Any]]: List of article dictionaries
        """
        return self.fetch(source)

