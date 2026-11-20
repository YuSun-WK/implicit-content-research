import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from d0_parser_v1 import parse


def test_direct_exact():
    assert parse("Final verdict: SAFE")["parsed_verdict"] == "Safe"
    assert parse("Final verdict: UNSAFE<|im_end|>")["parsed_verdict"] == "Unsafe"
    assert parse("SAFE or UNSAFE")["parsed_verdict"] == "INVALID"
    assert parse("Final verdict: SAFE\nother")["parsed_verdict"] == "INVALID"
