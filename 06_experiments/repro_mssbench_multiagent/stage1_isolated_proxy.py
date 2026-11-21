"""Run a bounded model transfer through one existing sing-box node.

The temporary proxy configuration stays in the experiment's ignored cache and
is removed at exit. No node credentials are printed or copied into the repo.
"""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--node", type=int, default=10)
    parser.add_argument("--port", type=int, default=17991)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command:
        parser.error("command required")
    config = json.loads(Path("/etc/sing-box/config.json").read_text())
    nodes = [node for node in config["outbounds"]
             if node["type"] not in ("direct", "urltest", "selector", "block", "dns")]
    node = dict(nodes[args.node - 1])
    node["tag"] = "candidate"
    proxy_config = {
        "log": {"disabled": True},
        "inbounds": [{"type": "mixed", "listen": "127.0.0.1", "listen_port": args.port}],
        "outbounds": [node],
        "route": {"final": "candidate", "auto_detect_interface": True},
    }
    with tempfile.TemporaryDirectory(prefix="native-proxy-", dir=args.cache) as folder:
        path = Path(folder) / "config.json"
        path.write_text(json.dumps(proxy_config))
        path.chmod(0o600)
        proxy = subprocess.Popen(["sing-box", "run", "-c", str(path)],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(30):
                if proxy.poll() is not None:
                    raise RuntimeError("isolated proxy failed to start")
                try:
                    with socket.create_connection(("127.0.0.1", args.port), timeout=0.1):
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("isolated proxy did not listen")
            env = os.environ.copy()
            for key in ("http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
                env[key] = f"http://127.0.0.1:{args.port}"
            raise SystemExit(subprocess.call(args.command, env=env))
        finally:
            proxy.terminate()
            try:
                proxy.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proxy.kill()
                proxy.wait()


if __name__ == "__main__":
    main()
