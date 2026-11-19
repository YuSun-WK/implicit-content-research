from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from email.message import Message
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
import errno
import socket
import sys
from threading import Thread
import time

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import stage1_download as download
import stage1_manifest as manifest
import stage1_report as reporting
import stage1_transport as net


URL = "https://fixture.example/photo"
OTHER = "https://other.example/photo"


@pytest.fixture
def config():
    return download.load_config(download.DEFAULT_CONFIG) | {"backoff": 0, "min_free_bytes": 0}


@pytest.fixture
def png():
    output = BytesIO()
    Image.new("RGB", (2, 3)).save(output, format="PNG")
    return output.getvalue()


@pytest.fixture
def db_root(tmp_path):
    for name in ("partials", "objects"):
        (tmp_path / name).mkdir()
    rows = make_rows()
    with download.connect(tmp_path) as db:
        download.initialize(db, rows)
    return tmp_path


def make_rows():
    return [
        ("a", URL, "safe", "safe", "safe", "S-S-S", 1),
        ("b", URL, "not_sure", "safe", "borderline", "?-S-B", 2),
        ("c", OTHER, "safe", "unsafe", "borderline", "S-U-B", 3),
    ]


class FakeResponse:
    def __init__(self, status, body=b"", **headers):
        self.status = status
        self.body = BytesIO(body)
        self.headers = Message()
        for k, v in headers.items():
            self.headers[k.replace("_", "-")] = str(v)

    def getheader(self, key, default=None):
        return self.headers.get(key, default)

    def read1(self, size):
        return self.body.read(size)


def plan(*responses):
    calls = []
    queue = iter(responses)

    @contextmanager
    def transport(url, headers, config, limiter, on_request):
        _, host, _, _ = net.target(url, 1, lambda *_: ["8.8.8.8"])
        with limiter.admit(host):
            calls.append((url, headers))
            on_request(url, host)
            response = next(queue)
            if isinstance(response, BaseException):
                raise response
            yield response, host
    return transport, calls


def state(root, url=URL):
    with download.connect(root) as db:
        return dict(db.execute("SELECT * FROM source WHERE url=?", (url,)).fetchone())


def outcomes(root):
    with download.connect(root) as db:
        return [r["data"] for r in db.execute("SELECT data FROM events")]


def png_response(body, **headers):
    return FakeResponse(200, body, Content_Type="image/png", Content_Length=len(body), **headers)


def test_verified_cache_resume_url_fanout_and_manifest(db_root, config, png, tmp_path):
    transport, calls = plan(png_response(png), png_response(png))
    limiter = net.Limiter(config, 2)
    for url in (URL, OTHER):
        download.process(db_root, url, config, limiter, transport)
    with download.connect(db_root) as db:
        download.verify_cache(db, db_root)
    download.process(db_root, URL, config, limiter, transport)
    assert len(calls) == 2
    assert len(list((db_root / "objects").iterdir())) == 1
    assert state(db_root)["digest"] == sha256(png).hexdigest()
    summary = reporting.build(db_root, tmp_path / "report", make_rows())
    assert summary["cohort_counts"] == {
        "release_roster": 3, "joint_decoded": 3, "image_decoded_gold": 2,
        "text_only_eligible": 3, "three_modality_intersection": 2}
    assert summary["decoded_urls"] == 2
    assert summary["duplicate_url_additional_uuid"] == 1


@pytest.mark.parametrize("status", [403, 404, 410])
def test_http_failures_are_terminal(db_root, config, status):
    transport, calls = plan(FakeResponse(status))
    limiter = net.Limiter(config, 2)
    for _ in range(2):
        download.process(db_root, URL, config, limiter, transport)
    assert len(calls) == 1
    assert state(db_root)["reason"] == f"http_{status}"


@pytest.mark.parametrize("result", [FakeResponse(503), net.Failure("request_timeout", retry=True)])
def test_retry_caps(db_root, config, result):
    transport, calls = plan(*(result for _ in range(4)))
    limiter = net.Limiter(config | {"host_interval": 0}, 8)
    for _ in range(6):
        download.process(db_root, URL, config, limiter, transport)
    assert len(calls) == 4
    assert state(db_root)["state"] == "failed_terminal"


