"""CPU-only checks using small fixtures, including an isolated resume test."""
import contextlib
import io
import json
import os
from pathlib import Path
import random
import tempfile
import unittest

import torch
from PIL import Image
from transformers import CLIPConfig, CLIPModel

from data_manifest import FIELDS, read_rows, summary
from prepare_clip import WeightsBlocked, inspect_files, require_verified
from run_stage0 import (
    AuthorCaptionsBlocked, DIAGNOSTIC, LOSS_CONFIG, ORIGINAL, assert_inputs,
    author_loss, dataset_digest, grad_report, restore, rng_state, save_checkpoint, threshold_for, upstream,
)


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

    def test_missing_author_captions_only_block_original(self):
        with tempfile.TemporaryDirectory() as private:
            root = Path(private)
            paths = {}
            for split, item in (("train", 10), ("dev_seen", 20)):
                img = f"{item}.png"
                Image.new("RGB", (4, 4)).save(root / img)
                paths[split] = root / f"{split}.jsonl"
                paths[split].write_text(json.dumps({"id": item, "img": img, "label": 0,
                                                   "text": "CPU fixture"}) + "\n")
            source = root / "combined.json"
            source.write_text(json.dumps([row for split, path in paths.items() for row in read_rows(path, split)]))
            cfg = {"data_path": source, "image_root": root, "model_dir": root,
                   "authorization_confirmed": True, "caption_provenance_confirmed": False,
                   "train_split": "train", "dev_split": "dev_seen"}
            with self.assertRaisesRegex(AuthorCaptionsBlocked, "captions.*train"):
                assert_inputs(cfg)
            diagnostic = {**cfg, "data_path": None, "split_files": paths, "experiment_mode": DIAGNOSTIC}
            rows, model_dir = assert_inputs(diagnostic)
            self.assertEqual(model_dir, root)
            self.assertEqual([(row["id"], row["img"], row["split"]) for row in rows],
                             [(10, "10.png", "train"), (20, "20.png", "dev_seen")])
            source.write_text(json.dumps([{**row, "ivl_8b_new_caption": "fixture A",
                                          "gemini_caption": "fixture B"} for row in rows]))
            with self.assertRaisesRegex(AuthorCaptionsBlocked, "provenances"):
                assert_inputs(cfg)
            matched_rows, _ = assert_inputs({**cfg, "caption_provenance_confirmed": True})
            self.assertEqual(dataset_digest(rows, ("text",)), dataset_digest(matched_rows, ("text",)))

    def test_image_integrity_counts(self):
        with tempfile.TemporaryDirectory() as private:
            root = Path(private)
            (root / "broken.png").write_bytes(b"bad image")
            refs = ("broken.png", "gone.png", "../outside.png")
            report = summary([{"img": ref, "split": "train"} for ref in refs], root,
                             verify_splits=("train",))
            stats = report["splits"]["train"]
            self.assertEqual(stats["images_invalid_path"], 1)
            self.assertEqual(stats["images_missing"], 1)
            self.assertEqual(stats["images_unreadable"], 1)

    def test_weights_reject_wrong_or_missing_sha(self):
        with tempfile.TemporaryDirectory() as private:
            root = Path(private)
            (root / "config.json").touch()
            report = inspect_files(root, {"files": {"config.json": "bad", "model.safetensors": "missing"}})
            with self.assertRaisesRegex(WeightsBlocked, "sha_mismatch.*missing"):
                require_verified(report)

    def test_threshold(self):
        self.assertEqual(threshold_for("fixed_0.5", [], []), 0.5)
        self.assertAlmostEqual(threshold_for("dev_f1", [0, 1], [0.2, 0.8]), 0.8)
        with self.assertRaisesRegex(ValueError, "both binary"):
            threshold_for("dev_f1", [1], [0.8])

    @staticmethod
    def small_author_model():
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
        return model, collate, losses

    def test_small_author_path_singleton(self):
        torch.set_num_threads(1)
        torch.manual_seed(121)
        device = torch.device("cpu")
        model, collate, losses = self.small_author_model()
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

    def test_single_text_candidate_uses_only_classification(self):
        torch.set_num_threads(1)
        torch.manual_seed(121)
        model, collate, losses = self.small_author_model()
        batch = collate([{"pixel_values": torch.randn(3, 4, 4),
                          "input_ids": [torch.ones(77, dtype=torch.long)],
                          "attention_mask": [torch.ones(77, dtype=torch.long)],
                          "labels": torch.tensor(1.), "image_ids": "fixture", "num_captions": 1}])
        self.assertEqual(batch["input_ids"].shape, (1, 1, 77))
        self.assertEqual(batch["labels"].shape, (1,))
        device = torch.device("cpu")
        with self.assertRaisesRegex(ValueError, "Candidate count"):
            author_loss(losses, model, batch, device, True, ORIGINAL)
        loss, components = author_loss(losses, model, batch, device, True, DIAGNOSTIC)
        self.assertEqual(len(components), 1)
        self.assertTrue(torch.isfinite(loss))
        loss.backward()
        grads = grad_report(model, torch)
        self.assertEqual(grads["caption_scorer"], 0)
        self.assertEqual(grads["frozen_grad_count"], 0)
        for group in ("classifier", "clip_model.text_model.encoder.layers.4",
                      "text_projection", "image_projection", "cross_attn"):
            self.assertGreater(grads[group], 0)
        model.eval()
        with torch.no_grad():
            logits, _ = author_loss(losses, model, batch, device, False, DIAGNOSTIC)
        self.assertEqual(logits.shape, (1,))

    def test_diagnostic_checkpoint_resume_and_mode_mismatch(self):
        device = torch.device("cpu")
        signature = {"experiment_mode": DIAGNOSTIC, "candidate_fields": ["text"]}
        model = torch.nn.Linear(2, 1)
        optimizer = torch.optim.AdamW(model.parameters())
        scaler = torch.amp.GradScaler("cpu", enabled=False)
        example = torch.ones(1, 2)
        model(example).sum().backward()
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        model(example).sum().backward()
        with tempfile.TemporaryDirectory() as private:
            path = Path(private) / "last.pt"
            save_checkpoint(torch, path, {
                "signature": signature, "cursor": 3, "updates": 1,
                "trainable": {name: p.detach() for name, p in model.named_parameters()},
                "pending_grads": {name: p.grad for name, p in model.named_parameters()},
                "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                "rng": rng_state(torch, device),
            })
            next_python, next_tensor = random.random(), torch.rand(1)
            reloaded = torch.nn.Linear(2, 1)
            reloaded_opt = torch.optim.AdamW(reloaded.parameters())
            with self.assertRaisesRegex(ValueError, "signature mismatch"):
                restore(torch, path, reloaded, reloaded_opt, scaler, {"experiment_mode": ORIGINAL})
            cursor = restore(torch, path, reloaded, reloaded_opt, scaler, signature)
            self.assertEqual(cursor, (3, 1))
            self.assertEqual(random.random(), next_python)
            torch.testing.assert_close(torch.rand(1), next_tensor)
            for expected, actual in zip(model.parameters(), reloaded.parameters()):
                torch.testing.assert_close(actual, expected)
                torch.testing.assert_close(actual.grad, expected.grad)
            optimizer.step()
            reloaded_opt.step()
            for expected, actual in zip(model.parameters(), reloaded.parameters()):
                torch.testing.assert_close(actual, expected)

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
