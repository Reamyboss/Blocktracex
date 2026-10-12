from pathlib import Path

from rich import print

from btx.report import print_validation_summary
from btx.scoring import calculate_score

REQUIRED_DIRS = [
    "docs",
    "src",
    "tests",
    "scripts",
    "notebooks",
    "data",
]


def check_project(root: Path | None = None) -> dict:
    """
    Check the target project's structure without printing anything.

    If no root is supplied, the current working directory is used.
    """

    if root is None:
        root = Path.cwd()

    checks = [
        {"name": "btx.toml", "kind": "file", "passed": (root / "btx.toml").exists()}
    ]

    for directory in REQUIRED_DIRS:
        checks.append(
            {
                "name": directory,
                "kind": "directory",
                "passed": (root / directory).exists(),
            }
        )

    passed = sum(check["passed"] for check in checks)
    failed = len(checks) - passed

    return {
        "valid": failed == 0,
        "passed": passed,
        "failed": failed,
        "score": calculate_score(passed, failed),
        "checks": checks,
        "missing": [check["name"] for check in checks if not check["passed"]],
    }


def validate_project(root: Path | None = None):
    """
    Validate the target project's structure and print the results.

    If no root is supplied, the current working directory is used.
    """

    result = check_project(root)

    for check in result["checks"]:
        name = check["name"]

        if check["passed"]:
            found = " found" if check["kind"] == "file" else ""
            print(f"[green]✔ {name}{found}[/green]")
        elif check["kind"] == "file":
            print(f"[red]❌ No {name} found[/red]")
        else:
            print(f"[red]❌ {name}[/red]")

    print_validation_summary(
        passed=result["passed"],
        failed=result["failed"],
        missing_items=result["missing"],
    )

    return result["valid"]
