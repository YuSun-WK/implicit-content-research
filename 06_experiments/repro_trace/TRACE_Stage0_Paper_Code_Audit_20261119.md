# TRACE (AAAI 2026 AISI) — Stage 0 Paper Reading & Reproduction Gate
Date: 2026-11-19
Status: Literature/code audit complete; no local GPU training or dataset acquisition verified.
Venue: AAAI 2026, Special Track on AI for Social Impact (AISI), CCF-A.
Paper: https://ojs.aaai.org/index.php/AAAI/article/view/41220
Supplement: https://arxiv.org/pdf/2504.17902
Official code: https://github.com/surrey-nlp/TRACE
Pinned public code commit: 83ecb799f897fe275185e082ee9a669f7d04bfaa

## 1. Scope and reporting rules
Reproduce FHM CLIP ViT-L/14 pathway first. No VLSU migration, no new model, no paid API, no proprietary LVLM inference. Differentiate (i) paper-table reproduction; (ii) verbatim public-code reproduction; (iii) original-text or partial-caption constrained reproduction; (iv) adapted open-source-caption reproduction. Do not equate these.

## 2. Architecture
Image + Meme overlaid text -> RAM++ tags -> GroundingDINO open-vocabulary detections -> grounded caption generation by InternVL2.5-8B / Gemini-2.5-Flash -> candidates (original text, InternVL, Gemini) -> CLIP text encoder -> caption MLP scorer -> Gumbel-Softmax hard selection (training), soft weighted combination (inference) -> projection + bidirectional cross-attention + classifier.
Image CLIP tower frozen; selected text encoder blocks, caption scorer, projections, attention, and classifier trainable.

## 3. Main scientific results (author-reported, not reproduced)
Paper Table 4 FHM CLIP-ViT-L/14 projection-only Acc .720 F1 .710.
Table 5 FHM ViT-L/14 T(-1): Acc .743 F1 .740; T(-4): Acc .764 F1 .764.
Table 5 FHM CLIP-XLM-R-ViT-H/14 T(-4): Acc .807 F1 .806 (best headline is NOT the ViT-L/14 result).
Table 6 MultiOFF TRACE with XLM-R-ViT-H/14 T(-4), cls+rel: Acc .678 F1 .673.
Table 5 is a text-layer tuning ablation with Lcls+Lrel, NOT a four-cell classification/relevance/contrastive loss ablation.

