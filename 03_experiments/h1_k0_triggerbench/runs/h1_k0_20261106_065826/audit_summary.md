# H1-K0 audit summary

Status: stopped before GPU inference under the six-hour budget rule.

- CSV files: 36 (18 Test, 18 Train); 5,600 rows.
- Reconstructed pairs: 2,800 total, including 868 Test and 1,932 Train. No invalid CSV pairs.
- Exact text overlap between Train and Test: 0 unique texts.
- CSV index differs from the image filename in 442 pairs; explicit mapping uses the original image basename.
- Selected: 36 Test pairs (4 in each of 9 categories), seed 20261105.
- Images decoded: 70/72; complete selected pairs: 35/36. The missing pair is test/misinformation/45.
- Image review remains pending_review. Contact sheets are for human review only.
- ThinkingGuard download failed before model load; Qwen 8B download and GPU inference did not start.
- No accuracy, pair accuracy, or model comparison is available.
