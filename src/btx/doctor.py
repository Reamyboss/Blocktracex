import platform
import shutil

from rich import print


def check(tool: str):
    if shutil.which(tool):
        print(f"[green]✔[/green] {tool}")
    else:
        print(f"[red]✘[/red] {tool} (Not Found)")


def run_doctor():
    print("\n[bold cyan]🔍 Blocktracex Environment Check[/bold cyan]\n")

    print(f"Operating System: {platform.system()} {platform.release()}\n")

    check("python")
    check("git")
    check("pip")
    check("code")

    print("\n[bold green]Environment scan complete.[/bold green]")
