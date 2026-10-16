"""Tests for src/evaluation/benchmark.py. Run from backend/:  pytest tests/test_benchmark.py"""

import json
import sys

import pytest

from src import config
from src.evaluation import benchmark

CONTRACT_FIELDS = [
    "precision", "recall", "quote_verified_rate", "notes_per_minute",
    "matcher_model", "judge_model", "gpu", "false_alarms",
]

KEY = {
    "drifts": [
        {"note_id": "N1", "sop_id": "SOP-01", "step_id": 1, "drift_type": "skipped_step", "evidence": "skipped lockout"},
        {"note_id": "N2", "sop_id": "SOP-01", "step_id": 4, "drift_type": "workaround_substitution", "evidence": "used a hammer"},
    ],
    "traps": [{"note_id": "N3", "why": "pedestrian behaviour, not an SOP step"}],
}

NOTES = [
    {"note_id": "N1", "text": "We skipped lockout today."},
    {"note_id": "N2", "text": "Operator used a hammer instead."},
    {"note_id": "N3", "text": "Someone walked on the yellow line."},
    {"note_id": "N4", "text": "Everything normal."},
]

STATS = {"flags_proposed": 5, "flags_kept": 4, "notes_per_minute": 12.5,
         "judge_model": "some-model", "used_fake_model": False}


def flag(flag_id, note_id, sop_id="SOP-01", step_id=1, drift_type="skipped_step", quote="skipped lockout"):
    return {"flag_id": flag_id, "note_id": note_id, "sop_id": sop_id, "step_id": step_id,
            "drift_type": drift_type, "quote": quote}


F1 = flag("flag-1", "N1")                                                              # correct
F2 = flag("flag-2", "N2", step_id=4, drift_type="workaround_substitution", quote="used a hammer")  # correct


def run(flags, stats=STATS, gpu=None):
    return benchmark.build_results(flags, KEY, NOTES, stats, gpu)


def test_all_found_gives_perfect_scores():
    bench, details = run([F1, F2])
    assert bench["precision"] == 1.0
    assert bench["recall"] == 1.0
    assert bench["false_alarms"] == []
    assert details["missed_drifts"] == []


def test_benchmark_has_exactly_the_contract_fields_in_order():
    bench, _ = run([F1, F2])
    assert list(bench.keys()) == CONTRACT_FIELDS


def test_one_drift_missed():
    bench, details = run([F1])
    assert bench["precision"] == 1.0
    assert bench["recall"] == 0.5
    assert [m["note_id"] for m in details["missed_drifts"]] == ["N2"]


def test_no_flags_gives_none_precision_and_zero_recall():
    bench, details = run([])
    assert bench["precision"] is None
    assert bench["recall"] == 0.0
    assert len(details["missed_drifts"]) == 2


def test_flag_on_trap_note_is_a_false_alarm_with_the_trap_reason():
    bench, details = run([F1, F2, flag("flag-3", "N3")])
    assert bench["precision"] == pytest.approx(2 / 3)
    alarm = bench["false_alarms"][0]
    assert alarm["reason"] == "trap note"
    assert alarm["trap_why"] == "pedestrian behaviour, not an SOP step"
    assert details["false_alarms_by_reason"] == {"trap note": 1}


def test_flag_on_clean_note_is_a_false_alarm():
    bench, _ = run([F1, F2, flag("flag-3", "N4")])
    assert bench["false_alarms"][0]["reason"] == "clean note"
    assert bench["false_alarms"][0]["trap_why"] is None


def test_wrong_drift_type_on_a_drift_note_is_false_alarm_and_a_miss():
    wrong_type = flag("flag-1", "N1", drift_type="sop_unclear")
    bench, details = run([wrong_type, F2])
    assert bench["false_alarms"][0]["reason"] == "drift note, wrong step or drift type"
    assert bench["recall"] == 0.5
    assert [m["note_id"] for m in details["missed_drifts"]] == ["N1"]
    # same note and step, so the type-blind recall still counts it
    assert details["recall_ignoring_drift_type"] == 1.0


def test_wrong_step_on_a_drift_note_is_false_alarm():
    wrong_step = flag("flag-1", "N1", step_id=7)
    bench, details = run([wrong_step, F2])
    assert bench["false_alarms"][0]["reason"] == "drift note, wrong step or drift type"
    assert details["recall_ignoring_drift_type"] == 0.5


def test_second_flag_for_the_same_drift_is_a_duplicate_false_alarm():
    bench, details = run([F1, flag("flag-9", "N1"), F2])
    assert bench["recall"] == 1.0
    assert bench["precision"] == pytest.approx(2 / 3)
    assert bench["false_alarms"][0]["reason"] == "duplicate of a drift already found"


def test_quote_verified_rate_comes_from_run_stats():
    bench, _ = run([F1, F2])
    assert bench["quote_verified_rate"] == pytest.approx(4 / 5)
    assert bench["notes_per_minute"] == 12.5
    assert bench["judge_model"] == "some-model"


def test_missing_stats_give_none_fields():
    bench, _ = run([F1, F2], stats=None)
    assert bench["quote_verified_rate"] is None
    assert bench["notes_per_minute"] is None
    assert bench["judge_model"] is None


def test_zero_proposals_in_stats_gives_none_rate_not_a_crash():
    bench, _ = run([], stats={"flags_proposed": 0, "flags_kept": 0})
    assert bench["quote_verified_rate"] is None


