from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from time import perf_counter

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - runtime dependency
    sync_playwright = None
    PlaywrightError = Exception


@dataclass
class PageFetch:
    response: object | None
    elapsed_ms: float
    resources: list[dict]


class Browser(AbstractContextManager):
    def __init__(self, *, headless: bool, timeout_ms: int, wait_until: str) -> None:
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.wait_until = wait_until
        self._playwright = None
        self._browser = None
        self._context = None

    def __enter__(self) -> "Browser":
        if sync_playwright is None:
            raise RuntimeError(
                "Playwright is not installed. Run: uv pip install playwright && playwright install"
            )
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._context is not None:
            self._context.close()
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()

    def open(self, url: str) -> tuple[object | None, object | None, float, list[dict]]:
        if self._context is None:
            raise RuntimeError("Browser not initialized")
        page = self._context.new_page()
        resources: list[dict] = []

        def handle_response(resp) -> None:
            try:
                request = resp.request
                resources.append(
                    {
                        "url": resp.url,
                        "status": resp.status,
                        "resource_type": request.resource_type,
                    }
                )
            except Exception:
                return

        page.on("response", handle_response)
        start = perf_counter()
        response = None
        try:
            response = page.goto(url, wait_until=self.wait_until, timeout=self.timeout_ms)
        except PlaywrightError:
            pass
        elapsed_ms = (perf_counter() - start) * 1000
        return page, response, elapsed_ms, resources
