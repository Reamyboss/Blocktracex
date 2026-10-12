# Field Tests

Results of running Blocktracex on real open-source projects, to find where its
verdicts are wrong before the Alpha 0.1 release (#7).

## Method

- **Blocktracex version:** 0.4.0 plus unreleased changes on `main` as of 2026-10-12
  (includes #25, #26 and #28).
- **Commands run** on each project, all with `--path <project> --json`:
  `inspect`, `architecture`, `knowledge`, `coach` and `validate`.
- Each result was checked by hand against the project's actual files.
- Projects were shallow clones at the commits below, chosen to cover different
  shapes.

| Project | Commit | Shape |
|---|---|---|
| [Textualize/rich](https://github.com/Textualize/rich) | `9d8f9a3` | Large library, flat layout, Poetry |
| [psf/requests](https://github.com/psf/requests) | `611c616` | Library, `src/` layout |
| [theskumar/python-dotenv](https://github.com/theskumar/python-dotenv) | `0b28805` | Small library, `src/` layout, optional CLI extra |
| [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | `7257e60` | Web app in a monorepo (`backend/` + `frontend/`) |
| [jakevdp/PythonDataScienceHandbook](https://github.com/jakevdp/PythonDataScienceHandbook) | `d662314` | Notebook-based book, no tests |

## Results

| Project | Source / tests | Framework | Health | Next best action |
|---|---|---|---|---|
| rich | 146 / 67 | None detected ✅ | 94 Excellent ✅ | Create a Blocktracex configuration file ❌ |
| requests | 22 / 15 | None detected ✅ | 82 Healthy ⚠️ (90 once #30 is fixed) | Create a Blocktracex configuration file ❌ |
| python-dotenv | 8 / 12 | **Click** ❌ | 90 Excellent ✅ | Create a Blocktracex configuration file ❌ |
| full-stack-fastapi-template | 28 / 15 | **None detected** ❌ (FastAPI) | 70 Fair ⚠️ | Create a Blocktracex configuration file ❌ |
| PythonDataScienceHandbook | 10 / 0 | None detected ✅ | 50 Needs Attention ⚠️ | Increase automated testing ⚠️ |

`btx validate` failed on all five projects, with scores of 14–43 (see finding 7).

## What worked

- **File counting** (fixed in #25) was correct in every layout: flat (`rich`),
  `src/` (`requests`, `python-dotenv`), and nested `backend/tests/`. Virtual
  environments and build folders were never counted.
- **Ranking:** the three mature libraries scored highest and the notebook repo
  lowest. The overall order matches what an experienced reviewer would expect.
- **`--json`** (#26) worked on every project and command, which made this
  whole test scriptable.
- No crashes on any project.

## Findings

Each finding has an issue. They're ordered by how much they affect trust in
the results.

| # | Finding | Effect | Issue |
|---|---|---|---|
| 1 | "Create a Blocktracex configuration file" is the top advice for 4 of 5 projects, including the three best ones. `btx.toml` is required for "Advanced" maturity | The main advice is useless for real projects, and it looks self-serving | #29 |
| 2 | Changelogs named `HISTORY.md` (requests) or `release-notes.md` (template) aren't recognized | Documentation rated Basic instead of Excellent (−8 points for requests) | #30 |
| 3 | Dev-only `requirements.txt` is treated as runtime dependencies | python-dotenv reported as a "Click" app | #31 |
| 4 | Projects in a subfolder (monorepos) are only read at the root | FastAPI template: framework missed, and `architecture` says testing "None" while `knowledge` counts 15 test files | #32 |
| 5 | "Python version detected" is the Python running `btx`, not the project's | Every project shows the same version in its evidence | #33 |
| 6 | Notebook projects (136 `.ipynb`, 10 `.py`) are judged as code libraries | Generic "add unit tests" advice for a book | #34 |
| 7 | `btx validate` only checks the Blocktracex template folder layout | Every real project fails (14–43%), which contradicts `btx knowledge` (e.g. rich: 29% vs 94/100) | #35 |

## Conclusion

The data collection is solid. The trust problems come from **what the
knowledge engine does with the data**: the btx.toml bias (finding 1) and the
narrow file-name checks (findings 2, 3 and 5). Fixing #29–#33 should make the
results credible on typical Python projects, and those are the remaining
blockers for Alpha 0.1. #34 and #35 can follow.

## Re-running these tests

```bash
git clone --depth 1 https://github.com/psf/requests /tmp/requests
btx knowledge --path /tmp/requests --json
```

Repeat for each project in the table. When findings are fixed, update the
Results table and add the issue number of the fix.
