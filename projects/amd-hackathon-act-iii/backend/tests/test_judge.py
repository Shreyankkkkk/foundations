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


def test_parse_skips_brackets_in_the_words_before_the_list():
    reply = 'As asked in note [1], here is the answer: [{"a": 1}]'
    assert parse_reply(reply) == [{"a": 1}]


def test_parse_skips_a_broken_bracket_before_the_list():
    assert parse_reply('Steps [see below: [{"a": 1}]') == [{"a": 1}]


def test_parse_prefers_the_list_of_objects_over_a_list_of_numbers():
    assert parse_reply('Used [1, 2] first. Answer: [{"a": 1}]') == [{"a": 1}]


def test_parse_still_returns_a_list_that_has_no_objects():
    assert parse_reply("[1, 2]") == [1, 2]


def test_parse_treats_one_bare_object_as_a_list_of_one():
    assert parse_reply('{"a": 1}') == [{"a": 1}]


def test_parse_finds_a_bare_object_after_words():
    assert parse_reply('Here you go: {"a": 1} done') == [{"a": 1}]


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


# ---------- RealModel: timeout and retries (the requests library is replaced, no network) ----------

class FakeResponse:
    def __init__(self, status_code=200, retry_after=None):
        self.status_code = status_code
        self.headers = {} if retry_after is None else {"Retry-After": str(retry_after)}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise FakeRequests.HTTPError(f"status {self.status_code}")

    def json(self):
        return {"choices": [{"message": {"content": "[]"}}]}


class FakeRequests:
    """Stands in for the requests library: the first `fail` calls raise ConnectionError, then it answers."""

    class ConnectionError(Exception):
        pass

    class Timeout(Exception):
        pass

    class HTTPError(Exception):
        pass

    def __init__(self, fail):
        self.fail = fail
        self.timeouts = []

    def post(self, url, headers, json, timeout):
        self.timeouts.append(timeout)
        if len(self.timeouts) <= self.fail:
            raise self.ConnectionError("server down")
        return FakeResponse()


def real_model_with(monkeypatch, fail, **settings):
    import sys
    from src.stages.judge import RealModel
    fake = FakeRequests(fail)
    monkeypatch.setitem(sys.modules, "requests", fake)
    return RealModel("http://example/v1", "m", **settings), fake


def test_real_model_retries_a_connection_failure_then_succeeds(monkeypatch):
    model, fake = real_model_with(monkeypatch, fail=2, retries=2)
    assert model.ask("hi") == "[]"
    assert len(fake.timeouts) == 3  # two failures, then the answer


def test_real_model_gives_up_when_the_retries_run_out(monkeypatch):
    model, fake = real_model_with(monkeypatch, fail=5, retries=2)
    with pytest.raises(FakeRequests.ConnectionError):
        model.ask("hi")
    assert len(fake.timeouts) == 3  # first try plus 2 retries


def test_real_model_does_not_retry_by_default(monkeypatch):
    model, fake = real_model_with(monkeypatch, fail=1)
    with pytest.raises(FakeRequests.ConnectionError):
        model.ask("hi")
    assert len(fake.timeouts) == 1


def test_real_model_passes_the_timeout_on(monkeypatch):
    model, fake = real_model_with(monkeypatch, fail=0, timeout=7.5)
    model.ask("hi")
    assert fake.timeouts == [7.5]


# ---------- too many requests (429): wait as long as the server says, then try again ----------

def scripted_model(monkeypatch, responses, retries):
    import sys
    import time
    from src.stages.judge import RealModel

    class Scripted(FakeRequests):
        def post(self, url, headers, json, timeout):
            self.timeouts.append(timeout)
            return responses.pop(0)

    fake = Scripted(fail=0)
    waits = []
    monkeypatch.setitem(sys.modules, "requests", fake)
    monkeypatch.setattr(time, "sleep", waits.append)
    return RealModel("http://example/v1", "m", retries=retries), fake, waits


def test_real_model_waits_for_retry_after_on_429_then_succeeds(monkeypatch):
    model, fake, waits = scripted_model(monkeypatch, [FakeResponse(429, retry_after=60), FakeResponse(200)], retries=2)
    assert model.ask("hi") == "[]"
    assert waits == [60.0]
    assert len(fake.timeouts) == 2


def test_real_model_gives_up_on_429_when_retries_run_out(monkeypatch):
    model, fake, waits = scripted_model(monkeypatch, [FakeResponse(429, retry_after=1)] * 3, retries=2)
    with pytest.raises(FakeRequests.HTTPError):
        model.ask("hi")
    assert len(fake.timeouts) == 3
    assert waits == [1.0, 1.0]  # no wait after the last try


def test_real_model_does_not_retry_429_when_retries_is_zero(monkeypatch):
    model, fake, waits = scripted_model(monkeypatch, [FakeResponse(429, retry_after=60)], retries=0)
    with pytest.raises(FakeRequests.HTTPError):
        model.ask("hi")
    assert waits == []


def test_real_model_never_retries_a_400(monkeypatch):
    model, fake, waits = scripted_model(monkeypatch, [FakeResponse(400)], retries=5)
    with pytest.raises(FakeRequests.HTTPError):
        model.ask("hi")
    assert len(fake.timeouts) == 1 and waits == []


# ---------- config.judge_limits ----------

def test_judge_limits_read_the_environment_values(monkeypatch):
    from src import config
    monkeypatch.setattr(config, "JUDGE_TIMEOUT_S", "30")
    monkeypatch.setattr(config, "JUDGE_RETRIES", "2")
    assert config.judge_limits() == (30.0, 2)


def test_judge_limits_when_nothing_is_set(monkeypatch):
    from src import config
    monkeypatch.setattr(config, "JUDGE_TIMEOUT_S", None)
    monkeypatch.setattr(config, "JUDGE_RETRIES", None)
    assert config.judge_limits() == (None, 0)


@pytest.mark.parametrize("timeout, retries", [("abc", None), ("0", None), ("-5", None), (None, "1.5"), (None, "-1")])
def test_judge_limits_reject_bad_values(monkeypatch, timeout, retries):
    from src import config
    monkeypatch.setattr(config, "JUDGE_TIMEOUT_S", timeout)
    monkeypatch.setattr(config, "JUDGE_RETRIES", retries)
    with pytest.raises(RuntimeError):
        config.judge_limits()