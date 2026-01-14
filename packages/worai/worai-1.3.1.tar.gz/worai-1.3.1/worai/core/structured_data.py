"""Generate structured data from a rendered web page."""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Any

import wordlift_client
from wordlift_client import ApiClient, Configuration
from wordlift_client import AgentApi
from wordlift_client.models.ask_request import AskRequest

from worai.core.prune_entities_outside_dataset import DEFAULT_BASE_URL
from worai.errors import ExternalServiceError, UsageError
from worai.seocheck.browser import Browser


_SCHEMA_BASE = "https://schema.org"
_AGENT_BASE_URL = "https://api.wordlift.io/agent"


@dataclass
class RenderOptions:
    url: str
    headless: bool = True
    timeout_ms: int = 30000
    wait_until: str = "domcontentloaded"


@dataclass
class StructuredDataOptions:
    url: str
    target_type: str | None
    dataset_uri: str
    headless: bool = True
    timeout_ms: int = 30000
    wait_until: str = "domcontentloaded"


@dataclass
class StructuredDataResult:
    jsonld: dict[str, Any]
    yarrml: str
    jsonld_filename: str
    yarrml_filename: str


def _build_client(api_key: str, base_url: str) -> ApiClient:
    config = Configuration(host=base_url)
    config.api_key["ApiKey"] = api_key
    config.api_key_prefix["ApiKey"] = "Key"
    return ApiClient(config)


def _build_agent_client(api_key: str) -> ApiClient:
    config = Configuration(host=_AGENT_BASE_URL)
    config.api_key["ApiKey"] = api_key
    config.api_key_prefix["ApiKey"] = "Key"
    return ApiClient(config)


async def get_dataset_uri_async(api_key: str, base_url: str = DEFAULT_BASE_URL) -> str:
    async with _build_client(api_key, base_url) as api_client:
        api = wordlift_client.AccountApi(api_client)
        account = await api.get_me()
    dataset_uri = getattr(account, "dataset_uri", None)
    if not dataset_uri:
        raise RuntimeError("Failed to resolve dataset_uri from account get_me.")
    return dataset_uri


def get_dataset_uri(api_key: str, base_url: str = DEFAULT_BASE_URL) -> str:
    return asyncio.run(get_dataset_uri_async(api_key, base_url))


def render_html(options: RenderOptions) -> str:
    with Browser(headless=options.headless, timeout_ms=options.timeout_ms, wait_until=options.wait_until) as browser:
        page, _response, _elapsed_ms, _resources = browser.open(options.url)
        if page is None:
            raise RuntimeError("Failed to open page in browser.")
        try:
            html = page.content()
        finally:
            page.close()
    return html


def normalize_type(value: str) -> str:
    value = value.strip()
    if value.startswith("schema:"):
        return value.split(":", 1)[1]
    if value.startswith("http://schema.org/"):
        return value.split("/", 3)[-1]
    if value.startswith("https://schema.org/"):
        return value.split("/", 3)[-1]
    return value


def _slugify(value: str, default: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or default


def _dash_type(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.strip())
    value = re.sub(r"(?<!^)(?=[A-Z])", "-", value)
    return re.sub(r"-+", "-", value).strip("-").lower()


def _pluralize(value: str) -> str:
    if value.endswith("y") and len(value) > 1 and value[-2] not in "aeiou":
        return value[:-1] + "ies"
    if value.endswith(("s", "x", "z", "ch", "sh")):
        return value + "es"
    return value + "s"


def _hash_url(url: str, length: int = 12) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:length]


def build_id(dataset_uri: str, type_name: str, name: str, url: str) -> str:
    base = dataset_uri.rstrip("/")
    dashed_type = _dash_type(type_name)
    plural_type = _pluralize(dashed_type)
    name_slug = _slugify(name, default="item")
    url_hash = _hash_url(url)
    return f"{base}/{plural_type}/{name_slug}-{url_hash}"


