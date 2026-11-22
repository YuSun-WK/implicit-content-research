"""Small CPU checks for the frozen Stage 2 selection and resume identity."""
import csv
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
import unittest

from journal import Journal, run_key
from stage1_smoke import build_work, read_journal
from stage2_runner import checked_model, configure, frozen_rows

HERE = Path(__file__).parent
ROOT = HERE / ".stage0-local"
SNAPSHOT = Path("/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3")


class Stage2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = frozen_rows(HERE / "stage2/frozen_100_pairs.csv", ROOT / "stage1/data")

    def test_frozen_pairs_and_strata(self):
        pairs = {(r["task"], r["pair_id"]) for r in self.rows}
        self.assertEqual(Counter(task for task, _ in pairs), {"chat": 60, "embodied": 40})
        self.assertEqual(Counter(r["gold_label"] for r in self.rows), {"safe": 100, "unsafe": 100})
        self.assertEqual(len({(r["task"], r["record_index"]) for r in self.rows}), 100)
        self.assertEqual(len({r["image_path"] for r in self.rows}), 200)
        self.assertEqual(len({r["pair_id"] for r in self.rows if r["anchor"]}), 20)

    def test_anchor_run_keys_are_reused(self):
        args = SimpleNamespace(data_root=ROOT / "stage1/data", processor="mssbench_224",
                               max_new_tokens=256, seed=0)
        work = build_work(args, [r for r in self.rows if r["anchor"]], checked_model(
            ROOT / "fasttrack/B-thinkingguard", SNAPSHOT))
        configure(work)
        old = {r["key"] for r in read_journal(Journal(
            ROOT / "fasttrack/B-thinkingguard/run-nf4-v2-256/smoke.sqlite"))
               if r["status"] in ("complete", "invalid")}
        self.assertEqual(len(work), 120)
        self.assertTrue({run_key(w.config) for w in work} <= old)

    def test_512_has_separate_identity(self):
        rows = self.rows[:2]
        lock = checked_model(ROOT / "fasttrack/B-thinkingguard", SNAPSHOT)
        keys = []
        for tokens in (256, 512):
            args = SimpleNamespace(data_root=ROOT / "stage1/data", processor="mssbench_224",
                                   max_new_tokens=tokens, seed=0)
            work = build_work(args, rows, lock)
            configure(work)
            keys.append({run_key(w.config) for w in work})
        self.assertFalse(keys[0] & keys[1])


if __name__ == "__main__":
    unittest.main()
