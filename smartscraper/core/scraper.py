"""Main scraper orchestrating fetch and extract operations."""

from typing import List, Dict, Any, Optional
from .fetcher import SmartFetcher
from .extractor import ContentExtractor
from .result import ScrapingResult


class SmartScraper:
    """Zero-config intelligent web scraping framework."""

    def __init__(
        self,
        timeout: int = 30,
        retries: int = 3,
        delay: float = 1.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.fetcher = SmartFetcher(
            timeout=timeout,
            retries=retries,
            delay=delay,
            headers=headers,
        )

    def scrape(
        self,
        url: str,
        description: str = "",
        selector: Optional[str] = None,
    ) -> ScrapingResult:
        """Scrape a single URL.
        
        Args:
            url: Target URL to scrape
            description: Natural language description of what to extract
            selector: Optional CSS selector for precise extraction
            
        Returns:
            ScrapingResult containing extracted data
        """
        html = self.fetcher.fetch(url)
        extractor = ContentExtractor(html, url)
        title = extractor.get_title()
        
        if selector:
            data = self._extract_by_selector(extractor, selector)
        elif description:
            data = extractor.smart_extract(description)
        else:
            # Default: extract text content
            data = [{"content": extractor.get_text()}]
        
        return ScrapingResult(data, url, title)

    def scrape_batch(
        self,
        urls: List[str],
        description: str = "",
        selector: Optional[str] = None,
    ) -> Dict[str, ScrapingResult]:
        """Scrape multiple URLs sequentially.
        
        Args:
            urls: List of target URLs
            description: Natural language description of what to extract
            selector: Optional CSS selector
            
        Returns:
            Dict mapping URL to ScrapingResult
        """
        results = {}
        for url in urls:
            try:
                results[url] = self.scrape(url, description, selector)
            except Exception as e:
                results[url] = ScrapingResult(
                    [{"error": str(e)}], url, ""
                )
        return results

    def scrape_links(
        self,
        url: str,
        pattern: Optional[str] = None,
        max_links: int = 50,
    ) -> List[Dict[str, str]]:
        """Scrape and filter links from a page.
        
        Args:
            url: Target URL
            pattern: Optional regex pattern to filter links
            max_links: Maximum number of links to return
            
        Returns:
            List of link dictionaries
        """
        html = self.fetcher.fetch(url)
        extractor = ContentExtractor(html, url)
        links = extractor.get_links()
        
        if pattern:
            import re
            regex = re.compile(pattern)
            links = [l for l in links if regex.search(l.get("href", ""))]
        
        return links[:max_links]

    def _extract_by_selector(
        self,
        extractor: ContentExtractor,
        selector: str,
    ) -> List[Dict[str, Any]]:
        """Extract data using CSS selector."""
        from bs4 import BeautifulSoup
        soup = extractor.soup
        elements = soup.select(selector)
        results = []
        for el in elements:
            item = {
                "text": el.get_text(strip=True, separator=" "),
                "html": str(el),
            }
            # Extract common attributes
            for attr in ["href", "src", "alt", "title", "id", "class"]:
                if el.get(attr):
                    item[attr] = el.get(attr)
            results.append(item)
        return results

    @staticmethod
    def quick_scrape(url: str, description: str = "") -> ScrapingResult:
        """One-liner quick scrape without instantiation."""
        scraper = SmartScraper()
        return scraper.scrape(url, description)