def _agent_prompt(url: str, html: str, target_type: str | None) -> str:
    target = target_type or "AUTO"
    return (
        f"analyze the entities on this webpage: {url}\n"
        "\n"
        "You are a structured data extraction agent.\n"
        "Goal: produce a YARRRML mapping using XPath only.\n"
        "Use the provided HTML source instead of fetching the URL.\n"
        "Do NOT parse any existing structured data (JSON-LD, RDFa, Microdata).\n"
        "Output ONLY the YARRRML mapping (no prose, no code fences).\n"
        "\n"
        f"Target Schema.org type: {target}\n"
        "\n"
        "Requirements:\n"
        "- Use XPath in all selectors.\n"
        "- The main mapping must include schema:url with the exact URL.\n"
        "- Always include schema:name for every mapped node.\n"
        "- Include relevant properties for the main type.\n"
        "- If Target Schema.org type is AUTO, infer the best type and use it.\n"
        "- Define dependent nodes as separate mappings and link them from the main mapping.\n"
        "\n"
        "HTML:\n"
        f"{html}\n"
    )


async def _ask_agent_async(prompt: str, api_key: str) -> object:
    async with _build_agent_client(api_key) as api_client:
        api = AgentApi(api_client)
        ask_request = AskRequest(message=prompt)
        return await api.ask_request_api_ask_post(ask_request)


def ask_agent_for_yarrml(
    api_key: str,
    url: str,
    html: str,
    target_type: str | None,
    debug: bool = False,
    debug_path: Path | None = None,
) -> str:
    prompt = _agent_prompt(url, html, target_type)
    try:
        response = asyncio.run(_ask_agent_async(prompt, api_key))
    except Exception as exc:
        raise ExternalServiceError(f"Agent request failed: {exc}") from exc

    if isinstance(response, dict):
        data = response
    else:
        try:
            data = response.model_dump()
        except Exception:
            data = {}

    if debug and debug_path is not None:
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_payload = {
            "prompt": prompt,
            "response": data,
        }
        debug_path.write_text(json.dumps(debug_payload, indent=2))

    for key in ("response", "answer", "content", "result", "output", "text", "message"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    raise ExternalServiceError("Agent response did not include YARRRML content.")


def _replace_sources_with_file(yarrml: str, file_uri: str) -> str:
    pattern = re.compile(r"(\[\s*['\"])([^'\"]+)(['\"]\s*,\s*['\"]xpath['\"])")

    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{file_uri}{match.group(3)}"

    return pattern.sub(repl, yarrml)


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _strip_wrapped_list(value: str) -> str:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1].strip()
    return _strip_quotes(value)


def _strip_all_quotes(value: str) -> str:
    value = value.strip()
    while (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1].strip()
    return value


def _looks_like_xpath(value: str) -> bool:
    value = value.strip()
    return (
        value.startswith("/")
        or value.startswith(".//")
        or value.startswith("//")
        or value.startswith("normalize-")
        or value.startswith("normalize(")
        or value.startswith("string(")
        or value.startswith("concat(")
    )


