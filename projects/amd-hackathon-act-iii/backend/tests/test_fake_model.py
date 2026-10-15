"""Tests for src/models/fake_model.py. Run from backend/:  pytest tests/test_fake_model.py"""

import zlib

from src.models.fake_model import FakeModel, find_trigger, read_first_step, read_note_text
from src.stages.judge import build_prompt, judge_note, parse_reply
from src.stages.quote_check import quote_in_note

STEPS = [
    {"sop_id": "SOP-1", "step_id": 4, "title": "Isolate", "text": "Tell the line crew before isolating."},
    {"sop_id": "SOP-1", "step_id": 5, "title": "Vent", "text": "Vent the line."},
]


def make_note(text):
    return {"note_id": "N1", "date": "2026-09-01", "shift": "Day", "source": "handover", "text": text}


def find_note_text(wanted, start_text, limit=2000):
    """Search made-up note texts until the checksum rule matches (wanted = function of the checksum)."""
    for i in range(limit):
        text = f"{start_text} {i}"
        if wanted(zlib.crc32(text.encode("utf-8"))):
            return text
    raise AssertionError("no matching text found")


def test_reads_note_and_first_step_back_out_of_the_prompt():
    note = make_note("Something happened. Then more.")
    prompt = build_prompt(note, STEPS)
    assert read_note_text(prompt) == note["text"]
    assert read_first_step(prompt) == ("SOP-1", 4)


def test_find_trigger_picks_the_sentence_with_the_trigger_word():
    drift_type, sentence = find_trigger("Gauge replaced. We skipped the check, no time. All fine.")
    assert drift_type == "skipped_step"
    assert sentence == "We skipped the check, no time."


def test_find_trigger_none_for_a_clean_note():
    assert find_trigger("Replaced the gauge. Tested and fine.") is None


def test_clean_note_gives_no_flags():
    # clean replies only, so the invented-quote behaviour cannot interfere
    prompt = build_prompt(make_note("Replaced the gauge. Tested and fine."), STEPS)
    assert FakeModel(misbehave=False).ask(prompt) == "[]"


def test_drift_note_gives_a_valid_flag_with_a_real_quote():
    note = make_note("Fitters swapped the gearbox. We didn't tell the line crew before isolating.")
    flags = judge_note(note, STEPS, FakeModel(misbehave=False))
    assert len(flags) == 1
    assert flags[0]["sop_id"] == "SOP-1" and flags[0]["step_id"] == 4
    assert quote_in_note(flags[0]["quote"], note["text"])


def test_same_prompt_gives_same_reply():
    prompt = build_prompt(make_note("We skipped the check."), STEPS)
    model = FakeModel()
    assert model.ask(prompt) == model.ask(prompt)


def test_misbehaving_model_invents_a_quote_the_quote_check_rejects():
    text = find_note_text(lambda c: c % 5 == 0, "We skipped the check.")
    note = make_note(text)
    flags = judge_note(note, STEPS, FakeModel())
    quotes_ok = [quote_in_note(f["quote"], note["text"]) for f in flags]
    assert False in quotes_ok  # the invented one is there and fails the check
    assert True in quotes_ok  # the real one still passes


def test_misbehaving_model_sometimes_wraps_reply_in_a_fence_and_parse_reply_copes():
    text = find_note_text(lambda c: c % 7 == 0, "We skipped the check.")
    reply = FakeModel().ask(build_prompt(make_note(text), STEPS))
    assert reply.startswith("```json")
    assert isinstance(parse_reply(reply), list)


def test_prompt_without_steps_or_note_gives_empty_list():
    assert FakeModel().ask("nothing useful here") == "[]"