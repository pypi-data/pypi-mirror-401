"""
Batch crawling examples for vnewsapi.
"""

from vnewsapi import Crawler, BatchCrawler
import pandas as pd

# Example: Batch fetch article details
print("=" * 60)
print("Batch Crawling Example")
print("=" * 60)

# Step 1: Get article list
crawler = Crawler('cafef')
print("\n1. Fetching article list...")
articles = crawler.get_articles(limit=10)
print(f"   Found {len(articles)} articles")

# Step 2: Initialize batch crawler with delay
batch = BatchCrawler('cafef', request_delay=0.5)
print("\n2. Fetching article details (with 0.5s delay between requests)...")

# Step 3: Fetch details for all articles
details_df = batch.fetch_details_for_urls(
    articles['link'].tolist(),
    show_progress=True
)

print(f"\n3. Successfully fetched {len(details_df)} article details")
print(f"   Failed: {details_df['error'].notna().sum()}")

# Step 4: Display results
print("\n4. Sample results:")
if not details_df.empty:
    successful = details_df[details_df['error'].isna()]
    print(f"\n   Successful articles ({len(successful)}):")
    for idx, row in successful.head(3).iterrows():
        print(f"   - {row.get('title', 'N/A')[:50]}...")
        print(f"     Author: {row.get('author', 'N/A')}")
        print(f"     Time: {row.get('publish_time', 'N/A')}")

# Example: Merge with original DataFrame
print("\n" + "=" * 60)
print("Merging with original DataFrame")
print("=" * 60)

merged_df = batch.fetch_details_from_dataframe(articles, url_column='link')
print(f"\nMerged DataFrame shape: {merged_df.shape}")
print(f"Columns: {list(merged_df.columns)}")

