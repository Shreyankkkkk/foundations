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

---

# Lesson 11: Merging Branches

After developing a feature on a branch, you'll want to integrate it back into your main branch. This is called merging.

---

## What is Merging?

Merging combines the changes from one branch into another:

```bash
# Before merge:
# main:      A ← B ← C
#                     \
# feature:             D ← E

# After merge:
# main:      A ← B ← C ← ← ← M
#                     \     /
# feature:             D ← E
```

---

## Types of Merges

---

### Fast Forward Merge

when the target branch has no new commits since the source branched off:

```bash
# Before:
# main:      A ← B ← C
#                   ↑
#                  main
# feature:           D ← E
#                       ↑
#                     feature

# After (fast-forward):
# main:      A ← B ← C ← D ← E
#                            ↑
#                          main
#                          feature
```

Git just moves the main pointer forward. No merge commit needed.

```bash
git switch main
git merge feature
#fast forward merge
```

---

### Three-Way Merge

when both branches have new commits:

```bash
# Before:
# main:      A ← B ← C ← F
#                    \
# feature:            D ← E

# After:
# main:      A ← B ← C ← F ← M
#                    \     /
# feature:            D ← E
```

Git creates merge commit (M) with two parents

```bash
git switch main
git merge feature
# Three way merge, creates merge commit
```

---

## Performing a Merge

---

### Basic Merge

```bash
# Switch to the target branch
git switch main

# Merge the source branch
git merge feature

# The feature branch still exists
git branch -d feature  # Delete if done
```

---

#### Merge with Custom Messages

```bash
git merge feature -m "Merge feature branch: add user login"
```

---

### No Fast - Forward

force a merge commit even when fast-forward is possible:

```bash
git merge --no--ff feature

# With --no-ff:
# main:      A ← B ← C ← ← ← M
#                    \     /
# feature:            D ← E
#
# Without --no-ff (fast-forward):
# main:      A ← B ← C ← D ← E
#                          ↑
#                        (feature history lost)
```

---

### Squash Merge

Combine all commits into a single commit:

```bash
git merge --sqaush feature
git commit -m "Add Login Feature"

# Before:
# feature:  D ← E ← F (3 commits)

# After squash merge:
# main:     ... ← X (single commit with all changes)
```

the feature branch commits are combined. Original Hitory is lost in main

---

## Merge Options

| Option                        | Description                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `--no-ff`                     | Always create a merge commit, even if Git could perform a fast-forward merge                                 |
| `--ff-only`                   | Only perform the merge if it can be completed as a fast-forward merge; otherwise fail                        |
| `--squash`                    | Combine all changes from the branch into one set of changes and create a single commit on the current branch |
| `--no-commit`                 | Perform the merge but stop before creating the merge commit, allowing manual changes before committing       |
| `--abort`                     | Cancel an ongoing merge and return the repository to the state before the merge started                      |
| `--edit`                      | Open the editor to modify the default merge commit message                                                   |
| `--no-edit`                   | Accept the default merge commit message without opening an editor                                            |
| `--strategy=<strategy>`       | Choose a specific merge strategy                                                                             |
| `--strategy-option=<option>`  | Pass additional options to the selected merge strategy                                                       |
| `--verify-signatures`         | Verify that the commits being merged have valid GPG signatures                                               |
| `--allow-unrelated-histories` | Allow merging branches that do not share a common ancestor                                                   |
| `-m <message>`                | Provide a custom merge commit message                                                                        |

---

## Understanding Merge Commits

A merge commit has two (or more) parents

```bash
git log --oneline
# abc123 Merge branch 'feature' into main
# def456 Add login form (from feature)
# 789abc Update homepage (from main)

git show abc123
# Shows merge commit with both parents
```

---

## Merge Strategies

Git uses different strategies depending on the situation:

---

### Recursive (Default):

Used for three-way merges. Handles most cases well.

```bash
git merge -s recursive feature
```

---

### Ours

keeps our version of everything (dicard their changes):

```bash
git merge -s ours feature
```

---

### Octopus

Merge multiple branches at once:

```bash
git merge feature1 feature2 feature3
```

---

## Viewing Merge History

```bash
# See merge commits
git log --merges

# See non-merge commits
git log --no-merges

# Graphical view
git log --oneline --graph

# First-parent only (main branch history)
git log --first-parent
```

---

## Aborting a Merge

if something goes wrong during a merge:

```bash
git merge --abort
```

this restores your branch to the state before the merge started

---

## Good Practises

