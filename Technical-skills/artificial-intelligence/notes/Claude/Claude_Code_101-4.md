# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Daily Workflows

---

## Lesson 1 : The CLAUDE.md File

---

### The CLAUDE.md File

One of the most useful features in Claude Code is the `CLAUDE.md` file.

It provides Claude with **persistent memory and project-specific context** so that it doesn't have to rediscover the same information every time you start a new session.

### The Problem It Solves

Without a `CLAUDE.md` file, Claude Code starts each session with no project-specific memory.

It has to:

- Re-explore the codebase
- Understand the project's dependencies
- Figure out what features have already been implemented
- Discover the project's conventions
- Make assumptions about how things should be built

This can make it harder to steer Claude in the direction you want.

`CLAUDE.md` solves this by giving Claude a persistent set of instructions and information about the project.

### What is CLAUDE.md?

`CLAUDE.md` is a **Markdown file placed in the root of your project**.

Claude Code automatically reads it when starting a session.

A useful mental model is:

> **CLAUDE.md = an onboarding document for Claude**

It tells Claude things such as:

- What technologies the project uses
- How to run the project
- How to run tests
- How to lint the code
- Coding conventions
- Architectural preferences
- Project-specific rules
- Other information Claude should know when working on the project

You can also use `/init` to have Claude generate an initial `CLAUDE.md` based on the existing codebase.

### Example CLAUDE.md

A project might contain something like:

```markdown
# Project

This is a Next.js 15 app using the App Router, Tailwind, and Drizzle ORM.

# Commands

- Dev server: `pnpm dev`
- Run tests: `pnpm test`
- Lint: `pnpm lint`

# Code Style

- Use 2-space indentation
- Prefer named exports
- All API routes go in app/api/
- Use server actions instead of API routes where possible
```

Now, when you ask Claude Code to create a React component, it already knows:

- The project uses Next.js
- Tailwind is available for styling
- The project's preferred code style
- Where API routes belong
- When server actions should be preferred

This allows Claude to produce better results **immediately**, rather than spending time first figuring out how the project works.

### CLAUDE.md and Teams

`CLAUDE.md` can be committed to version control so that the entire team benefits from the same project instructions.

There is also a hierarchy of memory files depending on who the information is intended for.

#### Project-level CLAUDE.md

The project-level `CLAUDE.md` lives in the root directory of the project.

It contains information that should apply to the **entire project and team**.

Examples:

- Project architecture
- Framework and dependencies
- Commands
- Testing requirements
- Coding conventions
- Project-specific rules

Because it is part of the repository, it can be shared through version control.

#### User-level CLAUDE.md

A user-level `CLAUDE.md` lives in your Claude Code configuration directory.

This information applies **across your projects** and is intended for personal preferences.

For example:

- Personal coding preferences
- Comment-writing style
- General development preferences

The distinction is:

**Project-level = shared project knowledge**

**User-level = personal preferences across projects**

### Tips

#### 1. Save Corrections to Memory

If you repeatedly have to correct Claude about the same rule, explicitly ask Claude to save that behavior to memory.

For example:

> "Always use server actions instead of API routes for this type of functionality. Save this rule to memory."

This prevents you from having to repeat the same correction in future sessions.

The broader principle is:

> **If you repeatedly correct Claude about something, turn that correction into persistent project knowledge.**

#### 2. Reference Project Documentation

If your project already contains documentation that Claude should reference, you can use the `@` symbol followed by the file path.

For example:

```markdown
## README.md

Please read if you need more information: @README.md
```

This allows you to explicitly point Claude toward existing project documentation instead of rewriting that information in `CLAUDE.md`.

#### 3. Start Without a CLAUDE.md

It can be useful to **start a project without a `CLAUDE.md` file**.

This lets you observe where Claude repeatedly needs to be corrected.

You can then add only the information that is genuinely useful.

This keeps the file:

- Compact
- Focused
- Relevant
- Easier for Claude to work with

Once you understand what should be included, you can use `/init` to have Claude generate a starting version.

### What Should Go Into CLAUDE.md?

A good starting point is:

1. **Project stack** — frameworks, libraries, databases, and other important technologies
2. **Commands** — development, testing, linting, and build commands
3. **Coding preferences** — formatting and naming conventions
4. **Architecture** — important project structure and design decisions
5. **Project-specific rules** — things Claude repeatedly needs to know

You don't need to document everything.

The goal is to provide Claude with the **important context it needs to work effectively**.

### The Key Mental Model

Think of `CLAUDE.md` as the project's **persistent onboarding guide for Claude**.

Instead of repeatedly explaining:

> "This project uses X, we structure files like Y, and we always do Z..."

you can put those instructions into `CLAUDE.md` and let Claude reference them automatically.

### Recap

**CLAUDE.md = persistent project context for Claude Code.**

It helps Claude:

