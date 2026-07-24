# Git & GitHub Notes

---

## **RUN** git --help #for any details you need

## **RUN** git help git #for almost all details

## Objective

The purpose of these notes is to learn Git well enough to confidently use it in every software project.

By the end of learning Git, I should be able to:

- Track changes in my code.
- Save meaningful project snapshots.
- Upload projects to GitHub.
- Maintain a professional GitHub portfolio.
- Use Git comfortably inside VS Code.

These notes are a **quick reference**, not a complete Git textbook.

---

# Terminal Basics

## What is the Terminal?

The terminal is a text-based interface that allows me to communicate directly with my computer using commands.

As a developer, I use it to:

- Navigate folders
- Create files
- Run Python programs
- Execute Git commands

---

## Running the Terminal

**VS Code Shortcut**

```
Ctrl + `
```

---

## Command Syntax

```text
command argument
```

Example:

```bash
echo "Hello World!"
```

Output:

```text
Hello World!
```

---

## Important Notes

- The terminal is **case-sensitive**.
- Commands must be typed exactly.
- Press **Enter** to execute a command.

---

# Git Fundamentals

## What is Git?

Git is a **Version Control System (VCS)**.

Instead of saving multiple copies of a project like:

```
project
project_final
project_final_v2
project_final_REAL
```

Git stores every version inside one repository.

---

## What is Version Control?

Version Control records changes made to files over time.

It allows me to:

- View previous versions
- Undo mistakes
- Track progress
- Collaborate with others

Think of it as an **unlimited undo button** for an entire project.

---

# Git vs GitHub

| Git                      | GitHub                     |
| ------------------------ | -------------------------- |
| Version control software | Cloud hosting platform     |
| Runs on my computer      | Runs on the web            |
| Tracks project history   | Stores repositories online |

**Remember:**

> Git is the tool.
>
> GitHub is where my Git repositories are hosted.

---

# Core Concepts

---

> Make sure to run these when you initiall install git so git can recognise you and your github account

git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

---

## Repository (Repo)

A repository is a project that Git is tracking.

Example:

    ```
    quant-foundations/
    ├── .git/
    ├── README.md
    ├── kaggle/
    └── trading/
    ```

The hidden `.git` folder stores the entire history of the project.

---

## Commit

A commit is a **snapshot** of my project.

Every commit contains:

- The current state of my files
- A unique ID
- A commit message
- The date and time

Example:

    ```
    Initial commit

    ↓

    Added README

    ↓

    Completed Pandas Indexing

    ↓

    Fixed filtering examples
    ```

---

## Branch

A branch is an independent line of development.

The default branch is called:

```
main
```

Branches allow me to experiment without affecting the main project.

---

# My Daily Git Workflow

    ```
    Open VS Code
        ↓
    Write Python code
        ↓
    Run & test code
        ↓
    git status
        ↓
    git add .
        ↓
    git commit -m "Meaningful message"
        ↓
    git push
        ↓
    GitHub updates
    ```

---

# Essential Commands

## Check Repository Status

---

```bash
git status
```

Shows:

- Modified files
- New files
- Staged files

---

## Stage Changes

```bash
git add .
```

## Stages every changed file.

## Create a Commit

```bash
git commit -m "Describe the changes"
```

## Creates a new snapshot.

## View Commit History

```bash
git log --oneline
```

Displays a compact history of commits.
Example

    ```
    4615871 Initial commit
    ```

---

## Upload to GitHub

```bash
git push
```

## Uploads local commits to GitHub.

## Download Updates

```bash
git pull
```

Downloads changes from GitHub.

---

# VS Code Source Control

Everything can be done through the Source Control panel.

Instead of typing commands manually, I can:

- Stage files
- Commit changes
- Push to GitHub
- Pull updates

Git is still doing the work.

VS Code simply provides a graphical interface.

---

# Things to Remember

- Git is **not** a programming language.
- Git tracks project history.
- GitHub stores Git repositories online.
- Commit often.
- Write meaningful commit messages.
- Push regularly.

---

# Quick Cheat Sheet

```bash
git status
git add .
git commit -m "message"
git push
git pull
git log --oneline
```

---

# Configuration Level

Configuration Levels
Git has three configuration levels:

_Level Flag Location Scope_
System --system /etc/gitconfig All users on the system
Global --global ~/.gitconfig All repos for current user
Local --local .git/config Current repository only

Local settings override global, which override system.

---

# Essential Configuration Options

## Default Branch Name

    Set the default branch name for new repositories:

```bash
git config --global init.defaultBranch main
```

## Default Editor

    Set your preferred text editor for commit messages:

```bash
# VS CODE
git config --global core.editor "code --wait"
# Vim
git config --global core.editor "vim"
# Nano
git config --global core.editor "nano"
# Notepad++ (Windows)
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"
```

## Line Endings

    Configure how Git handles line endings across platforms:
    Windows         -> "When I download (check out) files from Git, convert them to Windows format (CRLF)."
    MacOS / Linux   -> "Don't change files when I open them. (keep them as LF)"

    History:
        Before computers, there were typewriters
            Old mechanical typewriters had two separate actions when you finished a line.

            Carriage Return (CR) → move the print head back to the left.
            Line Feed (LF) → move the paper up one line.
        ---
        Early computers copied this
            When operating systems were invented, they made different choices.
            Unix (which Linux and later macOS are based on) said:

            "One character is enough."

            So Unix used:
            LF

            Windows (through MS-DOS) kept the older convention:
            CRLF

            because it inherited behavior from older systems.
        ---
        Why not change Windows now?
            Imagine Microsoft said:

            "Starting tomorrow every text file uses LF."

            Millions of things could break:

            old programs
            scripts
            editors
            enterprise software
            legacy applications

            Some software written 20 or 30 years ago still expects CRLF.
            Changing it would risk breaking countless existing systems.

Git's solution
Git says:

"I don't care what operating system you're using."

Internally, Git prefers LF.
Then, depending on your settings:
Windows users see CRLF in their working copy (if configured that way).
Linux/macOS users see LF.
Everyone commits the same normalized content.

```bash
# Windows: Convert LF to CRLF when checking out
git config --global core.autocrlf true