```bash

1. Update Before Merging

    git switch main
    git pull                    # Get latest changes
    git switch feature
    git merge main              # Update feature with main's changes
    # Resolve any conflicts
    git switch main
    git merge feature           # Now merge feature to main

2. Use --no-ff for feature branches

    git merge --no-ff feature -m "Merge feature: user authentication"

3. Delete Merged Branches

    git branch -d features
    # keep your branch list clean

4. Test before merging
    # Always verify that merge doesn't break anything:
    git merge feature
    npm test
    npm run build
```

---

# Lesson 12: Resolving Merge Conflicts

Merge conflicts occur when Git can't automatically combine changes from different branches. This happens when the same lines of code are modified differently in both branches.

---

## When do conflicts occur?

- The same lines are changed in both branches
- A file is modified in one branch and deleted in another
- The same file is added with different content in both branches

---

## Anatomy of a Conflict

when a conflict occurs

```bash
# function greet() {
# <<<<<<< HEAD
#   return "Hello World";
# =======
#   return "Hello Git";
# >>>>>>> feature
```

Everything between <<<<<<< and ======= is YOUR version. Everything between ======= and >>>>>>> is THEIR version.

---

## Conflict resolution process

1. Attempt to merge
2. Check Status
3. Open the conflicted file and edit the file to resolve the conflict
4. Mark as resolved
5. Complete the Merge

---

## Resolution Strategies

---

### Keep Ours

Keep your version, discard theirs:

---

### Keep theirs

Keep their version, discard yours:

---

### Combine both

Merge the logic from both:

---

### Rewrite Completely

Sometimes neither version is right

---

## Using Merge tools

---

### built in merge tool

```bash
git mergetool
```

git will open your configured merge tool.

---

### Configure a merge tool

```bash
# Use VS Code
git config --global merge.tool vscode
# Tell Git to use VS Code as the merge conflict tool.
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
# Tell Git how to open the conflicted file in VS Code and wait until it is resolved.

# Use vimdiff
git config --global merge.tool vimdiff
```

---

### VS Code Conflict Resolution

VS Code shows conflict markers with helpful buttons:

    "Accept Current Change" (yours)
    "Accept Incoming Change" (theirs)
    "Accept Both Changes"
    "Compare Changes"

---

## Check conflicting status

```bash
# See conflicted files
git diff --name-only --diff-filter=U

# See conflict details
git diff

# See specific file
git diff file.js
```

---

## Using git checkout during conflicts

During a conflict, you can choose versions:

```bash
# Use our version entirely
git checkout --ours file.js

# Use their version entirely
git checkout --theirs file.js

# Then mark as resolved
git add file.js
```

---

# Lesson 13: Introduction to Remotes

So far, we've worked with local repositories. To collaborate with others, you need to connect to remote repositories—copies of your project hosted on a server.

---

## What is remote?

A remote is a refrence to repository hosted elsewhere like github, gitlab or bibucket

---

## Why use remotes:

| Benefit       | Description                             |
| ------------- | --------------------------------------- |
| Backup        | Your code is safely stored in the cloud |
| Collaboration | Share code with team members            |
| Deployment    | Deploy from a central location          |
| CI/CD         | Trigger automated tests and builds      |
| Code Review   | Review changes before merging           |

---

## The origin remote

when you close a repository, git automatically creates a remote called "origin"

```bash
git clone https://github.com/user/repo.git
cd repo

git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)
```

"origin" is just a converntion, the default name for the primary remote

---

## Managing Remotes

---

### View Remotes

```bash
# List remote names
git remote

# List with URLs
git remote -v

# Show detailed info
git remote show origin
```

---

### Add a remote

```bash
git remote add upstream https://github.com/original/repo.git
```

now you have two remotes

- "origin" - Your fork
- "upstream" - the original repo

---

### Rename a remote

```bash
git remote rename origin github
```

---

### Change remote URL

```bash
git remove set-url origin git@githum.com:user/repo.git
```

---

### Remove a remote

```bash
git remote remove upstream
```

---

## Remote tracking branches

when you fetch from a remote, git creates a remote-tracking branches:
remote tracking branches like "origin/main" are read only references to where the remote branches were last time you fetched

---

### View remote tracking branches

```bash
# All branches including remote-tracking
git branch -a

# Remote-tracking only
git branch -r
```

---

## Understanding Remote URLS

---

### HTTPS URLS

    https://github.com/username/repository.git

    Works through firewalls
    Requires username/password or token
    Easier to set up

### SSH URLS

    git@github.com:username/repository.git

    Requires SSH key setup
    No password prompts after setup
    More secure

---

#### Switching between protocols

