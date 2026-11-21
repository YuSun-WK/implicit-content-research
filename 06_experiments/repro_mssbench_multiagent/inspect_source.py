"""Compile fixed sources and reproduce latent failures with inert dependencies."""

import argparse
import ast
import contextlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch

from manifest import SOURCES


def verify_source(root):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()
    if git("rev-parse", "HEAD") != SOURCES["official_commit"] or git("status", "--porcelain"):
        raise ValueError("expected a clean checkout of the fixed official source")


def expect(label, expected, operation):
    try:
        operation()
    except expected as exc:
        print(f"{label}: {type(exc).__name__}: {exc}")
    else:
        raise AssertionError(f"{label}: expected {expected.__name__}")


def main(root):
    sys.dont_write_bytecode = True
    root = root.resolve()
    verify_source(root)
    paths = [root / "inference.py", *sorted((root / "utils").glob("*.py")),
             *sorted((root / "models").glob("*.py"))]
    for path in paths:
        if path.name == "infer_on_multiagent.py":
            expect(str(path.relative_to(root)), IndentationError,
                   lambda: compile(path.read_bytes(), path.name, "exec"))
        else:
            compile(path.read_bytes(), path.name, "exec")
            print(f"{path.relative_to(root)}: compile PASS")
    with contextlib.ExitStack() as stack:
        temp = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        stack.enter_context(patch.object(sys, "path", [str(root), *sys.path]))
        stack.enter_context(patch.dict(sys.modules, {"utils.gpt4_eval": types.ModuleType("utils.gpt4_eval")}))
        expect("import utils.infer_on_data with inert judge", IndentationError,
               lambda: __import__("utils.infer_on_data"))
        path = root / "utils/infer_on_multiagent.py"
        raw = path.read_text().replace("\n     elif ", "\n    elif ", 1)
        expect("indentation-only repair, package import", ModuleNotFoundError,
               lambda: exec(compile(raw, path.name, "exec"), {}))
        source = ast.parse(raw, filename=path.name)
        prompts = __import__("utils.prompts", fromlist=["prompts"])
        calls = []

        def mock(image, prompt):
            calls.append((image, prompt))
            if "Potential intent activity" in prompt:
                return "Potential intent activity: INTENT_PROBE"
            if "Important environment state" in prompt:
                return "Important environment state: STATE_PROBE"
            return "Answer: Yes"

        namespace = {**vars(prompts), "os": __import__("os"), "json": __import__("json"),
                     "tqdm": lambda data: data,
                     "gpt4_eval": lambda *_: (0,) * 6}
        functions = [node for node in source.body if isinstance(node, ast.FunctionDef)]
        exec(compile(ast.Module(body=functions, type_ignores=[]), path.name, "exec"), namespace)
        chat = namespace["chat_response"]
        robot = namespace["embodied_response"]
        multi = namespace["test_multiagent"]
        expect("chat_response missing model binding", NameError, lambda: chat("image", "Answer: Yes", "Q"))
        namespace["model"] = mock
        expect("embodied_response missing safe_image binding", NameError,
               lambda: robot("safe", "unsafe", "S", "U"))
        namespace["safe_image"] = "safe"
        robot("safe", "unsafe", "S", "U")
        assert calls[2][0] == "safe" and calls[3][0] == "unsafe"
        print("original unsafe locator used safe image; state reached unsafe response")
        expect("embodied loop missing safe_imge binding", NameError, lambda: multi(
            {"chat": [], "embodied": [{"safe_instructions": ["S"], "unsafe_instructions": ["U"]}]},
            mock, str(temp)))
        fixture = [{"safe_image_path": "s.png", "unsafe_image_path": "u.png",
                    "queries": ["QUERY_PROBE"]}]
        calls.clear()
        expect("multiagent JSON file created as a directory", IsADirectoryError, lambda: multi(
            {"chat": fixture, "embodied": []}, mock, str(temp), str(temp / "out.json")))
        assert len(calls) == 6
        assert "QUERY_PROBE" in calls[2][1] and "INTENT_PROBE" not in calls[2][1]
        assert calls[4][1] == calls[5][1] == "QUERY_PROBE"
        print("original Chat: 3 calls/side; no caption; judges saw query instead of intent; QA saw plain query")
        expect("multiagent output_path=None", TypeError,
               lambda: multi({"chat": [], "embodied": []}, mock, str(temp)))

        data_source = ast.parse((root / "utils/infer_on_data.py").read_bytes())
        funcs = [node for node in data_source.body if isinstance(node, ast.FunctionDef)]
        exec(compile(ast.Module(body=funcs, type_ignores=[]), "infer_on_data.py", "exec"), namespace)
        baseline = namespace["test_each_mss"]
        expect("baseline output parent missing", FileNotFoundError, lambda: baseline(
            {"chat": fixture, "embodied": []}, mock, str(temp), str(temp / "absent/out.json")))
        evaluations = []

        def judge(outputs, filename):
            evaluations.append(outputs)
            return (0,) * 6

        namespace["gpt4_eval"] = judge
        baseline({"chat": fixture, "embodied": []}, mock, str(temp),
                 str(temp / "qc.json"), setting="qc")
        assert evaluations[0]["chat"][0]["safe_output"] == "Answer: Yes"
        print("baseline QC passed binary output unparsed to the response-Judge slot")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    main(parser.parse_args().root)
