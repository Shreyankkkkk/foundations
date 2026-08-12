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