```bash
# Check current URL
git remote -v

# Switch to SSH
git remote set-url origin git@github.com:user/repo.git

# Switch to HTTPS
git remote set-url origin https://github.com/user/repo.git
```

---

## Multiple remotes

you can have multiple remotes for differnt purposes

```bash
# Your fork (Fork basically means make a copy of that repository and put that in my own repositories)
git remote add origin git@github.com:you/project.git

# Original project (to get updates)
git remote add upstream git@github.com:org/project.git

# Deployment server
git remote add production ssh://deploy@server.com/var/git/project.git
```

Common remote names:

    origin - Your primary remote (your fork)
    upstream - Original project you forked from
    production - Production server
    staging - Staging server

---

## The fetch, push and pull cycle

```bash
#              ┌──────────────────────┐
#              │    Remote Server     │
#              │    (e.g., GitHub)    │
#              └──────────────────────┘
#                   ↑           ↓
#              push │           │ fetch
#                   │           ↓
#              ┌──────────────────────┐
#              │   Your Local Repo    │
#              │                      │
#              │   origin/main ←────── fetched data
#              │   main ←────────────── your work
#              │                      │
#              └──────────────────────┘
```

1. Fetch
   Means:
   "Go check GitHub and download any new information, but don't touch my current work."

2. Pull
   Means:
   "Fetch the updates and apply them to my current branch."

3. Push
   Means:
   "Send my local commits to GitHub."

---

## Remote Configuration

Remote settings are stored in .git/config.

```bash
[remote "origin"]
    url = git@github.com:user/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*

[remote "upstream"]
    url = https://github.com/org/repo.git
    fetch = +refs/heads/*:refs/remotes/upstream/*

[branch "main"]
    remote = origin
    merge = refs/heads/main
```

You can edit this directly or use git config:

```bash
git config remote.origin.url
git config remote.origin.url "new-url"
```

---

# Lesson 14 - Pushing and Pulling

Pushing and pulling are how you synchronize changes between your local repository and remote repositories.

---

## Git Push

Pushing uploads your local commits to a remove repository

---

### Basic Push

```bash
git push origin main
```

this pushes your local main branch to the origin remote.

---

### Push Current Branch

```bash
git push
```

if your branch is tracking a remote branch, this pushes to it.

---

### Push with upstream

```bash
git push -u origin feature
or
git push --set-upstream origin feature
```

the -u flag 1. Pushes the branch 2. Sets up tracking (so future git push and git pull just work)

    (Basically, this creates a branch on remote and sets up a connection between local branch and the remote branch, so everytime i commit on the local branch and push it, github or any other cloud serive platform knows that it needs to push to that default branch and not get confused with other branches in the same repository)

---

### Push all branches

```bash
git push --all origin
```

    (basically, pushes all branches to their respective remote default branches that it represents)

---

### Push tags

```bash
#push specific tag
git push origin {Tag}

# Push all tags
git push origin --tags
```

    (basically, in my local computer i have commits with specific tags, if i want github to remember that this commit has tag this, it needs to know, for that we do git push origin tag, so it tells git that this commit has tag, if there are multiple tags on my local computer, all of them get pushed. You are pushing tag references so each commit corresponds to a tag reference, thats why github can understand even if an older commit has a tag and adds it)

---

### Push Rejections

if the remote has commits you don't have:
and you try to push, git throws an error
so to solve this, you gotta pull first from github, all the new commits and then push

or force push the commit but in this case, new commits on github will be lost

---

## Git Pull

Pulling downlaods and integrates remote changes

---

### Basic Pull

```bash
git pull origin main
```

this is equivalent to
git fetch origin main
git merge origin/main

---

### Pull Current Branch

```bash
git pull
```

if tracking is set up, pulls from the tracked remote branch to local branch.

---

### Pull with rebase

```bash
git pull --rebase origin main
```

instead of merging, this rebases your changes on top of remote changes. Creates a cleaner history

    (basically, let me temporarily removey your work, pull and merge the new work and THEN add your work back so it becomes clearer)

---

## The Push Pull Workflow

```bash
# Start of day: Get latest changes
git pull origin main

# Make your changes
# ... edit files ...

# Commit your work
git add .
git commit -m "Add feature"

# Before pushing, get any new changes
git pull origin main

# Push your changes
git push origin main
```

---

## Configuring Default Behaviour

---

### Set Push Default

```bash
# Push current branch to matching remote branch
git config --global push.default current

# Only push if upstream is set
git config --global push.default simple  # (default)
```

---

### Set Pull Default

```bash
# Always rebase on pull
git config --global pull.rebase true

# Always merge on pull (default)
git config --global pull.rebase false
```

---

