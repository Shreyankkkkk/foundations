"""benchmark.py: compares the pipeline's flags with the answer key and writes benchmark.json.

Run from backend/:
    python -m src.evaluation.benchmark --fake              scores output/fake/ (pretend model)
    python -m src.evaluation.benchmark --gpu "1x MI300X"   scores output/ (real run)

A flag is CORRECT only if note_id, sop_id, step_id and drift_type all match a
planted drift in the answer key. Each planted drift can be found once; a second
flag for the same drift counts as a false alarm (duplicate).

Writes two files next to flags.json:
  benchmark.json          exactly the fields of the data contract (front end reads it)
  benchmark_details.json  extra numbers for our own review (missed drifts, by type, ...)

Numbers from a --fake run say nothing about the real model.
"""

import argparse
import json

from src import config
from src.stages.judge import DRIFT_TYPES
from src.stages.quote_check import quote_in_note

MATCHER_NAME = "word-overlap matcher (plain Python, no model)"
DETAILS_FILE_NAME = "benchmark_details.json"


def load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def drift_key(item):
    """The four fields that must all match for a flag to count as correct."""
    return (item["note_id"], item["sop_id"], item["step_id"], item["drift_type"])


def score_flags(flags, answer_key):
    """Split the flags into correct ones and false alarms; list the drifts nobody found.

    Returns (found_keys, false_alarms, missed_drifts).
    """
    drifts = answer_key["drifts"]
    traps = {trap["note_id"]: trap.get("why", "") for trap in answer_key["traps"]}
    drift_note_ids = {drift["note_id"] for drift in drifts}
    wanted = {drift_key(drift) for drift in drifts}

    found = set()
    false_alarms = []
    for flag in flags:
        key = drift_key(flag)
        if key in wanted and key not in found:
            found.add(key)  # correct, first time this drift is found
            continue
        if key in wanted:
            reason = "duplicate of a drift already found"
        elif flag["note_id"] in traps:
            reason = "trap note"
        elif flag["note_id"] in drift_note_ids:
            reason = "drift note, wrong step or drift type"
        else:
            reason = "clean note"
        false_alarms.append({
            "flag_id": flag["flag_id"],
            "note_id": flag["note_id"],
            "sop_id": flag["sop_id"],
            "step_id": flag["step_id"],
            "drift_type": flag["drift_type"],
            "quote": flag["quote"],
            "reason": reason,
            "trap_why": traps.get(flag["note_id"]),  # None unless it is a trap note
        })

    missed = [drift for drift in drifts if drift_key(drift) not in found]
    return found, false_alarms, missed


def build_results(flags, answer_key, notes, stats, gpu=None):
    """Return (benchmark, details). benchmark has exactly the data-contract fields."""
    drifts = answer_key["drifts"]
    found, false_alarms, missed = score_flags(flags, answer_key)

    # precision = correct flags / all flags; recall = drifts found / planted drifts
    precision = len(found) / len(flags) if flags else None
    recall = len(found) / len(drifts) if drifts else None

    # share of the model's proposals whose quote really was in the note (from the run stats)
    quote_verified_rate = None
    notes_per_minute = None
    judge_model = None
    if stats:
        if stats.get("flags_proposed"):
            quote_verified_rate = stats["flags_kept"] / stats["flags_proposed"]
        notes_per_minute = stats.get("notes_per_minute")
        judge_model = stats.get("judge_model")

    benchmark = {
        "precision": precision,
        "recall": recall,
        "quote_verified_rate": quote_verified_rate,
        "notes_per_minute": notes_per_minute,
        "matcher_model": MATCHER_NAME,
        "judge_model": judge_model,
        "gpu": gpu,
        "false_alarms": false_alarms,
    }

    # --- extra numbers for our own review ---
    located = {(f["note_id"], f["sop_id"], f["step_id"]) for f in flags}
    found_ignoring_type = [d for d in drifts if (d["note_id"], d["sop_id"], d["step_id"]) in located]

    by_type = {}
    for drift_type in DRIFT_TYPES:
        planted = [d for d in drifts if d["drift_type"] == drift_type]
        got = [d for d in planted if drift_key(d) in found]
        by_type[drift_type] = {"planted": len(planted), "found": len(got)}

    reasons = {}
    for alarm in false_alarms:
        reasons[alarm["reason"]] = reasons.get(alarm["reason"], 0) + 1

    texts = {note["note_id"]: note["text"] for note in notes}
    flags_with_bad_quote = [
        f["flag_id"] for f in flags if not quote_in_note(f["quote"], texts.get(f["note_id"], ""))
    ]

    details = {
        "flags_total": len(flags),
        "drifts_planted": len(drifts),
        "drifts_found": len(found),
        "false_alarm_count": len(false_alarms),
        "false_alarms_by_reason": reasons,
        "recall_ignoring_drift_type": (len(found_ignoring_type) / len(drifts)) if drifts else None,
        "by_drift_type": by_type,
        "missed_drifts": missed,
        "flags_with_quote_not_in_note": flags_with_bad_quote,  # should always be empty
    }
    return benchmark, details


def main():
    parser = argparse.ArgumentParser(description="Score flags.json against the answer key.")
    parser.add_argument("--fake", action="store_true",
                        help="score output/fake/ (pretend-model run) instead of output/")
    parser.add_argument("--gpu", default=None,
                        help='GPU name for the record, e.g. "1x MI300X" (the code cannot know it)')
    args = parser.parse_args()

    out_dir = config.FAKE_OUTPUT_DIR if args.fake else config.OUTPUT_DIR
    flags_path = out_dir / config.FLAGS_FILE.name
    stats_path = out_dir / config.RUN_STATS_FILE.name
    if not flags_path.exists():
        raise SystemExit(f"{flags_path} not found. Run the pipeline first.")

    flags = load_json(flags_path)
    stats = load_json(stats_path) if stats_path.exists() else None
    answer_key = load_json(config.ANSWER_KEY_FILE)
    notes = load_json(config.NOTES_FILE)

    benchmark, details = build_results(flags, answer_key, notes, stats, args.gpu)

    save_json(out_dir / config.BENCHMARK_FILE.name, benchmark)
    save_json(out_dir / DETAILS_FILE_NAME, details)

    def show(value):
        return "n/a" if value is None else f"{value:.3f}"

    print(f"precision {show(benchmark['precision'])}, recall {show(benchmark['recall'])}, "
          f"quote_verified_rate {show(benchmark['quote_verified_rate'])}")
    print(f"found {details['drifts_found']}/{details['drifts_planted']} drifts, "
          f"{details['false_alarm_count']} false alarms -> {out_dir}")
    if stats and stats.get("used_fake_model"):
        print("WARNING: this run used the pretend model. Do not use these numbers anywhere.")


if __name__ == "__main__":
    main()