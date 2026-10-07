# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Automate Repeat Work

---

## Lesson 1 : Routines and Headless

---

### Core Idea

Once a task is reliable enough to trust, automate it instead of manually starting it every time.

There are two main approaches:

1. **Routines** — managed automation with little/no infrastructure.
2. **Headless mode / Agent SDK** — automation controlled by your own scripts or applications.

---

### 1. Routines

A **routine** is a saved prompt that runs automatically.

It combines:

- A prompt
- A repository
- Connectors
- A trigger

The infrastructure runs on Anthropic's side, so you don't need your own machine running continuously.

#### Possible triggers

- Cron schedule
- HTTP POST
- GitHub events

#### Good use cases

- Daily dependency audits
- PR review/triage
- Recurring repository checks
- Regular issue/ticket analysis

#### Creating a routine

From the web:

```text
claude.ai/code/routines
```

Or from Claude Code:

```text
/schedule daily dependency audit at 9am
```

#### Important limitations

- Routines are a **research preview**.
- Recurring schedules run at most **hourly**.
- Each run starts from a fresh clone of the default branch.
- By default, routines can only push to branches beginning with:

```text
claude/
```

---

### 2. Headless Mode

Headless mode allows Claude Code to run without the interactive UI.

The main flag is:

```bash
-p
```

or:

```bash
--print
```

Example:

```bash
claude -p "summarize the changes in this diff"
```

This makes Claude behave more like a normal command-line program:

```text
input → Claude → output
```

#### Important

`-p` does **not** automatically discover:

- Hooks
- Skills
- Plugins
- MCP servers
- CLAUDE.md

You explicitly control what the headless run gets.

The benefit is faster and more predictable startup.

---

### 3. Structured Output

Headless Claude can return structured JSON instead of only normal text.

You can provide a JSON schema:

```bash
claude -p "Extract the exported function names from src/core/style.js" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

The resulting structured data appears in:

```text
structured_output
```

You can extract it with:

```bash
jq
```

Example:

```bash
... | jq '.structured_output.functions'
```

This allows Claude's output to be passed directly into:

- Scripts
- Databases
- Other programs
- Automation pipelines

---

### 4. Resuming Sessions

Longer automation doesn't have to happen in one command.

Claude can return a session ID.

Save that ID and resume the session later:

```bash
claude --resume "$(jq -r .session_id /tmp/plan.json)"
```

This allows automation to happen in multiple stages.

Example:

```text
Script 1
    ↓
Claude creates a plan
    ↓
Session ID saved
    ↓
Script 2
    ↓
Resume same session
    ↓
Claude implements the plan
```

---

### 5. `--bare`

`--bare` is intended for deterministic CI runs.

Use it when you want Claude Code inside a pipeline to have predictable, repeatable behavior.

```bash
claude --bare
```

---

### 6. Agent SDK

The Agent SDK allows you to put Claude Code inside your own application.

It is available for:

- TypeScript
- Python

It provides a `query` function and allows you to control things such as:

- `allowedTools`
- System prompt
- Permission mode

Your application can then process Claude's streamed messages and decide what to do with them.

Conceptually:

```text
Your Python/TypeScript application
            ↓
       Agent SDK
            ↓
        Claude
            ↓
     Tool execution
            ↓
      Your application
```

---

### 7. Choosing the Right Method

| Method | Use when |
|---|---|
| **Routines** | You have a recurring task and want the simplest automation |
| **Headless `-p`** | You want Claude inside your own scripts/pipelines |
| **`--bare`** | You need predictable CI runs |
| **Agent SDK** | You want Claude integrated directly into your own application |

### Mental Model

```text
Simple recurring task
        ↓
     Routines
        ↓
Need your own scripts/environment?
        ↓
    Headless -p
        ↓
Need deterministic CI?
        ↓
      --bare
        ↓
Need Claude inside your own application?
        ↓
    Agent SDK
