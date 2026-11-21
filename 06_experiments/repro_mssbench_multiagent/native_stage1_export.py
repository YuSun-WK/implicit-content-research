"""Export canonical native G1/G2 calls while retaining all retry traces."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    results = list(csv.DictReader((args.run / "smoke_results.csv").open()))
    if len(results) != 120 or any(row["status"] not in ("complete", "invalid") for row in results):
        raise ValueError("unexpected native Smoke denominator or statuses")
    selected = {int(row["attempt_id"]) for row in results}
    if len(selected) != 120:
        raise ValueError("not one final attempt per method and input")
    all_traces = [json.loads(line) for line in (args.run / "agent_traces.jsonl").open()]
    canonical = [row for row in all_traces if row["attempt_id"] in selected]
    if len(canonical) != 200 or sum(row["gate"] == "g1" for row in canonical) != 20:
        raise ValueError("canonical native generation count differs from the protocol")
    (args.out / "canonical_agent_traces.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in canonical))
    (args.out / "retry_agent_traces.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n"
                for row in all_traces if row["attempt_id"] not in selected))
    values = {
        "method_inputs": len(results),
        "complete": sum(row["status"] == "complete" for row in results),
        "invalid": sum(row["status"] == "invalid" for row in results),
        "canonical_calls": len(canonical),
        "retry_calls": len(all_traces) - len(canonical),
        "all_retained_calls": len(all_traces),
        "canonical_input_tokens": sum(row.get("input_tokens") or 0 for row in canonical),
        "canonical_output_tokens": sum(row.get("output_tokens") or 0 for row in canonical),
        "canonical_generation_seconds": round(sum(row["elapsed_ms"] for row in canonical) / 1000, 3),
        "peak_allocated_bytes": max(row.get("peak_allocated_bytes") or 0 for row in canonical),
        "peak_reserved_bytes": max(row.get("peak_reserved_bytes") or 0 for row in canonical),
        "peak_nvml_delta_bytes": max(row.get("nvml_delta_bytes") or 0 for row in canonical),
        "role_calls": dict(Counter(row["role"] for row in canonical)),
        "qa_routes": dict(Counter(row["route"] for row in canonical if row["role"] == "qa")),
        "token_cap_calls": sum(row["output_tokens"] == 256 for row in canonical),
        "label_format": dict(Counter(row["label_format"] for row in results if row["method"] != "base")),
        "answer_unknown": sum(row["answer_status"] == "unknown" for row in results),
        "gates": {},
    }
    for gate in ("g1", "g2"):
        calls = [row for row in canonical if row["gate"] == gate]
        values["gates"][gate] = {
            "calls": len(calls),
            "input_tokens": sum(row.get("input_tokens") or 0 for row in calls),
            "output_tokens": sum(row.get("output_tokens") or 0 for row in calls),
            "generation_seconds": round(sum(row["elapsed_ms"] for row in calls) / 1000, 3),
        }
    (args.out / "canonical_summary.json").write_text(json.dumps(values, indent=2) + "\n")
    print(json.dumps(values, indent=2))


if __name__ == "__main__":
    main()
