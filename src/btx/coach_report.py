from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_coach_report(coaching: dict):
    """
    Display the Engineering Coach report.
    """

    table = Table(show_header=False)

    table.add_column("Item", style="bold cyan", width=22)
    table.add_column("Value", style="bold green")

    table.add_row(
        "Next Action",
        f"[bold yellow]★ {coaching['next_action']}[/bold yellow]",
    )

    table.add_row(
        "Estimated Impact",
        f"[bold green]{coaching['impact']}[/bold green]",
    )

    table.add_row(
        "Estimated Effort",
        coaching["estimated_effort"],
    )

    table.add_row(
        "Why",
        coaching["why"],
    )

    table.add_row(
        "First Step",
        coaching["first_step"],
    )

    console.print(
        Panel.fit(
            table,
            title="🎯 ENGINEERING COACH",
            border_style="cyan",
        )
    )

    console.print(
        "\n[bold blue]Engineering coaching generated successfully.[/bold blue]"
    )
