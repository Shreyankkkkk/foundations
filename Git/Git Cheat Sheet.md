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
# Additional Git Commands & Options

## Configuration

### Configuration Levels

| Level | Flag | Scope |
|------|------|------|
| System | `--system` | All users |
| Global | `--global` | Current user |
| Local | `--local` | Current repository |

Priority:

```
Local > Global > System
```

---

## Repository Information

### List tracked files

```bash
git ls-files
```

### Show repository root

```bash
git rev-parse --show-toplevel
```

### Show current branch

```bash
git branch --show-current
```

---

# Viewing History

## Advanced git log

### Show patch for each commit

```bash
git log -p
```

### Show statistics

```bash
git log --stat
```

### Pretty format

```bash
git log --pretty=format:"%h %an %ar - %s"
```

### Show all branches

```bash
git log --oneline --graph --all
```

---

## Filter History

### By date

```bash
git log --since="2025-01-01"
git log --after="2 weeks ago"

git log --until="2025-01-15"
git log --before="yesterday"
```

### By commit message

```bash
git log --grep="bug"
git log --grep="fix" --grep="auth" --all-match
```

### Find commits that changed text

```bash
git log -S "search_text"
```

### Find commits matching regex

```bash
git log -G "regex"
```

---

## git show

Show commit message only

```bash
git show -s <commit>
```

Show a file from a specific commit

```bash
git show <commit>:path/to/file
```

---

## More git diff

Compare current working tree with a commit

```bash
git diff <commit>
```

Show only filenames

```bash
git diff --name-only <commit1> <commit2>
```

Show statistics

```bash
git diff --stat <commit1> <commit2>
```

---

# Commit References

Current commit

```text
HEAD
```

Previous commit

```text
HEAD~1
```

Two commits back

```text
HEAD~2
```

Parent commit

```text
HEAD^
```

Previous commits from branch

```text
main~3
```

Examples

```bash
git show HEAD~1

git diff HEAD~3 HEAD

git log HEAD~5..HEAD
```

---

# Shortlog

Summarize commits by author

```bash
git shortlog
```

Count commits

```bash
git shortlog -sn
```

---

# Blame

Show who last modified each line

```bash
git blame file.js
```

Specific lines

```bash
git blame -L 10,20 file.js
```

Show email

```bash
git blame -e file.js
```

Ignore whitespace

```bash
git blame -w file.js
```

---

# Bisect

Start binary search

```bash
git bisect start
```

Mark bad

```bash
git bisect bad
```

Mark good

```bash
git bisect good <commit>
```

Finish

```bash
git bisect reset
```

---

# Undo Changes

## Restore

Discard file changes

```bash
git restore <file>
```

Discard all working directory changes

```bash
git restore .
```

Restore from another commit

```bash
git restore --source=<commit> <file>
```

---

## Reset

Soft reset

```bash
git reset --soft HEAD~1
```

Mixed reset (default)

```bash
git reset --mixed HEAD~1
```

Hard reset

```bash
git reset --hard HEAD~1
```

---

## Revert

Revert latest commit

```bash
git revert HEAD
```

Stage revert without committing

```bash
git revert --no-commit <commit>
```

---

## Reflog

View HEAD history

```bash
git reflog
```

Recover commit

```bash
git branch recovered <commit>
```

---

## Clean

Preview removal

```bash
git clean -n
```

Delete untracked files

```bash
git clean -f
```

Delete files and directories

```bash
git clean -fd
```

Delete ignored files too

```bash
git clean -fdx
```

---

# Branches

## Branch Information

Show local branch with latest commit

```bash
git branch -v
```

Show remote branches

```bash
git branch -r
```

Show branches containing a commit

```bash
git branch --contains <commit>
```

Merged branches

```bash
git branch --merged
```

Unmerged branches

```bash
git branch --no-merged
```

---

## Create Branch

Create from another branch

```bash
git branch <new-branch> main

git switch -c <new-branch> main
```

Create from commit

```bash
git branch <new-branch> <commit>

git switch -c <new-branch> <commit>
```

Create from tag

```bash
git switch -c <new-branch> <tag>
```

---

## Rename Branch

Rename current branch

```bash
git branch -m new-name
```

Rename another branch

```bash
git branch -m old-name new-name
```

Force rename

```bash
git branch -M new-name
```

---

# Merge

Custom merge message

```bash
git merge feature -m "Merge feature"
```

Force merge commit

```bash
git merge --no-ff feature
```

Squash merge

```bash
git merge --squash feature
```

Abort merge

```bash
git merge --abort
```

---

## Merge History

Merge commits only

```bash
git log --merges
```

Non-merge commits

```bash
git log --no-merges
```

Main branch history

```bash
git log --first-parent
```

---

# Merge Conflict Resolution

Launch merge tool

```bash
git mergetool
```

Show conflicted files

```bash
git diff --name-only --diff-filter=U
```

Choose our version

```bash
git checkout --ours file
```

Choose their version

```bash
git checkout --theirs file
```