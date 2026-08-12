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

