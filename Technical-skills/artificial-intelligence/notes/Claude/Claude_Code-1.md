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

## Lesson 1 : A CLAUDE.md THAT follows

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

## Lesson 2 : Verification Skills

---

### Why Build a Verification Skill First

A verification skill automates the process of checking Claude's work after completing a task.

Without one:
- You ask Claude to make a change.
- Claude finishes.
- You have to remember to ask it to test and review the work.
- If you forget, bad code can slip through.

With one:
1. Claude completes the task.
2. The verification skill triggers.
3. It runs the test suite.
4. It reads the diff.
5. It checks that tests were not weakened just to make them pass.
6. It reports **pass or fail**, including the evidence.

The key idea:

> "Done" means the verification gates were actually run and their results were explicitly reported.

Running tests alone is not enough. A test could have been weakened so that it passes regardless of whether the code works correctly.

---

### When to Create a Skill

A skill is useful for repeated procedures.

**Rule of thumb:**

> If you've typed the same multi-step instruction twice, consider turning it into a skill.

Examples:
- Verification checklist
- Release checklist
- Migration procedure
- Pre-PR checks
- Repeated testing workflow

---

### A Skill Can Contain More Than `skill.md`

A skill is a folder, not just a single file.

Example:

```text
.claude/
└── skills/
    └── verification/
        ├── skill.md
        ├── reference.md
        └── check.sh
```

#### `skill.md`

Contains:
- The skill name
- The description that triggers it
- The procedure Claude should follow

Keep this file **short and focused**.

#### `reference.md`

Contains:
- Detailed explanations
- Reference material
- Longer instructions

Claude can read it when deeper information is needed.

#### Scripts

Scripts can be placed inside the skill folder.

Example:

```text
check.sh
```

Claude can execute the script instead of loading the script's contents into its context.

This allows a skill to carry its own tools.

---

### Keep Skills Lean

The main `skill.md` should describe **what to do**.

Move:
- Long explanations → `reference.md`
- Detailed reference material → reference files
- Executable checks → scripts

This keeps the main skill easy for Claude to follow.

---

### Instruction Surfaces

Different types of instructions belong in different places.

| Instruction | Where it belongs |
|---|---|
| Always-follow project conventions | `CLAUDE.md` |
| Procedures for a specific type of task | Skill |
| Reference material for a task | Skill reference files |
| Rules that must be technically enforced | Hook |

#### `CLAUDE.md`

Use for conventions that apply broadly.

Examples:
- Naming rules
- File locations
- Project conventions

#### Skills

Use for procedures and reference material associated with particular tasks.

Examples:
- Verification procedure
- Release procedure
- Migration procedure
- PR checklist

#### Hooks

Use when Claude **must not be able to skip the rule**.

`CLAUDE.md` and skills are instructions Claude follows.

A hook is code that actually runs and can enforce or block an action.

---

### Verification Skill Workflow

```text
Task completed
      ↓
Verification skill triggers
      ↓
Run tests
      ↓
Read diff
      ↓
Check tests were not weakened
      ↓
Collect evidence
      ↓
PASS / FAIL
```

The important distinction:

**"Claude says it works" ≠ verified**

**"Tests were run, diff was reviewed, tests were checked for weakening, and results were reported" = verified**

---

### Key Takeaways

1. Build a verification skill early.
2. Automate repeated checking procedures.
3. Run tests automatically.
4. Review the diff.
5. Check that tests weren't weakened to produce a passing result.
6. Report explicit evidence for pass/fail.
7. Keep `skill.md` lean.
8. Put detailed material in reference files.
9. Put executable checks in scripts.
10. Use `CLAUDE.md` for general conventions.
11. Use skills for task-specific procedures.
12. Use hooks for rules that must be enforced.
13. Store project skills in `.claude/skills`.

---

### Video

