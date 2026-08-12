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

## Lesson 3 : Skills

---

### What Are Skills?

Skills allow you to teach Claude **how to perform a specific task once and have it automatically apply that knowledge whenever it is relevant**.

Without skills, you may repeatedly explain the same instructions to Claude:

- Your team's coding standards
- How you want PR reviews structured
- Your preferred commit message format
- How documentation should be written
- Your organization's design guidelines

A skill turns these repeated instructions into reusable knowledge.

### How Skills Work

An **agent skill** is a collection of instructions, scripts, and resources that an agent can discover and use to complete a particular type of task more accurately and efficiently.

In Claude Code, the core file is:

```text
skill.md
```

The skill's **description** is especially important because it tells Claude when the skill is relevant.

The basic workflow is:

**User request → Claude checks available skill descriptions → Matching skill is activated → Claude uses the skill**

For example, if you have a skill specifically for code reviews and ask Claude:

> "Review this PR."

Claude can recognize that the request matches the skill's description and load the relevant instructions.

### Where Skills Are Stored

Skills can be stored at different levels depending on who should use them.

#### Personal Skills

Personal skills live in:

```text
~/.claude/skills
```

These follow you across your projects.

They are useful for personal preferences such as:

- Commit message style
- Documentation format
- How you like code explained
- Personal coding preferences

#### Project Skills

Project skills live inside the repository:

```text
.claude/skills
```

These are shared with the project and can be committed to version control.

Anyone who clones the repository can then use the same skills.

Project skills are useful for team standards such as:

- Code review standards
- Brand guidelines
- Preferred fonts
- Color palettes
- Documentation conventions
- Team-specific workflows

### Skills vs. CLAUDE.md

Claude Code provides several ways to customize its behavior, but **skills are different because they are automatic and task-specific**.

A `CLAUDE.md` file is loaded into every conversation.

This makes `CLAUDE.md` appropriate for rules that should **always** apply.

For example:

> Always use TypeScript strict mode.

Skills work differently.

They are loaded **on demand when Claude determines that they are relevant**.

For example, a PR review checklist does not need to occupy context while you are debugging a bug.

Instead:

**Debugging → PR review skill stays unloaded**

**PR review → PR review skill becomes relevant and loads**

This makes skills more efficient for specialized instructions because they do not unnecessarily consume the main context window.

### Skills vs. Slash Commands

Slash commands require you to explicitly invoke them.

For example:

```text
/some-command
```

Skills do not require this.

Claude can recognize when a request matches a skill and **apply it automatically**.

The key difference is:

**Slash command → You explicitly invoke it**

**Skill → Claude recognizes when it is relevant**

### When Should You Create a Skill?

Skills work best for **specialized knowledge that applies to a specific type of task**.

Good examples include:

- Team code review standards
- Preferred commit message formats
- Documentation conventions
- Brand guidelines
- Design standards
- Organization-specific workflows

A useful rule is:

> **If you find yourself explaining the same thing to Claude repeatedly, it may be a skill waiting to be written.**

### Key Mental Model

Don't think of skills as general instructions that Claude always needs.

Think of them as:

> **"Task-specific knowledge that Claude can automatically load when the situation calls for it."**

This makes skills particularly useful for keeping specialized instructions out of the context window until they are actually needed.

### Recap

**Skills = Reusable + Task-specific + Automatically activated**

They allow Claude Code to remember **how to perform specialized tasks** without requiring you to repeat the same instructions every time.

The main distinction is:

**CLAUDE.md → Always loaded**

**Skills → Loaded when relevant**

**Slash commands → Manually invoked**

Skills are especially useful for repeated workflows such as code reviews, commit messages, documentation, and organizational standards.

---

### Video