# Lesson 15 - Fetch vs Pull

Understanding the difference between "fetch" and "pull" is crucial for workign with remote repositories effectively.

---

## The Key difference

| Command     | What it does                         |
| ----------- | ------------------------------------ |
| `git fetch` | Downloads changes, doesn't integrate |
| `git pull`  | Downloads changes AND merges them    |

---

## Git Fetch

```bash
git fetch origin
```

fetch downloads remote changes without affecting your working directory:

---

### What Fetch Does

1. Contacts the remote repository
2. Downloads any new commits
3. Updates remote-tracking branches (e.g., origin/main)
4. Does NOT change your local branches
5. Does NOT change your working directory

---

### Why use fetch?

    Safe: Won't mess up your current work
    Preview: See what changed before integrating
    Control: Decide when and how to integrate

---

### Fetch Commands

```bash
# Fetch all branches from origin
git fetch origin

# Fetch specific branch
git fetch origin main

# Fetch from all remotes
git fetch --all

# Fetch and prune deleted branches
git fetch --prune

# Fetch tags
git fetch --tags
```

---

### After Fetching

View what was fetched:

```bash
# See the difference
git log main..origin/main

# See what commits are new
git log --oneline origin/main ^main

# View the changes
git diff main origin/main
```

then intergrate when ready:

```bash
# Merge the fetched changes
git merge origin/main

# Or rebase
git rebase origin/main
```

---

## When to use Each

---

### Use Fetch When

- You want to see what changed before integrating
- You're not sure if you want to integrate yet
- You want to integrate differently (rebase vs merge)
- You want to compare branches before merging
- You're working on something delicate and don't want surprises

```bash
git fetch origin
git log --oneline main..origin/main  # What's new?
git diff main origin/main             # What changed?
# Looks good, now merge
git merge origin/main
```

---

### Use Pull When

- You just want the latest changes quickly
- You trust the remote changes
- You're starting fresh work and need to update first
- Simple workflow with no local uncommitted work

```bash
git pull origin main # Done!
```

---

# Lesson 16 - Tracking Branches

Tracking branches create a connection between your local branches and remote branches, making push and pull operations simpler and more intuitive.

---

## What is tracking branch?

A tracking branch is a local branch that has a direct relationship with a remote branch:

When a local branch tracks a remote branch:

- git push knows where to push
- git pull knows where to pull from
- git status shows how far ahead/behind you are

```bash
# Local Branch         Remote-Tracking Branch       Remote Branch
# main         ←────→  origin/main          ←────→  origin's main
# feature      ←────→  origin/feature       ←────→  origin's feature
```

---

## Setting up Tracking

---

### When cloning

when you clone a repository, "main" is auotmatically set up to track "origin/main":

```bash
git clone https://github.com/user/repo.git
cd repo

git status
# On branch main
# Your branch is up to date with 'origin/main'.
```

---

### When Pushing a new branch

Use "-u" or "--set-upstream" to set up tracking

```bash
git push -u origin feature
```

Feature tracks origin/feature

---

### For exisiting branches

```bash
# Set upstream for current branch
git branch --set-upstream-to=origin/feature

# Short form
git branch -u origin/feature
```

---

### When checking out remote branches

```bash
# If there is no local branch but there is a remote branch

# Automatic tracking if branch name matches
git checkout feature
# If origin/feature exists, local 'feature' will track it

# Or explicitly
# Tracing remote branches that dont exist yet
    # when you create a new branch and watnt to push it:

    # create branch
    git checkout -b feature origin/feature

    # Push and set up tracking in one command
    git push -u origin new-feature
```

---

## Viewign trackig information

---

### git branch with verbose flag

```bash
git branch -vv

# Output:
    #* main      abc123 [origin/main] Latest commit message
    #  feature   def456 [origin/feature: ahead 2] Add new feature
    #  bugfix    789abc [origin/bugfix: behind 3] Fix bug
    #  local     111222 Work in progress  # No tracking (no brackets)
```

The brackets show

- which remote branch is tracked
- how many commits ahead/behind

---

### git status

```bash
git status
```

shows tracking information

```bash
# on branch feature
#   Your branch is ahead of 'origin/feature' by 2 commits.
#   (use "git push" to publish your local commits)
```

---

### Using git remote show

```bash
git remote show origin
```

shows which local branches track which remote branches

---

## Ahead and Behind

When your local branch and remote branch have diverged:

    git status
    # Your branch and 'origin/main' have diverged,
    # and have 2 and 3 different commits each, respectively.

Check specific counts:

