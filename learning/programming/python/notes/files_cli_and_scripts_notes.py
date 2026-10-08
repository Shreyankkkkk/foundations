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
