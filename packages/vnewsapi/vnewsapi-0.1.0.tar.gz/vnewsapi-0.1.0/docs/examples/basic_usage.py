"""
Basic usage examples for vnewsapi.
"""

from vnewsapi import Crawler, BatchCrawler, RSS, Sitemap

# Example 1: Get latest articles from CafeF
print("=" * 60)
print("Example 1: Get latest articles from CafeF")
print("=" * 60)

crawler = Crawler('cafef')
articles = crawler.get_articles(limit=5)
print(f"\nFound {len(articles)} articles:")
print(articles[['title', 'link']].head() if not articles.empty else "No articles found")

# Example 2: Get article details
print("\n" + "=" * 60)
print("Example 2: Get article details")
print("=" * 60)

if not articles.empty:
    first_article_url = articles.iloc[0]['link']
    details = crawler.get_article_details(first_article_url)
    print(f"\nTitle: {details.get('title', 'N/A')}")
    print(f"Author: {details.get('author', 'N/A')}")
    print(f"Publish Time: {details.get('publish_time', 'N/A')}")
    print(f"Content (first 200 chars): {details.get('content', '')[:200]}...")

# Example 3: Parse RSS feed
print("\n" + "=" * 60)
print("Example 3: Parse RSS feed")
print("=" * 60)

rss = RSS()
rss_articles = rss.fetch('https://cafef.vn/rss/tin-moi-nhat.rss')
print(f"\nFound {len(rss_articles)} articles from RSS:")
for article in rss_articles[:3]:
    print(f"- {article['title']}")

# Example 4: Parse sitemap
print("\n" + "=" * 60)
print("Example 4: Parse sitemap")
print("=" * 60)

sitemap = Sitemap()
urls_df = sitemap.run('https://cafef.vn/sitemap.xml', limit=10)
print(f"\nFound {len(urls_df)} URLs from sitemap:")
print(urls_df.head())

# Example 5: Batch crawling
print("\n" + "=" * 60)
print("Example 5: Batch crawling")
print("=" * 60)

batch = BatchCrawler('cafef', request_delay=0.5)
articles_list = crawler.get_articles(limit=3)
if not articles_list.empty:
    details_df = batch.fetch_details_from_dataframe(articles_list, url_column='link')
    print(f"\nFetched details for {len(details_df)} articles:")
    print(details_df[['title', 'author', 'publish_time']].head() if 'title' in details_df.columns else "No details")