def test_retry_after_is_persisted(db_root, config):
    transport, calls = plan(FakeResponse(429, Retry_After=120))
    limiter = net.Limiter(config, 2)
    t0 = time.time()
    download.process(db_root, URL, config, limiter, transport)
    with download.connect(db_root) as db:
        restored = dict(db.execute("SELECT * FROM cooldown"))
    assert restored["fixture.example"] >= t0 + 120
    assert state(db_root)["state"] == "deferred"
    download.process(db_root, URL, config, net.Limiter(config, 2, restored), transport)
    assert len(calls) == 1
    assert net.retry_after("Wed, 21 Oct 2015 07:28:00 GMT") == 0


@pytest.mark.parametrize(("response", "reason", "bytes_complete"), [
    (FakeResponse(200, b"<html>", Content_Type="text/html"), "unsupported_content_type", 1),
    (FakeResponse(200, b"x" * 11, Content_Type="image/png", Content_Length=11), "image_byte_limit", 0),
    (FakeResponse(200, b"x" * 11, Content_Type="image/png"), "image_byte_limit", 0),
    (FakeResponse(200, b"abc", Content_Length=10), "incomplete_body", 0),
])
def test_body_and_format_limits(db_root, config, response, reason, bytes_complete):
    transport, _ = plan(response)
    download.process(db_root, URL, config | {"max_bytes": 10}, net.Limiter(config, 2), transport)
    assert state(db_root)["reason"] == reason
    assert state(db_root)["http_success"] == 1
    assert state(db_root)["complete_bytes"] == bytes_complete


@pytest.mark.parametrize(("fmt", "mime"), [("PNG", "image/png"), ("JPEG", "image/jpeg"), ("WEBP", "image/webp")])
def test_corrupt_formats(db_root, config, fmt, mime):
    stream = BytesIO()
    Image.new("RGB", (32, 32)).save(stream, format=fmt)
    transport, _ = plan(FakeResponse(200, stream.getvalue()[:30], Content_Type=mime))
    download.process(db_root, URL, config, net.Limiter(config, 2), transport)
    assert state(db_root)["complete_bytes"] == 1
    assert state(db_root)["state"] == "failed_terminal"


@pytest.mark.parametrize(("mime", "cap", "reason"), [
    ("image/jpeg", 6, "image_mime_mismatch"), ("image/png", 5, "image_pixel_limit"),
])
def test_mime_and_pixel_limits(db_root, config, png, mime, cap, reason):
    transport, _ = plan(FakeResponse(200, png, Content_Type=mime))
    download.process(db_root, URL, config | {"max_pixels": cap}, net.Limiter(config, 2), transport)
    assert state(db_root)["reason"] == reason


@pytest.mark.parametrize("mode", ["206", "200", "416", "bad_range", "wrong_etag"])
def test_range_continuation(db_root, config, png, mode):
    config |= {"host_interval": 0}
    first = FakeResponse(200, png[:30], Content_Type="image/png", Content_Length=len(png), ETag='"v1"')
    options = {
        "206": FakeResponse(206, png[30:], Content_Type="image/png", ETag='"v1"',
                            Content_Range=f"bytes 30-{len(png)-1}/{len(png)}"),
        "200": png_response(png, ETag='"v2"'),
        "416": FakeResponse(416),
        "bad_range": FakeResponse(206, png[30:], Content_Type="image/png", ETag='"v1"', Content_Range="oops"),
        "wrong_etag": FakeResponse(206, png[30:], Content_Type="image/png", ETag='"v2"',
                                   Content_Range=f"bytes 30-{len(png)-1}/{len(png)}"),
    }
    transport, calls = plan(first, options[mode], png_response(png))
    limiter = net.Limiter(config, 4)
    for _ in range(3):
        download.process(db_root, URL, config, limiter, transport)
    assert calls[1][1]["Range"] == "bytes=30-"
    assert calls[1][1]["If-Range"] == '"v1"'
    assert state(db_root)["digest"] == sha256(png).hexdigest()
    if mode in {"416", "bad_range", "wrong_etag"}:
        assert "Range" not in calls[2][1]
    if mode == "206":
        with download.connect(db_root) as db:
            assert db.execute("SELECT COUNT(*) FROM events WHERE kind='range_resumed'").fetchone()[0] == 1


