# Stage 0 CSV audit

**PASS** · SHA-256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`.

8159 records, 8159 with nine columns, 8159 unique UUIDs, 8157 unique URLs and 7638 unique prompts. Schema errors 0.

## Theoretical upper bounds before downloading or decoding images

| Task | Count |
|---|---:|
| E1_image | 8018 |
| E1_text | 8159 |
| E1_joint | 8159 |
| E4_paper_patterns | 8016 |
| E4_release_extras | 2 |
| E4_image_not_sure | 141 |
| Figures4_5_three_valid_gold | 8018 |
| E2_binary_joint | 8159 |
| E3_direct_joint | 8159 |
| E5_paired_direct_cot | 8159 |
| E6_error_decomposition | 8018 |
| E7_behavior_joint | 8159 |
| E1_E2_E5_generations_reusing_direct | 40654 |

## Gold safety labels

| Field | Safe | Borderline | Unsafe | not_sure |
|---|---:|---:|---:|---:|
| image_grade | 4182 | 1810 | 2026 | 141 |
| consensus_text_grade | 4328 | 1452 | 2379 | 0 |
| consensus_combined_grade | 2189 | 3310 | 2660 | 0 |

Image availability **NOT RUN**. The paper describes 8,187 pairs. See the experiment matrix and patterns table for comparisons.
