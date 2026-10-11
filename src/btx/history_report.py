import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

HISTORY_FILE = Path.home() / ".btx_history.json"


def print_history():
    """
    Display engineering history.
    """

    if not HISTORY_FILE.exists():
        console.print("[yellow]No engineering history found.[/yellow]")
        return

    history = json.loads(HISTORY_FILE.read_text())

    table = Table(
        title="📈 Engineering Timeline",
        expand=True,
    )

    table.add_column("Date")
    table.add_column("Health")
    table.add_column("Maturity")
    table.add_column("Risk")

    for snapshot in history[-10:]:

        table.add_row(
            snapshot["timestamp"][:19],
            snapshot["health_score"],
            snapshot["maturity"],
            snapshot["risk"],
        )

    console.print(table)
