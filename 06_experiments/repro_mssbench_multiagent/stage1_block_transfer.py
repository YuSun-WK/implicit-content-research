"""Durable, bounded HTTP Range transfer of pinned original LLaVA/CLIP weights."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import time

import requests

from stage1_weights import ARTIFACTS, locked_files, verify_file
from manifest import SOURCES


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--block-mib", type=int, default=16)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--hours", type=float, default=6)
    parser.add_argument("--rounds", type=int, default=5)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    block_size = args.block_mib * 2**20
    deadline = time.monotonic() + args.hours * 3600
    work = []
    for artifact, (model, revision_key, _) in ARTIFACTS.items():
        metadata = json.loads((root / f"{artifact}.metadata.json").read_text())
        for entry in locked_files(metadata, artifact):
            if "lfs" not in entry or entry["size"] < 2**30:
                continue
            target = root / artifact / entry["rfilename"]
            if target.exists():
                verify_file(target, entry)
                print("verified existing", artifact, target.name, flush=True)
                continue
            prefix = target.with_suffix(target.suffix + ".part")
            offset = prefix.stat().st_size if prefix.exists() else 0
            if offset >= entry["size"]:
                raise ValueError(f"invalid prefix length: {prefix}")
            blocks = root / artifact / (entry["rfilename"] + f".blocks{args.block_mib}")
            blocks.mkdir(exist_ok=True)
            url = f"https://huggingface.co/{model}/resolve/{SOURCES[revision_key]}/{entry['rfilename']}"
            work.append((artifact, entry, target, prefix, offset, blocks, url))

    def fetch(item, index):
        artifact, entry, target, prefix, offset, blocks, url = item
        start = offset + index * block_size
        end = min(start + block_size, entry["size"]) - 1
        dest = blocks / str(index)
        receipt = blocks / f"{index}.json"
        if dest.exists() and receipt.exists():
            recorded = json.loads(receipt.read_text())
            if dest.stat().st_size == end - start + 1 and sha256(dest) == recorded.get("sha256"):
                return True
        for attempt in range(3):
            if time.monotonic() >= deadline:
                return False
            started = time.monotonic()
            temporary = blocks / f"{index}.tmp"
            temporary.unlink(missing_ok=True)
            try:
                with requests.get(url + f"?nodeprobe={time.time_ns()}",
                                  headers={"Range": f"bytes={start}-{end}"},
                                  stream=True, timeout=(10, 45)) as response:
                    if response.status_code != 206 or response.headers.get("Content-Range") != f"bytes {start}-{end}/{entry['size']}":
                        raise ValueError("HTTP Range response mismatch")
                    count = 0
                    digest = hashlib.sha256()
                    with temporary.open("wb") as stream:
                        for chunk in response.iter_content(2**20):
                            if time.monotonic() >= deadline:
                                raise TimeoutError("global transfer deadline")
                            count += len(chunk)
                            if count > end - start + 1:
                                raise ValueError("Range overflow")
                            stream.write(chunk)
                            digest.update(chunk)
                        stream.flush()
                        os.fsync(stream.fileno())
                    if count != end - start + 1:
                        raise ValueError("short Range body")
                    temporary.replace(dest)
                    receipt.write_text(json.dumps({"bytes": count, "sha256": digest.hexdigest()}))
                    return True
            except Exception as exc:
                print("block error", artifact, target.name, index, attempt + 1,
                      type(exc).__name__, round(time.monotonic() - started, 2), flush=True)
            finally:
                temporary.unlink(missing_ok=True)
        return False

    for round_number in range(1, args.rounds + 1):
        pending = []
        for item in work:
            size = item[1]["size"]
            offset = item[4]
            pending.extend((item, index) for index in range(math.ceil((size - offset) / block_size)))
        print("round", round_number, "blocks", len(pending), flush=True)
        successes = failures = 0
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(fetch, item, index) for item, index in pending]
            for future in as_completed(futures):
                if future.result():
                    successes += 1
                else:
                    failures += 1
                if (successes + failures) % 50 == 0:
                    print("progress", successes + failures, len(pending), "failed", failures, flush=True)
        print("round complete", round_number, successes, failures, flush=True)
        if failures == 0 or time.monotonic() >= deadline:
            break

    for artifact, entry, target, prefix, offset, blocks, url in work:
        count = math.ceil((entry["size"] - offset) / block_size)
        if any(not (blocks / str(index)).is_file() for index in range(count)):
            print("incomplete", artifact, target.name, flush=True)
            continue
        assembly = target.with_suffix(target.suffix + ".assembling")
        with assembly.open("wb") as output:
            if prefix.exists():
                with prefix.open("rb") as stream:
                    shutil.copyfileobj(stream, output)
            for index in range(count):
                with (blocks / str(index)).open("rb") as stream:
                    shutil.copyfileobj(stream, output)
            output.flush()
            os.fsync(output.fileno())
        try:
            verified = verify_file(assembly, entry)
        except ValueError:
            assembly.unlink(missing_ok=True)
            raise
        assembly.replace(target)
        print("official verified", artifact, target.name, verified["sha256"], flush=True)
    if any(not item[2].exists() for item in work):
        raise RuntimeError("one or more pinned weights remain incomplete")


if __name__ == "__main__":
    main()
