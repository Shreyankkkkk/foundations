# Git & GitHub Fundamentals

---

# Lesson 1 — Git Fundamentals

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

# Lesson 2 — Git Configuration

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

# Line Endings

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

## Why Line Endings Exist

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

## Git Solution

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

# Colorful Output

Enable colored Git output:

```bash
git config --global color.ui auto
```

---

# Git Aliases

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

# Lesson 3
 
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
    HEAD        - Points to current directory
    config      - Repository configurations
    objects/    - stores all contents (Commits, trees, blobs)
    refs/       - stores branch and tag references

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
Untracked       Git doesn't know about this file
Unmodified      Tracked file with no changes
Modified        Tracked file that has been changed
Staged          Changes marked for the next commit

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

Running "git init"  in an existing repository is safe - it wont overwrite anything

---

# Lesson 4 - Basic Git Workflow

---

## The Three Working Area

    Area	                Description
Working Directory   The files you see and edit
Staging Area        Changes queued for the next commit
Repository          Permanent storage of all commits

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

Benefit	                        Description
Selective commits       Choose exactly which changes to commit
Review changes          See what's about to be committed
Logical commits         Group related changes together
Split work              Separate unrelated changes into different commits

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
# Unstage a specific file (keep changes)
git restore --staged filename.js

# Older syntax (still works)
git reset HEAD filename.js

# Unstage all files
git restore --staged .
git reset HEAD
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
SHA Hash        Unique 40-character identifier
Author          Who created the changes
Committer       Who made the commit (usually same as author)
Date            When the commit was made
Parent          The previous commit (or commits for merges)
Message         Description of the changes
Tree            Snapshot of the entire project

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