def _normalize_agent_yarrml(
    raw: str,
    url: str,
    file_uri: str,
    target_type: str | None,
) -> str:
    lines = raw.splitlines()
    mappings: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_mappings = False
    ignore_keys = {"mappings", "prefixes", "sources", "po"}
    last_p: str | None = None

    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if not stripped:
            continue
        if stripped == "mappings:":
            in_mappings = True
            continue
        if in_mappings and stripped.endswith(":") and not stripped.startswith("-"):
            name = stripped[:-1].strip()
            if name in ignore_keys:
                continue
            current = {"name": name, "type": None, "props": []}
            mappings.append(current)
            last_p = None
            continue
        if current is None:
            continue
        if stripped == "sources:" or stripped == "po:":
            continue
        if stripped.startswith("- [") and "value:" in stripped:
            if current is None:
                continue
            match = re.search(r"value:\s*\"([^\"]+)\"", stripped) or re.search(
                r"value:\s*'([^']+)'", stripped
            )
            if match:
                current["source_xpath"] = match.group(1)
            else:
                match = re.search(r"\\['html'\\]\\s*,\\s*\"([^\"]+)\"", stripped)
                if match:
                    current["source_xpath"] = match.group(1)
            continue
        if stripped.startswith("s:"):
            value = _strip_quotes(stripped.split(":", 1)[1].strip())
            if not (value.startswith("http://") or value.startswith("https://")):
                current["type"] = value
            continue
        if stripped.startswith("- p:"):
            _, value = stripped.split("p:", 1)
            last_p = _strip_quotes(value.strip())
            continue
        if stripped.startswith("o:") and last_p:
            _, value = stripped.split("o:", 1)
            obj = _strip_all_quotes(_strip_wrapped_list(value.strip()))
            current["props"].append((last_p, obj))
            last_p = None
            continue
        if stripped.startswith("- ["):
            if "p:" in stripped and "o:" in stripped:
                match = re.search(r"\[p:\s*([^,]+),\s*o:\s*(.+)\]$", stripped)
                if match:
                    prop = _strip_quotes(match.group(1).strip())
                    obj = _strip_all_quotes(_strip_wrapped_list(match.group(2).strip()))
                    current["props"].append((prop, obj))
                continue
            match = re.search(r"\[\s*([^,]+)\s*,\s*(.+)\]$", stripped)
            if match:
                prop = _strip_quotes(match.group(1).strip())
                obj = _strip_all_quotes(_strip_wrapped_list(match.group(2).strip()))
                current["props"].append((prop, obj))

    if not mappings:
        raise UsageError("Agent response did not include recognizable mappings.")

    mapping_names = {m["name"] for m in mappings}
    target = normalize_type(target_type) if target_type else None

    main_mapping = None
    for mapping in mappings:
        if target and normalize_type(mapping["type"] or "") == target:
            main_mapping = mapping
            break
    if main_mapping is None:
        main_mapping = mappings[0]

    output_lines = [
        "prefixes:",
        f"  schema: '{_SCHEMA_BASE}/'",
        "  ex: 'http://example.com/'",
        "mappings:",
    ]

    for mapping in mappings:
        map_name = mapping["name"]
        map_type = mapping["type"] or ("Review" if mapping is main_mapping else "Thing")
        map_type = normalize_type(map_type)
        output_lines += [
            f"  {map_name}:",
            "    sources:",
            f"      - [{file_uri}~xpath, '/']",
            f"    s: ex:{map_name}~iri",
            "    po:",
            f"      - [a, 'schema:{map_type}']",
        ]
        props = list(mapping["props"])
        source_xpath = mapping.get("source_xpath")

        if mapping is main_mapping:
            has_url = any(p == "schema:url" for p, _ in props)
            if not has_url:
                props.insert(0, ("schema:url", url))

        for prop, obj in props:
            if not prop.startswith("schema:"):
                prop = f"schema:{prop}"
            if obj == "{value}" and source_xpath:
                obj = source_xpath
            if obj in mapping_names:
                output_lines.append(f"      - [{prop}, ex:{obj}]")
                continue
            if _looks_like_xpath(obj):
                xpath = obj.replace("'", '"')
                output_lines.append(f"      - [{prop}, '$(%s)']" % xpath)
                continue
            output_lines.append(f"      - [{prop}, '{obj}']")

    return "\n".join(output_lines) + "\n"


