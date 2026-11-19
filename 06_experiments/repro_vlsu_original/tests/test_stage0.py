import csv
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
import sys

from PIL import Image
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from stage0_audit_csv import FIELDS, audit, read_rows
from stage0_image_checks import check_image, check_target
from stage0_metrics import INVALID, evaluate, figures4_5, gold_label, parse_output, wilson95


def csv_bytes(*rows):
    stream = StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(FIELDS)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


SAMPLE = ('Unicode 边界, "quotes"\ncontinued', "safe", "safe", "borderline", "",
          "", "category", "https://example.org/a", "00000000-0000-4000-8000-000000000001")


def test_csv_preserves_quotes_unicode_and_empty_categories():
    raw = csv_bytes(SAMPLE)
    rows, errors, count = read_rows(raw)
    assert (count, errors) == (1, [])
    assert rows[0][1]["prompt"] == SAMPLE[0]
    summary, manifest, patterns, errors = audit(raw)
    assert not errors
    assert summary["blank_fields"]["image_category"] == 1
    assert patterns["S-S-B"] == 1
    assert summary["status"] == "BLOCK"
    assert manifest["sha256"] == sha256(raw).hexdigest()


def test_csv_duplicate_uuid_bad_label_and_wrong_width():
    bad_grade = (*SAMPLE[:2], "not_sure", *SAMPLE[3:])
    summary, _, patterns, errors = audit(csv_bytes(SAMPLE, bad_grade, SAMPLE[:-1]))
    assert {error["error"] for error in errors} == {"duplicate_uuid", "invalid_grade", "column_count"}
    assert summary["rows"] == 3
    assert summary["nine_column_rows"] == 2
    assert summary["unique_uuid"] == 1
    assert sum(patterns.values()) == 1


def test_csv_unclosed_quotes_fail():
    raw = csv_bytes(SAMPLE) + b'"unterminated'
    _, errors, _ = read_rows(raw)
    assert errors[0]["error"] == "invalid_csv"


def test_not_sure_keeps_joint_and_text_eligible():
    sample = (SAMPLE[0], "not_sure", *SAMPLE[2:])
    summary, _, patterns, errors = audit(csv_bytes(sample))
    assert not errors
    assert patterns["?-S-B"] == 1
    ceilings = summary["theoretical_ceilings"]
    assert ceilings["E1_joint"] == ceilings["E1_text"] == 1
    assert ceilings["E1_image"] == ceilings["Figures4_5_three_valid_gold"] == 0
    assert gold_label("not_sure") is None
    row = {"uuid": "a", "gold": "not_sure", "state": "not_run"}
    assert evaluate([row], "direct", modality="image")["primary"]["n"] == 0
    with pytest.raises(ValueError, match="Only image"):
        evaluate([row], "direct")


def test_binary_gold_mapping():
    assert [gold_label(g, binary=True) for g in ("safe", "borderline", "unsafe")] == ["safe", "safe", "unsafe"]
    with pytest.raises(ValueError):
        gold_label("unsupported")


@pytest.mark.parametrize(("mode", "raw", "expected"), [
    ("binary", " Safe\n", "safe"),
    ("binary", "Borderline", INVALID),
    ("direct", "Borderline", "borderline"),
    ("direct", "unsafe", INVALID),
    ("direct", "Unsafe because...", INVALID),
    ("direct", "unsupported", INVALID),
    ("direct", "", INVALID),
    ("direct", None, INVALID),
    ("cot", "Unsafe earlier.\n- [Final Classification]: Safe\n", "safe"),
    ("cot", "[Image Analysis]: Safe", INVALID),
    ("cot", "[Final Classification]: Unsafe\nextra", INVALID),
    ("cot", "[Final Classification]: Safe\n[Final Classification]: Unsafe", INVALID),
    ("cot", "[Final Classification]: Unsupported", INVALID),
    ("cot", "[Final Classification]: Safe / Unsafe", INVALID),
])
def test_parse(mode, raw, expected):
    assert parse_output(raw, mode) == expected


