# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Automate Repeat Work

---

## Lesson 1 : Routines and Headless

---

### Core Idea

Once a task is reliable enough to trust, automate it instead of manually starting it every time.

There are two main approaches:

1. **Routines** — managed automation with little/no infrastructure.
2. **Headless mode / Agent SDK** — automation controlled by your own scripts or applications.

---

### 1. Routines

A **routine** is a saved prompt that runs automatically.

It combines:

- A prompt
- A repository
- Connectors
- A trigger

The infrastructure runs on Anthropic's side, so you don't need your own machine running continuously.

#### Possible triggers

- Cron schedule
- HTTP POST
- GitHub events

#### Good use cases

- Daily dependency audits
- PR review/triage
- Recurring repository checks
- Regular issue/ticket analysis

#### Creating a routine

From the web:

```text
claude.ai/code/routines
```

Or from Claude Code:

```text
/schedule daily dependency audit at 9am
```

#### Important limitations

- Routines are a **research preview**.
- Recurring schedules run at most **hourly**.
- Each run starts from a fresh clone of the default branch.
- By default, routines can only push to branches beginning with:

```text
claude/
```

---

### 2. Headless Mode

Headless mode allows Claude Code to run without the interactive UI.

The main flag is:

```bash
-p
```

or:

```bash
--print
```

Example:

```bash
claude -p "summarize the changes in this diff"
```

This makes Claude behave more like a normal command-line program:

```text
input → Claude → output
```

#### Important

`-p` does **not** automatically discover:

- Hooks
- Skills
- Plugins
- MCP servers
- CLAUDE.md

You explicitly control what the headless run gets.

The benefit is faster and more predictable startup.

---

### 3. Structured Output

Headless Claude can return structured JSON instead of only normal text.

You can provide a JSON schema:

```bash
claude -p "Extract the exported function names from src/core/style.js" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

The resulting structured data appears in:

```text
structured_output
```

You can extract it with:

```bash
jq
```

Example:

```bash
... | jq '.structured_output.functions'
```

This allows Claude's output to be passed directly into:

- Scripts
- Databases
- Other programs
- Automation pipelines

---

### 4. Resuming Sessions

Longer automation doesn't have to happen in one command.

Claude can return a session ID.

Save that ID and resume the session later:

```bash
claude --resume "$(jq -r .session_id /tmp/plan.json)"
```

This allows automation to happen in multiple stages.

Example:

```text
Script 1
    ↓
Claude creates a plan
    ↓
Session ID saved
    ↓
Script 2
    ↓
Resume same session
    ↓
Claude implements the plan
```

---

### 5. `--bare`

`--bare` is intended for deterministic CI runs.

Use it when you want Claude Code inside a pipeline to have predictable, repeatable behavior.

```bash
claude --bare
```

---

### 6. Agent SDK

The Agent SDK allows you to put Claude Code inside your own application.

It is available for:

- TypeScript
- Python

It provides a `query` function and allows you to control things such as:

- `allowedTools`
- System prompt
- Permission mode

Your application can then process Claude's streamed messages and decide what to do with them.

Conceptually:

```text
Your Python/TypeScript application
            ↓
       Agent SDK
            ↓
        Claude
            ↓
     Tool execution
            ↓
      Your application
```

---

### 7. Choosing the Right Method

| Method | Use when |
|---|---|
| **Routines** | You have a recurring task and want the simplest automation |
| **Headless `-p`** | You want Claude inside your own scripts/pipelines |
| **`--bare`** | You need predictable CI runs |
| **Agent SDK** | You want Claude integrated directly into your own application |

### Mental Model

```text
Simple recurring task
        ↓
     Routines
        ↓
Need your own scripts/environment?
        ↓
    Headless -p
        ↓
Need deterministic CI?
        ↓
      --bare
        ↓
Need Claude inside your own application?
        ↓
    Agent SDK
```

### Key Takeaway

**Start with routines.**

Move to headless mode when you need your own scripts and environment.

Use `--bare` for deterministic CI.

Use the Agent SDK when Claude needs to become part of your own application.

---

### Video

[Automate Claude Code - Youtube](https://www.youtube.com/watch?v=b9TCW-pdzDA)

---