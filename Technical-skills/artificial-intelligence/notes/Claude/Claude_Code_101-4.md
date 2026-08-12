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