```

### Key Takeaway

**Start with routines.**

Move to headless mode when you need your own scripts and environment.

Use `--bare` for deterministic CI.

Use the Agent SDK when Claude needs to become part of your own application.

---

### Video

[Automate Claude Code - Youtube](https://www.youtube.com/watch?v=b9TCW-pdzDA)

---

## Lesson 2 : Github Actions and Code Review

---

### Why Pull Requests Are Useful

Pull requests are a good place to automate repetitive work because they are where:

- Code review happens
- Changes are introduced
- Changes are merged
- A lot of development busywork occurs

There are two main ways to use Claude with pull requests:

1. **Code Review** — managed by Anthropic
2. **GitHub Action** — custom automation that you configure

---

### 1. Code Review

#### What It Is

**Code Review** is an Anthropic-hosted service that reviews GitHub pull requests through the Claude GitHub app.

You do not need to build or host anything.

Claude:

- Reviews the pull request
- Analyzes the diff against the full codebase
- Finds potential issues
- Posts inline comments on relevant lines
- Ranks findings by severity
- Provides a summary of findings

#### Setup

An organization admin enables Code Review through the Claude Code admin settings.

General process:

1. Open Claude Code admin settings.
2. Find **Code Review**.
3. Select **Configure**.
4. Install the Claude GitHub app.
5. Select the repositories to monitor.
6. Choose when reviews should run.

#### Review Triggers

Code Review can run:

- Once when a PR opens
- On every push to the PR
- When someone comments `@claude review`

#### What Claude Reviews

Claude analyzes the changes against the **full codebase**, rather than looking only at the changed lines in isolation.

Findings are posted as inline comments on the relevant lines.

The findings are:

- Ranked
- Deduplicated
- Tagged by severity
- Accompanied by a summary table

#### What Code Review Does NOT Do

Code Review:

- Does **not** approve PRs
- Does **not** block PRs
- Does **not** automatically fix findings

A human still makes the final decision.

#### Local Fixes

The `/code-review` command can review a diff locally.

Use:

```bash
/code-review --fix
```

to apply the findings to the working tree.

Typical workflow:

```text
PR
 ↓
Claude Code Review
 ↓
Findings posted to PR
 ↓
Pull changes locally
 ↓
/code-review --fix
 ↓
Review changes
```

---

### 2. GitHub Action

#### What It Is

The GitHub Action is the customizable option.

Use it when Claude needs to **do something**, rather than simply review a PR.

Examples:

- Implement changes from a PR comment
- Respond to `@claude`
- Generate reports
- Run scheduled tasks
- Automate other CI workflows
- React to GitHub events

The action runs inside GitHub Actions.

#### Setup

Inside Claude Code, run:

```bash
/install-github-app
```

You need repository admin permissions.

The setup walks through:

- Installing the GitHub app
- Configuring the repository
- Setting the Anthropic API key secret

The action is:

```yaml
anthropics/claude-code-action@v1
```

---

### GitHub Action Inputs

Important inputs include:

##### `anthropic_api_key`

The Anthropic API key.

Optional depending on the configuration.

##### `github_token`

GitHub authentication token.

Defaults to:

```yaml
secrets.GITHUB_TOKEN
```

##### `trigger_phrase`

The phrase that causes the action to run.

Default:

```text
@claude
```

##### `use_bedrock`

Use Amazon Bedrock instead of the Anthropic API.

##### `use_vertex`

Use Google Vertex instead of the Anthropic API.

##### `prompt`

The instructions Claude should follow.

##### `claude_args`

CLI arguments passed directly to Claude Code.

---

### GitHub Action: `@claude` Workflow

Create:

```text
.github/workflows/claude.yaml
```

Example:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}
    trigger_phrase: "@claude"
    prompt: "Your instructions here"
    claude_args: "--max-turns 5 --model claude-sonnet-5"
```

Now a user can comment:

```text
@claude implement the spec in the linked Linear issue
```

Claude can then:

- Pick up the request
- Make changes
- Push commits
- Post comments explaining what it did

