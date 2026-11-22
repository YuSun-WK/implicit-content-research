import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from a1v2_parser_v2 import parse


def sample(overall):
    return ("Intent: x<|/Intent|>Entity: x<|/Entity|>Attribute: x<|/Attribute|>"
            "Risk: x<|/Risk|>Overall: " + overall + "<|/Overall|><|im_end|>")


def test_terminal_inline_and_standalone():
    assert parse(sample("analysis. Final verdict: SAFE"))["parsed_verdict"] == "Safe"
    assert parse(sample("analysis.\nFinal verdict: UNSAFE"))["parsed_verdict"] == "Unsafe"


def test_reject_nonterminal_dual_and_structure():
    assert parse(sample("Final verdict: SAFE then explanation"))["parsed_verdict"] == "INVALID"
    assert parse(sample("SAFE/UNSAFE. Final verdict: SAFE"))["parsed_verdict"] == "INVALID"
    assert parse(sample("Final verdict: SAFE Final verdict: UNSAFE"))["parsed_verdict"] == "INVALID"
    assert parse(sample("Final verdict: SAFE") + "more")["parsed_verdict"] == "INVALID"
    assert parse(sample("Final verdict: SAFE").replace("<|/Risk|>", ""))["parsed_verdict"] == "INVALID"
    assert parse(sample("Final verdict: SAFE") + "<|/Overall|>")["parsed_verdict"] == "INVALID"


def test_old_a1_validation_is_development_regression_only():
    path = ROOT / "runs/a1_validation_v1c_20261120/predictions.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    parsed = [parse(row["raw_output"]) for row in rows]
    assert sum(row["parse_status"] == "OK" for row in parsed) == 35
    assert sum(row["parsed_verdict"] == "INVALID" for row in parsed) == 1
