"""Tests for src/stages/judge.py. Run from backend/:  pytest tests/test_judge.py

No GPU and no network: a stub model returns a fixed reply text.
"""

import pytest

from src.stages.judge import (
    DRIFT_TYPES,
    build_prompt,
    is_valid_proposal,
    judge_note,
    parse_reply,
)

NOTE = {
    "note_id": "note-1",
    "date": "2026-10-01",
    "shift": "night",
    "source": "handover",
    "text": "Skipped the lockout step because the key was missing.",
}

STEPS = [
    {"sop_id": "sop-1", "step_id": 1, "title": "Lockout", "text": "Lock out the machine before cleaning."},
    {"sop_id": "sop-1", "step_id": 2, "title": "Clean", "text": "Clean the rollers."},
    {"sop_id": "sop-2", "step_id": 1, "title": "Restart", "text": "Restart the line."},
]

REQUIRED_FIELDS = ["sop_id", "step_id", "drift_type", "quote", "confidence"]


def good_item(**changes):
    """A valid proposal; pass keyword arguments to change fields."""
    item = {
        "sop_id": "sop-1",
        "step_id": 1,
        "drift_type": "skipped_step",
        "quote": "Skipped the lockout step",
        "confidence": 0.9,
    }
    item.update(changes)
    return item


class StubModel:
    """Pretend model: always returns the same reply text and remembers the prompts it got."""

    def __init__(self, reply):
        self.reply = reply
        self.prompts = []

    def ask(self, prompt):
        self.prompts.append(prompt)
        return self.reply


# ---------- DRIFT_TYPES ----------

def test_drift_types_match_the_contract():
    assert DRIFT_TYPES == [
        "skipped_step",
        "reordered_steps",
        "workaround_substitution",
        "sop_outdated_or_impractical",
        "sop_unclear",
    ]


# ---------- build_prompt ----------

def test_prompt_contains_note_and_every_step():
    prompt = build_prompt(NOTE, STEPS)
    assert NOTE["text"] in prompt
    for step in STEPS:
        assert step["text"] in prompt
        assert step["title"] in prompt
        assert f'"{step["sop_id"]}"' in prompt


def test_prompt_lists_every_drift_type_and_the_empty_reply_rule():
    prompt = build_prompt(NOTE, STEPS)
    for drift_type in DRIFT_TYPES:
        assert drift_type in prompt
    assert "[]" in prompt


# ---------- parse_reply ----------

def test_parse_plain_list():
    assert parse_reply('[{"a": 1}]') == [{"a": 1}]


def test_parse_empty_list():
    assert parse_reply("[]") == []


def test_parse_list_inside_code_fence():
    reply = '```json\n[{"a": 1}]\n```'
    assert parse_reply(reply) == [{"a": 1}]


def test_parse_list_with_words_around_it():
    reply = 'Here is my answer: [{"a": 1}] Hope that helps!'
    assert parse_reply(reply) == [{"a": 1}]


def test_parse_reply_without_a_list_raises():
    with pytest.raises(ValueError):
        parse_reply("There is no drift in this note.")


def test_parse_brackets_in_wrong_order_raises():
    with pytest.raises(ValueError):
        parse_reply("] oops [")


def test_parse_broken_json_raises():
    with pytest.raises(ValueError):
        parse_reply("[not json at all]")


# ---------- is_valid_proposal ----------

def test_good_item_is_valid():
    assert is_valid_proposal(good_item(), STEPS)


def test_extra_fields_are_allowed():
    assert is_valid_proposal(good_item(reason="because"), STEPS)


@pytest.mark.parametrize("missing", REQUIRED_FIELDS)
def test_missing_field_is_invalid(missing):
    item = good_item()
    del item[missing]
    assert not is_valid_proposal(item, STEPS)


@pytest.mark.parametrize("bad", ["a string", None, 5, ["list"]])
def test_non_dict_is_invalid(bad):
    assert not is_valid_proposal(bad, STEPS)


def test_step_not_shown_to_the_model_is_invalid():
    assert not is_valid_proposal(good_item(step_id=99), STEPS)


def test_step_from_the_wrong_sop_is_invalid():
    # (sop-2, step 2) does not exist in the candidates, even though sop-1 step 2 and sop-2 step 1 do
    assert not is_valid_proposal(good_item(sop_id="sop-2", step_id=2), STEPS)


def test_step_id_as_text_is_invalid():
    # the model must give a number; "1" is not 1 (counted as a drop, visible in the stats)
    assert not is_valid_proposal(good_item(step_id="1"), STEPS)


def test_unknown_drift_type_is_invalid():
    assert not is_valid_proposal(good_item(drift_type="lazy_operator"), STEPS)


@pytest.mark.parametrize("quote", ["", "   \n", None, 42])
def test_bad_quote_is_invalid(quote):
    assert not is_valid_proposal(good_item(quote=quote), STEPS)


@pytest.mark.parametrize("confidence", [0, 0.0, 0.5, 1, 1.0])
def test_confidence_inside_0_to_1_is_valid(confidence):
    assert is_valid_proposal(good_item(confidence=confidence), STEPS)


@pytest.mark.parametrize("confidence", [-0.1, 1.5, 90, "0.9", None, True, False])
def test_bad_confidence_is_invalid(confidence):
    assert not is_valid_proposal(good_item(confidence=confidence), STEPS)


# ---------- judge_note ----------

def test_judge_note_returns_valid_proposals():
    model = StubModel('[{"sop_id": "sop-1", "step_id": 1, "drift_type": "skipped_step", '
                      '"quote": "Skipped the lockout step", "confidence": 0.9}]')
    result = judge_note(NOTE, STEPS, model)
    assert result == [good_item()]


def test_judge_note_sends_the_note_text_to_the_model():
    model = StubModel("[]")
    judge_note(NOTE, STEPS, model)
    assert len(model.prompts) == 1
    assert NOTE["text"] in model.prompts[0]


def test_judge_note_empty_reply_means_no_flags():
    assert judge_note(NOTE, STEPS, StubModel("[]")) == []


def test_judge_note_drops_invalid_items_and_keeps_valid_ones():
    reply = (
        '[{"sop_id": "sop-1", "step_id": 1, "drift_type": "skipped_step", "quote": "Skipped the lockout step", "confidence": 0.9},'
        ' {"sop_id": "sop-1", "step_id": 99, "drift_type": "skipped_step", "quote": "x", "confidence": 0.9},'
        ' {"sop_id": "sop-1", "step_id": 2, "drift_type": "made_up", "quote": "x", "confidence": 0.9},'
        ' "not even a dict"]'
    )
    result = judge_note(NOTE, STEPS, StubModel(reply))
    assert result == [good_item()]


def test_judge_note_without_candidates_does_not_call_the_model():
    model = StubModel("[]")
    assert judge_note(NOTE, [], model) == []
    assert model.prompts == []


def test_judge_note_reply_without_a_list_raises():
    with pytest.raises(ValueError):
        judge_note(NOTE, STEPS, StubModel("I cannot answer that."))