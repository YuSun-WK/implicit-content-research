# Stage 1 image coverage

**PARTIAL** · Paper 8,187 (AUTHOR-REPORTED), release 8,159 (PINNED CSV).

Processing exhaustive: **False**. FULL means all URLs have terminal outcomes and the acquisition smoke passed. Decoded coverage is reported independently.

Smoke gate PASS. The smoke includes 51 UUIDs and 49 unique URLs, with 30 decoded UUIDs and 21 terminal failures at the gate. Observed full-release UUID coverage is 30/8159 (0.37%).

Unique URLs: 8,157 total, 65 attempted under the URL policy, 58 admitted for network request, 8,092 not attempted.
HTTP 200/206: 31; validated complete bodies: 29 bodies (2,322,371 bytes); decoded URL images: 28.
UUID outcomes: 30 decoded, 30 failed terminally, 7 attempted and unresolved, 8092 not attempted.

Last smoke stop: `COMPLETE`. Last full-run stop: `environment_dns_unavailable`. 8 URLs exhausted the transient DNS attempt budget. These outcomes remain eligible for the documented environment retry.
Requests after successful decode for the same URL: 0.

| Task cohort | Count | Pinned-release gold ceiling |
|---|---:|---:|
| release_roster | 8,159 | 8,159 |
| joint_decoded | 30 | 8,159 |
| image_decoded_gold | 23 | 8,018 |
| text_only_eligible | 8,159 | 8,159 |
| three_modality_intersection | 23 | 8,018 |

The Figure 4/5 intersection is a pre-inference ceiling. E2, E3 and E5 share the joint list.

| Priority pattern | Decoded UUID | Release UUID | Coverage | Terminal failures | Not attempted |
|---|---:|---:|---:|---:|---:|
| S-S-S | 0 | 2166 | 0.00% | 2 | 2161 |
| S-S-B | 1 | 58 | 1.72% | 1 | 56 |
| S-S-U | 2 | 35 | 5.71% | 0 | 32 |
| U-S-B | 4 | 924 | 0.43% | 2 | 918 |
| U-S-U | 0 | 142 | 0.00% | 3 | 139 |
| B-B-U | 1 | 32 | 3.12% | 1 | 30 |

The smoke intentionally oversamples rare patterns. Its outcomes do not estimate overall image availability. Compare the per-pattern and modality-label tables for observed failure concentration and incomplete coverage. Image semantics and historical identity are UNKNOWN. Classification accuracy, F1 and model performance are NOT RUN.

Private immutable UUID manifest SHA-256 `78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512`.
