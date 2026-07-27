# Git & GitHub Fundamentals

---

# Lesson 1 — Git and Why Version Control

## Objective

The purpose of these notes is to learn Git well enough to confidently use it in every software project.

By the end of learning Git, I should be able to:

- Track changes in my code.
- Save meaningful project snapshots.
- Upload projects to GitHub.
- Maintain a professional GitHub portfolio.
- Use Git comfortably inside VS Code.

These notes are documentation of my learning process, not a complete Git textbook.

---

# Lesson 2 — Installing and Git Configuration

## Configuration Levels

Git has three configuration levels:

| Level  | Flag       | Location         | Scope                             |
| ------ | ---------- | ---------------- | --------------------------------- |
| System | `--system` | `/etc/gitconfig` | All users on the system           |
| Global | `--global` | `~/.gitconfig`   | All repositories for current user |
| Local  | `--local`  | `.git/config`    | Current repository only           |

Priority order:

```
Local > Global > System
```

Local settings override global settings, which override system settings.

---

## Essential Configuration Options

### Default Branch Name

Set the default branch name for new repositories:

```bash
git config --global init.defaultBranch main
```

---

### Default Editor

Set the preferred text editor for Git messages:

VS Code:

```bash
git config --global core.editor "code --wait"
```

Vim:

```bash
git config --global core.editor "vim"
```

Nano:

```bash
git config --global core.editor "nano"
```

---

## Line Endings

Git handles line endings differently between operating systems.

Windows:

```
CRLF
```

Linux/macOS:

```
LF
```

Git normalizes these differences so developers can collaborate across different systems.

---

### Why Line Endings Exist

Historically:

- CR = Carriage Return
- LF = Line Feed

Older typewriters required two actions:

1. Move back to the start of the line.
2. Move down to the next line.

Different operating systems inherited different conventions.

Windows uses:

```
CRLF
```

Linux/macOS use:

```
LF
```

---

### Git Solution

Git internally prefers LF.

Depending on configuration, Git converts files automatically.

Windows:

```bash
git config --global core.autocrlf true
```

Mac/Linux:

```bash
git config --global core.autocrlf input
```

---

## Colorful Output

Enable colored Git output:

```bash
git config --global color.ui auto
```

---

## Git Aliases

Aliases create shortcuts for commonly used commands.

Example:

Short status:

```bash
git config --global alias.st status
```

Usage:

```bash
git st
```

---

Short checkout:

```bash
git config --global alias.co checkout
```

Usage:

```bash
git co main
```

---

Pretty log:

```bash
git config --global alias.lg "log --oneline --graph --decorate"
```

Usage:

```bash
git lg
```

---

Amend last commit:

```bash
git config --global alias.amend "commit --amend --no-edit"
```

Usage:

```bash
git amend
```

---

# Lesson 3: Creating First Repository

## Creating your First Repository

### What is a repository

A repository (or "repo") is simply a folder that Git monitors for changes. It contains:
Your project files
A hidden .git directory with all version history

---

### Creating a Repository

1. Initialize a Repository

```bash
git init
```

This creates .git directory containing:
HEAD - Points to current directory
config - Repository configurations
objects/ - stores all contents (Commits, trees, blobs)
refs/ - stores branch and tag references

    .git/
    ├── HEAD           # Current branch reference
    ├── config         # Repository configuration
    ├── description    # Used by GitWeb
    ├── hooks/         # Scripts for Git events
    ├── info/          # Additional info (like exclude patterns)
    ├── objects/       # All stored content
    └── refs/          # Branch and tag pointers

2. Clone an existing repository from somewhere else

---

### Checking Status

displays the current state of repository

```bash
git status
```

---

### File Stages

    State               Description

Untracked Git doesn't know about this file
Unmodified Tracked file with no changes
Modified Tracked file that has been changed
Staged Changes marked for the next commit

---

### Adding Files

Use "git add" to start tracking file

```bash
git add .
```

---

### Making First Commit

A commit saves a snapshot of your staged changes:

```bash
git commit -m "Initial commit: Add README and app.js"
```

---

### Viewing your Commit

see your commit history

```bash
git log
```

for a compact view

```bash
git log --oneline
```

