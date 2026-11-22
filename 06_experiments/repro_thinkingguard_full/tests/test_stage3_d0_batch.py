import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from stage2_inference import batch_pair_order
from stage2_cumulative import check_lineages


def test_d0_batch_keeps_a1_and_historical_pairs():
    pairs = ["test/x/1", "test/x/2", "test/x/3"]
    queues = {"a1_smoke": ["test/x/1/safe", "test/x/1/unsafe"],
              "a1_validation": ["test/x/2/safe", "test/x/2/unsafe"]}
    assert batch_pair_order("d0", pairs, queues) == pairs
    assert batch_pair_order("a1", pairs, queues) == ["test/x/3"]


def test_d0_runner_compatibility_rejects_changed_protocol():
    old = json.loads((ROOT / "runs/d0_pilot100_20261120/summary.json").read_text())["identity"]
    compat = json.loads((ROOT / "artifacts/d0_batch_runner_compatibility.json").read_text())
    new = dict(old, runner_sha256=compat["new_runner_sha256"], stage="batch",
               run_id="synthetic_batch", batch_queue_sha256="synthetic",
               batch_start_pair=100, batch_slice_pairs=1)
    assert set(check_lineages([old, new], "d0")["runner_sha256s"]) == {
        compat["old_runner_sha256"], compat["new_runner_sha256"]}
    for field in ("prompt_sha256", "parser_sha256", "config_sha256", "model_audit_sha256"):
        bad = copy.deepcopy(new)
        bad[field] = "changed"
        with pytest.raises(ValueError):
            check_lineages([old, bad], "d0")
    bad = copy.deepcopy(new)
    bad["runner_sha256"] = "unreviewed"
    with pytest.raises(ValueError):
        check_lineages([old, bad], "d0")


def test_missing_stays_in_fixed_300_denominator(tmp_path, monkeypatch):
    from stage2_cumulative import main
    output = tmp_path / "metrics.json"
    pilot = ROOT / "runs/d0_pilot100_20261120/predictions.jsonl"
    monkeypatch.setattr(sys, "argv", ["stage2_cumulative", "--protocol", "d0",
        "--pairs", "300", "--output", str(output), str(pilot)])
    main()
    result = json.loads(output.read_text())
    strict = result["reports"]["strict_full_denominator"]["micro"]
    valid = result["reports"]["valid_only"]["micro"]
    assert result["status"] == "COVERAGE_IN_PROGRESS"
    assert strict["n_total"] == 600 and strict["missing_prediction_rows"] == 400
    assert strict["n_correct"] == valid["n_correct"] == 143
    monkeypatch.setattr(sys, "argv", ["stage2_cumulative", "--protocol", "d0",
        "--pairs", "300", "--output", str(output), str(pilot), str(pilot)])
    with pytest.raises(ValueError, match="Duplicate prediction"):
        main()
