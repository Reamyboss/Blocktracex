from rich.console import Console
from rich.table import Table

console = Console()


def print_knowledge_report(knowledge: dict):
    """
    Display structured project knowledge.
    """

    table = Table(
        title="🧠 BLOCKTRACEX PROJECT KNOWLEDGE",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column(
        "Knowledge",
        style="bold cyan",
        no_wrap=True,
    )

    table.add_column(
        "Assessment",
        style="bold green",
    )

    for key, value in knowledge.items():
        label = key.replace("_", " ").title()

        if label == "Knowledge Version":
            label = "Engine Version"

        table.add_row(label, str(value))

    console.print(table)

    console.print(
        "\n[bold blue]Engineering insight generated successfully.[/bold blue]"
    )