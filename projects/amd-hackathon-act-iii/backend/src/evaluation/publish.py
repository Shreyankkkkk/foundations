"""publish.py: the gate between a finished REAL run and the demo.

Run from backend/ on the AMD machine, after the pipeline and the benchmark:
    python -m src.evaluation.publish --price-per-hour 1.99      checks, then copies
    python -m src.evaluation.publish --check-only               checks, copies nothing

What it does, in this order:
  1. Checks every file against the data contract (fields, types, ids, and that
     every flag's quote really is in its note).
  2. Checks the run was REAL: not the pretend model, a judge model and notes per
     minute recorded, no failed notes, every note processed, benchmark made from
     these same flags. Any problem stops it before anything is copied.
  3. Builds output/amd.json from run_stats.json. cost_per_1000_notes is only
     filled when --price-per-hour is given. The Evolus fields stay empty until
     there is a real Evolus integration to count.
  4. Copies sop, notes, flags, benchmark and amd (.json) to data/demo/ and to
     ../frontend/data/ (when that folder exists). The front end's saved
     decisions.json is moved to decisions.backup.json.

Nothing in here invents a number: every value is read from a file or calculated
from one.
"""

import argparse
import os
from datetime import datetime

from src import config
from src.evaluation.benchmark import DETAILS_FILE_NAME, load_json, real_run_problem, save_json
from src.stages.judge import DRIFT_TYPES
from src.stages.quote_check import quote_in_note

STEP_FIELDS = {"sop_id", "step_id", "title", "text"}
NOTE_FIELDS = {"note_id", "date", "shift", "source", "text"}
FLAG_FIELDS = {"flag_id", "sop_id", "step_id", "note_id", "date", "shift", "drift_type",
               "quote", "confidence", "status", "suggested_fix"}
BENCHMARK_FIELDS = {"precision", "recall", "quote_verified_rate", "notes_per_minute",
                    "matcher_model", "judge_model", "gpu", "false_alarms"}
