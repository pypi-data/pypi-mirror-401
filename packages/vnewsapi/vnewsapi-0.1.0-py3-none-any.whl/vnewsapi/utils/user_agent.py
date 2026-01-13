"""
User agent management for vnewsapi.
Adapted from vnstock.
"""

import random
from typing import Optional, Dict
from vnewsapi.utils.browser_profiles import USER_AGENTS

DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
}


# Source-specific headers for news websites
HEADERS_MAPPING_SOURCE = {
    'CAFEF': {
        'Referer': 'https://cafef.vn/',
        'Origin': 'https://cafef.vn'
    },
    'VIETSTOCK': {
        'Referer': 'https://vietstock.vn/',
        'Origin': 'https://vietstock.vn'
    },
    'VNEXPRESS': {
        'Referer': 'https://vnexpress.net/',
        'Origin': 'https://vnexpress.net'
    },
    'BAODAUTU': {
        'Referer': 'https://baodautu.vn/',
        'Origin': 'https://baodautu.vn'
    },
    'TUOITRE': {
        'Referer': 'https://tuoitre.vn/',
        'Origin': 'https://tuoitre.vn'
    },
}


def get_headers(
    data_source: str = 'CAFEF',
    random_agent: bool = True,
    browser: str = 'chrome',
    platform: str = 'windows',
    custom_headers: Optional[Dict[str, str]] = None,
    override_headers: Optional[Dict[str, str]] = None,
    include_defaults: bool = True
) -> Dict[str, str]:
    """
    Generate browser-like headers with optional referer/origin and realistic User-Agent.

    Args:
        data_source (str): Predefined data source (e.g., 'CAFEF', 'VIETSTOCK', 'VNEXPRESS').
        random_agent (bool): Whether to use a random browser/platform User-Agent.
        browser (str): Browser name to simulate if not random.
        platform (str): Platform name to simulate if not random.
        custom_headers (Optional[Dict[str, str]]): Additional custom headers to merge.
        override_headers (Optional[Dict[str, str]]): Headers to override (highest priority).
        include_defaults (bool): Whether to include DEFAULT_HEADERS as base.

    Returns:
        Dict[str, str]: HTTP headers with realistic settings.
    """
    # Step 1: Start with default headers (if enabled)
    if include_defaults:
        headers = DEFAULT_HEADERS.copy()
    else:
        headers = {}

    # Step 2: Get source-specific configuration
    source_config = HEADERS_MAPPING_SOURCE.get(data_source.upper(), {})

    # Step 3: Determine and set User-Agent
    if random_agent:
        browser = random.choice(list(USER_AGENTS.keys()))
        platform = random.choice(list(USER_AGENTS[browser].keys()))

    ua = USER_AGENTS.get(browser.lower(), {}).get(platform.lower())

    if not ua:
        # Fallback to chrome/windows
        ua = USER_AGENTS.get("chrome", {}).get("windows")
        if not ua:
            # As a last resort, pick any user agent
            for b in USER_AGENTS.values():
                if isinstance(b, dict):
                    ua = next(iter(b.values()))
                    break

    if ua:
        headers["User-Agent"] = ua

    # Step 4: Add Referer and Origin from source config
    referer = source_config.get("Referer", "")
    origin = source_config.get("Origin", "")

    if referer:
        headers["Referer"] = referer
    if origin:
        headers["Origin"] = origin

    # Step 5: Merge custom headers
    if custom_headers:
        headers.update(custom_headers)

    # Step 6: Apply override headers (highest priority)
    if override_headers:
        headers.update(override_headers)

    # Step 7: Validate and return (remove None values)
    return {k: v for k, v in headers.items() if v is not None and v != ''}

