from pathlib import Path

from btx.architecture import detect_architecture


def test_default_root_matches_explicit_cwd():
    """No argument must behave exactly like passing the current directory."""

    assert detect_architecture() == detect_architecture(Path.cwd())


def test_explicit_path_analyzes_supplied_project(tmp_path):
    project = tmp_path / "python_project"
    project.mkdir()

    (project / "pyproject.toml").write_text("[project]\nname = 'x'\n")
    (project / "tests").mkdir()
    (project / "src").mkdir()
    (project / "README.md").write_text("# X\n")

    architecture = detect_architecture(project)

    assert architecture["language"] == "Python"
    assert architecture["testing"] == "pytest"
    assert architecture["documentation"] is True
    assert architecture["package_layout"] is True


def test_bare_directory_reports_missing_signals(tmp_path):
    project = tmp_path / "bare_project"
    project.mkdir()

    architecture = detect_architecture(project)

    assert architecture["language"] == "Unknown"
    assert architecture["testing"] == "None"
    assert architecture["documentation"] is False
    assert architecture["package_layout"] is False