```bash
# Commits ahead of origin
git rev-list --count origin/main..main

# Commits behind origin
git rev-list --count main..origin/main

# Both
git rev-list --left-right --count main...origin/main
# Output: 2    3  (2 ahead, 3 behind)
```

---

## Changing or Removing tracking

---

### Change what a branch tracks

```bash
# change current branch tracking to another remote branch
git branch -u origin/other-branch
```

---

### Remove tracking

```bash
# remove current branch tracking
git branch --unset-upstream
```

---

### Change for a specific branch

```bash
git branch -u origin/main feature
```

---

## Trackign and Push/Pull

- Without tracking
  you must specify remote and branch

```bash
git push origin feature
git pull origin feature
```

- With tracking
  just use the commands directly

```bash
git push
git pull
```

git knows where to push/pull from

---

## Fetching and Tracking

after fetching, new remote branches appear:

```bash
git fetch origin
git branch -r
#origin/main
#origin/feature
#origin/new-branch (new!)
```

to work on the new branch

```bash
# Automatic tracking if names match
git checkout new-branch

# Or explicitly
git checkout -b new-branch origin/new-branch
```

---

## The Upstream Configuration

Trackign is stored in ".git/config"

```bash
[branch "feature"]
    remote = origin
    merge = refs/heads/feature
```

You can view it with

```bash
git config --get branch.feature.remote
# origin

git config --get branch.feature.merge
# refs/heads/feature
```

---

# Lesson 17 - Introduction to Github

GitHub is the world's largest platform for hosting and collaborating on Git repositories. It adds powerful features on top of Git that make collaboration easier.

---

## What is GitHub?

Github is a web-based platform that provides:

- _Repository hosting_ : Store your Git repos in the cloud
- _Collaboration tools_ : Work with teams on code
- _Social features_ : Follow developers, star projects
- _Project management_ : Issues, projects, milestones
- _Automation_ : GitHub Actions for CI/CD
- _Documentation_ : Wikis, README rendering

---

## Git vs Github

| Git                      | GitHub                 |
| ------------------------ | ---------------------- |
| Version control software | Cloud hosting platform |
| Runs on your computer    | Runs in the cloud      |
| Command-line tool        | Web interface + API    |
| Free, open source        | Free tier + paid plans |
| Works offline            | Requires internet      |

You can use git without github (using gitlab, bitbucket, or self-hosted) but most developers use github.

---

## Github Concepts

---

### Repository

A repository on github contains:

- Your project files
- Complete git history
- Issues and discussions
- Pull requests
- Project settings

---

### Owner Types

**Type Description**
User - Personal account (github.com/username)
Organization - Team/Company account (githum.com/org)

---

### Visibility

**Visibility Who can see**
Public Anyone on the internet
Private Only you and collaborators
Internal Organization members (Enterprise)

---

## The Github Interface

| Tab           | Purpose                       |
| ------------- | ----------------------------- |
| Code          | Browse files, view README     |
| Issues        | Bug reports, feature requests |
| Pull requests | Proposed code changes         |
| Actions       | CI/CD workflows               |
| Projects      | Kanban boards, planning       |
| Wiki          | Documentation                 |
| Security      | Vulnerability alerts          |
| Insights      | Analytics, graphs             |
| Settings      | Repository configuration      |

---

## Github Features

---

### Stars

"Starring" a repository is like bookmarking it:

- Shows appreciation
- Saves to your starred list
- Helps repositories gain visibility

---

### Forks

A fork is your personal copy of someone else's repository:

- Full copy under your account
- Can Make changes freely
- User for contributing to projects

---

### Watch

get notifications about repository activity:

- _Participating_: Issues/PRs you're involved in
- _All Activity_: Every issue, PR, commit
- _Ignore_: No notifications
- _Custom_: Choose what to watch

---

## The Github CLI

Github provides a CLI tool called "gh":
(basically, "I control GitHub features through commands instead of clicking buttons.")

```bash
# YOU DO NOT NEED IT RIGHT NOW, ITS FOR THE FUTURE

# Install (macOS)
brew install gh

# Authenticate
gh auth login

# Create repo
gh repo create my-project --public

# Clone repo
gh repo clone owner/repo

# Create issue
gh issue create --title "Bug" --body "Description"

# Create PR
gh pr create --title "Feature" --body "Description"
```

---

# Lesson 18 - Creating Repositories on Github

There are several ways to create a repositories on Github. This lesson covers all the methods and options

---

## Creating a new Repsoitory

---

### Via Web Interface

1. Click the + button in the top right
2. Select New repository
3. Fill in the details:

**Field Description**
Repository name URL-friendly name (e.g., my-project)
Description Brief explanation (optional)
Visibility Public or Private
Initialize Add README, .gitignore, license

