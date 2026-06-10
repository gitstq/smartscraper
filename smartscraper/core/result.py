"""Scraping result container and export utilities."""

import json
import csv
import io
from typing import Any, Dict, List


class ScrapingResult:
    """Container for scraped data with export capabilities."""

    def __init__(self, data: List[Dict[str, Any]], url: str, title: str = ""):
        self.data = data
        self.url = url
        self.title = title
        self._metadata = {
            "source": url,
            "title": title,
            "count": len(data),
        }

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        return self.data[index]

    def first(self) -> Dict[str, Any]:
        """Return the first item or empty dict."""
        return self.data[0] if self.data else {}

    def to_json(self, indent: int = 2) -> str:
        """Export results as JSON string."""
        return json.dumps(
            {"metadata": self._metadata, "data": self.data},
            ensure_ascii=False,
            indent=indent,
        )

    def to_csv(self) -> str:
        """Export results as CSV string."""
        if not self.data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.data[0].keys())
        writer.writeheader()
        writer.writerows(self.data)
        return output.getvalue()

    def to_markdown(self) -> str:
        """Export results as Markdown table."""
        if not self.data:
            return ""
        keys = list(self.data[0].keys())
        lines = ["| " + " | ".join(keys) + " |"]
        lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
        for item in self.data:
            row = "| " + " | ".join(str(item.get(k, "")) for k in keys) + " |"
            lines.append(row)
        return "\n".join(lines)

    def to_txt(self) -> str:
        """Export results as plain text."""
        lines = []
        for i, item in enumerate(self.data, 1):
            lines.append(f"[{i}] ---")
            for k, v in item.items():
                lines.append(f"  {k}: {v}")
            lines.append("")
        return "\n".join(lines)

    def save(self, filepath: str, format: str = "auto") -> None:
        """Save results to file with auto-detected or specified format."""
        if format == "auto":
            ext = filepath.split(".")[-1].lower()
            format = ext if ext in ("json", "csv", "md", "txt") else "json"

        exporters = {
            "json": self.to_json,
            "csv": self.to_csv,
            "md": self.to_markdown,
            "txt": self.to_txt,
        }
        content = exporters.get(format, self.to_json)()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
