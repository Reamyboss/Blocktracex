from pathlib import Path

from btx.project_files import declared_dependencies, iter_python_files

# Checked in order: web frameworks first, so a FastAPI service that also
# ships a Typer CLI is reported as FastAPI.
KNOWN_FRAMEWORKS = [
    ("django", "Django"),
    ("fastapi", "FastAPI"),
    ("flask", "Flask"),
    ("litestar", "Litestar"),
    ("sanic", "Sanic"),
    ("tornado", "Tornado"),
    ("aiohttp", "aiohttp"),
    ("pyramid", "Pyramid"),
    ("streamlit", "Streamlit"),
    ("typer", "Typer"),
    ("click", "Click"),
]

NO_FRAMEWORK = "None detected"

PYTHON_PROJECT_MARKERS = ["pyproject.toml", "setup.py", "setup.cfg"]


def detect_framework(dependencies: set[str]) -> str:
    for package, framework in KNOWN_FRAMEWORKS:
        if package in dependencies:
            return framework

    return NO_FRAMEWORK


def detect_language(root: Path) -> str:
    has_marker = any((root / marker).exists() for marker in PYTHON_PROJECT_MARKERS)
    has_requirements = any(root.glob("requirements*.txt"))
    has_python_files = next(iter_python_files(root), None) is not None

    if has_marker or has_requirements or has_python_files:
        return "Python"

    return "Unknown"


def detect_architecture(root: Path | None = None):
    """
    Detect the target project's architecture characteristics.

    If no root is supplied, the current working directory is used.
    """

    if root is None:
        root = Path.cwd()

    language = detect_language(root)

    framework = detect_framework(declared_dependencies(root))

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
