"""
Utility modules for vnewsapi.
"""

from vnewsapi.utils.client import send_request, send_request_direct
from vnewsapi.utils.user_agent import get_headers
from vnewsapi.utils.logger import setup_logger, get_logger
from vnewsapi.utils.parser import parse_html, html_to_markdown

__all__ = [
    "send_request",
    "send_request_direct",
    "get_headers",
    "setup_logger",
    "get_logger",
    "parse_html",
    "html_to_markdown",
]