---

### Repository Naming

Good names are:

- Lowercase with hyphens: my-awesome-project
- Descriptive: react-todo-app
- Concise: blog-api

Avoid:

- Spaces (use hyphens instead)
- Special characters
- Generic names like project1

---

## Initialization Options

---

### README.md

A README.md is the first thing visitors see:

```bash
# Project Name
Brief description of what this project does.

## Installation
Enter all the installations
```

---

## Creating from template

---

### Using Template Repositories

Some repos are marked as template:

1. Go to template repository
2. Click "Use this template"
3. Choose "Create a new repository"
4. Name your new repo
   Your repo will have the same files but a fresh git history

---

### Making your Repo a Template

Settings → General → Check "Template repository"

---

## Repository settings

---

### After Creation

Navigate to settings tab:
| Setting | Purpose |
|---------|---------|
| General | Name, visibility, features |
| Collaborators | Add team members |
| Branches | Protection rules |
| Pages | Host static website |
| Secrets | Environment variables for Actions |

---

### Branch Protection

Protect important branches:

Branch: main
Rules:

- ✓ Require pull request before merging
- ✓ Require approvals: 1
- ✓ Require status checks to pass
- ✓ Require branches to be up to date

---

### Features to Enable/Disable

- Issues
- Wiki
- Projects
- Discussions
- Sponsorship

---

## Repository Visibility

---

### Changing Visibility

Settings → General → Danger Zone → Change visibility
⚠️ Warning: Making a private repo public exposes all history!

---

### Visibility Options

**Option Use Case**
Public Open source, portfolio projects
Private Work projects, sensitive code

---

## Repository best practices

---

### Include these files

├── README.md # Project documentation
├── LICENSE # How others can use it
├── .gitignore # Files to exclude
├── CONTRIBUTING.md # How to contribute
├── CODE_OF_CONDUCT.md # Community guidelines
├── CHANGELOG.md # Version history
└── .github/
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE.md
└── workflows/ # GitHub Actions

---

### Good README structure

1. Title and badges
2. Description: What, why
3. Installation: How to set up
4. Usage: Basic examples
5. API/Documentation: Link or details
6. Contributing: How to help
7. License: Legal terms

---

## Archiving and Deleting

---

### Archive

Settings → Danger Zone → Archive

    Makes repo read-only
    Keeps all history
    Good for deprecated projects

---

### Delete

Settings → Danger Zone → Delete

    ⚠️ Permanent - cannot be undone
    Type repo name to confirm

---

# Lesson 19 - Cloning and Forking

