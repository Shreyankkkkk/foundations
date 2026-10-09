# mcp_helper

A small local MCP server for Claude Desktop with two read-only tools:

| Tool | What it does |
|---|---|
| `search_code(query, glob)` | text search inside the repo's files, returns `path:line: text` |
| `read_lines(path, start, end)` | returns only lines `start`-`end` of one file |

Why: the filesystem MCP reads whole files and matches file *names* only, so finding one function costs a whole-file read. Measured cost of these two tool definitions: about 195 tokens per turn (estimate: 752 characters / 3.85 chars per token).

Safety: only files git would publish are visible (`.gitignore` is respected, so `_local/`, coursework and ignored secrets cannot be read), read-only, every result capped at about 1000 tokens. Limits live at the top of `helper_server.py`.

## Setup (once per computer)
1. Install the SDK (pinned to 1.x, the version known to work with Claude Desktop; the code also runs on 2.x):
   ```
   pip install "mcp>=1.28,<2"
   ```
2. Print the two values the config needs, already escaped for JSON:
   ```
   (Get-Command python).Source -replace '\\','\\\\'
   python --version
   ```
   The Python version must be 3.10 or newer.
3. Open `%APPDATA%\Claude\claude_desktop_config.json`. Inside the existing `"mcpServers": { ... }` block, next to the `foundations` entry, add (keep the comma between entries):
   ```json
   "foundations-helper": {
     "command": "<python path from step 2>",
     "args": ["C:\\Users\\Shreyank\\Documents\\Development\\Foundations\\scripts\\mcp_helper\\helper_server.py"]
   }
   ```
4. Fully quit and restart Claude Desktop. In a new chat, open the connectors list: `foundations-helper` should show `search_code` and `read_lines`.

## If it does not show up
- Read `%APPDATA%\Claude\logs\mcp-server-foundations-helper.log` (errors from the server) and `mcp.log`.
- Run it by hand: `python scripts\mcp_helper\helper_server.py`. It should sit silently waiting (Ctrl+C to stop). An `ImportError` means step 1 was run for a different Python than step 2.
- Try the other SDK line: `pip install -U mcp` (2.x). No code change needed.

## Remove
Delete the `foundations-helper` entry from the config and restart Claude Desktop.
