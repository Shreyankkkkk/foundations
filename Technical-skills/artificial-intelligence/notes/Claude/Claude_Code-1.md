# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Daily Workflows

---

## Lesson 1 : Steering Long Sessions

---

### 1. Plan before execution

- **Plan Mode** → Claude researches the codebase without modifying it.
- Claude produces a plan before implementation.
- **Review the plan yourself.**
- Correct/add anything missing.
- Only then let Claude execute.

> **Core idea:** Planning first is cheaper than fixing a bad implementation later.

---

### 2. Compact

```text
/compact
```

- Summarizes the current conversation.
- Replaces the old context with the summary.
- Frees context space for a longer task.
- Risk: important information can be lost.

**Better:**

```text
/compact Focus on the --version flag implementation
```

The instruction after `/compact` tells Claude what information matters.

> **Core idea:** Don't blindly compact. Tell Claude what to preserve.

---

### 3. Rewind

**Double-tap `Esc` on an empty prompt.**

Every user prompt creates a checkpoint.

You can:

- **Restore code and conversation** → undo both.
- **Restore conversation** → undo the conversation only.
- **Restore code** → undo the code only.
- **Summarize from here** → compress everything after that checkpoint.
- **Summarize up to here** → compress everything before that checkpoint.

**Use when:** Claude starts going in the wrong direction.

> **Core idea:** Don't spend 30 prompts trying to fix a bad direction. Rewind.

---

### 4. Goal

```text
/goal all tests in src/billing pass, and the type checker reports zero errors
```

- Defines what **"done"** means.
- Claude continues working toward that condition.
- Claude stops when the condition is confirmed.
- Cancel with:

```text
/goal clear
```

**Important:** The evaluator checks the **visible transcript**, so the goal needs to be verifiable.

**Good:**

> All tests pass and type checking reports zero errors.

**Bad:**

> Make the code really good.

> **Core idea:** Define the destination, not every step.

---

### 5. Loop

- Runs a prompt repeatedly.
- Can run at a fixed interval or self-paced.
- Useful for repeatedly checking something external.

**Example use:**

> Check CI status and fix issues when they appear.

Stop with **Esc**.

> **Core idea:** Useful when the environment changes while Claude is working.

---

### 6. Worktrees

When running multiple Claude sessions on one repository:

#### Without worktrees

```text
Claude A ──┐
           ├── same files → conflicts
Claude B ──┘
```

#### With worktrees

```text
Claude A → Worktree A
Claude B → Worktree B
Claude C → Worktree C
```

Each session gets its **own independent copy of the working tree**.

This allows parallel work without agents modifying the same files underneath each other.

Clean worktrees can be automatically removed when the session exits.

---

### 7. `.worktreeinclude`

A file at the repository root can specify Git-ignored files that should be copied into each worktree.

Useful for things such as:

- Local configuration
- Environment files
- Other ignored files needed to run the project

These stay out of Git while still being available to each worktree.

---

### The Actual Workflow

```text
PLAN
  ↓
Review plan
  ↓
EXECUTE
  ↓
Monitor
  ↓
Claude drifting?
  ├── YES → REWIND
  └── NO
       ↓
Context getting full?
  ├── YES → COMPACT + instructions
  └── NO
       ↓
Can "done" be clearly defined?
  ├── YES → GOAL
  └── NO
       ↓
Need repeated monitoring?
  ├── YES → LOOP
  └── NO
       ↓
Need parallel agents?
  ├── YES → WORKTREES
  └── NO
       ↓
      DONE
```

### The 5 Things to Remember

| Tool | Purpose |
|---|---|
| **Plan** | Think before changing code |
| **Compact** | Free context while preserving what matters |
| **Rewind** | Undo a bad direction |
| **Goal** | Tell Claude exactly what "done" means |
| **Worktree** | Let multiple Claude sessions work safely in parallel |

### One-Line Mental Model

> **Plan → Execute → Steer → Rewind if wrong → Compact when needed → Goal when autonomous → Worktrees when parallel.**

---

### Video

[Steering Claude Code - YouTube](https://www.youtube.com/watch?v=l_4ZYAiyP7U)

---