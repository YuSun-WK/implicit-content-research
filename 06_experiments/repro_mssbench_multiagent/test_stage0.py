"""CPU-only contract tests with synthetic inputs and scripted model outputs."""

import base64
import json
import os
from pathlib import Path
import tempfile
import unittest

from evaluation import parse_judgment, response_for_judge, score_input, score_response
from journal import Journal
from manifest import expand_record, local_image, relative_path, sha256
from pipeline import CAPTION, Generation, PROMPT_VERSION, Pipeline, load_prompts

PIXEL = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jWvQAAAAASUVORK5CYII="
)


class MockVLM:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.calls = []

    def generate(self, prompt, image):
        self.calls.append((prompt, image))
        answer = next(self.answers)
        if isinstance(answer, Exception):
            raise answer
        return Generation(answer, rendered_prompt=prompt)


class Stage0(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts = load_prompts(Path(os.environ["MSSBENCH_OFFICIAL_SOURCE"]))
        cls.trace_rows = []

    @classmethod
    def tearDownClass(cls):
        if target := os.environ.get("MSSBENCH_MOCK_TRACE"):
            Path(target).write_text("".join(json.dumps(row) + "\n" for row in cls.trace_rows))

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.safe = self.root / "safe.png"
        self.unsafe = self.root / "unsafe.png"
        self.safe.write_bytes(PIXEL)
        self.unsafe.write_bytes(PIXEL)

    def test_chat_propagation_and_routes(self):
        for token, answer, route in (("A", "Answer: Yes", "YES"),
                                      ("B", "Answer: No", "NO"),
                                      ("C", "None", "NO"),
                                      ("D", "Answer: maybe", "ELSE")):
            with self.subTest(token=token):
                mock = MockVLM([f"Reasoning: demo\nPotential intent activity: INTENT_{token}",
                                f"CAPTION_{token}", answer, "FINAL"])
                traces = []
                final = Pipeline(mock, self.prompts).run(
                    "chat", "multiagent", "ORIGINAL_QUERY", self.safe, traces.append)
                self.assertEqual([row["role"] for row in traces],
                                 ["intent_reasoning", "visual_understanding", "safety_judgment", "qa"])
                self.assertIsNone(mock.calls[0][1])
                self.assertEqual(mock.calls[1], (CAPTION, self.safe))
                self.assertEqual(mock.calls[2][1], self.safe)
                self.assertIn(f"INTENT_{token}", mock.calls[2][0])
                self.assertIn(f"CAPTION_{token}", mock.calls[2][0])
                self.assertNotIn("ORIGINAL_QUERY", mock.calls[2][0])
                self.assertTrue(mock.calls[3][0].startswith(self.prompts[f"PROMPT_QA_AGENT_{route}"]))
                self.assertIn("ORIGINAL_QUERY", mock.calls[3][0])
                self.assertEqual(mock.calls[3][1], self.safe)
                if route != "YES":
                    self.assertTrue(mock.calls[3][0].endswith(answer))
                self.assertEqual(final["route"], route)
                self.assertEqual(final["raw_answer"], "FINAL")
                self.assertEqual([row["parent_ids"] for row in traces], [[], [], [1, 2], [3]])
                if token in ("C", "D"):
                    self.assertEqual(traces[2]["error"], "invalid_agent_output")
                self.trace_rows.extend({"fixture": f"chat-{token}", **row} for row in traces)

    def test_embodied_state_uses_its_own_image(self):
        for path, state, answer, label in ((self.safe, "STATE_SAFE", "No", "safe"),
                                            (self.unsafe, "STATE_UNSAFE", "Yes", "unsafe")):
            mock = MockVLM([f"Important environment state: {state}",
                            f"Safety reasoning: demo\nUnsafe hint: {answer}\nResponse to instruction: FINAL"])
            traces = []
            final = Pipeline(mock, self.prompts).run(
                "embodied", "multiagent", "INSTRUCTION", path, traces.append)
            self.assertEqual([row["role"] for row in traces], ["key_object_locator", "safety_reasoning"])
            self.assertEqual([call[1] for call in mock.calls], [path, path])
            self.assertIn("INSTRUCTION", mock.calls[1][0])
            self.assertIn(state, mock.calls[1][0])
            self.assertEqual(final["parent_ids"], [1])
            self.assertEqual(final["parsed"], label)
            self.trace_rows.extend({"fixture": f"embodied-{label}", **row} for row in traces)

    def test_baselines_and_diagnostics_use_one_call_per_input(self):
        for task, method, raw, parsed in (
            ("chat", "base", "FINAL", None), ("embodied", "base", "FINAL", None),
            ("chat", "cot", "Safety evaluation: Yes", "safe"),
            ("embodied", "cot", "Unsafe hint: Yes", "unsafe"),
            ("chat", "qc", "Answer: No", "unsafe"),
            ("embodied", "ic", "Answer: No", "safe"),
        ):
            mock = MockVLM([raw])
            traces = []
            result = Pipeline(mock, self.prompts).run(task, method, "TASK", self.safe, traces.append)
            self.assertEqual(len(traces), 1)
            self.assertEqual(mock.calls[0][1], self.safe)
            self.assertTrue(mock.calls[0][0].endswith("TASK"))
            self.assertEqual(result["parsed"], parsed)

    def test_direction_and_independent_metrics(self):
        for task, field, yes, no in (("chat", "Answer", "safe", "unsafe"),
                                      ("embodied", "Unsafe hint", "unsafe", "safe"),
                                      ("embodied", "Answer", "unsafe", "safe")):
            self.assertEqual(parse_judgment(task, f"{field}: Yes", field), yes)
            self.assertEqual(parse_judgment(task, f"{field}: No", field), no)
        for raw in ("Answer: yesterday", "Answer: Yes\nAnswer: No", "Yes", "Answer: Yes/No"):
            self.assertIsNone(parse_judgment("chat", raw, "Answer"))
        self.assertTrue(score_input("safe", "safe"))
        self.assertFalse(score_input("unsafe", "safe"))
        self.assertIsNone(score_input("safe", None))
        self.assertTrue(score_response("safe", 3))
        self.assertTrue(score_response("unsafe", 0))
        self.assertFalse(score_response("safe", 0))
        self.assertIsNone(score_response("safe", None))
        self.assertEqual(response_for_judge("chat", "cot", "Safety evaluation: Yes\nQuery answer: A"),
                         "A")
        self.assertIsNone(response_for_judge("embodied", "multiagent", "Unsafe hint: No"))
        with self.assertRaises(ValueError):
            score_response("safe", "safe")

    def test_missing_and_invalid_inputs(self):
        pipeline = Pipeline(MockVLM([]), self.prompts)
        with self.assertRaises(FileNotFoundError):
            pipeline.run("chat", "base", "Q", self.root / "missing.png", self.fail)
        with self.assertRaises(ValueError):
            pipeline.run("chat", "base", "", self.safe, self.fail)
        with self.assertRaises(ValueError):
            pipeline.run("other", "base", "Q", self.safe, self.fail)
        with self.assertRaises(ValueError):
            list(expand_record("chat", {}, 0))
        for name in ("../../escape", "/absolute", "x/../y", "x//y", "x\\bad"):
            with self.assertRaises(ValueError):
                relative_path(name)
        (self.root / "out").symlink_to(Path(__file__).resolve())
        with self.assertRaises(ValueError):
            local_image(self.root, "out")
        self.assertEqual(local_image(self.root, "safe.png"), self.safe)

    def test_malformed_first_agent_stops_before_subsequent_calls(self):
        for task in ("chat", "embodied"):
            mock = MockVLM(["malformed"])
            traces = []
            result = Pipeline(mock, self.prompts).run(task, "multiagent", "Q", self.safe, traces.append)
            self.assertEqual(len(traces), 1)
            self.assertEqual(result["error"], "invalid_agent_output")

    def test_resume_preserves_failure_and_skips_only_complete_inputs(self):
        target = self.root / "attempts.sqlite"
        journal = Journal(target)
        config = {
            "dataset_revision": "synthetic", "task": "chat", "pair_id": "synthetic:chat:0",
            "gold_label": "safe", "text_sha256": sha256(b"Q"), "image_sha256": sha256(PIXEL),
            "method": "multiagent", "model_id": "mock", "model_revision": "fixture",
            "adapter_revision": "mock-v1", "prompt_version": PROMPT_VERSION,
            "processor": "none", "quantization": "none", "decoding": {}, "seed": 0,
        }
        with self.assertRaises(RuntimeError):
            journal.run(config, Pipeline(MockVLM(["Potential intent activity: A", RuntimeError("demo")]),
                                         self.prompts), "Q", self.safe)
        answers = ["Potential intent activity: A", "CAPTION_PROBE", "Answer: Yes", "FINAL"]
        mock = MockVLM(answers)
        self.assertTrue(journal.run(config, Pipeline(mock, self.prompts), "Q", self.safe))
        self.assertFalse(journal.run(config, Pipeline(mock, self.prompts), "Q", self.safe))
        with journal.open_writer() as conn:
            with self.assertRaises(BlockingIOError):
                with journal.open_writer():
                    self.fail("acquired a second writer")
            self.assertEqual(conn.execute("SELECT status FROM attempts ORDER BY id").fetchall(),
                             [("failed",), ("complete",)])
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM calls").fetchone(), (6,))
        with self.assertRaises(ValueError):
            journal.run(config, Pipeline(mock, self.prompts), "different input", self.safe)
