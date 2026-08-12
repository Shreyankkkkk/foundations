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

# Configure Claude

---

## Lesson 2 : A CLAUDE.md THAT follows

---

### 1. CLAUDE.md Is Guidance, Not Enforcement

- `CLAUDE.md` gives Claude guidance.
- It is **not hard enforcement**.
- Every line competes for Claude's attention.
- As the file grows, individual rules become less reliable.

> **Core idea:** Keep `CLAUDE.md` lean. The less it contains, the more reliably Claude follows it.

---

### 2. Know When to Use CLAUDE.md

Before adding a rule, ask:

> **Is this guidance or a hard rule?**

#### Guidance → `CLAUDE.md`

Examples:

- Coding conventions
- Project structure
- Preferred workflows
- Naming conventions

#### Hard rule → Hook

Example:

> Never push directly to `main`.

Putting this only in `CLAUDE.md` means Claude is being asked to remember it.

A **PreToolUse hook** can actually block the action.

> **Core idea:** Use `CLAUDE.md` for conventions. Use hooks for rules that must not be violated.

---

### 3. The Four CLAUDE.md Locations

Claude can load `CLAUDE.md` from four locations.

| Location | Purpose |
|---|---|
| **Managed policy** | Organization-level rules controlled by the platform/team |
| **User** | Personal preferences across projects on your machine |
| **Project** | Shared project rules, usually committed to Git |
| **Local** | Personal rules for one repository, ignored by Git |

#### Local

Useful for personal project-specific notes that shouldn't affect teammates.

Example:

> You're refactoring something on your own branch and want Claude to remember temporary architectural decisions.

Put those in the **local** CLAUDE.md rather than the shared project file.

---

### 4. Split Large Files with Imports

Instead of putting everything into one file:

```text
@.claude/conventions/code-style.md
@.claude/conventions/testing.md
@.claude/conventions/workflow.md
```

This makes the project easier to organize.

#### Important

Imports **do not reduce context usage**.

Claude expands the imported files inline when it launches.

So:

```text
One large CLAUDE.md
        ↓
   lots of content
```

and:

```text
CLAUDE.md
   ↓
imports
   ├── code-style.md
   ├── testing.md
   └── workflow.md
```

still result in all of that content being loaded.

> **Core idea:** Use imports for organization, not for reducing context.

---

### 5. Write Specific, Checkable Rules

Vague rules are harder for Claude to follow.

#### Bad

> Follow best practices for API routes.

#### Good

> Put new API routes in `src/api/handlers`, one per file.

The second rule is:

- Specific
- Easy to understand
- Easy to check

> **Core idea:** If you can't clearly check whether a rule was followed, the rule is probably too vague.

---

### 6. Say What to Do Instead

When banning something, provide the replacement.

#### Bad

> Don't use default exports.

#### Good

> Use named exports, not default exports.

The second version tells Claude exactly what behaviour is expected.

> **Core idea:** Don't only say what Claude shouldn't do. Tell it what to do instead.

---

### 7. Don't Overuse Emphasis

Words such as:

- `IMPORTANT`
- `MUST`
- `YOU MUST`

can make rules stand out.

But if everything is emphasized, nothing is emphasized.

Treat emphasis as a limited resource.

#### Good

Use strong emphasis for the **2–3 rules that matter most**.

#### Bad

```text
IMPORTANT: rule 1
IMPORTANT: rule 2
IMPORTANT: rule 3
IMPORTANT: rule 4
IMPORTANT: rule 5
IMPORTANT: rule 6
```

> **Core idea:** If everything screams, nothing stands out.

---

### 8. Treat CLAUDE.md Like Living Code

`CLAUDE.md` should evolve as you use Claude.

When Claude repeatedly does something wrong:

1. Identify what went wrong.
2. Decide whether the problem belongs in `CLAUDE.md`.
3. Add a clear rule if necessary.
4. Make the rule specific and checkable.
5. Continue working.

You can also tell Claude:

```text
Add that to CLAUDE.md.
```

This allows the file to improve based on real problems encountered during development.

> **Core idea:** Claude making a repeated mistake is a potential bug in your instructions.

---

### The 5 Rules to Remember

1. **Move hard rules to hooks** where they can actually be enforced.
2. **Use imports to organize** large CLAUDE.md files, not to reduce context.
3. **Make rules specific and checkable.**
4. **Name the replacement** when banning something.
5. **Keep revising CLAUDE.md** when Claude gets something wrong.

---

### One-Line Mental Model

> **CLAUDE.md = guidance. Hooks = enforcement. Keep CLAUDE.md lean, specific, and constantly revised.**

---

### Video

[Writing CLAUDE.md - Youtube](http://youtube.com/watch?v=sfE5UQEumdM)

---

