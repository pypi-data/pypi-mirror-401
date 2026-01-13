"""
HTML parsing utilities for vnewsapi.
Adapted from vnstock transform.py.
"""

from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import html2text


def parse_html(html_content: str, parser: str = 'lxml') -> BeautifulSoup:
    """
    Parse HTML content with BeautifulSoup.

    Args:
        html_content (str): HTML content to parse
        parser (str): Parser to use ('lxml', 'html.parser', 'html5lib')

    Returns:
        BeautifulSoup: Parsed BeautifulSoup object
    """
    return BeautifulSoup(html_content, parser)


def extract_text(soup: BeautifulSoup, selector_config: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Extract text from HTML element using selector configuration.

    Args:
        soup (BeautifulSoup): BeautifulSoup object
        selector_config (Optional[Dict[str, Any]]): Selector config with keys:
            - tag: HTML tag name (e.g., 'h1', 'div')
            - class: CSS class name
            - id: Element ID
            - selector: CSS selector string (takes precedence)

    Returns:
        Optional[str]: Extracted text or None if not found
    """
    if not selector_config:
        return None

    try:
        # If CSS selector is provided, use it directly
        if 'selector' in selector_config:
            element = soup.select_one(selector_config['selector'])
            if element:
                return element.get_text(strip=True)
            return None

        # Otherwise, build selector from tag, class, id
        tag = selector_config.get('tag', 'div')
        class_name = selector_config.get('class')
        element_id = selector_config.get('id')

        # Build CSS selector
        selector = tag
        if element_id:
            selector = f"{tag}#{element_id}"
        elif class_name:
            selector = f"{tag}.{class_name}"

        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
        return None
    except Exception:
        return None


def html_to_markdown(html_content: str, ignore_links: bool = False) -> str:
    """
    Convert HTML content to Markdown format.

    Args:
        html_content (str): HTML content to convert
        ignore_links (bool): Whether to ignore links in conversion

    Returns:
        str: Markdown formatted content
    """
    h = html2text.HTML2Text()
    h.ignore_links = ignore_links
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    return h.handle(html_content)


def clean_html_text(html_content: str) -> str:
    """
    Clean HTML content and extract plain text.

    Args:
        html_content (str): HTML content to clean

    Returns:
        str: Cleaned plain text
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Normalize whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