There are two ways to get a copy of a repository: cloding (for your own repos or to work locally) and forking (to contribute to others' repos)

---

## Cloning Repositories

Cloning creates a local copy of a remote repository.

---

### Basic Clone

```bash
# HTTPS
git clone https://github.com/owner/repository.git

# SSH (recommended)
git clone git@github.com:owner/repository.git

# GitHub CLI
gh repo clone owner/repository
```

---

### What Clone Does

1. Creates a directory named after the repo
2. Downloads all files and history
3. Sets up origin remote pointing to the source
4. Checks out the default branch

---

#### Clone Options

```bash
# Clone to specific folder
git clone https://github.com/owner/repo.git my-folder

# Clone specific branch
git clone -b develop https://github.com/owner/repo.git

# Shallow clone (only recent history)
git clone --depth 1 https://github.com/owner/repo.git

# Clone with submodules
git clone --recursive https://github.com/owner/repo.git
```

---

#### After Cloning

```bash
cd repository

# See the remote
git remote -v
# origin  https://github.com/owner/repository.git (fetch)
# origin  https://github.com/owner/repository.git (push)

# See branches
git branch -a

# Start working
git checkout -b my-feature
```

---

## Forking Repositories

A fork if your personal copy of someone else's repository on Github.

---

### Why Fork?

| Use Case        | Description                          |
| --------------- | ------------------------------------ |
| Contributing    | Make changes to propose back         |
| Experimentation | Try ideas without affecting original |
| Starting point  | Use as a base for your own project   |
| Archiving       | Keep a copy of important code        |

---

### How to Fork

1. Go to the repository on GitHub
2. Click the Fork button
3. Choose where to fork (your account or organization)
4. Wait for GitHub to copy the repo

---

### The fork workflow

Step 1:
Click "Fork" on original repository
Step 2:
Clone your fork

    "git clone https://github.com/owner/repo.git"

Step 3:
Add upstream remote to keep track of changes made by the owner of original repository

    "git remote add upstream https://github.com/owner/repo.git"
    "git remote -v" - To check the remotes

Step 4: - Always start by fetching the new changes made by the original owner - Merge the changes into your main branch, this merges the commits in your local computer - Push the new changes into your github fork (repository)

    - "git fetch upstream"
    - "git checkout main"
      "git merge upstream/main"
    - "git push origin main"

Step 5:
Make changes and then push them, note all the changes should be made in another branch and then push it onto main branch

    "git checkout -b new_changes"
    "git push -u origin new_changes"

---

## When to clone vs fork

---

### Clone when

- It's your own repository
- You have direct push access
- You just want a local copy to browse
- You're working on a private team project

---

### Fork when

- You want to contribute to someone else's project
- You don't have push access
- You want your own copy to modify
- You want to propose changes via pull request

---

## Submodules

some repositories contain other repositories

```bash
# Clone with submodules
git clone --recursive https://github.com/owner/repo.git

# Initialize submodules after clone
git submodule init
git submodule update

# Update submodules
git submodule update --remote
```

---

## Large Repositories

for very large repositories

```bash
# Shallow clone (faster, less history)
git clone --depth 1 https://github.com/owner/large-repo.git

# Later, get more history if needed
git fetch --unshallow

# Partial clone (Git 2.22+)
git clone --filter=blob:none https://github.com/owner/large-repo.git
```

---

## Troubleshooting

---

### Permission Denied

- Check SSH key is added to GitHub
- Verify repository access permissions
- Use HTTPS with personal access token

---

### Slow Clone

- Use shallow clone: --depth 1
- Clone specific branch only
- Check network connection

---

# Lesson 20 - Good practices for github profile

Your GitHub profile is your developer identity. A well-crafted profile helps with job opportunities, networking, and building credibility in the developer community.

---

# Lesson 21 - Pull Request Basics

Pull requests (PRs) are how you propose changes on GitHub. They're the center of collaborative development, enabling code review, discussion, and automated testing before changes are merged.

---

## What is a pull request

A pull request says "I have changes in my branch that i'd like to merge into your branch"

Despite the name "pull" request, youre actually askign the maintainer to pull your changes into their branch.

---

## Creating a pull request

---

### From github web UI

1. Push your branch to GitHub
2. Go to the repository
3. Click "Compare & pull request" (appears after pushing)
4. Or: Pull requests tab → New pull request

---

## Pull Request Components

---

### Title

Short, descriptive summary:
✅ "Add user authentication with JWT"
✅ "Fix memory leak in image processor"
❌ "Changes"
❌ "Fix bug"

### Description

Explain what and why

### Labels

Categorize your PR (Pull Request)
bug, feature, enhancement
documentation, refactor
breaking-change, needs-review

### Reviewers

Request specific people to review your code.

### Assignees

Who's responsible for the PR.

### Linked Issues

Connect to related issues:

    "Closes # 123" (auto-closes when merged)
    "Fixes # 456"
    "Relates to # 789"

---

## The PR Lifecycle

1. Create Branch
   ↓
2. Make Commits
   ↓
3. Push to GitHub
   ↓
4. Create PR ←────────────────┐
   ↓ │
5. CI Checks Run │
   ↓ │
6. Code Review ─── Requested Changes
   ↓
7. Approval
   ↓
8. Merge
   ↓
9. Delete Branch

---

## PR Status Checks

Github can run automated checks

| Check        | Purpose                  |
| ------------ | ------------------------ |
| **CI Tests** | Run automated tests      |
| **Linting**  | Check code style         |
| **Build**    | Verify it builds         |
| **Security** | Scan for vulnerabilities |
| **Coverage** | Check test coverage      |

PRs can require checks to pass before merging.

---

## Viewing a Pull Request

---

### Files Changed Tab

Shows the diff

    Green: Added lines
    Red: Removed lines
    Yellow: Modified files

---

### Conversation Tab

    Description
    Comments and discussion
    Review summaries
    Check statuses

---

### Commits Tab

List of all commits in the PR.

---

### Checks Tab

Status of automated checks.

---

## Updating a Pull Request

---

### Adding more commmits

Simply push more commits to the same branch
The PR automatically updates

---

### Keeping up with base branch

if the target branch has new commits

```bash
# Merge approach
git fetch origin
git checkout feature
git merge origin/main
git push

# Merge approach
git checkout feature
git pull origin main
git push

#------------------------------------------------------------------

# Rebase approach (cleaner history) - fetch merge
git fetch origin
git checkout feature
git rebase origin/main
git push --force-with-lease

# Rebase approach (cleaner history) - pull
git checkout feature
git pull --rebase origin main
git push --force-with-lease
```

---

## Closing Pull Requests

---

### Merging

Click "merge pull request" when approved and checks pass

---

### Closing Without Merging

For PRs that won't be merged:

    Click "Close pull request"
    Leave a comment explaining why

---

### Draft → Ready

For draft PRs, click "Ready for review" when done.

---

# Lesson 22 - Code Review Best Practices

Code review is a critical part of software development. It catches bugs, improves code quality, shares knowledge, and builds team cohesion.

---

## Why Code Review?

| Benefit               | Description                             |
| --------------------- | --------------------------------------- |
| **Quality**           | Catch bugs before they reach production |
| **Knowledge sharing** | Learn from each other's code            |
| **Consistency**       | Maintain code standards                 |
| **Mentoring**         | Help junior developers grow             |
| **Documentation**     | Comments explain the "why"              |

---

## The Review Process

---

### As a reviewer

1. Understand the context: Read the PR description
2. Check the big picture: Does the approach make sense?
3. Review the code: Look at the implementation
4. Test if needed: Pull and run locally
5. Leave constructive feedback: Be helpful, not harsh
6. Approve or request changes: Make a decision

---

### As an Author

1. Self-review first: Check your own code
2. Write a good description: Help reviewers understand
3. Keep PRs small: Easier to review
4. Respond promptly: Keep the process moving
5. Be open to feedback: Code review is collaborative

---

## Github Review Features

Use this to mark parts of the code

| Prefix          | Meaning                        |
| --------------- | ------------------------------ |
| **nit:**        | Minor suggestion, not blocking |
| **question:**   | Seeking clarification          |
| **suggestion:** | Optional improvement           |
| **important:**  | Must be addressed              |
| **blocking:**   | Cannot merge until fixed       |

---

# Lesson 23 - PR Templates

Pull request templates help ensure all PRs include necessary information. They guide contributors and maintain consistency across your project.

---

## Why us PR Templates?

| Benefit          | Description                            |
| ---------------- | -------------------------------------- |
| **Consistency**  | Every PR has the same structure        |
| **Completeness** | Don't forget important information     |
| **Efficiency**   | Less back-and-forth asking for details |
| **Onboarding**   | New contributors know what's expected  |

---

## Creating a PR Template

---

### Single Template

Create a file at one of these locations

    .github/PULL_REQUEST_TEMPLATE.md
    .github/pull_request_template.md
    docs/pull_request_template.md
    PULL_REQUEST_TEMPLATE.md

The ".github/" location is most common.

---

### Basic Template Example

Summary
Changes Made
Type of Change
Testing
Checklist
Related Issues

---

## Multiple Templates

for projects with different types of PRs:

---

### Directory Structure

.github/
└── PULL_REQUEST_TEMPLATE/
├── bug_fix.md
├── feature.md
└── documentation.md

---

### Using Template Links

When creating a PR, add a query parameter:
https://github.com/owner/repo/compare/main...feature?template=feature.md
or use the template dropdown in Github UI

---

## Template Types

---

### Feature Template

Feature Description
Motivation - Why is this feature needed
Implementation Detials
Screenshots
Breaking Changes
Migration Guide
Checklist

---

### Bug fix template

Bug description
Boot Cause
Solution
Steps to Reproduce
Before/After
Testing
Related Issues

---

### Documentation Template

Documentation Change
Reasons for Change
Affected Pages
Preview Link
Checklist

---

## Template Best Practices

Keep it Concise
Use Comments for Guidance
Make Checklists Actionable
Include Examples

---

## Conditional Sections

Use HTML comments for optional sections:
Screenshots
Breaking Changes

---

## Integrating with Issues

Link templates to issue templates
Related Issues
Link issues using Keywords - Closes #123 (closes when merged) - Fixes #456 (same as closes) - Relates to #789 (just links)

---

## Template Configuration

---

### Enforce Template Usage

In repository settings:
Require PR Description
Use branch protection rules

---

### Default Labels

You can suggest labels in templates:
<!-- Please add appropriate labels: bug, feature, docs -->
but automatic labeling requires Github Actions or bots

---

## Automation with Templates

GitHub Actions Integration
Templates can prompt for automation:

---

### Deployment

- [ ] Ready for staging deployment
- [ ] Needs production deployment

<!--
Check 'Ready for staging' to trigger automatic deployment.
A maintainer will handle production deployment.
-->

---

### Bot Commands

Some projects use bot commands in templates:

## Bot Commands

<!-- Uncomment to use -->
<!-- /deploy staging -->
<!-- /run-benchmarks -->

---