def test_restart_after_interruption_and_enospc(db_root, config, png):
    config |= {"host_interval": 0}
    transport, _ = plan(KeyboardInterrupt(), OSError(errno.ENOSPC, "fixture"), png_response(png))
    with pytest.raises(KeyboardInterrupt):
        download.process(db_root, URL, config, net.Limiter(config, 1), transport)
    with download.connect(db_root) as db:
        assert state(db_root)["state"] == "inflight"
        download.verify_cache(db, db_root)
    assert state(db_root)["state"] == "queued"
    with pytest.raises(net.Pause, match="disk_full"):
        download.process(db_root, URL, config, net.Limiter(config, 1), transport)
    download.process(db_root, URL, config, net.Limiter(config, 1), transport)
    assert state(db_root)["state"] == "success_decode"
    assert any("disk_full" in e for e in outcomes(db_root))


@pytest.mark.parametrize("destination", ["http://localhost/photo", "http://192.168.1.1/photo",
                                         "http://[::ffff:127.0.0.1]/photo", "https://a@fixture.example/x"])
def test_redirects_are_a_new_security_decision(db_root, config, destination):
    transport, calls = plan(FakeResponse(302, Location=destination))
    download.process(db_root, URL, config, net.Limiter(config, 2), transport)
    assert len(calls) == 1
    assert state(db_root)["category"] == "security"


def test_dns_rebinding_is_rejected_before_socket_creation():
    answers = iter([["8.8.8.8"], ["192.168.1.1"]])
    resolver = lambda *_: next(answers)
    assert net.target(URL, 1, resolver)[-1] == ("8.8.8.8",)
    with pytest.raises(net.Failure, match="unsafe_target"):
        net.target(URL, 1, resolver)


def test_pinned_target_peer_and_tls_name(monkeypatch, config):
    seen = []

    class Socket:
        def settimeout(self, value):
            pass

        def connect(self, address):
            seen.append(address)

        def getpeername(self):
            return ("8.8.8.8", 443)

        def close(self):
            pass

        def do_handshake(self):
            seen.append("handshake")

    class TLS:
        def wrap_socket(self, sock, **kwargs):
            seen.append(kwargs)
            return sock

    monkeypatch.setattr(net.socket, "socket", lambda *_: Socket())
    monkeypatch.setattr(net.ssl, "create_default_context", TLS)
    conn = net.PinnedConnection("fixture.example", 443, "8.8.8.8", True, config)
    conn.connect()
    assert seen == [("8.8.8.8", 443),
                    {"server_hostname": "fixture.example", "do_handshake_on_connect": False}, "handshake"]
    monkeypatch.setattr(Socket, "getpeername", lambda _: ("8.8.4.4", 443))
    with pytest.raises(net.Failure, match="peer_mismatch"):
        net.PinnedConnection("fixture.example", 443, "8.8.8.8", True, config).connect()


def test_http_fixture_host_header_and_https_redirect(db_root, config, png, monkeypatch):
    hosts = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            hosts.append((self.headers["Host"], self.path))
            if self.path == "/start":
                self.send_response(301)
                self.send_header("Location", "https://fixture.example/photo")
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(png)))
                self.end_headers()
                self.wfile.write(png)

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        hops = []

        def fixture_socket(conn):
            hops.append((conn.address, conn.host, conn.port, conn.secure))
            conn.sock = socket.create_connection(server.server_address, 1)
            conn.active_socket = conn.sock

        monkeypatch.setattr(net.PinnedConnection, "connect", fixture_socket)
        resolver = lambda *_: ["8.8.8.8"]
        limiter = net.Limiter(config | {"host_interval": 0}, 2)
        try:
            body, mime = download.download(
                "http://fixture.example/start", db_root / "partials/test", db_root / "partials/test.json",
                config, limiter, lambda *a, **kw: None, lambda *a: None,
                lambda *args: net.response(*args, resolver=resolver))
        finally:
            server.shutdown()
            thread.join()
    assert (body, mime) == (len(png), "image/png")
    assert hops == [("8.8.8.8", "fixture.example", 80, False),
                    ("8.8.8.8", "fixture.example", 443, True)]
    assert hosts == [("fixture.example", "/start"), ("fixture.example:443", "/photo")]


def test_rate_limit_enforces_global_spacing_and_same_host_serialization(config):
    limiter = net.Limiter(config | {"host_interval": 0.05, "global_interval": 0.02}, 3)
    intervals = []

    def job(host):
        with limiter.admit(host):
            start = time.monotonic()
            time.sleep(0.03)
            intervals.append((start, time.monotonic(), host))

    with ThreadPoolExecutor(3) as pool:
        list(pool.map(job, ["a", "a", "b"]))
    first, second, third = sorted(intervals)
    assert second[0] - first[0] >= 0.018
    assert third[0] - second[0] >= 0.018
    a, b = sorted(i for i in intervals if i[-1] == "a")
    assert b[0] >= a[1] and b[0] - a[0] >= 0.048
    with pytest.raises(net.Pause):
        with limiter.admit("d"):
            pass


