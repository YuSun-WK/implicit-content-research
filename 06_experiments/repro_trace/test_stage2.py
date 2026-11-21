"""Focused checks for two-caption identity, shapes and three-loss gradients."""
from pathlib import Path
import unittest

import torch

from stage2_caption import PROMPT_TEMPLATE, grounding_prompt, parse_caption, records
from stage2_train import author_class, forward_components


class TinyBackbone(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.visual = torch.nn.Linear(4, 8)
        self.text = torch.nn.Embedding(32, 8)
        for parameter in self.visual.parameters():
            parameter.requires_grad = False

    def encode_image(self, images):
        return self.visual(images)

    def encode_text(self, tokens):
        return self.text(tokens).mean(1)


class TinyTrace(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.clip_model = TinyBackbone()
        self.caption_scorer = torch.nn.Linear(8, 1)
        self.image_projection = torch.nn.Linear(8, 8)
        self.text_projection = torch.nn.Linear(8, 8)
        self.cross_attn = torch.nn.Linear(8, 8)
        self.cross_attn_reverse = torch.nn.Linear(8, 8)
        self.pre_output = torch.nn.Linear(16, 8)
        self.classifier = torch.nn.Linear(8, 1)

    def combine_features(self, image, text):
        left = self.image_projection(image)
        right = self.text_projection(text)
        return torch.cat([left + self.cross_attn(right), right + self.cross_attn_reverse(left)], 1)


class Stage2Checks(unittest.TestCase):
    def test_real_complete_case_identity(self):
        root = Path.home() / "data/trace-assets/multioff"
        if not root.is_dir():
            self.skipTest("Official MultiOFF data not mounted")
        rows = records(root)
        self.assertEqual(len(rows), 740)
        self.assertEqual(len({row["key"] for row in rows}), 740)
        self.assertEqual([sum(row["split"] == split for row in rows) for split in ("train", "dev", "test")],
                         [444, 148, 148])

    def test_prompt_and_parser(self):
        self.assertIn("grounding", PROMPT_TEMPLATE)
        self.assertNotIn("{label}", PROMPT_TEMPLATE)
        self.assertIn("high certainty", grounding_prompt({"object": [[0, 0, 1, 1, 0.9]]}))
        self.assertEqual(parse_caption("Caption: A short example"), "A short example")
        for response in ("no marker", "Caption: ", "Caption: No caption"):
            with self.assertRaises(ValueError):
                parse_caption(response)

    def test_author_class_is_pinned(self):
        classifier, digest = author_class(Path("/tmp/trace-s0-reference"), torch)
        self.assertEqual(classifier.__name__, "CLIPClassifier")
        self.assertEqual(len(digest), 64)

    def test_two_caption_losses_and_gradients_at_b1_b2(self):
        for batch in (1, 2):
            with self.subTest(batch=batch):
                torch.manual_seed(42)
                model = TinyTrace()
                image = torch.randn(batch, 4)
                token = torch.randint(1, 32, (batch, 2, 5))
                labels = torch.tensor([i % 2 for i in range(batch)], dtype=torch.float32)
                total, parts, scores, mask = forward_components(model, image, token, labels, 1.0, True, torch)
                self.assertEqual(set(parts), {"classification", "contrastive", "relevance"})
                self.assertEqual(scores.shape, (batch, 2))
                self.assertEqual(mask.shape, (batch, 2))
                self.assertTrue(torch.isfinite(total))
                total.backward()
                for module in (model.caption_scorer, model.clip_model.text, model.image_projection,
                               model.text_projection, model.cross_attn, model.cross_attn_reverse,
                               model.pre_output, model.classifier):
                    self.assertTrue(any(p.grad is not None and p.grad.abs().sum() > 0 for p in module.parameters()))
                self.assertTrue(all(p.grad is None for p in model.clip_model.visual.parameters()))
                model.eval()
                with torch.no_grad():
                    logits, eval_scores, _ = forward_components(model, image, token, labels, 0.1, False, torch)
                self.assertEqual(logits.shape, (batch,))
                self.assertEqual(eval_scores.shape, (batch, 2))


if __name__ == "__main__":
    unittest.main()
