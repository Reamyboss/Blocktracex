import subprocess
from pathlib import Path

from rich import print

from btx.config import create_config
from btx.templates import (
    CHANGELOG_TEMPLATE,
    CONTRIBUTING_TEMPLATE,
    GITIGNORE_TEMPLATE,
    LICENSE_TEMPLATE,
    README_TEMPLATE,
)

PROJECT_FOLDERS = [
    "docs",
    "src",
    "tests",
    "scripts",
    "notebooks",
    "data/raw",
    "data/processed",
]


def create_project(name: str):
    root = Path(name)

    if root.exists():
        print(f"[red]❌ Project '{name}' already exists.[/red]")
        return

    root.mkdir(parents=True)

    print("[bold cyan]🚀 Creating Blocktracex project...[/bold cyan]\n")

    # Create folders
    for folder in PROJECT_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)
        print(f"[green]✔[/green] {folder}")

    # Create files
    (root / "README.md").write_text(
        README_TEMPLATE.format(name=name),
        encoding="utf-8",
    )

    (root / ".gitignore").write_text(
        GITIGNORE_TEMPLATE,
        encoding="utf-8",
    )

    (root / "CHANGELOG.md").write_text(
        CHANGELOG_TEMPLATE,
        encoding="utf-8",
    )

    (root / "CONTRIBUTING.md").write_text(
        CONTRIBUTING_TEMPLATE,
        encoding="utf-8",
    )

    (root / "LICENSE").write_text(
        LICENSE_TEMPLATE,
        encoding="utf-8",
    )

    (root / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    create_config(root, name)

    # Initialize Git
    try:
        subprocess.run(
            ["git", "init"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        print("[green]✔[/green] Git initialized")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[yellow]⚠ Git initialization skipped[/yellow]")

    print("\n[bold green]🎉 Project created successfully![/bold green]")
