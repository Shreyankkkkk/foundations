"""pipeline.py: the conductor. Same job as robot.cpp in the sumo robot.

It does no thinking itself. It calls the other files in order, one note at a time:

    loader        -> reads sop.json and notes.json
    matcher       -> picks the closest SOP steps for a note      (no AI)
    judge         -> asks the AI model if the note shows drift   (AI)
    quote_check   -> keeps a flag only if its quote is really in the note,
                     and replaces the model's quote with the note's own wording
    pipeline      -> builds the flags, merges duplicates and saves flags.json

Run it from the backend/ folder:
    python -m src.pipeline --fake --limit 10    pretend model, first 10 notes
    python -m src.pipeline                      real model, all notes, one at a time
    python -m src.pipeline --workers 8          real model, 8 notes at the same time (faster)
"""

import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from src import config
from src.models.fake_model import FakeModel
from src.stages.judge import judge_note, make_real_model
from src.stages.loader import load_notes, load_sop_steps
from src.stages.matcher import pick_candidate_steps
from src.stages.quote_check import exact_quote


def flag_id_for(note_id, sop_id, step_id, drift_type):
    """A flag's id is built from what the flag IS, so the same finding has the same id on every run.

    (Numbering flags 1, 2, 3 would give the same id to different flags after a
    re-run, and the front end saves approve/reject decisions by flag id.)
    """
    return f"{note_id}-{sop_id}-{step_id}-{drift_type}"


def build_flag(note, proposal):
    """Turn one model proposal into a flag in the data-contract format."""
    return {
        "flag_id": flag_id_for(note["note_id"], proposal["sop_id"], proposal["step_id"], proposal["drift_type"]),
        "sop_id": proposal["sop_id"],
        "step_id": proposal["step_id"],
        "note_id": note["note_id"],
        "date": note["date"],
        "shift": note["shift"],
        "drift_type": proposal["drift_type"],
        "quote": proposal["quote"],
        "confidence": proposal["confidence"],
        "status": "pending",  # the human approves or rejects in the front end
        "suggested_fix": None,  # filled later, only if we have time
    }


def process_note(note, steps, model):
    """Run ONE note through matcher, judge and quote check.

    Returns (proposals that passed the quote check, how many the model proposed).
    A kept proposal carries the note's own wording as its quote, and the sop_id
    and step_id exactly as written in sop.json (a model that answers 1.0 for 1
    still gives a whole number).
    """
    candidates = pick_candidate_steps(note, steps)
    proposals = judge_note(note, candidates, model)
    shown = {(step["sop_id"], step["step_id"]): step for step in candidates}

    kept = []
    for proposal in proposals:
        # Drop every proposal whose quote is not word for word in the note.
        quote = exact_quote(proposal["quote"], note["text"])
        if quote is None:
            continue
        step = shown[(proposal["sop_id"], proposal["step_id"])]  # judge_note checked it is there
        kept.append({**proposal, "sop_id": step["sop_id"], "step_id": step["step_id"], "quote": quote})
    return kept, len(proposals)


