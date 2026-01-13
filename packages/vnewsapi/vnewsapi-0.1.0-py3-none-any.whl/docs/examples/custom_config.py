"""
Custom configuration examples for vnewsapi.
"""

from vnewsapi import Crawler

# Example: Using custom configuration
print("=" * 60)
print("Custom Configuration Example")
print("=" * 60)

# Define custom site configuration
custom_config = {
    'name': 'Custom News Site',
    'base_url': 'https://example.com',
    'rss': {
        'urls': [
            'https://example.com/rss/feed1.rss',
            'https://example.com/rss/feed2.rss',
        ]
    },
    'sitemap': {
        'url': 'https://example.com/sitemap.xml',
        'pattern_type': 'static'
    },
    'selectors': {
        'title': {
            'tag': 'h1',
            'class': 'article-title'
        },
        'content': {
            'tag': 'div',
            'class': 'article-content'
        },
        'short_desc': {
            'tag': 'div',
            'class': 'article-summary'
        },
        'publish_time': {
            'tag': 'time',
            'class': 'publish-date'
        },
        'author': {
            'tag': 'span',
            'class': 'author-name'
        }
    }
}

# Use custom configuration
print("\n1. Initializing crawler with custom config...")
crawler = Crawler('cafef', custom_config=custom_config)
print(f"   Site name: {crawler.config['name']}")
print(f"   Base URL: {crawler.config['base_url']}")

# Example: Override selectors using CSS selector
print("\n2. Using CSS selector directly...")
custom_config_with_selector = {
    **custom_config,
    'selectors': {
        'title': {
            'selector': 'h1.article-title'
        },
        'content': {
            'selector': 'div.article-content > p'
        }
    }
}

crawler2 = Crawler('cafef', custom_config=custom_config_with_selector)
print("   Using CSS selectors for more precise extraction")

