"""CLI for structured data generation."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from worai.core.structured_data import (
    CleanupOptions,
    RenderOptions,
    StructuredDataOptions,
    StructuredDataResult,
    clean_xhtml,
    generate_from_agent,
    get_dataset_uri,
    render_html,
    shape_specs_for_type,
)
from worai.core.validate_shacl import validate_file
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


def _echo_debug(debug_path: Path) -> None:
    if not debug_path.exists():
        return
    try:
        payload = json.loads(debug_path.read_text())
    except Exception:
        typer.echo(f"Debug output written to {debug_path}", err=True)
        return
    prompt = payload.get("prompt", "")
    response = payload.get("response")
    typer.echo("--- Agent prompt ---", err=True)
    typer.echo(prompt, err=True)
    typer.echo("--- Agent response ---", err=True)
    typer.echo(json.dumps(response, indent=2), err=True)


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
    max_retries: int = typer.Option(
        2, "--max-retries", help="Max retries for agent refinement when required props are missing."
    ),
    max_xhtml_chars: int = typer.Option(
        40000, "--max-xhtml-chars", help="Max characters to keep in cleaned XHTML."
    ),
    max_text_node_chars: int = typer.Option(
        400, "--max-text-node-chars", help="Max characters per text node in cleaned XHTML."
    ),
    max_nesting_depth: int = typer.Option(
        2, "--max-nesting-depth", help="Max depth for related types in the schema guide."
    ),
    verbose: bool = typer.Option(
        True, "--verbose/--no-verbose", help="Emit progress logs to stderr."
    ),
    validate: bool = typer.Option(
        False, "--validate", help="Validate JSON-LD output with SHACL shapes."
    ),
    wait_until: str = typer.Option(
        "networkidle",
        "--wait-until",
        help="Playwright wait strategy.",
    ),
) -> None:
    api_key = resolve_api_key(ctx.obj.get("config") if ctx.obj else None)
    if not api_key:
        raise UsageError("WORDLIFT_KEY is required (or set wordlift.api_key in config).")

    if target_type is None:
        target_type = target_type_arg
    if not target_type:
        raise UsageError("Schema.org type is required. Pass it as an argument or via --type.")

    dataset_uri = get_dataset_uri(api_key)

    render_options = RenderOptions(
        url=url,
        headless=not headed,
        timeout_ms=timeout_ms,
        wait_until=wait_until,
    )
    def log(message: str) -> None:
        if verbose:
            typer.echo(message, err=True)

    log("Rendering page with Playwright...")
    rendered = render_html(render_options)

    log("Cleaning XHTML for prompt usage...")
    cleanup_options = CleanupOptions(
        max_xhtml_chars=max_xhtml_chars,
        max_text_node_chars=max_text_node_chars,
    )
    cleaned_xhtml = clean_xhtml(rendered.xhtml, cleanup_options)

    options = StructuredDataOptions(
        url=url,
        target_type=target_type,
        dataset_uri=dataset_uri,
        headless=not headed,
        timeout_ms=timeout_ms,
        wait_until=wait_until,
        max_retries=max_retries,
        max_xhtml_chars=max_xhtml_chars,
        max_text_node_chars=max_text_node_chars,
        max_nesting_depth=max_nesting_depth,
        verbose=verbose,
    )

    workdir = output_dir / ".structured-data"
    debug_path = workdir / "agent_debug.json"
    try:
        log("Generating YARRRML mapping and JSON-LD...")
        yarrml, jsonld = generate_from_agent(
            options.url,
            rendered.html,
            rendered.xhtml,
            cleaned_xhtml,
            api_key,
            options.dataset_uri,
            options.target_type,
            workdir,
            debug=debug,
            max_retries=options.max_retries,
            max_nesting_depth=options.max_nesting_depth,
            log=log,
        )
    except Exception:
        if debug:
            _echo_debug(debug_path)
        raise
    if debug:
        _echo_debug(debug_path)

    if jsonld_path is None or yarrml_path is None:
        jsonld_path, yarrml_path = _default_output_paths(output_dir, base_name)

    _write_output(jsonld_path, json.dumps(jsonld, indent=2))
    _write_output(yarrml_path, yarrml)

    if verbose:
        mapping_validation_path = workdir / "mapping.validation.json"
        if mapping_validation_path.exists():
            try:
                validation_payload = json.loads(mapping_validation_path.read_text())
            except Exception:
                validation_payload = {}
            for warning in validation_payload.get("warnings", []):
                if "reviewRating dropped" in warning:
                    typer.echo(warning, err=True)

    if validate:
        log("Validating JSON-LD output...")
        shape_specs = shape_specs_for_type(options.target_type)
        result = validate_file(str(jsonld_path), shape_specs=shape_specs)
        (workdir / "jsonld.validation.json").write_text(
            json.dumps(
                {
                    "conforms": result.conforms,
                    "warning_count": result.warning_count,
                    "report_text": result.report_text,
                },
                indent=2,
            )
        )
        typer.echo(result.report_text, err=True)

    result = StructuredDataResult(
        jsonld=jsonld,
        yarrml=yarrml,
        jsonld_filename=str(jsonld_path),
        yarrml_filename=str(yarrml_path),
    )
    typer.echo(json.dumps(result.__dict__, indent=2))
