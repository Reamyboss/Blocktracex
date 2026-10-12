import json
from importlib.metadata import version as package_version
from pathlib import Path

import pytest
from typer.testing import CliRunner

import btx.history
from btx.json_output import SCHEMA_VERSION, emit_json
from btx.main import app

runner = CliRunner()

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolated_history(tmp_path, monkeypatch):
    """`dashboard` saves a snapshot; keep it out of the real home directory."""

    history_file = tmp_path / "history.json"
    monkeypatch.setattr(btx.history, "HISTORY_FILE", history_file)

    return history_file


def _run_json(*args):
    result = runner.invoke(app, [*args, "--json"])

    assert result.exit_code == 0, result.output

    payload = json.loads(result.stdout)

    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["btx_version"] == package_version("blocktracex-cli")
    assert payload["command"] == args[0]

    return payload["data"]


@pytest.mark.parametrize(
    ("command", "expected_keys"),
    [
        ("inspect", {"project_name", "source_files", "test_files", "git"}),
        ("architecture", {"language", "framework", "testing", "package_layout"}),
        ("validate", {"valid", "passed", "failed", "score", "checks", "missing"}),
        (
            "knowledge",
            {
                "engineering_health_score",
                "engineering_health_value",
                "engineering_verdict",
                "next_best_action",
            },
        ),
        ("coach", {"next_action", "why", "estimated_effort", "first_step"}),
        ("dashboard", {"project", "knowledge", "coaching", "roadmap"}),
    ],
)
def test_report_commands_emit_json(command, expected_keys):
    data = _run_json(command, "--path", str(REPO_ROOT))

    assert expected_keys <= data.keys()


def test_json_output_has_no_rich_markup():
    result = runner.invoke(app, ["inspect", "--path", str(REPO_ROOT), "--json"])

    assert "\x1b[" not in result.stdout
    assert "┃" not in result.stdout


def test_validate_json_reports_each_check(tmp_path):
    (tmp_path / "btx.toml").write_text("[project]\nname = 'x'\n")
    (tmp_path / "docs").mkdir()

    data = _run_json("validate", "--path", str(tmp_path))

    assert data["valid"] is False
    assert data["passed"] == 2
    assert {"name": "btx.toml", "kind": "file", "passed": True} in data["checks"]
    assert "src" in data["missing"]


def test_history_json_lists_saved_snapshots(isolated_history):
    assert _run_json("history") == {"snapshots": []}

    _run_json("dashboard", "--path", str(REPO_ROOT))

    snapshots = _run_json("history")["snapshots"]

    assert len(snapshots) == 1
    assert {"timestamp", "health_score", "maturity", "risk"} <= snapshots[0].keys()


def test_dashboard_fail_under_passes_when_score_is_high_enough():
    result = runner.invoke(
        app, ["dashboard", "--path", str(REPO_ROOT), "--json", "--fail-under", "0"]
    )

    assert result.exit_code == 0
    json.loads(result.stdout)


def test_dashboard_fail_under_exits_1_when_score_is_too_low(tmp_path):
    result = runner.invoke(
        app, ["dashboard", "--path", str(tmp_path), "--fail-under", "100"]
    )

    assert result.exit_code == 1
    assert "below --fail-under 100" in result.stderr


def test_dashboard_fail_under_keeps_stdout_valid_json(tmp_path):
    result = runner.invoke(
        app, ["dashboard", "--path", str(tmp_path), "--json", "--fail-under", "100"]
    )

    assert result.exit_code == 1
    assert json.loads(result.stdout)["command"] == "dashboard"


def test_fail_under_rejects_out_of_range_values():
    result = runner.invoke(app, ["dashboard", "--fail-under", "101"])

    assert result.exit_code != 0


def test_paths_and_sets_are_serialized(capsys):
    emit_json("example", {"path": Path("/tmp/x"), "tags": {"b", "a"}})

    data = json.loads(capsys.readouterr().out)["data"]

    assert data == {"path": "/tmp/x", "tags": ["a", "b"]}
