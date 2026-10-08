# Project workflow (hackathons, competitions, courses, personal builds)

Rule of thumb: **the repo is the shared context.** Never paste code between chats; the AI reads `AI-CONTEXT.md` and the project's `STATE.md`, edits files in place, and you review with `git diff` and commit.

## 0. One-time setup per computer
- The local MCP lives in `%APPDATA%\Claude\claude_desktop_config.json` (a JSON file, not JavaScript). It belongs to the computer, not to a Claude account, so any account logged into the desktop app on this PC should get the same `foundations` server. After switching accounts, fully restart the app and check in a new chat that the foundations tools are listed. If not, re-check that JSON file.
- Memory and preferences are per account and are NOT shared between accounts. Everything that must apply to every chat lives in `AI-CONTEXT.md`.
- Phone, web or a PC without the MCP: the GitHub connection can read only what is pushed, so push at the end of every session.

## 1. Start a project (5 min)
Use the new-project prompt below. The AI creates `projects/<slug>/` with `STATE.md`, `LOG.md`, `README.md`, `docs/`, `notes/`, adds a row to `projects/README.md` and a line to `journal/`.
Day-0 checklist, filled into `STATE.md` with a source for each item: goal, deadline, rules and constraints, judging criteria, deliverables, team (solo or roles; no private details), allowed tools, constants to measure.
Hackathon/competition: split the time before you start (about 20% research, 60% build, 20% demo, README, submission); pick a freeze date for hardware or architecture; list the submission checklist.

## 2. Three stages (same template for every project)
1. **Primary research:** rulebook/brief checklist; list every constant the work needs and how to measure it; bench-test on the real target before writing strategy code; opponent/user-view check. Unmeasured values stay `PLACEHOLDER`.
2. **Secondary research:** repos, papers, docs, other AIs. Tag each finding `SOURCED` or `RECALLED`; verify `RECALLED` items on the target before they become constants. A second AI's review is a claim to check against a `git diff`, not a patch to apply blindly.
3. **Implementation:** one freeze date, then no new rewrites; compile and run on the real target early; wiring/integration tested end to end before polishing logic; fallback version kept (git tag).

## 3. Session loop (every session)
1. New chat with the resume prompt.
2. AI reads `AI-CONTEXT.md` + `projects/<slug>/STATE.md` (+ last 15 lines of `LOG.md`); opens code only when needed.
3. Work happens in the files; the AI says which file and where for every change; every constant comes with its calculation or measurement.
4. Say `log it`. The AI appends a line to `journal/YYYY-MM.md` and the project `LOG.md`, updates `STATE.md` if the truth changed, and lists changed files.
5. You: `git status`, `git diff`, then commit and push (see below).

## 4. Git routine (you commit; the AI never does)
```
git status
git diff
git add <paths>
git commit -m "type: what changed"
git push
```
- Commit before each AI session as a checkpoint, and once per logical change after reviewing.
- Versions come from git, not folders: tag working milestones (`git tag v0.1`, `git push --tags`). Use `archive/` only for abandoned approaches.
- Team projects: if teammates hold the code in their own repo, keep only notes, logs and a link here.
- Never commit secrets, keys, `.env`, private team information or other people's copyrighted files (put them in `_local/`).

## 5. Files every project has
`STATE.md` (under ~150 lines, current truth only):
```
# <Project> STATE
Status / deadline / goal
Rules and constraints (rule | value | source)
Constants (name | value | calculation or measurement | source | MEASURED/DERIVED/PLACEHOLDER/ASSUMED)
Decisions (choice | reason | rejected | FINAL/SUPERSEDED)
Open items / next actions
Where things are (folders)
```
`LOG.md`: one line per change, newest at the bottom: `YYYY-MM-DD | what changed | why | evidence (file or commit)`.
`journal/YYYY-MM.md`: `YYYY-MM-DD | learn/build/plan/research/achieve | what | files`.

## 6. Finish a project
Write `Retrospective.md` (what worked and what didn't per stage, decisions, open items); add certificates to `certificates/README.md`; push; then archive or delete the old chats.

## Prompts
**New project**
```
New project: <name>. Type: <hackathon/competition/course/personal>. Deadline: <date>. Goal: <one line>.
Rules/brief: <paste, or "I'll add to docs/brief.md">. Team: <solo / how many>.
Read AI-CONTEXT.md and projects/WORKFLOW.md. Create projects/<slug>/ per the workflow, add a row to projects/README.md and today's line to journal/.
Ask at most 3 questions to fill STATE.md, then list what we must measure or look up first. No code yet.
```
**Continue a project**
```
Continue <project>. Read AI-CONTEXT.md and projects/<slug>/STATE.md (and the last 15 lines of LOG.md).
Today's goal: <one line>. Edit files directly; tell me file + location for each change.
```
**End of session:** `log it`