[Skills - YouTube](https://www.youtube.com/watch?v=bjdBVZa66oU)

---

## Lesson 4 : MCP (Model Context Protocol)

---

### What is MCP?

**Model Context Protocol (MCP)** is an open standard that allows Claude Code to connect to **external tools and data sources**.

A lot of the context Claude needs may live outside the codebase:

- Databases
- Project management tools
- Productivity applications
- Public repositories
- External documentation
- Other developer tools

MCP provides a standardized way for Claude Code to access this external context.

The important idea is:

> **MCP connects Claude Code to external tools and data so it can take actions and gather information beyond the local codebase.**

### MCP and Tools

In agentic AI, **tools** give an agent the ability to perform actions rather than simply return text.

A traditional AI interaction might look like:

**Prompt → Text response**

An agent with tools can instead work like:

**Prompt → Reason → Use tool → Receive result → Continue**

For example:

- **Linear MCP** can allow Claude Code to access project and issue information.
- **Context7 MCP** can provide up-to-date documentation for dependencies.
- Other MCP connectors can connect Claude Code to different external services.

### MCP vs. API

MCP and APIs are related, but they solve different problems.

An **API** is a way for software to communicate with another software system.

**MCP** is a standardized protocol designed specifically for connecting AI models and agents to tools and data sources.

| | API | MCP |
|---|---|---|
| **Purpose** | Allows software to communicate with another service | Allows AI agents to discover and use external tools and data |
| **Designed for** | Applications and software systems | AI models and agents |
| **Interaction** | Application explicitly calls an endpoint | Agent can determine when a tool should be used |
| **Tool discovery** | Usually requires the developer to know the available endpoints | Tools can expose their capabilities to the agent |
| **Context** | Returns data requested by the application | Designed to provide models with the context and capabilities needed for a task |
| **Standardization** | Each API has its own interface and conventions | MCP provides a common protocol for connecting AI agents to tools |
| **Example** | Your application calls a GitHub API endpoint to retrieve a repository | Claude Code uses a GitHub MCP server to interact with GitHub through available tools |
| **Main mental model** | **Software → Service** | **AI Agent → Tool/Data Source** |

The key distinction is:

> **An API is an interface that software uses to communicate with a service. MCP is a standardized interface that allows AI agents to discover and use tools and external context.**

MCP servers can themselves communicate with underlying APIs or services. MCP therefore does **not necessarily replace APIs** — it provides an agent-friendly layer for interacting with external capabilities.

### Adding an MCP Server

You can add MCP servers with:

```bash
claude mcp add
```

There are two main types of MCP servers.

#### HTTP Servers

**HTTP servers** connect to remote services over the network.

The server is hosted remotely, usually by the service provider.

#### Stdio Servers

**Stdio servers** run as local processes on your machine.

They communicate with Claude Code through standard input and output.

### Managing MCP Servers

Inside a Claude Code session, use:

```text
/mcp
```

This allows you to:

- See which MCP servers are connected
- Check their status
- Disable servers you don't need

This is especially important because MCP servers have a cost in terms of context usage.

### Scoping MCP Servers

MCP servers can be configured at three different scopes.

#### Local

Available only in the **current project and only for you**.

#### User

Available across **all of your projects**.

#### Project

Configured through:

```text
.mcp.json
```

The `.mcp.json` file can be committed to version control.

This allows everyone working on the project to automatically receive the same MCP server configuration.

### MCP and Context Usage

One of the most important things to understand about MCP is that connected servers can consume **context window space even when you aren't actively using them**.

MCP servers provide tool definitions to Claude so that it knows what capabilities are available.

If you connect many servers, all of those tool definitions can consume part of your available context.

Therefore:

> **More connected MCP servers ≠ automatically better.**

If you aren't using a server, consider disabling it with:

```text
/mcp
```

### MCP vs. CLI Tools

If an MCP-connected service already has a CLI equivalent, the CLI can sometimes be more context-efficient.

For example:

- GitHub → `gh`
- AWS → `aws`

A CLI does not require Claude Code to keep a large collection of persistent MCP tool definitions in its context.

The general principle is:

> **Use the simplest tool that gives Claude the capability it needs without unnecessarily consuming context.**

### MCP vs. Skills

A **Skill** can sometimes be a better choice than MCP when the goal is primarily to provide specialized instructions or workflows.

Skills load their **name and description** first, allowing Claude to determine whether the skill is relevant before loading its full contents.

This can be more context-efficient than keeping many MCP tool definitions available.

A useful distinction is:

**MCP → Gives Claude access to external tools and data**

**Skill → Gives Claude specialized instructions for performing a task**

### Tool Search

If MCP tools consume more than **10% of the context window**, Claude Code can automatically switch to **tool search mode**.

Instead of keeping all tools immediately available in context, Claude can discover the tools it needs on demand.

This helps reduce context usage, although the video notes that on-demand discovery may be less reliable than having the relevant tools already available.

### Key Mental Model

Don't think of MCP as simply another API.

Think of it as:

> **"A standardized way for an AI agent to discover and interact with external tools and sources of context."**

The broader architecture can look like:

**Claude Code → MCP → External Tool / Service → Data or Action**

The external service might itself use an API internally.

### Recap

**MCP = Standardized connection between AI agents and external tools/data.**

It allows Claude Code to:

- Access external information
- Use third-party tools
- Interact with project management systems
- Retrieve current documentation
- Connect to remote or local services
- Perform actions outside the local codebase

The main concepts are:

**MCP → External tools and data**

**API → Software-to-service communication**

**Skill → Specialized task instructions**

**CLI → Direct command-line interaction**

MCP is powerful, but connected servers consume context. Keep only the servers you actually need active and use `/mcp` to manage them.

---

### Video

[MCP — YouTube](https://www.youtube.com/watch?v=kkBFmwkDzdo)

---

## Lesson 5 : Hooks

---

Hooks let you run commands at specific points in Claude Code's lifecycle. The key difference between hooks and prompts is that hooks are **deterministic** — they always run.

### Why Use Hooks?

You can tell Claude in `CLAUDE.md` to run Prettier after every file edit, but Claude may occasionally forget. A hook makes the behavior happen **every time, without exceptions**.

Common use cases:

- Auto-formatting after file edits
- Logging executed commands for compliance
- Blocking dangerous operations
- Preventing modifications to production files
- Sending notifications when Claude finishes a task

### How Hooks Work

Hooks are configured in `settings.json`. You choose:

1. An **event** — when the hook should run
2. An optional **matcher** — which tools the hook applies to
3. A **command** — what should actually execute

Common events:

- **`UserPromptSubmit`** — runs when you submit a prompt, before Claude processes it
- **`PreToolUse`** — runs before a tool call
- **`PostToolUse`** — runs after a tool call completes
- **`Notification`** — runs when Claude sends a notification
- **`Stop`** — runs when Claude finishes responding

You can configure hooks through `/hooks` inside Claude Code or directly in `settings.json`.

### Practical Example: Auto-Formatting

A common use case is automatically formatting files after Claude edits them.

Use a **PostToolUse** hook with a matcher such as:

```json
"Edit|MultiEdit|Write"
```

The hook can inspect the file extension and run the appropriate formatter:

- TypeScript/JavaScript → Prettier
- Go → `gofmt`
- Python → Ruff
- etc.

This guarantees formatting happens after Claude modifies a file.

### Blocking Dangerous Operations

**PreToolUse** hooks can block a tool call before it executes.

The hook receives the tool name and input as JSON through `stdin`.

#### Exit codes

- **Exit code `0`** → allow the action
- **Exit code `2`** → block the action
  - The `stderr` message is sent back to Claude as feedback so it understands why the action was blocked and can adjust.
- **Other non-zero codes** → report an error without necessarily blocking the action

This allows you to enforce rules that must be **guaranteed**, rather than merely suggested.

Examples:

- Block writes to production configuration
- Block `rm -rf` commands
- Block commits directly to `main`
- Prevent dangerous database operations

> **Rule of thumb:** If something must happen every time without fail, use a hook instead of a prompt.

### Project-Level Hooks

Hooks configured in:

```text
.claude/settings.json
```

are project-level and can be committed to version control.

This means the entire team gets the same hooks automatically.

Use the `CLAUDE_PROJECT_DIR` environment variable when referencing project scripts so they work regardless of Claude's current working directory.

### Hooks vs CLAUDE.md

| CLAUDE.md | Hooks |
|---|---|
| Gives Claude instructions | Executes commands deterministically |
| Claude can interpret and follow instructions | Commands always execute |
| Good for coding conventions and project context | Good for enforcement and automation |
| Claude may occasionally miss an instruction | Runs automatically at the configured lifecycle event |
| "Prefer Prettier" | "Run Prettier after every edit" |

#### Key distinction

**CLAUDE.md = tell Claude what to do.**

**Hooks = guarantee that something happens.**

### Recap

- Hooks provide **deterministic control** over Claude Code.
- Use **PostToolUse** for things like formatting and logging.
- Use **PreToolUse** to block dangerous operations.
- Configure hooks with `/hooks` or `settings.json`.
- Put project hooks in `.claude/settings.json` and commit them so the team shares the same rules.
- Use `CLAUDE_PROJECT_DIR` when referencing project scripts.
- If something needs to happen **every time without fail**, don't put it in a prompt — **put it in a hook**.

---

### Video

[Hooks — YouTube](https://www.youtube.com/watch?v=IkaPHiMDazM)

---