# Blocktracex — Project Handoff

_Snapshot: 2026-10-11. Last code commit: 2026-08-23._

## What it is

`btx` is a Python CLI (Typer + Rich) that sets up and inspects software projects.
The goal, from `docs/ROADMAP.md` on the feature branch, is to become "the
knowledge layer between software projects and intelligent systems": it validates,
inspects and scores a repo, then gives engineering advice.

## Where the code is (read this first)

| Branch | State | Notes |
|---|---|---|
| `main` | CI green, 4 commands (`version`, `hello`, `new`, `doctor`) | About 150 lines. Only the scaffold MVP. |
| `feature/btx-init` | **22 commits ahead of `main`, CI red, no PR open** | About 1,700 lines and 14 commands. Holds nearly all real work from "Sprints" 11–22. |
| tag `v0.3.0` | Points at `84b9def` (a `main` commit) | Doesn't match the feature-branch work. |

On `feature/btx-init`, the commands are `new`, `init`, `doctor`, `validate`,
`info`, `inspect`, `architecture`, `knowledge`, `coach`, `dashboard` and
`history`, plus `version` and `hello`.

The code is split into engines (`inspect.py`, `knowledge.py`, `coach.py`, ...),
reports (`*_report.py`) and the CLI orchestration in `main.py`. The docs are
`README.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`,
`docs/ALPHA_0.1.md` and `docs/ENGINEERING_PRINCIPLES.md`.

## Why the feature branch is red

The CI workflow `.github/workflows/blocktracex-cl..yml` runs ruff, then black, then pytest.

1. **Ruff: 10 errors.** There are 7 unsorted imports and 2 `SIM114` errors in
   `knowledge.py`, all auto-fixable. There's also one `BLE001` at
   `src/btx/scaffold.py:87` (`except Exception`). `main` already fixed that one
   in `aa50485`, but the fix never reached the feature branch.
2. **Pytest: 1 failure out of 44.** `tests/test_cli.py::test_inspect_default_behavior_still_works`
   expects the string `BLOCKTRACEX PROJECT INSPECTION` on one line. Rich wraps
   the table title to the table's width, so it prints across two lines. The fix
   is to give the table a `min_width` or make the assertion ignore whitespace.
3. Black passes.

## Known bugs and debt (both branches unless noted)

- `scaffold.py`: the template files (README, .gitignore, CHANGELOG, ...) are
  written **inside** the folder loop, so each one gets rewritten 7 times. The
  output is correct but the code is wrong. Dedent that block.
- `requirements.txt` is a UTF-16 `pip freeze` dump (pandas, numpy, fastapi...)
  that doesn't match `pyproject.toml`. Make `pyproject.toml` the single source
  and move dev tools to `[project.optional-dependencies] dev`.
- `src/blocktracex_cli.egg-info/` is committed. `main` also commits
  `__pycache__/*.pyc`. Remove both and add them to `.gitignore`.
- The version is hard-coded as `v0.1.0` in `main.py`. Read it from package metadata instead.
- Empty placeholder files: `tests/test_reports.py`, `tests/test_scoring.py`, `src/btx/explain_report.py`.
- `main` README title says `project_egde` (typo / old name).
- The workflow filename `blocktracex-cl..yml` has a stray double dot.

## Restart plan

**Week 1: get to green and merge.**
1. On `feature/btx-init`, merge `main` in to bring over the BLE001 fix. Then run
   `ruff check --fix .`, fix the inspect test, and dedent the scaffold loop.
2. Open a PR from `feature/btx-init` into `main` and get CI green.
3. Clean up the repo: drop the egg-info and the `.pyc` files, replace
   `requirements.txt` with pyproject extras, and rename the workflow file.
4. Tag a real `v0.4.0` (or `alpha-0.1`) from the merged `main`.

**Week 2: make it usable by someone else.**
5. Add a quick start to the README showing install, `btx inspect --path .` and sample output.
6. Run `btx` against 3–5 real repos and turn the false positives into issues.
7. Turn the open roadmap items into GitHub issues with labels. Right now the
   repo has no issues or PRs at all.

**Then: Phase 2 of the roadmap (Project Intelligence).**
8. Start with import and dependency graph analysis (`ast`-based), which feeds
   architecture and risk scoring.
9. Add a `--json` output flag to every report command. That's the prerequisite
   for the "AI context layer" phase.

## Working conventions

- Work goes in sprint-numbered commits. `CHANGELOG.md` is updated per sprint.
- Keep the engine / report / CLI split. Engines return data, reports render it,
  and `main.py` only wires them together.
- Run `ruff check . && black --check . && pytest` before pushing. CI runs the same checks.
