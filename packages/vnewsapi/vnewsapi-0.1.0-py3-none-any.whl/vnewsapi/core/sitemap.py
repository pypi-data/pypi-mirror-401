"""
Sitemap parser for vnewsapi.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import pandas as pd
from urllib.parse import urljoin, urlparse
from vnewsapi.core.base import BaseParser
from vnewsapi.utils.client import send_request
from vnewsapi.utils.user_agent import get_headers
from vnewsapi.utils.logger import get_logger
from vnewsapi.exceptions import SitemapParseError, NetworkError

logger = get_logger(__name__)


class Sitemap(BaseParser):
    """
    Sitemap parser.
    
    Fetches and parses XML sitemaps to extract article URLs.
    Supports both regular sitemaps and sitemap index files.
    """
    
    def __init__(self, timeout: int = 30, data_source: str = 'CAFEF'):
        """
        Initialize Sitemap parser.
        
        Args:
            timeout (int): Request timeout in seconds
            data_source (str): Data source name for headers
        """
        super().__init__(timeout)
        self.data_source = data_source
    
    def _fetch_sitemap(self, sitemap_url: str) -> str:
        """
        Fetch sitemap content from URL.
        
        Args:
            sitemap_url (str): Sitemap URL
            
        Returns:
            str: Sitemap XML content
            
        Raises:
            NetworkError: If network request fails
        """
        try:
            logger.info(f"Fetching sitemap: {sitemap_url}")
            headers = get_headers(data_source=self.data_source)
            
            response = send_request(
                url=sitemap_url,
                headers=headers,
                method="GET",
                timeout=self.timeout,
                request_mode="direct"
            )
            
            if isinstance(response, bytes):
                return response.decode('utf-8')
            elif isinstance(response, str):
                return response
            else:
                raise SitemapParseError(f"Unexpected response type: {type(response)}")
                
        except NetworkError as e:
            logger.error(f"Network error fetching sitemap: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching sitemap: {e}")
            raise NetworkError(f"Failed to fetch sitemap: {e}")
    
    def _parse_sitemap(self, sitemap_content: str, base_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Parse sitemap XML content.
        
        Args:
            sitemap_content (str): Sitemap XML content
            base_url (Optional[str]): Base URL for resolving relative URLs
            
        Returns:
            List[Dict[str, Any]]: List of URL dictionaries with keys:
                - loc: URL location
                - lastmod: Last modification date (ISO format)
                
        Raises:
            SitemapParseError: If parsing fails
        """
        try:
            root = ET.fromstring(sitemap_content)
            
            # Check if this is a sitemap index
            if root.tag.endswith('sitemapindex') or 'sitemapindex' in root.tag:
                logger.info("Detected sitemap index, fetching child sitemaps...")
                sitemap_urls = []
                for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                    loc_elem = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc_elem is not None and loc_elem.text:
                        sitemap_urls.append(loc_elem.text)
                
                # Fetch and parse each child sitemap
                all_urls = []
                for sitemap_url in sitemap_urls:
                    try:
                        child_content = self._fetch_sitemap(sitemap_url)
                        urls = self._parse_sitemap(child_content, base_url)
                        all_urls.extend(urls)
                    except Exception as e:
                        logger.warning(f"Error fetching child sitemap {sitemap_url}: {e}")
                        continue
                
                return all_urls
            
            # Regular sitemap
            urls = []
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                lastmod_elem = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
                
                if loc_elem is not None and loc_elem.text:
                    url_dict = {
                        'loc': loc_elem.text,
                        'lastmod': self._normalize_date(lastmod_elem.text if lastmod_elem is not None else None)
                    }
                    urls.append(url_dict)
            
            logger.info(f"Successfully parsed {len(urls)} URLs from sitemap")
            return urls
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            raise SitemapParseError(f"Failed to parse sitemap XML: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing sitemap: {e}")
            raise SitemapParseError(f"Unexpected error: {e}")
    
    def run(self, sitemap_url: str, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Fetch and parse sitemap, return as DataFrame.
        
        Args:
            sitemap_url (str): Sitemap URL
            limit (Optional[int]): Maximum number of URLs to return
            
        Returns:
            pd.DataFrame: DataFrame with columns 'loc' and 'lastmod'
            
        Raises:
            SitemapParseError: If parsing fails
            NetworkError: If network request fails
        """
        try:
            # Extract base URL from sitemap URL
            parsed = urlparse(sitemap_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Fetch and parse
            sitemap_content = self._fetch_sitemap(sitemap_url)
            urls = self._parse_sitemap(sitemap_content, base_url)
            
            # Apply limit if specified
            if limit is not None and limit > 0:
                urls = urls[:limit]
            
            # Convert to DataFrame
            df = pd.DataFrame(urls)
            
            if df.empty:
                logger.warning("Sitemap returned no URLs")
            else:
                logger.info(f"Returning {len(df)} URLs from sitemap")
            
            return df
            
        except (SitemapParseError, NetworkError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Sitemap.run: {e}")
            raise SitemapParseError(f"Unexpected error: {e}")
    
    def parse(self, source: str) -> List[Dict[str, Any]]:
        """
        Parse sitemap (alias for run, returns list instead of DataFrame).
        
        Args:
            source (str): Sitemap URL
            
        Returns:
            List[Dict[str, Any]]: List of URL dictionaries
        """
        df = self.run(source)
        return df.to_dict('records')

