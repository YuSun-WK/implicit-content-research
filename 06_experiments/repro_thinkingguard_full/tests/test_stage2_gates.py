import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from stage2_gates import batch_ready


def test_complete_pair_gate():
    rows = {}
    tree = {}
    for side in ("safe", "unsafe"):
        uid = f"test/x/1/{side}"
        path = f"test/images_test/x/1_{side}.png"
        rows[uid] = dict(sample_uid=uid, pair_id="test/x/1", side=side,
            split="test", ground_truth=side.capitalize(), dataset_revision="rev",
            run_status="READY", image_decode_status="OK", image_hash_reference="HF_LFS_SHA256",
            hf_image_path=path, expected_image_sha256=side, image_sha256=side,
            text="same", category="x")
        tree[path] = side
    ordered=list(rows)
    assert batch_ready(rows,ordered,tree,"rev",lambda _: True)["ready"]
    assert not batch_ready(rows,ordered[:1],tree,"rev",lambda _: True)["ready"]
    rows[ordered[1]]["text"]="different"
    assert not batch_ready(rows,ordered,tree,"rev",lambda _: True)["ready"]
