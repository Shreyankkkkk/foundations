# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Daily Workflows

---

## Lesson 1 : The explore -> plan -> code -> commit workflow

---

### The Explore → Plan → Code → Commit Workflow

---

#### The Core Workflow

One of the most important workflows for using Claude Code effectively is:

**Explore → Plan → Code → Commit**

The main idea is to **avoid immediately asking Claude to start writing code**.

Instead, first give Claude the opportunity to understand the codebase and build a framework for how the task should be implemented.

This reduces unnecessary course-correcting later because problems can be identified **before code is written**.

The workflow can be thought of as:

**Understand the project → Build the implementation plan → Execute the code → Review and commit**

---

### Explore and Plan

The fastest way to combine exploration and planning is through **Plan Mode**.

In Plan Mode, Claude uses **read-only tools** to investigate the project without modifying files.

To enter Plan Mode, press `Shift + Tab` until **Plan Mode** appears under the text input.

You can then give Claude a high-level implementation request.

For example:

```text
I need to add WebP conversion to our image upload pipeline. Figure out where in the pipeline it should happen, whether we need new dependencies, and how to approach it.
```

Claude can then:

- Read the relevant files
- Explore the existing architecture
- Search for relevant documentation
- Determine where the change should happen
- Identify dependencies that may be required
- Develop an implementation plan

The result is a **plan of action** that you can review before any code is changed.

#### Why planning first matters

Plan Mode is the best place to **course-correct**.

If Claude misunderstands the requirements or proposes an approach you don't like, you can ask it to revise the plan before any implementation happens.

This is much easier than discovering the problem after Claude has already modified multiple files.

You can also ask Claude to **explore the codebase without Plan Mode** when you simply want to understand the project and don't intend to immediately implement a change.

#### The planning workflow

**Prompt → Explore codebase → Research → Create plan → Review → Revise if necessary → Approve**

The goal is to create a strong framework for the implementation before Claude begins coding.

---

### Code

Once the plan looks good, you can **approve the plan** and let Claude begin executing it.

Claude will work through the tasks in the plan and attempt to troubleshoot problems along the way.

You can choose how much control Claude has over the implementation:

- **Approval-based workflow** — Claude asks for permission before making changes or performing certain actions.
- **Auto-accept workflow** — Claude can automatically make file changes while still requiring permission for commands where appropriate.

This gives you a choice between **verification and direct manipulation** depending on how much oversight you want.

A useful mental model is:

**Plan first → approve → Claude implements → verify → course-correct → repeat**

Even after approving the plan, you may still need to guide Claude when unexpected problems appear.

The advantage of Plan Mode is that Claude already has the context of **why the implementation was designed the way it was**, which can help it make better decisions during execution.

---

#### Define Success Criteria

Claude needs to know what **"correct"** means.

When creating your plan or writing your prompt, make the success criteria explicit.

For example, don't only say:

> "Implement WebP conversion."

Instead, clarify what the finished implementation should accomplish and how you will determine that it works.

Clear success criteria give Claude something concrete to validate against.

**Clear requirements → clear definition of success → easier verification**

---

#### Give Claude the Right Tools

Providing Claude with tools that help it verify its work can significantly reduce back-and-forth.

For example, when building web interfaces, Claude can use the **Claude in Chrome extension** to interact with a browser and test the UI directly.

The general principle is:

> **Give Claude the tools it needs to verify the outcome itself.**

The more effectively Claude can inspect and test its work, the less manual intervention is required.

---

#### Use Tests as a Source of Truth

A reliable test suite gives Claude something concrete to continuously validate against.

Claude can:

- Run existing tests
- Investigate test failures
- Use test results to determine whether the implementation is working
- Write additional tests when necessary

However, the tests themselves need to be trustworthy.

Before relying on a test suite as the source of truth, make sure it actually validates the intended behavior and does not produce misleading **false positives**.

The principle is:

**Implementation → Tests → Results → Verification**

---

#### Save Solutions to `CLAUDE.md`