def test_gpu_and_matcher_fields():
    bench, _ = run([F1], gpu="1x MI300X")
    assert bench["gpu"] == "1x MI300X"
    assert "no model" in bench["matcher_model"]


def test_by_drift_type_counts():
    _, details = run([F1])
    assert details["by_drift_type"]["skipped_step"] == {"planted": 1, "found": 1}
    assert details["by_drift_type"]["workaround_substitution"] == {"planted": 1, "found": 0}
    assert details["by_drift_type"]["reordered_steps"] == {"planted": 0, "found": 0}


def test_flag_with_quote_not_in_its_note_is_reported():
    bad = flag("flag-5", "N4", quote="this text is not in the note")
    _, details = run([F1, F2, bad])
    assert details["flags_with_quote_not_in_note"] == ["flag-5"]


def test_good_flags_have_no_bad_quotes():
    _, details = run([F1, F2])
    assert details["flags_with_quote_not_in_note"] == []


def write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_main_writes_benchmark_and_details_files(monkeypatch, tmp_path):
    fake_dir = tmp_path / "fake"
    fake_dir.mkdir()
    write(fake_dir / config.FLAGS_FILE.name, [F1, F2])
    write(fake_dir / config.RUN_STATS_FILE.name, {**STATS, "used_fake_model": True})
    write(tmp_path / "key.json", KEY)
    write(tmp_path / "notes.json", NOTES)
    monkeypatch.setattr(config, "FAKE_OUTPUT_DIR", fake_dir)
    monkeypatch.setattr(config, "ANSWER_KEY_FILE", tmp_path / "key.json")
    monkeypatch.setattr(config, "NOTES_FILE", tmp_path / "notes.json")
    monkeypatch.setattr(sys, "argv", ["benchmark", "--fake", "--gpu", "test-gpu"])

    benchmark.main()

    bench = json.loads((fake_dir / config.BENCHMARK_FILE.name).read_text(encoding="utf-8"))
    details = json.loads((fake_dir / benchmark.DETAILS_FILE_NAME).read_text(encoding="utf-8"))
    assert list(bench.keys()) == CONTRACT_FIELDS
    assert bench["gpu"] is None  # a pretend run never records a GPU, even if one is passed
    assert details["drifts_found"] == 2


def test_quote_verified_rate_uses_quotes_verified_when_the_run_stats_have_it():
    stats = {**STATS, "quotes_verified": 3, "flags_kept": 2}  # 1 of the 3 verified was a duplicate
    bench, _ = run([F1, F2], stats=stats)
    assert bench["quote_verified_rate"] == pytest.approx(3 / 5)


def test_main_without_flags_file_stops_with_a_clear_message(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "FAKE_OUTPUT_DIR", tmp_path / "nothing-here")
    monkeypatch.setattr(sys, "argv", ["benchmark", "--fake"])
    with pytest.raises(SystemExit) as error:
        benchmark.main()
    assert "Run the pipeline first" in str(error.value)


def setup_real_run(monkeypatch, tmp_path, stats):
    out = tmp_path / "output"
    out.mkdir()
    write(out / config.FLAGS_FILE.name, [F1, F2])
    write(out / config.RUN_STATS_FILE.name, stats)
    write(tmp_path / "key.json", KEY)
    write(tmp_path / "notes.json", NOTES)
    monkeypatch.setattr(config, "OUTPUT_DIR", out)
    monkeypatch.setattr(config, "ANSWER_KEY_FILE", tmp_path / "key.json")
    monkeypatch.setattr(config, "NOTES_FILE", tmp_path / "notes.json")
    return out


def test_real_run_without_gpu_is_refused(monkeypatch, tmp_path):
    setup_real_run(monkeypatch, tmp_path, STATS)
    monkeypatch.setattr(sys, "argv", ["benchmark"])
    with pytest.raises(SystemExit) as error:
        benchmark.main()
    assert "--gpu" in str(error.value)


def test_real_run_records_the_gpu(monkeypatch, tmp_path):
    out = setup_real_run(monkeypatch, tmp_path, STATS)
    monkeypatch.setattr(sys, "argv", ["benchmark", "--gpu", "1x MI300X"])
    benchmark.main()
    bench = json.loads((out / config.BENCHMARK_FILE.name).read_text(encoding="utf-8"))
    assert bench["gpu"] == "1x MI300X"
    assert bench["judge_model"] == "some-model"


def test_real_run_with_pretend_run_stats_is_refused(monkeypatch, tmp_path):
    out = setup_real_run(monkeypatch, tmp_path, {**STATS, "used_fake_model": True})
    monkeypatch.setattr(sys, "argv", ["benchmark", "--gpu", "1x MI300X"])
    with pytest.raises(SystemExit) as error:
        benchmark.main()
    assert "pretend" in str(error.value)
    assert not (out / config.BENCHMARK_FILE.name).exists()  # nothing was written


def test_real_run_problem_cases():
    assert benchmark.real_run_problem(STATS) is None
    assert "not found" in benchmark.real_run_problem(None)
    assert "judge_model" in benchmark.real_run_problem({**STATS, "judge_model": None})
    assert "notes_per_minute" in benchmark.real_run_problem({**STATS, "notes_per_minute": None})
    no_flag = {key: value for key, value in STATS.items() if key != "used_fake_model"}
    assert "pretend" in benchmark.real_run_problem(no_flag)  # an unknown origin is not trusted