---

### Scheduled GitHub Action

The same action can run on a schedule.

For example:

```text
Cron trigger
     ↓
GitHub Action
     ↓
Claude
     ↓
Generate report
     ↓
Post results
```

You can also add:

```yaml
workflow_dispatch
```

to allow manually starting the workflow from GitHub Actions.

Runs can be monitored through the **Actions** tab.

---

### `claude_args`

`claude_args` controls how Claude Code runs.

#### `--max-turns`

Limits the number of agent turns.

Example:

```bash
--max-turns 5
```

This prevents an agent from running indefinitely.

#### Permission Mode

For unattended jobs, Claude cannot stop and wait for a human approval.

Use an appropriate non-interactive permission mode.

#### Allowed Tools

Give the workflow only the tools it actually needs.

For example:

##### Report generation

Use read-only tools.

##### Code modification

Allow the tools necessary to edit and commit code.

Principle:

> Give an automated job exactly what it needs and nothing more.

---

### Code Review vs GitHub Action

| Feature | Code Review | GitHub Action |
|---|---|---|
| Managed by Anthropic | Yes | No |
| Requires custom workflow | No | Yes |
| Main purpose | PR review | Custom automation |
| Posts review findings | Yes | Can |
| Automatically modifies code | No | Yes |
| Responds to `@claude` | Review trigger | Yes |
| Scheduled jobs | No | Yes |
| Custom prompts | Limited | Yes |
| Custom CI workflows | No | Yes |
| Infrastructure | Anthropic | GitHub Actions |

---

### Which One To Use

#### Use Code Review when:

- You want PR reviews
- You want inline findings
- You don't want to maintain workflows
- You want Claude to identify problems but leave the final decision to a human

#### Use GitHub Actions when:

- Claude needs to actually modify code
- You need custom automation
- You want `@claude` commands
- You need scheduled jobs
- You want Claude integrated into CI
- You need control over tools and CLI options

#### Simple Rule

```text
PR review
    ↓
Code Review

Anything beyond review
    ↓
GitHub Action
```

Start with **Code Review** for simple PR review.

Move to the **GitHub Action** when you need Claude to actually perform work in CI.

---

### Video