# Mac/Linux: Convert CRLF to LF when committing
git config --global core.autocrlf input
```

## Colorful Outputs

    Enable colored output (usually enabled by default):

```bash
git config --global color.ui auto
```

## Useful Alias

    Aliases create shortcuts for common commands:

```bash
# Short status
git config --global alias.st status

# Short commit
git config --global alias.co checkout

# Pretty log
git config --global alias.lg "log --oneline --graph --decorate"

# Amend last commit
git config --global alias.amend "commit --amend --no-edit"

    Now you can use:

git st        # instead of git status
git co main   # instead of git checkout main
git lg        # pretty one-line log with graph
```

---

# SSH vs HTTPS Authentication

    what are we trying to do?
    This section is about SSH authentication.
    Normally, when you push to GitHub:
    git push
    github asks
    "Who are you? Prove it"
    You can prove it with
        * HTTPS + Login / Token
        * SSH Key

    NOTE: SSH basically means "my computer has a secret key, Github has the matching public key. if they match, allow access"~

## HTTPS

    * Easier to set up
    * Works through firewalls
    * Requires entering credntials (or using a crendtial manager)

## SSH (recommended)

    * More Secure
    * No password prompts after setup
    * Requries generating SSH Keys

    ```bash
    # Generate a new SSH key
    ssh-keygen -t ed25519 -C "your.email@example.com"
        # ssh-keygen = ssh key generator
        # -t = type - "You are specifying what type of key to create."
        # ed25519 = is the key type
            # -t ed25519 = create an SSH key using the Ed25519 algorithm
        # -C = comment - "It adds a label to the key."
            # -C "your.email@example.com" = Attach this email address as label

        # Altogether it becomes "Run ssh-keygen. Create an Ed25519 key. Attach this email as a label."

    # Start the SSH agent
    eval "$(ssh-agent -s)"
        # ssh-agent -s = Runs the SSH agent, The SSH agent is a background program that remembers your private key.
        # $() = Runs this command first and insert the output here
        # eval = execute the text that was written

        # Altogether it becomes "Start SSH agent and apply the environment variables it gives me."

    # Add your key to the agent
    ssh-add ~/.ssh/id_ed25519
        # ssh-add = Add an SSH key to the SSH agent
        # ~ = Home Directory - On windows its "C:\User\YourName"
        # .ssh = is the hidden folder
            # .ssh/
                ├── id_ed25519      # private key, for the computer
                └── id_ed25519.pub  # public key, this goes to github

    # Copy your public key
    cat ~/.ssh/id_ed25519.pub
        # cat = display the contents of the file

    # Add this to your GitHub account settings
    ```