def run(model, limit=None, workers=1):
    """Run the notes through the stages. limit = only the first N notes (for tests).

    workers = how many notes are sent to the model at the same time. 1 = one after
    the other. A vLLM server handles several requests at once, so more workers raise
    notes per minute; the best number is measured (run with 1, 4, 8 and compare).
    Results are always handled in note order, so the flags are the same either way.
    """
    if workers < 1:
        raise ValueError("workers must be 1 or more.")
    steps = load_sop_steps()
    if not steps:
        raise ValueError("sop.json has no steps, so there is nothing to compare the notes against.")
    notes = load_notes()
    if limit is not None:
        notes = notes[:limit]

    flags_by_id = {}  # a dict keeps the order flags were first found in
    proposed_total = 0
    verified_total = 0
    failed_note_ids = []
    slowest_note_seconds = 0.0  # measured, so a request timeout can be calculated from it

    def work(note):
        """One note through the stages. A failure is returned, not raised, so one bad note cannot stop the run."""
        began = time.perf_counter()
        try:
            kept, proposed = process_note(note, steps, model)
            return note, kept, proposed, None, time.perf_counter() - began
        except Exception as error:
            return note, [], 0, error, time.perf_counter() - began

    start = time.perf_counter()  # stopwatch, to measure notes per minute
    pool = ThreadPoolExecutor(max_workers=workers)
    try:
        # pool.map hands the results back in note order, however many run at once
        for position, (note, kept, proposed, error, took) in enumerate(pool.map(work, notes), 1):
            slowest_note_seconds = max(slowest_note_seconds, took)
            print(f"{position}/{len(notes)} notes", end="\r", flush=True)
            if error is not None:
                failed_note_ids.append(note["note_id"])
                print(f"\nnote {note['note_id']} failed: {error}")
                continue
            proposed_total += proposed
            verified_total += len(kept)
            for proposal in kept:
                flag = build_flag(note, proposal)
                old = flags_by_id.get(flag["flag_id"])
                # Same note, step and drift type twice = one finding; keep the more confident copy.
                if old is None or flag["confidence"] > old["confidence"]:
                    flags_by_id[flag["flag_id"]] = flag
    finally:
        pool.shutdown(wait=False, cancel_futures=True)  # Ctrl+C stops quickly instead of finishing every queued note
    seconds = time.perf_counter() - start
    print()  # ends the progress line

    flags = list(flags_by_id.values())
    notes_done = len(notes) - len(failed_note_ids)
    # notes per minute = notes done / (seconds / 60); measured, not assumed
    notes_per_minute = notes_done / (seconds / 60) if seconds > 0 else None

    stats = {
        "notes_done": notes_done,
        "failed_note_ids": failed_note_ids,
        "flags_proposed": proposed_total,           # well-formed proposals from the model
        "quotes_verified": verified_total,          # of those, quote really in the note
        "flags_duplicate": verified_total - len(flags),  # merged into an identical flag
        "flags_kept": len(flags),                   # flags written to flags.json
        "flags_dropped": proposed_total - verified_total,  # dropped by the quote check
        "seconds": seconds,
        "slowest_note_seconds": slowest_note_seconds,
        "workers": workers,                         # notes sent to the model at the same time
        "notes_per_minute": notes_per_minute,
    }
    return flags, stats


def save_json(path, data):
    temp = f"{path}.tmp"  # write a temp file, then swap it in, so a crash never leaves half a file
    with open(temp, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    os.replace(temp, path)


def main():
    parser = argparse.ArgumentParser(description="Run the Procedure Drift Finder pipeline.")
    parser.add_argument("--fake", action="store_true",
                        help="use the pretend model (no GPU needed); results go to output/fake/")
    parser.add_argument("--limit", type=int, default=None,
                        help="only process the first N notes")
    parser.add_argument("--workers", type=int, default=1,
                        help="notes sent to the model at the same time (default 1, one after the other)")
    args = parser.parse_args()

    if args.fake:
        model = FakeModel()
        out_dir = config.FAKE_OUTPUT_DIR  # keeps pretend results away from real ones
    else:
        config.require_judge_settings()
        model = make_real_model()
        out_dir = config.OUTPUT_DIR
        if config.judge_limits()[0] is None:
            print("NOTE: JUDGE_TIMEOUT_S is not set, so one stuck request would wait forever.")

    flags, stats = run(model, args.limit, args.workers)
    if stats["failed_note_ids"] and stats["notes_done"] == 0:
        # nothing is written, so a good earlier result is never overwritten by an empty one
        raise SystemExit("Every note failed, so nothing was saved. Check JUDGE_BASE_URL, JUDGE_MODEL and that the model server is running.")
    if stats["failed_note_ids"]:
        print(f"WARNING: {len(stats['failed_note_ids'])} notes failed. publish.py will refuse this run until it is run again without failures.")
    stats["used_fake_model"] = args.fake
    stats["judge_model"] = None if args.fake else config.JUDGE_MODEL

    out_dir.mkdir(parents=True, exist_ok=True)
    save_json(out_dir / config.FLAGS_FILE.name, flags)
    save_json(out_dir / config.RUN_STATS_FILE.name, stats)
    print(f"{stats['notes_done']} notes done, {stats['flags_kept']} flags kept, "
          f"{stats['flags_dropped']} dropped by the quote check, "
          f"{stats['flags_duplicate']} duplicates merged -> {out_dir}")


if __name__ == "__main__":
    main()
