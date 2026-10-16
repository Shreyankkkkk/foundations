"""Tests for src/pipeline.py. Run from backend/:  pytest tests/test_pipeline.py

No GPU, no network, no real data files: loaders and matcher are replaced with tiny fixed ones.
"""

import json
import sys

import pytest

from src import config, pipeline
from src.models.fake_model import FakeModel
from src.stages.quote_check import quote_in_note

FLAG_FIELDS = [
    "flag_id", "sop_id", "step_id", "note_id", "date", "shift",
    "drift_type", "quote", "confidence", "status", "suggested_fix",
]

STEPS = [{"sop_id": "SOP-1", "step_id": 1, "title": "Lockout", "text": "Lock out the machine."}]


def make_note(note_id, text, shift="Day"):
    return {"note_id": note_id, "date": "2026-09-01", "shift": shift, "source": "handover", "text": text}


NOTES = [
    make_note("N1", "We skipped the lockout step today."),   # quote is in this note: kept
    make_note("N2", "BOOM everything fine."),                # the stub model crashes on this one
    make_note("N3", "Clean shift, all good."),               # quote is NOT in this note: dropped
]

PROPOSAL = {
    "sop_id": "SOP-1", "step_id": 1, "drift_type": "skipped_step",
    "quote": "skipped the lockout step", "confidence": 0.9,
}


class StubModel:
    """Same reply for every note; raises for a note containing BOOM."""

    def ask(self, prompt):
        if "BOOM" in prompt:
            raise RuntimeError("model crashed")
        return json.dumps([PROPOSAL])


class ReplyModel:
    """Answers every note with the proposals it was given."""

    def __init__(self, *proposals):
        self.reply = json.dumps(list(proposals))

    def ask(self, prompt):
        return self.reply


@pytest.fixture
def small_data(monkeypatch):
    """Replace loaders and matcher inside pipeline.py with tiny fixed versions."""
    monkeypatch.setattr(pipeline, "load_sop_steps", lambda: STEPS)
    monkeypatch.setattr(pipeline, "load_notes", lambda: list(NOTES))
    monkeypatch.setattr(pipeline, "pick_candidate_steps", lambda note, steps: steps)


# ---------- build_flag ----------

def test_build_flag_has_exactly_the_contract_fields():
    flag = pipeline.build_flag(NOTES[0], PROPOSAL)
    assert list(flag.keys()) == FLAG_FIELDS


def test_build_flag_values():
    flag = pipeline.build_flag(NOTES[0], PROPOSAL)
    assert flag["flag_id"] == "N1-SOP-1-1-skipped_step"
    assert flag["note_id"] == "N1"
    assert flag["date"] == "2026-09-01" and flag["shift"] == "Day"
    assert flag["sop_id"] == "SOP-1" and flag["step_id"] == 1
    assert flag["drift_type"] == "skipped_step"
    assert flag["quote"] == "skipped the lockout step"
    assert flag["confidence"] == 0.9
    assert flag["status"] == "pending"
    assert flag["suggested_fix"] is None


def test_flag_id_depends_only_on_note_step_and_drift_type():
    other_quote = {**PROPOSAL, "quote": "something else", "confidence": 0.2}
    assert pipeline.build_flag(NOTES[0], PROPOSAL)["flag_id"] == pipeline.build_flag(NOTES[0], other_quote)["flag_id"]
    other_type = {**PROPOSAL, "drift_type": "sop_unclear"}
    assert pipeline.build_flag(NOTES[0], PROPOSAL)["flag_id"] != pipeline.build_flag(NOTES[0], other_type)["flag_id"]


# ---------- process_note ----------

def test_process_note_keeps_flag_whose_quote_is_in_the_note(small_data):
    kept, proposed = pipeline.process_note(NOTES[0], STEPS, StubModel())
    assert proposed == 1
    assert kept == [PROPOSAL]


def test_process_note_drops_flag_whose_quote_is_not_in_the_note(small_data):
    kept, proposed = pipeline.process_note(NOTES[2], STEPS, StubModel())
    assert proposed == 1
    assert kept == []


def test_process_note_lets_model_errors_through_for_run_to_handle(small_data):
    with pytest.raises(RuntimeError):
        pipeline.process_note(NOTES[1], STEPS, StubModel())


def test_process_note_replaces_the_models_quote_with_the_notes_own_words(small_data):
    model = ReplyModel({**PROPOSAL, "quote": "SKIPPED the  Lockout step."})
    kept, _ = pipeline.process_note(NOTES[0], STEPS, model)
    assert kept[0]["quote"] == "skipped the lockout step"  # exactly as written in the note


def test_process_note_keeps_punctuation_that_belongs_to_the_notes_words(small_data):
    note = make_note("N9", "Crew didn't lock out, said it was fine. Moved on.")
    model = ReplyModel({**PROPOSAL, "quote": "said it was fine"})
    kept, _ = pipeline.process_note(note, STEPS, model)
    assert kept[0]["quote"] == "said it was fine."


