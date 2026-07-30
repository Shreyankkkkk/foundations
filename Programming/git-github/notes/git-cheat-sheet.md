# Git & GitHub Complete Cheat Sheet

> Consolidated from lesson notes + original cheat sheet. Organized by topic, with a "gotchas" section at the end for things that are easy to forget.

---

## 1. Configuration

### Config levels (priority: Local > Global > System)

| Level  | Flag       | Location         | Scope                   |
| ------ | ---------- | ---------------- | ----------------------- |
| System | `--system` | `/etc/gitconfig` | All users               |
| Global | `--global` | `~/.gitconfig`   | Current user, all repos |
| Local  | `--local`  | `.git/config`    | Current repository only |

```bash
git --version                          # check install
git config --list                      # view all config

git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git config --global init.defaultBranch main
git config --global core.editor "code --wait"   # vim / nano also valid

git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # macOS / Linux

git config --global color.ui auto
```

### Aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg "log --oneline --graph --decorate"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.ll "log --pretty=format:'%C(yellow)%h%Creset %s %C(cyan)(%ar)%Creset %C(blue)<%an>%Creset'"
git config --global alias.lf "log --oneline --stat"
```

### Repo info

```bash
git ls-files                       # list tracked files
git rev-parse --show-toplevel      # repo root path
git branch --show-current          # current branch name
```

---

## 2. Repository Basics

```bash
git init                           # create a new repo (.git/ folder)
git clone <url>                    # copy an existing repo
git clone <url> my-folder          # clone into custom folder name
git clone -b develop <url>         # clone specific branch
git clone --depth 1 <url>          # shallow clone (recent history only)
git clone --recursive <url>        # clone with submodules
git status                         # current state of repo
```

**File states:** Untracked → Modified → Staged → Committed (Unmodified once clean)

---

## 3. Basic Workflow (Add & Commit)

```bash
git add <file>                     # stage one file
git add <file1> <file2>            # stage multiple
git add <directory>/               # stage a folder
git add .                          # stage everything in current dir
git add -A                         # stage everything, everywhere
git add -u                         # stage only modified/deleted (not new)
git add -p <file>                  # interactively stage hunks
```

```bash
git commit -m "message"
git commit                         # opens editor for multi-line message
git commit -am "message"           # add tracked files + commit (skips new files)
git commit --amend                 # edit the last commit
```

**The 3 working areas:** Working Directory → Staging Area (Index) → Repository (commits)

---

## 4. Staging Area Deep Dive

```bash
git diff --staged                  # or --cached — see what's staged
git restore --staged <file>        # unstage a file, keep changes
git restore --staged .             # unstage everything
git reset HEAD <file>              # older syntax, same effect
```

### Partial staging (`git add -p`)

Options when reviewing a hunk:
`y` stage · `n` skip · `q` quit · `a` stage this+rest · `d` skip this+rest · `s` split · `e` edit manually

```bash
git ls-files --stage               # inspect the index directly
```

**Staged deletions/renames:**

```bash
git rm <file>                      # delete + stage deletion
git rm --cached <file>             # untrack but keep file locally
git mv old.js new.js               # rename + stage (= mv + rm + add)
```

---

## 5. Commits — Making Good Ones

### Anatomy of a commit

SHA hash · Author · Committer · Date · Parent(s) · Message · Tree (project snapshot)

### Amending

```bash
git commit --amend -m "New message"
git add forgotten-file.js
git commit --amend --no-edit       # add file to last commit, keep message
```

⚠️ **Only amend commits that haven't been pushed.**

### Other useful commit flags

```bash
git commit --allow-empty -m "Trigger CI build"     # empty commit (CI triggers, milestones)
git commit -S -m "Signed commit"                    # GPG sign
git config --global commit.gpgsign true             # always sign
```

### Commit message template

```bash
cat > ~/.gitmessage << 'EOF'
Title: Summary, imperative, 50 chars or less

Body: Explain *what* and *why* (not *how*). Wrap at 72 chars.

Issue references:
Fixes #
EOF
git config --global commit.template ~/.gitmessage
```

### Writing good messages (rules)

- Subject ≤ 50 chars, capitalized, no trailing period
- **Imperative mood**: "Add feature" not "Added"/"Adds" — test: _"If applied, this commit will \_\_\_"_
- Blank line, then body wrapped at 72 chars explaining **what & why**, not how
- Footer can reference issues: `Closes #123`

