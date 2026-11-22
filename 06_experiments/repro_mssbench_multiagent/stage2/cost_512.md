# ThinkingGuard-8B 512-token measured cost

Method inputs: 60; complete: 60; invalid: 0; real generation calls: 100; cap hits: 10.

| Task | Method | Calls | Input tokens | Output tokens | Sum generation s | Peak allocated GiB | Peak reserved GiB | Peak NVML delta GiB |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| chat | base | 10 | 984 | 4549 | 338.3 | 6.877 | 7.771 | 8.189 |
| chat | cot | 10 | 1714 | 2873 | 224.2 | 6.892 | 7.771 | 8.189 |
| chat | multiagent | 40 | 4863 | 5378 | 450.8 | 6.914 | 7.771 | 8.189 |
| embodied | base | 10 | 1350 | 1848 | 153.6 | 6.884 | 7.773 | 8.191 |
| embodied | cot | 10 | 2000 | 2320 | 184.9 | 6.898 | 7.773 | 8.191 |
| embodied | multiagent | 20 | 3644 | 2772 | 241.1 | 6.919 | 7.773 | 8.191 |

| Task | MA / CoT calls | MA / CoT output tokens | MA / CoT generation time |
|---|---:|---:|---:|
| chat | 4.00× | 1.87× | 2.01× |
| embodied | 2.00× | 1.19× | 1.30× |
| all | 3.00× | 1.57× | 1.69× |

| Agent role | Calls | Input tokens | Output tokens | Sum generation s | Cap hits |
|---|---:|---:|---:|---:|---:|
| base | 20 | 2334 | 6397 | 491.8 | 8 |
| cot | 20 | 3714 | 5193 | 409.0 | 1 |
| intent_reasoning | 10 | 784 | 1250 | 87.8 | 0 |
| key_object_locator | 10 | 1080 | 564 | 64.0 | 0 |
| qa | 10 | 1979 | 2278 | 183.5 | 1 |
| safety_judgment | 10 | 1910 | 1292 | 115.3 | 0 |
| safety_reasoning | 10 | 2564 | 2208 | 177.1 | 0 |
| visual_understanding | 10 | 190 | 558 | 64.2 | 0 |
