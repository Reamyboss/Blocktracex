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
        # Machine-readable copy of engineering_health_score, for --json only.
        if key == "engineering_health_value":
            continue

        label = key.replace("_", " ").title()

        if label == "Knowledge Version":
            label = "Engine Version"

        # Render values
        if isinstance(value, list):
            formatted = "\n".join(f"• {item}" for item in value)

        elif key == "engineering_verdict":
            formatted = f"[bold cyan]{value}[/bold cyan]"

        elif key == "next_best_action":
            formatted = f"[bold yellow]★ {value}[/bold yellow]"

        elif key == "estimated_impact":
            formatted = f"[bold green]{value}[/bold green]"

        else:
            formatted = str(value)

        table.add_row(label, formatted)

    console.print(table)

    console.print(
        "\n[bold blue]Engineering insight generated successfully.[/bold blue]"
    )
