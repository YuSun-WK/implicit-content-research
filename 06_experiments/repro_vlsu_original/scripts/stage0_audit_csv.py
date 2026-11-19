"""Audit the pinned Apple VLSU release without network or image access."""

import argparse
from collections import Counter
import csv
from hashlib import sha1, sha256
from io import StringIO
from itertools import product
import json
from pathlib import Path
from uuid import UUID

from stage0_metrics import LABELS, gold_label

FIELDS = (
    "prompt", "image_grade", "consensus_text_grade", "consensus_combined_grade",
    "image_category", "text_category", "combined_category", "web_path", "uuid",
)
GRADE_FIELDS = FIELDS[1:4]
REQUIRED = {"prompt", "web_path", "uuid", *GRADE_FIELDS}
APPLE_REV = "cbe363a26d2129ff1b526c283af0a2b7aa3d9b28"
APPLE_BLOB = "09421adeb2e68eac1d5e829dcbd48848f21a0be6"
CSV_SHA256 = "9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f"
FIGURE9_LEGEND = {
    "S-S-S": 2175, "S-U-U": 1024, "U-S-B": 956, "B-S-B": 911, "S-B-B": 907,
    "U-U-U": 768, "B-U-U": 608, "B-B-B": 274, "U-B-B": 204, "U-S-U": 150,
    "S-S-B": 59, "B-S-U": 46, "S-S-U": 37, "B-B-U": 33, "U-B-U": 14,
    "S-B-S": 10, "S-B-U": 9,
}
EXTRA = {"B-S-S": 1, "S-U-B": 1}
EXPECTED_PATTERNS = {"S-S-U": 35, "S-S-B": 58, "U-S-B": 924, "U-S-U": 142, "B-B-U": 32}
PATTERNS = tuple("-".join(parts) for parts in product("SBU", repeat=3))
QUESTION_PATTERNS = tuple(f"?-{t}-{j}" for t, j in product("SBU", repeat=2))


def read_rows(raw):
    """Return structurally usable rows and private diagnostics (no content echoed)."""
    try:
        stream = StringIO(raw.decode("utf-8"), newline="")
    except UnicodeDecodeError as error:
        return [], [{"error": "invalid_utf8", "byte": error.start}], 0
    reader = csv.reader(stream, strict=True)
    rows, errors = [], []
    record = 0
    try:
        if tuple(next(reader, ())) != FIELDS:
            return [], [{"line": 1, "error": "invalid_header"}], 0
        for values in reader:
            record += 1
            if len(values) != len(FIELDS):
                errors.append({"line": reader.line_num, "record": record,
                               "error": "column_count", "actual": len(values)})
                continue
            rows.append((record, dict(zip(FIELDS, values))))
    except csv.Error:
        errors.append({"line": reader.line_num, "record": record + 1, "error": "invalid_csv"})
    return rows, errors, record


def audit(raw):
    rows, errors, n_rows = read_rows(raw)
    labels = {field: Counter() for field in GRADE_FIELDS}
    empty = dict.fromkeys(FIELDS, 0)
    identifiers = {field: set() for field in ("uuid", "web_path", "prompt")}
    patterns, ceilings = Counter(), Counter()
    for record, row in rows:
        def error(reason, field):
            errors.append({"record": record, "uuid": row["uuid"], "field": field, "error": reason})

        for field, value in row.items():
            if not value.strip():
                empty[field] += 1
                if field in REQUIRED:
                    error("blank_required_field", field)
        for field, seen in identifiers.items():
            if row[field].strip():
                if field == "uuid":
                    try:
                        value = UUID(row[field])
                    except ValueError:
                        error("invalid_uuid", field)
                        continue
                    if value in seen:
                        error("duplicate_uuid", field)
                    seen.add(value)
                else:
                    seen.add(row[field])

        normalized = []
        for field in GRADE_FIELDS:
            value = row[field]
            if value in LABELS:
                normalized.append(gold_label(value)[0].upper())
            elif field == "image_grade" and value == "not_sure":
                normalized.append("?")
            else:
                error("invalid_grade", field)
                normalized.append(None)
                continue
            labels[field][value] += 1
        image, query, joint = normalized
        has_url, has_text = bool(row["web_path"].strip()), bool(row["prompt"].strip())
        ceilings["E1_image"] += bool(image in {"S", "B", "U"} and has_url)
        ceilings["E1_text"] += bool(query and has_text)
        ceilings["E1_joint"] += bool(joint and has_url and has_text)
        if all(normalized):
            pattern = "-".join(normalized)
            patterns[pattern] += 1
            ceilings["E4_paper_patterns"] += bool(pattern in FIGURE9_LEGEND and has_url and has_text)
            ceilings["E4_release_extras"] += bool(pattern in EXTRA and has_url and has_text)
            ceilings["E4_image_not_sure"] += bool(image == "?" and has_url and has_text)
            ceilings["Figures4_5_three_valid_gold"] += bool(image != "?" and has_url and has_text)

    for task in ("E2_binary_joint", "E3_direct_joint", "E5_paired_direct_cot"):
        ceilings[task] = ceilings["E1_joint"]
    ceilings["E6_error_decomposition"] = ceilings["Figures4_5_three_valid_gold"]
    ceilings["E7_behavior_joint"] = ceilings["E1_joint"]
    ceilings["E1_E2_E5_generations_reusing_direct"] = sum(
        ceilings[task] for task in ("E1_image", "E1_text", "E1_joint", "E2_binary_joint", "E5_paired_direct_cot")
    )
    manifest = {
        "schema_version": 1, "source": "https://github.com/apple-aiml-research/ml-vlsu",
        "path": "data/VLSU.csv", "reference_commit": APPLE_REV,
        "expected_git_blob": APPLE_BLOB, "git_blob": sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest(),
        "expected_sha256": CSV_SHA256, "sha256": sha256(raw).hexdigest(), "bytes": len(raw),
    }
    summary = {
        "schema_version": 1, "rows": n_rows, "nine_column_rows": len(rows), "columns": list(FIELDS),
        "unique_uuid": len(identifiers["uuid"]), "unique_url": len(identifiers["web_path"]),
        "unique_prompt": len(identifiers["prompt"]), "blank_fields": empty, "labels": labels,
        "schema_errors": len(errors), "observed_patterns": len(patterns),
        "standard_patterns_observed": sum(p in patterns for p in PATTERNS),
        "question_patterns_observed": sum(p in patterns for p in QUESTION_PATTERNS),
        "paper_patterns_observed": sum(p in patterns for p in FIGURE9_LEGEND),
        "release_extra_standard_patterns": {p: patterns[p] for p in PATTERNS
                                            if p in patterns and p not in FIGURE9_LEGEND},
        "theoretical_ceilings": dict(ceilings), "image_availability": "NOT RUN",
    }
    expected = {"rows": 8159, "nine_column_rows": 8159, "unique_uuid": 8159, "unique_url": 8157,
                "unique_prompt": 7638, "schema_errors": 0, "observed_patterns": 25,
                "standard_patterns_observed": 19, "question_patterns_observed": 6,
                "paper_patterns_observed": 17, "release_extra_standard_patterns": EXTRA}
    checks = {key: summary[key] == value for key, value in expected.items()}
    checks.update({
        "image_not_sure_141": labels["image_grade"]["not_sure"] == 141,
        "git_blob": manifest["git_blob"] == APPLE_BLOB,
        "sha256": manifest["sha256"] == CSV_SHA256,
        **{f"pattern_{p}": patterns[p] == value for p, value in EXPECTED_PATTERNS.items()},
    })
    summary["checks"] = checks
    summary["status"] = "PASS" if all(checks.values()) else "BLOCK"
    manifest["pinned_bytes_verified"] = checks["git_blob"] and checks["sha256"]
    return summary, manifest, patterns, errors


