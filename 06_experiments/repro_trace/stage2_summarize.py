"""Validate and aggregate Stage 2 event logs without exporting sample records."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import statistics


def p95(values):
    return sorted(values)[math.ceil(len(values) * 0.95) - 1]


def summarize(path, require_formal=False):
    events = [json.loads(line) for line in path.read_text().splitlines()]
    if not events or events[-1]["event"] not in {"completed", "test_completed"}:
        raise ValueError("Run did not complete")
    batches = [event for event in events if event["event"] == "batch"]
    if not batches or any(not math.isfinite(event["loss"]) or any(
            not math.isfinite(value) for value in event["components"].values()) for event in batches):
        raise ValueError("Missing or nonfinite batch losses")
    if [event["cursor"] for event in batches] != list(range(1, len(batches) + 1)):
        raise ValueError("Training cursor gap or duplicate")
    checkpoints = [event["cursor"] for event in events if event["event"] == "checkpoint_restored"]
    if checkpoints != sorted(set(checkpoints)) or max(b - a for a, b in zip([0] + checkpoints[:-1], checkpoints)) > 25:
        raise ValueError("Checkpoint interval exceeds 25 microbatches")
    if checkpoints[-1] != len(batches):
        raise ValueError("Final checkpoint was not restored")
    epochs = defaultdict(list)
    for event in batches:
        epochs[event["epoch"]].append(event)
    dev = {event["epoch"]: event for event in events if event["event"] == "epoch_dev"}
    epoch_rows = []
    for number, items in sorted(epochs.items()):
        components = {name: statistics.mean(item["components"][name] for item in items)
                      for name in ("classification", "contrastive", "relevance")}
        epoch_rows.append({"epoch": number, "microbatches": len(items),
                           "train_loss_mean": statistics.mean(item["loss"] for item in items),
                           "train_components_mean": components,
                           "train_caption_selected": {
                               "original": sum(item["selected_original"] for item in items),
                               "internvl": sum(item["selected_internvl"] for item in items)},
                           "dev": {key: value for key, value in dev.get(number, {}).items()
                                   if key not in {"event", "elapsed_s", "phase", "epoch"}} or None})
    durations = [event["seconds"] for event in batches]
    complete = next(event for event in reversed(events) if event["event"] == "completed")
    segment_ends = [event for event in events if event["event"] in {"interrupted", "completed"}]
    segment_seconds = [event["elapsed_s"] for event in segment_ends]
    result = {"protocol": events[0]["signature"]["protocol"], "phase": events[0]["phase"],
              "microbatches": len(batches), "optimizer_updates": complete["updates"],
              "elapsed_s": sum(segment_seconds), "segment_elapsed_s": segment_seconds,
              "step_p50_s": statistics.median(durations),
              "step_p95_s": p95(durations),
              "peak_allocated_gib": complete["allocated_bytes"] / 1024**3,
              "peak_reserved_gib": complete["reserved_bytes"] / 1024**3,
              "checkpoint_cursors": checkpoints, "cross_process_resume": any(
                  event["event"] == "resumed" for event in events),
              "epochs": epoch_rows, "best_epoch": complete.get("best_epoch")}
    if events[-1]["event"] == "test_completed":
        result["test_evaluation_elapsed_s"] = events[-1]["elapsed_s"]
    finals = [event for event in events if event["event"] == "final_metrics"]
    if require_formal:
        if len([event for event in finals if event["split"] == "test"]) != 1:
            raise ValueError("Formal run must contain exactly one Test evaluation")
        result["final_metrics"] = {event["split"]: {key: value for key, value in event.items()
                                                    if key not in {"event", "elapsed_s", "phase", "split"}}
                                   for event in finals}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formal", action="store_true")
    args = parser.parse_args()
    args.output.write_text(json.dumps(summarize(args.events, args.formal), indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
