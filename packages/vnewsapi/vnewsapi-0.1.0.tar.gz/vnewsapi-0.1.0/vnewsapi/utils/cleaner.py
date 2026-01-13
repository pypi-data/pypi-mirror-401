"""
Content cleaning utilities for vnewsapi.
"""

import re
from bs4 import BeautifulSoup
from typing import Optional


def remove_ads(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove common ad elements from HTML.

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        BeautifulSoup: Cleaned BeautifulSoup object
    """
    # Remove common ad classes/ids
    ad_selectors = [
        '[class*="ad"]',
        '[id*="ad"]',
        '[class*="advertisement"]',
        '[id*="advertisement"]',
        '[class*="banner"]',
        '[class*="sponsor"]',
    ]
    
    for selector in ad_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    return soup


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text (str): Text to normalize

    Returns:
        str: Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with double newline
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Strip leading/trailing whitespace
    return text.strip()


def clean_special_characters(text: str) -> str:
    """
    Clean special characters from text.

    Args:
        text (str): Text to clean

    Returns:
        str: Cleaned text
    """
    # Remove zero-width characters
    text = re.sub(r'[\u200b-\u200f\u2028-\u202f]', '', text)
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    return text


def clean_content(html_content: str, remove_ads_flag: bool = True) -> str:
    """
    Clean HTML content comprehensively.

    Args:
        html_content (str): HTML content to clean
        remove_ads_flag (bool): Whether to remove ads

    Returns:
        str: Cleaned text content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style
    for element in soup(['script', 'style', 'noscript', 'iframe']):
        element.decompose()
    
    # Remove ads if requested
    if remove_ads_flag:
        soup = remove_ads(soup)
    
    # Get text
    text = soup.get_text()
    
    # Normalize
    text = normalize_whitespace(text)
    text = clean_special_characters(text)
    
    return text

