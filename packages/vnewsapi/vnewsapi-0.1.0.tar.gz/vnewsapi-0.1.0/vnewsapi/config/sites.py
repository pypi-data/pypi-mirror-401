"""
News sites configuration for vnewsapi.

This module contains configuration for various Vietnamese news websites,
including RSS feeds, sitemaps, and CSS selectors for content extraction.
"""

from typing import Dict, Any, List

# Supported news sites
SUPPORTED_SITES = [
    "cafef",
    "cafebiz",
    "vietstock",
    "vnexpress",
    "baodautu",
    "tuoitre",
    "thanhnien",
    "dantri",
    "vneconomy",
    "vietnamnet",
]

# Site configurations
SITES_CONFIG: Dict[str, Dict[str, Any]] = {
    "cafef": {
        "name": "CafeF",
        "base_url": "https://cafef.vn",
        "rss": {
            "urls": [
                "https://cafef.vn/rss/tin-moi-nhat.rss",
                "https://cafef.vn/rss/thi-truong-chung-khoan.rss",
            ]
        },
        "sitemap": {
            "url": "https://cafef.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "cafebiz": {
        "name": "CafeBiz",
        "base_url": "https://cafebiz.vn",
        "rss": {
            "urls": [
                "https://cafebiz.vn/rss/tin-moi-nhat.rss",
            ]
        },
        "sitemap": {
            "url": "https://cafebiz.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "vietstock": {
        "name": "VietStock",
        "base_url": "https://vietstock.vn",
        "rss": {
            "urls": [
                "https://vietstock.vn/rss/tin-moi-nhat.rss",
            ]
        },
        "sitemap": {
            "url": "https://vietstock.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "vnexpress": {
        "name": "VnExpress",
        "base_url": "https://vnexpress.net",
        "rss": {
            "urls": [
                "https://vnexpress.net/rss/kinh-doanh.rss",
                "https://vnexpress.net/rss/tin-moi-nhat.rss",
            ]
        },
        "sitemap": {
            "url": "https://vnexpress.net/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title-detail"},
            "content": {"tag": "article", "class": "fck_detail"},
            "short_desc": {"tag": "p", "class": "description"},
            "publish_time": {"tag": "span", "class": "date"},
            "author": {"tag": "p", "class": "author_mail"}
        }
    },
    "baodautu": {
        "name": "Bao Dau Tu",
        "base_url": "https://baodautu.vn",
        "rss": {
            "urls": [
                "https://baodautu.vn/rss/tin-moi-nhat.rss",
            ]
        },
        "sitemap": {
            "url": "https://baodautu.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "tuoitre": {
        "name": "Tuoi Tre",
        "base_url": "https://tuoitre.vn",
        "rss": {
            "urls": [
                "https://tuoitre.vn/rss/kinh-te.rss",
            ]
        },
        "sitemap": {
            "url": "https://tuoitre.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "article-title"},
            "content": {"tag": "div", "class": "content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "div", "class": "date-time"},
            "author": {"tag": "div", "class": "author"}
        }
    },
    "thanhnien": {
        "name": "Thanh Nien",
        "base_url": "https://thanhnien.vn",
        "rss": {
            "urls": [
                "https://thanhnien.vn/rss/kinh-te.rss",
            ]
        },
        "sitemap": {
            "url": "https://thanhnien.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "detail-title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "dantri": {
        "name": "Dan Tri",
        "base_url": "https://dantri.com.vn",
        "rss": {
            "urls": [
                "https://dantri.com.vn/rss/kinh-te.rss",
            ]
        },
        "sitemap": {
            "url": "https://dantri.com.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title-page"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "vneconomy": {
        "name": "Vietnam Economy",
        "base_url": "https://vneconomy.vn",
        "rss": {
            "urls": [
                "https://vneconomy.vn/rss/tin-moi-nhat.rss",
            ]
        },
        "sitemap": {
            "url": "https://vneconomy.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
    "vietnamnet": {
        "name": "VietnamNet",
        "base_url": "https://vietnamnet.vn",
        "rss": {
            "urls": [
                "https://vietnamnet.vn/rss/kinh-te.rss",
            ]
        },
        "sitemap": {
            "url": "https://vietnamnet.vn/sitemap.xml",
            "pattern_type": "static"
        },
        "selectors": {
            "title": {"tag": "h1", "class": "title"},
            "content": {"tag": "div", "class": "detail-content"},
            "short_desc": {"tag": "div", "class": "sapo"},
            "publish_time": {"tag": "span", "class": "time"},
            "author": {"tag": "span", "class": "author"}
        }
    },
}


def get_site_config(site_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific site.
    
    Args:
        site_name (str): Site name (e.g., 'cafef', 'vietstock')
        
    Returns:
        Dict[str, Any]: Site configuration dictionary
        
    Raises:
        KeyError: If site name is not found
    """
    site_name_lower = site_name.lower()
    if site_name_lower not in SITES_CONFIG:
        raise KeyError(
            f"Site '{site_name}' not found. "
            f"Supported sites: {', '.join(SUPPORTED_SITES)}"
        )
    return SITES_CONFIG[site_name_lower]

