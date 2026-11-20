"""CPU regressions for projection baseline input admission and the pinned author class."""
import csv
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from PIL import Image
import torch

from multioff_baseline import SPLITS, admit, author_classes
from cuda_architecture_selftest import snapshot, verify_equal


class ProjectionBaselineChecks(unittest.TestCase):
    def test_audit_reports_image_overlap_and_preserves_label_counts(self):
        with tempfile.TemporaryDirectory() as private:
            root = Path(private)
            (root / "Labelled Images").mkdir()
            split_dir = root / "Split Dataset"
            split_dir.mkdir()
            for split, name in SPLITS.items():
                image_name = split + ".png"
                Image.new("RGB", (4, 4)).save(root / "Labelled Images" / image_name)
                with (split_dir / f"{name}_meme_dataset.csv").open("w", newline="") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(("image_name", "sentence", "label"))
                    writer.writerow((image_name, "fixture text", "offensive"))
            _, report = admit(root)
        self.assertEqual(report["cross_split_identical_image_hashes"], {"dev+test+train": 1})
        self.assertEqual(report["splits"]["train"]["offensive"], 1)
        self.assertNotIn("fixture text", str(report))

    def test_author_singleton_projection_loss_and_frozen_backbone(self):
        class Tower(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.proj = torch.nn.Linear(2, 2)
            def forward(self, **inputs):
                features = next(iter(inputs.values())).float()
                return SimpleNamespace(pooler_output=self.proj(features))

        class Backbone(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.text_model = Tower()
                self.vision_model = Tower()
                config = SimpleNamespace(hidden_size=2)
                self.config = SimpleNamespace(text_config=config, vision_config=config)

        classifier, focal, collate = author_classes("/tmp/trace-s0-reference", torch, lambda _: Backbone())
        model = classifier(map_dim=8, weight_image_loss=0.3, weight_text_loss=0.7)
        batch = collate([({"input_ids": torch.ones(2), "pixel_values": torch.ones(2),
                           "attention_mask": torch.ones(2)}, torch.tensor(1.0))])
        outputs = model(batch["text_inputs"], batch["image_inputs"], batch["attention_mask"])
        loss = model.calculate_loss(outputs, batch["labels"])
        expected = sum(focal()(outputs[key], batch["labels"]) * coefficient for key, coefficient in
                       (("logits", 1.0), ("image_logits", 0.3), ("text_logits", 0.7)))
        torch.testing.assert_close(loss, expected)
        self.assertEqual(outputs["logits"].shape, (1,))
        loss.backward()
        self.assertIsNone(model.clip_model.vision_model.proj.weight.grad)
        self.assertIsNotNone(model.output.bias.grad)

    def test_selftest_snapshot_holds_values_after_tensor_update(self):
        state = {"trainable": torch.ones(1), "rng": [1, 2]}
        saved = snapshot(state, torch)
        verify_equal(state, saved, torch)
        state["trainable"].zero_()
        with self.assertRaises(AssertionError):
            verify_equal(state, saved, torch)
