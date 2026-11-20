# Route B · measured generation cost

Successful model loads 1. Separate preliminary calls 2.
Input counts an unexpanded image as one token. Effective input includes visual grid tokens.

| Method / Role | Call rows | Input tokens | Effective input tokens | Output tokens | Generation s | Allocated GiB | Reserved GiB | NVML delta GiB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base / base | 40 | 4618 | 7138 | 7165 | 588.204 | 6.885 | 7.773 | 8.191 |
| cot / cot | 40 | 7378 | 9898 | 7402 | 603.124 | 6.899 | 7.773 | 8.191 |
| multiagent / intent_reasoning | 20 | 1554 | 1554 | 2256 | 153.584 | 6.856 | 7.771 | 8.189 |
| multiagent / key_object_locator | 20 | 2124 | 3384 | 1151 | 128.110 | 6.880 | 7.773 | 8.191 |
| multiagent / qa | 19 | 3027 | 4224 | 4153 | 331.337 | 6.920 | 7.771 | 8.189 |
| multiagent / safety_judgment | 20 | 3745 | 5005 | 2906 | 250.138 | 6.904 | 7.771 | 8.189 |
| multiagent / safety_reasoning | 20 | 5115 | 6375 | 2709 | 233.443 | 6.921 | 7.773 | 8.191 |
| multiagent / visual_understanding | 20 | 380 | 1640 | 1153 | 130.354 | 6.859 | 7.771 | 8.189 |
| G1+G2 trace total | 199 | 27941 | 39218 | 28895 | 2418.293 | 6.921 | 7.773 | 8.191 |
| Separate probes | 2 | 33 | 96 | 31 | 5.097 | 6.859 | 7.713 | 8.130 |
| Model load peaks | 1 | 0 | 0 | 0 | 0.000 | 7.586 | 7.695 | 8.095 |

Model load elapsed 19.190 s.

Conservative Pilot planning only, 400–1,200 calls for 50–100 pairs depending on task mix. Using 2× the slowest measured call (21.568 s), the upper end at 1,200 calls is 14.38 h plus load/export.

Primary wall time 2479.79 s (41 min 19.79 s), including offline load, probes, G1/G2 and export. Maximum absolute NVML device use during generation was 8.811 GiB. The sampled device delta peaked at 8.191 GiB during generation and 8.095 GiB during load.
