"""
helper_server.py - a small local MCP server that gives Claude Desktop two cheap tools:

    search_code(query, glob)       find text across the repo, returns path:line: text
    read_lines(path, start, end)   return only the lines asked for

Why: the filesystem MCP can only read whole files (or the first/last N lines) and search by file
name. These tools let Claude find and read just the part it needs, which costs fewer tokens.

Safety rules (all enforced in code):
  * Only files git would publish are visible: tracked or new files minus .gitignore. So _local/,
    coursework and .env-style ignored files can never be read through this server.
  * Read-only. It cannot write, delete or run anything.
  * Every result is capped to a token budget, so one call can never flood the chat.

Claude Desktop starts this program itself (see the config snippet in scripts/mcp_helper/README.md).
Never print() in this file: for a stdio server, stdout is the channel to Claude, so extra text breaks it.
"""
import fnmatch
import functools
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    from mcp.server import MCPServer  # mcp 2.x
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer  # mcp 1.x

# <repo>/scripts/mcp_helper/helper_server.py -> repo root is 2 folders up.
REPO_ROOT = Path(__file__).resolve().parents[2]

# Measured with scripts/token_tools on AI-CONTEXT.md: 4439 characters = 1153 tokens.
# Estimate only: tiktoken is OpenAI's tokenizer, and code usually has fewer chars per token than prose.
CHARS_PER_TOKEN = 4439 / 1153  # = 3.85
# A choice, not a measurement: the most one tool result may cost. Change here to loosen or tighten.
RESULT_BUDGET_TOKENS = 1000
RESULT_BUDGET_CHARS = int(RESULT_BUDGET_TOKENS * CHARS_PER_TOKEN)  # = 3849
# A choice: at least this many matches should fit in one search result.
MIN_MATCHES_SHOWN = 20
# Longest single line shown in search results, so one huge line cannot use up the whole budget.
LINE_CHARS = RESULT_BUDGET_CHARS // MIN_MATCHES_SHOWN  # = 192
# git decides "binary file" by looking for a NUL byte in the first 8000 bytes; same rule here.
BINARY_CHECK_BYTES = 8000

server = MCPServer("foundations-helper")

# TEMPORARY debugging: _local/ is gitignored, so this log is never published. Remove when the
# Claude Desktop hang is solved.
DEBUG_LOG = REPO_ROOT / "_local" / "helper_debug.log"


def debug(message):
    """Append a timestamped line, to see whether (and where) Claude Desktop's calls reach this server."""
    try:
        DEBUG_LOG.parent.mkdir(exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} {message}\n")
    except OSError:
        pass  # logging must never break a tool call


def logged(function):
    """Decorator: log when a tool call arrives, how long it took, or the error it raised."""
    @functools.wraps(function)  # keeps the name, docstring and signature that MCP reads
    def wrapper(*args, **kwargs):
        debug(f"{function.__name__} received {kwargs or args}")
        started = time.perf_counter()
        try:
            result = function(*args, **kwargs)
        except Exception as error:
            debug(f"{function.__name__} raised {type(error).__name__}: {error}")
            raise
        debug(f"{function.__name__} returning {len(result)} chars after {time.perf_counter() - started:.2f} s")
        return result
    return wrapper


# ---------- helpers ----------

def publishable_files():
    """{repo-relative path with /: absolute Path} for every file git would publish."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        # stdin=DEVNULL: git must not inherit this server's stdin, which is the channel to Claude Desktop.
        cwd=REPO_ROOT, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace",
        # Windows only: stops a console window flashing on every call. getattr -> 0 elsewhere.
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode != 0:
        raise OSError(f"git ls-files failed: {result.stderr.strip()}")
    files = {}
    for name in result.stdout.split("\0"):  # -z separates names with a null character
        path = REPO_ROOT / name
        if name and path.is_file():  # skips files deleted but not yet committed
            files[name] = path
    return files


def read_text(path):
    """File text, or None if the file looks binary."""
    with open(path, "rb") as f:
        raw = f.read()
    if b"\0" in raw[:BINARY_CHECK_BYTES]:
        return None
    return raw.decode("utf-8-sig", errors="replace")


# ---------- tools ----------

@server.tool()
@logged
def search_code(query: str, glob: str = "") -> str:
    """Case-insensitive text search in the repo's git-publishable files. Returns path:line: text. glob filters paths, e.g. *.py"""
    if not query:
        return "Error: query is empty."
    try:
        files = publishable_files()
    except OSError as error:
        return f"Error: {error}"

    needle = query.lower()
    matches = []  # (path, line number, line text)
    for rel in sorted(files):
        if glob and not fnmatch.fnmatch(rel, glob):
            continue
        try:
            text = read_text(files[rel])
        except OSError:
            continue  # unreadable file: skip it
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if needle in line.lower():
                matches.append((rel, number, line.strip()))

    if not matches:
        return f"No matches for '{query}'" + (f" in {glob}" if glob else "") + "."

    out, used = [], 0
    for rel, number, line in matches:
        row = f"{rel}:{number}: {line[:LINE_CHARS]}"
        if out and used + len(row) + 1 > RESULT_BUDGET_CHARS:
            break  # always show at least one match
        out.append(row)
        used += len(row) + 1
    hidden = len(matches) - len(out)
    file_count = len({rel for rel, _, _ in matches})
    header = f"{len(matches)} matches in {file_count} files"
    if hidden:
        header += f" (showing {len(out)}; narrow with glob or a longer query for the other {hidden})"
    return header + "\n" + "\n".join(out)


@server.tool()
@logged
def read_lines(path: str, start: int, end: int) -> str:
    """Return lines start..end (1-based, inclusive) of one git-publishable file."""
    try:
        files = publishable_files()
        # resolve() makes the path absolute and removes any ../ so it can be checked against the repo.
        target = (REPO_ROOT / path).resolve()
        rel = target.relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return "Error: path is outside the repo."
    except OSError as error:
        return f"Error: {error}"
    if rel not in files:
        return f"Error: {rel} is not a git-publishable file (missing, ignored or private)."
    if start < 1 or end < start:
        return "Error: need 1 <= start <= end."
    try:
        text = read_text(target)
    except OSError as error:
        return f"Error: {error}"
    if text is None:
        return f"Error: {rel} looks like a binary file."

    lines = text.splitlines()
    if start > len(lines):
        return f"Error: {rel} has only {len(lines)} lines."
    last = min(end, len(lines))

    out, used, cut_line = [], 0, False
    for number in range(start, last + 1):
        line = lines[number - 1]
        if out and used + len(line) + 1 > RESULT_BUDGET_CHARS:
            break  # always return at least one line
        if len(line) > RESULT_BUDGET_CHARS:
            cut_line = True  # a single line bigger than the whole budget
        out.append(line[:RESULT_BUDGET_CHARS])
        used += len(line) + 1
    shown_end = start + len(out) - 1
    header = f"{rel} lines {start}-{shown_end} of {len(lines)}"
    if shown_end < last:
        header += f" (stopped at the size cap; call again with start={shown_end + 1})"
    if cut_line:
        header += " (one very long line was cut at the size cap)"
    return header + "\n" + "\n".join(out)


if __name__ == "__main__":
    debug(f"started: python={sys.executable} cwd={os.getcwd()} git={shutil.which('git')}")
    server.run()  # stdio is the default transport in both SDK versions
