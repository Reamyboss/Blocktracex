from pathlib import Path
import tomllib

from rich import print


def show_project_info():
    """Display information about the current Blocktracex project."""

    config_file = Path.cwd() / "btx.toml"

    if not config_file.exists():
        print("[red]❌ No btx.toml found in this directory.[/red]")
        return

    with config_file.open("rb") as f:
        config = tomllib.load(f)

    print(f"[bold cyan]📦 Project:[/bold cyan] {config['project']['name']}")
    print(f"[bold green]🚀 Version:[/bold green] {config['project']['version']}")
    print(f"[bold yellow]🐍 Python:[/bold yellow] {config['python']['version']}")
    print(f"[bold magenta]🔧 Git:[/bold magenta] {config['git']['enabled']}")