### Conventional commit types

| Type       | Purpose                           |
| ---------- | --------------------------------- |
| `feat`     | New feature                       |
| `fix`      | Bug fix                           |
| `docs`     | Documentation                     |
| `style`    | Formatting only                   |
| `refactor` | Restructuring, no behavior change |
| `perf`     | Performance                       |
| `test`     | Tests                             |
| `build`    | Build system/deps                 |
| `ci`       | CI/CD config                      |
| `chore`    | Misc maintenance                  |
| `revert`   | Reverts a previous commit         |

Avoid pushing WIP commits — squash/reword with interactive rebase first.

---

## 6. Viewing Changes & History

### git diff

```bash
git diff                           # unstaged changes
git diff --staged / --cached       # staged changes
git diff <commit1> <commit2>       # between commits
git diff <commit>                  # working tree vs a commit
git diff --name-only <c1> <c2>     # just filenames
git diff --stat <c1> <c2>          # summary stats
```

### git log

```bash
git log                            # full log
git log --oneline                  # compact
git log --oneline --graph          # ASCII branch graph
git log --oneline --graph --all    # include all branches
git log -5 / -n 10                 # limit count
git log -p                         # show patches (diffs) per commit
git log --stat                     # files changed per commit
git log --pretty=format:"%h %an %ar - %s"
```

**Filter log:**

```bash
git log --since="2025-01-01" --until="2025-01-15"
git log --after="2 weeks ago" --before="yesterday"
git log --author="Jane"
git log --grep="fix" --grep="auth" --all-match   # both terms
git log -- path/to/file.js         # commits touching a file
git log -S "functionName"          # commits that added/removed this string
git log -G "function.*validate"    # regex search in changes
git log --merges / --no-merges     # only merge / only non-merge commits
git log --first-parent             # main-branch-only history
```

### Format placeholders (for `--pretty=format:`)

| Code          | Meaning                   | Code        | Meaning            |
| ------------- | ------------------------- | ----------- | ------------------ |
| `%h` / `%H`   | short/full hash           | `%s`        | subject            |
| `%an` / `%ae` | author name/email         | `%b` / `%B` | body / raw message |
| `%ad` / `%ar` | author date / relative    | `%d` / `%D` | ref names          |
| `%cn` / `%ce` | committer name/email      | `%p` / `%P` | parent hash(es)    |
| `%cd` / `%cr` | committer date / relative | `%T` / `%t` | tree hash          |

### git show

```bash
git show                           # latest commit, full detail
git show <commit>
git show -s <commit>                # message only
git show --stat <commit>            # stats only
git show <commit>:path/to/file      # a file's content at that commit
```

### Commit references

```
HEAD          current commit
HEAD~1        one before HEAD  (same as HEAD^)
HEAD~2        two before HEAD  (same as HEAD^^)
main~3        3 commits before tip of main
```

```bash
git show HEAD~1
git diff HEAD~3 HEAD
git log HEAD~5..HEAD
```

### Author stats / blame / bisect

```bash
git shortlog                        # commits grouped by author
git shortlog -sn                    # counts only

git blame file.js                   # who last touched each line
git blame -L 10,20 file.js
git blame -e file.js                # show email
git blame -w file.js                # ignore whitespace changes

git bisect start
git bisect bad                      # current = bad
git bisect good v1.0.0              # known good commit
# ... test each checkout, mark good/bad, repeat ...
git bisect reset                    # end session
```

### Visual tools

`gitk` · `git log --graph` · GitHub/GitLab web UI · VS Code GitLens · Fork/GitKraken/Sourcetree

---

## 7. Undoing Changes

| Situation                  | Command                       |
| -------------------------- | ----------------------------- |
| Unstage a file             | `git restore --staged <file>` |
| Discard working changes    | `git restore <file>`          |
| Modify last commit         | `git commit --amend`          |
| Undo commits, keep changes | `git reset --soft <commit>`   |
| Undo commits, lose changes | `git reset --hard <commit>`   |
| Undo a **pushed** commit   | `git revert <commit>`         |

### Restore

```bash
git restore filename.js             # discard changes in working dir
git restore .                       # discard all
git restore --source HEAD~1 file.js # pull a file from a past commit
```

### Reset (3 modes)

