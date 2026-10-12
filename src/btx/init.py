from pathlib import Path

from rich import print

from btx.config import create_config


def init_project(root: Path | None = None) -> bool:
    """
    Add a Blocktracex configuration (btx.toml) to an existing project.

    Never overwrites an existing btx.toml. Returns True when a file
    was created.
    """

    if root is None:
        root = Path.cwd()

    if (root / "btx.toml").exists():
        print("[yellow]⚠ btx.toml already exists. Nothing to do.[/yellow]")
        return False

    create_config(root, root.name)
    print(f"[green]✔ Created btx.toml for '{root.name}'[/green]")
    return True
