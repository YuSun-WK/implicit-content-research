"""CPU-testable orchestration. The VLM adapter owns rendering and generation."""

import ast
from dataclasses import dataclass
from pathlib import Path
import re
from time import perf_counter
from typing import Protocol

from evaluation import parse_judgment
from manifest import SOURCES, sha256

PROMPT_VERSION = "mssbench-stage0-v1"
CAPTION = "Describe the image in one long sentence."


@dataclass(frozen=True)
class Generation:
    text: str
    rendered_prompt: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    peak_allocated_bytes: int | None = None
    peak_reserved_bytes: int | None = None
    nvml_used_bytes: int | None = None


class VLM(Protocol):
    def generate(self, prompt: str, image: Path | None) -> Generation: ...


def load_prompts(source):
    path = source / "utils" / "prompts.py"
    data = path.read_bytes()
    if sha256(data) != SOURCES["official_prompts_sha256"]:
        raise ValueError("official prompts differ from the source lock")
    return {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in ast.parse(data).body if isinstance(node, ast.Assign)
    }


def parsed_field(text, field):
    values = re.findall(rf"(?<!\w){re.escape(field)}:[ \t]*([^\r\n]*)", text,
                        re.IGNORECASE)
    if len(values) == 1 and values[0].strip():
        return values[0].strip()
    return None


class Pipeline:
    def __init__(self, model: VLM, prompts):
        self.model = model
        self.prompts = prompts

    def run(self, task, method, text, image, emit):
        if task not in ("chat", "embodied") or method not in (
            "base", "cot", "multiagent", "qc", "ic"
        ):
            raise ValueError("unsupported task or method")
        if not isinstance(text, str) or not text.strip() or not isinstance(image, Path):
            raise ValueError("a non-empty input and an image path are required")
        if not image.is_file():
            raise FileNotFoundError(image)
        calls = 0

        def call(role, prompt, *, visual=True, parents=(), parse=None, route=None):
            nonlocal calls
            calls += 1
            trace = {
                "call_id": calls, "parent_ids": list(parents), "role": role,
                "prompt": prompt, "image_attached": visual, "route": route,
                "raw_answer": None, "parsed": None, "error": None,
                "rendered_prompt": None, "input_tokens": None, "output_tokens": None,
                "peak_allocated_bytes": None, "peak_reserved_bytes": None,
                "nvml_used_bytes": None,
            }
            start = perf_counter()
            try:
                result = self.model.generate(prompt, image if visual else None)
                trace.update(vars(result))
                trace["raw_answer"] = trace.pop("text")
                if not result.text.strip():
                    trace["error"] = "invalid_agent_output"
                if parse:
                    trace["parsed"] = parse(result.text)
                    if trace["parsed"] is None:
                        trace["error"] = "invalid_agent_output"
            except Exception as exc:
                trace["error"] = type(exc).__name__
                trace["error_detail"] = str(exc)
                raise
            finally:
                trace["elapsed_ms"] = round((perf_counter() - start) * 1000, 3)
                emit(trace)
            return trace

        def prompt(key):
            return self.prompts["PROMPT_" + key]

        if method != "multiagent":
            if method == "cot":
                template = prompt(f"COT_{task.upper()}")
                field = "Safety evaluation" if task == "chat" else "Unsafe hint"
            else:
                suffix = "IF" if method == "base" else method.upper()
                template = prompt(f"{task.upper()}_{suffix}")
                field = "Answer"
            parse = None if method == "base" else lambda raw: parse_judgment(task, raw, field)
            return call(method, template + text, parse=parse)

        if task == "embodied":
            state = call("key_object_locator", prompt("IMPORTANT_POINT_AGENT") + text,
                         parse=lambda raw: parsed_field(raw, "Important environment state"))
            if state["parsed"] is None:
                return state
            return call("safety_reasoning", prompt("RESPONSE_AGENT") + text
                        + "\nOne point to consider is: " + state["parsed"], parents=(1,),
                        parse=lambda raw: parse_judgment(task, raw, "Unsafe hint"))

        intent = call("intent_reasoning", prompt("CHAT_INTENT_AGENT") + text, visual=False,
                      parse=lambda raw: parsed_field(raw, "Potential intent activity"))
        if intent["parsed"] is None:
            return intent
        caption = call("visual_understanding", CAPTION, parse=lambda raw: raw.strip() or None)
        if caption["parsed"] is None:
            return caption
        safety = call("safety_judgment", prompt("CHAT_JUDGE_AGENT") + intent["parsed"]
                      + "\nImage caption: " + caption["parsed"], parents=(1, 2),
                      parse=lambda raw: parse_judgment(task, raw, "Answer"))
        label = safety["parsed"]
        no_or_none = label == "unsafe" or safety["raw_answer"].strip().lower() == "none"
        if label == "safe":
            route = "YES"
        else:
            route = "NO" if no_or_none else "ELSE"
        qa = prompt(f"QA_AGENT_{route}") + text
        if route != "YES":
            qa += "\nThe safety evaluation is: " + safety["raw_answer"]
        return call("qa", qa, parents=(3,), route=route)
