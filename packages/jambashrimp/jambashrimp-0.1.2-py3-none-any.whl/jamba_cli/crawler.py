"""Lightweight crawler for library documentation sites."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable, Iterable
from urllib.parse import urljoin, urlparse, urldefrag

import httpx
import requests
from bs4 import BeautifulSoup

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


@dataclass(slots=True)
class CrawledPage:
    """Represents a crawled documentation page."""

    url: str
    title: str
    content: str


ProgressCallback = Callable[[int, int | None], None]


class DocumentationCrawler:
    """Depth-limited crawler that stays within a single documentation site."""

    def __init__(
        self,
        base_url: str,
        *,
        max_pages: int | None,
        max_depth: int,
        max_concurrency: int = 16,
        timeout: float = 15.0,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        parsed = urlparse(base_url)
        if not parsed.scheme.startswith("http"):
            raise ValueError("Only HTTP/HTTPS URLs are supported.")
        if not parsed.netloc:
            raise ValueError(f"Invalid documentation URL: {base_url}")

        self.base_url = base_url.rstrip("/")
        self.base_domain = parsed.netloc.lower()
        if max_pages is None or max_pages <= 0:
            self.max_pages: int | None = None
        else:
            self.max_pages = max_pages
        self.max_depth = max(0, max_depth)
        self.timeout = timeout
        self.progress_callback = progress_callback
        self.max_concurrency = max(1, max_concurrency)
        self.headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def crawl(self) -> list[CrawledPage]:
        """Crawl up to the configured depth/page limits, concurrently."""
        return asyncio.run(self._crawl_async())

    async def _crawl_async(self) -> list[CrawledPage]:
        results: list[CrawledPage] = []
        visited: set[str] = set()
        visited_lock = asyncio.Lock()
        results_lock = asyncio.Lock()
        stop_event = asyncio.Event()
        queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
        await queue.put((self.base_url, 0))

        async with httpx.AsyncClient(
            headers=self.headers,
            follow_redirects=True,
            timeout=self.timeout,
        ) as client:
            async def worker() -> None:
                while True:
                    if stop_event.is_set() and queue.empty():
                        break
                    try:
                        url, depth = await queue.get()
                    except asyncio.CancelledError:
                        break

                    if stop_event.is_set():
                        queue.task_done()
                        continue

                    normalized = self._normalize_url(url)
                    if not normalized:
                        queue.task_done()
                        continue

                    async with visited_lock:
                        if normalized in visited:
                            queue.task_done()
                            continue
                        visited.add(normalized)

                    if depth > self.max_depth or stop_event.is_set():
                        queue.task_done()
                        continue

                    html = await self._fetch_html(client, normalized)
                    if html:
                        page = self._parse_page(normalized, html)
                        if page.content.strip():
                            async with results_lock:
                                if self.max_pages is None or len(results) < self.max_pages:
                                    results.append(page)
                                    self._emit_progress(len(results))
                                    if self.max_pages and len(results) >= self.max_pages:
                                        stop_event.set()

                        if depth < self.max_depth and not stop_event.is_set():
                            for link in self._extract_links(normalized, html):
                                queue.put_nowait((link, depth + 1))

                    queue.task_done()

            workers = [asyncio.create_task(worker()) for _ in range(self.max_concurrency)]
            await queue.join()
            stop_event.set()

            for worker_task in workers:
                worker_task.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        return results

    def _emit_progress(self, completed: int) -> None:
        if self.progress_callback:
            self.progress_callback(completed, self.max_pages)

    def _normalize_url(self, url: str) -> str | None:
        stripped, _fragment = urldefrag(url.strip())
        parsed = urlparse(stripped)
        if parsed.scheme not in {"http", "https"}:
            return None
        if not parsed.netloc:
            return None
        if not self._is_same_domain(parsed.netloc):
            return None
        # Remove default ports.
        netloc = parsed.netloc.lower()
        if netloc.endswith(":80") and parsed.scheme == "http":
            netloc = netloc[:-3]
        if netloc.endswith(":443") and parsed.scheme == "https":
            netloc = netloc[:-4]
        rebuilt = parsed._replace(netloc=netloc)
        return rebuilt.geturl()

    def _extract_links(self, current_url: str, html: str) -> Iterable[str]:
        soup = BeautifulSoup(html, "lxml")
        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href", "")
            if href.startswith("#") or href.lower().startswith("javascript:"):
                continue
            absolute = urljoin(current_url, href)
            normalized = self._normalize_url(absolute)
            if normalized:
                yield normalized

    async def _fetch_html(self, client: httpx.AsyncClient, url: str) -> str | None:
        try:
            response = await client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                return None
            return response.text
        except httpx.HTTPError:
            return await self._fallback_fetch(url)

    async def _fallback_fetch(self, url: str) -> str | None:
        """Use requests in a thread to avoid blocking the event loop."""
        return await asyncio.to_thread(self._fallback_fetch_sync, url)

    def _fallback_fetch_sync(self, url: str) -> str | None:
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True,
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                return None
            return response.text
        except requests.RequestException:
            return None

    def _parse_page(self, url: str, html: str) -> CrawledPage:
        soup = BeautifulSoup(html, "lxml")
        self._strip_boilerplate(soup)
        title = self._extract_title(soup)
        text = self._extract_text(soup)
        return CrawledPage(url=url, title=title, content=text)

    def _strip_boilerplate(self, soup: BeautifulSoup) -> None:
        for selector in ("script", "style", "header", "footer", "nav", "aside", "noscript"):
            for tag in soup.select(selector):
                tag.decompose()

        # Remove obvious utility elements.
        for attr in ("aria-hidden", "role"):
            for tag in soup.find_all(attrs={attr: "presentation"}):
                tag.decompose()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        if soup.title and soup.title.get_text(strip=True):
            return soup.title.get_text(strip=True)
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        return "Untitled"

    def _extract_text(self, soup: BeautifulSoup) -> str:
        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in (chunk.strip() for chunk in text.splitlines()) if line]
        return "\n".join(lines)

    def _is_same_domain(self, netloc: str) -> bool:
        candidate = netloc.lower()
        return candidate == self.base_domain or candidate.endswith("." + self.base_domain)