[Building Verification Skills - Youtube](https://www.youtube.com/watch?v=soLPOXXAc1w)

---

## Lesson 3 : Permission Modes

---

### Permission Modes

Permission modes control what Claude is allowed to do without asking for approval.

Instead of approving every action individually, choose a mode that matches the level of trust you are comfortable with.

---

### The Six Permission Modes

| Mode | What Claude Can Do |
|---|---|
| **Manual** | Reads without prompting. Everything else requires approval. |
| **Accept Edits** | Reads, edits files, and runs common file-system Bash commands without asking. |
| **Plan** | Reads and researches, then proposes changes without editing. |
| **Auto** | Accepts actions automatically, with a separate classifier model reviewing each action first. |
| **Don't Ask** | Only pre-approved tools are allowed. Everything else is automatically denied. |
| **Bypass Permissions** | Skips all permission checks. Only use inside an isolated container or VM. |

---

### Cycling Through Modes

Press:

```text
Shift + Tab
```

This cycles through the everyday modes.

The status bar shows the current permission mode.

---

### Auto Mode

**Auto** is designed for hands-off work.

Before each action runs:

```text
Claude wants to perform an action
        ↓
Classifier reviews the action
        ↓
Allowed → action runs
Blocked → action does not run
```

The classifier checks whether Claude's **intent** matches what it is supposed to be doing.

#### Examples of actions it may block

- Production deployments
- Production migrations
- Force pushes
- Piping downloaded code directly into a shell
- Sending sensitive information to external endpoints
- Destroying files needed for the session

#### Examples of normal actions it may allow

- Editing files in the local project
- Installing dependencies from the lock file
- Read-only requests
- Pushing to your own branch

---

### What Auto Mode Does NOT Check

The classifier checks **intent**, not whether the resulting code is correct.

For example:

```text
You ask Claude to refactor authentication
        ↓
Claude writes broken authentication code
        ↓
Classifier sees a normal refactor
        ↓
Action is allowed
```

So Auto mode does **not** replace testing or verification.

---

### Auto Mode + Stop Hook

For stronger protection, combine:

```text
Auto Mode
    +
Stop Hook
```

#### Auto Mode

Checks what Claude is **trying to do** before each action.

#### Stop Hook

Checks whether the resulting code **actually works** after Claude finishes.

```text
           Claude works
                ↓
      ┌─────────┴─────────┐
      ↓                   ↓
 Auto classifier      Stop hook
 checks intent        runs checks/tests
      ↓                   ↓
 Safe action?          Correct code?
```

Together:

- **Auto mode → intent**
- **Stop hook → correctness**

---

### Don't Ask Mode

Use **Don't Ask** when nobody will be available to approve prompts.

Good use cases:

- CI pipelines
- Scheduled jobs
- Overnight tasks
- Automated batches

Only pre-approved tools are allowed.

Anything outside the approved list is automatically denied rather than waiting for someone to respond.

---

### Bypass Permissions

**Bypass Permissions** skips permission checks completely.

It is equivalent to running Claude with dangerously skipped permissions.

Only use it inside an **isolated container or virtual machine**.

Do not use it casually on your normal machine or important projects.

---

### Choosing a Mode

| Situation | Recommended Mode |
|---|---|
| Normal hands-on work | **Manual** |
| Coding while reviewing changes afterward | **Accept Edits** |
| Researching/planning before implementation | **Plan** |
| Hands-off development | **Auto** |
| CI / scheduled / unattended work | **Don't Ask** |
| Fully isolated environment | **Bypass Permissions** |

---

### Key Takeaways

1. Permission modes control what Claude can run without asking.
2. **Manual** is the most hands-on everyday mode.
3. **Accept Edits** is useful for normal coding iterations.
4. **Plan** is for research and planning without modifications.
5. **Auto** is the main hands-off mode.
6. Auto uses a separate classifier to review actions before execution.
7. The classifier checks **intent**, not whether the code is correct.
8. Pair Auto with a **stop hook** for post-task verification.
9. **Don't Ask** is designed for unattended runs.
10. **Bypass Permissions** should only be used in isolated environments.
11. Use `Shift + Tab` to cycle through permission modes.

---

### Video

[Permission Modes - Youtube](https://www.youtube.com/watch?v=Fjg4O-ZcRSU)

---
