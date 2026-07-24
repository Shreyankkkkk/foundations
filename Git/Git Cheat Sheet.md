# Git & GitHub Cheat Sheet

---

# Terminal Navigation

## `pwd`

Show current directory.

```bash
pwd
```

---

## `dir`

List files and folders.

```bash
dir
```

---

## `dir -Force`

Show all files including hidden files.

```bash
dir -Force
```

---

## `cd folder-name`

Enter a folder.

```bash
cd folder-name
```

---

## `cd ..`

Move back one folder.

```bash
cd ..
```

---

## `clear`

Clear terminal.

```bash
clear
```

---

# Git Setup

## Check Git Version

```bash
git --version
```

Check installed Git version.

---

## View Git Configuration

```bash
git config --list
```

Show Git configuration.

---

## Set Git Username

```bash
git config --global user.name "Name"
```

Set Git username.

---

## Set Git Email

```bash
git config --global user.email "email"
```

Set Git email.

---

## Set Default Branch

```bash
git config --global init.defaultBranch main
```

Set default branch name.

---

# Repository Commands

## Create Repository

```bash
git init
```

Create a new Git repository.

---

## Clone Repository

```bash
git clone URL
```

Download a GitHub repository.

---

## Check Status

```bash
git status
```

Show repository changes.

---

## Show All Untracked Files

```bash
git status --untracked-files=all
```

Show all untracked files.

---

# Staging & Commits

## Stage All Changes

```bash
git add .
```

Stage all changed files.

---

## Stage Specific File

```bash
git add filename
```

Stage a specific file.

---

## Create Commit

```bash
git commit -m "message"
```

Create a commit with a description.

---

## View Commit History

```bash
git log --oneline
```

Show commit history.

---

# GitHub Synchronization

## Upload Changes

```bash
git push
```

Upload commits to GitHub.

---

## Download Changes

```bash
git pull
```

Download changes from GitHub.

---

# Undo Changes

## Discard File Changes

```bash
git restore filename
```

Restore a file to its last committed state.

---

## Remove From Staging

```bash
git restore --staged filename
```

Remove file from staging area.

---

# Branches

## List Branches

```bash
git branch
```

Show existing branches.

---

## Create Branch

```bash
git branch branch-name
```

Create a new branch.

---

## Switch Branch

```bash
git checkout branch-name
```

Switch to another branch.

---

## Merge Branch

```bash
git merge branch-name
```

Merge another branch into the current branch.

---

# SSH Authentication

## Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "email"
```

Create an SSH key pair.

---

## Start SSH Agent

```bash
eval "$(ssh-agent -s)"
```

Start SSH authentication agent.

---

## Add SSH Key

```bash
ssh-add ~/.ssh/id_ed25519
```

Add private key to SSH agent.

---

## Display Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Display public SSH key.

---

# Useful Commands

## View Unstaged Changes

```bash
git diff
```

Show changes not yet staged.

---

## View Staged Changes

```bash
git diff --staged
```

Show changes ready for commit.

---

## View Remote Repository

```bash
git remote -v
```

Show connected GitHub repository.

---

## Rename Current Branch

```bash
git branch -M main
```

Rename current branch to main.

---
