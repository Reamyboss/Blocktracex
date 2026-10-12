import platform
from pathlib import Path

from btx.project_files import is_test_file, iter_python_files


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

    source_files = 0
    test_files = 0

    for path in iter_python_files(root):
        if is_test_file(path, root):
            test_files += 1
        else:
            source_files += 1

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