STATUSES = ("pending", "approved", "rejected")


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_whole(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_text(value):
    return isinstance(value, str) and value.strip() != ""


def _is_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat() == value
    except (TypeError, ValueError):
        return False


def _is_share(value):
    return _is_number(value) and 0 <= value <= 1


def _wrong_fields(item, expected):
    """A message if item is not a dict with exactly the expected fields, else None."""
    if not isinstance(item, dict):
        return "is not an object"
    if set(item) != expected:
        missing, extra = sorted(expected - set(item)), sorted(set(item) - expected)
        return f"fields wrong (missing {missing}, extra {extra})"
    return None


def check_contract(sop, notes, flags, bench):
    """Every way the four files break the data contract, as a list of messages (empty = fine)."""
    problems = []

    steps = set()
    for i, step in enumerate(sop, 1):
        wrong = _wrong_fields(step, STEP_FIELDS)
        if wrong:
            problems.append(f"sop.json item {i}: {wrong}")
            continue
        if not (_is_text(step["sop_id"]) and _is_whole(step["step_id"]) and _is_text(step["title"]) and _is_text(step["text"])):
            problems.append(f"sop.json item {i}: sop_id, title and text must be text and step_id a whole number")
        key = (step["sop_id"], step["step_id"])
        if key in steps:
            problems.append(f"sop.json item {i}: {key[0]} step {key[1]} appears twice")
        steps.add(key)

    notes_by_id = {}
    for i, note in enumerate(notes, 1):
        wrong = _wrong_fields(note, NOTE_FIELDS)
        if wrong:
            problems.append(f"notes.json item {i}: {wrong}")
            continue
        if not all(_is_text(note[name]) for name in NOTE_FIELDS):
            problems.append(f"notes.json item {i}: every field must be non-empty text")
        if not _is_date(note["date"]):
            problems.append(f"notes.json item {i}: date must look like 2026-09-01")
        if note["note_id"] in notes_by_id:
            problems.append(f"notes.json item {i}: note_id {note['note_id']} appears twice")
        notes_by_id[note["note_id"]] = note

    flag_ids = set()
    for i, flag in enumerate(flags, 1):
        wrong = _wrong_fields(flag, FLAG_FIELDS)
        if wrong:
            problems.append(f"flags.json item {i}: {wrong}")
            continue
        label = f"flags.json item {i} ({flag['flag_id']})"
        if not _is_text(flag["flag_id"]) or flag["flag_id"] in flag_ids:
            problems.append(f"{label}: flag_id must be unique text")
        flag_ids.add(flag["flag_id"])
        if (flag["sop_id"], flag["step_id"]) not in steps:
            problems.append(f"{label}: no step {flag['sop_id']} {flag['step_id']} in sop.json")
        note = notes_by_id.get(flag["note_id"])
        if note is None:
            problems.append(f"{label}: no note {flag['note_id']} in notes.json")
        else:
            if (flag["date"], flag["shift"]) != (note["date"], note["shift"]):
                problems.append(f"{label}: date or shift differs from its note")
            if not quote_in_note(flag["quote"], note["text"]):
                problems.append(f"{label}: the quote is not word for word in the note")
        if flag["drift_type"] not in DRIFT_TYPES:
            problems.append(f"{label}: unknown drift_type {flag['drift_type']!r}")
        if not _is_share(flag["confidence"]):
            problems.append(f"{label}: confidence must be a number from 0 to 1")
        if flag["status"] not in STATUSES:
            problems.append(f"{label}: status must be pending, approved or rejected")
        if flag["suggested_fix"] is not None and not isinstance(flag["suggested_fix"], str):
            problems.append(f"{label}: suggested_fix must be text or null")

    wrong = _wrong_fields(bench, BENCHMARK_FIELDS)
    if wrong:
        problems.append(f"benchmark.json: {wrong}")
    else:
        for name in ("precision", "recall", "quote_verified_rate"):
            if not _is_share(bench[name]):
                problems.append(f"benchmark.json: {name} must be a number from 0 to 1 (it is {bench[name]!r})")
        if not (_is_number(bench["notes_per_minute"]) and bench["notes_per_minute"] > 0):
            problems.append("benchmark.json: notes_per_minute must be a number above 0")
        for name in ("matcher_model", "judge_model", "gpu"):
            if not _is_text(bench[name]):
                problems.append(f"benchmark.json: {name} must be filled (it is {bench[name]!r})")
        if not isinstance(bench["false_alarms"], list):
            problems.append("benchmark.json: false_alarms must be a list")
        else:
            for alarm in bench["false_alarms"]:
                alarm_id = alarm.get("flag_id") if isinstance(alarm, dict) else alarm
                if alarm_id not in flag_ids:
                    problems.append(f"benchmark.json: false alarm {alarm_id!r} is not a flag in flags.json")
    return problems


def check_real_run(stats, bench, details, flags, notes):
    """Everything that says this is NOT a finished, consistent real run, as a list of messages."""
    problem = real_run_problem(stats)
    if problem:
        return [problem]
    problems = []
    if isinstance(bench, dict) and stats["judge_model"] != bench.get("judge_model"):
        problems.append("benchmark.json names a different judge_model than run_stats.json: run the benchmark again")
    if stats.get("failed_note_ids"):
        problems.append(f"{len(stats['failed_note_ids'])} notes failed in the run ({stats['failed_note_ids'][:5]}...): run again")
    if stats.get("notes_done") != len(notes):
        problems.append(f"the run processed {stats.get('notes_done')} notes but notes.json has {len(notes)} (a --limit run, or stale files)")
    if stats.get("flags_kept") != len(flags):
        problems.append("flags.json does not match run_stats.json: it was changed or is from another run")
    if not details:
        problems.append(f"{DETAILS_FILE_NAME} is missing: run the benchmark first")
    elif details.get("flags_total") != len(flags):
        problems.append("benchmark.json was made from different flags than flags.json: run the benchmark again")
    return problems


def build_amd(stats, price_per_hour=None):
    """The front end's amd.json, from measured values only. Unknown stays None / empty."""
    cost = None
    notes_per_minute = stats.get("notes_per_minute")
    if price_per_hour is not None and notes_per_minute:
        # dollars per 1,000 notes = price per hour / notes per hour * 1,000
        # (counts the time the pipeline ran, not setup or idle time on the machine)
        cost = round(price_per_hour / (notes_per_minute * 60) * 1000, 4)
    return {
        # a saved file cannot know if the endpoint is up now; only a live server can say that
        "endpoint_status": "saved run",
        "cost_per_1000_notes": cost,
        "evolus_api_calls": None,  # no Evolus integration exists, so nothing was counted
        "evolus_blocks": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Check a real run and publish it to the demo folders.")
    parser.add_argument("--price-per-hour", type=float, default=None,
                        help="AMD machine price in dollars per hour (from the AMD console); gives cost_per_1000_notes")
    parser.add_argument("--check-only", action="store_true", help="run the checks, copy nothing")
    args = parser.parse_args()
    if args.price_per_hour is not None and args.price_per_hour <= 0:
        raise SystemExit("--price-per-hour must be above 0.")

    out = config.OUTPUT_DIR
    paths = {
        "flags": out / config.FLAGS_FILE.name,
        "stats": out / config.RUN_STATS_FILE.name,
        "benchmark": out / config.BENCHMARK_FILE.name,
        "details": out / DETAILS_FILE_NAME,
    }
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise SystemExit("Missing files (run the pipeline, then the benchmark):\n  " + "\n  ".join(missing))

    flags, stats = load_json(paths["flags"]), load_json(paths["stats"])
    bench, details = load_json(paths["benchmark"]), load_json(paths["details"])
    sop, notes = load_json(config.SOP_FILE), load_json(config.NOTES_FILE)

    problems = check_real_run(stats, bench, details, flags, notes) + check_contract(sop, notes, flags, bench)
    if problems:
        for problem in problems[:20]:
            print("PROBLEM:", problem)
        more = f" (first 20 of {len(problems)} shown)" if len(problems) > 20 else ""
        raise SystemExit(f"NOT published: {len(problems)} problem(s){more}. Nothing was copied.")

    amd = build_amd(stats, args.price_per_hour)
    print(f"Checks passed: {len(flags)} flags, {len(notes)} notes, judge {stats['judge_model']}, gpu {bench['gpu']}.")
    if amd["cost_per_1000_notes"] is None:
        print("cost_per_1000_notes is empty: pass --price-per-hour to fill it.")
    if args.check_only:
        return

    save_json(out / config.AMD_FILE.name, amd)
    files = {"sop.json": sop, "notes.json": notes, "flags.json": flags, "benchmark.json": bench, "amd.json": amd}
    folders = [config.DEMO_DIR]
    if config.FRONTEND_DATA_DIR.exists():
        folders.append(config.FRONTEND_DATA_DIR)
    else:
        print(f"No front end folder at {config.FRONTEND_DATA_DIR}; only the demo copy was written.")
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            save_json(folder / name, data)
        print(f"wrote {len(files)} files -> {folder}")

    decisions = config.FRONTEND_DATA_DIR / "decisions.json"
    if decisions.exists():
        os.replace(decisions, decisions.with_name("decisions.backup.json"))
        print("old front end decisions saved as decisions.backup.json")


if __name__ == "__main__":
    main()
