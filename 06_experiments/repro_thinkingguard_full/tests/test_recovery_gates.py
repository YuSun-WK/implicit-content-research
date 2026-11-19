import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from recovery_gates import bind_pid, prior_summary, queue_hash, queue_ready, registry_key, require_idle
from run_resumeable_inference import read, sha


def fixture():
    rows = {}
    for index in range(868):
        pair = f"test/category/{index}"
        for side in ("safe", "unsafe"):
            uid = f"{pair}/{side}"
            rows[uid] = dict(sample_uid=uid, pair_id=pair, side=side, ground_truth=side.capitalize(),
                             text="Example", split="test", category="category", hf_image_path=uid,
                             expected_image_sha256="abc", image_sha256="abc", dataset_revision="rev",
                             run_status="READY", image_decode_status="OK", image_local_path="image",
                             image_hash_reference="HF_LFS_SHA256")
    return rows, dict.fromkeys(rows, "abc")


def test_stage_data_checks_only_selected_complete_pairs():
    rows, tree = fixture()
    all_uids = list(rows)
    smoke = all_uids[:6]
    rows[all_uids[-1]]["run_status"] = "MISSING"
    assert queue_ready("smoke", rows, smoke, tree, "rev")["ready"]
    assert not queue_ready("full", rows, all_uids, tree, "rev")["ready"]
    rows[all_uids[-1]]["run_status"] = "READY"
    assert queue_ready("full", rows, all_uids, tree, "rev")["ready"]

    assert not queue_ready("smoke", rows, smoke, tree, "rev", lambda r: r["sample_uid"] != smoke[0])["ready"]
    assert not queue_ready("smoke", rows, smoke[:-1] + [all_uids[-1]], tree, "rev")["ready"]
    rows[smoke[0]]["image_sha256"] = "wrong"
    assert not queue_ready("smoke", rows, smoke, tree, "rev")["ready"]


@pytest.mark.parametrize(("snapshots", "expected"), [
    ([{"4102338":348}, {"4102338":412}, {"4102338":348}], "4102338"),
    ([{"4102338":348}, {"4102338":349}, {"4102338":348}], None),
    ([{"4102338":348}, {"4102338":412,"7":120}, {"4102338":348}], None),
])
def test_gpu_pid_challenge(snapshots, expected):
    snapshots = iter(snapshots)
    args = (lambda: next(snapshots), object, lambda: None, {150837}, lambda _:None, lambda _:None)
    if expected:
        assert bind_pid(*args)["host_pid"] == expected
    else:
        with pytest.raises(ValueError):
            bind_pid(*args)


def test_idle_check_refuses_an_existing_process():
    card = lambda _: {"uuid":"uuid","name":"4090","used_mib":3,"utilization_pct":0}
    with pytest.raises(ValueError):
        require_idle("uuid", card, lambda: {"another":20})


def test_registry_resolves_timestamped_run_and_rejects_drift(tmp_path):
    rows, _ = fixture()
    ordered = list(rows)[:6]
    inputs = queue_hash(rows, ordered)
    rows[ordered[0]]["image_local_path"] = "/other/verified/location"
    assert queue_hash(rows, ordered) == inputs
    base = {"runner_sha256":"runner"}
    run = tmp_path / "smoke_20261119"
    run.mkdir()
    path = run / "summary.json"
    identity = dict(**base, inputs_sha256=inputs, stage="smoke", run_id=run.name)
    path.write_text(json.dumps(dict(identity=identity, resource_gate=True, prediction_count=6)))
    registry = {registry_key(base, "smoke", inputs): dict(run_id=run.name, summary_sha256=sha(path))}
    assert prior_summary(tmp_path, registry, base, "smoke", inputs, read, sha)[0] == path
    with pytest.raises(ValueError):
        prior_summary(tmp_path, registry, {"runner_sha256":"changed"}, "smoke", inputs, read, sha)
    with pytest.raises(ValueError):
        prior_summary(tmp_path, registry, base, "validation", inputs, read, sha)
    path.write_text(path.read_text() + "\n")
    with pytest.raises(ValueError):
        prior_summary(tmp_path, registry, base, "smoke", inputs, read, sha)


def test_cli_prerequisite_is_global_and_compatibility_is_exact():
    from run_resumeable_inference import main, prerequisite_base
    assert "prior_summary" not in main.__code__.co_varnames
    new = {"runner_sha256": "new", "config_sha256": "config"}
    old = dict(new, runner_sha256="old")
    key = registry_key(old, "smoke", "inputs")
    registry = {key: {"summary_sha256": "verified"}}
    compatible = {"new_runner_sha256": "new", "old_runner_sha256": "old",
                  "smoke_summary_sha256": "verified"}
    assert prerequisite_base(new, registry, "smoke", "inputs", compatible) == old
    assert prerequisite_base(new, registry, "validation", "inputs", compatible) == new
    assert prerequisite_base(new, registry, "smoke", "other", compatible) == new
