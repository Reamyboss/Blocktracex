import configparser
import os
import re
import tomllib
from collections.abc import Iterator
from pathlib import Path

# Directories that never contain the project's own code.
IGNORED_DIRS = {
    "__pycache__",
    "build",
    "dist",
    "env",
    "node_modules",
    "site-packages",
    "venv",
}

TEST_DIRS = {"test", "tests"}

_REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def _is_ignored_dir(name: str) -> bool:
    # Hidden directories cover .git, .venv, .tox and the tool caches.
    return name.startswith(".") or name in IGNORED_DIRS or name.endswith(".egg-info")


def iter_python_files(root: Path) -> Iterator[Path]:
    """
    Yield every Python file in the project, skipping virtualenvs,
    build output, caches and hidden directories.
    """

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not _is_ignored_dir(d))

        for filename in sorted(filenames):
            if filename.endswith(".py"):
                yield Path(dirpath) / filename


def is_test_file(path: Path, root: Path) -> bool:
    """
    A file is a test if it lives under a tests/ directory or follows
    the pytest naming convention (test_*.py or *_test.py).
    """

    relative = path.relative_to(root)

    if any(part in TEST_DIRS for part in relative.parts[:-1]):
        return True

    return path.name.startswith("test_") or path.stem.endswith("_test")


def normalize_package_name(name: str) -> str:
    """Normalize a distribution name as described in PEP 503."""

    return re.sub(r"[-_.]+", "-", name).lower()


def _requirement_name(requirement: str) -> str | None:
    match = _REQUIREMENT_NAME.match(requirement)

    if match is None:
        return None

    return normalize_package_name(match.group(1))


def _pyproject_requirements(root: Path) -> list[str]:
    try:
        data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return []

    requirements = list(data.get("project", {}).get("dependencies", []))

    poetry = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    requirements.extend(name for name in poetry if name.lower() != "python")

    return requirements


def _requirements_txt(root: Path) -> list[str]:
    requirements = []

    for path in sorted(root.glob("requirements*.txt")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue

        for line in lines:
            line = line.strip()

            # Skip comments and pip options such as -r, -e and --index-url.
            if line and not line.startswith(("#", "-")):
                requirements.append(line)

    return requirements


def _setup_cfg_requirements(root: Path) -> list[str]:
    parser = configparser.ConfigParser()

    try:
        parser.read(root / "setup.cfg", encoding="utf-8")
    except (configparser.Error, UnicodeDecodeError):
        return []

    install_requires = parser.get("options", "install_requires", fallback="")

    return [line for line in install_requires.splitlines() if line.strip()]


def declared_dependencies(root: Path) -> set[str]:
    """
    Return the normalized names of the project's runtime dependencies,
    read from pyproject.toml, requirements*.txt and setup.cfg.

    Optional extras are ignored: they describe add-ons, not the
    project's own stack.
    """

    requirements = (
        _pyproject_requirements(root)
        + _requirements_txt(root)
        + _setup_cfg_requirements(root)
    )

    names = (_requirement_name(requirement) for requirement in requirements)

    return {name for name in names if name}
