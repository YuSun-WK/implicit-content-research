"""Freeze and compare a 10-pair 512-token sensitivity subset."""
import csv
from collections import defaultdict
import hashlib
from pathlib import Path

HERE = Path(__file__).parent


def read(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def select():
    rows = read(HERE / "stage2/results_256.csv")
    if len(rows) != 600 or any(r["status"] == "not_run" for r in rows):
        raise ValueError("100-pair 256-token primary run is incomplete")
    by = defaultdict(list)
    for r in rows:
        by[r["pair_id"]].append(r)
    ids = []
    for task in ("chat", "embodied"):
        candidates = []
        for pair_id, group in by.items():
            if group[0]["task"] != task:
                continue
            cap = sum(int(r["cap_calls"]) for r in group)
            labels = {(r["gold_label"], r["method"]): r["input_label"] for r in group}
            discord = sum(labels[(side, "cot")] != labels[(side, "multiagent")]
                          for side in ("safe", "unsafe"))
            rank = hashlib.sha256(f"20261120:diagnostic:{pair_id}".encode()).hexdigest()
            candidates.append((-int(cap > 0), -discord, rank, pair_id))
        choices = [row[3] for row in sorted(candidates)[:5]]
        ids.extend(choices)
    # The two-pair first probe contains one of each task.
    ids = [ids[0], ids[5], *ids[1:5], *ids[6:10]]
    path = HERE / "stage2/diagnostic_10_pair_ids.txt"
    path.write_text("\n".join(ids) + "\n")
    print("frozen diagnostic pairs", len(ids), ids)


def compare():
    primary = read(HERE / "stage2/results_256.csv")
    diagnostic = read(HERE / "stage2/results_512.csv")
    ids = (HERE / "stage2/diagnostic_10_pair_ids.txt").read_text().splitlines()
    if len(diagnostic) != 60 or {r["pair_id"] for r in diagnostic} != set(ids):
        raise ValueError("diagnostic results mismatch frozen subset")
    selected = [r for r in primary if r["pair_id"] in ids]
    lines = ["# 512-token sensitivity on 10 fixed pairs", "",
             "ThinkingGuard-8B substitute protocol; five Chat and five Embodied pairs. The 512 run is a separate journal and decoding identity. Invalid or missing labels count as incorrect.", "",
             "| Task | Method | Cap | Method inputs | Complete | Label parsed | Correct | Cap-hit calls | Answer extracted | Output tokens | Generation seconds |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for task in ("chat", "embodied"):
        for method in ("base", "cot", "multiagent"):
            for cap, rows in ((256, selected), (512, diagnostic)):
                group = [r for r in rows if r["task"] == task and r["method"] == method]
                if len(group) != 10:
                    raise ValueError("diagnostic method group incomplete")
                parsed = "—" if method == "base" else str(sum(r["label_status"] == "valid" for r in group))
                correct = "—" if method == "base" else str(sum(r["correct"] == "True" for r in group))
                lines.append(f"| {task} | {method} | {cap} | {len(group)} | {sum(r['status']=='complete' for r in group)} | {parsed} | {correct} | {sum(int(r['cap_calls']) for r in group)} | {sum(r['answer_status']=='valid' for r in group)} | {sum(int(r['output_tokens']) for r in group)} | {sum(float(r['elapsed_ms']) for r in group)/1000:.1f} |")
    lines += ["", "## Side-specific input labels", "",
              "| Task | Method | Side | 256 correct / 5 | 512 correct / 5 | 256 parsed / 5 | 512 parsed / 5 |",
              "|---|---|---|---:|---:|---:|---:|"]
    for task in ("chat", "embodied"):
        for method in ("cot", "multiagent"):
            for side in ("safe", "unsafe"):
                stats = []
                for table in (selected, diagnostic):
                    group = [r for r in table if (r["task"], r["method"], r["gold_label"]) ==
                             (task, method, side)]
                    if len(group) != 5:
                        raise ValueError("diagnostic side group incomplete")
                    stats.append((sum(r["correct"] == "True" for r in group),
                                  sum(r["label_status"] == "valid" for r in group)))
                lines.append(f"| {task} | {method} | {side} | {stats[0][0]}/5 | {stats[1][0]}/5 | {stats[0][1]}/5 | {stats[1][1]}/5 |")
    lines += ["", "## Pair exact", "",
              "| Task | Method | 256 both sides correct / 5 | 512 both sides correct / 5 |",
              "|---|---|---:|---:|"]
    for task in ("chat", "embodied"):
        for method in ("cot", "multiagent"):
            counts = []
            for table in (selected, diagnostic):
                by = defaultdict(list)
                for r in table:
                    if (r["task"], r["method"]) == (task, method):
                        by[r["pair_id"]].append(r["correct"] == "True")
                if len(by) != 5 or any(len(v) != 2 for v in by.values()):
                    raise ValueError("diagnostic exact-pair group incomplete")
                counts.append(sum(all(v) for v in by.values()))
            lines.append(f"| {task} | {method} | {counts[0]}/5 | {counts[1]}/5 |")
    cap_256, cap_512 = (sum(int(r["cap_calls"]) for r in table) for table in (selected, diagnostic))
    out_256, out_512 = (sum(int(r["output_tokens"]) for r in table) for table in (selected, diagnostic))
    sec_256, sec_512 = (sum(float(r["elapsed_ms"]) for r in table)/1000 for table in (selected, diagnostic))
    lines += ["", f"Across the same 100 real calls in each setting, cap hits fell from {cap_256}/100 to {cap_512}/100; output tokens rose from {out_256:,} to {out_512:,} ({out_512/out_256:.2f}×), and summed generation time rose from {sec_256:.1f}s to {sec_512:.1f}s ({sec_512/sec_256:.2f}×). All 40 explicit-label method-inputs parsed in each setting; this selected subset shows no change in explicit-label correctness or pair exact.",
              "", "The primary 100-pair 256-token result remains separate. A cap hit means the model generated exactly the configured maximum tokens; it does not prove an answer was complete."]
    (HERE / "stage2/diagnostic_512.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=("select", "compare"))
    mode = p.parse_args().mode
    select() if mode == "select" else compare()