def test_process_note_gives_whole_number_step_ids(small_data):
    model = ReplyModel({**PROPOSAL, "step_id": 1.0})  # some models answer 1.0 for 1
    kept, _ = pipeline.process_note(NOTES[0], STEPS, model)
    assert type(kept[0]["step_id"]) is int and kept[0]["step_id"] == 1


# ---------- run ----------

def test_run_counts_kept_dropped_and_failed(small_data):
    flags, stats = pipeline.run(StubModel())
    assert len(flags) == 1
    assert flags[0]["note_id"] == "N1"
    assert stats["notes_done"] == 2                # N1 and N3; N2 crashed
    assert stats["failed_note_ids"] == ["N2"]
    assert stats["flags_proposed"] == 2            # N1 and N3 each proposed one
    assert stats["quotes_verified"] == 1
    assert stats["flags_kept"] == 1
    assert stats["flags_dropped"] == 1
    assert stats["flags_duplicate"] == 0


def test_run_keeps_going_after_a_failed_note(small_data):
    flags, stats = pipeline.run(StubModel())
    # N3 comes after the crashing N2 and was still processed
    assert stats["notes_done"] == 2


def test_run_flag_ids_are_stable_and_follow_note_order(small_data, monkeypatch):
    notes = [make_note(f"N{i}", "We skipped the lockout step today.") for i in range(1, 4)]
    monkeypatch.setattr(pipeline, "load_notes", lambda: notes)
    flags, _ = pipeline.run(StubModel())
    expected = ["N1-SOP-1-1-skipped_step", "N2-SOP-1-1-skipped_step", "N3-SOP-1-1-skipped_step"]
    assert [f["flag_id"] for f in flags] == expected
    again, _ = pipeline.run(StubModel())
    assert [f["flag_id"] for f in again] == expected   # same ids on a second run


def test_run_merges_identical_flags_and_keeps_the_more_confident_one(small_data):
    model = ReplyModel({**PROPOSAL, "confidence": 0.4}, {**PROPOSAL, "confidence": 0.9})
    flags, stats = pipeline.run(model, limit=1)
    assert len(flags) == 1 and flags[0]["confidence"] == 0.9
    assert stats["flags_proposed"] == 2 and stats["quotes_verified"] == 2
    assert stats["flags_duplicate"] == 1 and stats["flags_kept"] == 1


def test_run_limit_only_processes_the_first_notes(small_data):
    flags, stats = pipeline.run(StubModel(), limit=1)
    assert stats["notes_done"] == 1
    assert stats["failed_note_ids"] == []
    assert len(flags) == 1


def test_run_stats_has_timing_fields(small_data):
    _, stats = pipeline.run(StubModel())
    assert stats["seconds"] >= 0
    # notes_per_minute is None only if the run took 0 seconds (clock too coarse)
    assert stats["notes_per_minute"] is None or stats["notes_per_minute"] > 0


def test_run_with_the_fake_model_gives_flags_with_real_quotes_only(small_data, monkeypatch):
    # different text per note, so the fake model's checksum rules hit different notes
    notes = [
        make_note(f"N{i}", f"Gauge replaced. We skipped the lockout step today. Ref {i}.")
        for i in range(100)
    ]
    texts = {note["note_id"]: note["text"] for note in notes}
    monkeypatch.setattr(pipeline, "load_notes", lambda: notes)
    flags, stats = pipeline.run(FakeModel())
    assert len(flags) > 0
    for flag in flags:
        assert list(flag.keys()) == FLAG_FIELDS
        # every surviving quote is really in its own note, and is a piece of the note's own text
        assert quote_in_note(flag["quote"], texts[flag["note_id"]])
        assert flag["quote"] in texts[flag["note_id"]]
    # the fake model invents a quote for about 1 note in 5; the quote check removed those
    assert stats["flags_dropped"] > 0
    assert stats["flags_kept"] + stats["flags_duplicate"] + stats["flags_dropped"] == stats["flags_proposed"]

# ---------- save_json and main ----------

def test_save_json_round_trip_keeps_text_as_is(tmp_path):
    path = tmp_path / "out.json"
    data = [{"quote": "café, naïve"}]
    pipeline.save_json(path, data)
    assert path.read_text(encoding="utf-8").count("café") == 1  # not turned into \u escapes
    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_main_fake_mode_writes_flags_and_stats_to_the_fake_folder(small_data, monkeypatch, tmp_path):
    fake_dir = tmp_path / "fake"
    monkeypatch.setattr(config, "FAKE_OUTPUT_DIR", fake_dir)
    monkeypatch.setattr(sys, "argv", ["pipeline", "--fake", "--limit", "1"])
    pipeline.main()

    flags = json.loads((fake_dir / config.FLAGS_FILE.name).read_text(encoding="utf-8"))
    stats = json.loads((fake_dir / config.RUN_STATS_FILE.name).read_text(encoding="utf-8"))
    for flag in flags:
        assert list(flag.keys()) == FLAG_FIELDS
    assert stats["used_fake_model"] is True
    assert stats["judge_model"] is None
    assert stats["notes_done"] == 1
