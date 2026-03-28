"""Main entry point: fetch → summarize → email."""

import sys

from fetch_news import fetch_articles
from summarize import summarize_articles
from send_email import render_email, send_email


def main():
    print("=== Stock News Digest ===")

    # Step 1: Fetch
    print("\n[1/3] Fetching news from RSS feeds...")
    articles = fetch_articles()
    print(f"  Found {len(articles)} relevant articles")

    if not articles:
        print("  No articles found. Exiting.")
        sys.exit(0)

    # Step 2: Summarize
    print(f"\n[2/3] Generating AI summaries ({len(articles)} articles)...")
    print("  This may take a few minutes (rate-limited to stay within free tier)")
    articles = summarize_articles(articles)
    print("  Summaries done!")

    # Step 3: Send
    print("\n[3/3] Rendering and sending email...")
    html = render_email(articles)
    send_email(html, len(articles))

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
