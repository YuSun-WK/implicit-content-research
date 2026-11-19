from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import socket
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import stage1_download as download
import stage1_manifest as manifest
import stage1_transport as transport
from stage1r_probe import supervised_lookup
import stage1r_state as state_check


URL = "https://fixture.example/image"
TEST_ROWS = [
    ("a", URL, "safe", "borderline", "unsafe", "S-B-U", 1),
    ("b", URL, "not_sure", "safe", "safe", "?-S-S", 2),
]


def test_stage1_resolver_on_local_numeric_address():
    assert transport.resolve("127.0.0.1", 443, 5) == ["127.0.0.1"]
    assert supervised_lookup("127.0.0.1", 5) == (["127.0.0.1"], None)


def test_stage1_resolver_slow_real_subprocess_is_bounded(monkeypatch):
    original = subprocess.run

    def slow(args, **kwargs):
        return original([*args[:3], "import time; time.sleep(2)\n" + args[3], *args[4:]], **kwargs)

    monkeypatch.setattr(transport.subprocess, "run", slow)
    with pytest.raises(transport.Failure, match="dns_timeout") as caught:
        transport.resolve("127.0.0.1", 443, 0.05)
    assert caught.value.retry
    assert isinstance(caught.value.__cause__, subprocess.TimeoutExpired)


@pytest.mark.parametrize(("errno", "reason", "retry"), [
    (socket.EAI_NONAME, "dns_name_not_found", False),
    (socket.EAI_AGAIN, "dns_resolution", True),
])
def test_resolver_keeps_permanent_and_transient_errors_distinct(monkeypatch, errno, reason, retry):
    monkeypatch.setattr(transport.subprocess, "run", lambda *a, **kw:
                        subprocess.CompletedProcess(a, 0, stdout=json.dumps({"error": errno}).encode()))
    with pytest.raises(transport.Failure, match=reason) as caught:
        transport.resolve("fixture.example", 443, 5)
    assert caught.value.retry is retry


def test_serial_controls_require_two_healthy_resolutions(monkeypatch):
    seen = []

    def resolve(host, port, timeout):
        seen.append((host, port, timeout))
        if host == "github.com":
            raise transport.Failure("dns_timeout", retry=True)
        return ["8.8.8.8"]

    monkeypatch.setattr(download, "resolve", resolve)
    assert not download.dns_controls({"connect_timeout": 5})
    assert seen == [("github.com", 443, 5), ("example.com", 443, 5)]
    monkeypatch.setattr(download, "resolve", lambda *args: ["8.8.8.8"])
    assert download.dns_controls({"connect_timeout": 5})


def init(root):
    (root / "run.lock").touch()
    for name in ("objects", "partials", "snapshots"):
        (root / name).mkdir()
    with closing(download.connect(root)) as db:
        download.initialize(db, TEST_ROWS)


def test_failed_dns_resume_leaves_prior_state_and_history(tmp_path, monkeypatch):
    init(tmp_path)
    with closing(download.connect(tmp_path)) as db:
        with db:
            download.event(db, URL, 4, "failure", reason="dns_timeout", state="failed_terminal")
            db.execute("UPDATE source SET state='failed_terminal',attempt=4,reason='dns_timeout'")
        events = db.execute("SELECT * FROM events").fetchall()
        sources = db.execute("SELECT * FROM source").fetchall()
        monkeypatch.setattr(download, "dns_controls", lambda _: False)

        def never(*args):
            pytest.fail("Acquisition started despite an unsuccessful DNS gate")

        monkeypatch.setattr(download, "run", never)
        for _ in range(2):
            assert download.run_with_dns_gate(tmp_path, db, [URL], {}, None, retry_environment_dns=True) == (
                "environment_dns_unavailable"
            )
        assert events == db.execute("SELECT * FROM events").fetchall()
        assert sources == db.execute("SELECT * FROM source").fetchall()


def test_figure_intersection_requires_every_uuid_in_each_modality(tmp_path, monkeypatch):
    snapshot = tmp_path / "snapshot.json"
    monkeypatch.setattr(manifest, "pinned_rows", lambda _: TEST_ROWS)
    raw = manifest.canonical(manifest.make_manifest(TEST_ROWS, {URL: "a" * 64}, "code"))
    snapshot.write_bytes(raw)
    expected = sha256(raw).hexdigest()
    valid = {
        "joint_decoded": [{"uuid": "a", "gold": "unsafe", "state": "not_run"}],
        "image_decoded_gold": [{"uuid": "a", "gold": "safe", "state": "generated", "raw_output": "unknown"}],
        "text_only_eligible": [{"uuid": "a", "gold": "borderline", "state": "generated", "raw_output": "Borderline"}],
    }
    assert manifest.validate_three_modality_predictions(valid, snapshot, expected, release_csv=None) == valid
    for entries in ([], valid["joint_decoded"] * 2, [{"uuid": "a", "gold": "unknown"}],
                    valid["joint_decoded"] + [{"uuid": "b", "gold": "safe"}]):
        with pytest.raises(ValueError):
            manifest.validate_three_modality_predictions(
                valid | {"joint_decoded": entries}, snapshot, expected, release_csv=None)
    with pytest.raises(ValueError, match="requires joint"):
        manifest.validate_three_modality_predictions(
            {"joint_decoded": valid["joint_decoded"]}, snapshot, expected, release_csv=None)


def test_state_inventory_rejects_changed_cache_bytes(tmp_path, monkeypatch):
    init(tmp_path)
    monkeypatch.setattr(state_check, "pinned_rows", lambda _: TEST_ROWS)
    raw = b"fixture cache"
    hex_digest = sha256(raw).hexdigest()
    obj = tmp_path / "objects" / hex_digest
    obj.write_bytes(raw)
    with closing(download.connect(tmp_path)) as db, db:
        db.execute("UPDATE source SET state='success_decode',digest=?", (hex_digest,))
        download.event(db, URL, 1, "decoded", sha256=hex_digest)
    info, inventory = state_check.check_state(tmp_path, None)
    assert info["sqlite_integrity"] == "ok"
    assert info["source_states"] == {"success_decode": 1}
    assert info["history_events"] == 1
    assert inventory[f"objects/{hex_digest}"] == hex_digest
    obj.write_bytes(b"corrupt")
    with pytest.raises(ValueError, match="object hash"):
        state_check.check_state(tmp_path, None)
