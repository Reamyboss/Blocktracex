from pathlib import Path

from btx.validate import validate_project

REQUIRED_DIRS = ("docs", "src", "tests", "scripts", "notebooks", "data")


def test_default_root_matches_explicit_cwd():
    """No argument must behave exactly like passing the current directory."""

    assert validate_project() == validate_project(Path.cwd())


def test_complete_external_project_passes(tmp_path):
    project = tmp_path / "complete_project"
    project.mkdir()

    (project / "btx.toml").write_text("[project]\nname = 'x'\n")
    for directory in REQUIRED_DIRS:
        (project / directory).mkdir()

    assert validate_project(project) is True


def test_incomplete_external_project_fails(tmp_path):
    project = tmp_path / "incomplete_project"
    project.mkdir()

    assert validate_project(project) is False
