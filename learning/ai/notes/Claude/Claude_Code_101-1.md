# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# What is Claude Code?

---

## Lesson 1 : What is Claude Code?

---

### What is Claude Code?

Claude Code is an **agentic coding tool** that can work directly with a codebase rather than simply generating code for you to copy and paste.

It can:

- Read and understand your codebase
- Edit files directly
- Run terminal commands
- Execute build scripts and tests
- Install packages
- Use command output to determine its next steps
- Search the web for current technical documentation
- Work with other developer tools and services

Claude Code is available in the **terminal, VS Code, Claude Desktop, the web, and JetBrains IDEs**. This lesson focuses on using it through the terminal.

### Claude vs. Claude Code

The main difference is **direct access to the development environment**.

With regular Claude, you might paste code into the conversation, receive a response, and manually apply the changes.

Claude Code can instead work directly inside the project:

> **Read → understand → modify → run → inspect results → continue**

This is what makes Claude Code an **agent** rather than simply a coding chatbot.

### What does "agentic" mean?

An **AI agent** is software that interacts with its environment and takes actions toward a defined goal.

A simple way to think about Claude Code is:

**Goal → reason → use tools → observe results → decide next action → repeat**

Its tools and environment can include:

- Your files
- Terminal commands
- Development tools
- Tests and build systems
- External services
- Web documentation
- Potentially other AI agents

This allows Claude Code to work through multi-step development tasks rather than stopping after generating a single piece of code.

### What Claude Code can actually do

Claude Code can work across an entire codebase rather than only looking at one file.

For example, you can ask it to:

- Explain how a feature works across multiple files
- Trace a bug through the codebase
- Implement a feature
- Run the project's tests
- Investigate test failures
- Install required packages
- Run build scripts
- Use the results of commands to determine what to do next
- Look up current API documentation when needed

This means you can give Claude a **goal**, rather than manually directing every individual coding step.

### Core concepts

#### 1. Context window

The context window is essentially Claude's **working memory**.

It can hold a large amount of information, but it is still finite. Claude Code therefore doesn't need to load your entire codebase into its context at once.

Instead, its agentic behavior allows it to **strategically explore the codebase**:

- Find relevant files
- Read the necessary sections
- Follow references
- Investigate related code
- Gather only the context needed for the current task

This is important for large projects because blindly putting an entire repository into context would be inefficient and eventually exceed the available context.

#### 2. Permissions

Claude Code does not simply have unlimited authority over your environment.

By default, it can ask for permission before:

- Running commands
- Modifying files
- Performing other potentially consequential actions

This keeps the user in control.

You can choose to be more hands-on and approve actions individually, or allow Claude to work more autonomously where appropriate.

#### 3. Claude Code can make mistakes

Claude Code is powerful, but it is **not infallible**.

It can:

- Misunderstand your requirements
- Introduce bugs
- Modify the wrong thing
- Make incorrect assumptions
- Over-engineer a solution
- Produce a technically working but unnecessarily complicated implementation

Therefore, being able to **review, test, and verify its work** remains important.

The fact that Claude Code can execute actions makes verification especially important: a mistake isn't necessarily confined to an answer in the chat—it can affect the actual project.

### The key mental model

Don't think of Claude Code as:

> **"An AI that writes code for me."**

A better mental model is:

> **"An AI agent that can operate inside my development environment to accomplish coding tasks."**

That distinction matters because Claude Code can go beyond generating code.

It can **inspect the environment, take actions, observe the results, and adapt its next action**.

#### Quick recap

**Claude Code = agentic coding inside your development environment.**

It can:

**Understand code → edit files → run commands → inspect results → iterate**

Its biggest advantages are direct codebase access, tool use, and the ability to work through multi-step development workflows.

Its biggest limitations are the finite context window, the possibility of mistakes, and the need for appropriate permissions and human verification.

---

### Video

