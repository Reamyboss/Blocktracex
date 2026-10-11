import re
from importlib.metadata import version as package_version

from typer.testing import CliRunner

from btx.main import app

runner = CliRunner()

ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def test_inspect_default_behavior_still_works():
    """`btx inspect` with no arguments must keep working exactly as before."""

    result = runner.invoke(app, ["inspect"])

    assert result.exit_code == 0
    assert "BLOCKTRACEX PROJECT INSPECTION" in result.stdout


def test_inspect_explicit_path_analyzes_supplied_project(tmp_path):
    """
    Proves the CLI actually uses the supplied --path, not the process cwd:
    the fixture project's name and file counts are asserted directly out
    of the rendered report, and they do not match Blocktracex's own repo.
    """

    external = tmp_path / "sample_external_project"
    (external / "src").mkdir(parents=True)
    (external / "src" / "one.py").write_text("x = 1\n")
    (external / "src" / "two.py").write_text("x = 2\n")
    (external / "src" / "three.py").write_text("x = 3\n")

    result = runner.invoke(app, ["inspect", "--path", str(external)])

    assert result.exit_code == 0
    assert "sample_external_project" in result.stdout
    assert "3" in result.stdout


def test_architecture_and_validate_accept_the_same_explicit_path(tmp_path):
    """Confirms path plumbing is consistent across the other two commands."""

    project = tmp_path / "consistency_check"
    project.mkdir()
    (project / "pyproject.toml").write_text("[project]\nname = 'x'\n")

    architecture_result = runner.invoke(app, ["architecture", "--path", str(project)])
    validate_result = runner.invoke(app, ["validate", "--path", str(project)])

    assert architecture_result.exit_code == 0
    assert "Python" in architecture_result.stdout
    assert validate_result.exit_code == 0


def test_inspect_rejects_nonexistent_path_cleanly(tmp_path):
    """
    An invalid target must fail in a controlled way (a clean Typer/Click
    usage error) rather than an unhandled Python traceback.
    """

    missing = tmp_path / "does-not-exist"

    result = runner.invoke(app, ["inspect", "--path", str(missing)])

    # Rich colors the error panel when it detects CI (e.g. GITHUB_ACTIONS).
    output = ANSI_ESCAPE.sub("", result.output).lower()

    assert result.exit_code != 0
    assert "invalid value for '--path'" in output
    assert "does not" in output and "exist" in output
    assert "Traceback (most recent call last)" not in result.output


def test_version_reports_installed_package_version():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert f"v{package_version('blocktracex-cli')}" in result.output
