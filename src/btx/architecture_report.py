from rich.console import Console
from rich.table import Table

console = Console()


def print_architecture_report(architecture: dict):
    """
    Display the detected project architecture.
    """

    table = Table(
        title="BLOCKTRACEX ARCHITECTURE REPORT",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property", style="green")
    table.add_column("Value", style="white")

    table.add_row("Language", architecture["language"])
    table.add_row("Framework", architecture["framework"])
    table.add_row("Testing", architecture["testing"])

    table.add_row(
        "Documentation",
        "Present" if architecture["documentation"] else "Missing",
    )

    table.add_row(
        "Package Layout",
        "src/" if architecture["package_layout"] else "Flat",
    )

    console.print(table)
