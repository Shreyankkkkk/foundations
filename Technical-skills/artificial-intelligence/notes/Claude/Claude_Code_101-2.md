# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Your First Prompt

---

## Lesson 1 : Installing Claude Code

---

### Installing Claude Code

Claude Code can be installed and used across several environments:

- Terminal
- Visual Studio Code
- JetBrains IDEs
- Claude Desktop
- Web

The experience is broadly similar across environments, but each option has different advantages.

#### Terminal

The **terminal is the best option for staying up to date**, because new Claude Code features generally arrive there first.

#### macOS, Linux, and WSL

Use the provided `curl` command to install Claude Code in one step.

Alternatively, Claude Code can be installed through Homebrew:

```bash
brew install
```

**Important:** The Homebrew installation method does not support automatic updates.

#### Windows

There are several installation options:

- **PowerShell:** `Invoke-RestMethod`
- **CMD:** `curl`
- **WinGet:** `winget`

Like Homebrew, the WinGet installation method does not support automatic updates.

#### Starting Claude Code

After installation, navigate to your project directory and run:

```bash
claude
```

If the command is not recognized, restart the terminal and try again.

#### Initial Setup

When Claude Code is launched for the first time, it will guide you through initial setup, including:

- Choosing a color theme
- Signing in
- Selecting an authentication method

You can authenticate using:

- Claude Pro
- Claude Max
- Claude Enterprise
- An API key

If your organization uses Claude Enterprise, select the Enterprise option.

#### Directory Access

The directory from which Claude Code is launched determines what local files it can access.

> Claude Code can access the directory in which it is launched and all of its subdirectories.

This makes it important to be aware of **which directory you launch Claude Code from**.

---

### Visual Studio Code

Claude Code can be integrated directly into VS Code.

#### Installation

1. Open the **Extensions** panel.
2. Search for **Claude Code**.
3. Find the extension published by **Anthropic**.
4. Make sure it has the blue verification check.
5. Install the extension.
6. Restart VS Code if necessary.

#### Opening Claude Code

Open the Command Palette:

```text
Ctrl/Cmd + Shift + P
```

Then search for:

```text
Claude Code: Open in New Tab
```

You can also click the Claude logo if it appears in the VS Code sidebar.

#### Experience

The VS Code extension provides a very similar experience to the terminal version.

You can also opt out of the integrated UI and use the terminal experience directly through the settings.

---

### JetBrains

Claude Code can also be integrated into JetBrains IDEs.

#### Installation

1. Open the **JetBrains Marketplace**.
2. Search for the Claude Code plugin.
3. Install it.
4. Restart the IDE.

After restarting, the Claude logo will appear.

Clicking it opens a pane containing the Claude Code terminal experience alongside the editor.

---

### Claude Desktop

Claude Code is also available inside **Claude Desktop**.

After installing and signing into Claude Desktop, a **Code** toggle appears at the top.

Claude Desktop's Code mode provides a similar experience to Claude's normal chat interface while allowing you to:

- Work within a specific folder
- Change permissions
- Work in a cloud environment

#### Main Advantage

Desktop is useful when you want Claude Code to **run in the background while you work on other tasks**.

---

### Web

Claude Code can also be accessed through the web:

`claude.ai/code`

You can also access it by clicking **Code** in the sidebar of the Claude web application.

The web experience is similar to the Desktop version.

#### Important Limitation

Claude Code on the web is restricted to **GitHub repositories**.

#### Main Advantages

The web version is useful for:

- Remote work through GitHub repositories
- Working on projects without being at your local development environment
- Running multiple Claude Code sessions in parallel

---

### Which Claude Code Environment Should I Use?

| Environment | Best Use |
|---|---|
| **Terminal** | Staying up to date with the latest features |
| **VS Code** | Claude Code integrated directly into VS Code |
| **JetBrains** | Claude Code integrated into JetBrains IDEs |
| **Desktop** | Background work while doing other tasks |
| **Web** | Remote GitHub work and parallel sessions |

#### Terminal

The **terminal is the best choice for staying fully up to date** because new features generally arrive there first.

#### IDE Integrations

VS Code and JetBrains provide a very similar Claude Code experience while making Claude feel more integrated with the code editor.

#### Desktop

Desktop is useful when you want Claude to work in the background while you focus on other tasks.

#### Web

The web version is useful for remotely working on projects through GitHub repositories and running multiple sessions in parallel.

---

### Practical Mental Model

Claude Code is fundamentally the same agentic coding system regardless of the interface.

The main difference is **where and how you interact with it**:

```text
                         Claude Code
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
         Terminal            IDE          Desktop / Web
            │                 │                 │
       Latest features    Editor-based      Remote /
       & direct access      workflow        background
```

The choice of environment depends mainly on your preferred workflow rather than one environment being universally superior.

---

### Key Takeaways

- Claude Code can be used through the **terminal, VS Code, JetBrains, Claude Desktop, or the web**.
- The **terminal is the best option for staying up to date** because features generally ship there first.
- VS Code and JetBrains provide closely integrated IDE experiences.
- Claude Desktop is useful for **background work**.
- Claude Code on the web is useful for **remote GitHub work and parallel sessions**.
- Homebrew and WinGet installations do **not** support automatic updates.
- The directory from which Claude Code is launched determines which local files and subdirectories it can access.
- Claude Code can be authenticated using a supported Claude account or an API key.
- The best environment depends on the workflow and development setup.

