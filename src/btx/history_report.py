from rich.console import Console
from rich.table import Table

from btx.history import load_history

console = Console()


def print_history():
    """
    Display engineering history.
    """

    history = load_history()

    if not history:
        console.print("[yellow]No engineering history found.[/yellow]")
        return

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
