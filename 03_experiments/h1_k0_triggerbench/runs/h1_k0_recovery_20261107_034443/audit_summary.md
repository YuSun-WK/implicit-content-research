# H1-K0 recovery audit

- Source run: `h1_k0_20261106_065826`; source run unchanged.
- Original 36 Test pairs and sampling order preserved; missing pair `test/misinformation/45` recovered without replacement.
- 72/72 images decoded; 72 unique SHA256; review status remains `pending_review`.
- CPU unit tests: 9 passed.
- ThinkingGuard fixed revision weight download failed; no model loaded, no GPU inference, 0 predictions.
- Stopped under network/time condition; no Qwen comparison.