def write_reports(out, summary, manifest, patterns, errors):
    out.mkdir(parents=True, exist_ok=True)
    for name, data in (("dataset_audit", summary), ("version_manifest", manifest)):
        (out / f"{name}.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (out / "patterns.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["pattern", "group", "release_n", "figure9_legend_n"])
        for pattern in (*PATTERNS, *QUESTION_PATTERNS):
            if pattern in FIGURE9_LEGEND:
                group = "paper17"
            elif pattern.startswith("?"):
                group = "image_not_sure"
            elif patterns[pattern]:
                group = "release_extra"
            else:
                group = "unobserved_standard"
            writer.writerow([pattern, group, patterns[pattern], FIGURE9_LEGEND.get(pattern, "")])
    private = out / "schema_errors.jsonl"
    with private.open("w", encoding="utf-8") as stream:
        private.chmod(0o600)
        for error in errors:
            stream.write(json.dumps(error, ensure_ascii=False) + "\n")
    lines = [
        "# Stage 0 CSV audit", "",
        f"**{summary['status']}** · SHA-256 `{manifest['sha256']}`.", "",
        f"{summary['rows']} records, {summary['nine_column_rows']} with nine columns, "
        f"{summary['unique_uuid']} unique UUIDs, {summary['unique_url']} unique URLs and "
        f"{summary['unique_prompt']} unique prompts. Schema errors {len(errors)}.", "",
        "## Theoretical upper bounds before downloading or decoding images", "",
        "| Task | Count |", "|---|---:|",
    ]
    lines.extend(f"| {task} | {count} |" for task, count in summary["theoretical_ceilings"].items())
    lines.extend(["", "## Gold safety labels", "",
                  "| Field | Safe | Borderline | Unsafe | not_sure |", "|---|---:|---:|---:|---:|"])
    for field, counts in summary["labels"].items():
        values = " | ".join(str(counts.get(label, 0)) for label in (*LABELS, "not_sure"))
        lines.append(f"| {field} | {values} |")
    lines.extend(["", "Image availability **NOT RUN**. The paper describes 8,187 pairs. "
                  "See the experiment matrix and patterns table for comparisons."])
    (out / "CSV_Audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        for filename in ("dataset_audit.json", "version_manifest.json", "patterns.csv", "schema_errors.jsonl", "CSV_Audit.md"):
            destination = args.out / filename
            if destination.resolve() == args.csv.resolve() or (
                destination.exists() and destination.samefile(args.csv)
            ):
                parser.error("report path aliases the source CSV")
        result = audit(args.csv.read_bytes())
        write_reports(args.out, *result)
    except OSError as error:
        parser.exit(2, f"BLOCK: {error}\n")
    summary, manifest, _, _ = result
    print(f"{summary['status']}: rows={summary['rows']}, sha256={manifest['sha256']}")
    if summary["status"] != "PASS":
        print("Failed checks:", ", ".join(key for key, ok in summary["checks"].items() if not ok))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
