"""Basic usage examples for SmartScraper."""

from smartscraper import SmartScraper


def example_simple_scrape():
    """Simple one-line scrape."""
    result = SmartScraper.quick_scrape("https://example.com")
    print(f"Title: {result.title}")
    print(f"Items: {len(result)}")
    print(result.to_json()[:500])


def example_with_description():
    """Scrape with natural language description."""
    scraper = SmartScraper()
    result = scraper.scrape(
        "https://news.ycombinator.com",
        description="extract all article titles and links"
    )
    print(f"Found {len(result)} items")
    for item in result.data[:5]:
        print(f"- {item.get('text', 'N/A')}")


def example_with_selector():
    """Scrape with CSS selector."""
    scraper = SmartScraper()
    result = scraper.scrape(
        "https://example.com",
        selector="h1"
    )
    print(result.to_json())


def example_batch_scrape():
    """Batch scrape multiple URLs."""
    scraper = SmartScraper()
    urls = [
        "https://example.com",
        "https://example.org",
    ]
    results = scraper.scrape_batch(urls, description="extract title")
    for url, result in results.items():
        print(f"{url}: {result.title}")


def example_export():
    """Export results to different formats."""
    scraper = SmartScraper()
    result = scraper.scrape("https://example.com")
    
    # Save as JSON
    result.save("output.json")
    
    # Save as CSV
    result.save("output.csv")
    
    # Save as Markdown
    result.save("output.md")
    
    # Get as string
    json_str = result.to_json()
    csv_str = result.to_csv()
    md_str = result.to_markdown()
    
    print("Export complete!")


if __name__ == "__main__":
    print("SmartScraper Examples")
    print("=" * 50)
    
    # Run a simple example
    try:
        example_simple_scrape()
    except Exception as e:
        print(f"Note: Network example requires internet: {e}")
