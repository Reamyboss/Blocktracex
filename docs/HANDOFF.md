# Blocktracex — Project Handoff

_Last updated: 2026-10-12, after PR #26. Version on `main`: **0.4.0**._

This document is the starting point for anyone picking up Blocktracex: the
owner coming back to it, or a new developer. It covers what the software is,
what it does today, where the project stands, and what to do next.

---

## 1. What Blocktracex is

`btx` is a command-line tool for Python projects. You point it at a project and
it reports how healthy the project is (structure, tests, documentation, risk),
then tells you the single most useful thing to improve next.

The long-term goal (`docs/ROADMAP.md`) is for Blocktracex to become "the
knowledge layer between software projects and intelligent systems": a tool
that turns a codebase into structured knowledge that people, CI pipelines and
AI agents can all use.

## 2. What it can do today

| Command | What it does |
|---|---|
| `btx new <name>` | Create a new project with the standard Blocktracex layout, `btx.toml` and git |
| `btx init` | Add a `btx.toml` to an existing project (never overwrites) |
| `btx doctor` | Check that Python, git, pip and an editor are installed |
| `btx inspect` | Count source and test files (any layout), detect git, README, docs and `btx.toml` |
| `btx architecture` | Detect the language, the framework (Django, FastAPI, Flask, Typer, …), testing and layout |
| `btx validate` | Check the project against the Blocktracex standard structure |
| `btx knowledge` | Health score (0–100), maturity, risk, verdict, evidence and priorities |
| `btx coach` | The next best action, why it matters, the estimated effort and the first step |
| `btx dashboard` | All of the above on one screen. Also saves a history snapshot |
| `btx history` | The timeline of saved snapshots |
| `btx info` | Show the current project's `btx.toml` |

Every analysis command takes `--path <dir>` (the default is the current
directory). Every report command also takes `--json`, which prints a
machine-readable envelope (`schema_version`, `btx_version`, `command`,
`data`) and nothing else.

`btx dashboard --fail-under N` exits with status 1 when the health score is
below N, for gating CI.

### Honest limits (read before showing it to anyone)

- **The scoring is heuristic.** It's based on whether files and folders exist
  (is there a `tests/` folder, a README, a `btx.toml`?) and on file counts.
  It doesn't read the code yet. Real code analysis is Phase 2 (#9).
