'''
Files, command-line scripts and automation
(learned while building scripts/token_tools/token_tools.py and scripts/codemap/codemap.py)
'''

'''
pathlib: paths as objects

from pathlib import Path
p = Path("notes") / "file.txt"          # / joins path parts
Path(__file__).resolve().parents[2]     # __file__ = this script's own path; parents[2] = two folders up
                                        # finds the repo root from the script's location, works from any folder
p.exists()  p.is_file()                 # True / False
p.read_text(encoding="utf-8")           # whole file as a string
p.write_text(text, encoding="utf-8")    # create / overwrite
p.with_name("x.md")  p.with_suffix(".tmp")   # same folder, new file name / new extension
p.relative_to(root).as_posix()          # path relative to root, written with / on every OS
p.parent.mkdir(parents=True, exist_ok=True)  # create the folder (and parents), no error if it exists
'''

'''
Reading and writing files

with open(path, "a", newline="", encoding="utf-8") as f:     # "r" read, "w" overwrite, "a" append
    ...                                                      # with = the file closes automatically
    # newline="" is the csv module's requirement, stops blank lines appearing on Windows
    # encoding "utf-8-sig" = utf-8 that drops the invisible BOM mark some editors put at the start

import csv
writer = csv.DictWriter(f, fieldnames=["a", "b"]);  writer.writeheader();  writer.writerow({"a": 1, "b": 2})
rows = list(csv.DictReader(f))          # each row is a dict; all values are strings, convert with int()

Safe overwrite (atomic write):
    temp.write_text(text);  os.replace(temp, target)    # a reader sees the old file or the new one, never half of one

import os
for folder, subfolders, filenames in os.walk(root):     # visits every folder under root
    subfolders[:] = [s for s in subfolders if s not in SKIP]    # editing the list in place stops os.walk entering them
'''

'''
argparse: command-line options

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", type=Path)      # no dashes = positional; nargs="*" = zero or more
parser.add_argument("--text")                            # with dashes = optional, value follows
parser.add_argument("--watch", action="store_true")     # a flag: True if given, False if not
parser.add_argument("--percentile", type=float, default=95)
args = parser.parse_args();  args.percentile

Subcommands (like git add / git commit):
    sub = parser.add_subparsers(dest="command", required=True)
    p_count = sub.add_parser("count");  p_count.set_defaults(func=run_count)
    args.func(args)                    # set_defaults(func=...) stores a function, so the chosen command runs its own function
'''

'''
Tokens and pip

pip install tiktoken       # installs a library from the internet, once
tiktoken                   # OpenAI's tokenizer: splits text into the pieces a model counts and bills (about 3/4 of a word each)
                           # exact for OpenAI models, an estimate for Claude and Gemini (they tokenize differently)
chars per token = len(text) / tokens        # measure it on your own text instead of assuming 4
'''

'''
Percentile, nearest-rank method

import math
ordered = sorted(values)
rank = math.ceil(pct / 100 * len(ordered))
value = ordered[rank - 1]                 # list positions start at 0, rank starts at 1
    # 6 values at the 95th percentile: ceil(0.95 * 6) = 6 -> the 6th (largest) value
    # use: pick a max_tokens cap that 95% of your replies already fit under
'''

'''
ast: reading Python code without running it

import ast
tree = ast.parse(source_text)             # source -> tree of nodes; raises SyntaxError if the code is invalid
for node in tree.body:                    # tree.body = the top-level statements
    isinstance(node, ast.FunctionDef)     # is this node a def? (ast.AsyncFunctionDef, ast.ClassDef likewise)
    node.name  node.lineno                # its name, the line it starts on
    ast.unparse(node.args)                # the parameter list written back as text: "self, amount, note=None"
    # a class node has its own .body holding its methods: a tree inside a tree (see graphs_and_trees_notes.py)
'''

'''
Watching for changes (polling) and choosing the wait

path.stat().st_mtime_ns, path.stat().st_size     # last-modified time (nanoseconds) and size; they change when a file is edited
time.sleep(seconds)                               # pause
time.perf_counter()                               # precise stopwatch: end - start = how long something took

Do not guess the wait between checks, derive it:
    interval = scan_time / cpu_budget
    # scan 4 ms, budget 0.01 (1% of one CPU core) -> wait 0.4 s
    # a slower scan automatically waits longer, so the load stays at about the budget
Take the snapshot BEFORE doing the work, so a file edited during the work is caught on the next round.
'''

