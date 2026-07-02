from pathlib import Path
import platform


def inspect_project():
    """
    Collect information about the current project.
    """

    root = Path.cwd()

    project_name = root.name
    python_version = platform.python_version()

    git_exists = (root / ".git").exists()
    config_exists = (root / "btx.toml").exists()

    source_files = len(list(root.glob("src/**/*.py")))
    test_files = len(list(root.glob("tests/**/*.py")))

    return {
        "project_name": project_name,
        "python_version": python_version,
        "git": git_exists,
        "btx_config": config_exists,
        "source_files": source_files,
        "test_files": test_files,
    }