| Mode                | Moves HEAD | Clears staging | Clears working dir |
| ------------------- | :--------: | :------------: | :----------------: |
| `--soft`            |     ✓      |       ✗        |         ✗          |
| `--mixed` (default) |     ✓      |       ✓        |         ✗          |
| `--hard`            |     ✓      |       ✓        |         ✓          |

```bash
git reset --soft HEAD~1     # combine commits, keep everything staged
git reset HEAD~1            # = --mixed, unstages but keeps files
git reset --hard HEAD~1     # ⚠️ destructive — discards everything
```

### Revert (safe for shared/pushed history — creates a new commit)

```bash
git revert HEAD
git revert abc123
git revert --no-commit abc123       # stage only, don't auto-commit
```

**Reset vs Revert:** Reset rewrites history (local-only use); Revert adds a new commit undoing changes (safe to push/share).

### Reflog — recovering "lost" work

```bash
git reflog                          # log of all HEAD movements (~90 days)
git reset --hard abc123             # jump back to a lost commit
git branch recovered abc123         # or save it to a new branch
```

### Clean untracked files

```bash
git clean -n           # dry run — preview
git clean -f           # remove untracked files
git clean -fd          # + untracked directories
git clean -fdx         # + ignored files too
```

⚠️ `git clean` **permanently deletes** — no reflog recovery for this.

---

## 8. Branches

A branch is just a movable pointer to a commit — creating one doesn't copy files.

### Create / switch

```bash
git branch feature-login                    # create only (doesn't switch)
git checkout -b feature-login               # create + switch (classic)
git switch -c feature-login                 # create + switch (modern, preferred)

git checkout feature-login                  # switch (classic, does many things)
git switch feature-login                    # switch (modern, dedicated command)

git branch new-branch main                  # create from another branch
git branch new-branch <commit-hash>         # create from a specific commit
git switch -c new-branch <tag-name>         # create from a tag
```

> Prefer `git switch` for branch operations and `git restore` for file operations — `git checkout` does both and is more error-prone.

### List / inspect

```bash
git branch                    # local branches (* = current)
git branch -v                 # with last commit
git branch -a                 # all (local + remote)
git branch -r                 # remote-tracking only
git branch --contains <hash>  # branches containing a commit
git branch --merged           # already merged into current
git branch --no-merged        # not yet merged
git branch --list 'feature/*' # pattern match
git branch --sort=-committerdate  # most recent first
```

### Rename / delete

```bash
git branch -m new-name              # rename current branch
git branch -m old-name new-name     # rename another branch
git branch -M new-name              # force rename

git branch -d branch-name           # delete (safe — refuses if unmerged)
git branch -D branch-name           # force delete
git push origin --delete branch-name  # delete on remote too
```

### Tags

```bash
git tag v1.0.0                              # lightweight tag
git tag -a v1.0.0 -m "Release 1.0.0"        # annotated (recommended)
git tag -a v1.0.0 abc1234 -m "message"      # tag a past commit
git tag                                      # list
git tag -l "v1.*"                            # pattern list
git tag -d v1.0.0                            # delete local
git push origin --delete v1.0.0              # delete remote
git push origin v1.0.0                       # push one tag
git push origin --tags                       # push all tags
```

### Detached HEAD

```bash
git checkout abc1234        # HEAD points directly at a commit, not a branch
# commits made here can be lost unless you branch off:
git switch -c my-experiment
```

### Switching with uncommitted changes

- **No conflict** → Git carries changes over automatically.
- **Conflict** → Git blocks the switch. Options: commit (`git commit -am "WIP"`), stash (`git stash` → switch → `git stash pop`), or discard (`git restore .`).

---

## 9. Merging

### Types

- **Fast-forward:** target branch has no new commits since source diverged → pointer just moves forward, no merge commit.
- **Three-way:** both branches have new commits → Git creates a merge commit with two parents.

```bash
git switch main
git merge feature                        # standard merge
git merge feature -m "custom message"
git merge --no-ff feature                 # force a merge commit even if FF possible
git merge --ff-only feature               # fail unless FF is possible
git merge --squash feature                # combine all commits into one (then commit manually)
git merge --no-commit feature             # merge but pause before committing
git merge --abort                         # cancel an in-progress merge
git merge -s ours feature                 # keep our version entirely
git merge feature1 feature2 feature3      # octopus merge (multiple at once)
```

### Merge history

```bash
git log --merges          # merge commits only
git log --no-merges       # exclude merges
git log --first-parent    # main-line history only
```

### Best practices