[Delegation Diligence Loop — YouTube](https://www.youtube.com/watch?v=VojDzHaciKQ&t)

---

## Lesson 2 : How Claude Code Works

---

### How Claude Code Works

Claude Code is different from typical chat applications. Understanding how it works under the hood will help you use it more effectively.

#### The Agentic Loop

Claude Code is best explained through the **agentic loop**:

1. You enter a prompt into Claude Code.
2. Claude gathers the context it needs by interacting with the model, which returns text or a tool call that Claude Code can execute.
3. It takes action — for example, editing a file or running a command.
4. It verifies the results and determines whether they achieve what your prompt set out to do.
5. If they do, Claude finishes and waits for the next prompt. If they don't, it loops back and tries again until the results are complete and verifiable.

Throughout this loop, you can add context, interrupt, or steer the model to help guide it toward your goal.

### The basic mental model

**Prompt → Gather context → Use tools → Take action → Verify → Repeat if necessary**

This is what allows Claude Code to work toward a goal rather than simply producing a single response.

### Context

Claude has a **context window** that determines how much of your conversation, file contents, command outputs, and other information it can store and reference.

Once the context window gets close to its limit, Claude Code can **compact the conversation**. It determines what information can be removed or summarized so that the context is brought back down to a usable size while preserving important information.

This allows longer agentic tasks to continue without requiring the entire conversation and every piece of previously gathered information to remain in the active context.

### Tools

**Tools are the backbone of how agents work.**

Most basic AI assistants follow:

**Text input → Text output**

Agents add another layer:

**Text → Reasoning → Tool call → Result → Reasoning → Next action**

Tools allow Claude Code to interact with its environment instead of only talking about what should be done.

Examples include:

- Reading files
- Searching the codebase
- Editing files
- Running shell commands
- Executing code
- Running tests
- Searching the web
- Accessing other developer tools

Claude Code uses its understanding of the task and available context to determine **when a tool is useful and which tool to call**.

### Permissions

Claude Code has configurable permission modes that determine how much control it has over actions.

#### Default mode

Claude asks for explicit permission before:

- Editing files
- Running shell commands

This provides the most direct human oversight.

#### Auto-accept edits

Claude can edit files without asking for approval each time, but still asks before running commands.

This is useful when you trust Claude to make file changes but still want control over command execution.

#### Plan mode

Plan mode uses **read-only tools** to investigate the project and create a plan before actually making changes.

This is useful for complex tasks where you want Claude to understand the codebase and propose an approach before execution begins.

#### Permission safety

Skipping permissions should be done carefully.

Giving Claude unrestricted ability to run commands means a mistake could have consequences **before you have an opportunity to catch it**.

A good principle is:

> **The more consequential the action, the more oversight you should maintain.**

### Why Claude Code differs from a normal chat

Claude Code combines several concepts directly inside the development environment:

- **Agentic loop** — continuously works toward a goal
- **Context management** — gathers and manages the information needed for the task
- **Tools** — interacts with files, commands, code, and external resources
- **Permissions** — lets you control what actions Claude is allowed to take
- **Verification** — checks whether its actions actually produced the desired result

Because Claude Code can **read your codebase, take actions, observe the results, and adapt**, it is fundamentally different from a standard chat interface.

### Key Mental Model

Don't think of Claude Code as:

> **"A chatbot that writes code."**

Think of it as:

> **"An agent operating inside my development environment toward a defined goal."**

The important shift is from asking:

> "What code should I write?"

to:

> "What outcome do I want Claude Code to accomplish, and what context and permissions does it need to get there?"

### Recap

**Claude Code = Agentic Loop + Context + Tools + Permissions + Verification**

Its workflow can be summarized as:

**Prompt → Context → Tools → Action → Verification → Repeat**

The agent keeps working until it determines that the task is complete, while you can provide additional context, interrupt it, or adjust its direction throughout the process.

---

### Video

[https://www.youtube.com/watch?v=6bs5b4FltCU](https://www.youtube.com/watch?v=6bs5b4FltCU)