"""Offline tests for the smoke roster, strict parser integration, and durable resume."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from stage2_qwen_smoke import available_gpu, execute
from stage2_roster import select_ids, task_rows


def test_selection_is_deterministic_favors_intersection_and_covers_classes():
    labels = ("safe", "borderline", "unsafe")
    rows = {
        str(i): (str(i), "url", "safe" if i < 11 else "not_sure", "safe", labels[i % 3], f"P{i}", i)
        for i in range(13)
    }
    selected = select_ids(rows, list(rows), 12, 10)
    assert select_ids(rows, list(reversed(rows)), 12, 10) == selected
    assert len(set(selected)) == 10
    assert {rows[u][4] for u in selected} == set(labels)
    assert all(rows[u][2] != "not_sure" for u in selected)
    with pytest.raises(ValueError):
        select_ids(rows, selected[:9], 12, 10)


def test_diagnostic_arms_use_the_same_frozen_prefix():
    roster = {"subjects": list(range(10))}
    assert task_rows(roster, "direct", 5) == list(range(10))
    assert task_rows(roster, "binary", 5) == task_rows(roster, "structured_cot", 5) == list(range(5))


def test_gpu_guard_refuses_shared_gpu(monkeypatch):
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "GPU-fixture")
    gpu = {"uuid": "GPU-fixture", "memory.used": "3", "utilization.gpu": "0"}
    assert available_gpu({"gpus": [gpu], "compute_apps": []}) == gpu
    with pytest.raises(ValueError, match="already in use"):
        available_gpu({"gpus": [gpu], "compute_apps": [{"gpu_uuid": "GPU-fixture"}]})


def test_mock_interruption_resume_and_strict_cot_output(tmp_path):
    image = b"fixture"
    digest = sha256(image).hexdigest()
    (tmp_path / digest).write_bytes(image)
    subjects = [{"uuid": uid, "gold": "safe", "pattern": "S-S-S",
                 "query_sha256": "query", "image_sha256": digest} for uid in ("a", "b", "c")]
    rows = {r["uuid"]: (r["uuid"], "url", "safe", "safe", "safe") for r in subjects}
    mode = "structured_cot"
    spec = {"prompt_sha256": "prompt", "model_revision": "fixture", "precision": "fixture",
            "seed": 0, "generation": {}, "runtime": {"quantization": None}}
    calls = []

    class Fake:
        def generate(self, path, prompt, query, settings):
            calls.append(query)
            if query == "b" and calls.count("b") == 1:
                raise KeyboardInterrupt
            answer = "Safe" if query == "a" else "Unsafe\n[Final Classification]: Safe"
            return {"raw_output": answer, "generated_tokens": 2, "runtime_s": 1,
                    "peak_allocated_bytes": 10, "peak_reserved_bytes": 20}

    def run():
        return execute(Fake(), tmp_path, subjects, {r["uuid"]: r["uuid"] for r in subjects},
                       rows, tmp_path, {mode: "prompt"}, spec, mode)

    partial = run()
    assert partial["generated"] == 1
    assert partial["states"] == {"generated": 1, "not_run": 2}
    finished = run()
    assert finished["run_id"] == partial["run_id"]
    assert finished["generated"] == 3
    assert finished["parse_status"] == {"invalid": 1, "valid": 2}
    assert calls == ["a", "b", "b", "c"]
    raw = [json.loads(line) for line in (tmp_path / finished["run_id"] / "raw.jsonl").read_text().splitlines()]
    parsed = [json.loads(line) for line in (tmp_path / finished["run_id"] / "parsed.jsonl").read_text().splitlines()]
    assert [r["raw_output"] for r in raw][0] == "Safe"
    assert [r["prediction"] for r in parsed] == ["INVALID", "safe", "safe"]
    assert all("raw_output" not in r for r in parsed)
    assert run()["generated"] == 3
    assert calls == ["a", "b", "b", "c"]
