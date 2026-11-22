# ThinkingGuard-8B 256-token measured cost

Method inputs: 600; complete: 598; invalid: 2; real generation calls: 1039; cap hits: 291.

| Task | Method | Calls | Input tokens | Output tokens | Sum generation s | Peak allocated GiB | Peak reserved GiB | Peak NVML delta GiB |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| chat | base | 120 | 11794 | 30540 | 2358.1 | 6.880 | 7.773 | 8.191 |
| chat | cot | 120 | 20554 | 28560 | 2220.4 | 6.894 | 7.773 | 8.191 |
| chat | multiagent | 479 | 52467 | 63806 | 5190.9 | 6.920 | 7.773 | 8.191 |
| embodied | base | 80 | 10693 | 8378 | 771.2 | 6.885 | 7.773 | 8.191 |
| embodied | cot | 80 | 15893 | 11009 | 947.2 | 6.899 | 7.773 | 8.191 |
| embodied | multiagent | 160 | 29182 | 16907 | 1550.0 | 6.924 | 7.773 | 8.191 |

| Task | MA / CoT calls | MA / CoT output tokens | MA / CoT generation time |
|---|---:|---:|---:|
| chat | 3.99× | 2.23× | 2.34× |
| embodied | 2.00× | 1.54× | 1.64× |
| all | 3.19× | 2.04× | 2.13× |

| Agent role | Calls | Input tokens | Output tokens | Sum generation s | Cap hits |
|---|---:|---:|---:|---:|---:|
| base | 200 | 22487 | 38918 | 3129.3 | 122 |
| cot | 200 | 36447 | 39569 | 3167.6 | 83 |
| intent_reasoning | 120 | 9394 | 14304 | 968.0 | 0 |
| key_object_locator | 80 | 8533 | 4756 | 522.0 | 0 |
| qa | 119 | 18196 | 26620 | 2087.3 | 78 |
| safety_judgment | 120 | 22597 | 15853 | 1366.1 | 1 |
| safety_reasoning | 80 | 20649 | 12151 | 1028.0 | 7 |
| visual_understanding | 120 | 2280 | 7029 | 769.4 | 0 |
