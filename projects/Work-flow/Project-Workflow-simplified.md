# Project Workflow

For hackathons, competitions, courses, and personal builds.

**Core rule:** the repository is the shared context. Claude Desktop with MCP can edit project files directly. Other AIs work from `PORTABLE.md` and return suggestions or text for you to apply. You review every change and make every commit.

## 1. Use each AI for a clear purpose

Keep the toolset small. Start with these defaults instead of choosing a different model for every task.

| Task | Use | How to use it |
|---|---|---|
| Find information, documentation, repositories, and current sources | **Perplexity** | Ask a focused question, open the useful sources, and save links or findings in the project docs. |
| Read and compare a collection of PDFs, rulebooks, papers, or other supplied documents | **NotebookLM** | Add the relevant documents and ask questions grounded in those sources. Check important claims in the cited passages. |
| Plan, write prompts, understand topics, solve problems, review work, and verify reasoning | **ChatGPT** | Give it the goal and relevant context. Ask it to explain assumptions, identify failure cases, and distinguish facts from guesses. |
| Build the project, edit repository files, and write or change code | **Claude Desktop with MCP** | Use the project workflow prompts. It can work directly in the repository; you review its changes. |

**Keep the roles flexible, not complicated:**
- Use Perplexity for research and source discovery. If the answer depends on official rules or exact requirements, check the official source yourself.
- Use NotebookLM when there are several documents to work through. For a single document, use whichever tool is simplest.
- Use ChatGPT to plan the next step, improve prompts, learn something, challenge a decision, review a diff, or work through a calculation.
- Use Claude Desktop for hands-on project work inside the repository.
- If a tool is unavailable or reaches its limit, use whichever of the other tools can reasonably do the job. Do not maintain a long list of model-specific fallbacks.

**Verification rule:** an AI answer is a claim, not proof. Open sources, run code, check calculations with Python, and test on the real target when applicable. For consequential code changes, have ChatGPT review the diff produced by Claude before you commit.

## 2. Set up once per computer

- The local MCP configuration is `%APPDATA%\\Claude\\claude_desktop_config.json`. It belongs to this computer, not to a Claude account. After switching accounts, fully restart Claude Desktop and check that the `foundations` tools appear in a new chat.
- Account memory and preferences are not shared. Put instructions that must apply across chats in `AI-CONTEXT.md`.
- Keep `scripts/codemap/CODEMAP.md` current with `scripts/codemap/codemap.py --watch`. On a new PC, configure the watcher to start at login if needed.
- The GitHub repository is `https://github.com/Shreyankkkkk/foundations`. The old `quant-foundations` name is retired.

## 3. Start a project

Use the **New project** prompt in the Prompts section.

The AI should create `projects/<slug>/` with:

- `STATE.md` — current facts, decisions, unknowns, and next actions.
- `LOG.md` — a short record of meaningful changes.
- `README.md` — project overview.
- `docs/` and `notes/` — source material, project research, and learning notes.

It should also add the project to `projects/README.md` and add a line to `journal/`.

Complete the day-one checklist in `STATE.md`, with a source for each item:

- Goal and deadline.
- Rules, constraints, judging criteria, and deliverables.
- Team and responsibilities (no private details).
- Allowed tools.
- Important values to measure or confirm.

For a hackathon or competition, plan the time roughly as **20% research, 60% building, and 20% demo and submission**. Choose a freeze date for major hardware or architecture decisions, and keep a submission checklist.

## 4. Work through the project

### Understand the task

- Start with the official brief, rulebook, requirements, and judging criteria.
- List important rules, constants, and unknowns.
- Record the source and how each value will be measured or verified.
- Use Perplexity to find relevant documentation, repositories, and other sources.
- Use NotebookLM when you need to compare or question a collection of documents.
- Label unverified values `PLACEHOLDER`. Label findings `SOURCED` when you have opened the source, or `RECALLED` when they still need verification.
- Test on the real target early when the project depends on hardware or a specific runtime.
- Check the solution from the opponent's, user's, or judge's point of view.

### Build and test

- Choose a freeze date for major hardware or architecture decisions. After it, avoid unnecessary rewrites.
- Compile and run on the real target early.
- Test the complete path end to end before polishing individual parts.
- Keep a known-working fallback; tag important milestones in Git.
- Ask ChatGPT to challenge assumptions or review consequential changes. Treat its findings as claims to check, not patches to apply blindly.

### Every work session

**Start with the right context**

Open a fresh chat when the task changes or the conversation gets long.

- **Claude Desktop with MCP:** use the **Continue a project** prompt. It reads `AI-CONTEXT.md`, the project's `STATE.md`, and only the last 10 lines of `LOG.md`. It opens source code only when needed, using `scripts/codemap/CODEMAP.md` to locate relevant files.
- **Any AI without MCP:** commit and push your latest work so the AI can access it. Give it the project's raw `PORTABLE.md` link using the **External start** prompt. For code questions, also provide the raw `CODEMAP.md` link. If it cannot open a link, paste the relevant file content instead of asking it to guess.

**Work on one task**

- State one clear goal and any important constraints.
- Claude Desktop can edit files directly. Ask it to identify the file and location for each change.
- Other AIs should return suggestions, proposed text, or instructions for you to apply; they do not edit your local repository.
- Every important constant should include its source and its calculation or measurement.

**Close the session**

- With Claude Desktop, say **`log it`**. It should append one line to the project `LOG.md` and `journal/YYYY-MM.md`, update `STATE.md` only if current facts changed, and list changed files.
- With another AI, use the **External end** prompt, then paste its STATE and LOG updates into the repository yourself.

