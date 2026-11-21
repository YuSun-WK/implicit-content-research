"""Verify Stage 1 wiring on CPU, including the pinned native prompt renderer."""
from copy import deepcopy
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from journal import IDENTITY_FIELDS, Journal, run_key
from manifest import sha256
from pipeline import Generation, InvalidAgentOutput, Pipeline, load_prompts
from stage1_data import inspect_image, smoke_inputs
from stage1_native import render_prompt
from stage1_smoke import behavior_type, build_work, g1_work, label_format, validate_traces
from evaluation import response_for_judge
from test_stage0 import PIXEL


class CapturingModel:
    def __init__(self, outputs):
        self.outputs = iter(outputs)

    def generate(self, prompt, image):
        rendered = ("<image>\n" if image else "") + prompt
        return Generation(next(self.outputs), rendered_prompt=rendered, input_tokens=5,
                          effective_input_tokens=20 if image else 5, output_tokens=3,
                          image_dimensions=(1, 1) if image else None, model_load_count=1,
                          peak_allocated_bytes=1, peak_reserved_bytes=1, nvml_delta_bytes=1)


class Stage1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts = load_prompts(Path(os.environ["MSSBENCH_OFFICIAL_SOURCE"]))

    def setUp(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        self.root = Path(root.name)
        self.image = self.root / "input.png"
        self.image.write_bytes(PIXEL)

    def traces(self, intent="A", caption="B", decision="Yes"):
        mock = CapturingModel([f"Potential intent activity: {intent}", caption,
                               f"Answer: {decision}", "Final answer"])
        traces = []
        Pipeline(mock, self.prompts, stop_on_invalid=True).run(
            "chat", "multiagent", "QUERY", self.image, traces.append)
        config = {"task": "chat", "method": "multiagent", "image_dimensions": [1, 1]}
        validate_traces(config, traces, self.prompts)
        return config, traces

    def test_changed_agent_outputs_change_rendered_downstream_prompt(self):
        config, base = self.traces()
        _, intent = self.traces(intent="CHANGED_INTENT")
        _, caption = self.traces(caption="CHANGED_CAPTION")
        _, safety = self.traces(decision="No")
        for changed, token in ((intent, "CHANGED_INTENT"), (caption, "CHANGED_CAPTION")):
            self.assertNotEqual(base[2]["rendered_prompt"], changed[2]["rendered_prompt"])
            self.assertIn(token, changed[2]["rendered_prompt"])
        self.assertNotEqual(base[3]["rendered_prompt"], safety[3]["rendered_prompt"])
        self.assertIn("Answer: No", safety[3]["rendered_prompt"])
        broken = deepcopy(base)
        broken[3]["route"] = "NO"
        with self.assertRaisesRegex(ValueError, "QA routing"):
            validate_traces(config, broken, self.prompts)

    def test_strict_gate_stops_immediately_and_retains_invalid_trace(self):
        model = CapturingModel(["Potential intent activity: INTENT", "CAPTION", "Answer: perhaps"])
        config = dict.fromkeys(IDENTITY_FIELDS, "fixture")
        config.update(task="chat", method="multiagent", image_sha256=sha256(PIXEL), text_sha256=sha256(b"Q"))
        journal = Journal(self.root / "invalid.sqlite")
        with self.assertRaises(InvalidAgentOutput):
            journal.run(config, Pipeline(model, self.prompts, stop_on_invalid=True), "Q", self.image)
        with journal.open_writer() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts").fetchone(), ("invalid",))
            self.assertEqual(db.execute("SELECT count(*) FROM calls").fetchone(), (3,))

    def test_embodied_unsafe_hint_without_response_is_unknown(self):
        model = CapturingModel(["Important environment state: The object is a knife.",
                                "Safety reasoning: Unsafe to drop.\nUnsafe hint: Yes"])
        traces = []
        Pipeline(model, self.prompts, stop_on_invalid=True).run(
            "embodied", "multiagent", "Drop the object", self.image, traces.append)
        config = {"task": "embodied", "method": "multiagent", "image_dimensions": [1, 1]}
        validate_traces(config, traces, self.prompts)
        self.assertEqual(traces[-1]["parsed"], "unsafe")
        self.assertIsNone(response_for_judge("embodied", "multiagent", traces[-1]["raw_answer"]))

    def test_explained_label_keeps_noncanonical_format(self):
        trace = {"parsed": "safe", "raw_answer": "Answer: Yes. The scene is safe."}
        self.assertEqual(label_format("chat", "multiagent", trace), "noncanonical")

    def test_process_exit_keeps_partial_trace_and_completed_key(self):
        path = self.root / "resume.sqlite"
        config = dict.fromkeys(IDENTITY_FIELDS, "fixture")
        config.update(task="chat", method="base", image_sha256=sha256(PIXEL),
                      text_sha256=sha256(b"Q"))
        journal = Journal(path)
        ready = Pipeline(CapturingModel(["answer"]), self.prompts)
        self.assertTrue(journal.run({**config, "pair_id": "done"}, ready, "Q", self.image))
        script = """
from pathlib import Path
import json, os, sys
from journal import Journal
class Interrupt:
    def run(self, task, method, text, image, emit):
        emit({"call_id": 1, "error": None})
        os._exit(23)
Journal(Path(sys.argv[1])).run(json.loads(sys.argv[2]), Interrupt(), "Q", Path(sys.argv[3]))
"""
        import json
        process = subprocess.run([sys.executable, "-c", script, str(path),
                                  json.dumps(config), str(self.image)])
        self.assertEqual(process.returncode, 23)
        self.assertTrue(journal.run(config, Pipeline(CapturingModel(["answer"]), self.prompts),
                                    "Q", self.image))
        self.assertFalse(journal.run({**config, "pair_id": "done"}, None, "Q", self.image))
        with journal.open_writer() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts ORDER BY id").fetchall(),
                             [("complete",), ("interrupted",), ("complete",)])
            self.assertEqual(db.execute("SELECT count(*) FROM calls").fetchone(), (3,))

    def test_native_text_and_image_conversation_render(self):
        root = Path(os.environ["MSSBENCH_NATIVE_SOURCE"])
        file = root / "llava" / "conversation.py"
        spec = importlib.util.spec_from_file_location("stage1_native_conversation", file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        template = module.conv_templates["llava_v1"]
        tokens = "<image>", "<im_start>", "<im_end>"
        self.assertNotIn("<image>", render_prompt(template, "TEXT", None, False, tokens))
        self.assertIn("<image>\nTEXT", render_prompt(template, "TEXT", self.image, False, tokens))
        self.assertIn("<im_start><image><im_end>\nTEXT",
                      render_prompt(template, "TEXT", self.image, True, tokens))
        self.assertFalse(template.messages)

    def test_fixed_manifest_and_probe_denominators(self):
        from argparse import Namespace
        data = Path(os.environ["MSSBENCH_STAGE1_DATA"])
        rows = smoke_inputs(data / "combined.json")
        args = Namespace(data_root=data, processor="mssbench_224", max_new_tokens=128, seed=0)
        work = build_work(args, rows, "fixture")
        self.assertEqual(len(work), 120)
        self.assertEqual(len({run_key(row.config) for row in work}), 120)
        self.assertEqual(len(g1_work(work)), 12)
        self.assertEqual({r.config["pair_id"] for r in g1_work(work)},
                         {"query:chat:016:00", "query:embodied:056:00"})

    def test_corrupted_assets_and_behavior_screen(self):
        with self.assertRaisesRegex(ValueError, "SHA256"):
            inspect_image(self.image, {"expected_bytes": str(len(PIXEL)), "hf_lfs_sha256": "0" * 64})
        self.assertEqual(behavior_type("There may be a hazard."), "warning_keyword")
        self.assertEqual(behavior_type("I cannot help."), "refusal_keyword")
        self.assertEqual(behavior_type(None), "unknown")
