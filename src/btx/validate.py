from pathlib import Path

from rich import print

from btx.report import print_validation_summary


def validate_project(root: Path | None = None):
    """
    Validate the target project's structure.

    If no root is supplied, the current working directory is used.
    """

    if root is None:
        root = Path.cwd()

    config = root / "btx.toml"

    project_is_valid = True

    passed = 0
    failed = 0
    missing_items = []

    # --------------------------------------------------
    # Validate configuration file
    # --------------------------------------------------

    if config.exists():
        print("[green]✔ btx.toml found[/green]")
        passed += 1
    else:
        print("[red]❌ No btx.toml found[/red]")
        failed += 1
        missing_items.append("btx.toml")
        project_is_valid = False

    # --------------------------------------------------
    # Required project directories
    # --------------------------------------------------

    required_dirs = [
        "docs",
        "src",
        "tests",
        "scripts",
        "notebooks",
        "data",
    ]

    # --------------------------------------------------
    # Validate directories
    # --------------------------------------------------

    for directory in required_dirs:

        path = root / directory

        if path.exists():
            print(f"[green]✔ {directory}[/green]")
            passed += 1
        else:
            print(f"[red]❌ {directory}[/red]")
            failed += 1
            missing_items.append(directory)
            project_is_valid = False

    # --------------------------------------------------
    # Print summary
    # --------------------------------------------------

    print_validation_summary(
        passed=passed,
        failed=failed,
        missing_items=missing_items,
    )

    return project_is_valid
