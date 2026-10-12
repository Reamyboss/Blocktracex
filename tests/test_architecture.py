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


REPO_ROOT = Path(__file__).resolve().parents[1]


def _project(tmp_path, files: dict[str, str]) -> Path:
    project = tmp_path / "project"

    for name, content in files.items():
        path = project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    return project


def test_typer_project_reports_typer(tmp_path):
    project = _project(
        tmp_path,
        {"pyproject.toml": "[project]\nname = 'x'\ndependencies = ['typer>=0.12']\n"},
    )

    assert detect_architecture(project)["framework"] == "Typer"


def test_web_framework_wins_over_cli_framework(tmp_path):
    project = _project(
        tmp_path,
        {
            "pyproject.toml": (
                "[project]\nname = 'x'\n"
                "dependencies = ['typer', 'FastAPI[standard]==0.115']\n"
            )
        },
    )

    assert detect_architecture(project)["framework"] == "FastAPI"


def test_project_without_framework_reports_none_detected(tmp_path):
    project = _project(
        tmp_path,
        {
            "pyproject.toml": (
                "[project]\nname = 'x'\ndependencies = ['requests']\n"
                "[project.optional-dependencies]\nserver = ['django']\n"
            )
        },
    )

    assert detect_architecture(project)["framework"] == "None detected"


def test_requirements_txt_only_project(tmp_path):
    project = _project(
        tmp_path,
        {
            "requirements.txt": (
                "# web stack\n-r base.txt\n--index-url https://example.com\n"
                "Django==5.1  # pinned\n"
            )
        },
    )

    architecture = detect_architecture(project)

    assert architecture["language"] == "Python"
    assert architecture["framework"] == "Django"


def test_setup_cfg_project(tmp_path):
    project = _project(
        tmp_path,
        {"setup.cfg": "[options]\ninstall_requires =\n    flask>=3\n    requests\n"},
    )

    architecture = detect_architecture(project)

    assert architecture["language"] == "Python"
    assert architecture["framework"] == "Flask"


def test_poetry_project(tmp_path):
    project = _project(
        tmp_path,
        {
            "pyproject.toml": (
                "[tool.poetry.dependencies]\n" 'python = "^3.11"\nStreamlit = "^1.30"\n'
            )
        },
    )

    assert detect_architecture(project)["framework"] == "Streamlit"


def test_python_files_without_packaging_are_python(tmp_path):
    project = _project(tmp_path, {"script.py": "print('hi')\n"})

    assert detect_architecture(project)["language"] == "Python"


def test_malformed_pyproject_does_not_raise(tmp_path):
    project = _project(tmp_path, {"pyproject.toml": "[project\nname = \n"})

    architecture = detect_architecture(project)

    assert architecture["language"] == "Python"
    assert architecture["framework"] == "None detected"


def test_blocktracex_itself_reports_typer():
    assert detect_architecture(REPO_ROOT)["framework"] == "Typer"
