# Author and reproduction scope

A0 uses the author prompt with a local ThinkingGuard-8B cache, NF4 quantization and BF16 compute on an RTX 4090 D. The published author result is not a strict comparator for this quantized hardware path. A1 changes only the fifth-stage output instruction to require one terminal verdict; it is a repaired protocol, not the original author prompt. D0 asks the same model to classify directly without five-stage reasoning and uses a 256-token generation cap versus A1's 1,024-token cap. D0 is a prompt baseline, not SFT, DPO or an author Table 3 training ablation.

All Stage 2 predictions must use the fixed model revision `76892f9768ce828268265171f4bbc5dfb75eafc3`, TriggerBench revision `3ac26e778db94a282711f463f22ba6db99643bee`, fixed CSV-derived labels and official LFS image hashes. Any score on a ready-image subset must be described as coverage in progress; final 868-pair Test metrics require explicit terminal status for all 1,736 samples.