'''
Running a script in the background on Windows

pythonw script.py          # like python, but no console window (print() output goes nowhere)
Startup folder (shell:startup): a shortcut placed there runs at every login
    # target: pythonw.exe   arguments: path/to/script.py --watch
'''

'''
subprocess: running another program from Python (from codemap.py and helper_server.py)

import subprocess
result = subprocess.run(["git", "ls-files", "-z"], cwd=folder, capture_output=True, text=True)
result.stdout  result.stderr  result.returncode     # output, error text, 0 = success
    # a list, not one string, so spaces in names cannot break the command
    # git ls-files --cached --others --exclude-standard = files git tracks + new files - .gitignore matches
    # -z separates names with a null character, so any file name splits correctly: output.split("\0")
creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
    # Windows only: no flashing console window; getattr(obj, name, default) returns the default if the name does not exist
'''

'''
MCP server (scripts/mcp_helper/helper_server.py)

MCP = Model Context Protocol: a standard way for an AI app to call tools in a program you write.
Claude Desktop starts the program itself and talks to it through stdin/stdout ("stdio").
    -> never print() in a stdio server, extra text on stdout breaks the conversation

server = MCPServer("name")
@server.tool()                  # a decorator: registers the function below as a tool
def read_lines(path: str, start: int, end: int) -> str:
    """This docstring becomes the tool description the AI sees (and is sent every turn: keep it short)."""
    # the type hints (str, int) become the tool's input schema
server.run()                    # stdio by default

try:
    from mcp.server import MCPServer                         # SDK 2.x
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer      # SDK 1.x: same code runs on both ("as" renames on import)

pip install "mcp>=1.28,<2"      # >=1.28,<2 = any 1.x from 1.28 up, but not 2.0 (version pinning)

Safe file access (path traversal):
    target = (REPO_ROOT / user_path).resolve()               # resolve() removes ../ and follows symlinks
    target.relative_to(REPO_ROOT.resolve())                  # raises ValueError if target is outside the repo
    # then also require the file to be in git's publishable list, so ignored/private files are refused

fnmatch.fnmatch("a/b.py", "*.py")    # shell-style wildcard match on a string (here * also matches /)
raw = open(path, "rb").read();  b"\0" in raw[:8000]    # binary check: git treats a NUL byte in the first 8000 bytes as binary
raw.decode("utf-8-sig", errors="replace")                # bad bytes become ? instead of crashing
'''

'''
re: regular expressions (build_portable.py repo_slug)

import re
m = re.search(r"github[.]com[:/](.+?)(?:[.]git)?$", url)    # r"..." = raw string: backslashes stay as written; [.] = a literal dot (same as an escaped dot)
m.group(1) if m else None          # search returns None when nothing matches, always check
    # . any character, [.] or a backslash-dot = a real dot   [:/] one of : or /   (...) capture group   (?:...) group, not captured
    # +? lazy (as few as possible)   ? optional   $ end of text
'''

'''
Decorators that wrap a function (helper_server.py logged)

import functools
def logged(function):
    @functools.wraps(function)           # copies name, docstring, type hints onto wrapper (MCP reads them)
    def wrapper(*args, **kwargs):        # *args/**kwargs = accept any arguments and pass them on
        ...before...
        result = function(*args, **kwargs)
        ...after...
        return result
    return wrapper                       # the decorator returns the new function that replaces the old one
@server.tool()
@logged
def f(): ...                             # stacked: logged wraps f first, then server.tool() registers the wrapped result
'''

'''
async / await (selftest.py)

import asyncio
async def main(): ...            # coroutine function: calling it only creates a coroutine
await something()                # run it and wait, letting other work happen meanwhile
asyncio.run(main())              # the single entry point that starts everything
async with open_connection() as c: ...    # with, where opening/closing needs await
await asyncio.wait_for(coro, 60)           # raises asyncio.TimeoutError if it takes over 60 s (how a hang is detected)
'''

'''
Small tools used across the scripts

from collections import defaultdict
groups = defaultdict(lambda: {"calls": 0, "total": 0})    # a missing key is created with this default instead of KeyError
sorted(d.items(), key=lambda item: item[1]["total"], reverse=True)    # sort by a chosen value, biggest first
sys.exit("message")              # stop the script, print the message to stderr, exit code 1 (no traceback)
for n, line in enumerate(lines, start=1):    # number the items from 1 (line numbers)
"x".startswith(("a", "b"))       # a tuple = true if it starts with any of them
text or "(none)"                 # `or` returns the right side when the left is empty/falsy

Full walkthrough of every script: scripts_walkthrough_notes.py (same folder).
'''
