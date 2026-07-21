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
