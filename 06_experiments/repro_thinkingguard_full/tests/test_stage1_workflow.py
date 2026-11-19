import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evaluate_pairwise import score
from run_resumeable_inference import journal, read_journal


def test_resume_rejects_duplicates_and_config_drift(tmp_path):
    path = tmp_path / "predictions.jsonl"
    identity = {"stage": "smoke"}
    row = {"identity": identity, "sample_uid": "test/pair/safe", "raw_output": "line 1\nline 2"}
    remaining = {row["sample_uid"]: row}
    journal(path, remaining)
    assert read_journal(path, remaining, identity) == remaining
    with pytest.raises(ValueError):
        read_journal(path, remaining, {"stage": "validation"})
    with path.open("a") as handle:
        handle.write(json.dumps(row) + "\n")
    with pytest.raises(ValueError):
        read_journal(path, remaining, identity)


def test_strict_and_valid_denominators():
    pairs = [("Safe", "Unsafe"), ("INVALID", "Safe"), ("Safe", "MISSING"), ("Unsafe", "Safe")]
    strict = score(pairs)
    valid = score(pairs, valid_only=True)
    assert strict["accuracy"] == 3/8
    assert strict["pair_accuracy"] == 1/4
    assert strict["unsafe_recall"] == 1/4
    assert strict["unsafe_fnr"] == 3/4
    assert strict["safe_fpr"] == 1/4
    assert strict["invalid"] == 2
    assert valid["accuracy"] == 3/6
    assert valid["pair_accuracy"] == 1/2
