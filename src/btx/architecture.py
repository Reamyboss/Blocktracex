from pathlib import Path


def detect_architecture(root: Path | None = None):
    """
    Detect the target project's architecture characteristics.

    If no root is supplied, the current working directory is used.
    """

    if root is None:
        root = Path.cwd()

    language = "Python" if (root / "pyproject.toml").exists() else "Unknown"

    framework = "Typer"

    testing = "pytest" if (root / "tests").exists() else "None"

    documentation = (root / "README.md").exists()

    package_layout = (root / "src").exists()

    return {
        "language": language,
        "framework": framework,
        "testing": testing,
        "documentation": documentation,
        "package_layout": package_layout,
    }
