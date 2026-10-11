# Blocktracex — Project Handoff

_Snapshot: 2026-10-11. Last code commit: 2026-08-23._

## What it is

`btx` is a Python CLI (Typer + Rich) that sets up and inspects software projects.
The goal, from `docs/ROADMAP.md` on the feature branch, is to become "the
knowledge layer between software projects and intelligent systems": it validates,
inspects and scores a repo, then gives engineering advice.

## Where the code is (read this first)

As of 2026-10-11, the Sprint 11–22 work from `feature/btx-init` is being
merged into `main`:

- [Reamyboss/Blocktracex#1](https://github.com/Reamyboss/Blocktracex/pull/1)
  merges `feature/btx-init` and fixes CI. CI is green on it.
- A follow-up PR from `claude/repo-cleanup` does the repo cleanup. It's stacked
  on #1, so merge #1 first.

After both merge, `feature/btx-init` can be deleted. The `v0.3.0` tag points at
an early `main` commit (`84b9def`) and doesn't reflect the current code.

The commands are `new`, `init`, `doctor`, `validate`, `info`, `inspect`,
`architecture`, `knowledge`, `coach`, `dashboard` and `history`, plus `version`
and `hello`.

The code is split into engines (`inspect.py`, `knowledge.py`, `coach.py`, ...),
reports (`*_report.py`) and the CLI orchestration in `main.py`. The docs are
`README.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`,
`docs/ALPHA_0.1.md` and `docs/ENGINEERING_PRINCIPLES.md`.

## CI

`.github/workflows/ci.yml` runs on pushes to `main`, `develop` and
`feature/**`, and on PRs into `main` and `develop`. It installs
`pip install -e ".[dev]"`, then runs ruff, then black, then pytest. Rich turns
on color when it detects GitHub Actions, so tests that assert on CLI output
should strip ANSI codes first (see `tests/test_cli.py`).

## Fixed in the get-to-green PRs

- Ruff errors (import order, `SIM114`, blind `except Exception` in `scaffold.py`).
- `scaffold.py` wrote every template file 7 times (inside the folder loop).
- The inspect table title wrapped onto two lines.
- A UTF-16 `requirements.txt` that didn't match `pyproject.toml`. Dependencies
  now live only in `pyproject.toml`, with dev tools under the `dev` extra.
- Committed `egg-info/` and `.pyc` files. Both are now ignored.
- The version was hard-coded in `main.py`. It's now read from package metadata.
- Empty placeholder files and the workflow filename `blocktracex-cl..yml`.

## Remaining debt

- `src/btx/docs/` (sprint notes, decision log) lives inside the Python package.
  Move it to `docs/`.
- `templates.py` still has a hard-coded `version = "0.1.0"` for generated projects.
- Typer and Rich are unpinned. Add lower bounds once a release is tagged.

## Restart plan

**Week 1: get to green and merge.**
1. ~~Fix CI and merge `feature/btx-init` into `main`~~: PR #1.
2. ~~Clean up the repo~~: the `claude/repo-cleanup` PR.
3. Bump `version` in `pyproject.toml` and tag a real `v0.4.0` (or
   `alpha-0.1`) from the merged `main`.

**Week 2: make it usable by someone else.**
4. Extend the README's Development section into a user quick start with sample output.
5. Run `btx` against 3–5 real repos and turn the false positives into issues.
6. Turn the open roadmap items into GitHub issues with labels. Right now the
   repo has no issues at all.

**Then: Phase 2 of the roadmap (Project Intelligence).**
7. Start with import and dependency graph analysis (`ast`-based), which feeds
   architecture and risk scoring.
8. Add a `--json` output flag to every report command. That's the prerequisite
   for the "AI context layer" phase.

## Working conventions

- Work goes in sprint-numbered commits. `CHANGELOG.md` is updated per sprint.
- Keep the engine / report / CLI split. Engines return data, reports render it,
  and `main.py` only wires them together.
- Run `ruff check . && black --check . && pytest` before pushing. CI runs the same checks.