---

### Re-initializing a Repo

Running "git init" in an existing repository is safe - it wont overwrite anything

---

# Lesson 4 - Basic Git Workflow

---

## The Three Working Area

    Area	                Description

Working Directory The files you see and edit
Staging Area Changes queued for the next commit
Repository Permanent storage of all commits

---

## The Basic Cycle

---

### Step 1: Make Changes

Edit files in your working directory:

```bash
echo "function greet() { return 'Hello!'; }" > utils.js
```

---

### Step 2: Check Status

See what's changed:

```bash
git status
```

---

### Step 3: Stage Change

Add files to the staging area:

```bash
git add utils.js
```

---

### Step 4: Commit

Save the staged changes:

```bash
git commit -m "Add utils.js with greet function"
```

---

### Step 5: Repeat

Continue making changes, staging, and committing.

---

## Understanding git add

The "git add" command has several forms:

```bash
# Add a specific file
git add filename.js

# Add multiple specific files
git add file1.js file2.js file3.js

# Add all files in a directory
git add src/

# Add all changes in the current directory
git add .

# Add all changes everywhere
git add -A

# Interactively choose what to add
git add -p
```

---

## Understanding git commit

The "git commit" command has several forms:

```bash
# Commit with inline message
git commit -m "Your commit message"

# Commit with multi-line message (opens editor)
git commit

# Add all tracked files and commit
git commit -a -m "Message"
# or
git commit -am "Message"

# Amend the last commit
git commit --amend
```

---

## Viewing Changes

"Git Diff": See what changed in the working directory (unstaged changes):

```bash
git diff
```

See what's staged for commit:

```bash
git diff --staged
# or
git diff --cached
```

Compare two commits:

```bash
git diff abc123 def456
```

---

## Viewing History

1. "git log" : See the commit history:

```bash
# Full log
git log

# One line per commit
git log --oneline

# With graph showing branches
git log --oneline --graph

# Last 5 commits
git log -5

# Commits by a specific author
git log --author="Your Name"

# Commits affecting a specific file
git log -- filename.js
```

2. "git show" : View a specific commit:

```bash
# Show the latest commit
git show

# Show a specific commit
git show abc1234

# Show just the files changed
git show --stat abc1234
```

---

## Removing and Moving Files

---

### 1. Removing Files

```bash
# Remove from Git and filesystem
git rm filename.js

# Remove from Git only (keep the file)
git rm --cached filename.js

# After removing, commit the change
git commit -m "Remove filename.js"
```

---

### 2. Moving / Renaming Files

```bash
# Rename a file
git mv oldname.js newname.js

# This is equivalent to:
# mv oldname.js newname.js
# git rm oldname.js
# git add newname.js

# Commit the rename
git commit -m "Rename oldname.js to newname.js"
```

---

# Lesson 5 - Understanding the staging area

---

It's an intermediate area between your working directory and the repository where you prepare commits.

---

## What is Staging Area

Only changes in the staging area will be included in the next commit

The staging area gives you fine-grained control:

Benefit Description
Selective commits Choose exactly which changes to commit
Review changes See what's about to be committed
Logical commits Group related changes together
Split work Separate unrelated changes into different commits

---

#### Without Staging Area

```bash
# Some systems commit all changes at once
svn commit -m "Everything changed"  # No control!
```

---

#### With Staging Area

```bash
# Git lets you choose
git add login.js           # Stage only login changes
git commit -m "Fix login"  # Commit just that

git add signup.js          # Stage signup changes separately
git commit -m "Add signup" # Different commit
```

---

### Adding Files

```bash
# Add a specific file
git add filename.js

# Add multiple files
git add file1.js file2.js

# Add all files in a directory
git add src/

# Add all changes (new, modified, deleted)
git add .
git add -A

# Add only modified and deleted files (not new)
git add -u
```

---

### Checking whats staged

```bash
# See status
git status

# See staged changes
git diff --staged
git diff --cached  # Same thing
```

---

### Unstaging File

```bash
# Unstage a specific file (keep changes in working directory)
git restore --staged filename.js

# Older syntax (still works)
git reset HEAD
git reset HEAD filename.js

# Unstage all files
git restore --staged .
```

