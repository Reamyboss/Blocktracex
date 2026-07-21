from pathlib import Path


def detect_architecture():
    """
    Detect the project's architecture characteristics.
    """

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