def _run_yarrrml_parser(input_path: Path, output_path: Path) -> None:
    parser = shutil.which("yarrrml-parser")
    if not parser:
        raise UsageError(
            "yarrrml-parser is required. Install with: npm install -g @rmlio/yarrrml-parser"
        )
    if output_path.exists():
        output_path.unlink()
    result = subprocess.run(
        [parser, "-i", str(input_path), "-o", str(output_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if not output_path.exists():
        error = (result.stderr or result.stdout).strip()
        raise UsageError(f"yarrrml-parser failed to produce output. {error}")
    if result.returncode != 0:
        raise UsageError(f"yarrrml-parser failed: {result.stderr.strip()}")


def _materialize_jsonld(mapping_path: Path) -> dict[str, Any] | list[Any]:
    try:
        import morph_kgc
    except ImportError as exc:
        raise UsageError("morph-kgc is required. Install with: pip install morph-kgc") from exc

    config = (
        "[CONFIGURATION]\n"
        "output_format = N-TRIPLES\n"
        "\n"
        "[DataSource1]\n"
        f"mappings = {mapping_path}\n"
    )
    graph = morph_kgc.materialize(config)
    jsonld_str = graph.serialize(format="json-ld")
    return json.loads(jsonld_str)


def _flatten_jsonld(data: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [node for node in data if isinstance(node, dict)]
    if "@graph" in data and isinstance(data["@graph"], list):
        return [node for node in data["@graph"] if isinstance(node, dict)]
    return [data] if isinstance(data, dict) else []


def _extract_type(node: dict[str, Any]) -> str | None:
    raw = node.get("@type")
    if isinstance(raw, list) and raw:
        raw = raw[0]
    if isinstance(raw, str):
        return normalize_type(raw)
    return None


def _extract_name(node: dict[str, Any]) -> str | None:
    for key in ("name", "headline", "title"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _build_id_map(
    nodes: list[dict[str, Any]],
    dataset_uri: str,
    url: str,
) -> dict[str, str]:
    id_map: dict[str, str] = {}
    for idx, node in enumerate(nodes):
        old_id = node.get("@id") or f"_:b{idx}"
        type_name = _extract_type(node) or "Thing"
        name = _extract_name(node) or "item"
        new_id = build_id(dataset_uri, type_name, name, url)
        if old_id in id_map:
            new_id = f"{new_id}-{idx}"
        id_map[str(old_id)] = new_id
    return id_map


def _rewrite_refs(value: Any, id_map: dict[str, str], node_map: dict[str, dict[str, Any]]) -> Any:
    if isinstance(value, dict):
        if "@id" in value and isinstance(value["@id"], str):
            ref_id = id_map.get(value["@id"], value["@id"])
            if ref_id in node_map:
                return node_map[ref_id]
            return {"@id": ref_id}
        return {k: _rewrite_refs(v, id_map, node_map) for k, v in value.items()}
    if isinstance(value, list):
        return [_rewrite_refs(item, id_map, node_map) for item in value]
    return value


def normalize_jsonld(
    data: dict[str, Any] | list[Any],
    dataset_uri: str,
    url: str,
    target_type: str | None,
) -> dict[str, Any]:
    nodes = _flatten_jsonld(data)
    if not nodes:
        raise UsageError("No JSON-LD nodes produced by morph-kgc.")

    target = normalize_type(target_type) if target_type else None
    main_node: dict[str, Any] | None = None
    main_old_id = "_:b0"
    for idx, node in enumerate(nodes):
        node_type = _extract_type(node)
        if target and node_type == target:
            main_node = node
            main_old_id = str(node.get("@id") or f"_:b{idx}")
            break
    if main_node is None:
        main_node = nodes[0]
        main_old_id = str(main_node.get("@id") or "_:b0")

    id_map = _build_id_map(nodes, dataset_uri, url)
    node_map: dict[str, dict[str, Any]] = {}
    for idx, node in enumerate(nodes):
        old_id = str(node.get("@id") or f"_:b{idx}")
        new_id = id_map[old_id]
        node["@id"] = new_id
        node_map[new_id] = node

    for node in nodes:
        for key, value in list(node.items()):
            if key in ("@id", "@type"):
                continue
            node[key] = _rewrite_refs(value, id_map, node_map)

    main_id = id_map.get(main_old_id)
    if not main_id:
        raise UsageError("Failed to resolve main node @id.")
    main = node_map[main_id]
    main["@context"] = _SCHEMA_BASE
    return main


def generate_from_agent(
    url: str,
    html: str,
    api_key: str,
    dataset_uri: str,
    target_type: str | None,
    workdir: Path,
    debug: bool = False,
) -> tuple[str, dict[str, Any]]:
    debug_path = workdir / "agent_debug.json" if debug else None
    yarrml = ask_agent_for_yarrml(
        api_key, url, html, target_type, debug=debug, debug_path=debug_path
    )
    workdir.mkdir(parents=True, exist_ok=True)
    html_path = (workdir / "rendered.html").resolve()
    html_path.write_text(html)
    file_uri = html_path.as_uri()
    yarrml = _normalize_agent_yarrml(yarrml, url, file_uri, target_type)
    yarrml_path = workdir / "mapping.yarrml"
    rml_path = workdir / "mapping.ttl"
    yarrml_path.write_text(yarrml)
    _run_yarrrml_parser(yarrml_path, rml_path)
    jsonld_raw = _materialize_jsonld(rml_path)
    jsonld = normalize_jsonld(jsonld_raw, dataset_uri, url, target_type)
    return yarrml, jsonld
