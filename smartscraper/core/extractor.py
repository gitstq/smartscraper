"""HTML content extractor with multiple strategies."""

import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag


class ContentExtractor:
    """Extract structured data from HTML using multiple strategies."""

    def __init__(self, html: str, url: str = ""):
        self.soup = BeautifulSoup(html, "lxml")
        self.url = url

    def get_title(self) -> str:
        """Extract page title."""
        title_tag = self.soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)
        h1 = self.soup.find("h1")
        if h1:
            return h1.get_text(strip=True)
        return ""

    def get_text(self, selector: Optional[str] = None) -> str:
        """Extract clean text content."""
        if selector:
            elements = self.soup.select(selector)
            return "\n".join(el.get_text(strip=True, separator=" ") for el in elements)
        # Remove script/style tags
        for tag in self.soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return self.soup.get_text(separator="\n", strip=True)

    def get_links(self) -> List[Dict[str, str]]:
        """Extract all links."""
        links = []
        for a in self.soup.find_all("a", href=True):
            links.append({
                "text": a.get_text(strip=True),
                "href": a["href"],
                "title": a.get("title", ""),
            })
        return links

    def get_images(self) -> List[Dict[str, str]]:
        """Extract all images."""
        images = []
        for img in self.soup.find_all("img"):
            images.append({
                "src": img.get("src", ""),
                "alt": img.get("alt", ""),
                "title": img.get("title", ""),
            })
        return images

    def get_tables(self) -> List[List[Dict[str, str]]]:
        """Extract all tables as list of row dicts."""
        tables = []
        for table in self.soup.find_all("table"):
            rows = []
            headers = []
            thead = table.find("thead")
            if thead:
                headers = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
            else:
                first_row = table.find("tr")
                if first_row:
                    headers = [cell.get_text(strip=True) for cell in first_row.find_all(["th", "td"])]
            for tr in table.find_all("tr")[1 if not thead else 0:]:
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cells:
                    row = {}
                    for i, h in enumerate(headers):
                        row[h if h else f"col_{i}"] = cells[i] if i < len(cells) else ""
                    rows.append(row)
            if rows:
                tables.append(rows)
        return tables

    def get_articles(self) -> List[Dict[str, str]]:
        """Extract article-like content blocks."""
        articles = []
        # Try article tags
        for article in self.soup.find_all("article"):
            articles.append(self._extract_article_block(article))
        # Try common article containers
        if not articles:
            for cls in ["post", "entry", "content", "article", "blog-post"]:
                for div in self.soup.find_all(class_=re.compile(cls, re.I)):
                    articles.append(self._extract_article_block(div))
        return [a for a in articles if a.get("title") or a.get("content")]

    def _extract_article_block(self, tag: Tag) -> Dict[str, str]:
        """Extract title and content from an article block."""
        title = ""
        for h in tag.find_all(["h1", "h2", "h3"]):
            title = h.get_text(strip=True)
            if title:
                break
        content = tag.get_text(separator="\n", strip=True)
        # Clean up
        lines = [l for l in content.split("\n") if len(l.strip()) > 10]
        return {
            "title": title,
            "content": "\n".join(lines[:20]),  # Limit length
        }

    def get_meta(self) -> Dict[str, str]:
        """Extract meta tags."""
        meta = {}
        for tag in self.soup.find_all("meta"):
            name = tag.get("name", tag.get("property", ""))
            content = tag.get("content", "")
            if name and content:
                meta[name] = content
        return meta

    def get_structured_data(self) -> List[Dict[str, Any]]:
        """Extract JSON-LD structured data."""
        data = []
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                import json
                data.append(json.loads(script.string))
            except Exception:
                pass
        return data

    def smart_extract(self, description: str) -> List[Dict[str, Any]]:
        """AI-assisted extraction based on natural language description."""
        description = description.lower()
        
        # Keyword-based routing
        if any(k in description for k in ["链接", "link", "url", "href"]):
            return self.get_links()
        if any(k in description for k in ["图片", "image", "photo", "img"]):
            return self.get_images()
        if any(k in description for k in ["表格", "table", "数据", "data"]):
            tables = self.get_tables()
            return tables[0] if tables else []
        if any(k in description for k in ["文章", "article", "新闻", "news", "博客", "blog"]):
            return self.get_articles()
        if any(k in description for k in ["标题", "title", "headline"]):
            return [{"title": self.get_title()}]
        if any(k in description for k in ["元数据", "meta", "描述", "description"]):
            return [self.get_meta()]
        
        # Default: extract text paragraphs
        text = self.get_text()
        paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 30]
        return [{"content": p} for p in paragraphs[:20]]
