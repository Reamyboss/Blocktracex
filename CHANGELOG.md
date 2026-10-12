# Changelog

## Sprint 11 — Project Intelligence Foundation

### Added

- Project Inspection Engine (`inspect.py`)
- Inspection Report Engine (`inspect_report.py`)
- `btx inspect` CLI command
- Rich table output for project inspection
- Structured project metadata collection

### Features

- Detects project name
- Detects Python version
- Detects Git repository
- Detects `btx.toml`
- Counts source files
- Counts test files

### Architecture

Introduced the Project Intelligence Foundation by separating:

- Inspection Engine (data collection)
- Report Engine (presentation)
- CLI (orchestration)

This establishes the architecture pattern that future AI engines will build upon.

🚀 **Sprint 11 Complete — Blocktracex Project Intelligence Foundation**

Today Blocktracex took an important step.

It no longer just validates projects.

It now begins to **understand** them.

### New capability

```bash
btx inspect
```

The command now reports:

- 📦 Project Name
- 🐍 Python Version
- 🔧 Git Repository
- 📄 BTX Configuration
- 📁 Source Files
- 🧪 Test Files

### Why this matters

Most developer tools inspect files.

We're building toward a platform that understands software architecture.

Today's output is simple.

Tomorrow it will include:

- Framework detection
- Architecture detection
- Dependency analysis
- AI readiness
- Blockchain-backed project identity

The vision hasn't changed.

We're still building an AI-native engineering platform—one engine at a time.

Every sprint is another brick in the foundation.

#buildinpublic #opensource #python #ai #softwareengineering #cli #blocktracex

Milestone 002

Project Intelligence Foundation

Status:
COMPLETE

Repository State:
SAFE

GitHub:
PUSHED

Architecture:
STABLE

## Sprint 12 — Architecture Intelligence

### Added

- Architecture Detection Engine (architecture.py)

- Architecture Report Engine (architecture_report.py)

- btx architecture CLI command

- Rich table output for architecture analysis

### Features

- Detects project language

- Detects framework

- Detects testing setup

- Detects documentation presence

- Detects package layout structure

### Architecture

Introduced the second Project Intelligence capability:

- Architecture Detection Engine

- Architecture Report Engine

- CLI orchestration layer

This extends the Project Intelligence Foundation established in Sprint 11.

Checkpoint Record
Protected

Checkpoint

Sprint 12

Milestone

Architecture Intelligence

Status

Protected

GitHub

Synced

Architecture

Stable

Future

A future worth building

Current Platform State
Stable

Validation Engine

Scoring Engine

Recommendation Engine

Dashboard Engine

Inspection Engine

Architecture Engine

btx validate

Working

btx inspect

Working

btx architecture

Working

Final line for the changelog
Official

Sprint Status: ✅ Complete

Future Status: A future worth building.

## Sprint 18 — Engineering Verdict Engine

### Added

- Engineering Evidence Engine
- Engineering Verdict
- Improved knowledge reporting
- Knowledge Engine upgraded to v1.3

### Outcome

Blocktracex now explains not only what it found during project inspection, but also the evidence supporting its conclusions and an overall engineering verdict.

## Sprint 20.2

### Added

- Introduced automated testing for the Knowledge Engine.
- Added validation for engineering intelligence outputs.
- Protected Engineering Verdict, Evidence, Priorities,
  Next Best Action, Estimated Impact, and Health Score
  against future regressions.
- Blocktracex now includes an automated verification
  framework for core engineering intelligence.

## v0.4.0 — Alpha consolidation

First release from `main` that includes the Sprint 11–22 work.

### Added

- Commands: `init`, `validate`, `info`, `inspect`, `architecture`,
  `knowledge`, `coach`, `dashboard`, `history` (merged from `feature/btx-init`).

### Fixed

- CI green again: ruff errors, the wrapped inspect table title, and a test
  that broke under GitHub Actions' colored output.
- `btx new` wrote each template file once per folder; it now writes each once.
- A missing `git` binary no longer crashes `btx new`.

### Changed

- Dependencies live only in `pyproject.toml`; dev tools install with
  `pip install -e ".[dev]"`. `requirements.txt` was removed.
- `btx version` reads the installed package version.
- CI workflow renamed to `ci.yml`, on Node 24 action versions.

## Unreleased

### Added

- `--json` on `inspect`, `validate`, `architecture`, `knowledge`, `coach`,
  `dashboard` and `history`: prints only a JSON payload
  (`schema_version`, `btx_version`, `command`, `data`) for scripts, CI and
  AI agents. (#20)
- `btx dashboard --fail-under N` exits with status 1 when the health score is
  below N, so CI can gate on it. (#20)
- `engineering_health_value` (integer 0-100) in the knowledge output,
  alongside the existing `"90/100"` string.
- README quick start: install, analyze, sample output, how the health score
  is calculated, limits and a command reference. (#6)

### Fixed

- `btx init` printed a message and created nothing. It now adds a
  `btx.toml` to an existing project and never overwrites one. (#6)
- `btx knowledge` showed a redundant "Engineering Health Value" row.
- `btx coach` suggested "Create unit tests for the Knowledge Engine" for
  every project; the advice is now generic.
- `btx architecture` detects the framework from declared dependencies
  (`pyproject.toml`, Poetry, `requirements*.txt`, `setup.cfg`) instead of
  always reporting Typer, and recognizes `setup.py`/`setup.cfg`/requirements
  or plain `.py` files as Python projects. (#4)
- `btx inspect` counts source files in any layout, not only `src/`, skips
  virtualenvs, build output and caches, and recognizes `test_*.py` /
  `*_test.py` files outside `tests/`. (#5)