---

## Partial Staging with git add -p

The -p (or --patch) flag lets you interactively choose which parts of a file to stage:

```bash
git add -p filename.js (or any other file)
```

Git will show you each change (called a "hunk") and ask what to do:

    @@ -1,5 +1,7 @@
    function login() {
    +  // Added validation
    validateInput();
    +  logAttempt();
    return authenticate();
    }
    Stage this hunk [y,n,q,a,d,s,e,?]?

Options:

    y - Stage this hunk
    n - Don't stage this hunk
    q - Quit (don't stage remaining)
    a - Stage this and all remaining hunks
    d - Don't stage this or remaining hunks
    s - Split into smaller hunks
    e - Manually edit the hunk

---

### The index File

The staging area is stored in .git/index. This binary file tracks:

    Which files are staged
    Their content (as blob references)
    File permissions and timestamps

You can inspect it with:

```bash
git ls-files --stage
```

---

### Staging Deleted Files

when you delete a file, you need to stage the deltion

```bash
# Delete and stage in one command
git rm filename.js

# Or manually
rm filename.js
git add filename.js  # Stages the deletion
```

---

### Staging Renamed Files

Git tracks renames through content similarity:

```bash
# Rename and stage in one command
git mv oldname.js newname.js

# Or manually
mv oldname.js newname.js
git add oldname.js newname.js
```

---

## Staging Area Best Practices

---

### Review Before Commiting

Always check what you're about to commit:

```bash
git diff --staged  # See the actual changes
git status         # See which files
```

---

### Make Atomic Commits

Each commit should represent one logical change:

```bash
# Good: Separate concerns
git add auth.js
git commit -m "Add authentication logic"

git add auth.test.js
git commit -m "Add auth tests"
```

---

### Dont Stage Debug Code

Use "git add -p" to leave console.log statements out:

```bash
git add -p
# Answer 'n' to debug code hunks
# Answer 'y' to real changes
```

---

### Use Staging as a Review Step

The staging area is your chance to review changes before making them permanent.

---

# Lesson 6 - Making Meaningful Commits

---

Commits are the building blocks of Git history. Each commit is a snapshot of your project at a point in time. Learning to make good commits is essential for maintaining a useful project history.

---

## What is a Commit

A commit is a permanent snapshot that contains:

---

### Commit Componenets

    Component	        Description

SHA Hash Unique 40-character identifier
Author Who created the changes
Committer Who made the commit (usually same as author)
Date When the commit was made
Parent The previous commit (or commits for merges)
Message Description of the changes
Tree Snapshot of the entire project

---

## Creating Commits

---

### Basic Commit

```bash
# Stage changes first
git add filename.js

# Commit with a message
git commit -m "Add login validation"
```

---

### Multi-Line Commit Messages

```bash
# Opens your editor
git commit

# Or inline with -m (use multiple -m flags)
git commit -m "Add login validation" -m "This includes email format checking and password strength requirements."
```

---

### Stage and Commit Together

```bash
# Only works for already-tracked files
git commit -am "Update all tracked files"
```

---

## Viewing Commits

```bash
# Full log
git log

# One line per commit
git log --oneline

# Show diffs
git log -p

# Last 3 commits
git log -3

# Show stats (files changed)
git log --stat

# Pretty format
git log --pretty=format:"%h %an %ar - %s"

# Graphical branch history
git log --oneline --graph --all
```

---

## Amending Commis

---

### Fix the last Commit message

```bash
git commit --amend -m "New Message"
```

--

### Add Forgotten files to new commit

```bash
git add forgotten-file.js
git commit --amend --no-edit
```

Warning: Only amend commits that haven't been pushed!

---

## Atomic Commits

An atomic commit is a self-contained unit of change:

---

### Characteristics of atomic commits:

1. Single purpose: One logical change per commit
2. Complete: The project works after each commit
3. Independent: Can be reverted without side effects
4. Reviewable: Easy to understand and review

---

### Empty Commits

Sometimes you need a commit without file changes:

```bash
git commit --allow-empty -m "Trigger CI build"
```

Use cases:
Triggering CI/CD pipelines
Marking milestones
Documentation-only commits

---

### Signing Commits

For security, you can sign commits with GPG:

```bash
# Configure GPG key
git config --global user.signingkey YOUR_KEY_ID

# Sign a commit
git commit -S -m "Signed commit"

# Always sign commits
git config --global commit.gpgsign true
```

---

### Commit Templates

Create a template for consistent messages:

```bash
# Create template file
cat > ~/.gitmessage << 'EOF'

# Title: Summary, imperative, 50 chars or less

# Body: Explain *what* and *why* (not *how*). Wrap at 72 chars.

# Issue references:
# Fixes #
EOF

# Configure Git to use it
git config --global commit.template ~/.gitmessage
```

---

# Lesson 7: Viewing Commit History

---

Git keeps a complete record of every change ever made to your project. Learning to navigate and explore this history is essential for understanding your codebase and tracking down issues.

---

## The git log commit

The primary tool for viewing history is git log:

```bash
git log
```

---

## Log Formatting Options

---

### One-Line Format

```bash
git log --oneline
```

---

### Graph View

```bash
git log --oneline --graph
```

---

#### Include all branches

```bash
git log --oneline --graph -all
```

---

### Custom Format

```bash
git log --pretty=format:"%h %an %ar - %s"
```

| Placeholder | Meaning                                            | Example                           |
| ----------- | -------------------------------------------------- | --------------------------------- |
| `%h`        | Short commit hash                                  | `a1b2c3d`                         |
| `%H`        | Full commit hash (SHA-1/SHA-256 depending on repo) | `a1b2c3d4e5f...`                  |
| `%an`       | Author name                                        | `John Smith`                      |
| `%ae`       | Author email                                       | `john@email.com`                  |
| `%aD`       | Author date (RFC 2822 format)                      | `Mon, 25 Jul 2026 12:30:00 +0000` |
| `%ad`       | Author date                                        | `Mon Jul 25 12:30:00 2026 +0000`  |
| `%ar`       | Author date, relative                              | `2 hours ago`                     |
| `%at`       | Author date as UNIX timestamp                      | `1785328200`                      |
| `%ai`       | Author date (ISO 8601 format)                      | `2026-07-25 12:30:00 +0000`       |
| `%cn`       | Committer name                                     | `John Smith`                      |
| `%ce`       | Committer email                                    | `john@email.com`                  |
| `%cD`       | Committer date (RFC 2822 format)                   | `Mon, 25 Jul 2026 12:30:00 +0000` |
| `%cd`       | Committer date                                     | `Mon Jul 25 12:30:00 2026 +0000`  |
| `%cr`       | Committer date, relative                           | `2 hours ago`                     |
| `%ct`       | Committer date as UNIX timestamp                   | `1785328200`                      |
| `%ci`       | Committer date (ISO 8601 format)                   | `2026-07-25 12:30:00 +0000`       |
| `%s`        | Commit message subject (first line)                | `Fix login bug`                   |
| `%f`        | Sanitized subject for filenames                    | `fix-login-bug`                   |
| `%b`        | Commit message body                                | `Added validation logic`          |
| `%B`        | Raw commit message (subject + body)                | `Full message`                    |
| `%d`        | Ref names (branches/tags)                          | `(HEAD -> main)`                  |
| `%D`        | Ref names without parentheses                      | `HEAD -> main, origin/main`       |
| `%p`        | Parent commit hashes (short)                       | `a1b2c3d`                         |
| `%P`        | Parent commit hashes (full)                        | `a1b2c3d4e5...`                   |
| `%N`        | Commit notes                                       | `Notes attached to commit`        |
| `%T`        | Tree hash                                          | `Project snapshot hash`           |
| `%t`        | Short tree hash                                    | `Short tree hash`                 |

---

## Limiting Log Output

---

### By Number

```bash
git log -5              # Last 5 commits
git log -n 10           # Last 10 commits
```

---

### By Date

```bash
git log --since="2025-01-01"
git log --after="2 weeks ago"
git log --until="2025-01-15"
git log --before="yesterday"
```

---

### By Author

```bash
git log --author="Jane"
git log --author="jane@example.com"
111
```

---

### By Message Content

```bash
git log --grep="bug"
git log --grep="fix" --grep="auth" --all-match  # Both terms
```

---

### By File Changes

```bash
git log -- path/to/file.js
git log -- src/
```

---

### By Content Changes

```bash
# Find commits that changed a specific string
git log -S "functionName"

# Find commits matching a regex
git log -G "function.*validate"
```

---

## Viewing Commit Details

---

### git show

View the full details of a specific commit:

```bash
# Show latest commit
git show

# Show specific commit
git show a1b2c3d # a1b2c3 represents the hash value

# Show just the message
git show -s a1b2c3d

# Show stats only
git show --stat a1b2c3d

# Show specific file from a commit
git show a1b2c3d:path/to/file.js
```

---

### git diff between commits

```bash
# Compare two commits
git diff a1b2c3d b2c3d4e

# Compare commit with current state
git diff a1b2c3d

# Show only file names
git diff --name-only a1b2c3d b2c3d4e

# Show stats
git diff --stat a1b2c3d b2c3d4e
```

---

## Navigating History

---

### HEAD and reference

HEAD - Current commit
HEAD~1 - One commit before HEAD
HEAD~2 - Two commits before HEAD
HEAD^ - Parent of HEAD (same as HEAD~1)
HEAD^^ - Grandparent of HEAD

main - Latest commit on main branch
main~3 - Three commits before main

Example

```bash
# Show the previous commit
git show HEAD~1

# Diff between 3 commits ago and now
git diff HEAD~3 HEAD # Show me the difference in file contents between the commit that is 5 commits behind HEAD and the current HEAD commit.

# Log from specific point
git log HEAD~5..HEAD # basically means "show me the log of commits from head 5 to head"
```

---

## The git shortlog Command

Summarize commits by author:

```bash
git shortlog
```

Output:
Name 1:
commits
Name 2:
commits
...

---

### Count by author

```bash
git shortlog -sn
```

Output
{number of commits} Name 1
{number of commits} Name 2
...

---

## Blame: Finding who changed what

The git blame command shows who last modified each line:

```bash
git blame path/to/file.js
```

---

### Blame Options

```bash
# Specific line range
git blame -L 10,20 file.js

# Show email instead of name
git blame -e file.js

# Ignore whitespace changes
git blame -w file.js
```

---

## Finding Bugs with git bisect

Binary search through history to find when a bug was introduced:

```bash
# Start bisecting
git bisect start

# Mark current version as bad
git bisect bad

# Mark known good version
git bisect good v1.0.0

# Git checks out a middle commit
# Test and mark as good or bad
git bisect good   # or: git bisect bad

# Repeat until found
# Git tells you: "abc123 is the first bad commit"

# End bisecting
git bisect reset
```

---

## Creating Useful Aliases

Set up aliases for common log formats:

```bash
# Pretty log with graph
git config --global alias.lg "log --oneline --graph --decorate"

# Detailed log
git config --global alias.ll "log --pretty=format:'%C(yellow)%h%Creset %s %C(cyan)(%ar)%Creset %C(blue)<%an>%Creset'"

# Log with files changed
git config --global alias.lf "log --oneline --stat"
```

---

## Visual Tools

Visual Tools
Many GUI tools make history exploration easier:

    gitk: Built-in visual history browser
    git log --graph: ASCII art in terminal
    GitHub/GitLab: Web interfaces
    VS Code GitLens: Extension with inline blame
    Fork, GitKraken, Sourcetree: Desktop GUI clients

---

# Lesson 8: Undoing Changes

Everyone makes mistakes. Git provides several ways to undo changes, from simple fixes to complete reverts. Understanding these tools will save you from many headaches.

---

## The Undo ToolKit

| Situation                   | Solution                      |
| --------------------------- | ----------------------------- |
| Unstage a file              | `git restore --staged <file>` |
| Discard working changes     | `git restore <file>`          |
| Modify the last commit      | `git commit --amend`          |
| Undo commits (keep changes) | `git reset --soft <commit>`   |
| Undo commits (lose changes) | `git reset --hard <commit>`   |
| Undo a pushed commit        | `git revert <commit>`         |

---

## Discarding Working Directory Changes

When you want to throw away changes you haven't staged:

```bash
# Discard changes to a specific file
git restore filename.js

# Discard all working directory changes
git restore .

# Older syntax (still works)
git checkout -- filename.js
```

---

### Restore a File from a specific commit

```bash
# Get file from previous commit
git restore --source HEAD~1 filename.js

# Get file from specific commit
git restore --source abc123 filename.js
```

---

## Understanding git reset

The git reset command moves the branch pointer and optionally modifies the staging area and working directory.

---

### Three Reset Modes

| Reset Mode            | Moves HEAD | Clears Staging Area | Clears Working Directory |
| --------------------- | :--------: | :-----------------: | :----------------------: |
| `--soft`              |     ✓      |          ✗          |            ✗             |
| `--mixed` _(default)_ |     ✓      |          ✓          |            ✗             |
| `--hard`              |     ✓      |          ✓          |            ✓             |

---

### Soft Reset

Moves HEAD but keeps everything staged:

```bash
git reset --soft HEAD~1
```

Use case: Combine multiple commits into one.

---

### Mixed Reset (Default)

Moves HEAD and unstages changes:

```bash
git reset HEAD~1
# Some as: git reset --mixed HEAD~1
```

---

### Hard Reset

Moves HEAD and discards all changes

```bash
git reset --hard HEAD~1
```

WARNING: This is destructive! All changes are lost
USE CASE: Completely discrad recent commits

---

## Using git Revert

Unlike reset, "revert" creates a new commit that undoes changes. This is safe for pushed commits.

```bash
# Revert the last commit
git revert HEAD

# Revert a specific commit
git revert abc123

# Revert without auto-commit (stage changes only)
git revert --no-commit abc123
```

---

### Reset vs Revert

| Aspect                  | Reset | Revert |
| ----------------------- | ----- | ------ |
| Modifies history        | Yes   | No     |
| Safe for pushed commits | No    | Yes    |
| Creates new commit      | No    | Yes    |

---

## Recovering from mistakes

---

### The Reflog

git keeps a log of all HEAD movements

```bash
git reflog
```

---

### Reover a "LOST" Commit

if you accidentally reset too far:

```bash
# Find the lost commit in reflog
git reflog

# Reset back to it
git reset --hard abc123

# Or create a new branch pointing to it
git branch recovered abc123
```

the reflog keeps entries for about 90 days

```bash
#   A--B--C--D (bug)
#        |
#       E -- F -- G
```

---

## Cleaning Untracked Files

Remove files that arent tracked by git

```bash
# See what would be removed (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove ignored files too
git clean -fdx
```

Warning: git clean permanently deletes files!

---

# Lesson 9: What are Branches

Branches are one of Git's most powerful features. They allow you to work on different features, fixes, or experiments in isolation without affecting the main codebase.

---

## Understanding Branches

A branch is simply a pointer to a commit. When you create a branch, Git creates a new pointer—it doesn't copy any files.

The default branch (usually main or master) is just a branch like any other.

---

## Why Use Branches?

| Benefit              | Description                                    |
| -------------------- | ---------------------------------------------- |
| Isolation            | Work on features without affecting stable code |
| Parallel development | Multiple features developed simultaneously     |
| Experimentation      | Try ideas without risk                         |
| Code review          | Review changes before merging                  |
| Releases             | Maintain different versions                    |

---

## The HEAD Pointer

Head is a special pointer that indicates your current position in the repository.

- Usually points to branch name (eg: HEAD -> main -> commit)
- When you commit, the current branch moves forward
- When you checkout a branch, HEAD moves to that branch

---

### Detach Head

if HEAD points directly to a commit (not a branch), youre in "Detached HEAD" state:

```bash
git checkout abc1234
```

this is useful for looking at old commits, but be carful, commits made here right be lost if you dont create a branch

---

## Visualizing Branches

```bash
# See all branches
git branch

# See branches with last commit
git branch -v

# See all branches including remote
git branch -a

# Visual log with branches
git log --oneline --graph -- all
```

---

## Branch Naming

Branches can have almost any name, but follows these conentions:

## Common Prefixes

| Prefix     | Use                     |
| ---------- | ----------------------- |
| `feature/` | New features            |
| `bugfix/`  | Bug fixes               |
| `hotfix/`  | Urgent production fixes |
| `release/` | Release preparation     |
| `docs/`    | Documentation           |
| `test/`    | Testing                 |

---

# Lesson 10: Creating and Switching Branches

Now that you understand what branches are, let's learn how to create, switch between, and manage them.

---

## Creating a New branch

---

### git branch

Create a new branch:

```bash
git branch feature-login
```

this create the branch but doesnt switch to it. You're still on your current branch.

---

### git checkout -b (Classic way)

Create and switch in one command

```bash
git checkout -b feature-login
```

---

### git switch -c (Modern Way)

The newer, more intuitive command:

```bash
git swtich -c feature-login
```

---

## Switching Branches

---

### git checkout (Classic)

```bash
git checkout feature-login
```

---

### git swtich (Modern)

```bash
git switch feature-login
```

---

#### why git switch

"git checkout" does many things (switch branches, restore files, etc.) "git switch" is dedicated to branch switching, making it clearer and safer

```bash
# These do the same thing:
git checkout main
git switch main

# But only checkout can restore files:
git checkout -- file.js    # Restore file
# git switch -- file.js    # Doesn't work
```

---

## Creating Branches from Specific Points

---

### From another Branch

```bash
# create branch from main (while on any branch)
git branch {name} main

#Create and switch
git switch -c {name} main
```

---

### From a specific commit

```bash
# Create branch from commit
git branch {branch_name} {hash_value}

# Create and switch
git switch -c {branch_name} {hash_value}
```

---

### From a specific tag

---

#### Creating a tag

A tag is just a name attached to a specific commit, but unlike a branch, it doesn't move.

```bash
# A --- B --- C --- D --- E
#                  ^      ^
#               v1.0.0   main

git tag {tag_label}

#if you wanna create a tag at a specific commit
git tag {tag_label} {hash_value}
```

---

```bash
git switch -c {branch_name} {tag_name}
```

---

## Listing Branches

```bash
# List local branches
git branch

# List with more info
git branch -v

# List all branches (including remote)
git branch -a

# List remote branches only
git branch -r

# List branches containing a commit
git branch --contains abc123

# List merged branches
git branch --merged

# List unmerged branches
git branch --no-merged
```

NOTE: The \* indicates the current branch.

---

## Renaming Branches

```bash
# Rename current branch
git branch -m new-name

# Rename specific branch
git branch -m old-name new-name

# Force rename (even if new name exists)
git branch -M new-name
```

---

### Renaming the default branch

```bash
# Rename master to main
git branch -m master main

# Update remote (if applicable)
git push -u origin main
git push origin --delete master
```

---

## Deleting Branches

---

### Delete Merged Branches

```bash
# Delete a branch
git branch -d {branch_name}

# Force delete a branch
git branch -D {branch_name}
```

git will refuse if the branch isnt merged, if its -d
otherwise force delete it if its -D


---

## Switching with Uncommitted Changes

Case 1: No Conflict

if your changes dont conflict with the target branch, Git carries them over:

```bash
# Make changes to file.js
git switch other-branch
# Changes come with you
```

Case 2: Conflict

if changes would be overwritten, Git prevents the switch:

```bash
error: Your local changes to the following files would be overwritten by checkout:
        file.js
Please commit your changes or stash them before you switch branches.
```

Solution:

```bash
# Option 1: Commit your changes
git commit -am "WIP: save work"
git switch other-branch

# Option 2: Stash your changes
git stash
git switch other-branch
git stash pop  # Later, restore changes

# Option 3: Discard changes (careful!)
git restore .
git switch other-branch
```

---

## The detached HEAD State

sometimes you need to look at an old commit

```bash
git checkout abc123 (hash)
```

---

### Workign in detached HEAD

you can make commits, but they are not on any branch

```bash
git checkout abc123
# make changes
git commit -m "Experimental Change"
```

---

### Keeping Detached HEAD Commits

if you wnat ot keep commits made in detached HEAD:

```bash
# While still in detached HEAD
git switch -c my-experiment
# Now your commits are on a branch
```

or if you already switched away:

```bash
# Find the commit in reflog
git reflog
# Create branch pointing to it
git branch rescue abc123
```