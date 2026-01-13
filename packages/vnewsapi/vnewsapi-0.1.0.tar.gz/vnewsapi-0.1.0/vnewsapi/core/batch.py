"""
Batch crawler for vnewsapi.
"""

import time
import pandas as pd
from typing import List, Dict, Any, Optional
from vnewsapi.core.crawler import Crawler
from vnewsapi.utils.logger import get_logger
from vnewsapi.exceptions import CrawlerError

logger = get_logger(__name__)


class BatchCrawler:
    """
    Batch crawler for fetching multiple article details.
    
    Manages request delays, progress tracking, and error handling
    for bulk article fetching.
    """
    
    def __init__(
        self,
        site_name: str,
        request_delay: float = 0.5,
        timeout: int = 30,
        custom_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize batch crawler.
        
        Args:
            site_name (str): Name of the news site
            request_delay (float): Delay between requests in seconds
            timeout (int): Request timeout in seconds
            custom_config (Optional[Dict[str, Any]]): Custom configuration override
        """
        self.site_name = site_name
        self.request_delay = request_delay
        self.crawler = Crawler(site_name, custom_config=custom_config, timeout=timeout)
        logger.info(f"Initialized BatchCrawler for site: {site_name} (delay: {request_delay}s)")
    
    def fetch_details_for_urls(
        self,
        urls: List[str],
        show_progress: bool = True
    ) -> pd.DataFrame:
        """
        Fetch detailed content for multiple article URLs.
        
        Args:
            urls (List[str]): List of article URLs
            show_progress (bool): Whether to log progress
            
        Returns:
            pd.DataFrame: DataFrame with article details, including:
                - url: Article URL
                - title: Article title
                - content: Article content (Markdown)
                - content_html: Article content (HTML)
                - short_desc: Article summary
                - publish_time: Publication time
                - author: Article author
                - error: Error message if fetch failed
                
        Raises:
            CrawlerError: If all fetches fail
        """
        if not urls:
            logger.warning("No URLs provided")
            return pd.DataFrame()
        
        results = []
        total = len(urls)
        successful = 0
        failed = 0
        
        logger.info(f"Starting batch fetch for {total} URLs...")
        
        for idx, url in enumerate(urls, 1):
            try:
                if show_progress:
                    logger.info(f"Processing {idx}/{total}: {url}")
                
                # Fetch article details
                article_details = self.crawler.get_article_details(url)
                article_details['error'] = None
                results.append(article_details)
                successful += 1
                
                # Delay between requests
                if idx < total and self.request_delay > 0:
                    time.sleep(self.request_delay)
                    
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Failed to fetch {url}: {error_msg}")
                results.append({
                    'url': url,
                    'title': None,
                    'content': None,
                    'content_html': None,
                    'short_desc': None,
                    'publish_time': None,
                    'author': None,
                    'error': error_msg
                })
                failed += 1
                
                # Still delay even on error
                if idx < total and self.request_delay > 0:
                    time.sleep(self.request_delay)
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        logger.info(
            f"Batch fetch completed: {successful} successful, {failed} failed "
            f"out of {total} URLs"
        )
        
        if df.empty:
            logger.warning("No articles were successfully fetched")
        elif successful == 0:
            raise CrawlerError("All article fetches failed")
        
        return df
    
    def fetch_details_from_dataframe(
        self,
        df: pd.DataFrame,
        url_column: str = 'link',
        show_progress: bool = True
    ) -> pd.DataFrame:
        """
        Fetch detailed content for URLs from a DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame containing article URLs
            url_column (str): Name of the column containing URLs
            show_progress (bool): Whether to log progress
            
        Returns:
            pd.DataFrame: DataFrame with article details merged with original data
        """
        if df.empty:
            logger.warning("Input DataFrame is empty")
            return pd.DataFrame()
        
        if url_column not in df.columns:
            raise ValueError(f"Column '{url_column}' not found in DataFrame")
        
        urls = df[url_column].dropna().tolist()
        
        if not urls:
            logger.warning(f"No valid URLs found in column '{url_column}'")
            return df
        
        # Fetch details
        details_df = self.fetch_details_for_urls(urls, show_progress=show_progress)
        
        # Merge with original DataFrame
        merged_df = df.merge(
            details_df,
            left_on=url_column,
            right_on='url',
            how='left',
            suffixes=('', '_detail')
        )
        
        return merged_df

