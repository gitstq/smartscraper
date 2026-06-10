"""HTTP fetcher with smart retry, rotation and anti-detection."""

import time
import random
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from fake_useragent import UserAgent


class SmartFetcher:
    """Intelligent HTTP fetcher with built-in anti-blocking strategies."""

    def __init__(
        self,
        timeout: int = 30,
        retries: int = 3,
        delay: float = 1.0,
        random_delay: bool = True,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.random_delay = random_delay
        self.ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self._default_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        if headers:
            self._default_headers.update(headers)

    def _get_headers(self, url: str) -> Dict[str, str]:
        """Generate request headers with rotating User-Agent."""
        headers = self._default_headers.copy()
        headers["User-Agent"] = self.ua.random
        # Add referer for some sites
        if "://" in url:
            parts = url.split("/")
            headers["Referer"] = f"{parts[0]}//{parts[2]}/"
        return headers

    def _should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if request should be retried."""
        if attempt >= self.retries:
            return False
        if isinstance(error, urllib.error.HTTPError):
            # Retry on rate limit or server errors
            return error.code in (429, 500, 502, 503, 504)
        if isinstance(error, (urllib.error.URLError, TimeoutError)):
            return True
        return False

    def _wait(self, attempt: int) -> None:
        """Wait with exponential backoff and jitter."""
        base = self.delay * (2 ** attempt)
        jitter = random.uniform(0, base * 0.5) if self.random_delay else 0
        time.sleep(base + jitter)

    def fetch(self, url: str) -> str:
        """Fetch URL content with smart retry logic."""
        last_error = None
        for attempt in range(self.retries + 1):
            try:
                headers = self._get_headers(url)
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = resp.read()
                    # Handle gzip
                    if resp.headers.get("Content-Encoding") == "gzip":
                        import gzip
                        data = gzip.decompress(data)
                    charset = "utf-8"
                    content_type = resp.headers.get("Content-Type", "")
                    if "charset=" in content_type:
                        charset = content_type.split("charset=")[-1].split(";")[0].strip()
                    return data.decode(charset, errors="replace")
            except Exception as e:
                last_error = e
                if self._should_retry(e, attempt):
                    self._wait(attempt)
                    continue
                break
        raise Exception(f"Failed to fetch {url} after {self.retries + 1} attempts: {last_error}")

    def fetch_batch(self, urls: list, concurrency: int = 5) -> Dict[str, str]:
        """Fetch multiple URLs sequentially with rate limiting."""
        results = {}
        for url in urls:
            try:
                results[url] = self.fetch(url)
                # Polite delay between requests
                if self.delay > 0:
                    time.sleep(self.delay + random.uniform(0, 0.5))
            except Exception as e:
                results[url] = f"ERROR: {e}"
        return results