If Claude repeatedly encounters the same problem, you can ask it to save the solution or relevant guidance in `CLAUDE.md`.

This allows useful project-specific knowledge to persist and helps prevent Claude from repeatedly making the same mistake in future sessions.

A simple mental model is:

**Problem discovered → Solution established → Save guidance → Future sessions can use it**

---

### Commit

Once Claude has completed the implementation, **test the changes yourself** and make sure you are satisfied with the result.

Before committing, it is useful to run a **subagent code reviewer**.

A separate reviewer provides a fresh perspective on the changes because it does not carry the same assumptions or context as the main agent that implemented the code.

This creates another verification layer:

**Claude implements → Tests → Human review → Subagent review → Commit**

#### Working with a Team

When working on a shared project, the final step will typically involve creating a **pull request (PR)** rather than directly pushing changes into the main branch.

The general team workflow becomes:

**Explore → Plan → Code → Review → Pull Request → Merge**

The PR provides an opportunity for other developers to review the changes before they become part of the main branch.

After the work has been reviewed and you're ready to commit, Claude can also generate a **commit message in your preferred style**.

---

### The Complete Workflow

The complete Claude Code workflow can be summarized as:

#### 1. Explore

Understand the existing codebase and gather the relevant context.

**Goal:** Understand what already exists and where the change belongs.

#### 2. Plan

Use Plan Mode to create an implementation framework.

**Goal:** Decide how the change should be implemented before modifying code.

#### 3. Code

Approve the plan and let Claude execute the implementation.

**Goal:** Turn the plan into working code while allowing for verification and course-correction.

#### 4. Verify

Run tests, inspect the results, review the implementation, and correct any problems.

**Goal:** Establish that the implementation actually satisfies the requirements.

#### 5. Commit

Review the final changes and commit them.

For team projects, create a **pull request** so the changes can be reviewed before being merged into the main branch.

**Goal:** Safely integrate the completed work into the project.

---

#### Key Mental Model

Don't think of Claude Code as:

> **"Give Claude a prompt and let it immediately write the code."**

Instead, think:

> **"First build the framework for the solution, then let Claude execute it, verify the result, and finally review and integrate the changes."**

The most important shift is:

**Don't start with code. Start with understanding and planning.**

Then:

**Plan → Code → Verify → Review → Commit/PR**

---

#### Recap

The core Claude Code workflow is:

**Explore → Plan → Code → Commit**

- **Explore** gives Claude the relevant context about the project.
- **Plan** creates the framework for how the task should be implemented.
- **Code** turns the approved plan into an actual implementation.
- **Verify** uses tests, tools, Claude's own investigation, and human review to ensure the result is correct.
- **Commit** integrates the completed work into the project.
- **Pull Requests** provide the appropriate review and integration workflow when working with a team.

The key principle is:

> **Start with Plan Mode and build the framework for the code. Then let Claude implement the plan, choose the appropriate level of verification or autonomy, review the result, and create a PR when working with a team.**

**Explore → Plan → Code → Verify → Commit/PR**

---

#### Video

