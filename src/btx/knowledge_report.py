from rich.console import Console
from rich.table import Table

console = Console()


def print_knowledge_report(knowledge: dict):
    """
    Display structured project knowledge.
    """

    table = Table(title="BLOCKTRACEX PROJECT KNOWLEDGE")

    table.add_column("Knowledge", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    for key, value in knowledge.items():
        label = key.replace("_", " ").title()
        table.add_row(label, str(value))

    console.print(table)