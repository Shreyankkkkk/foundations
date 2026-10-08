# AI-CONTEXT (read this first, every chat)

Purpose: one-page entry point for any AI working on this repo. Read this, then only the STATE.md of the project in question. Do not ask for whole codebases and do not open `_local/`. New project or resuming one: follow `projects/WORKFLOW.md`.

## Who
Shreyank, 2nd-year Mechatronics Engineering student (UOWD). Goal: quantitative finance (discretionary trading + systematic/quant development). This repo is a public log of everything he learns, builds and earns.

## Folder map (all names lowercase kebab-case)
| Folder | Holds |
|---|---|
| `journal/` | master dated ledger, one file per month: `YYYY-MM.md` |
| `roadmap/` | learning plans by year (`roadmap/2026/`) |
| `certificates/` | every certificate earned, by domain, indexed in `certificates/README.md` |
| `learning/` | notes and exercises: `programming/` (python, git-github, data-analysis, apis-automation, embedded-arduino), `mathematics/`, `ai/`, `engineering/`, `finance/` |
| `projects/` | built things; each has `STATE.md` + `LOG.md` (`sumo-robot` finished, `monte-carlo-simulation` active, `quant-finance-sim-forage` to redo) |
| `coursework/` | school/university work, local-only (gitignored) |
| `playground/` | scratch space, not part of the log |
| `_local/` | local-only: books, vendor files, old context transfers. Gitignored. Never read, never publish |

Inside a learning topic: `notes/`, `exercises/`, `datasets/`, `projects/` (only the ones that have content).
Inside a project: `STATE.md`, `LOG.md`, then folders by kind (`docs/`, `design/`, `firmware/`, `notes/`, `archive/`). Sumo detail: `projects/sumo-robot/README.md`.

## Rules for AI
1. Read `AI-CONTEXT.md`, then `projects/<X>/STATE.md`. Open code files only when the task needs them.
2. Constants: never invent or hard-code. Every constant gets its calculation or measurement shown beside it, plus the source. Unmeasured = say so, mark it `PLACEHOLDER`; assumed = `ASSUMED`.
3. Code changes: give the code and say which file and where in it the change goes (he does not know the file layout by heart).
4. Be token-efficient: no padding.
5. Never run git commit/push. Shreyank commits. Before big edits, remind him to commit first.
6. Use today's date for every log line; never guess a date. If a date is unknown, write `date?`.
7. Naming: lowercase kebab-case, no spaces, `exercises` (not excercises). Do not create empty folders. Every folder with real content gets a README.
8. Public repo: no passwords, tokens, ID numbers, personal finances or private chat content.

## How to log (three layers, end of every session)
1. `journal/YYYY-MM.md`: append one line per session: `YYYY-MM-DD | learn/build/plan/research/achieve | what | files`.
2. Project work only: also append the detailed line to that project's `LOG.md`: `YYYY-MM-DD | what changed | why | evidence (file path or commit)`.
3. If the project's truth changed (a constant, a decision, a status): update its `STATE.md`. If a certificate was earned: add a row to `certificates/README.md`.
Newest at the bottom. One line per entry, however small. List changed files in the reply.
