"""Low-frequency diagnostic of the existing resolver and direct HTTPS path."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timezone
import http.client
from ipaddress import ip_address
import json
from multiprocessing import get_context
import os
from pathlib import Path
import platform
import shutil
import socket
import ssl
import subprocess
from time import monotonic, sleep
from urllib.parse import urlsplit

from stage1_download import connect
from stage1_transport import Failure, resolve, target

CONTROLS = ("github.com", "example.com")
TIMEOUT = 5


def emit(**row):
    print(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), **row}, sort_keys=True), flush=True)


def elapsed(start):
    return round(monotonic() - start, 4)


def lookup_in_process(host, pipe):
    """Call getaddrinfo in an already-started interpreter, supervised by the parent."""
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        pipe.send((sorted({row[4][0] for row in addresses}), None))
    except socket.gaierror as error:
        pipe.send(([], error.errno))
    finally:
        pipe.close()


def supervised_lookup(host, timeout):
    context = get_context("fork")
    reader, writer = context.Pipe(duplex=False)
    process = context.Process(target=lookup_in_process, args=(host, writer))
    with reader, writer:
        process.start()
        writer.close()
        try:
            if reader.poll(timeout):
                try:
                    return reader.recv()
                except EOFError:
                    return [], "worker_exit"
            return [], "watchdog_timeout"
        finally:
            if process.is_alive():
                process.kill()
            process.join()
            process.close()


def measure(host, label, round_no):
    results = {}
    for method in ("getent", "python_in_process", "stage1_isolated_subprocess"):
        start = monotonic()
        addresses, error = [], None
        try:
            if method == "getent":
                output = subprocess.run(["getent", "ahosts", host], capture_output=True, timeout=TIMEOUT)
                if output.returncode:
                    error = f"exit_{output.returncode}_errno_unavailable"
                else:
                    addresses = sorted({line.split()[0] for line in output.stdout.decode().splitlines() if line.split()})
            elif method == "python_in_process":
                addresses, error = supervised_lookup(host, TIMEOUT)
            else:
                addresses = resolve(host, 443, TIMEOUT)
        except FileNotFoundError:
            error = "command_unavailable"
        except subprocess.TimeoutExpired:
            error = "watchdog_timeout"
        except Failure as exc:
            error = exc.reason
        results[method] = addresses
        emit(probe="dns", domain=label, round=round_no, method=method,
             success=bool(addresses), elapsed_s=elapsed(start), error_or_errno=error,
             address_count=len(addresses))
    return results


def https_head(host, addresses):
    if not addresses:
        emit(probe="https_head", domain=host, success=False, stage="dns", result="skipped_no_address")
        return False
    stage, start, timings = "address_policy", monotonic(), {}
    try:
        _, host, port, vetted = target(f"https://{host}/", TIMEOUT, lambda *_: addresses)
        address = min(vetted, key=lambda ip: ip_address(ip).version)
        family = socket.AF_INET if ip_address(address).version == 4 else socket.AF_INET6
        stage = "tcp"
        start = monotonic()
        with socket.socket(family, socket.SOCK_STREAM) as raw:
            raw.settimeout(TIMEOUT)
            raw.connect((address, port))
            if ip_address(raw.getpeername()[0]) != ip_address(address):
                raise Failure("peer_mismatch")
            timings["tcp_s"] = elapsed(start)
            stage = "tls"
            start = monotonic()
            with ssl.create_default_context().wrap_socket(raw, server_hostname=host) as secure:
                timings["tls_s"] = elapsed(start)
                stage = "http"
                start = monotonic()
                secure.sendall(f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode("ascii"))
                with http.client.HTTPResponse(secure, method="HEAD") as response:
                    response.begin()
                    status = response.status
        ok = 200 <= status < 400
        emit(probe="https_head", domain=host, success=ok, stage="http", status=status,
             http_s=elapsed(start), **timings)
        return ok
    except (OSError, Failure, http.client.HTTPException) as error:
        emit(probe="https_head", domain=host, success=False, stage=stage, elapsed_s=elapsed(start),
             error=type(error).__name__, errno=getattr(error, "errno", None), **timings)
        return False


def sample_domains(root):
    if not (root / "audit.sqlite").is_file():
        return []
    with closing(connect(root)) as db:
        successes = db.execute("SELECT url FROM source WHERE state='success_decode' ORDER BY url")
        resolved = list(dict.fromkeys(urlsplit(row["url"]).hostname for row in successes))[:2]
        failures = db.execute("SELECT url FROM source WHERE reason='dns_timeout' ORDER BY url")
        failed = next((host for row in failures if (host := urlsplit(row["url"]).hostname) not in resolved), None)
    result = [(host, f"dataset_previously_decoded_{i}") for i, host in enumerate(resolved, 1) if host]
    if failed:
        result.append((failed, "dataset_previous_dns_timeout"))
    return result


def local_startup(workers):
    def measure_local(_):
        start = monotonic()
        result = resolve("127.0.0.1", 443, TIMEOUT)
        assert result == ["127.0.0.1"]
        return elapsed(start)

    with ThreadPoolExecutor(workers) as pool:
        durations = list(pool.map(measure_local, range(8)))
    emit(probe="isolated_startup_numeric_no_dns", workers=workers, durations_s=durations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(".local/stage1"))
    args = parser.parse_args()
    emit(probe="environment", system=platform.system(), release=platform.release(),
         architecture=platform.machine(), python=platform.python_version(),
         tls=ssl.OPENSSL_VERSION, getent_available=bool(shutil.which("getent")),
         proxy_env_present=any(os.environ.get(k) for k in
                               ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "https_proxy", "http_proxy", "all_proxy")),
         proxy_used=False, timeout_s=TIMEOUT)
    for workers in (1, 4):
        local_startup(workers)
    healthy = True
    for round_no in (1, 2):
        for host in CONTROLS:
            results = measure(host, host, round_no)
            answers = results["stage1_isolated_subprocess"] or results["python_in_process"] or results["getent"]
            status = https_head(host, answers)
            healthy = healthy and all(results.values()) and status
            sleep(1)
    for host, label in sample_domains(args.root):
        measure(host, label, 1)
    emit(probe="decision", control_rounds=2, status="PASS" if healthy else "BLOCKED_BY_ENVIRONMENT")
    return 0 if healthy else 2


if __name__ == "__main__":
    raise SystemExit(main())
