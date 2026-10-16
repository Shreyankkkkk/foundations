"""Tests for src/evaluation/publish.py. Run from backend/:  pytest tests/test_publish.py

No GPU, no network. Every folder is a temporary one.
"""

import copy
import json
import sys

import pytest

from src import config
from src.evaluation import publish
from src.evaluation.benchmark import DETAILS_FILE_NAME

SOP = [{"sop_id": "SOP-01", "step_id": 1, "title": "Lockout", "text": "Lock out the machine."}]
NOTES = [{"note_id": "N1", "date": "2026-09-01", "shift": "Day", "source": "handover",
          "text": "We skipped the lockout step today."}]
FLAGS = [{"flag_id": "N1-SOP-01-1-skipped_step", "sop_id": "SOP-01", "step_id": 1, "note_id": "N1",
          "date": "2026-09-01", "shift": "Day", "drift_type": "skipped_step",
          "quote": "skipped the lockout step", "confidence": 0.9, "status": "pending", "suggested_fix": None}]
BENCH = {"precision": 1.0, "recall": 0.5, "quote_verified_rate": 0.8, "notes_per_minute": 120.0,
         "matcher_model": "word-overlap matcher (plain Python, no model)", "judge_model": "some-model",
         "gpu": "1x MI300X", "false_alarms": []}
STATS = {"notes_done": 1, "failed_note_ids": [], "flags_proposed": 1, "quotes_verified": 1,
         "flags_duplicate": 0, "flags_kept": 1, "flags_dropped": 0, "seconds": 0.5,
         "notes_per_minute": 120.0, "used_fake_model": False, "judge_model": "some-model"}
DETAILS = {"flags_total": 1}


def problems(sop=SOP, notes=NOTES, flags=FLAGS, bench=BENCH):
    return publish.check_contract(copy.deepcopy(sop), copy.deepcopy(notes), copy.deepcopy(flags), copy.deepcopy(bench))


def with_flag(**changes):
    return [{**FLAGS[0], **changes}]


# ---------- check_contract ----------

def test_good_files_have_no_contract_problems():
    assert problems() == []


def test_a_quote_that_is_not_in_the_note_is_a_problem():
    found = problems(flags=with_flag(quote="the crew ignored every rule"))
    assert any("word for word" in p for p in found)


def test_a_flag_on_an_unknown_step_or_note_is_a_problem():
    assert any("no step" in p for p in problems(flags=with_flag(step_id=9)))
    assert any("no note" in p for p in problems(flags=with_flag(note_id="N77")))


def test_bad_confidence_status_and_drift_type_are_problems():
    assert any("confidence" in p for p in problems(flags=with_flag(confidence=1.5)))
    assert any("confidence" in p for p in problems(flags=with_flag(confidence=True)))
    assert any("status" in p for p in problems(flags=with_flag(status="done")))
    assert any("drift_type" in p for p in problems(flags=with_flag(drift_type="lazy")))


def test_an_extra_or_missing_flag_field_is_a_problem():
    extra = [{**FLAGS[0], "reason": "x"}]
    assert any("extra" in p for p in problems(flags=extra))
    short = [{k: v for k, v in FLAGS[0].items() if k != "quote"}]
    assert any("missing" in p for p in problems(flags=short))


def test_duplicate_flag_ids_are_a_problem():
    assert any("unique" in p for p in problems(flags=FLAGS + FLAGS))


def test_flag_date_or_shift_that_differs_from_its_note_is_a_problem():
    assert any("differs" in p for p in problems(flags=with_flag(shift="Night")))


def test_null_benchmark_numbers_are_problems_because_this_is_the_real_run():
    assert any("precision" in p for p in problems(bench={**BENCH, "precision": None}))
    assert any("judge_model" in p for p in problems(bench={**BENCH, "judge_model": None}))
    assert any("gpu" in p for p in problems(bench={**BENCH, "gpu": None}))
    assert any("notes_per_minute" in p for p in problems(bench={**BENCH, "notes_per_minute": None}))


def test_a_false_alarm_that_is_not_a_flag_is_a_problem():
    assert any("false alarm" in p for p in problems(bench={**BENCH, "false_alarms": [{"flag_id": "nope"}]}))
    assert problems(bench={**BENCH, "false_alarms": [{"flag_id": FLAGS[0]["flag_id"]}]}) == []
    assert problems(bench={**BENCH, "false_alarms": [FLAGS[0]["flag_id"]]}) == []  # plain ids are fine too


def test_bad_sop_and_note_rows_are_problems():
    assert any("whole number" in p for p in problems(sop=[{**SOP[0], "step_id": "1"}]))
    assert any("2026-09-01" in p for p in problems(notes=[{**NOTES[0], "date": "01/09/2026"}]))
    assert any("twice" in p for p in problems(notes=NOTES + NOTES))


# ---------- check_real_run ----------

def real_problems(stats=STATS, bench=BENCH, details=DETAILS, flags=FLAGS, notes=NOTES):
    return publish.check_real_run(stats, bench, details, flags, notes)


