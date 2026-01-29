"""
Example: Scrape Data from a Single Post/Reel
Demonstrates how to extract metadata (likes, tags, date) from a specific URL.

Usage:
    python examples/example_post_data.py
"""

from instaharvest import PostDataScraper
from instaharvest.config import ScraperConfig

def main():
    print("=" * 60)
    print("📷 Single Post/Reel Data Scraper")
    print("=" * 60)

    # 1. Setup Config
    # headless=False so you can see it working
    config = ScraperConfig(headless=False)
    
    # 2. Create Scraper
    scraper = PostDataScraper(config=config)

    try:
        # Load session (required)
        print("\n📂 Loading session...")
        session_data = scraper.load_session()
        scraper.setup_browser(session_data)

        # 3. Get URL from user
        url = input("\nEnter Instagram Post/Reel URL: ").strip()
        if not url:
            print("❌ No URL provided.")
            return

        print(f"\n🔍 Scraping data from: {url}")
        print("   (Getting likes, tags, and timestamp...)")

        # 4. Scrape Data
        # Returns a PostData object
        post_data = scraper.scrape(
            url,
            get_tags=True,
            get_likes=True,
            get_timestamp=True
        )

        # 5. Show Results
        print("\n" + "=" * 60)
        print("✅ RESULTS")
        print("=" * 60)
        print(f"📌 Type:       {post_data.content_type}")
        print(f"🔗 URL:        {post_data.url}")
        print(f"📅 Timestamp:  {post_data.timestamp}")
        print(f"❤️  Likes:      {post_data.likes}")
        
        if post_data.tagged_accounts:
            print(f"🏷️  Tags ({len(post_data.tagged_accounts)}): {', '.join(post_data.tagged_accounts)}")
        else:
            print(f"🏷️  Tags:       None")

        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Always close the scraper
        scraper.close()

if __name__ == "__main__":
    main()
