import typer
from rich import print
from btx.inspect import inspect_project
from btx.inspect_report import print_inspection_report

from btx.scaffold import create_project
from btx.doctor import run_doctor
from btx.init import init_project
from btx.info import show_project_info
from btx.validate import validate_project

app = typer.Typer(
    name="btx",
    help="Blocktracex Developer CLI\n\nBuild • Transform • eXecute.",
    no_args_is_help=True,
    rich_markup_mode="rich",
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
def doctor():
    """Check the development environment."""
    run_doctor()


@app.command()
def validate():
    """Validate the current Blocktracex project."""
    validate_project()
    

@app.command()
def init():
    """Initialize the current directory."""
    init_project()


@app.command()
def info():
    """Display information about the current project."""
    show_project_info()

@app.command()
def inspect():
    """
    Inspect the current Blocktracex project.
    """

    project = inspect_project()
    print_inspection_report(project)
    
if __name__ == "__main__":
    app()