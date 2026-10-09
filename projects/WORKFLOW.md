# Project workflow (hackathons, competitions, courses, personal builds)

Rule of thumb: **the repo is the shared context.** Never paste code between chats; the AI reads `AI-CONTEXT.md` and the project's `STATE.md`, edits files in place, and you review with `git diff` and commit.

## 0. One-time setup per computer
- The local MCP lives in `%APPDATA%\Claude\claude_desktop_config.json` (a JSON file, not JavaScript). It belongs to the computer, not to a Claude account, so any account logged into the desktop app on this PC should get the same `foundations` server. After switching accounts, fully restart the app and check in a new chat that the foundations tools are listed. If not, re-check that JSON file.
- Memory and preferences are per account and are NOT shared between accounts. Everything that must apply to every chat lives in `AI-CONTEXT.md`.
- Phone, web or a PC without the MCP: the AI can read only what is pushed, so push at the end of every session. Use section 3a.
- Code map: `scripts/codemap/codemap.py --watch` keeps `scripts/codemap/CODEMAP.md` current. On a new PC, set it to start at login (Startup-folder shortcut to `pythonw codemap.py --watch`). It lists only git-publishable files, and it is committed so other AIs can read it.
- The GitHub repo is named `foundations` (`https://github.com/Shreyankkkkk/foundations`). Its old name `quant-foundations` is retired; do not use it in links.

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
2. AI reads `AI-CONTEXT.md` + `projects/<slug>/STATE.md` (+ last 10 lines of `LOG.md`, tail only); opens code only when needed.
3. Work happens in the files; the AI says which file and where for every change; every constant comes with its calculation or measurement.
4. Say `log it`. The AI appends a line to `journal/YYYY-MM.md` and the project `LOG.md`, updates `STATE.md` if the truth changed, and lists changed files.
5. You: `git status`, `git diff`, then commit and push (see below).

## 3a. Any other AI (ChatGPT, Gemini, web/phone Claude): no MCP
One self-contained file per project, built by a script (no AI tokens): `projects/<slug>/PORTABLE.md` = rules + STATE + last 10 LOG lines + raw links to docs/notes.
1. Commit and push (a git hook rebuilds PORTABLE.md on every commit; if it did not run, run `python scripts/build_portable.py` first).
2. New chat, send the **External start** prompt below with that project's raw link.
3. For code questions also send the raw link to `scripts/codemap/CODEMAP.md` (function/class index; it is only as new as your last push). If the AI says it cannot open a link, do not argue: open the file in your browser, copy it, paste it into the chat. It is only about 1.5-3k tokens.
4. Work. The AI cannot edit your files, so at the end send the **External end** prompt and paste the result into STATE.md and LOG.md yourself.

## 3b. Learning notes (new topics, zero knowledge)
The AI writes the note content only; you paste it into the file. That costs zero file-edit tokens.
1. Glossary first: paste the brief's terms, use the **Glossary** prompt. Learn Tier 1 only; leave Tier 2-3 until needed.
2. One topic per chat (history is re-sent every message, so long chats burn tokens).
3. Use the **Teach me** prompt. Read the note, then paste it into `projects/<slug>/notes/<topic>.md` (project-specific) or `learning/<area>/notes/<topic>.md` (reusable). One file per topic, topic name in the filename.
4. Revise later in a fresh chat: paste ONE note and use the **Quiz me** prompt. Never load the repo for revision.
5. Add to STATE.md only what changed the project (a decision, a constant, a rule); the note itself stays in notes/.

## 3c. Token rules
- The AI reads at most: `AI-CONTEXT.md` + one `STATE.md` + the last 10 LOG lines. Never a whole LOG, never `learning/`, never `_local/`.
- `STATE.md` is rewritten only where the truth changed. `LOG.md` and the journal get one appended line each, only on `log it`.
- One topic or task per chat. Start a new chat when the topic changes or the chat gets long.
- To find code, read `scripts/codemap/CODEMAP.md` first, then open only the one file it points to.
- Do not paste code or files the AI can open itself (MCP) or that are in PORTABLE.md.
- Keep prompts short: goal + constraint + output format.

## 4. Git routine (you commit; the AI never does)
```
git status
git diff
git add <paths>
git commit -m "type: what changed"
git push
```
- Commit before each AI session as a checkpoint, and once per logical change after reviewing.
- Each commit rebuilds `projects/*/PORTABLE.md` automatically (pre-commit hook in `.git/hooks`, local to this PC). On a new PC, copy the hook or run `python scripts/build_portable.py` before committing.
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
Continue <project>. Read AI-CONTEXT.md and projects/<slug>/STATE.md (and the last 10 lines of LOG.md, tail only).
Today's goal: <one line>. Edit files directly; tell me file + location for each change.
```
**End of session (desktop with MCP):** `log it`

**External start (any other AI)**
```
Read this file first and follow its rules: https://raw.githubusercontent.com/Shreyankkkkk/foundations/main/projects/<slug>/PORTABLE.md
If you cannot open it, say so and I will paste it. Do not guess its contents.
Today's goal: <one line>.
```
**External end (any other AI)**
```
End of session. In ONE code block give me: (1) a 5-line STATE.md update (decisions, constants, what is next, what is still unknown), (2) one LOG.md line: YYYY-MM-DD | what changed | why | evidence. Use today's date: <date>.
```
**Glossary (paste the brief's terms)**
```
Terms from the brief: <paste>. Sort into Tier 1 (must know first), Tier 2 (later), Tier 3 (ignore for now). One line each, no explanations yet.
```
**Teach me**
```
Teach me <term> from zero, for <project>. Plain language first, then the technical definition. One code block, template: Definition / Why it matters (for <project>) / How it works / Example / 3 self-test questions. Max 200 words. No file edits.
```
**Quiz me (fresh chat, paste ONE note)**
```
Quiz me on this note: 5 questions, one at a time, wait for my answer, then correct me and say what to re-read.
<paste note>
```
**Research (primary, then secondary)**
```
<project> primary research: from STATE.md and docs/brief.md, list every rule, constant and unknown I must confirm, each with where to find it. No answers from memory; mark anything unverified RECALLED.
```
```
<project> secondary research on <topic>: find sources (docs, repos, papers). Tag each finding SOURCED (with link) or RECALLED. Max 10 lines.
```