def test_a_finished_real_run_has_no_problems():
    assert real_problems() == []


def test_the_pretend_model_is_refused():
    assert any("pretend" in p for p in real_problems(stats={**STATS, "used_fake_model": True}))


def test_run_with_failed_notes_or_missing_notes_is_refused():
    assert any("failed" in p for p in real_problems(stats={**STATS, "failed_note_ids": ["N1"]}))
    assert any("--limit" in p for p in real_problems(stats={**STATS, "notes_done": 0}))


def test_benchmark_from_other_flags_or_other_model_is_refused():
    assert any("different flags" in p for p in real_problems(details={"flags_total": 5}))
    assert any("different judge_model" in p for p in real_problems(bench={**BENCH, "judge_model": "other"}))
    assert any("does not match" in p for p in real_problems(stats={**STATS, "flags_kept": 7}))


# ---------- build_amd ----------

def test_cost_per_1000_notes_comes_from_price_and_speed():
    amd = publish.build_amd(STATS, price_per_hour=2.0)
    # 120 notes per minute = 7200 notes per hour; $2 / 7200 * 1000 = $0.2778
    assert amd["cost_per_1000_notes"] == pytest.approx(2.0 / 7200 * 1000, abs=1e-4)


def test_without_a_price_nothing_is_invented():
    amd = publish.build_amd(STATS)
    assert amd == {"endpoint_status": "saved run", "cost_per_1000_notes": None,
                   "evolus_api_calls": None, "evolus_blocks": []}


# ---------- main ----------

def write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def setup(monkeypatch, tmp_path, stats=STATS):
    out = tmp_path / "output"
    out.mkdir()
    write(out / config.FLAGS_FILE.name, FLAGS)
    write(out / config.RUN_STATS_FILE.name, stats)
    write(out / config.BENCHMARK_FILE.name, BENCH)
    write(out / DETAILS_FILE_NAME, DETAILS)
    write(tmp_path / "sop.json", SOP)
    write(tmp_path / "notes.json", NOTES)
    front = tmp_path / "frontend_data"
    front.mkdir()
    monkeypatch.setattr(config, "OUTPUT_DIR", out)
    monkeypatch.setattr(config, "SOP_FILE", tmp_path / "sop.json")
    monkeypatch.setattr(config, "NOTES_FILE", tmp_path / "notes.json")
    monkeypatch.setattr(config, "DEMO_DIR", tmp_path / "demo")
    monkeypatch.setattr(config, "FRONTEND_DATA_DIR", front)
    return out, front


def test_main_copies_five_files_to_demo_and_front_end(monkeypatch, tmp_path):
    out, front = setup(monkeypatch, tmp_path)
    write(front / "decisions.json", {"N1-SOP-01-1-skipped_step": "approved"})
    monkeypatch.setattr(sys, "argv", ["publish", "--price-per-hour", "2"])

    publish.main()

    for folder in (tmp_path / "demo", front):
        for name in ("sop.json", "notes.json", "flags.json", "benchmark.json", "amd.json"):
            assert (folder / name).exists(), f"{name} missing in {folder}"
    amd = json.loads((front / "amd.json").read_text(encoding="utf-8"))
    assert amd["cost_per_1000_notes"] == pytest.approx(2.0 / 7200 * 1000, abs=1e-4)
    assert json.loads((front / "benchmark.json").read_text(encoding="utf-8"))["gpu"] == "1x MI300X"
    assert not (front / "decisions.json").exists()
    assert (front / "decisions.backup.json").exists()
    assert (out / config.AMD_FILE.name).exists()


def test_main_refuses_the_pretend_model_and_copies_nothing(monkeypatch, tmp_path):
    _, front = setup(monkeypatch, tmp_path, stats={**STATS, "used_fake_model": True})
    monkeypatch.setattr(sys, "argv", ["publish"])
    with pytest.raises(SystemExit) as error:
        publish.main()
    assert "NOT published" in str(error.value)
    assert list(front.iterdir()) == []
    assert not (tmp_path / "demo").exists()


def test_check_only_copies_nothing(monkeypatch, tmp_path):
    _, front = setup(monkeypatch, tmp_path)
    monkeypatch.setattr(sys, "argv", ["publish", "--check-only"])
    publish.main()
    assert list(front.iterdir()) == []
    assert not (tmp_path / "demo").exists()


def test_main_stops_with_a_clear_message_when_the_benchmark_has_not_run(monkeypatch, tmp_path):
    out, _ = setup(monkeypatch, tmp_path)
    (out / config.BENCHMARK_FILE.name).unlink()
    monkeypatch.setattr(sys, "argv", ["publish"])
    with pytest.raises(SystemExit) as error:
        publish.main()
    assert "benchmark.json" in str(error.value)


def test_main_without_a_front_end_folder_still_writes_the_demo_copy(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path)
    monkeypatch.setattr(config, "FRONTEND_DATA_DIR", tmp_path / "no-such-folder")
    monkeypatch.setattr(sys, "argv", ["publish"])
    publish.main()
    assert (tmp_path / "demo" / "flags.json").exists()
