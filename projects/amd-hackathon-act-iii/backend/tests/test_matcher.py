"""tests/test_matcher.py: tests for matcher.py, run with the fake model.

Status: empty skeleton, code comes in the build stage listed in STATE.md.
"""
from src import config
from src.stages.matcher import pick_candidate_steps


def make_step(step_id, text):
    return {"sop_id": "S", "step_id": step_id, "title": "", "text": text}


def test_picks_the_step_that_shares_words():
    steps = [make_step(1, "stop the line"), make_step(2, "fit your lock")]
    note = {"text": "We did not fit the lock today"}
    assert pick_candidate_steps(note, steps)[0]["step_id"] == 2


def test_rare_word_beats_common_word():
    steps = [
        make_step(1, "the red valve"),
        make_step(2, "the blue lock"),
        make_step(3, "the green lamp"),
    ]
    note = {"text": "the lock"}
    assert pick_candidate_steps(note, steps, top_n=1)[0]["step_id"] == 2


def test_never_returns_more_than_the_limit():
    steps = [make_step(i, "check the gauge") for i in range(config.TOP_STEPS_PER_NOTE + 5)]
    note = {"text": "gauge"}
    assert len(pick_candidate_steps(note, steps)) == config.TOP_STEPS_PER_NOTE


def test_no_shared_words_returns_empty_list():
    steps = [make_step(1, "stop the line")]
    note = {"text": "completely unrelated sentence"}
    assert pick_candidate_steps(note, steps) == []