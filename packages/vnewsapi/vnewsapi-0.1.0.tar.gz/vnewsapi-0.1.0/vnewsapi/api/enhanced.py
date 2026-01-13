"""
Enhanced high-level API for vnewsapi.
"""

from typing import Optional, Dict, Any, List
import pandas as pd
from vnewsapi.core.crawler import Crawler
from vnewsapi.core.batch import BatchCrawler
from vnewsapi.utils.logger import get_logger

logger = get_logger(__name__)


class EnhancedNewsCrawler:
    """
    Enhanced high-level API wrapper for news crawling.
    
    Provides convenient methods for common use cases.
    """
    
    def __init__(
        self,
        site_name: str,
        request_delay: float = 0.5,
        timeout: int = 30,
        custom_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize enhanced crawler.
        
        Args:
            site_name (str): Name of the news site
            request_delay (float): Delay between batch requests
            timeout (int): Request timeout
            custom_config (Optional[Dict[str, Any]]): Custom configuration
        """
        self.site_name = site_name
        self.crawler = Crawler(site_name, custom_config=custom_config, timeout=timeout)
        self.batch_crawler = BatchCrawler(
            site_name,
            request_delay=request_delay,
            timeout=timeout,
            custom_config=custom_config
        )
    
    def get_latest_articles(
        self,
        limit: int = 20,
        with_details: bool = False
    ) -> pd.DataFrame:
        """
        Get latest articles from the news site.
        
        Args:
            limit (int): Number of articles to fetch
            with_details (bool): If True, fetch full article details
            
        Returns:
            pd.DataFrame: DataFrame with articles
        """
        # Get article list
        articles_df = self.crawler.get_articles(limit=limit)
        
        if with_details and not articles_df.empty:
            # Fetch details for all articles
            articles_df = self.batch_crawler.fetch_details_from_dataframe(
                articles_df,
                url_column='link'
            )
        
        return articles_df
    
    def search_articles(
        self,
        keyword: str,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Search articles by keyword (filters by title/description).
        
        Args:
            keyword (str): Search keyword
            limit (Optional[int]): Maximum results
            
        Returns:
            pd.DataFrame: Filtered articles DataFrame
        """
        # Get all articles
        articles_df = self.crawler.get_articles(limit=None)
        
        if articles_df.empty:
            return articles_df
        
        # Filter by keyword
        keyword_lower = keyword.lower()
        title_mask = articles_df['title'].str.lower().str.contains(keyword_lower, na=False)
        desc_series = articles_df.get('description', pd.Series(dtype=str))
        desc_mask = desc_series.str.lower().str.contains(keyword_lower, na=False) if not desc_series.empty else pd.Series([False] * len(articles_df))
        mask = title_mask | desc_mask
        filtered_df = articles_df[mask]
        
        if limit:
            filtered_df = filtered_df.head(limit)
        
        return filtered_df

