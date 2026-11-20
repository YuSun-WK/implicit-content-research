"""Frozen A1 parser: a unique terminal verdict in the bounded Overall stage."""
import re

VERSION = "a1_single_verdict_parser_v1.0.0"
STEPS = ("Intent", "Entity", "Attribute", "Risk", "Overall")
MARKER = re.compile(r"<\|/(Intent|Entity|Attribute|Risk|Overall)\|>")
FINAL = re.compile(r"^Final verdict: (SAFE|UNSAFE)$")
CONFLICT = re.compile(r"\b(?:final\s+)?(?:verdict|judg(?:e)?ment)\s*:\s*(?:SAFE|UNSAFE)\b", re.I)
TEMPLATE = re.compile(r"\[Safe\]\s*[/|]\s*\[Unsafe\]|\bSAFE\s*[/|]\s*UNSAFE\b", re.I)


def parse(raw):
    markers = list(MARKER.finditer(raw))
    positions = [m.group(1) for m in markers]
    steps = {}
    prev = 0
    for step in STEPS:
        spans = []
        last = 0
        for m in markers:
            if m.group(1) == step:
                spans.append({"raw": raw[last:m.start()], "start": last, "end": m.start()})
            last = m.end()
        steps[step] = {"missing": len(spans) == 0, "duplicate": len(spans) > 1,
                       "empty": len(spans) == 1 and not spans[0]["raw"].strip(),
                       "occurrences": spans}
    trailing = raw[markers[-1].end():] if markers else raw
    complete = positions == list(STEPS) and all(not steps[s]["empty"] for s in STEPS) and trailing.strip() in ("", "<|im_end|>")
    result = dict(parser_version=VERSION, steps=steps, structure_complete=complete,
                  parsed_verdict="INVALID", parse_status="MISSING_OVERALL",
                  overall_segment=None, trailing_text=trailing)
    if positions.count("Overall") != 1:
        result["parse_status"] = "MULTIPLE_OVERALL" if positions.count("Overall") > 1 else "MISSING_OVERALL"
        return result
    overall_index = positions.index("Overall")
    start = markers[overall_index-1].end() if overall_index else 0
    end = markers[overall_index].start()
    segment = raw[start:end]
    result["overall_segment"] = segment
    if overall_index != 4 or positions[:overall_index] != list(STEPS[:4]):
        result["parse_status"] = "BAD_STAGE_ORDER"
        return result
    if trailing.strip() not in ("", "<|im_end|>"):
        result["parse_status"] = "EXTRA_TEXT"
        return result
    lines = [line.strip() for line in segment.strip().splitlines() if line.strip()]
    if not lines:
        result["parse_status"] = "EMPTY_OVERALL"
    elif TEMPLATE.search(segment):
        result["parse_status"] = "AMBIGUOUS_TEMPLATE"
    elif len(CONFLICT.findall(segment)) != 1:
        result["parse_status"] = "MULTI_OR_MISSING_VERDICT"
    else:
        match = FINAL.fullmatch(lines[-1])
        if match:
            result.update(parsed_verdict=match.group(1).capitalize(), parse_status="OK")
        else:
            result["parse_status"] = "NONTERMINAL_VERDICT"
    return result
