import json
from importlib.metadata import version as package_version
from pathlib import Path

import typer

# Bump when a payload's shape changes in a way consumers must handle.
SCHEMA_VERSION = 1

JSON_OPTION = typer.Option(
    False,
    "--json",
    help="Print machine-readable JSON instead of the report.",
)


def _to_jsonable(value):
    if isinstance(value, Path):
        return str(value)

    if isinstance(value, (set, frozenset)):
        return sorted(value)

    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def build_payload(command: str, data) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "btx_version": package_version("blocktracex-cli"),
        "command": command,
        "data": data,
    }


def emit_json(command: str, data) -> None:
    """
    Print a command's result as JSON on stdout and nothing else,
    so the output can be piped straight into other tools.
    """

    payload = build_payload(command, data)

    typer.echo(json.dumps(payload, indent=2, ensure_ascii=False, default=_to_jsonable))
