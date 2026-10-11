# AI Workflow Prompts

Reusable prompts for the AI tools and tasks defined in `projects/WORKFLOW.md`.

## General rules

- Use one AI per task. Use the designated fallback only when the primary AI is unavailable.
- Give the AI one concrete objective per task.
- Do not paste files the AI can already access. For external AIs, provide the project's `PORTABLE.md` and only the additional material needed for the task.
- Replace every `<placeholder>` before sending.
- Keep stable workflow rules in `AI-CONTEXT.md` and `WORKFLOW.md`; do not repeat them in every prompt.
- Review AI-generated code, research, calculations, and conclusions independently.
- Never treat an AI's claim as verified evidence without checking it.
- Keep responses concise unless the task genuinely requires depth.

---

## 1. Claude Desktop — Continue a project

**Use for:** Implementing features, fixing bugs, editing project files, and maintaining documentation.

**Input:** Project name and today's objective.

```text
Continue <project>. Read AI-CONTEXT.md, projects/<slug>/STATE.md, and only the last 10 lines of LOG.md.

Goal: <specific outcome>.

Follow the repository workflow. Inspect CODEMAP.md first for code navigation, then read only the relevant source files and dependencies. Make the smallest correct change directly in the files. Do not refactor unrelated code or create unnecessary files.

Verify the change with relevant tests or checks. Report only changed files, verification results, and unresolved issues. Do not commit or push.
```

For a simple change, shorten this to:

```text
<goal>. Follow the existing workflow, inspect the relevant code through CODEMAP.md, make the minimal change, and verify it. No unrelated changes. Do not commit.
```

### 1.1 Claude Desktop — New project

**Use for:** Creating a project folder for a competition, hackathon, course, or personal build.

```text
New project: <name>.
Type: <hackathon/competition/course/personal>.
Deadline: <date or none>.
Goal: <one sentence>.
Brief: <source or path to docs/brief.md>.
Team: <solo or team structure>.

Read AI-CONTEXT.md and projects/WORKFLOW.md. Follow the new-project procedure and create the required project structure, documentation, project index entry, and journal entry.

Ask at most 3 questions if essential information is missing. Separate verified facts from assumptions and unknowns. Do not begin implementation.
```

### 1.2 Claude Desktop — Primary research

**Use for:** Extracting requirements from a competition brief, rulebook, specification, or project documentation.

```text
Perform primary research for <project>. Read docs/brief.md and STATE.md.

Extract the requirements that directly affect implementation:
- Rules, constraints, deliverables, and judging criteria.
- Every required constant or parameter, with its source.
- Unknown values and how each can be measured or verified.
- Compliance requirements and potential disqualification risks.
- The immediate next actions.

Do not fill gaps using memory or guesswork. Mark unverified information as RECALLED or PLACEHOLDER, as appropriate, and identify the authoritative source or test needed to resolve it.

Keep the output actionable. Do not implement anything.
```

### 1.3 Claude Desktop — Log completed work

**Use after the work is finished and reviewed.**

Send:

```text
log it
```

The established workflow determines the required updates to `STATE.md`, `LOG.md`, and `journal/YYYY-MM.md`. Do not request a second narrative report.

---

## 2. External AI — Start a project session

**Use for:** ChatGPT, DeepSeek, Perplexity, or Claude on the web when it cannot access the local MCP.

Replace `<slug>` with the project directory name.

```text
Read and follow this project context:
https://raw.githubusercontent.com/Shreyankkkkk/foundations/main/projects/<slug>/PORTABLE.md

If you cannot access the file, tell me rather than guessing.

Today's task: <specific objective>.

Use the provided context, and request additional material only when necessary. Distinguish sourced facts from assumptions. Keep the response focused on the requested deliverable.
```

For code-related tasks, also provide:

`https://raw.githubusercontent.com/Shreyankkkkk/foundations/main/scripts/codemap/CODEMAP.md`

The code map is an index, not a substitute for the actual source code.

If the task requires reviewing uncommitted changes, provide the relevant `git diff` and test output as well.

---

## 3. ChatGPT / DeepSeek — Independent code review

**Use for:** Reviewing Claude's implementation, particularly consequential changes. The reviewer must not rewrite the code.

**Input:** Project context, relevant diff, and actual test output.

```text
Act as an independent code reviewer. Review this diff against the intended behavior and supplied project context.

Objective: <what the change is supposed to accomplish>.

Check for:
- Functional bugs and incorrect assumptions.
- Edge cases, failure modes, and regressions.
- Violations of project constraints or existing interfaces.
- Incorrect calculations, state transitions, or resource handling where relevant.
- Missing tests for consequential behavior.

For every finding, provide:
1. Severity.
2. File and line in the diff.
3. The specific defect.
4. A concrete scenario in which it fails.
5. Whether the issue is confirmed or possible, and the evidence.

Do not rewrite the code, propose broad refactors, or report style preferences as bugs. If you find no material issues, say so. Do not claim tests passed unless the supplied evidence establishes that.
```

