"""Prepare 30 diverse real traces for analyst inspection; do not auto-score behavior."""
import csv
from collections import defaultdict
import hashlib
import json
from pathlib import Path

from stage2_runner import frozen_rows

HERE = Path(__file__).parent


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    out = HERE / "stage2"
    rows = read_csv(out / "results_256.csv")
    if len(rows) != 600 or any(r["status"] in ("not_run", "engineering_error") for r in rows):
        raise ValueError("finish the 100-pair primary run before selecting review cases")
    frozen = {(r["pair_id"], r["gold_label"]): r for r in read_csv(out / "frozen_100_pairs.csv")}
    texts = {(r["pair_id"], r["gold_label"]): r["text"] for r in frozen_rows(
        out / "frozen_100_pairs.csv", HERE / ".stage0-local/stage1/data")}
    traces = defaultdict(list)
    with (out / "traces_256.jsonl").open() as stream:
        for lineno, line in enumerate(stream, 1):
            t = json.loads(line)
            traces[(t["pair_id"], t["gold_label"], t["method"])].append((lineno, t))
    selected = []
    for task in ("chat", "embodied"):
        for method in ("base", "cot", "multiagent"):
            for side, quota in (("safe", 2), ("unsafe", 3)):
                pool = [r for r in rows if (r["task"], r["method"], r["gold_label"]) ==
                        (task, method, side)]
                def rank(r):
                    incorrect = method != "base" and r["correct"] != "True"
                    digest = hashlib.sha256(f"20261120:review:{r['pair_id']}:{method}:{side}".encode()).hexdigest()
                    return (-int(r["status"] == "invalid"), -int(incorrect),
                            -int(int(r["cap_calls"]) > 0), digest)
                selected.extend(sorted(pool, key=rank)[:quota])
    if len(selected) != 30:
        raise ValueError("review queue should contain 30 method-inputs")
    path = out / "review_queue.jsonl"
    with path.open("w") as stream:
        for r in selected:
            key = r["pair_id"], r["gold_label"], r["method"]
            calls = traces[key]
            source = frozen[key[:2]]
            item = {k: r[k] for k in ("task", "pair_id", "gold_label", "method", "category",
                                       "subtask", "same_text", "image_path", "status",
                                       "input_label", "correct", "label_format", "cap_calls",
                                       "answer_status", "behavior")}
            item.update(query=texts[(r["pair_id"], r["gold_label"])],
                        text_sha256=source["text_sha256"], trace_lines=[n for n, _ in calls],
                        raw_agent_outputs=[{"role": t["role"], "raw_answer": t["raw_answer"],
                                            "parsed": t["parsed"], "route": t["route"],
                                            "cap_hit": t["cap_hit"]} for _, t in calls])
            stream.write(json.dumps(item, ensure_ascii=False) + "\n")
    print("review candidates", len(selected), "saved", path)


if __name__ == "__main__":
    main()
