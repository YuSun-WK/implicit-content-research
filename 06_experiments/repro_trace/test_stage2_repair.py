"""CPU gates for caption selection, immutable originals and atomic state."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from stage2_caption import save_state
from stage2_repair_captions import sha, token_count, validate_original, validate_repaired
from stage2_train import metrics, validate_caption_lengths


class SpaceTokenizer:
    def encode(self, text, add_special_tokens=True):
        return list(range(len(text.split()) + (2 if add_special_tokens else 0)))


class RepairTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = SpaceTokenizer()
        self.source = []
        self.old = {}
        for index in range(740):
            split = "train" if index < 444 else "dev" if index < 592 else "test"
            row = {"key": f"key-{index}", "split": split, "row_number": index,
                   "image_name": f"{index}.jpg", "image_sha256": f"sha-{index}",
                   "sentence": "meme original words"}
            self.source.append(row)
            self.old[row["key"]] = {key: row[key] for key in
                                    ("split", "row_number", "image_name", "image_sha256")}
            self.old[row["key"]]["caption"] = ("visual " * 76).strip() if index < 334 else "visual scene"

    def test_selects_exactly_334_and_preserves_406(self):
        overlong = validate_original(self.source, self.old, self.tokenizer)
        self.assertEqual(len(overlong), 334)
        new = copy.deepcopy(self.old)
        audit = {}
        for row in self.source[:334]:
            key = row["key"]
            new[key]["caption"] = "A concise visible scene."
            audit[key] = {"old_sha256": sha(self.old[key]["caption"]),
                          "new_sha256": sha(new[key]["caption"]),
                          "new_tokens": token_count(self.tokenizer, new[key]["caption"]),
                          "image_sha256": row["image_sha256"], "attempts": 1}
        result = validate_repaired(self.source, self.old, new, audit, self.tokenizer, overlong)
        self.assertEqual(result["repaired"], 334)
        self.assertEqual(result["remaining_over_77"], 0)
        self.assertEqual(result["unchanged_originally_valid"], 406)
        new["key-334"]["caption"] = "changed"
        with self.assertRaisesRegex(ValueError, "Originally valid caption changed"):
            validate_repaired(self.source, self.old, new, audit, self.tokenizer, overlong)

    def test_hard_gate_sees_untruncated_length(self):
        rows = {"train": [(None, "original", "short", 0)] * 444,
                "dev": [(None, "original", "short", 0)] * 148,
                "test": [(None, "original", "short", 0)] * 148}
        self.assertEqual(validate_caption_lengths(rows, self.tokenizer)["checked"], 740)
        rows["test"][-1] = (None, "original", "word " * 76, 0)
        with self.assertRaisesRegex(ValueError, "77-token gate failed for 1"):
            validate_caption_lengths(rows, self.tokenizer)

    def test_atomic_manifest_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "records.json"
            save_state(path, {"key": {"caption": "first"}})
            save_state(path, {"key": {"caption": "second"}})
            self.assertEqual(json.loads(path.read_text())["key"]["caption"], "second")
            self.assertFalse(path.with_suffix(".tmp").exists())

    def test_extended_metrics_keep_fixed_threshold_and_positive_definition(self):
        result = metrics([0, 0, 1, 1], [0.1, 0.8, 0.3, 0.9])
        self.assertEqual(result["threshold"], 0.5)
        self.assertEqual(result["predicted_positive"], 2)
        self.assertEqual(result["precision"], result["offensive_precision"])
        self.assertEqual(result["recall"], result["offensive_recall"])
        self.assertAlmostEqual(result["macro_precision"], 0.5)
        self.assertAlmostEqual(result["macro_recall"], 0.5)
        self.assertEqual(result["probability"]["min"], 0.1)
        self.assertEqual(result["probability"]["max"], 0.9)


if __name__ == "__main__":
    unittest.main()