**Review and commit**

You are responsible for Git. Before committing, run:

```bash
git status
git diff
git add <paths>
git commit -m "type: what changed"
git push
```

Review the diff before staging. Commit once per logical change and use commits as checkpoints before AI sessions.

## 5. Learning workflow

1. Collect unfamiliar terms from the brief and use the **Glossary** prompt. Learn Tier 1 terms first; defer Tier 2 and Tier 3.
2. Study one topic per fresh chat with **Teach me**. ChatGPT is the default.
3. Paste the resulting note into `projects/<slug>/notes/<topic>.md` or `learning/<area>/notes/<topic>.md`.
4. Later, test yourself in a fresh chat with **Quiz me**, pasting only that one note. Do not load the repository for revision.
5. Add something to `STATE.md` only if learning it changed a project decision, constant, rule, or next action. Keep the full learning note in `notes/`.

## 6. Keep context and token use small

- Load only `AI-CONTEXT.md`, one project `STATE.md`, and the last 10 lines of `LOG.md`.
- Never load the full log, `learning/`, or `_local/` by default.
- Update only the parts of `STATE.md` whose facts changed. Append to `LOG.md` and the journal only when closing a session with `log it` or the external-end process.
- Read `CODEMAP.md` first to find code; then open only the relevant source file.
- Do not paste code the AI can already access through MCP or that is already in `PORTABLE.md`.
- Keep prompts short: goal + constraints + requested output.

## 7. Git, versions, and sensitive files

- You make all commits; the AI does not.
- Each commit rebuilds `projects/*/PORTABLE.md` through a local pre-commit hook. On a new PC, copy the hook or run `python scripts/build_portable.py` before committing.
- Use Git tags for working milestones, for example `git tag v0.1` and `git push --tags`. Use `archive/` only for abandoned approaches.
- For team projects where teammates keep the code in their own repository, keep only notes, logs, and a link here.
- Never commit secrets, API keys, `.env` files, private team information, or other people's copyrighted files. Keep local-only material in `_local/`.

## 8. Code review and verification

- Claude Desktop is the default tool for implementing changes. You run tests, review the diff, and commit.
- For consequential changes you cannot fully test yourself (for example, strategy logic, motor or edge-sensor code, or backtest logic), send the diff and test output to ChatGPT for an independent review before logging and committing.
- Ask the reviewer to report file/line references and failure scenarios, and to label findings `CONFIRMED` or `POSSIBLE`. The reviewer should review, not rewrite, the code.
- Do not treat AI as the calculator of record. Recompute with Python or verify with real measurements.
- Check official sources for rules and requirements; check the cited passage when using NotebookLM; open the source when using Perplexity.

## 9. Prompts

### New project

```text
New project: <name>. Type: <hackathon/competition/course/personal>.
Deadline: <date>. Goal: <one line>.

Rules/brief: <paste, or "I'll add to docs/brief.md">.
Team: <solo / number of members and roles>.

Read AI-CONTEXT.md and projects/WORKFLOW.md. Create projects/<slug>/ using the workflow, add a row to projects/README.md, and add today's line to journal/.

Ask at most 3 questions to complete STATE.md. Then list what we must measure or look up first. No code yet.
```

### Continue a project

```text
Continue <project>. Read AI-CONTEXT.md and projects/<slug>/STATE.md
(and only the last 10 lines of LOG.md).

Today's goal: <one line>. Edit files directly and tell me the file
and location for each change.
```

**End a Claude Desktop session with:** `log it`

### External start (AI without MCP)

```text
Read this file first and follow its rules:
https://raw.githubusercontent.com/Shreyankkkkk/foundations/main/projects/<slug>/PORTABLE.md

If you cannot open it, say so and I will paste it. Do not guess its contents.

Today's goal: <one line>.
```

### External end (AI without MCP)

```text
End of session. In ONE code block give me:

1. A 5-line STATE.md update: decisions, constants, next actions, unknowns.
2. One LOG.md line: YYYY-MM-DD | what changed | why | evidence.

Use today's date: <date>.
```

### Glossary

```text
Terms from the brief: <paste>.

Sort into Tier 1 (must know first), Tier 2 (later), and Tier 3
(ignore for now). One line per term, no explanations yet.
```

### Teach me

```text
Teach me <term> from zero, for <project>.

Plain language first, then the technical definition. In one code block,
use this template:
Definition / Why it matters for this project / How it works /
Example / 3 self-test questions.

Maximum 200 words. Do not edit files.
```

### Quiz me

```text
Quiz me on this note: 5 questions, one at a time.
Wait for my answer, then correct me and say what to re-read.

<paste one note>
```

### Research a topic

```text
Research <topic> for <project>.

Find the most useful official documentation, reliable sources,
repositories, or papers. Start with the official source where one exists.
For each important finding, give me the source link and say what is
confirmed versus still uncertain. Keep it concise.
```

### Review a change

```text
Review this diff for correctness, logic errors, and failure cases.
Do not rewrite the code.

For each finding, give the file/line, the scenario that triggers it,
and mark it CONFIRMED or POSSIBLE. Separate definite bugs from questions
that need testing.

Diff and test output:
<paste>
```

## 10. Finish a project

Write `Retrospective.md` covering what worked and failed, important decisions, and unresolved items. Add certificates to `certificates/README.md`, push the work, then archive or delete old chats.
