from pathlib import Path
import sys

import typer
from rich import print

from btx.architecture import detect_architecture
from btx.architecture_report import print_architecture_report
from btx.coach import build_engineering_coach
from btx.coach_report import print_coach_report
from btx.doctor import run_doctor
from btx.info import show_project_info
from btx.init import init_project
from btx.inspect import inspect_project
from btx.inspect_report import print_inspection_report
from btx.knowledge import build_project_knowledge
from btx.knowledge_report import print_knowledge_report
from btx.scaffold import create_project
from btx.validate import validate_project
from btx.roadmap import build_roadmap
from btx.dashboard_report import print_dashboard_report
from btx.history import save_engineering_snapshot
from btx.history_report import print_history


def _ensure_utf8_console_output() -> None:
    """
    Every report module builds its own rich Console() with no explicit
    file=, so each one resolves sys.stdout/sys.stderr lazily at print time.
    Reconfiguring those two streams once, here, before any command runs,
    is therefore enough to fix all of them without touching a single
    report module.

    Windows-only: when stdout/stderr aren't attached to a native console
    (piped output, redirected output, or a non-native terminal such as
    Git Bash/MSYS2), Python falls back to the legacy ANSI codepage
    (commonly cp1252), which cannot encode the emoji used throughout the
    reports and raises UnicodeEncodeError. UTF-8 can encode every
    character Blocktracex prints, so this removes the failure mode
    instead of hiding it. macOS/Linux terminals are already UTF-8 and are
    left untouched.
    """

    if sys.platform != "win32":
        return

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


_ensure_utf8_console_output()

app = typer.Typer(
    name="btx",
    help="Blocktracex Developer CLI\n\nBuild • Transform • eXecute.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# Single, shared definition of the "which project am I analyzing" input.
# Every analysis command binds this the same way, so the resolved path is
# always sourced consistently before being passed down to the engines.
PROJECT_PATH_OPTION = typer.Option(
    Path("."),
    "--path",
    "-p",
    exists=True,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
    help="Path to the project to analyze (defaults to the current directory).",
)


@app.command()
def version():
    """Show the current CLI version."""
    print("[bold green]🚀 Blocktracex CLI v0.1.0[/bold green]")


@app.command()
def hello():
    """Say hello."""
    print("[bold blue]Hello from Blocktracex![/bold blue]")


@app.command()
def new(name: str):
    """Create a new Blocktracex project."""
    create_project(name)


@app.command()
def init():
    """Initialize the current directory."""
    init_project()


@app.command()
def doctor():
    """Check the development environment."""
    run_doctor()


@app.command()
def validate(path: Path = PROJECT_PATH_OPTION):
    """Validate the target Blocktracex project."""
    validate_project(path)


@app.command()
def info():
    """Display information about the current project."""
    show_project_info()


@app.command()
def inspect(path: Path = PROJECT_PATH_OPTION):
    """
    Inspect the target Blocktracex project.
    """
    project = inspect_project(path)
    print_inspection_report(project)


@app.command()
def architecture(path: Path = PROJECT_PATH_OPTION):
    """
    Analyze the target project's architecture.
    """
    architecture = detect_architecture(path)
    print_architecture_report(architecture)


@app.command()
def knowledge(path: Path = PROJECT_PATH_OPTION):
    """
    Generate structured knowledge about the target project.
    """
    project = inspect_project(path)

    knowledge = build_project_knowledge(project)

    print_knowledge_report(knowledge)


@app.command()
def coach(path: Path = PROJECT_PATH_OPTION):
    """
    Generate engineering coaching for the target project.
    """
    project = inspect_project(path)

    knowledge = build_project_knowledge(project)

    coaching = build_engineering_coach(knowledge)

    print_coach_report(coaching)


@app.command()
def dashboard(path: Path = PROJECT_PATH_OPTION):
    """
    Display the complete engineering dashboard.
    """

    project = inspect_project(path)

    knowledge = build_project_knowledge(project)

    save_engineering_snapshot(knowledge)

    coaching = build_engineering_coach(knowledge)

    roadmap = build_roadmap(knowledge)

    print_dashboard_report(
        project,
        knowledge,
        coaching,
        roadmap,
    )


@app.command()
def history():
    """
    Display engineering history.
    """

    print_history()


if __name__ == "__main__":
    app()
