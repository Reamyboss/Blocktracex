# Blocktracex

> Understand engineering, not just code.

Blocktracex (`btx`) is a command-line tool that inspects a Python project and
tells you how healthy it is: documentation, tests, structure, maturity and
risk. Then it tells you the single most useful thing to improve next.

**Status:** working toward the first public release, Alpha 0.1. The current
version is 0.4.0. Python projects only. See [Limits](#limits) before relying
on the scores.

---

## Quick Start

### 1. Install

Requires Python 3.11 or newer.

```bash
pip install git+https://github.com/Reamyboss/Blocktracex
```

Or install it in its own isolated environment with `pipx install git+https://github.com/Reamyboss/Blocktracex`.

Check that it works:

```bash
btx version
```

### 2. Analyze a project

Go to any Python project and run:

```bash
cd path/to/your/project
btx dashboard
```

All analysis commands also accept `--path` to point at another folder, e.g.
`btx dashboard --path ~/code/my-app`.

### 3. See what to do next

```bash
btx coach
```

Here is the real output for a small project with a README, three source files,
one test file and git, but no changelog or `docs/` folder:

```text
╭──────────────────────────── 🎯 ENGINEERING COACH ────────────────────────────╮
│ ┌────────────────────────┬─────────────────────────────────────────────────┐ │
│ │ Next Action            │ ★ Increase automated testing to improve         │ │
│ │                        │ software reliability.                           │ │
│ │ Estimated Impact       │ High                                            │ │
│ │ Estimated Effort       │ Medium                                          │ │
│ │ Why                    │ More automated tests reduce regressions and     │ │
│ │                        │ improve confidence when making changes.         │ │
│ │ First Step             │ Add unit tests for your most important module   │ │
│ │                        │ first.                                          │ │
│ └────────────────────────┴─────────────────────────────────────────────────┘ │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 4. See the full assessment and the evidence behind it

```bash
btx knowledge
```

For the same project (trimmed):

```text
│ Documentation Maturity    │ Basic                                            │
│ Testing Maturity          │ Low                                              │
│ Project Structure         │ Needs Improvement                                │
│ Engineering Maturity      │ Emerging                                         │
│ Risk Level                │ Low                                              │
│ Engineering Health Score  │ 64/100                                           │
│ Engineering Health Status │ Fair                                             │
│ Engineering Evidence      │ • ✓ Git repository detected.                     │
│                           │ • ⚠ Blocktracex configuration missing.           │
│                           │ • ✓ README.md documentation found.               │
│                           │ • ⚠ CHANGELOG.md not found.                      │
│                           │ • ⚠ Documentation directory missing.             │
│                           │ • ✓ 3 Python source file(s) discovered.          │
│                           │ • ⚠ 1 automated test file(s) detected (Low       │
│                           │ coverage).                                       │
```

### 5. Improve and re-run

Fix one thing and run the command again. For example, `btx init` adds a
Blocktracex configuration file (`btx.toml`) to the project. For the project
above, that raises the score from **64** to **70**.

---

## Reading Your Results

The **Engineering Health Score** (0–100) is the average of five dimension
scores. Every dimension is based on things Blocktracex can see in the project
folder:

| Dimension | How it's judged | Score |
|---|---|---|
| **Documentation** | `README.md`, `CHANGELOG.md` and a `docs/` folder all present → Excellent; README only → Basic; no README → Missing | 100 / 60 / 20 |
| **Testing** | Number of test files: 20+ → High, 5–19 → Moderate, 1–4 → Low, none → None | 100 / 80 / 50 / 20 |
| **Structure** | Has source files **and** a `docs/` folder → Healthy, otherwise Needs Improvement | 100 / 40 |
| **Engineering Maturity** | How many of git, `btx.toml`, README and tests are present: all 4 → Advanced, 2–3 → Emerging, 0–1 → Early | 100 / 70 / 30 |
| **Risk** | No git → High, git but no tests → Medium, otherwise Low | 20 / 60 / 100 |

The score maps to a **status**:

| Score | Status |
|---|---|
| 90–100 | Excellent |
| 75–89 | Healthy |
| 60–74 | Fair |
| 40–59 | Needs Attention |
| below 40 | Critical |

**Evidence** lists exactly what was found (✓) or missing (⚠ / ✗), so every
point in the score can be traced back to the project.

A file counts as a **test** if it's inside a `tests/` or `test/` folder, or is
named `test_*.py` or `*_test.py`. Virtual environments, build output and cache
folders are ignored.

### Limits

- The scores come from which files and folders exist and how many there are.
  Blocktracex doesn't read your code yet. Real code analysis (imports,
  complexity, dependencies) is planned for the next phase.
- Only Python projects are supported.
- `btx validate` checks against the full Blocktracex template (`docs`, `src`,
  `tests`, `scripts`, `notebooks`, `data`), so most ordinary projects won't
  pass it. Use `btx knowledge` or `btx dashboard` for a general health check.
- History from `btx dashboard` is stored in one file in your home folder
  (`~/.btx_history.json`) for all projects.

---

## Commands

| Command | What it does |
|---|---|
| `btx dashboard` | Everything on one screen: summary, health, coaching and roadmap. Also saves a history snapshot |
| `btx knowledge` | Health score, maturity, risk, verdict, evidence and priorities |
| `btx coach` | The single next best action, why it matters, the effort and the first step |
| `btx inspect` | Basic facts: source and test file counts, git, README, docs, `btx.toml` |
| `btx architecture` | Language, framework (Django, FastAPI, Flask, Typer, …), testing and layout |
| `btx validate` | Check the project against the full Blocktracex template |
| `btx history` | Timeline of saved dashboard snapshots |
| `btx init` | Add a `btx.toml` to an existing project. Never overwrites an existing one |
| `btx new <name>` | Create a new project with the Blocktracex layout, `btx.toml` and git |
| `btx info` | Show the current project's `btx.toml` |
| `btx doctor` | Check that Python, git and pip are installed |
| `btx version` | Show the installed version |

Run `btx <command> --help` for every option.

## Machine-Readable Output

Every report command accepts `--json` and prints only JSON, ready to pipe into
other tools:

```bash
btx knowledge --path . --json | jq '.data.engineering_health_value'
```

Each payload has the same envelope:

```json
{
  "schema_version": 1,
  "btx_version": "0.4.0",
  "command": "knowledge",
  "data": { "...": "..." }
}
```

To fail a CI build when engineering health drops, use `--fail-under`:

```bash
btx dashboard --path . --fail-under 75
```

---

## Why Blocktracex Exists

Developers know how many files exist, how many tests pass and which framework
they use. What they often don't know is:

- How healthy is this project?
- How mature is our engineering?
- Where are the biggest risks?
- What should we improve next?

Blocktracex turns a project into evidence-based answers to those questions.
The long-term goal is to become the knowledge layer between software projects
and intelligent systems: structured project knowledge that people, CI
pipelines and AI agents can all use. See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## How It Works

```text
Project folder
│
▼
Inspection Engine       collects facts (files, git, docs, tests)
│
▼
Knowledge Engine        reasons about them (maturity, risk, health score)
│
▼
Coach & Roadmap         turns them into next actions
│
▼
Reports / JSON          shows them to you or to other tools
```

More detail is in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Development

Requires Python 3.11+.

```bash
git clone https://github.com/Reamyboss/Blocktracex
cd Blocktracex
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Before pushing, run the same checks as CI:

```bash
ruff check . && black --check . && pytest
```

New contributors should start with [`docs/HANDOFF.md`](docs/HANDOFF.md).