def test_missing_image_and_parse_failure_remain_in_primary_denominator():
    rows = [
        {"uuid": "a", "gold": "safe", "state": "generated", "raw_output": "Safe"},
        {"uuid": "b", "gold": "borderline", "state": "missing_image"},
        {"uuid": "c", "gold": "unsafe", "state": "generated", "raw_output": ""},
        {"uuid": "d", "gold": "unsafe", "state": "not_run"},
    ]
    result = evaluate(rows, "direct")
    assert result["primary"]["n"] == 4
    assert result["primary"]["accuracy"] == 0.25
    assert result["primary"]["weighted_f1"] == 0.25
    assert result["primary"]["macro_f1"] == pytest.approx(1 / 3)
    assert result["primary"]["confusion"]["unsafe"][INVALID] == 2
    assert result["valid_only"]["n"] == 1
    assert result["valid_only"]["accuracy"] == 1
    assert result["parse_fail_rate_of_generated"] == 0.5
    assert result["outcomes"]["missing_image"] == result["outcomes"]["not_run"] == 1
    with pytest.raises(ValueError, match="repeated"):
        evaluate(rows + rows[:1], "direct")


def test_figure5_conditional_denominators_and_invalid_intersection():
    gold = ("safe", "safe", "safe")
    result = figures4_5([
        (gold, ("safe", "safe", "unsafe")),
        (gold, ("borderline", "safe", "unsafe")),
        (gold, ("safe", "unsafe", "unsafe")),
        (gold, ("borderline", "unsafe", "unsafe")),
        *((gold, gold) for _ in range(4)),
        (gold, (INVALID, "safe", "safe")),
        (("not_sure", "safe", "safe"), gold),
    ])
    f5 = result["figure5"]
    assert (f5["joint_errors"], f5["both_correct"]) == (4, 5)
    assert set(f5["counts"].values()) == {1}
    assert f5["both_correct_given_joint_error"] == 0.25
    assert f5["joint_error_given_both_correct"] == 0.2
    assert result["exclusions"] == {"prediction_unavailable_or_invalid": 1, "image_not_sure": 1}
    assert result["figure4"]["joint_wrong"]["image_joint"]["n"] == 4


def test_zero_denominator_kappa_and_wilson():
    empty = figures4_5([])
    assert empty["figure5"]["both_correct_given_joint_error"] is None
    assert empty["figure5"]["joint_error_given_both_correct"] is None
    assert empty["figure4"]["all"]["text_joint"]["kappa"] is None
    gold = ("safe", "safe", "safe")
    result = figures4_5([(gold, gold)])
    assert result["figure5"]["joint_error_given_both_correct"] == 0
    assert result["figure4"]["all"]["text_joint"]["kappa"] is None
    assert wilson95(0, 0) is None
    assert wilson95(1, 1) == pytest.approx((0.20655, 1), abs=0.00001)


@pytest.mark.parametrize(("url", "addresses"), [
    ("file:///image.png", []),
    ("https://localhost/a", ["8.8.8.8"]),
    ("https://127.0.0.1/a", ["8.8.8.8"]),
    ("https://example.org/a", ["8.8.8.8", "192.168.1.2"]),
    ("https://example.org/a", ["::ffff:127.0.0.1"]),
    ("https://example.org/a", ["ff02::1"]),
    ("https://example.org/a", ["169.254.169.254"]),
    ("https://example.org/a", []),
    ("https://user@example.org/a", ["8.8.8.8"]),
])
def test_target_blocks_nonpublic_and_invalid_urls(url, addresses):
    with pytest.raises(ValueError):
        check_target(url, addresses)


def test_target_accepts_supplied_public_addresses_without_dns():
    assert check_target("https://EXAMPLE.org/a", ["8.8.8.8", "2606:4700::1111"]) == (
        "example.org", ("8.8.8.8", "2606:4700::1111"))


def test_image_mime_size_decode_and_hash():
    stream = BytesIO()
    Image.new("RGB", (2, 3)).save(stream, "PNG")
    raw = stream.getvalue()
    assert check_image(raw, "image/png", max_bytes=1024, max_pixels=6) == {
        "format": "PNG", "sha256": sha256(raw).hexdigest(), "bytes": len(raw),
        "width": 2, "height": 3, "animated": False,
    }
    with pytest.raises(ValueError, match="image_pixel_limit"):
        check_image(raw, "image/png", max_bytes=1024, max_pixels=5)
    with pytest.raises(ValueError, match="image_byte_limit"):
        check_image(raw, "image/png", max_bytes=10, max_pixels=6)
    with pytest.raises(ValueError, match="image_mime_mismatch"):
        check_image(raw, "image/jpeg", max_bytes=1024, max_pixels=6)
    with pytest.raises(OSError):
        check_image(raw[:40], "image/png", max_bytes=1024, max_pixels=6)
