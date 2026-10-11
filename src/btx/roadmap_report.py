from rich.console import Console
from rich.table import Table

console = Console()


def print_roadmap_report(roadmap: dict):
    """
    Display the engineering roadmap.
    """

    table = Table(
        title="🗺 BLOCKTRACEX ENGINEERING ROADMAP",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column(
        "Roadmap",
        style="bold cyan",
        no_wrap=True,
    )

    table.add_column(
        "Plan",
        style="bold green",
    )

    for key, value in roadmap.items():
        label = key.replace("_", " ").title()

        if isinstance(value, list):
            formatted = "\n".join(f"• {item}" for item in value)

        elif key == "immediate_goal":
            formatted = f"[bold yellow]★ {value}[/bold yellow]"

        elif key == "estimated_impact":
            formatted = f"[bold green]{value}[/bold green]"

        else:
            formatted = str(value)

        table.add_row(label, formatted)

    console.print(table)

    console.print(
        "\n[bold blue]Engineering roadmap generated successfully.[/bold blue]"
    )
