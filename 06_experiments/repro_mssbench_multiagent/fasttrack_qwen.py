"""Locally cached Qwen3-VL derivative for D protocol transfer."""
import os
from pathlib import Path
from time import perf_counter

from pipeline import Generation
from stage1_native import ALLOCATOR_CAP, MemorySample, NativeLlava, QUANTIZATION

MODEL_ID = "Sandy124/ThinkingGuard-8B"
REVISION = "76892f9768ce828268265171f4bbc5dfb75eafc3"
ADAPTER = "fasttrack-thinkingguard-nf4-v1"
IMAGE_MARKER = "<|image_pad|>"


class ThinkingGuard:
    measurements = NativeLlava.measurements

    def __init__(self, checkpoint, gpu_uuid, *, max_new_tokens, seed):
        if os.environ.get("CUDA_VISIBLE_DEVICES") != gpu_uuid or not gpu_uuid.startswith("GPU-"):
            raise ValueError("the selected UUID must be the only visible GPU")
        if os.environ.get("HF_HUB_OFFLINE") != "1":
            raise ValueError("the substitute model must load offline")
        import torch
        from transformers import AutoProcessor, BitsAndBytesConfig, Qwen3VLForConditionalGeneration

        self.memory = MemorySample(gpu_uuid)
        self.torch = torch
        self.device = torch.device("cuda:0")
        if torch.cuda.device_count() != 1:
            raise RuntimeError("expected one visible GPU")
        total = torch.cuda.get_device_properties(self.device).total_memory
        torch.cuda.set_per_process_memory_fraction(min(1, ALLOCATOR_CAP / total), self.device)
        torch.manual_seed(seed)
        self.max_new_tokens = max_new_tokens
        start = perf_counter()
        torch.cuda.reset_peak_memory_stats(self.device)
        with self.memory.measure():
            self.processor = AutoProcessor.from_pretrained(checkpoint, local_files_only=True)
            self.model = Qwen3VLForConditionalGeneration.from_pretrained(
                checkpoint, local_files_only=True, attn_implementation="sdpa",
                dtype=torch.float16, device_map={"": "cuda:0"},
                quantization_config=BitsAndBytesConfig(
                    load_in_4bit=True, bnb_4bit_quant_type=QUANTIZATION["type"],
                    bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16,
                    llm_int8_skip_modules=["visual", "lm_head"]),
            ).eval()
            torch.cuda.synchronize(self.device)
        placements = {str(p.device) for p in self.model.parameters()}
        if placements != {"cuda:0"} or not getattr(self.model, "is_loaded_in_4bit", False):
            raise RuntimeError(f"unexpected device placement or missing NF4: {placements}")
        self.model_load = {"model_load_count": 1, "gpu_uuid": gpu_uuid,
                           "parameter_devices": sorted(placements), "load_ms": (perf_counter()-start)*1000,
                           "torch": torch.__version__, **self.measurements()}

    def generate(self, prompt: str, image: Path | None) -> Generation:
        from PIL import Image

        content = [{"type": "text", "text": prompt}]
        visual_kwargs = {}
        dimensions = processor_dimensions = None
        if image is not None:
            with Image.open(image) as source:
                dimensions = source.size
                pixels = source.convert("RGB").resize((224, 224))
            content.insert(0, {"type": "image"})
            visual_kwargs = {"images": [pixels]}
        rendered = self.processor.apply_chat_template(
            [{"role": "user", "content": content}], tokenize=False, add_generation_prompt=True,
        )
        if rendered.count(IMAGE_MARKER) != int(image is not None):
            raise RuntimeError("template image-marker mismatch")
        batch = self.processor(text=[rendered], return_tensors="pt", **visual_kwargs)
        ids = batch.input_ids
        effective = ids.shape[1]
        visual = int((ids == self.model.config.image_token_id).sum())
        if image is not None:
            if visual <= 1 or "pixel_values" not in batch:
                raise RuntimeError("visual tokens were not expanded")
            _, height, width = batch.image_grid_thw[0].tolist()
            patch = self.model.config.vision_config.patch_size
            processor_dimensions = (width * patch, height * patch)
        elif visual or "pixel_values" in batch:
            raise RuntimeError("text turn contains visual inputs")
        torch = self.torch
        torch.cuda.reset_peak_memory_stats(self.device)
        with self.memory.measure(), torch.inference_mode():
            output = self.model.generate(**batch.to(self.device), do_sample=False, num_beams=1,
                                         max_new_tokens=self.max_new_tokens, use_cache=True,
                                         repetition_penalty=1.0)
            torch.cuda.synchronize(self.device)
        sequence = output[0, effective:]
        answer = self.processor.tokenizer.decode(sequence, skip_special_tokens=True).strip()
        return Generation(answer, rendered_prompt=rendered,
                          input_tokens=effective - visual + int(image is not None),
                          effective_input_tokens=effective, output_tokens=sequence.numel(),
                          image_dimensions=dimensions, processor_dimensions=processor_dimensions,
                          model_load_count=1, **self.measurements())