## 4. Implementation discrepancies / reproducibility blockers
1. clip_vitL_14_ft.py L122-130 unfreezes [n-2,n-5,n-8], i.e. three NONCONSECUTIVE layers for n=12; paper T(-4) is last four layers. Freeze/unfreeze manifests must record names/counts.
2. clip_vitL_14_ft.py L427 data path points to private /backup/girish_datasets/Hateful_Memes_Extended/ivl_plus_gemini_captions_complete.json. No complete captions file appears in public Git tree as of audit; GitHub releases API returns []. Do not assert that no other author-hosted file exists.
3. Training requires image, text, label, split, ivl_8b_new_caption, gemini_caption for full candidate-set reproduction. Dataset code inserts literal "No caption" if absent, so missing fields must be audited, not silently treated as valid generated captions.
4. vg_caption_gen.py actively calls Gemini 'gemini-2.0-flash-exp' at L463; manuscript says Gemini-2.5-Flash; local InternVL loading/generation lines are commented out in the active process; RAM++ weight file ram_plus_swin_large_14m.pth is referenced but not included in repo. GroundingDINO is HF IDEA-Research/grounding-dino-base.
5. Paper Lrel is written using sum of Gumbel-Softmax probabilities (which equals one), whereas public utils/loss_functions.py L623-649 computes FocalLoss on MEAN RAW caption logits against sample label. Code's classification loss also uses FocalLoss, whereas paper prose describes BCE.
6. In calculate_loss_gs(), classification-only may STILL use scorer/Gumbel selection; enabling/disabling relevance changes caption selection policy vs contrastive-only cosine, confounding pure loss attribution. Train/inference selection differs (hard Gumbel vs softmax mixture).
7. clip_vitL_14_ft.py uses batch=128, accumulated to 512, not paper's physical batch=64 (effective to 512). GPU limits prohibit unmeasured batch=128. Code forwards visual tower twice (pooler + get_image_features) and text tower twice per candidate (pooler + get_text_features), increasing memory/compute.
8. evaluate_model() L375-383 chooses precision-recall F1 threshold ON THE EVALUATED LABELS. This includes test, causing leakage in metrics. Must log legacy behavior and add validation-only frozen threshold for valid evaluation. It has a possible thresholds indexing edge case.
9. checkpoint path best_model.pth is overwritten every epoch, including nonbest epochs; best_epoch can disagree with saved state. Resume resets best_val_auc=0 later in main; use corrected best/last separate files for actual runs, document as reproducibility fix.
10. benco_eval.py is for CLIP-XLM-R-ViT-H/14 and requires pseudo_text_idx/pseudo_img_idx (not guaranteed in base FHM); it also optimizes threshold on test labels. It does not directly evaluate ViT-L/14 checkpoint. Pair analysis must use label-opposite linked examples and validation threshold.
11. The two nn.MultiheadAttention layers receive sequences of length ONE for Q,K,V; attention softmax along single key is identically one. Thus these blocks function as learned cross-modal feature transforms, not nontrivial spatial/token-level attention.
12. Official requirements.txt is a broad mixed environment with torch 2.3.1, torchvision .18.1, transformers 4.26.1, openai CLIP git, and flash-attn 2.6.3; installed extras may conflict. Inspect imports and create separate minimal reproducible env file (record deviations).

## 5. Dataset gates
FHM: train 8500; dev_seen 500; test_seen 1000 in paper. There are also dev_unseen and test_unseen splits in repo; do not mix. Official license/registration at https://www.drivendata.org/competitions/64/hateful-memes/page/214/ ; Meta states access through DrivenData. Never commit images/data.
MultiOFF: 445 train, 149 validation, 149 test; OFFENSIVE vs NON-OFFENSIVE (not FHM hateful labels). Official publisher: https://zenodo.org/records/3899868 .
Do not inspect/optimize official test labels for threshold or model selection. Report split availability and metadata separately.

## 6. Cost and stop rules
Paper reports approx 2 hours per experiment on TWO 24GiB A5000 GPUs and says batch 64, accumulation up to 512; not evidence of our single-card runtime.
ViT-L/14 model approx 428M params (paper Table 1); 1.7 GB fp32 raw weights or 0.86 GB fp16/bf16 (EXCLUDING activations, optimizer, caches). Trainable parameter count/peak memory MUST be measured, not estimated as fact.
On ~16–20GiB, initial candidate microbatches: 2 then 4 then 8 only if safe; effective 128/256/512 conditional on wall clock. 100 batch dry run before any multi-epoch execution; record step times, max allocated/reserved VRAM, optimizer step, nonzero finite grads, loss, checkpoint roundtrip.
Run under <=6h per job, checkpoint each epoch and periodically; abort on OOM or >18GiB sustained peak, produce logs.

## 7. Stage priorities
P0 legality/caption provenance/data manifest; P0 code freeze/parameter map; P0 100 batch smoke.
P1 FHM genuine cls+rel using available original captions; P1 paper-aligned ViT-L/14 T(-4) if faithfully possible; P1 evaluation without test threshold leakage.
P2 controlled ablations (cls; cls+rel; cls+cont; all), label selection-policy differences, same backbone/data/caption source.
P2 confounders paired evaluation, error examples with permitted image use.
P3 MultiOFF only after FHM gates.
## Source notes
This is code-level audit, NOT proof of any local experimental outcomes.
