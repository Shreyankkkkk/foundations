"""
token_tools.py - Phase 0 of the token-saving plan: measure before optimizing.

Run from the Foundations folder:
    python scripts/token_tools/token_tools.py count AI-CONTEXT.md README.md
    python scripts/token_tools/token_tools.py count --text "any text"
    python scripts/token_tools/token_tools.py log --label research --model gemini --input 1200 --output 800
    python scripts/token_tools/token_tools.py report

Setup once: pip install tiktoken
Note: tiktoken is OpenAI's tokenizer. Claude and Gemini tokenize differently,
so counts are estimates for them. Use the real numbers an API reports when you have them.
"""
import argparse
import csv
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# This file lives at <repo>/scripts/token_tools/token_tools.py, so the repo root is 2 folders up.
REPO_ROOT = Path(__file__).resolve().parents[2]
# _local/ is in .gitignore, so the log is never published.
DEFAULT_LOG = REPO_ROOT / "_local" / "token_log.csv"
FIELDS = ["timestamp", "label", "model", "input_tokens", "output_tokens"]
# Tokenizer used by recent OpenAI models. A choice, not a measurement; change with --encoding.
DEFAULT_ENCODING = "o200k_base"


# ---------- count ----------

def count_tokens(text, encoding_name=DEFAULT_ENCODING):
    """Return how many tokens `text` is split into."""
    try:
        import tiktoken
    except ImportError:
        sys.exit("tiktoken is not installed. Run: pip install tiktoken")
    try:
        encoding = tiktoken.get_encoding(encoding_name)
    except ValueError:
        sys.exit(f"Unknown encoding: {encoding_name}")
    # disallowed_special=() makes text like "<|endoftext|>" count as normal text instead of crashing.
    return len(encoding.encode(text, disallowed_special=()))


def run_count(args):
    items = []  # list of (name, text)
    for path in args.files:
        if not path.is_file():
            sys.exit(f"Not a file: {path}")
        items.append((str(path), path.read_text(encoding="utf-8")))
    if args.text is not None:
        items.append(("(text)", args.text))
    if not items:
        sys.exit("Give at least one file or --text.")

    total = 0
    for name, text in items:
        tokens = count_tokens(text, args.encoding)
        total += tokens
        # chars per token is calculated from this text, not assumed
        ratio = f"{len(text) / tokens:.2f}" if tokens else "n/a"
        print(f"{name}: {tokens} tokens | {len(text)} chars | {len(text.split())} words | {ratio} chars/token")
    if len(items) > 1:
        print(f"TOTAL: {total} tokens")


# ---------- log ----------

def log_call(label, model, input_tokens, output_tokens, log_path=DEFAULT_LOG):
    """Append one row to the CSV. Later, API code can import and call this after each request."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not log_path.exists()
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "label": label,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        })


def run_log(args):
    if args.input_tokens < 0 or args.output_tokens < 0:
        sys.exit("Token counts cannot be negative.")
    log_call(args.label, args.model, args.input_tokens, args.output_tokens, args.file)
    print(f"Logged to {args.file}")


# ---------- report ----------

def read_log(log_path):
    if not Path(log_path).is_file():
        sys.exit(f"No log yet at {log_path}. Add rows with the 'log' command first.")
    with open(log_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["input_tokens"] = int(row["input_tokens"])
        row["output_tokens"] = int(row["output_tokens"])
    if not rows:
        sys.exit("The log has no rows yet.")
    return rows


def percentile(values, pct):
    """Nearest-rank method: sort, then take the value at position ceil(pct/100 * n)."""
    ordered = sorted(values)
    rank = math.ceil(pct / 100 * len(ordered))
    return ordered[rank - 1]


def run_report(args):
    if not 0 < args.percentile <= 100:
        sys.exit("--percentile must be above 0 and at most 100.")
    rows = read_log(args.file)

    grand_total = sum(r["input_tokens"] + r["output_tokens"] for r in rows)
    total_in = sum(r["input_tokens"] for r in rows)
    total_out = sum(r["output_tokens"] for r in rows)
    print(f"{len(rows)} calls | {grand_total} tokens total")
    print(f"input {total_in} ({total_in / grand_total * 100:.1f}%) | output {total_out} ({total_out / grand_total * 100:.1f}%)")

    # Token sinks: total tokens per label, biggest first.
    by_label = defaultdict(lambda: {"calls": 0, "total": 0})
    for r in rows:
        by_label[r["label"]]["calls"] += 1
        by_label[r["label"]]["total"] += r["input_tokens"] + r["output_tokens"]
    print("\nTop token sinks (by label):")
    for label, d in sorted(by_label.items(), key=lambda item: item[1]["total"], reverse=True):
        print(f"  {label}: {d['total']} tokens, {d['total'] / grand_total * 100:.1f}% of all, "
              f"{d['calls']} calls, {d['total'] / d['calls']:.0f} per call")

    # max_tokens suggestion, derived from your own replies.
    outputs = [r["output_tokens"] for r in rows]
    cap = percentile(outputs, args.percentile)
    cut = sum(1 for o in outputs if o > cap)
    print(f"\nReply length: average {sum(outputs) / len(outputs):.0f}, longest {max(outputs)} tokens, over {len(outputs)} replies")
    print(f"max_tokens suggestion: {cap} (the {args.percentile:g}th percentile of your replies, nearest-rank method)")
    print(f"With that cap, {cut} of {len(outputs)} logged replies would have been cut off.")
    print("Small sample = unreliable. Keep logging, and check the cut replies before applying a cap.")


# ---------- command line ----------

def build_parser():
    parser = argparse.ArgumentParser(description="Measure token usage.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_count = sub.add_parser("count", help="count tokens in files or text")
    p_count.add_argument("files", nargs="*", type=Path, help="one or more files")
    p_count.add_argument("--text", help="count this text instead of (or as well as) files")
    p_count.add_argument("--encoding", default=DEFAULT_ENCODING)
    p_count.set_defaults(func=run_count)

    p_log = sub.add_parser("log", help="add one row to the usage log")
    p_log.add_argument("--label", required=True, help="task type, e.g. research, file-edit")
    p_log.add_argument("--model", required=True)
    p_log.add_argument("--input", type=int, required=True, dest="input_tokens")
    p_log.add_argument("--output", type=int, required=True, dest="output_tokens")
    p_log.add_argument("--file", type=Path, default=DEFAULT_LOG, help="CSV path")
    p_log.set_defaults(func=run_log)

    p_report = sub.add_parser("report", help="show top token sinks and a max_tokens suggestion")
    p_report.add_argument("--percentile", type=float, default=95,
                          help="share of replies that should fit under the cap (your choice)")
    p_report.add_argument("--file", type=Path, default=DEFAULT_LOG, help="CSV path")
    p_report.set_defaults(func=run_report)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