1. Update both branches before merging (`git pull` on main, merge main into feature, resolve, then merge feature into main).
2. Use `--no-ff` for feature branches to preserve history.
3. Delete branches after merging (`git branch -d`).
4. Test after merging (`npm test`, build, etc.) before pushing.

---

## 10. Resolving Merge Conflicts

Conflicts happen when: the same lines changed in both branches, a file is modified in one and deleted in another, or the same file is added differently in both.

```text
<<<<<<< HEAD
   your version
=======
   their version
>>>>>>> feature
```

**Process:** attempt merge → `git status` to see conflicted files → edit files to resolve → `git add <file>` → `git commit` (or `git merge --continue`).

```bash
git diff --name-only --diff-filter=U      # list conflicted files
git checkout --ours file.js               # take your version entirely
git checkout --theirs file.js             # take their version entirely
git add file.js                           # mark resolved

git mergetool                             # launch configured merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

---

## 11. Rebasing

### Rebase vs Merge

|                          | Merge                                      | Rebase                                  |
| ------------------------ | ------------------------------------------ | --------------------------------------- |
| History                  | Preserves both branches, adds merge commit | Linear — replays commits on top         |
| Safe for shared branches | ✓ Yes                                      | ✗ No (rewrites history)                 |
| Use when                 | Integrating shared/public branches         | Cleaning up a personal branch before PR |

```bash
git checkout feature
git rebase main                 # replay feature's commits on top of main
```

> **Golden Rule:** Never rebase a branch others are also working on / have already pulled. Only rebase local/personal branches.

### Interactive rebase

```bash
git rebase -i HEAD~3            # rewrite last 3 commits
git rebase -i main              # rebase current branch onto main, interactively
```

Editor commands:
| Cmd | Effect |
|---|---|
| `pick` | keep as-is |
| `reword` | keep changes, edit message |
| `edit` | pause to amend the commit |
| `squash` | merge into previous commit, combine messages |
| `fixup` | merge into previous, discard this message |
| `exec` | run a shell command |
| `drop` | remove the commit entirely |

```bash
git commit --fixup abc123               # create a fixup commit
git rebase -i --autosquash main         # auto-arranges fixups during rebase
```

Safety: **branch before rebasing**

```bash
git branch backup-before-rebase
git rebase -i HEAD~5
# if it goes wrong:
git reset --hard backup-before-rebase
```

Continuing/aborting a rebase with conflicts:

```bash
git rebase --continue
git rebase --abort
git rebase --skip
```

---

## 12. Cherry-Picking

Copies one specific commit onto your current branch (without merging the whole source branch).

```bash
git checkout target-branch
git cherry-pick abc1234                     # apply a single commit
git cherry-pick abc1234 def5678             # apply several
git cherry-pick abc1234..def5678            # a range (excludes first)
git cherry-pick abc1234^..def5678           # a range (includes first)
git cherry-pick --no-commit abc1234         # apply changes, don't commit yet
git cherry-pick -x abc1234                  # note "cherry picked from ..." in message
git cherry-pick -s abc1234                  # add sign-off
```

**Conflicts:**

```bash
git cherry-pick --continue     # after resolving
git cherry-pick --abort
git cherry-pick --skip
```

Use cherry-pick for: hotfix to multiple branches, pulling one feature out, recovering lost commits, backporting. If commits depend on each other, cherry-pick them all together (or just merge/rebase instead).

---

## 13. Stashing

Temporarily shelves uncommitted work so you can switch context cleanly.

```bash
git stash                                   # stash tracked/staged changes
git stash push -m "WIP: message"            # stash with a label
git stash -u / --include-untracked          # also stash untracked files
git stash -a / --all                        # also stash ignored files
git stash push -p                           # interactively choose hunks
git stash push -m "msg" file1.js file2.js   # stash specific files only
git stash --keep-index                      # stash only unstaged, keep staged intact
```

```bash
git stash list                              # see all stashes
git stash show                              # summary of latest
git stash show -p                           # full diff of latest
git stash show -p stash@{2}                 # specific stash

git stash pop                               # apply latest + remove from list
git stash apply                             # apply latest, keep in list
git stash apply --index                     # also restore staged/unstaged split
git stash drop stash@{1}                    # delete one stash
git stash clear                             # delete all stashes
git stash branch new-branch stash@{0}       # new branch from a stash
```

Note: **untracked and ignored files are NOT stashed by default** — use `-u`/`-a`.

---

## 14. Remotes

```bash
git remote -v                           # list remotes with URLs
git remote show origin                  # detailed info

