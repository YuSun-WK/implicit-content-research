import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from a1_parser_v1 import parse


def raw(overall):
    return "1. Intent Analysis: x<|/Intent|>\n2. Environment and Entity Extraction: x<|/Entity|>\n3. Entity Attributes: x<|/Attribute|>\n4. Relationship Risk: x<|/Risk|>\n5. Overall: " + overall + "<|/Overall|>"


def test_unique_terminal_verdict():
    r = parse(raw("Reason.\nFinal verdict: UNSAFE\n"))
    assert r["parsed_verdict"] == "Unsafe" and r["structure_complete"]


def test_reject_dual_and_nonterminal():
    assert parse(raw("[Safe]/[Unsafe]\nFinal verdict: SAFE"))["parsed_verdict"] == "INVALID"
    assert parse(raw("Final verdict: SAFE\nExplanation"))["parsed_verdict"] == "INVALID"
    assert parse(raw("Final verdict: SAFE\nFinal verdict: UNSAFE"))["parsed_verdict"] == "INVALID"


def test_reject_risk_only_and_extra_text():
    assert parse(raw("Risky"))["parsed_verdict"] == "INVALID"
    assert parse(raw("Final verdict: SAFE") + "extra")["parsed_verdict"] == "INVALID"
