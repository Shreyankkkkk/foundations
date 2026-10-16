"""Tests for src/ingest.py and src/quote.py. Run from frontend/: python -m pytest"""
import ingest
from quote import quote_span

def test_numbered_steps_and_titles():
    steps = ingest.split_sop_steps("Heading\n1. Notify the crew: tell everyone.\n2) Stop the press and\nlock it out.\nStep 3: Try to start.")
    assert [t for t, _ in steps] == ["Notify the crew", "Stop the press and lock it out", "Try to start"]
    assert steps[1][1] == "Stop the press and lock it out."

def test_no_numbering_falls_back_to_paragraphs():
    assert len(ingest.split_sop_steps("Do this first.\n\nThen do that.")) == 2

def test_dated_log_becomes_notes_with_shift_and_type():
    n = ingest.split_notes_text("2026-10-08 Night handover: Skipped a check.\n2026-10-09 Evening near-miss: Almost started it.")
    assert n[0] == {"date": "2026-10-08", "shift": "Night", "source": "handover", "text": "Skipped a check."}
    assert n[1]["source"] == "near-miss"

def test_csv_columns_are_matched_by_alias():
    raw = ingest.parse_notes_file("n.csv", b"Date,Shift,Type,Note\n01/09/2026,night,Near miss report,Slipped on oil.\n")
    note = ingest.finish_notes(raw, {"date": "2026-01-01", "shift": "Day", "source": "handover"})[0]
    assert note == {"note_id": "N001", "date": "2026-09-01", "shift": "Night", "source": "near-miss", "text": "Slipped on oil."}

def test_validate_catches_problems_and_accepts_good_data():
    good_steps = [{"sop_id": "SOP-01", "step_id": 1, "title": "a", "text": "b"}]
    good_notes = [{"note_id": "N001", "date": "2026-09-01", "shift": "Day", "source": "handover", "text": "x"}]
    assert ingest.validate(good_steps, good_notes) == ([], [])
    errors, _ = ingest.validate(good_steps + good_steps, good_notes + [{**good_notes[0], "date": "1 Sept", "source": "gossip"}])
    assert len(errors) >= 4  # duplicate step, duplicate id, bad date, bad type

def test_quote_rule_ignores_case_spaces_and_curly_quotes():
    note = "We  didn\u2019t tell the line crew before isolating."
    s, e = quote_span(note, "DIDN'T tell the line crew")
    assert note[s:e] == "didn\u2019t tell the line crew"
    assert quote_span(note, "tell the crew") is None
