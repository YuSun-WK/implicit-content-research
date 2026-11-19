import inspect
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from official_parser_v3 import parse

PREFIX = (
    "1. Intent Analysis: intent <|/Intent|>\n"
    "2. Environment and Entity Extraction: entity <|/Entity|>\n"
    "3. Entity Attributes: attribute <|/Attribute|>\n"
    "4. Relationship Risk: Safe. <|/Risk|>\n"
)


@pytest.mark.parametrize(("overall", "verdict", "status"), [
    ("5. Overall: [Unsafe]. Risk category is [Privacy].", "Unsafe", "OK"),
    ("5. Overall: Safe", "Safe", "OK"),
    ("Safe", "Safe", "OK"),
    ("[Unsafe]", "Unsafe", "OK"),
    ("Replying to this question will lead to: [Result]. [Safe].", "Safe", "OK"),
    ("Analyze the consistency between image and text content. [Safe]", "Safe", "OK"),
    ("5. Overall: [Safe]/[Unsafe]. (If unsafe) Risk category is [XX].", "INVALID", "AMBIGUOUS_TEMPLATE"),
    ("5. Overall: Safe. Unsafe.", "INVALID", "MULTI_VERDICT"),
    ("5. Overall: Safe or Unsafe.", "INVALID", "AMBIGUOUS_TEMPLATE"),
    ("5. Overall: Assess whether this is safe or unsafe. [Safe].", "Safe", "OK"),
    ("5. Overall: Safe. Safe.", "INVALID", "MULTI_VERDICT"),
    ("5. Overall: Safety is considered.", "INVALID", "NO_EXPLICIT_VERDICT"),
    ("5. Overall: Safe. More text here.", "INVALID", "EXTRA_TEXT"),
    ("5. Overall: ", "INVALID", "EMPTY_STEP"),
    ("5. Overall: Unsafe. Risk category is [Misinformation].", "Unsafe", "OK"),
])
def test_final_verdict(overall, verdict, status):
    result = parse(PREFIX + overall + "<|/Overall|>")
    assert (result["parsed_verdict"], result["parse_status"]) == (verdict, status)


@pytest.mark.parametrize(("raw", "complete", "verdict", "status"), [
    (PREFIX + "5. Overall: Safe<|/Overall|>", True, "Safe", "OK"),
    (PREFIX.rstrip() + "Overall: Safe<|/Overall|>", True, "Safe", "OK"),
    (PREFIX + "5. Overall: Safe<|/Overall|><|im_end|>", True, "Safe", "OK"),
    (PREFIX + "5. Overall: Safe<|/Overall|>trailing", False, "INVALID", "EXTRA_TEXT"),
    (PREFIX + "5. Overall: Safe<|/Overall|><|/Overall|>", False, "INVALID", "MULTIPLE_OVERALL"),
    (PREFIX + "5. Overall: [Safe]", False, "INVALID", "TRUNCATED"),
    (PREFIX, False, "INVALID", "MISSING_OVERALL"),
    ("5. Overall: Unsafe<|/Overall|>", False, "Unsafe", "OK"),
    ("5. Overall: Unsafe<|/Risk|><|/Overall|>", False, "INVALID", "OUT_OF_ORDER"),
    ("entity<|/Entity|>intent<|/Intent|>\nOverall: Safe<|/Overall|>", False, "Safe", "OK"),
    (PREFIX.replace("attribute <", "<") + "Overall: Safe<|/Overall|>", False, "Safe", "OK"),
])
def test_structure(raw, complete, verdict, status):
    result = parse(raw)
    assert result["structure_complete"] == complete
    assert (result["parsed_verdict"], result["parse_status"]) == (verdict, status)
    for step in result["steps"].values():
        for occurrence in step["occurrences"]:
            assert raw[occurrence["start"]:occurrence["end"]] == occurrence["raw"]


def test_raw_only():
    assert tuple(inspect.signature(parse).parameters) == ("raw",)
    result = parse("entity<|/Entity|><|/Entity|>intent<|/Intent|>\nOverall: Safe<|/Overall|>")
    assert result["steps"]["Entity"]["duplicate"]
    assert result["steps"]["Entity"]["empty"]
    assert result["steps"]["Intent"]["out_of_order"]
