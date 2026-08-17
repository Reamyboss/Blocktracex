import io
import sys

import pytest
from rich.console import Console
from typer.testing import CliRunner

from btx.main import _ensure_utf8_console_output, app

runner = CliRunner()


class _RecordingStream:
    """Stand-in for sys.stdout/sys.stderr that records reconfigure() calls."""

    def __init__(self):
        self.calls = []

    def reconfigure(self, **kwargs):
        self.calls.append(kwargs)


class _StreamWithoutReconfigure:
    """Simulates a stream/proxy that doesn't support reconfigure() at all."""


def test_reconfigures_stdout_and_stderr_on_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    fake_stdout = _RecordingStream()
    fake_stderr = _RecordingStream()
    monkeypatch.setattr(sys, "stdout", fake_stdout)
    monkeypatch.setattr(sys, "stderr", fake_stderr)

    _ensure_utf8_console_output()

    assert fake_stdout.calls == [{"encoding": "utf-8", "errors": "replace"}]
    assert fake_stderr.calls == [{"encoding": "utf-8", "errors": "replace"}]


def test_does_nothing_on_non_windows_platforms(monkeypatch):
    """Existing macOS/Linux behavior must be untouched by this fix."""

    monkeypatch.setattr(sys, "platform", "linux")
    fake_stdout = _RecordingStream()
    fake_stderr = _RecordingStream()
    monkeypatch.setattr(sys, "stdout", fake_stdout)
    monkeypatch.setattr(sys, "stderr", fake_stderr)

    _ensure_utf8_console_output()

    assert fake_stdout.calls == []
    assert fake_stderr.calls == []


def test_tolerates_a_stream_without_reconfigure(monkeypatch):
    """Must not crash the whole CLI if some exotic stream lacks reconfigure()."""

    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(sys, "stdout", _StreamWithoutReconfigure())
    monkeypatch.setattr(sys, "stderr", _StreamWithoutReconfigure())

    _ensure_utf8_console_output()  # must not raise


def test_cp1252_stream_cannot_render_report_emoji():
    """
    Reproduces the exact crash observed on Windows, in isolation, without
    touching the machine's global encoding: a stream configured with the
    legacy ANSI codepage (cp1252) cannot encode the emoji rich prints in
    every report title, exactly like sys.stdout did before this fix.
    """

    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    console = Console(file=stream, force_terminal=False, legacy_windows=False)

    with pytest.raises(UnicodeEncodeError):
        console.print("🧠 BLOCKTRACEX PROJECT KNOWLEDGE")


def test_reconfiguring_the_stream_to_utf8_fixes_the_same_crash():
    """
    Proves the fix mechanism directly: reconfiguring the exact stream that
    just failed to UTF-8 -- the same operation _ensure_utf8_console_output
    performs on sys.stdout/sys.stderr -- is sufficient for the identical
    emoji output to render without raising.
    """

    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    console = Console(file=stream, force_terminal=False, legacy_windows=False)

    stream.reconfigure(encoding="utf-8", errors="replace")

    console.print("🧠 BLOCKTRACEX PROJECT KNOWLEDGE")  # must not raise


def test_knowledge_command_still_renders_normal_content():
    """
    Normal CLI usage (item A) must still work, and the fix must not alter
    ordinary report semantics (item D) -- the same structured content
    should appear as before, just without crashing.
    """

    result = runner.invoke(app, ["knowledge"])

    assert result.exit_code == 0
    assert "BLOCKTRACEX PROJECT KNOWLEDGE" in result.output
    assert "Engineering Health Score" in result.output