**Review standard:** A finding is a claim to verify, not an instruction to apply a patch blindly.

---

## 4. Perplexity — Secondary research

**Use for:** Current documentation, repositories, release notes, technical approaches, compatibility, and existing implementations.

**Input:** A specific research question and relevant project context.

```text
Research <topic> for <project>.

Question: <specific question to answer>.

Find the most relevant primary sources first: official documentation, specifications, release notes, original repositories, and papers where applicable.

Determine:
- What is currently supported and under what conditions.
- Compatibility requirements, limitations, and known issues.
- Which options are relevant to my actual requirements.
- What the evidence supports and what remains uncertain.

Provide a concise comparison or recommendation, with direct source links attached to the claims they support. Prefer current sources and state publication or release dates where relevant.

Do not treat search-result snippets as verification. Distinguish facts established by opened sources from claims that remain unverified. Avoid generic background that does not affect the decision.
```

For a narrow factual question, use a shorter prompt:

```text
Find the current official documentation for <specific question>. Give me the direct source, the relevant answer, any version constraints, and what remains uncertain.
```

**My verification step:** Open the cited source yourself before marking a finding `SOURCED` in project notes.

---

## 5. Consensus — Academic paper discovery

**Use for:** Quantitative finance, statistics, control systems, validation methods, and other questions where published research matters.

```text
Find academic research addressing:

Research question: <specific question>.

Context: <why this matters for the project>.

Prioritize directly relevant peer-reviewed research and original studies. Identify the most relevant papers and summarize each in terms of:
- Research question and method.
- Data, experimental setup, or assumptions.
- Main findings.
- Limitations and applicability to my question.
- DOI or direct paper link, publication year, and citation.

Include evidence that contradicts the leading conclusion where available. Distinguish empirical findings from theoretical results and author speculation.

Do not infer that a method works in my project simply because a paper reports success in a different setting. Identify which papers deserve full-text review.
```

For quantitative strategies, add:

```text
Pay particular attention to out-of-sample validation, data leakage, transaction costs, multiple testing, survivorship bias, and whether the reported result could plausibly survive realistic deployment.
```

**Verification:** Read the original abstract and methods before relying on a paper. Check whether the full text was actually available to the research tool.

---

## 6. NotebookLM — Analyze collected documents

**Use for:** A collection of PDFs, rulebooks, technical papers, and documents already uploaded to a notebook.

```text
Using the supplied sources, answer this question:

<question>.

Ground factual claims in the available documents and cite the relevant source passages. If the documents do not establish an answer, say so.

Separate:
- Explicit statements in the sources.
- Conclusions reasonably derived from them.
- Conflicts or gaps between sources.
- Information that still requires external verification.

Prioritize information relevant to <project objective>. Do not produce a generic summary of every document. End with the findings that change a decision or identify the next necessary verification.
```

For a pile of competition documents, add:

```text
Prioritize binding rules, eligibility, constraints, judging criteria, deadlines, submission requirements, and penalties. If two sources conflict, identify the conflict and determine which source is authoritative if the evidence permits.
```

**Verification:** Open the cited passage in the original source before treating a critical requirement as confirmed.

---

## 7. ChatGPT — Learn a new topic from zero

**Use for:** Learning a technical concept without loading the entire repository or project history.

### 7.1 Glossary

```text
For this topic: <topic>, explain the following terms for a beginner:

<terms>.

Sort them into:
Tier 1 — must understand first.
Tier 2 — learn when needed.
Tier 3 — ignore for now.

Give one concise sentence per term. Identify prerequisite relationships where useful. Do not explain the terms in depth yet.
```

### 7.2 Teach me

```text
Teach me <topic> from zero, for <project or application>.

Start with an intuitive explanation, then give the precise technical definition. Explain how it works, why it matters for my application, and one concrete example.

Structure the note as:
1. Definition.
2. Why it matters.
3. How it works.
4. Example.
5. Common misconception.
6. Three self-test questions.

Keep it focused on the knowledge required for my next practical task. Do not expand into unrelated advanced topics. Do not modify files.
```

For a topic that is already familiar, omit the beginner framing and ask only about the specific gap.

---

## 8. Claude Web — Test understanding

**Use for:** Testing knowledge from a single note, without reloading the repository.

```text
Quiz me on the following note.

Ask one question at a time. Wait for my answer before evaluating it.

For each answer, identify what is correct, what is incorrect or incomplete, and the specific concept I should revisit. Ask follow-up questions when my answer suggests memorization without understanding.

Cover the core mechanisms, assumptions, and practical application. After 5 questions, summarize my weak areas and what to reread.

Do not reveal the answer before I attempt the question.

NOTE:
<paste one note>
```

---

## 9. ChatGPT — Mathematics, physics, statistics, and derivations

**Use for:** Coursework and quantitative derivations where reasoning and verification matter.