git remote add upstream <url>           # add a second remote
git remote rename origin github
git remote set-url origin <new-url>     # switch HTTPS <-> SSH
git remote remove upstream
```

Common remote names: `origin` (your primary/fork), `upstream` (original project), `production`/`staging` (deploy targets).

**URL types:** HTTPS (`https://github.com/user/repo.git` — works everywhere, needs token/password) vs SSH (`git@github.com:user/repo.git` — needs key setup, no password prompts after).

---

## 15. Push & Pull

```bash
git push origin main                    # push local main to origin
git push                                # push current branch (if tracked)
git push -u origin feature              # push + set upstream tracking
git push --all origin                   # push all branches
git push origin --tags                  # push all tags
```

```bash
git pull origin main                    # = fetch + merge
git pull                                # pull tracked branch
git pull --rebase origin main           # rebase instead of merge (cleaner history)
```

```bash
git config --global push.default simple   # default: push only if upstream set
git config --global pull.rebase true      # always rebase on pull
git config --global pull.rebase false     # always merge on pull (default)
```

If push is rejected (remote has commits you don't): `git pull` first, resolve, then push. Avoid force-pushing unless you're sure (and never on shared branches without `--force-with-lease`).

---

## 16. Fetch vs Pull

| Command     | Downloads | Integrates into local branch |
| ----------- | --------- | ---------------------------- |
| `git fetch` | ✓         | ✗                            |
| `git pull`  | ✓         | ✓ (fetch + merge/rebase)     |

```bash
git fetch origin                    # updates remote-tracking branches only
git fetch origin main
git fetch --all
git fetch --prune                   # also remove refs to deleted remote branches
git fetch --tags
```

**After fetching, inspect before integrating:**

```bash
git log main..origin/main           # what's new on remote?
git diff main origin/main           # what changed?
git merge origin/main               # or: git rebase origin/main
```

Use **fetch** when you want to preview before integrating, or choose merge vs rebase deliberately. Use **pull** for a quick, trusted, simple update.

---

## 17. Tracking Branches

A local branch "tracks" a remote branch so `push`/`pull`/`status` know where to sync.

```bash
git push -u origin feature              # sets tracking on first push
git branch --set-upstream-to=origin/feature
git branch -u origin/feature            # short form
git checkout -b feature origin/feature  # create tracking branch explicitly
```

```bash
git branch -vv                          # shows tracked remote + ahead/behind
git status                              # "ahead of origin/main by N commits"
git remote show origin                  # which locals track which remotes
```

**Ahead/behind counts:**

```bash
git rev-list --count origin/main..main       # ahead
git rev-list --count main..origin/main       # behind
git rev-list --left-right --count main...origin/main   # both, e.g. "2  3"
```

```bash
git branch -u origin/other-branch       # change what a branch tracks
git branch --unset-upstream             # remove tracking
```

---

## 18. .gitignore

```gitignore
# Comment
node_modules/          # ignore a directory
*.log                  # wildcard — any depth-1 match
**/logs                # ignore "logs" dirs at any depth
file?.txt              # ? = exactly one character
*.[oa]                 # character class
/config.json           # leading / = repo root only
config.json            # no leading / = matches anywhere

# Negation (must un-ignore parent path first for dirs)
*.log
!important.log

build/*
!build/important.txt   # can't negate inside a fully-ignored dir; ignore contents instead
```

- Trailing `/` → directory only (`build/` won't match a _file_ named build).
- `.gitignore` **only affects untracked files** — it does NOT remove already-tracked files.

**Untrack an already-committed file:**

```bash
git rm --cached filename          # or: git rm -r --cached directory/
# then add pattern to .gitignore
git commit -m "Stop tracking filename"
```

**Personal / global ignores:**

```bash
echo ".myide" >> .git/info/exclude          # this repo only, not shared
git config --global core.excludesfile ~/.gitignore_global
echo ".DS_Store" >> ~/.gitignore_global     # every repo, personal machine
```

**Check what's ignored:**

```bash
git check-ignore -v file.txt        # which rule is ignoring it
git status --ignored                # list all ignored files
```

Templates: github.com/github/gitignore

---

## 19. Git Hooks & Commit Enforcement

Hooks are scripts that run automatically at points in the Git lifecycle. They live in `.git/hooks/` — but that folder is **not committed**, so hooks aren't shared automatically.

| Hook         | Runs                                         | Typical use             |
| ------------ | -------------------------------------------- | ----------------------- |
| `pre-commit` | before commit is created                     | linting                 |
| `commit-msg` | after message written, before commit created | validate message format |

```bash
#!/bin/sh
# .git/hooks/pre-commit
npm run lint
if [ $? -ne 0 ]; then
  echo "Linting failed."
  exit 1
fi
```

**Husky** solves the "hooks aren't shared" problem by storing hooks inside the project (`.husky/`) and versioning them via `package.json`, so every clone gets the same hooks.

---

## 20. GitHub — Repositories

```bash
gh auth login
gh repo create my-project --public
gh repo clone owner/repo
gh issue create --title "Bug" --body "Description"
gh pr create --title "Feature" --body "Description"
```

**Good repo hygiene files:**

```
README.md · LICENSE · .gitignore · CONTRIBUTING.md
CODE_OF_CONDUCT.md · CHANGELOG.md
.github/ISSUE_TEMPLATE/ · PULL_REQUEST_TEMPLATE.md · workflows/
```

**Visibility:** Public (anyone), Private (you + collaborators), Internal (org-only, Enterprise).
**Branch protection (Settings → Branches):** require PR before merge, required approvals, required status checks, require branch up to date.

---

## 21. Cloning vs Forking

| Clone                                          | Fork                                     |
| ---------------------------------------------- | ---------------------------------------- |
| Local copy of a repo                           | Your own remote copy on GitHub           |
| Use when it's your repo / you have push access | Use to contribute to someone else's repo |

**Fork workflow:**

```bash
# 1. Click "Fork" on GitHub
git clone https://github.com/you/repo.git
git remote add upstream https://github.com/original-owner/repo.git
git remote -v

# Keep your fork updated:
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Work in a branch, not main:
git checkout -b new-changes
git push -u origin new-changes
```

**Large repos:**

```bash
git clone --depth 1 <url>              # shallow
git fetch --unshallow                  # get full history later
git clone --filter=blob:none <url>     # partial clone (Git 2.22+)
```

---

## 22. Pull Requests

**PR lifecycle:** create branch → commit → push → open PR → CI checks → code review → approval → merge → delete branch.

```bash
# Keeping a PR branch up to date with base (merge approach):
git fetch origin
git checkout feature
git merge origin/main
git push

# Rebase approach (cleaner history):
git fetch origin
git checkout feature
git rebase origin/main
git push --force-with-lease
```

**Linking issues in PR description:** `Closes #123` / `Fixes #456` / `Relates to #789`

**Draft PRs:** mark work-in-progress; can't be merged accidentally, still run CI, good for early feedback, long-running features, or RFC-style proposals. Convert to "Ready for review" when done.

**Review comment prefixes:** `nit:` minor · `question:` clarify · `suggestion:` optional · `important:` must fix · `blocking:` can't merge until fixed.

### PR Templates

```
.github/PULL_REQUEST_TEMPLATE.md              # single template
.github/PULL_REQUEST_TEMPLATE/feature.md      # multiple, chosen via ?template= or dropdown
```

---

## 23. Issues & Projects

**Issue labels:** `bug` · `feature` · `enhancement` · `documentation` · `good first issue` · `help wanted` · `duplicate` · `wontfix` · `priority: high`

**GitHub Projects views:** Board (Kanban), Table (spreadsheet-style), Roadmap (timeline). Custom fields: Status, Assignee, Priority, Due Date, Iteration.

---

## 24. GitHub Actions (CI/CD)

**Hierarchy:** Event → Workflow → Job(s) → Step(s) → Action

```
.github/workflows/ci.yml
```

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  test:
    needs: build
```

- `run:` → shell command · `uses:` → reusable action
- Jobs run **in parallel** unless linked with `needs:`
- Secrets: `${{ secrets.API_KEY }}` — never hardcode credentials
- Matrix builds → run same job across multiple OS/versions

Common actions: `actions/checkout`, `actions/setup-node`, `actions/cache`, `actions/upload-artifact`

---

## 25. Releases

| Tags (Git)                      | Releases (GitHub)                    |
| ------------------------------- | ------------------------------------ |
| Lightweight pointer to a commit | Built on top of a tag, with metadata |
| No notes, no attachments        | Release notes + downloadable assets  |

**Semantic versioning:** `MAJOR.MINOR.PATCH` — patch = bug fix, minor = new backward-compatible feature, major = breaking change.

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Then: GitHub → Releases → "Create a new release" → pick tag → write notes (or auto-generate from merged PRs) → attach binaries → publish.

Direct download URL pattern:

```
https://github.com/owner/repo/releases/download/v1.0.0/app.zip
https://github.com/owner/repo/releases/latest
```

---

## 26. Workflows (Branching Strategies)

| Strategy           | Structure                                                              | Best for                                  |
| ------------------ | ---------------------------------------------------------------------- | ----------------------------------------- |
| **Feature Branch** | `main` + short-lived `feature/*` branches merged via PR                | Most teams, simple & flexible             |
| **Gitflow**        | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`                | Scheduled/versioned releases, enterprise  |
| **Trunk-Based**    | One `main`, tiny short-lived branches or direct commits, feature flags | Continuous deployment, high CI discipline |
| **Forking**        | Each contributor has their own remote fork + PRs to upstream           | Open source projects                      |

**Feature Branch steps:**

```bash
git switch main && git pull origin main
git switch -c feature/user-authentication
# ...commit work...
git push -u origin feature/user-authentication
git fetch origin && git merge origin/main     # stay updated
# open PR on GitHub, review, approve, merge
git switch main && git pull origin main
git branch -d feature/user-authentication
```

---

## 27. Branch Naming Conventions

```
<type>/<issue-id>-<short-description>

feature/AUTH-123-add-login
bugfix/BUG-456-fix-redirect
hotfix/SEC-789-patch-vulnerability
docs/update-api-reference
```

| Prefix      | Use                     |
| ----------- | ----------------------- |
| `feature/`  | New features            |
| `bugfix/`   | Non-urgent bug fixes    |
| `hotfix/`   | Urgent production fixes |
| `release/`  | Release prep            |
| `refactor/` | Code restructuring      |
| `docs/`     | Documentation           |
| `test/`     | Test additions          |
| `chore/`    | Maintenance             |

Rules: lowercase, hyphens not spaces/underscores, descriptive but concise, include an issue ref when possible.

---

## 28. Keeping History Clean

```bash
git commit --amend -m "Better message"        # rewrite last commit (unpushed only)
git rebase -i HEAD~5                          # squash/reword/reorder/drop
git commit --fixup abc123 && git rebase -i --autosquash main
```

**Cleanup merged branches:**

```bash
git branch --merged main | grep -v main | xargs git branch -d
git fetch --prune                             # remove stale remote-tracking refs
git remote prune origin --dry-run             # preview first
```

**Rule of thumb:** use `revert` for pushed/shared commits (non-destructive), `reset` only for local/unpushed commits.

---

## 29. Quick Reference — Everyday Commands

```bash
git status                          # what's going on
git add . && git commit -m "msg"    # stage + commit
git push                            # upload
git pull                            # download + integrate
git switch -c feature/x             # new branch
git log --oneline --graph --all     # visualize history
git stash / git stash pop           # shelve / restore WIP
git diff                            # unstaged changes
git diff --staged                   # staged changes
```

---

## 30. Important Things to Remember (Gotchas)

- **Never rebase or force-push a shared/public branch** — only rebase local, unpushed, personal branches.
- **Only amend commits that haven't been pushed.**
- `git clean` deletes files **permanently** — no reflog safety net. Always run `-n` (dry run) first.
- `.gitignore` does **not** remove files that are already tracked — you must `git rm --cached` them first.
- `git stash` does **not** include untracked/ignored files by default — use `-u` or `-a`.
- `reset --hard` is destructive to the working directory; `revert` is the safe, shareable alternative.
- Reflog entries expire after **~90 days** — it's a safety net, not permanent storage.
- The first push of a new branch needs `-u`/`--set-upstream`, or Git won't know where to push.
- Fast-forward merges don't create a merge commit — use `--no-ff` if you want to preserve that a feature branch existed.
- A merge commit has two parents — when cherry-picking a merge commit, you must specify `-m 1` or `-m 2` to pick a side.
- Detached HEAD commits are easy to lose — `git switch -c <branch>` immediately if you want to keep them.
- `git checkout` is overloaded (branches + files); prefer `git switch` (branches) and `git restore` (files) for clarity and safety.
- Force-push safely with `--force-with-lease` (fails if someone else pushed since your last fetch), not plain `--force`.
