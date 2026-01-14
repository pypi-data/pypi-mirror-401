"""CLI for structured data generation."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from worai.core.structured_data import (
    RenderOptions,
    StructuredDataOptions,
    StructuredDataResult,
    generate_from_agent,
    get_dataset_uri,
    render_html,
)
from worai.core.wordlift import resolve_api_key
from worai.errors import UsageError

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _default_output_paths(out_dir: Path, base_name: str) -> tuple[Path, Path]:
    jsonld_path = out_dir / f"{base_name}.jsonld"
    yarrml_path = out_dir / f"{base_name}.yarrml"
    return jsonld_path, yarrml_path


@app.command("create")
def create(
    ctx: typer.Context,
    url: str = typer.Argument(..., help="Target page URL."),
    target_type_arg: str | None = typer.Argument(
        None, help="Schema.org type to generate (e.g., Review)."
    ),
    target_type: str | None = typer.Option(
        None, "--type", help="Schema.org type to generate (e.g., Review)."
    ),
    output_dir: Path = typer.Option(Path("."), "--output-dir", help="Output directory."),
    base_name: str = typer.Option("structured-data", "--base-name", help="Base output filename."),
    jsonld_path: Path | None = typer.Option(
        None, "--jsonld", help="Write JSON-LD to this file path."
    ),
    yarrml_path: Path | None = typer.Option(
        None, "--yarrml", help="Write YARRRML to this file path."
    ),
    debug: bool = typer.Option(False, "--debug", help="Write agent prompt/response to disk."),
    headed: bool = typer.Option(False, "--headed", help="Run the browser with a visible UI."),
    timeout_ms: int = typer.Option(30000, "--timeout-ms", help="Timeout (ms) for page loads."),
    wait_until: str = typer.Option(
        "domcontentloaded",
        "--wait-until",
        help="Playwright wait strategy.",
    ),
) -> None:
    api_key = resolve_api_key(ctx.obj.get("config") if ctx.obj else None)
    if not api_key:
        raise UsageError("WORDLIFT_KEY is required (or set wordlift.api_key in config).")

    if target_type is None:
        target_type = target_type_arg

    dataset_uri = get_dataset_uri(api_key)

    render_options = RenderOptions(
        url=url,
        headless=not headed,
        timeout_ms=timeout_ms,
        wait_until=wait_until,
    )
    html = render_html(render_options)

    options = StructuredDataOptions(
        url=url,
        target_type=target_type,
        dataset_uri=dataset_uri,
        headless=not headed,
        timeout_ms=timeout_ms,
        wait_until=wait_until,
    )

    workdir = output_dir / ".structured-data"
    yarrml, jsonld = generate_from_agent(
        options.url,
        html,
        api_key,
        options.dataset_uri,
        options.target_type,
        workdir,
        debug=debug,
    )

    if jsonld_path is None or yarrml_path is None:
        jsonld_path, yarrml_path = _default_output_paths(output_dir, base_name)

    _write_output(jsonld_path, json.dumps(jsonld, indent=2))
    _write_output(yarrml_path, yarrml)

    result = StructuredDataResult(
        jsonld=jsonld,
        yarrml=yarrml,
        jsonld_filename=str(jsonld_path),
        yarrml_filename=str(yarrml_path),
    )
    typer.echo(json.dumps(result.__dict__, indent=2))
