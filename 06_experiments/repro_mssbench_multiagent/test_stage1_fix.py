"""CPU regressions for fixed-source transfer and the pre-G1 probe gate."""

import json
from pathlib import Path
import tempfile
import unittest

from pipeline import Generation
from stage1_smoke import run_preliminary_probes
from stage1_weights import MIRRORS, mirror_urls, validate_range


class Stage1Fix(unittest.TestCase):
    def test_accepts_only_exact_final_http_range(self):
        connect = "HTTP/1.1 200 Connection established\r\n\r\n"
        final = "HTTP/2 206 Partial Content\r\nContent-Range: bytes 10-19/25\r\n\r\n"
        self.assertTrue(validate_range(connect + final, 10, 10, 19, 25))
        self.assertFalse(validate_range(connect + final, 9, 10, 19, 25))
        self.assertFalse(validate_range(connect + final, 10, 10, 19, 26))
        self.assertFalse(validate_range(connect + final, 10, 11, 20, 25))
        self.assertFalse(validate_range(connect + final.replace("206", "200"), 10, 10, 19, 25))

    def test_mirror_requires_official_size_hash_and_locked_revision(self):
        entry = {"rfilename": "test.bin", "size": 25, "lfs": {"sha256": "a" * 64}}
        row = {"Path": "test.bin", "Size": 25, "Sha256": "a" * 64,
               "Revision": MIRRORS["native"][1], "Type": "blob"}
        def listing(value):
            return {"Data": {"Files": [value]}}
        self.assertIn(row["Revision"], mirror_urls("native", [entry], listing(row))["test.bin"])
        for differences in ({"Sha256": "b" * 64}, {"Size": 24}, {"Revision": "master"}):
            with self.assertRaises(ValueError):
                mirror_urls("native", [entry], listing({**row, **differences}))

    def test_probe_checks_image_expansion_and_preserves_failure(self):
        class FakeModel:
            def __init__(self, expand):
                self.expand = expand

            def generate(self, prompt, image):
                return Generation(text="demo", rendered_prompt=("<image>\n" if image else "") + prompt,
                                  input_tokens=8, output_tokens=2, model_load_count=1,
                                  effective_input_tokens=25 if image and self.expand else 8,
                                  image_dimensions=(8, 8) if image else None)

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            log = base / "probes.jsonl"
            with self.assertRaisesRegex(RuntimeError, "did not expand"):
                run_preliminary_probes(FakeModel(False), base / "image.png", log, "bad")
            run_preliminary_probes(FakeModel(True), base / "image.png", log, "ok")
            data = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual([x["error"] for x in data], [None, "RuntimeError", None, None])
            self.assertEqual([x["image_attached"] for x in data], [False, True, False, True])
