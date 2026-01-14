from __future__ import annotations

import gzip
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests


def _strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _parse_xml(content: bytes) -> ET.Element:
    return ET.fromstring(content)


def _decode_content(url: str, response: requests.Response) -> bytes:
    if url.endswith(".gz"):
        return gzip.decompress(response.content)
    content_type = response.headers.get("content-type", "").lower()
    if "application/x-gzip" in content_type or "application/gzip" in content_type:
        return gzip.decompress(response.content)
    return response.content


def _iter_locs(root: ET.Element) -> Iterable[str]:
    for loc in root.findall(".//{*}loc"):
        if loc.text:
            yield loc.text.strip()


def _parse_sitemap_xml(content: bytes) -> tuple[str, list[str]]:
    root = _parse_xml(content)
    root_tag = _strip_ns(root.tag)
    return root_tag, list(_iter_locs(root))


def _read_local_sitemap(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix == ".gz":
        return gzip.decompress(data)
    return data


def _fetch_sitemap(url: str, *, session: requests.Session, timeout: float) -> bytes:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return _decode_content(url, response)


def parse_sitemap_urls(
    sitemap_url: str,
    *,
    session: requests.Session,
    timeout: float,
    max_urls: int | None = None,
) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    queue: list[str] = [sitemap_url]

    while queue:
        current = queue.pop(0)
        if current in seen:
            continue
        seen.add(current)

        parsed = urlparse(current)
        if parsed.scheme in ("http", "https") or parsed.scheme == "":
            if parsed.scheme == "" and Path(current).exists():
                content = _read_local_sitemap(Path(current))
            else:
                content = _fetch_sitemap(current, session=session, timeout=timeout)
        elif parsed.scheme == "file":
            content = _read_local_sitemap(Path(parsed.path))
        else:
            raise ValueError(f"Unsupported sitemap URL scheme: {parsed.scheme}")
        root_tag, locs = _parse_sitemap_xml(content)

        if root_tag == "sitemapindex":
            queue.extend(locs)
            continue

        if root_tag != "urlset":
            raise ValueError(f"Unsupported sitemap type: {root_tag}")

        for loc in locs:
            if loc not in urls:
                urls.append(loc)
                if max_urls is not None and len(urls) >= max_urls:
                    return urls

    return urls


def get_base_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"