---

### Video

[Installing Claude Code — YouTube](https://www.youtube.com/watch?v=0kILa02vKuI&t)

---

### Recap

**Terminal → latest features**

**IDE → integrated coding workflow**

**Desktop → background work**

**Web → remote GitHub + parallel sessions**

**Important safety concept → always be aware of the directory and permissions Claude Code has access to.**

---

## Lesson 2 : Your First Prompt

---

### Your First Prompt

---

#### Talking to Claude Code

You interact with Claude Code much like you would with any other AI assistant, but because Claude Code can take actions inside your development environment, **how you prompt it and how much control you give it both matter**.

When starting a task, you can choose how much oversight you want over Claude's actions.

#### Auto-Accept vs. Approval

Claude Code provides different permission modes that let you control whether Claude can make changes automatically or needs your approval.

You can press `Shift + Tab` to cycle between the available modes.

##### Approval mode

Claude asks for your explicit permission before:

- Editing or creating files
- Running commands

This gives you more direct control over what Claude does.

##### Auto-accept mode

Claude automatically approves file edits and file creation, but still asks for permission before running commands.

There is no universally correct mode. The right choice depends on **how much control and oversight you want while Claude is working**.

#### Plan Mode

**Plan Mode** is another option available through the `Shift + Tab` menu.

Instead of immediately making changes, Claude uses **read-only tools** to investigate the codebase and understand how the requested change could be implemented.

During this process, Claude can:

- Analyze the existing codebase
- Research the suggested implementation
- Ask clarifying questions
- Identify relevant files and existing patterns
- Develop a detailed implementation plan

Once the investigation is complete, Claude provides a plan that can then be executed.

Plan Mode is particularly useful for:

- Complex changes
- Multi-step feature implementations
- Understanding an unfamiliar codebase
- Safe code reviews
- Tasks where you want to review the approach before changes are made

A useful workflow is:

**Prompt → Investigate → Ask clarifying questions → Create plan → Review plan → Execute**

This gives you an opportunity to catch problems in the proposed approach **before Claude starts modifying the project**.

#### Example: Adding a Dark Mode Toggle

Suppose an application needs a dark mode feature.

Instead of immediately asking Claude to modify the code, you can:

1. Open the root directory of the project.
2. Run `claude`.
3. Press `Shift + Tab` until Plan Mode is selected.
4. Give Claude a descriptive prompt explaining the desired outcome.
5. Let Claude investigate the existing application.
6. Review the proposed implementation plan.
7. Approve the plan if it looks appropriate.
8. Let Claude execute the implementation while maintaining the desired level of permission control.

For example:

> My app needs a dark mode implemented across the entire app. Can you create a toggle switch on the header that allows a user to toggle between light mode and dark mode? I need you to find a good contrast color that works based on my existing light theme.

The important part is that the prompt describes the **desired outcome and relevant requirements**, rather than prescribing every individual coding step.

Claude can then investigate the existing application and determine how the feature should fit into the current architecture and design.

#### Prompting Principle

When working with Claude Code, **be as descriptive as possible about what you want to achieve**.

You don't necessarily need to tell Claude exactly how to implement the solution.

Instead, provide enough context about:

- The desired outcome
- Important requirements
- Existing behavior that should be preserved
- Constraints or preferences
- What the final result should look like

Claude can then use the codebase and available tools to determine an appropriate implementation.

#### Staying in the Loop

You can choose how involved you want to be while Claude works.

If you want more control, use approval-based permissions and review actions as Claude performs them.

If you are comfortable with Claude making file changes automatically, auto-accept mode can reduce interruptions while still requiring approval for commands.

For more complex work, **Plan Mode provides an additional safety and reasoning step before execution**.

The goal is not to always maximize or minimize autonomy. Instead, choose the level of oversight that makes sense for the task and its potential consequences.

#### Key Mental Model

Don't think of prompting Claude Code as:

> **"Tell Claude exactly which files to edit and which code to write."**

A better approach is:

> **"Clearly describe the outcome I want, provide the necessary context and constraints, and let Claude investigate the codebase and determine an implementation."**

For complex tasks, add:

> **Plan first → review → execute**

This makes it easier to catch misunderstandings before they become changes in the codebase.

#### Recap

When using Claude Code:

- **Be descriptive** about the outcome you want.
- Choose between **Approval Mode** and **Auto-Accept Mode** based on how much oversight you want.
- Use **Plan Mode** for complex changes, multi-step implementations, and safe code reviews.
- Let Claude investigate the codebase before making complex changes.
- **Review the plan before execution** when the task is consequential.
- Stay involved when you want visibility into Claude's actions and decisions.

**Good prompting + appropriate permissions + planning = more controlled agentic development.**

---

#### Video

[Your First Claude Code Prompt](https://www.youtube.com/watch?v=gbetp6D7J_Q)

---

