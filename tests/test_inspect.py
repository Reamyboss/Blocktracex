from pathlib import Path

from btx.inspect import inspect_project


def test_returns_dictionary():
    project = inspect_project()

    assert isinstance(project, dict)


def test_project_name_exists():
    project = inspect_project()

    assert "project_name" in project


def test_python_version_exists():
    project = inspect_project()

    assert "python_version" in project


def test_git_status_exists():
    project = inspect_project()

    assert "git" in project


def test_source_files_exists():
    project = inspect_project()

    assert "source_files" in project


def test_test_files_exists():
    project = inspect_project()

    assert "test_files" in project


def test_readme_exists():
    project = inspect_project()

    assert "readme" in project


def test_changelog_exists():
    project = inspect_project()

    assert "changelog" in project


def test_docs_exists():
    project = inspect_project()

    assert "docs" in project


def test_btx_config_exists():
    project = inspect_project()

    assert "btx_config" in project


def test_default_root_matches_explicit_cwd():
    """No argument must behave exactly like passing the current directory."""

    assert inspect_project() == inspect_project(Path.cwd())


def test_explicit_path_analyzes_supplied_project_not_cwd(tmp_path):
    """
    Blocktracex has its own src/tests/README/git — an external fixture with
    deliberately different counts and no README proves the supplied path,
    not the current working directory, was actually inspected.
    """

    external = tmp_path / "external_project"
    (external / "src").mkdir(parents=True)
    (external / "tests").mkdir()

    (external / "src" / "one.py").write_text("x = 1\n")
    (external / "src" / "two.py").write_text("x = 2\n")
    (external / "tests" / "test_one.py").write_text("def test_x(): pass\n")
    (external / ".git").mkdir()

    project = inspect_project(external)

    assert project["project_name"] == "external_project"
    assert project["source_files"] == 2
    assert project["test_files"] == 1
    assert project["git"] is True
    assert project["readme"] is False
    assert project["btx_config"] is False


def test_nonexistent_path_does_not_raise(tmp_path):
    """
    The engine function itself stays simple/trusting (no path existence
    check) — invalid-path rejection is handled once, at the CLI boundary
    (see tests/test_cli.py). Calling it directly on a missing path must
    still degrade safely rather than raising.
    """

    missing = tmp_path / "does-not-exist"

    project = inspect_project(missing)

    assert project["source_files"] == 0
    assert project["test_files"] == 0
    assert project["git"] is False


def _write(path: Path, content: str = "x = 1\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_flat_layout_source_files_are_counted(tmp_path):
    project = tmp_path / "flat_project"
    _write(project / "mypackage" / "__init__.py")
    _write(project / "mypackage" / "core.py")
    _write(project / "mypackage" / "cli.py")
    _write(project / "tests" / "test_core.py")

    result = inspect_project(project)

    assert result["source_files"] == 3
    assert result["test_files"] == 1


def test_virtualenvs_build_output_and_caches_are_ignored(tmp_path):
    project = tmp_path / "project_with_venv"
    _write(project / "app.py")
    _write(project / ".venv" / "lib" / "site-packages" / "dep.py")
    _write(project / "venv" / "lib" / "other.py")
    _write(project / "build" / "lib" / "app.py")
    _write(project / "app.egg-info" / "stub.py")
    _write(project / "__pycache__" / "app.py")
    _write(project / ".git" / "hooks" / "hook.py")

    result = inspect_project(project)

    assert result["source_files"] == 1
    assert result["test_files"] == 0


def test_test_files_follow_pytest_naming_outside_tests_dir(tmp_path):
    project = tmp_path / "colocated_tests"
    _write(project / "pkg" / "core.py")
    _write(project / "pkg" / "test_core.py")
    _write(project / "pkg" / "cli_test.py")
    _write(project / "pkg" / "testing_utils.py")

    result = inspect_project(project)

    assert result["source_files"] == 2
    assert result["test_files"] == 2


def test_nested_tests_directory_counts_as_tests(tmp_path):
    project = tmp_path / "nested_tests"
    _write(project / "src" / "pkg" / "core.py")
    _write(project / "src" / "pkg" / "tests" / "conftest.py")
    _write(project / "src" / "pkg" / "tests" / "test_core.py")

    result = inspect_project(project)

    assert result["source_files"] == 1
    assert result["test_files"] == 2
