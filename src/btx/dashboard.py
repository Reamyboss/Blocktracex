from rich.console import Console

console = Console()


def print_dashboard(score: int):
    """
    Display a visual project health dashboard.
    """

    filled = score // 5
    empty = 20 - filled

    bar = "█" * filled + "░" * empty

    console.print("\n[bold cyan]Project Health[/bold cyan]")
    console.print(f"[green]{bar}[/green] {score}%")
    if score >= 90:
        status = "[bold green]🟢 Excellent[/bold green]"
    elif score >= 70:
        status = "[bold yellow]🟡 Good[/bold yellow]"
    elif score >= 50:
        status = "[bold orange3]🟠 Fair[/bold orange3]"
    else:
        status = "[bold red]🔴 Needs Attention[/bold red]"

    console.print(status)