```text
Solve or explain this problem:

<problem>.

What I tried:
<attempt, or "I have not attempted it yet">.

Requirements:
- State the relevant assumptions and definitions.
- Derive the result using valid steps.
- Explain the key reasoning rather than skipping directly to the answer.
- Check units, signs, boundary cases, and assumptions where applicable.
- Distinguish exact results from numerical approximations.

If computation would help, provide Python code using appropriate libraries or suggest a reproducible numerical check. Do not invent computational results or claim code was executed if it was not.

Finish with the result, its interpretation, and the most important condition under which it would fail.
```

For a problem where learning is the priority, add:

```text
Do not immediately reveal the full solution. Give me the next useful hint and let me attempt the next step.
```

---

## 10. DeepSeek — Independent mathematical or statistical review

**Use for:** A second opinion on a derivation or statistical-test design.

```text
Independently check this derivation or statistical method. Do not assume the supplied result is correct.

<derivation or method>.

Check the assumptions, algebra, logic, definitions, and interpretation. Identify the first invalid step if one exists. If the result is correct, explain why and identify important limitations.

Separate confirmed errors from possible concerns. Do not merely reproduce the original derivation or agree with its conclusion.

Provide a compact verification that I can independently reproduce in Python or by hand. Do not invent numerical results.
```

Verify numerical claims with Python, SymPy, NumPy, or another suitable independent method.

---

## 11. ChatGPT — Interpret a circuit, schematic, or robot-layout image

**Use for:** Visual inspection of electronics and robotics diagrams.

Provide the image and one specific question.

```text
Inspect this image to answer:

<specific question>.

Identify the visible components, labels, connections, and relevant geometry. Distinguish what is clearly visible from what is ambiguous or cannot be determined from the image.

Do not infer an electrical connection, pin assignment, component value, or physical dimension unless the image supports it. If additional information is needed, identify the exact datasheet, label, measurement, or photograph that would resolve the uncertainty.

Give a concise answer and the verification needed before acting on it.
```

Never use an AI interpretation alone to establish a critical pinout or wiring connection. Verify against the datasheet and physical hardware.

---

## 12. External AI — End a session

**Use after completing a task with an AI that cannot edit local files.**

```text
End this session. Return only the following in one code block:

1. A concise STATE.md update containing only verified changes to the current project status, decisions, constants, remaining unknowns, and next actions.
2. One LOG.md line in this format:
YYYY-MM-DD | what changed | why | evidence (file or commit).

Use the actual current date. Do not invent completed work, measurements, sources, or commits. If the project's state did not materially change, say so instead of fabricating an update.
```

Paste the result into the appropriate files yourself. Keep the state concise and the log factual.

---

## 13. Prompt selection rules

| Task                                    | AI                              | Prompt                      |
| --------------------------------------- | ------------------------------- | --------------------------- |
| Edit project files or code              | Claude Desktop                  | Continue a project          |
| Start a new project                     | Claude Desktop                  | New project                 |
| Extract requirements from a brief       | Claude Desktop                  | Primary research            |
| Review consequential code changes       | ChatGPT; DeepSeek fallback      | Independent code review     |
| Research current technical sources      | Perplexity; ChatGPT fallback    | Secondary research          |
| Find academic papers                    | Consensus; Perplexity fallback  | Academic paper discovery    |
| Analyze a collection of documents       | NotebookLM; Claude Web fallback | Analyze collected documents |
| Learn a new topic                       | ChatGPT; Claude Web fallback    | Glossary, then Teach me     |
| Test understanding                      | Claude Web; ChatGPT fallback    | Test understanding          |
| Solve coursework                        | ChatGPT; DeepSeek fallback      | Mathematics and derivations |
| Independently check a derivation        | DeepSeek; ChatGPT fallback      | Mathematical review         |
| Inspect a circuit or robot-layout image | ChatGPT; DeepSeek fallback      | Image interpretation        |
| End a non-MCP session                   | Same AI                         | End a session               |

Follow `projects/WORKFLOW.md` for the current tool assignments and fallback rules.

---

## 14. Sources and rationale

These references inform the prompt conventions used in this document:

- Anthropic, [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — explicit actions, focused instructions, response formatting, and tool use.
- OpenAI, [How to create a good prompt](https://help.openai.com/en/articles/4936848-how-do-i-create-a-good-prompt-for-an-ai-model-like-gpt-4) — clarity, context, appropriately scoped tasks, and iterative refinement.
- Perplexity, [Prompting tips and examples](https://www.perplexity.ai/help-center/en/articles/10354321-prompting-tips-and-examples) — instruction, context, input, keywords, and output format.
- Consensus, [How Consensus works](https://help.consensus.app/en/articles/9922673-how-consensus-works) — research retrieval, citations, and limitations of AI-generated summaries.

These are task-oriented defaults, not claims that one wording is universally optimal for every model or version. Use the shortest prompt that preserves the requirements of the actual task.
