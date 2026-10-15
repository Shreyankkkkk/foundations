"""Checks the test data. Run from the backend folder:  python scripts/check_data.py

Prints one line per check and exits with code 1 if anything fails.
"""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
DRIFT_TYPES = {"skipped_step", "reordered_steps", "workaround_substitution",
               "sop_outdated_or_impractical", "sop_unclear"}
SOURCES = {"handover", "near-miss", "maintenance"}
SHIFTS = {"Day", "Evening", "Night"}

failures = []


def check(ok, label, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def norm(s):
    """Same rule as the quote check: ignore capitals and extra spaces."""
    return re.sub(r"\s+", " ", s).strip().lower()


def load(name):
    try:
        return json.loads((DATA / name).read_text(encoding="utf-8"))
    except Exception as e:  # missing file, bad JSON
        check(False, f"{name} loads", str(e))
        return None


sop = load("sop.json")
notes = load("notes.json")
key = load("answer_key.json")
if sop is None or notes is None or key is None:
    sys.exit(1)

# ---- SOPs
check(all(set(r) == {"sop_id", "step_id", "title", "text"} for r in sop), "sop.json: every row has exactly sop_id, step_id, title, text")
by_sop = {}
for r in sop:
    by_sop.setdefault(r["sop_id"], []).append(r["step_id"])
check(len(by_sop) == 3, "3 SOPs", f"found {len(by_sop)}")
for sid, steps in sorted(by_sop.items()):
    check(8 <= len(steps) <= 15, f"{sid}: 8 to 15 steps", f"found {len(steps)}")
    check(sorted(steps) == list(range(1, len(steps) + 1)), f"{sid}: step_ids run 1..n with no gaps or repeats")
check(all(r["title"].strip() and r["text"].strip() for r in sop), "no empty SOP titles or texts")
valid_steps = {(r["sop_id"], r["step_id"]) for r in sop}

# ---- notes
check(all(set(n) == {"note_id", "date", "shift", "source", "text"} for n in notes), "notes.json: every row has exactly note_id, date, shift, source, text")
check(195 <= len(notes) <= 205, "about 200 notes", f"found {len(notes)}")
ids = [n["note_id"] for n in notes]
check(len(ids) == len(set(ids)), "note_ids are unique")
check(all(n["source"] in SOURCES for n in notes), "every source is handover, near-miss or maintenance")
check(all(n["shift"] in SHIFTS for n in notes), "every shift is Day, Evening or Night")
bad_dates = []
for n in notes:
    try:
        date.fromisoformat(n["date"])
    except ValueError:
        bad_dates.append(n["note_id"])
check(not bad_dates, "every date is a real YYYY-MM-DD date", str(bad_dates[:5]))
check(all(n["text"].strip() for n in notes), "no empty note texts")
check(len({norm(n["text"]) for n in notes}) == len(notes), "no two notes have identical text")
text_of = {n["note_id"]: n["text"] for n in notes}

# ---- answer key
drifts, traps = key.get("drifts", []), key.get("traps", [])
check(len(drifts) == 25, "25 planted drifts", f"found {len(drifts)}")
check(all(set(d) == {"note_id", "sop_id", "step_id", "drift_type", "evidence"} for d in drifts), "answer_key: every drift has exactly note_id, sop_id, step_id, drift_type, evidence")
missing = [d["note_id"] for d in drifts if d["note_id"] not in text_of]
check(not missing, "every planted drift's note exists in notes.json", str(missing))
check(len({d["note_id"] for d in drifts}) == len(drifts), "no note carries two planted drifts")
check(all(d["drift_type"] in DRIFT_TYPES for d in drifts), "every drift_type is one of the five allowed")
counts = Counter(d["drift_type"] for d in drifts)
check(set(counts) == DRIFT_TYPES and all(c == 5 for c in counts.values()), "5 drifts of each type", str(dict(counts)))
check(all((d["sop_id"], d["step_id"]) in valid_steps for d in drifts), "every drift points at a real SOP step")
not_found = [d["note_id"] for d in drifts if d["note_id"] in text_of and norm(d["evidence"]) not in norm(text_of[d["note_id"]])]
check(not not_found, "every drift's evidence quote is in its note (same words, same order)", str(not_found))
check(len(traps) >= 20, "at least 20 trap notes", f"found {len(traps)}")
check(all(t["note_id"] in text_of for t in traps), "every trap note exists in notes.json")
check(not ({t["note_id"] for t in traps} & {d["note_id"] for d in drifts}), "no note is both a trap and a drift")
check(len({t["note_id"] for t in traps}) == len(traps), "no note is listed as a trap twice")
n_clean = len(notes) - len(drifts) - len(traps)
check(n_clean >= 100, "at least 100 clean notes", f"found {n_clean}")

print()
print(f"SOPs: {len(by_sop)} ({', '.join(f'{k}: {len(v)} steps' for k, v in sorted(by_sop.items()))})")
print(f"Notes: {len(notes)} = {len(drifts)} drift + {len(traps)} trap + {n_clean} clean")
if failures:
    print(f"\n{len(failures)} check(s) FAILED")
    sys.exit(1)
print("\nAll checks passed")