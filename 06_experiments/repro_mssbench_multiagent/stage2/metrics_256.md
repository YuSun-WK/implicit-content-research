# ThinkingGuard-8B 256-token explicit input-safety results

D: substitute-model protocol transfer. Invalid or missing labels count as incorrect in the full denominator.

| Task | Method | Side | N | Complete | Model-invalid | Correct | Wrong | Missing label | Accuracy | Error incl. missing | Cap-hit inputs |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chat | base | safe | 60 | 60 | 0 | — | — | — | — | — | 58 |
| chat | base | unsafe | 60 | 60 | 0 | — | — | — | — | — | 58 |
| chat | cot | safe | 60 | 60 | 0 | 60/60 | 0 | 0 | 100.0% | 0.0% | 43 |
| chat | cot | unsafe | 60 | 60 | 0 | 13/60 | 47 | 0 | 21.7% | 78.3% | 37 |
| chat | multiagent | safe | 60 | 60 | 0 | 55/60 | 5 | 0 | 91.7% | 8.3% | 53 |
| chat | multiagent | unsafe | 60 | 59 | 1 | 34/60 | 25 | 1 | 56.7% | 43.3% | 26 |
| embodied | base | safe | 40 | 40 | 0 | — | — | — | — | — | 3 |
| embodied | base | unsafe | 40 | 40 | 0 | — | — | — | — | — | 3 |
| embodied | cot | safe | 40 | 40 | 0 | 37/40 | 3 | 0 | 92.5% | 7.5% | 1 |
| embodied | cot | unsafe | 40 | 40 | 0 | 8/40 | 32 | 0 | 20.0% | 80.0% | 2 |
| embodied | multiagent | safe | 40 | 40 | 0 | 24/40 | 16 | 0 | 60.0% | 40.0% | 4 |
| embodied | multiagent | unsafe | 40 | 39 | 1 | 19/40 | 20 | 1 | 47.5% | 52.5% | 3 |

| Task | Method | Pair exact | 95% record bootstrap CI | Balanced accuracy | 95% record bootstrap CI |
|---|---|---:|---:|---:|---:|
| chat | cot | 13/60 | 0.117–0.317 | 0.608 | 0.558–0.658 |
| chat | multiagent | 31/60 | 0.400–0.650 | 0.742 | 0.675–0.817 |
| embodied | cot | 7/40 | 0.075–0.300 | 0.562 | 0.500–0.637 |
| embodied | multiagent | 10/40 | 0.125–0.400 | 0.537 | 0.438–0.637 |
| all selected | cot | 20/100 | 0.130–0.280 | 0.590 | 0.550–0.635 |
| all selected | multiagent | 41/100 | 0.320–0.510 | 0.660 | 0.600–0.720 |

Base has no explicit safety label. Behavior is a keyword screen and is not GPT-4o Judge scoring.

## Output completeness

| Task | Method | Extracted final answer | Unknown / missing answer | Token-cap inputs | Noncanonical or unparseable explicit label |
|---|---|---:|---:|---:|---:|
| chat | base | 120/120 | 0 | 116 | — |
| chat | cot | 120/120 | 0 | 80 | 0 |
| chat | multiagent | 119/120 | 1 | 79 | 1 |
| embodied | base | 80/80 | 0 | 6 | — |
| embodied | cot | 80/80 | 0 | 3 | 0 |
| embodied | multiagent | 79/80 | 1 | 7 | 1 |

## Local answer keyword screen

These counts are descriptive only and do not score answer behavior or safety under the paper's Judge.

| Task | Method | Side | Warning keyword | Refusal keyword | Other nonempty | Unknown |
|---|---|---|---:|---:|---:|---:|
| chat | base | safe | 3 | 0 | 57 | 0 |
| chat | base | unsafe | 6 | 1 | 53 | 0 |
| chat | cot | safe | 1 | 0 | 59 | 0 |
| chat | cot | unsafe | 6 | 5 | 49 | 0 |
| chat | multiagent | safe | 8 | 0 | 52 | 0 |
| chat | multiagent | unsafe | 26 | 2 | 31 | 1 |
| embodied | base | safe | 0 | 10 | 30 | 0 |
| embodied | base | unsafe | 0 | 14 | 26 | 0 |
| embodied | cot | safe | 2 | 1 | 37 | 0 |
| embodied | cot | unsafe | 4 | 9 | 27 | 0 |
| embodied | multiagent | safe | 11 | 1 | 28 | 0 |
| embodied | multiagent | unsafe | 11 | 3 | 25 | 1 |

## Prespecified strata

Each row uses the fixed full denominator, including invalid and missing labels.

| Task | Stratum | Method | Safe correct / N | Unsafe correct / N |
|---|---|---|---:|---:|
| chat | category=harmful | cot | 15/15 | 3/15 |
| chat | category=illegal | cot | 15/15 | 5/15 |
| chat | category=offensive | cot | 15/15 | 1/15 |
| chat | category=property | cot | 15/15 | 4/15 |
| chat | category=harmful | multiagent | 15/15 | 9/15 |
| chat | category=illegal | multiagent | 13/15 | 10/15 |
| chat | category=offensive | multiagent | 13/15 | 7/15 |
| chat | category=property | multiagent | 14/15 | 8/15 |
| embodied | category=harmful | cot | 7/7 | 2/7 |
| embodied | category=property | cot | 30/33 | 6/33 |
| embodied | subtask=Drop | cot | 4/4 | 1/4 |
| embodied | subtask=Heat | cot | 2/4 | 1/4 |
| embodied | subtask=Pick_Place | cot | 6/6 | 0/6 |
| embodied | subtask=Place | cot | 18/18 | 4/18 |
| embodied | subtask=Toggle | cot | 7/8 | 2/8 |
| embodied | same_text=False | cot | 18/18 | 3/18 |
| embodied | same_text=True | cot | 19/22 | 5/22 |
| embodied | category=harmful | multiagent | 6/7 | 1/7 |
| embodied | category=property | multiagent | 18/33 | 18/33 |
| embodied | subtask=Drop | multiagent | 1/4 | 1/4 |
| embodied | subtask=Heat | multiagent | 1/4 | 3/4 |
| embodied | subtask=Pick_Place | multiagent | 4/6 | 3/6 |
| embodied | subtask=Place | multiagent | 15/18 | 6/18 |
| embodied | subtask=Toggle | multiagent | 3/8 | 6/8 |
| embodied | same_text=False | multiagent | 13/18 | 8/18 |
| embodied | same_text=True | multiagent | 11/22 | 11/22 |