def test_manifest_validates_distinct_planned_ids_and_gold(tmp_path, monkeypatch):
    rows = make_rows()
    monkeypatch.setattr(manifest, "pinned_rows", lambda _: rows)
    private = tmp_path / "manifest.json"
    data = manifest.canonical(manifest.make_manifest(rows, {URL: "a" * 64}, "code"))
    private.write_bytes(data)
    args = private, sha256(data).hexdigest(), "joint_decoded"
    predictions = [{"uuid": "a", "gold": "safe"}, {"uuid": "b", "gold": "borderline"}]
    assert manifest.validate_predictions(predictions, *args, release_csv=None) == predictions
    for modified in (predictions[:1], predictions + predictions[:1],
                     predictions[:1] + [{"uuid": "c", "gold": "borderline"}],
                     predictions[:1] + [{"uuid": "b", "gold": "unsafe"}]):
        with pytest.raises(ValueError):
            manifest.validate_predictions(modified, *args, release_csv=None)


def test_official_roster_denominators_if_provided():
    import os

    source = os.environ.get("VLSU_PINNED_CSV")
    if not source:
        pytest.skip("Run with VLSU_PINNED_CSV to validate the release roster")
    rows = manifest.pinned_rows(Path(source))
    assert len(rows) == 8159
    assert len({r[1] for r in rows}) == 8157
    assert sum(r[2] != "not_sure" for r in rows) == 8018
    groups = Counter("question" if r[5].startswith("?") else
                     "paper" if r[5] in reporting.FIGURE9_LEGEND else "extra" for r in rows)
    assert groups == {"paper": 8016, "extra": 2, "question": 141}
    smoke = manifest.smoke_rows(rows)
    assert smoke == manifest.smoke_rows(list(reversed(rows)))
    assert len(smoke) == 51 and len({r[1] for r in smoke}) == 49
    assert {r[5] for r in smoke} == {r[5] for r in rows}


def test_reopen_dns_failure_keeps_history_and_refusals(db_root, config):
    with download.connect(db_root) as db:
        for url, reason in [(URL, "dns_timeout"), (OTHER, "http_403")]:
            download.event(db, url, 4, "failure", reason=reason)
            db.execute("UPDATE source SET state='failed_terminal',attempt=4,reason=? WHERE url=?",
                       (reason, url))
    with download.connect(db_root) as db:
        assert download.reopen_environment_failures(db, [URL, OTHER]) == 1
    assert state(db_root)["retry_floor"] == 4
    assert state(db_root, OTHER)["state"] == "failed_terminal"
    transport, calls = plan(net.Failure("dns_timeout", retry=True))
    download.process(db_root, URL, config, net.Limiter(config, 1), transport)
    assert state(db_root)["state"] == "retryable"
    assert state(db_root)["attempt"] == 5
    assert sum("dns_timeout" in record for record in outcomes(db_root)) == 3


def test_recent_resolver_fault_is_based_on_consecutive_events(db_root):
    with download.connect(db_root) as db:
        for attempt in range(12):
            download.event(db, URL, attempt, "failure", reason="dns_timeout")
        assert download.resolver_fault_recent(db)
        download.event(db, OTHER, 1, "http", status=403)
        assert not download.resolver_fault_recent(db)


def test_smoke_summary_preserves_pass_time_outcomes():
    events = [
        {"url": URL, "kind": "attempt_started", "data": "{}", "at": 1},
        {"url": URL, "kind": "failure", "data": '{"state":"failed_terminal"}', "at": 2},
        {"url": URL, "kind": "environment_reopened", "data": "{}", "at": 4},
        {"url": URL, "kind": "decoded", "data": "{}", "at": 5},
    ]
    statuses, attempted = reporting.smoke_at_gate(make_rows(), events, 3)
    assert reporting.coverage(make_rows(), statuses, attempted) == {
        "n": 3, "decoded": 0, "failed": 2, "not_attempted": 1,
        "attempted_pending": 0, "coverage": 0,
    }
