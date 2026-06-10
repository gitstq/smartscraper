"""Unit tests for SmartScraper core functionality."""

import pytest
from smartscraper.core.scraper import SmartScraper
from smartscraper.core.extractor import ContentExtractor
from smartscraper.core.result import ScrapingResult


SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <h1>Main Title</h1>
    <article>
        <h2>Article 1</h2>
        <p>This is the first article content.</p>
        <a href="/link1">Link 1</a>
    </article>
    <article>
        <h2>Article 2</h2>
        <p>This is the second article content.</p>
        <a href="/link2">Link 2</a>
    </article>
    <img src="image1.jpg" alt="Image 1">
    <table>
        <tr><th>Name</th><th>Value</th></tr>
        <tr><td>Item 1</td><td>100</td></tr>
        <tr><td>Item 2</td><td>200</td></tr>
    </table>
</body>
</html>
"""


class TestContentExtractor:
    def test_get_title(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        assert extractor.get_title() == "Test Page"

    def test_get_links(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        links = extractor.get_links()
        assert len(links) == 2
        assert links[0]["text"] == "Link 1"
        assert links[0]["href"] == "/link1"

    def test_get_images(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        images = extractor.get_images()
        assert len(images) == 1
        assert images[0]["src"] == "image1.jpg"
        assert images[0]["alt"] == "Image 1"

    def test_get_tables(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        tables = extractor.get_tables()
        assert len(tables) == 1
        assert len(tables[0]) == 2
        assert tables[0][0]["Name"] == "Item 1"

    def test_get_articles(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        articles = extractor.get_articles()
        assert len(articles) == 2
        assert "Article 1" in articles[0]["title"]

    def test_smart_extract_links(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        data = extractor.smart_extract("extract all links")
        assert len(data) == 2

    def test_smart_extract_images(self):
        extractor = ContentExtractor(SAMPLE_HTML)
        data = extractor.smart_extract("get images")
        assert len(data) == 1


class TestScrapingResult:
    def test_to_json(self):
        result = ScrapingResult([{"a": 1}], "http://test.com")
        json_str = result.to_json()
        assert '"a": 1' in json_str
        assert "metadata" in json_str

    def test_to_csv(self):
        result = ScrapingResult([{"name": "A", "value": "1"}], "http://test.com")
        csv_str = result.to_csv()
        assert "name,value" in csv_str
        assert "A,1" in csv_str

    def test_to_markdown(self):
        result = ScrapingResult([{"name": "A", "value": "1"}], "http://test.com")
        md = result.to_markdown()
        assert "| name | value |" in md

    def test_save(self, tmp_path):
        result = ScrapingResult([{"a": 1}], "http://test.com")
        filepath = tmp_path / "test.json"
        result.save(str(filepath))
        assert filepath.exists()


class TestSmartScraper:
    def test_init(self):
        scraper = SmartScraper(timeout=10, retries=1)
        assert scraper.fetcher.timeout == 10
        assert scraper.fetcher.retries == 1

    def test_quick_scrape(self):
        # This would need mocking for real network tests
        pass
