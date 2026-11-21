# Resource measurements

Model loads in this invocation: 1.
All retained trace rows: 206.

| Gate / Role | Calls | Prompt tokens | Output tokens | Elapsed s | Allocated peak B | Reserved peak B | NVML delta peak B |
|---|---:|---:|---:|---:|---:|---:|---:|
| g1 / base | 4 | 656 | 905 | 81.080 | 5874432000 | 7243563008 | 7693795328 |
| g1 / cot | 5 | 1207 | 659 | 60.871 | 5910329856 | 7243563008 | 7693795328 |
| g1 / intent_reasoning | 2 | 252 | 126 | 11.115 | 4374678528 | 6723469312 | 7173701632 |
| g1 / key_object_locator | 3 | 453 | 100 | 11.318 | 5748644352 | 7243563008 | 7693795328 |
| g1 / qa | 2 | 389 | 360 | 29.681 | 5851820544 | 6723469312 | 7173701632 |
| g1 / safety_judgment | 2 | 409 | 118 | 10.808 | 5814100480 | 6723469312 | 7173701632 |
| g1 / safety_reasoning | 3 | 865 | 236 | 22.405 | 5933259264 | 7243563008 | 7693795328 |
| g1 / visual_understanding | 2 | 104 | 85 | 8.098 | 5645910016 | 6723469312 | 7173701632 |
| g2 / base | 36 | 5629 | 7198 | 524.328 | 5873678336 | 7302283264 | 7752450048 |
| g2 / cot | 36 | 8527 | 5591 | 407.754 | 5945541120 | 7302283264 | 7752450048 |
| g2 / intent_reasoning | 19 | 2224 | 1901 | 134.740 | 4440635392 | 7193231360 | 7643398144 |
| g2 / key_object_locator | 18 | 2605 | 795 | 63.415 | 5747990016 | 7302283264 | 7752450048 |
| g2 / qa | 18 | 3227 | 3731 | 265.797 | 5930057728 | 7193231360 | 7643398144 |
| g2 / safety_judgment | 19 | 4657 | 1507 | 115.239 | 5975114240 | 7193231360 | 7643398144 |
| g2 / safety_reasoning | 18 | 4936 | 1667 | 128.845 | 5943682048 | 7493124096 | 7943290880 |
| g2 / visual_understanding | 19 | 988 | 948 | 75.712 | 5648015360 | 7193231360 | 7643398144 |

Load measurements (current invocation)

`[{"model_load_count": 1, "gpu_uuid": "GPU-5a0ba87d-2dc2-fed4-276c-8bb93dcec495", "parameter_devices": ["cuda:0"], "hf_device_map": {"": "0"}, "load_ms": 22915.138, "peak_allocated_bytes": 4153617408, "peak_reserved_bytes": 4192206848, "nvml_used_bytes": 5287182336, "nvml_delta_bytes": 4621402112}]`
