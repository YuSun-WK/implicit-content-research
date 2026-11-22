"""Archive lossless GPU telemetry and distinguish resumed-job wall times."""
import argparse
import gzip
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path)
    args = ap.parse_args()
    run = args.run_dir
    raw = run / "gpu_samples.jsonl"
    records = [json.loads(line) for line in raw.read_text().splitlines()]
    groups = defaultdict(list)
    for record in records:
        groups[record["job_id"]].append(record)
    summary = json.loads((run / "summary.json").read_text())
    jobs = []
    for job_path in sorted(run.glob("job-*.json")):
        job = json.loads(job_path.read_text())
        jid = job_path.stem[4:]
        samples = groups[jid]
        elapsed = (datetime.fromisoformat(samples[-1]["utc"])-
                   datetime.fromisoformat(job["start_utc"])).total_seconds()
        jobs.append({"job_id": jid, "start_utc": job["start_utc"],
            "last_telemetry_utc": samples[-1]["utc"],
            "last_telemetry_elapsed_seconds": elapsed,
            "terminal": samples[-1].get("abort", "COMPLETE"),
            "gpu_uuid": job["gid"]["uuid"], "gpu_samples": len(samples),
            "process_peak_mib": max(x["process_mib"] for x in samples if x.get("process_mib") is not None),
            "card_peak_mib": max(x["used_mib"] for x in samples if x.get("used_mib") is not None)})
    jobs[-1]["job_wall_seconds"] = summary["job_wall_seconds"]
    wall_lower = sum(x["last_telemetry_elapsed_seconds"] for x in jobs[:-1])+summary["job_wall_seconds"]
    compressed = run / "gpu_samples.jsonl.gz"
    compressed.write_bytes(gzip.compress(raw.read_bytes(), compresslevel=9, mtime=0))
    assert gzip.decompress(compressed.read_bytes()) == raw.read_bytes()
    predictions = [json.loads(line) for line in (run / "predictions.jsonl").read_text().splitlines()]
    output = {"jobs": jobs, "prediction_rows": len(predictions),
              "total_generation_seconds": sum(x["elapsed"] for x in predictions),
              "total_measured_gpu_wall_lower_bound_seconds": wall_lower,
              "process_peak_mib": max(x["process_peak_mib"] for x in jobs),
              "card_peak_mib": max(x["card_peak_mib"] for x in jobs),
              "gpu_samples_raw_sha256": digest(raw),
              "gpu_samples_gzip_sha256": digest(compressed),
              "gpu_samples_archived_as": "gpu_samples.jsonl.gz (lossless gzip mtime=0)"}
    (run / "resource_accounting.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"prediction_rows":len(predictions),"wall_seconds_lower_bound":wall_lower,
                      "process_peak_mib":output["process_peak_mib"]}))


if __name__ == "__main__":
    main()
