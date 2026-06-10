"""SmartScraper - Zero-config intelligent web scraping framework."""

__version__ = "1.0.0"
__author__ = "Gitstq"
__license__ = "MIT"

from .core.scraper import SmartScraper
from .core.result import ScrapingResult

__all__ = ["SmartScraper", "ScrapingResult"]
