"""A1v2 parser for one terminal Overall verdict clause, inline or standalone."""
import re

VERSION = "a1v2_terminal_clause_parser_v2.0.0"
STEPS = ("Intent", "Entity", "Attribute", "Risk", "Overall")
MARKER = re.compile(r"<\|/(Intent|Entity|Attribute|Risk|Overall)\|>")
VERDICT = re.compile(r"Final verdict: (SAFE|UNSAFE)\b", re.I)
TERMINAL = re.compile(r"Final verdict: (SAFE|UNSAFE)\s*\Z", re.I)
DUAL = re.compile(r"\bSAFE\s*(?:/|\||\bor\b)\s*UNSAFE\b|\bUNSAFE\s*(?:/|\||\bor\b)\s*SAFE\b", re.I)


def parse(raw):
    markers = list(MARKER.finditer(raw))
    names = [m.group(1) for m in markers]
    steps = {}
    previous = 0
    for marker in markers:
        step = marker.group(1)
        steps.setdefault(step, []).append(raw[previous:marker.start()])
        previous = marker.end()
    trailing = raw[previous:] if markers else raw
    structure_complete = (names == list(STEPS) and trailing.strip() in ("", "<|im_end|>")
                          and all(steps.get(step) and steps[step][0].strip() for step in STEPS))
    result = {"parser_version": VERSION, "structure_complete": structure_complete,
              "steps": {step: {"missing": step not in steps, "duplicate": len(steps.get(step, [])) > 1,
                               "empty": bool(steps.get(step)) and not steps[step][0].strip()}
                        for step in STEPS},
              "parsed_verdict": "INVALID", "parse_status": "BAD_STAGE_STRUCTURE",
              "overall_segment": None, "trailing_text": trailing}
    if not structure_complete:
        return result
    segment = steps["Overall"][0]
    result["overall_segment"] = segment
    verdicts = list(VERDICT.finditer(segment))
    if DUAL.search(segment) or len(verdicts) > 1:
        result["parse_status"] = "MULTI_OR_DUAL_VERDICT"
        return result
    if not verdicts:
        result["parse_status"] = "MISSING_VERDICT"
        return result
    terminal = TERMINAL.search(segment)
    if terminal is None or terminal.start() != verdicts[0].start():
        result["parse_status"] = "NONTERMINAL_VERDICT"
        return result
    result.update(parsed_verdict=terminal.group(1).capitalize(), parse_status="OK")
    return result
