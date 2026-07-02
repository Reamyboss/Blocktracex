from rich.console import Console
from rich.table import Table

console = Console()


def print_inspection_report(project: dict):
    """
    Display project inspection information.
    """

    table = Table(
        title="BLOCKTRACEX PROJECT INSPECTION",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property", style="green")
    table.add_column("Value", style="white")

    table.add_row("Project Name", project["project_name"])
    table.add_row("Python Version", project["python_version"])
    table.add_row("Git Repository", "Yes" if project["git"] else "No")
    table.add_row("BTX Config", "Found" if project["btx_config"] else "Missing")
    table.add_row("Source Files", str(project["source_files"]))
    table.add_row("Test Files", str(project["test_files"]))

    console.print(table)