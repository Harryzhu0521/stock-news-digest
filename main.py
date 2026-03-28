"""Main entry point: fetch market data + news → summarize → email."""

import sys

from fetch_news import fetch_articles
from fetch_market import fetch_indices, fetch_tech_stocks, fetch_sectors, fetch_treasuries, format_market_data
from summarize import summarize_articles
from send_email import render_email, send_email


def main():
    print("=== Stock News Digest ===")

    # Step 1: Fetch market data
    print("\n[1/4] Fetching market data...")
    indices = fetch_indices()
    print(f"  Indices: {len(indices)} loaded")
    tech = fetch_tech_stocks()
    print(f"  Tech stocks: {len(tech)} loaded")
    sectors = fetch_sectors()
    print(f"  Sectors: {len(sectors)} loaded")
    treasuries = fetch_treasuries()
    print(f"  Treasuries: {len(treasuries)} loaded")
    market_data = format_market_data(indices, tech, sectors, treasuries)

    # Step 2: Fetch news
    print("\n[2/4] Fetching news from RSS feeds...")
    articles = fetch_articles()
    print(f"  Found {len(articles)} relevant articles")

    if not articles:
        print("  No articles found. Exiting.")
        sys.exit(0)

    # Step 3: Summarize
    print(f"\n[3/4] Generating AI summaries ({len(articles)} articles)...")
    articles = summarize_articles(articles)
    print("  Summaries done!")

    # Step 4: Send
    print("\n[4/4] Rendering and sending email...")
    html = render_email(articles, market_data)
    send_email(html, len(articles))

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
