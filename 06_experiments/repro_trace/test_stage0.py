"""CPU-only checks using small fixtures. No FHM inputs or Torch optimizer."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

import torch
from transformers import CLIPConfig, CLIPModel

from data_manifest import FIELDS, summary
from run_stage0 import DataBlocked, LOSS_CONFIG, assert_inputs, author_loss, save_checkpoint, threshold_for, upstream


class Stage0Checks(unittest.TestCase):
    def test_caption_inventory(self):
        row = {"id": 1, "img": "missing.png", "label": 1, "split": "train",
               "text": "fixture", "ivl_8b_new_caption": " No Caption "}
        with tempfile.TemporaryDirectory() as root:
            stats = summary([row, row, {**row, "split": "test_seen", "label": None}], root)
        counts = stats["splits"]["train"]
        self.assertEqual(counts["images_missing_or_outside_root"], 2)
        self.assertEqual(counts["duplicate_id_rows_beyond_first"], 1)
        self.assertEqual(counts["exact_duplicate_rows_beyond_first"], 1)
        self.assertEqual(counts["captions"][FIELDS[1]]["placeholder"], 2)
        self.assertEqual(counts["captions"][FIELDS[2]]["missing"], 2)
        self.assertEqual(stats["cross_split_repeated_keys"]["id"], 1)
        self.assertFalse(stats["splits"]["test_seen"]["label_scoring_available"])
        self.assertNotIn("fixture", str(stats))

    def test_missing_original_caption_blocks_training(self):
        with tempfile.TemporaryDirectory() as private:
            root = Path(private)
            (root / "fixture.png").touch()
            source = root / "fixture.json"
            source.write_text(json.dumps([{"split": "train", "id": 10, "img": "fixture.png",
                                          "label": 0, "text": "CPU fixture",
                                          "ivl_8b_new_caption": "No caption"}]))
            cfg = {"data_path": source, "image_root": root, "authorization_confirmed": True,
                   "caption_provenance_confirmed": True, "train_split": "train", "dev_split": "dev_seen"}
            with self.assertRaisesRegex(DataBlocked, "captions.*train"):
                assert_inputs(cfg)

    def test_threshold(self):
        self.assertEqual(threshold_for("fixed_0.5", [], []), 0.5)
        self.assertAlmostEqual(threshold_for("dev_f1", [0, 1], [0.2, 0.8]), 0.8)
        with self.assertRaisesRegex(ValueError, "both binary"):
            threshold_for("dev_f1", [1], [0.8])

    def test_small_author_path_singleton(self):
        torch.set_num_threads(1)
        torch.manual_seed(121)
        device = torch.device("cpu")
        config = CLIPConfig(
            text_config={"vocab_size": 32, "hidden_size": 8, "intermediate_size": 16,
                         "num_hidden_layers": 12, "num_attention_heads": 2,
                         "max_position_embeddings": 77, "eos_token_id": 31},
            vision_config={"hidden_size": 8, "intermediate_size": 16, "num_hidden_layers": 1,
                           "num_attention_heads": 2, "image_size": 4, "patch_size": 2},
            projection_dim=8,
        )
        classifier, collate, losses, _ = upstream(
            {"upstream_dir": os.environ.get("TRACE_UPSTREAM_DIR", "/tmp/trace-s0-reference")},
            torch, lambda _: CLIPModel(config))
        with contextlib.redirect_stdout(io.StringIO()):
            model = classifier(projection_dim=8)
        example = {"pixel_values": torch.randn(3, 4, 4),
                   "input_ids": [torch.full((77,), i, dtype=torch.long) for i in (1, 2, 3)],
                   "attention_mask": [torch.ones(77, dtype=torch.long)] * 3,
                   "labels": torch.tensor(1.), "image_ids": "fixture", "num_captions": 3}
        batch = collate([example])
        self.assertEqual(batch["input_ids"].shape, (1, 3, 77))
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "Target size"):
                losses.calculate_loss_gs(model, batch, device, LOSS_CONFIG)
        loss, components = author_loss(losses, model, batch, device, True)
        self.assertEqual(loss.shape, ())
        self.assertEqual(len(components), 2)
        self.assertTrue(torch.isfinite(loss))
        loss.backward()
        self.assertIsNotNone(model.caption_scorer[-1].weight.grad)
        self.assertIsNotNone(model.clip_model.text_model.encoder.layers[4].self_attn.v_proj.weight.grad)
        self.assertTrue(all(p.grad is None for p in model.clip_model.vision_model.parameters()))
        model.eval()
        with torch.no_grad():
            logits, _ = author_loss(losses, model, batch, device, False)
        self.assertEqual(logits.shape, (1,))

    def test_atomic_serialization(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "last.pt"
            save_checkpoint(torch, target, {"cursor": 25, "pending_grads": {"weight": torch.ones(1)}})
            state = torch.load(target, weights_only=True, map_location="cpu")
            self.assertEqual(state["cursor"], 25)
            torch.testing.assert_close(state["pending_grads"]["weight"], torch.ones(1))
            self.assertFalse(target.with_suffix(".tmp").exists())


if __name__ == "__main__":
    unittest.main()