- Understand the project faster
- Follow project conventions
- Avoid repeated mistakes
- Remember important architectural decisions
- Use the correct commands and tools
- Produce more consistent results

A good starting point is:

**Stack → Preferences → Commands → Project-specific rules**

Then build the file incrementally as you discover where Claude needs additional guidance.

The main principle is:

> **Don't try to document everything. Add the information that repeatedly helps Claude make better decisions.**

---

### Video

[The CLAUDE.md File - YouTube](https://www.youtube.com/watch?v=O0FGCxkHM-U&t)

---

## Lesson 2 : Subagents

---

### What are Subagents?

Subagents are **specialized assistants that Claude Code can delegate tasks to**.

Each subagent operates in its own **isolated context window** with its own system prompt and task. Once it finishes, it returns a summary to the main Claude Code session while the detailed work it performed remains isolated.

The main benefit is **context management**.

Instead of having the main agent spend its context window exploring files, running searches, and investigating implementation details, a subagent can handle that work separately and return only the information that matters.

### How Subagents Work

Normally, everything Claude Code does contributes to the main context window:

- Reading files
- Searching the codebase
- Running commands
- Searching the web
- Receiving tool results
- Reasoning about the results

This can consume a significant amount of context, even when the main task only requires a small piece of information.

With a subagent, the workflow becomes:

**Main Agent → Delegate Task → Subagent Explores → Subagent Summarizes → Main Agent Receives Result**

The subagent receives two main inputs:

1. A **system prompt** that defines how the subagent should behave
2. A **task description** from the main agent describing what it needs to accomplish

The subagent then works independently using its available tools.

Its file reads, searches, tool calls, and intermediate reasoning stay inside its own context window.

Once finished, the main agent receives a **summary of the results** rather than the entire journey.

### Why Context Isolation Matters

Consider a task where you need to understand how refunds work in an unfamiliar payment system.

Without a subagent, Claude might:

- Search the codebase
- Read 15 different files
- Trace multiple function calls
- Search for related services
- Investigate different payment providers
- Eventually determine which service handles refunds

All of that exploration becomes part of the main context window.

If you only needed the answer:

> **"Which service handles refunds?"**

then most of that exploration is unnecessary context for the main agent.

A subagent can perform the investigation separately and return something like:

> **"Refunds are handled by the PaymentService in `services/payment.ts`."**

This gives you the **answer without the journey**.

### The Tradeoff

Subagents improve context efficiency, but there is a tradeoff.

The main agent does **not** have access to the complete process the subagent went through.

It receives the subagent's summary rather than:

- Every file it inspected
- Every search it performed
- Every intermediate result
- Every reasoning step

This means the main context stays clean, but you lose some visibility into how the conclusion was reached.

For straightforward research tasks where you only need the result, this tradeoff is often worthwhile.

### Built-in Subagents

Claude Code includes several built-in subagents.

#### General-purpose subagent

Used for **multi-step tasks that require both exploration and action**.

#### Explore subagent

Used for **fast codebase exploration and searching** when you need to understand where something is or how something works.

#### Plan subagent

Used during **Plan Mode** to research and analyze the codebase before presenting an implementation plan.

Claude Code can also use **custom subagents** that you define yourself.

### Creating Your Own Subagent

Subagents are defined using **Markdown files with YAML frontmatter**.

The easiest way to create one is through Claude Code:

```text
/agents
```

Then select **Create new agent**.

Claude will walk you through configuring the subagent, including:

- Its scope
- Its purpose
- The tools it can access
- Its name and description
- Its behavior
- Its color

Claude then generates the configuration for the subagent.

The description also helps Claude determine **when the subagent should be used** based on the task you give it.

### Customizing Subagents

Subagents can be customized beyond their basic configuration.

#### Persistent memory

A subagent can have **persistent memory**, allowing it to retain information across conversations.

This is useful when you repeatedly use the same specialized subagent on a project.

#### Preload skills

You can also preload skills into a subagent using the `skill` key and specifying the skills by name.

Unlike skills in the main conversation, the **entire skill is loaded into the subagent's context**, so this should be used intentionally.

### Key Mental Model

Don't think of a subagent as simply another Claude conversation.

Think of it as:

> **"A separate worker that handles a focused task and returns only the result I need."**

The main agent can delegate context-heavy work while keeping its own context focused on the actual feature or problem being solved.

### Recap

**Subagents = Focused work + Isolated context + Summarized results**

They are especially useful when a task requires a lot of exploration but the main agent only needs the final answer.

The workflow is:

**Main Agent → Delegate → Subagent explores → Subagent summarizes → Main Agent continues**

Subagents help Claude Code scale to longer and more complex tasks by keeping unnecessary exploration out of the main context window.

They can be used through Claude Code's built-in subagents or customized with your own system prompts, tools, memory, and skills.

---

### Video

[Subagents - YouTube](https://www.youtube.com/watch?v=jKErNxuxPXg)

---
