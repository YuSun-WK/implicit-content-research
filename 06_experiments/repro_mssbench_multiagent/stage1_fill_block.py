"""Fill one stubborn pinned block through smaller checked HTTP ranges."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import time

import requests

from manifest import SOURCES
from stage1_weights import ARTIFACTS, locked_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--artifact", choices=ARTIFACTS, required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--block-mib", type=int, default=16)
    parser.add_argument("--subrange-mib", type=int, default=1)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    metadata = json.loads((root / f"{args.artifact}.metadata.json").read_text())
    entry = next(e for e in locked_files(metadata, args.artifact)
                 if e["rfilename"] == args.filename and "lfs" in e)
    model, revision_key, _ = ARTIFACTS[args.artifact]
    url = f"https://huggingface.co/{model}/resolve/{SOURCES[revision_key]}/{args.filename}"
    source = root / args.artifact / (args.filename + ".part")
    offset = source.stat().st_size if source.exists() else 0
    block_size = args.block_mib * 2**20
    sub_size = args.subrange_mib * 2**20
    start = offset + args.index * block_size
    end = min(start + block_size, entry["size"]) - 1
    if args.index < 0 or start >= entry["size"]:
        raise ValueError("block index outside pinned file")
    folder = root / args.artifact / (args.filename + f".blocks{args.block_mib}")
    parts = folder / (str(args.index) + f".subparts{args.subrange_mib}")
    parts.mkdir(exist_ok=True)
    for index in range(math.ceil((end - start + 1) / sub_size)):
        lo = start + index * sub_size
        hi = min(lo + sub_size, end + 1) - 1
        target = parts / str(index)
        if target.exists() and target.stat().st_size == hi - lo + 1:
            continue
        for attempt in range(1, 5):
            tmp = parts / f"{index}.tmp"
            tmp.unlink(missing_ok=True)
            try:
                with requests.get(url + f"?nodeprobe={time.time_ns()}",
                                  headers={"Range": f"bytes={lo}-{hi}"},
                                  stream=True, timeout=(10, 35)) as response:
                    if response.status_code != 206 or response.headers.get("Content-Range") != f"bytes {lo}-{hi}/{entry['size']}":
                        raise ValueError("invalid subrange response")
                    with tmp.open("wb") as output:
                        count = 0
                        for chunk in response.iter_content(2**20):
                            count += len(chunk)
                            output.write(chunk)
                        output.flush()
                        os.fsync(output.fileno())
                    if count != hi - lo + 1:
                        raise ValueError("short subrange response")
                    tmp.replace(target)
                    print("accepted subrange", index + 1, "/", math.ceil((end - start + 1) / sub_size), flush=True)
                    break
            except Exception as exc:
                print("subrange error", index, attempt, type(exc).__name__, flush=True)
            finally:
                tmp.unlink(missing_ok=True)
        else:
            raise RuntimeError(f"subrange {index} failed in bounded retries")
    assembled = folder / (str(args.index) + ".tmp")
    digest = hashlib.sha256()
    with assembled.open("wb") as output:
        for index in range(math.ceil((end - start + 1) / sub_size)):
            with (parts / str(index)).open("rb") as stream:
                for chunk in iter(lambda: stream.read(2**20), b""):
                    output.write(chunk)
                    digest.update(chunk)
        output.flush()
        os.fsync(output.fileno())
    if assembled.stat().st_size != end - start + 1:
        raise ValueError("assembled block length mismatch")
    assembled.replace(folder / str(args.index))
    (folder / f"{args.index}.json").write_text(json.dumps({"bytes": end - start + 1,
                                                               "sha256": digest.hexdigest()}))
    print("block complete", args.artifact, args.filename, args.index, flush=True)


if __name__ == "__main__":
    main()
