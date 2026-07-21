from rich import print


def print_recommendations(missing_items: list[str]) -> None:
    """
    Display recommendations based on missing project items.
    """

    if not missing_items:
        print(
            "\n[bold green]🎉 No recommendations. Your project looks great![/bold green]"
        )
        return

    print("\n[bold yellow]💡 Recommendations[/bold yellow]")

    for item in missing_items:
        print(f" • Create the [cyan]{item}[/cyan].")
