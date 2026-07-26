# Git Cheat Sheet

## Configuration

### Check Git installation

```bash
git --version
```

### View configuration

```bash
git config --list
```

### Set user identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Set default branch for new repos

```bash
git config --global init.defaultBranch main
```

### Set default editor

```bash
git config --global core.editor "code --wait"
```

### Line endings

```bash
git config --global core.autocrlf true    # Windows
```

```bash
git config --global core.autocrlf input   # macOS / Linux
```

### Enable colored output

```bash
git config --global color.ui auto

```

## Git Aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg "log --oneline --graph --decorate"
git config --global alias.amend "commit --amend --no-edit"
```

## Repository basics

### Initialize a repository

```bash
git init
```

### Clone a repository

```bash
git clone <repository-url>
```

### Check repository status

```bash
git status
```

## Basic workflow

### Stage files

```bash
git add <file>
git add <file1> <file2>
git add <directory>/
git add .
git add -A
git add -u
```

### Commit changes

```bash
git commit -m "message"
git commit
git commit -am "message"
git commit --amend
```

## Viewing changes

### Unstaged changes

```bash
git diff
```

### Staged changes

```bash
git diff --staged
git diff --cached
```

### Compare commits

```bash
git diff <commit1> <commit2>
```

## Commit history

### View history

```bash
git log
git log --oneline
git log --oneline --graph
git log -5
git log --author="Name"
git log -- <path>
```

### Show commit details

```bash
git show
git show <commit>
git show --stat <commit>
```

## Remove and move files

### Remove files

```bash
git rm <file>
git rm --cached <file>
```

### Rename files

```bash
git mv <oldname> <newname>
```

### Manual rename

```bash
mv <oldname> <newname>
git add <newname>
```

## Pager controls

```bash
q
```

```bash
git --no-pager <command>
```

## Staging area

The staging area (index) holds changes that will be included in the next commit.

### Review staged changes

```bash
git status
git diff --staged
git diff --cached
```

### Unstage changes

```bash
git restore --staged <file>
git restore --staged .
```

### Older unstage syntax

```bash
git reset HEAD <file>
git reset HEAD
```

### Partial staging

```bash
git add -p <file>
```

Options:

- y: stage this hunk
- n: do not stage this hunk
- q: quit
- a: stage this and remaining hunks
- d: do not stage this or remaining hunks
- s: split into smaller hunks
- e: manually edit the hunk

### Staged deletions and renames

```bash
git rm <file>          # delete and stage
rm <file>
git add <file>         # stage deletion
```

```bash
git mv <oldname> <newname>
```

### View index

```bash
git ls-files --stage
```

## Commit practices

### Make atomic commits

- One logical change per commit
- Keep commits small and focused
- Review staged changes before committing

### Create a commit

```bash
git add <file>
git commit -m "Add feature or fix"
```

### Multi-line commit message

```bash
git commit
```

Or:

```bash
git commit -m "Short summary" -m "Longer description"
```

### Amend the last commit

```bash
git commit --amend -m "Updated message"
git add <forgotten-file>
git commit --amend --no-edit
```

### Empty commit

```bash
git commit --allow-empty -m "Trigger CI build"
```

### Sign commits with GPG

```bash
git config --global user.signingkey <KEY_ID>
git commit -S -m "Signed commit"
git config --global commit.gpgsign true
```

### Commit template

```bash
cat > ~/.gitmessage << 'EOF'
Title: Short summary

Body: Explain what changed and why.

Issue references:
Fixes #
EOF
```

```bash
git config --global commit.template ~/.gitmessage
```
