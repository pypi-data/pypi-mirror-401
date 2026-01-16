"""Canonicalize duplicate pages using WordLift entities and GSC KPIs."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from worai.core.wordlift import DEFAULT_GRAPHQL_ENDPOINT, graphql_request


@dataclass
class CanonicalizeOptions:
    api_key: str
    input_csv: str
    output_csv: str
    url_regex: str | None
    endpoint: str = DEFAULT_GRAPHQL_ENDPOINT
    batch_size: int = 25
    kpi_window: str = "28d"
    kpi_metric: str = "clicks"


def normalize_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


def parse_float(value: Optional[str]) -> float:
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def load_gsc_csv(path: str, url_regex: Optional[str]) -> Dict[str, Dict[str, float]]:
    pattern = re.compile(url_regex) if url_regex else None
    data: Dict[str, Dict[str, float]] = {}

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "page" not in reader.fieldnames:
            raise RuntimeError("Input CSV missing required 'page' column")
        for row in reader:
            page = (row.get("page") or "").strip()
            if not page:
                continue
            if pattern and not pattern.search(page):
                continue
            data[page] = {k: parse_float(row.get(k)) for k in row.keys() if k != "page"}

    return data


def build_entity_query(urls: List[str]) -> str:
    fields = (
        'iri url: string(name: "schema:url") '
        'name: string(name: "schema:name") '
        'types: refs(name: "rdf:type")'
    )
    lines = ["query {"]
    for idx, url in enumerate(urls):
        alias = f"e{idx}"
        url_str = json.dumps(url)
        lines.append(f"  {alias}: entity(url: {url_str}) {{ {fields} }}")
    lines.append("}")
    return "\n".join(lines)


def fetch_entities_by_url(
    endpoint: str,
    api_key: str,
    urls: List[str],
    batch_size: int,
) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}

    for i in range(0, len(urls), batch_size):
        batch = urls[i : i + batch_size]
        query = build_entity_query(batch)
        data = graphql_request(endpoint, api_key, query)
        items = data.get("data", {})
        for idx, url in enumerate(batch):
            key = f"e{idx}"
            entity = items.get(key)
            if not entity:
                continue
            out[url] = entity

    return out


def extract_types(raw_types: object) -> List[str]:
    if raw_types is None:
        return []
    if isinstance(raw_types, list):
        types: List[str] = []
        for item in raw_types:
            if isinstance(item, str):
                types.append(item)
            elif isinstance(item, dict):
                iri = item.get("iri") or item.get("id") or item.get("@id")
                if iri:
                    types.append(iri)
        return types
    if isinstance(raw_types, str):
        return [raw_types]
    return []


def choose_primary_type(types: List[str]) -> Optional[str]:
    if not types:
        return None
    return sorted(types)[0]


def build_clusters(entities: Dict[str, Dict[str, object]]) -> Dict[Tuple[str, str], List[str]]:
    clusters: Dict[Tuple[str, str], List[str]] = {}
    for url, entity in entities.items():
        name = entity.get("name")
        if not name or not isinstance(name, str):
            continue
        name_key = normalize_name(name)
        types = extract_types(entity.get("types"))
        type_key = choose_primary_type(types)
        if not type_key:
            continue
        clusters.setdefault((type_key, name_key), []).append(url)
    return clusters


def select_canonical(urls: List[str], kpis: Dict[str, Dict[str, float]], kpi_key: str) -> str:
    def score(u: str) -> Tuple[float, str]:
        value = kpis.get(u, {}).get(kpi_key, 0.0)
        return (value, u)

    return max(urls, key=score)


def write_output_csv(path: str, rows: List[Dict[str, str]]) -> None:
    fieldnames = ["type", "name", "canonical_url", "duplicate_url", "kpi_metric", "kpi_value"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run(options: CanonicalizeOptions) -> None:
    kpi_key = f"{options.kpi_metric}_{options.kpi_window}"
    gsc_data = load_gsc_csv(options.input_csv, options.url_regex)

    urls = list(gsc_data.keys())
    entities = fetch_entities_by_url(options.endpoint, options.api_key, urls, options.batch_size)
    clusters = build_clusters(entities)

    output_rows: List[Dict[str, str]] = []
    for (type_key, name_key), cluster_urls in clusters.items():
        if len(cluster_urls) < 2:
            continue
        canonical = select_canonical(cluster_urls, gsc_data, kpi_key)
        for url in cluster_urls:
            if url == canonical:
                continue
            output_rows.append(
                {
                    "type": type_key,
                    "name": name_key,
                    "canonical_url": canonical,
                    "duplicate_url": url,
                    "kpi_metric": kpi_key,
                    "kpi_value": str(gsc_data.get(canonical, {}).get(kpi_key, 0.0)),
                }
            )

    write_output_csv(options.output_csv, output_rows)
