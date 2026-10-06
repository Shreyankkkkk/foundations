# AI-CONTEXT (read this first, every chat)

Purpose: one-page entry point for any AI working on this repo. Read this, then only the STATE.md of the project in question. Do not ask for whole codebases.

## Who
Shreyank, 2nd-year Mechatronics Engineering student (UOWD). Goal: quantitative finance (discretionary trading + systematic/quant development). This repo is a public log of everything he learns, builds and earns.

## Real folder map (local names are capitalised)
| Folder | Holds |
|---|---|
| `Certificates/` | every certificate earned |
| `Technical-skills/` | Python, Git, data analysis, etc. notes |
| `Mathematics/` | maths notes (statistics, calculus, ...) |
| `Finance/` | finance notes |
| `Projects/` | built things; each project has `STATE.md` + `LOG.md` |
| `Journal/` | monthly logs: `YYYY-MM.md` |
| `Roadmap/` | learning plans by year |
| `University/`, `School/` | coursework |
| `Playground/` | scratch space |
| `docs/` | glossary and misc docs |

Projects: `Projects/Sumo-Robot/` (finished), `Projects/monte-carlo-simulation/` (active), `Projects/quant-finance-sim-forage/` (to redo).
Note: the root `README.md` is outdated (lowercase paths, "first-year", `roadmaps/2025.md`). Trust this file over it.

## Rules for AI
1. Read `AI-CONTEXT.md`, then `Projects/<X>/STATE.md`. Open code files only when the task needs them.
2. Constants: never invent or hard-code. Every constant gets its calculation or measurement shown beside it, plus the source. Unmeasured = say so, mark it `PLACEHOLDER`.
3. Code changes: give the code and say which file and where in it the change goes (he does not know the file layout by heart).
4. Be token-efficient: no padding.
5. Mark anything assumed as `ASSUMED`.

## How to log
- End of every session: append lines to the project's `LOG.md` (or `Journal/YYYY-MM.md` for study), update `STATE.md` if the truth changed, list changed files.
- LOG line format: `YYYY-MM-DD | what changed | why | evidence (file path or commit)`.
- Newest at the bottom. One line per entry, however small.
- Public repo: no passwords, tokens or ID numbers.