[Claude Code on Pull Requests - Youtube](https://www.youtube.com/watch?v=gIVt_iqmACw)

---

# Verify and Share

---

## Lesson 1 : Trust it - Verifying Unsupervised Runs

---

### Core Principle

> The less you watched the run, the more you verify afterward.

Verification should scale with how unsupervised the run was:

- Short, supervised run → quick review
- Long, hands-off run → thorough verification
- CI / unattended run → full verification process

---

### Keep Unattended Runs in Auto Mode

- Use **Auto mode** for unattended work.
- Avoid **Bypass Permissions** unless running inside an isolated container or VM.
- Auto mode uses a classifier to review actions for potentially dangerous behavior.

#### Important

The classifier checks **dangerous intent**, not whether the code is correct.

Therefore:

> Auto mode is a safety layer, not a correctness check.

You still need proper verification.

---

### Start With the Diff, Not Claude's Summary

Do not trust the completion summary as proof that the work is correct.

#### Verification order

1. Run `/code-review`
2. Review the findings
3. Run `git diff`
4. Read the actual changes
5. Check that only expected files were modified
6. Compare the changes against the original task/plan

#### Why?

A summary can say:

> "Implemented the requested changes."

while the actual diff may contain:

- Unexpected files
- Unnecessary changes
- Incorrect logic
- Accidental deletions
- Changes outside the original scope

The diff is the source of truth.

---

### Turn Tests Into a Gate

Do not rely on Claude saying:

> "All tests passed."

Make verification automatic.

#### Useful hooks

##### Stop Hook

- Runs tests when Claude attempts to finish.
- Prevents the turn from ending if tests fail.
- Can feed the failure back to Claude so it can fix the problem.

##### PostToolUse Hook

Can automatically run:

- Linting
- Type checking
- Formatting
- Other checks after edits

#### Important Exit Code

Use:

```bash
exit 2
```

to block the action/turn and feed the failure back to Claude.

This makes the check happen automatically instead of relying on you to remember to ask.

---

### Get a Cold Second Opinion

For important or unattended work:

1. Start a fresh Claude session or sub-agent.
2. Give it the changed code.
3. Ask it to review the implementation.
4. Do not give it the original session's reasoning/history if possible.

#### Why?

A fresh reviewer:

- Has no attachment to the original approach.
- Has not seen the previous reasoning.
- Can identify problems the original agent overlooked.
- Provides an independent perspective.

> The original agent may rationalize its own decisions. A fresh reviewer does not have that context.

---

### Verify Headless Runs

For headless Claude Code runs:

- Check the JSON output.
- Check the process exit code.
- Do not rely only on Claude's textual response.
- Confirm that the expected checks actually ran.

---

### Verification Checklist

- [ ] Keep unattended runs in **Auto mode**
- [ ] Do not use **Bypass Permissions** outside isolated environments
- [ ] Run `/code-review`
- [ ] Read `git diff` yourself
- [ ] Check for unexpected file changes
- [ ] Compare changes against the original task/plan
- [ ] Run tests
- [ ] Use a **Stop hook** to enforce tests
- [ ] Use **PostToolUse hooks** for linting/type checking where useful
- [ ] Use `exit 2` when a hook must block progress
- [ ] Check JSON output and exit codes for headless runs
- [ ] Get a fresh second opinion for important changes

---

### Bottom Line

> "Claude did it while I wasn't looking" should never mean "I trust that it worked."

Use:

**Auto mode → Diff review → Automated tests → Hooks → Fresh second opinion**

The less you supervised the run, the stronger the verification should be.

---

### Video

[How to Trust Claude Code Run - Youtube](https://www.youtube.com/watch?v=lalGZSNhm8E)

---

## Lesson 2 : Plugins

---

### Why Plugins Exist

A good `.claude` setup becomes more valuable when an entire team can use it.

Without plugins, teams may have to:

- Copy `.claude` directories between machines
- Manually share skills
- Manually share subagents
- Manually share hooks
- Keep everything synchronized themselves

**Plugins package the setup into one installable unit.**

---

### What a Plugin Is

A plugin can bundle:

- Skills
- Subagents
- Hooks
- MCP server configurations
- Language Server Protocol servers
- Background monitors
- Themes
- Certain `settings.json` configuration

The goal is:

> One version → one install → shared setup

#### Installing a Plugin

```text
/plugin install org-name@plugin-name
```

After installation, Claude Code may ask you to run:

```text
/reload-plugins
```

to apply the changes.

---

### Marketplaces

A marketplace is a shared source from which plugins can be discovered and installed.

#### Add a Marketplace

```text
/plugin marketplace add your-org/claude-plugins
```

#### Benefits

A team marketplace provides:

- Centralized plugin discovery
- Version tracking
- Easier updates
- One shared source for the team

Plugins can then be browsed through the **Discover** tab.

---

### Security: Read Before Installing

A plugin runs code on your machine using your privileges.

This means a plugin can contain things such as:

- `PreToolUse` hooks
- `Stop` hooks
- MCP servers
- Subagents
- Skills
- Other executable behavior

#### Important

Installing a plugin means accepting **all of its components**, not just the skill or feature you wanted.

For example, a plugin could contain a hook that runs whenever a particular tool is used.

Therefore:

> Never blindly install a plugin just because its description looks useful.

#### Before Installing

Check:

- What hooks it contains
- What agents/subagents it contains
- What MCP servers it uses
- What code it executes
- What context cost it has
- What permissions it requires

Claude Code shows information about what a plugin will install and its estimated context cost.

#### Trust

Anthropic does not necessarily control the contents of third-party plugins.

Automated review ≠ guaranteed safety.

Only install plugins and marketplaces from sources you trust.

---

### Where Plugins Come From

There are different sources for plugins.

#### Community Marketplace

- Uses an in-app submission process
- Goes through automated review

#### Official Marketplace

- Curated separately

#### Important

> Reviewed does not mean automatically trustworthy.

Always inspect the plugin yourself.

---

### Plugin Components Run Alongside Your Own

Plugins generally do not replace your existing configuration.

Their components run alongside yours.

### Hooks

Hooks **stack**.

For example:

```text
Your PreToolUse hook
        +
Plugin PreToolUse hook
        ↓
Both execute
```

A plugin hook does not automatically replace your hook.

This is another reason to inspect plugins before installing them.

---

### Namespacing

Plugin components are namespaced so they do not normally conflict with your own components.

Skills, agents, and commands use the plugin's namespace.

Example:

```text
company-name:skill-name
```

This helps prevent naming conflicts.

---

### Plugin `settings.json`

A plugin can include a `settings.json`, but only certain settings are honored.

The relevant keys are:

- Agent status line
- Subagent status line

#### Important: Agent Setting

A plugin can promote one of its subagents to the main thread.

This can change:

- The system prompt
- Available tools
- Model
- Default behavior

Therefore:

> Enabling a plugin can change how Claude Code behaves by default.

---

### Managing Plugins

After installation, you can:

- View installed plugins
- See what they added
- Manage plugins
- Uninstall plugins

---

### Creating Your Own Plugin

Once your `.claude` setup works well, package it instead of manually copying it between machines.

A plugin uses the same basic `.claude` structure you're already familiar with.

#### Typical Structure

```text
plugin/
├── agents/
│   ├── reviewer.md
│   └── researcher.md
│
├── skills/
│   ├── verification/
│   │   └── skill.md
│   └── testing/
│       └── skill.md
│
├── hooks/
│   └── hooks.json
│
├── .mcp.json
│
└── .claude-plugin/
    └── plugin.json
```

#### Components

- One folder per skill
- One Markdown file per subagent under `agents`
- `hooks/hooks.json` at the plugin root
- `.mcp.json` at the plugin root

Claude Code discovers components based on these conventions.

---

### Plugin Manifest

An optional manifest can be placed at:

```text
.claude-plugin/plugin.json
```

Example:

```json
{
  "name": "svg-splitter-review",
  "version": "0.1.0",
  "description": "Reviews the SVG Splitter repo",
  "author": {
    "name": "Lewis Menelaws"
  }
}
```

### Manifest Fields

#### `name`

The only required field.

It also provides the namespace for plugin components.

Example:

```text
company-name:skill-name
```

#### `version`

Use versioning so updates can be tracked across the team.

#### `description`

Describes what the plugin does.

#### `author`

Identifies the creator.

---

### Plugin Rules

#### When Using Plugins

- [ ] Read the plugin before installing it
- [ ] Inspect its hooks
- [ ] Inspect its agents/subagents
- [ ] Inspect its MCP servers
- [ ] Check what code it executes
- [ ] Check its context cost
- [ ] Only install trusted plugins
- [ ] Remember that plugin hooks run alongside your own hooks

#### When Creating Plugins

- [ ] Package a working `.claude` setup
- [ ] Keep skills in `skills/`
- [ ] Keep subagents in `agents/`
- [ ] Keep hooks in `hooks/hooks.json`
- [ ] Keep MCP configuration in `.mcp.json`
- [ ] Add `.claude-plugin/plugin.json`
- [ ] Give the plugin a unique name
- [ ] Version the plugin
- [ ] Share it through a trusted marketplace

---

### Bottom Line

**Using plugins:**

> Read before you install.

**Creating plugins:**

> Package your `.claude` setup once it works.

The goal is:

**One installable unit → consistent setup → easier team sharing**

---

### Video

[Claude Code Plugins - Youtube](https://www.youtube.com/watch?v=k4kZwJ0FtX0)

---