[The explore, Plan, Code, Commit — YouTube](https://www.youtube.com/watch?v=GJ5jTgcbRHA)

---

## Lesson 2 : Context Management

---

### Context Management

---

#### Context Management

Context is Claude's **working memory**. Every file it reads, every command it runs, every message you send, and every tool result it receives takes up space in the context window.

The context window is finite, so understanding how to manage it is important for keeping Claude Code effective during longer tasks.

#### What is the Context Window?

The **context window** is the amount of information Claude can hold and reference at one time.

It can include:

- Your prompts and conversation history
- Files Claude has read
- Tool calls
- Tool call results
- Command output
- Other information gathered during the task

Because the context window is finite, inefficient use of context can make longer agentic tasks more difficult.

#### What Happens When Context Fills Up

When Claude approaches the context limit, Claude Code can automatically **compact** the conversation.

Compaction:

- Summarizes important information
- Removes unnecessary tool call results
- Frees space in the context window
- Preserves the important context needed to continue working

However, compaction can potentially **lose some details** from the earlier conversation.

#### Context Commands

##### `/compact`

The `/compact` command manually compacts the current conversation.

It is useful when:

- You are continuing work on the same feature
- The context is becoming too large
- You want to free up context space while preserving a summary of the previous work

The key idea is:

> **Compact when you want to continue the same task but need more context space.**

##### `/clear`

The `/clear` command completely clears the current conversation context.

It is useful when:

- You have finished one feature
- You want to start a completely new task
- You don't want previous conversation context to influence the new task

The key idea is:

> **Clear when you want a fresh start.**

For information Claude should remember across different sessions, put that information in your `CLAUDE.md` file instead of relying on the current conversation.

##### `/context`

The `/context` command shows the current state of your context window.

It provides:

- An overview of the context size
- The categories consuming the most context
- A visual breakdown of context usage

This helps you understand what is taking up space and decide whether you need to compact or change your workflow.

#### When to Use Which

A useful rule of thumb is:

| Situation | Action |
|---|---|
| Continuing the same feature but running out of context | `/compact` |
| Starting a completely new feature | `/clear` |
| Want to inspect what is consuming context | `/context` |
| Want Claude to remember information across sessions | `CLAUDE.md` |

The distinction is important because **compacting preserves useful context**, while **clearing intentionally removes the previous context**.

#### Tips for Saving Context Space

##### 1. Be Specific

Being more specific in your prompts can actually **save context**.

A vague prompt may seem shorter, but it can force Claude to:

- Explore more of the codebase
- Search through more files
- Perform additional reasoning
- Gather unnecessary information

A clear prompt gives Claude more direction and can reduce the amount of exploration required.

The key idea is:

> **A slightly longer and more precise prompt can use less context overall than a vague prompt.**

##### 2. Manage MCP Servers

MCP servers can make additional tools available to Claude.

However, their available tools can be loaded into the context even when you aren't actively using them.

If you have MCP servers configured for things unrelated to the current project, consider **turning them off** when they aren't needed.

This can reduce unnecessary context usage.

##### 3. Use Skills

Skills can provide functionality similar to MCP servers while avoiding the need to load everything into the context upfront.

This can help provide Claude with additional capabilities while using context more efficiently.

##### 4. Use Subagents

Subagents run alongside the main agent but have a **separate context window**.

This makes them useful when you only need the result of a task rather than the entire process used to reach that result.

For example, instead of having the main agent investigate:

> "Where are the authentication endpoints located?"

you can delegate that investigation to a subagent.

The subagent can explore the codebase and return a summary such as:

> "The authentication endpoints are located in these files..."

The main agent receives the useful result without filling its own context with the entire exploration process.

This makes subagents especially useful for **research, exploration, and delegated tasks**.

#### The Key Mental Model

Think of context as Claude's **limited working memory**.

Everything Claude sees and does during a session can consume part of that memory:

**Prompt → Files → Tool calls → Results → More reasoning → More context**

Therefore, effective Claude Code usage isn't just about giving Claude good instructions. It is also about **managing what information enters and remains in the context window**.

#### Practical Workflow

A useful context-management workflow is:

**Start task → Work → Monitor context → Compact if continuing → Clear when starting fresh**

For information that should persist beyond the current session:

**Save it in `CLAUDE.md`**

For tasks where you only need the result:

**Delegate to a subagent**

#### Recap

**Context = Claude's working memory.**

The main tools for managing it are:

- **`/compact`** — summarize the current session and free context space
- **`/clear`** — completely reset the current conversation
- **`/context`** — inspect current context usage
- **`CLAUDE.md`** — store information Claude should remember across sessions
- **Subagents** — delegate tasks to separate context windows

The most important principle is:

> **Manage context intentionally so Claude has the information it needs without filling its working memory with unnecessary information.**

Be specific in your prompts, disable unnecessary MCP servers, use skills where appropriate, and delegate research tasks to subagents when you only need the final result.

---

#### Video

[Context Management - YouTube](https://www.youtube.com/watch?v=eW3oTyfeWZ0)

---

