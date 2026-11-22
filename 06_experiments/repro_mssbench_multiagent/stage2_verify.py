"""Independently recheck canonical real Agent traces from all Stage 2 journals."""
from collections import Counter
from pathlib import Path

from journal import run_key
from pipeline import load_prompts
from stage1_smoke import validate_traces
from stage2_export import HERE, ROOT, expected_work, read_snapshot, sources
from stage2_runner import frozen_rows


def verify(tokens, rows, prompts):
    expected = {run_key(w.config): w.config for w in expected_work(rows, tokens)}
    found = {}
    role_counts = Counter()
    max_allocated = max_reserved = max_nvml = 0
    for path in sources(tokens):
        if not path.is_file():
            raise ValueError(f"missing journal: {path}")
        for attempt in read_snapshot(path):
            key = attempt["key"]
            if key not in expected:
                continue
            if key in found and found[key] in ("complete", "invalid"):
                raise ValueError("duplicate terminal run key")
            status = attempt["status"]
            if status not in ("complete", "invalid"):
                raise ValueError(f"unfinished canonical attempt: {key}: {status}")
            config = expected[key]
            validate_traces(config, attempt["traces"], prompts, allow_invalid=status == "invalid")
            found[key] = status
            for call in attempt["traces"]:
                role_counts[call["role"]] += 1
                max_allocated = max(max_allocated, call.get("peak_allocated_bytes") or 0)
                max_reserved = max(max_reserved, call.get("peak_reserved_bytes") or 0)
                max_nvml = max(max_nvml, call.get("nvml_delta_bytes") or 0)
    if set(found) != set(expected):
        raise ValueError(f"canonical keys missing: {len(expected) - len(found)}")
    return found, role_counts, max_allocated, max_reserved, max_nvml


if __name__ == "__main__":
    root = HERE / "stage2"
    rows = frozen_rows(root / "frozen_100_pairs.csv", ROOT / "stage1/data")
    prompts = load_prompts(Path("/tmp/mssbench-stage0-official"))
    for tokens in (256, 512):
        selected = rows
        if tokens == 512:
            ids = (root / "diagnostic_10_pair_ids.txt").read_text().splitlines()
            selected = [r for r in rows if r["pair_id"] in ids]
        found, roles, allocated, reserved, nvml = verify(tokens, selected, prompts)
        print(f"{tokens}: {len(found)} canonical method-inputs; "+
              f"status={dict(Counter(found.values()))}; roles={dict(roles)}; "+
              f"peaks GiB allocated={allocated/1024**3:.3f} reserved={reserved/1024**3:.3f} "+
              f"NVML delta={nvml/1024**3:.3f}")