- **Python only.**
- **Coaching text is generic and rule-based.** Field testing on real
  projects (#7) is meant to find advice that doesn't fit.
- **History is global.** Every project's snapshots go into
  `~/.btx_history.json` and are recorded as `"project": "Unknown"`. Tracked
  in #16.
- **`btx validate` expects the full Blocktracex template** (`docs`, `src`,
  `tests`, `scripts`, `notebooks`, `data`), so most ordinary projects fail it.

## 3. Where the project stands

```
Phase 1  Foundation              ████████░░  ← here: finishing Alpha 0.1
Phase 2  Project Intelligence    ░░░░░░░░░░  real code analysis (#9)
Phase 3  Engineering Memory      ░░░░░░░░░░  history, decisions (#15)
Phase 4  AI Context Layer        █░░░░░░░░░  --json done (#20); btx context next (#21)
Phase 5  Project Identity        ░░░░░░░░░░  (#22)
Phase 6  Enterprise Platform     ░░░░░░░░░░  (#23)
Phase 7  Ecosystem               ░░░░░░░░░░  (#24)
```

**Alpha 0.1** is the first public milestone (`docs/ALPHA_0.1.md`). It's reached
when a first-time user can install Blocktracex, analyze a project, and
understand and trust the results without reading the source code.

### How issue and PR numbers work

GitHub numbers issues and pull requests from one shared counter, so the
numbers aren't steps in a sequence.

- An **issue** is a to-do item: a bug or a feature.
- A **pull request (PR)** is finished code waiting to be merged into `main`.

| # | Type | What | Status |
|---|---|---|---|
| 1 | PR | Merged the Sprint 11–22 work from `feature/btx-init` and fixed CI | ✅ merged |
| 2 | PR | Repo cleanup: packaging, CI rename, version 0.4.0 | ✅ merged |
| 3 | Epic | Alpha 0.1: finish Phase 1 | 🟡 open |
| 4, 5 | Bugs | Framework always "Typer"; files outside `src/` not counted | ✅ fixed by #25 |
| 6, 7, 8 | Issues | README quick start, field testing, housekeeping | ⬜ to do (Alpha 0.1) |
| 9–14 | Epic and issues | Phase 2: Project Intelligence | ⬜ |
| 15–18 | Epic and issues | Phase 3: Engineering Memory | ⬜ |
| 19 | Epic | Phase 4: AI Context Layer | 🟡 open |
| 20 | Issue | `--json` output and `--fail-under` | ✅ done by #26 |
| 21 | Issue | `btx context`: AI-ready project summary | ⬜ |
| 22–24 | Epics | Phases 5–7 (checklists only) | ⬜ |
| 25 | PR | Fixed #4 and #5 | ✅ merged |
| 26 | PR | Built #20 | ✅ merged |

The live list is at <https://github.com/Reamyboss/Blocktracex/issues>.
Each epic lists its sub-issues.

### Release history

| Version | What changed |
|---|---|
| 0.1.0 | Scaffold MVP (`new`, `doctor`) |
| 0.4.0 | Sprint 11–22 engines on `main`, repo cleanup. See `CHANGELOG.md` |
| Unreleased | #4, #5 fixes and `--json` / `--fail-under` (#20) |

**Open:** the `v0.4.0` git tag hasn't been pushed yet. The old `v0.3.0` tag
points at an early commit (`84b9def`). To tag 0.4.0, at the commit where #2
merged:

```bash
git fetch origin
git tag -a v0.4.0 6917c7e -m "Blocktracex v0.4.0 — Alpha consolidation"
git push origin v0.4.0
```

## 4. Handing it over

### To someone who wants to use it

```bash
pip install git+https://github.com/Reamyboss/Blocktracex
btx dashboard --path /path/to/project
```

It requires Python 3.11+ and isn't on PyPI yet.

### To a developer who will work on it

```bash
git clone https://github.com/Reamyboss/Blocktracex
cd Blocktracex
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ruff check . && black --check . && pytest           # same checks as CI
```

Then read, in this order: this file, `docs/ARCHITECTURE.md`,
`docs/ENGINEERING_PRINCIPLES.md`, and the Alpha 0.1 epic (#3).

## 5. How the code is organized

The code follows one pattern throughout. **Engines** collect facts and return
plain dicts. **Reports** render those dicts with Rich. `main.py` only wires
the two together. Keep it that way: it's what made `--json` a small change.

| Engine (returns data) | Report (renders it) | Role |
|---|---|---|
| `inspect.py` | `inspect_report.py` | Facts about the project: files, git, docs |
| `architecture.py` | `architecture_report.py` | Language, framework, layout |
| `validate.py` (`check_project`) | `report.py`, `recommend.py` | Structure checks against the template |
| `knowledge.py` | `knowledge_report.py` | Scores, verdict, evidence, priorities |
| `coach.py` | `coach_report.py` | Next best action |
| `roadmap.py` | `roadmap_report.py` | Milestones from the knowledge output |
| `history.py` | `history_report.py` | Snapshot storage and timeline |
| — | `dashboard_report.py`, `dashboard.py` | Combined dashboard view |

Supporting modules:
- `project_files.py`: file discovery (skips venvs, build output and caches) and declared-dependency parsing
- `json_output.py`: the `--json` envelope
- `scaffold.py`, `templates.py`, `config.py`, `init.py`: project generation
- `scoring.py` and `explain.py`: score helpers
- `doctor.py` and `info.py`: environment and config display

Tests are in `tests/`, one file per engine plus `test_cli.py` and
`test_json_output.py`: 72 tests in total.

## 6. CI

`.github/workflows/ci.yml` runs on pushes to `main`, `develop` and
`feature/**`, and on PRs into `main` and `develop`. It runs
`pip install -e ".[dev]"`, then `ruff check .`, then `black --check .`, then
`pytest`.

**Gotcha:** Rich turns on color when it detects GitHub Actions. Tests that
assert on Rich output should strip ANSI codes first, as `tests/test_cli.py`
does. Run `GITHUB_ACTIONS=true pytest` locally to reproduce CI.

## 7. What to do next

In priority order:

1. **Push the `v0.4.0` tag** (command above).
2. **Finish Alpha 0.1 (#3).**
   - #7: run `btx` on 3–5 real open-source projects and fix wrong or
     Blocktracex-specific results (e.g. the coaching text above).
   - #8: housekeeping. Move `src/btx/docs/` to `docs/`, pin dependency floors,
     and delete the merged branches (everything except `main`).
3. **Release Alpha 0.1:** bump the version, tag it, and consider publishing to PyPI.
4. **Phase 2 (#9):** start with #10 (import graph) and #12 (metrics), then
   rebuild the score on them (#13).
5. **Then #21 (`btx context`)** and the per-project history rework (#16).

Recommendation: hold off on new features until Alpha 0.1 is out. A smaller
tool whose results people trust is worth more than a bigger one they don't.

## 8. Working conventions

- One PR per issue (or per tightly related pair). Write `Closes #N` in the PR
  description so the issue closes on merge.
- Add an entry under `## Unreleased` in `CHANGELOG.md` with every change.
- Keep the engine / report / CLI split. New data goes in engines, and new
  output goes in reports.
- New engine output must stay JSON-serializable. `--json` depends on it.
- Run `ruff check . && black --check . && pytest` before pushing.
