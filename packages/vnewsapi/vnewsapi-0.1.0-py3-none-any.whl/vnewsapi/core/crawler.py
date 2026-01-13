"""
Main crawler class for vnewsapi.
"""

import pandas as pd
from typing import Dict, Any, Optional, List
from vnewsapi.core.base import BaseCrawler
from vnewsapi.core.rss import RSS
from vnewsapi.core.sitemap import Sitemap
from vnewsapi.config.sites import get_site_config, SITES_CONFIG
from vnewsapi.utils.client import send_request
from vnewsapi.utils.user_agent import get_headers
from vnewsapi.utils.parser import parse_html, extract_text, html_to_markdown
from vnewsapi.utils.cleaner import clean_content
from vnewsapi.utils.logger import get_logger
from vnewsapi.exceptions import CrawlerError, ConfigurationError, NetworkError

logger = get_logger(__name__)


class Crawler(BaseCrawler):
    """
    Main crawler class for fetching news articles.
    
    Supports both RSS and Sitemap sources, with automatic detection
    and content extraction using CSS selectors.
    """
    
    def __init__(
        self,
        site_name: str,
        custom_config: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ):
        """
        Initialize crawler.
        
        Args:
            site_name (str): Name of the news site (e.g., 'cafef', 'vietstock')
            custom_config (Optional[Dict[str, Any]]): Custom configuration override
            timeout (int): Request timeout in seconds
        """
        super().__init__(site_name, custom_config)
        self.timeout = timeout
        
        # Load site configuration
        try:
            if custom_config:
                self.config = custom_config
            else:
                self.config = get_site_config(site_name)
        except KeyError as e:
            raise ConfigurationError(str(e))
        
        # Initialize parsers
        self.rss_parser = RSS(timeout=timeout, data_source=site_name.upper())
        self.sitemap_parser = Sitemap(timeout=timeout, data_source=site_name.upper())
        
        logger.info(f"Initialized Crawler for site: {self.config['name']}")
    
    def get_articles(
        self,
        limit: Optional[int] = None,
        sitemap_url: Optional[str] = None,
        rss_url: Optional[str] = None,
        prefer_rss: bool = True
    ) -> pd.DataFrame:
        """
        Get list of articles from the news site.
        
        Args:
            limit (Optional[int]): Maximum number of articles to fetch
            sitemap_url (Optional[str]): Override sitemap URL from config
            rss_url (Optional[str]): Override RSS URL from config
            prefer_rss (bool): If True, prefer RSS over Sitemap
            
        Returns:
            pd.DataFrame: DataFrame with columns:
                - title: Article title
                - link: Article URL
                - pubDate: Publication date
                - description: Article description
                
        Raises:
            CrawlerError: If fetching fails
        """
        try:
            articles = []
            
            # Try RSS first if preferred and available
            if prefer_rss:
                rss_urls = rss_url or self.config.get('rss', {}).get('urls', [])
                if rss_urls:
                    try:
                        logger.info(f"Fetching articles from RSS: {rss_urls[0]}")
                        articles = self.rss_parser.fetch(rss_urls[0])
                        if articles:
                            logger.info(f"Successfully fetched {len(articles)} articles from RSS")
                            df = pd.DataFrame(articles)
                            if limit:
                                df = df.head(limit)
                            return df
                    except Exception as e:
                        logger.warning(f"RSS fetch failed: {e}, trying sitemap...")
            
            # Fallback to sitemap
            sitemap_url = sitemap_url or self.config.get('sitemap', {}).get('url')
            if sitemap_url:
                try:
                    logger.info(f"Fetching articles from sitemap: {sitemap_url}")
                    df = self.sitemap_parser.run(sitemap_url, limit=limit)
                    if not df.empty:
                        # Convert sitemap format to article format
                        df = df.rename(columns={'loc': 'link', 'lastmod': 'pubDate'})
                        df['title'] = ''
                        df['description'] = ''
                        logger.info(f"Successfully fetched {len(df)} URLs from sitemap")
                        return df
                except Exception as e:
                    logger.error(f"Sitemap fetch failed: {e}")
                    raise CrawlerError(f"Failed to fetch articles: {e}")
            
            # If RSS was not preferred, try it now
            if not prefer_rss:
                rss_urls = rss_url or self.config.get('rss', {}).get('urls', [])
                if rss_urls:
                    try:
                        logger.info(f"Fetching articles from RSS: {rss_urls[0]}")
                        articles = self.rss_parser.fetch(rss_urls[0])
                        if articles:
                            df = pd.DataFrame(articles)
                            if limit:
                                df = df.head(limit)
                            return df
                    except Exception as e:
                        logger.warning(f"RSS fetch failed: {e}")
            
            raise CrawlerError("No valid RSS or Sitemap source available")
            
        except Exception as e:
            logger.error(f"Error in get_articles: {e}")
            if isinstance(e, CrawlerError):
                raise
            raise CrawlerError(f"Unexpected error: {e}")
    
    def get_article_details(self, url: str) -> Dict[str, Any]:
        """
        Get detailed content of a single article.
        
        Args:
            url (str): Article URL
            
        Returns:
            Dict[str, Any]: Article details dictionary with keys:
                - title: Article title
                - content: Full article content (Markdown format)
                - content_html: Full article content (HTML format)
                - short_desc: Article summary/description
                - publish_time: Publication time
                - author: Article author
                - url: Article URL
                
        Raises:
            CrawlerError: If extraction fails
            NetworkError: If network request fails
        """
        try:
            logger.info(f"Fetching article details: {url}")
            
            # Get headers
            headers = get_headers(data_source=self.site_name.upper())
            
            # Fetch article HTML
            try:
                response = send_request(
                    url=url,
                    headers=headers,
                    method="GET",
                    timeout=self.timeout,
                    request_mode="direct"
                )
                
                if isinstance(response, bytes):
                    html_content = response.decode('utf-8', errors='ignore')
                elif isinstance(response, str):
                    html_content = response
                else:
                    raise CrawlerError(f"Unexpected response type: {type(response)}")
                    
            except NetworkError as e:
                logger.error(f"Network error fetching article: {e}")
                raise
            except Exception as e:
                logger.error(f"Error fetching article: {e}")
                raise NetworkError(f"Failed to fetch article: {e}")
            
            # Parse HTML
            soup = parse_html(html_content)
            
            # Get selectors from config
            selectors = self.config.get('selectors', {})
            
            # Extract content using selectors
            article_details = {
                'url': url,
                'title': extract_text(soup, selectors.get('title', {})),
                'short_desc': extract_text(soup, selectors.get('short_desc', {})),
                'publish_time': extract_text(soup, selectors.get('publish_time', {})),
                'author': extract_text(soup, selectors.get('author', {})),
            }
            
            # Extract main content
            content_selector = selectors.get('content', {})
            if content_selector:
                content_element = None
                if 'selector' in content_selector:
                    content_element = soup.select_one(content_selector['selector'])
                else:
                    tag = content_selector.get('tag', 'div')
                    class_name = content_selector.get('class')
                    if class_name:
                        content_element = soup.select_one(f"{tag}.{class_name}")
                    else:
                        content_element = soup.find(tag)
                
                if content_element:
                    # Get HTML content
                    article_details['content_html'] = str(content_element)
                    # Convert to Markdown
                    article_details['content'] = html_to_markdown(str(content_element))
                else:
                    logger.warning("Content element not found, using fallback")
                    article_details['content_html'] = ''
                    article_details['content'] = clean_content(html_content)
            else:
                # Fallback: clean entire HTML
                article_details['content_html'] = html_content
                article_details['content'] = clean_content(html_content)
            
            logger.info(f"Successfully extracted article details: {article_details.get('title', 'N/A')}")
            return article_details
            
        except (CrawlerError, NetworkError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_article_details: {e}")
            raise CrawlerError(f"Unexpected error: {e}")

