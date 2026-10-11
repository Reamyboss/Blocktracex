import platform
from pathlib import Path


def inspect_project(root: Path | None = None):
    """
    Collect information about the target project.

    If no root is supplied, the current working directory is used.
    """

    if root is None:
        root = Path.cwd()

    project_name = root.name
    python_version = platform.python_version()

    git_exists = (root / ".git").exists()
    config_exists = (root / "btx.toml").exists()

    source_files = len(list(root.glob("src/**/*.py")))
    test_files = len(list(root.glob("tests/**/*.py")))

    # Documentation
    readme_exists = (root / "README.md").exists()
    changelog_exists = (root / "CHANGELOG.md").exists()
    docs_exists = (root / "docs").exists()

    return {
        "project_name": project_name,
        "python_version": python_version,
        "git": git_exists,
        "btx_config": config_exists,
        "source_files": source_files,
        "test_files": test_files,
        # New inspection fields
        "readme": readme_exists,
        "changelog": changelog_exists,
        "docs": docs_exists,
    }
