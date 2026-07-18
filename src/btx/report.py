
from btx.scoring import calculate_score
from btx.recommend import print_recommendations
from rich.console import Console

console = Console()

def print_validation_summary(
    passed: int,
    failed: int,
    missing_items: list[str],
):
    """
    Print the validation summary, project health,
    and recommendations.
    """
    from btx.dashboard import print_dashboard
    score = calculate_score(passed, failed)
    
    print_dashboard(score)

    console.rule("[bold cyan]BLOCKTRACEX VALIDATION")
    console.print("[bold cyan]Validation Summary[/bold cyan]\n")

    console.print(f"[green]✔ Passed:[/green] {passed}")
    console.print(f"[red]❌ Failed:[/red] {failed}")

    console.print(f"\n[bold cyan]📊 Project Health: {score}%[/bold cyan]")

    if failed == 0:
        console.print("\n[bold green]✅ Overall Status: PASSED[/bold green]")
    else:
        console.print("\n[bold red]❌ Overall Status: FAILED[/bold red]")

    print_recommendations(missing_items)