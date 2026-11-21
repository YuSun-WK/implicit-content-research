"""Single-device adapter for the locked original LLaVA Vicuna checkpoint."""
from contextlib import contextmanager
import os
from pathlib import Path
import threading
from time import perf_counter

from pipeline import Generation

GPU_BUDGET = 20 * 1024**3
ALLOCATOR_CAP = 19 * 1024**3
ADAPTER_REVISION = "stage1-native-v1"
QUANTIZATION = {"bits": 4, "type": "nf4", "double_quant": True, "compute_dtype": "float16"}


class MemorySample:
    """Sample whole-device NVML usage relative to the idle pre-context baseline."""

    def __init__(self, identifier):
        import pynvml

        self.nvml = pynvml
        pynvml.nvmlInit()
        self.device = pynvml.nvmlDeviceGetHandleByUUID(identifier)
        self.baseline = self.used()
        self.peak = self.baseline

    def used(self):
        return self.nvml.nvmlDeviceGetMemoryInfo(self.device).used

    @contextmanager
    def measure(self):
        stop = threading.Event()
        self.peak = self.used()

        def sample():
            while not stop.wait(0.05):
                self.peak = max(self.peak, self.used())

        monitor = threading.Thread(target=sample, daemon=True)
        monitor.start()
        try:
            yield
        finally:
            stop.set()
            monitor.join()
            self.peak = max(self.peak, self.used())

    @property
    def delta(self):
        return max(0, self.peak - self.baseline)


def render_prompt(template, prompt, image, use_markers, tokens):
    image_token, start, end = tokens
    if image_token in prompt or start in prompt or end in prompt:
        raise ValueError("unexpected model image marker in unrendered pipeline input")
    if image is not None:
        prefix = start + image_token + end if use_markers else image_token
        prompt = prefix + "\n" + prompt
    conversation = template.copy()
    conversation.append_message(conversation.roles[0], prompt)
    conversation.append_message(conversation.roles[1], None)
    return conversation.get_prompt()


class NativeLlava:
    def __init__(self, root, gpu_uuid, *, processor="mssbench_224", max_new_tokens=128, seed=0):
        if os.environ.get("CUDA_VISIBLE_DEVICES") != gpu_uuid or not gpu_uuid.startswith("GPU-"):
            raise ValueError("CUDA_VISIBLE_DEVICES must contain only the selected GPU UUID")
        if os.environ.get("HF_HUB_OFFLINE") != "1":
            raise ValueError("the native loader requires an offline, preverified checkpoint")
        if processor not in ("mssbench_224", "native_anyres") or max_new_tokens not in (128, 256):
            raise ValueError("unsupported Stage 1 processor or generation limit")

        import torch
        from llava.constants import DEFAULT_IMAGE_TOKEN, DEFAULT_IM_END_TOKEN, DEFAULT_IM_START_TOKEN
        from llava.conversation import conv_templates
        from llava.model.builder import load_pretrained_model
        from llava.model.language_model.llava_llama import LlavaConfig
        from llava.utils import disable_torch_init

        self.memory = MemorySample(gpu_uuid)
        self.torch = torch
        self.device = torch.device("cuda:0")
        if torch.cuda.device_count() != 1:
            raise RuntimeError("expected exactly one visible CUDA device")
        total = torch.cuda.get_device_properties(self.device).total_memory
        torch.cuda.set_per_process_memory_fraction(min(1, ALLOCATOR_CAP / total), self.device)
        torch.manual_seed(seed)
        self.processor = processor
        self.max_new_tokens = max_new_tokens
        self.template = conv_templates["llava_v1"]
        self.markers = (DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN)
        config = LlavaConfig.from_pretrained(root / "native", local_files_only=True)
        config.mm_vision_tower = str((root / "clip").resolve(strict=True))
        disable_torch_init()
        start = perf_counter()
        torch.cuda.reset_peak_memory_stats(self.device)
        with self.memory.measure():
            self.tokenizer, self.model, self.image_processor, _ = load_pretrained_model(
                str(root / "native"), None, "llava-v1.6-vicuna-7b", load_4bit=True,
                device_map="auto", max_memory={0: "19GiB"}, config=config, local_files_only=True,
            )
            self.model.eval()
            torch.cuda.synchronize(self.device)
        self.load_count = 1
        if not getattr(self.model, "is_loaded_in_4bit", False):
            raise RuntimeError("native model did not report 4-bit loading")
        placements = {str(parameter.device) for parameter in self.model.parameters()}
        if placements != {"cuda:0"}:
            raise RuntimeError(f"single-device model placement violated: {placements}")
        self.model_load = {"model_load_count": self.load_count, "gpu_uuid": gpu_uuid,
                           "parameter_devices": sorted(placements),
                           "hf_device_map": {key: str(value) for key, value in
                                             getattr(self.model, "hf_device_map", {}).items()},
                           "load_ms": round((perf_counter() - start) * 1000, 3),
                           **self.measurements()}

    def measurements(self):
        allocated = self.torch.cuda.max_memory_allocated(self.device)
        reserved = self.torch.cuda.max_memory_reserved(self.device)
        delta = self.memory.delta
        if max(allocated, reserved, delta) >= GPU_BUDGET:
            raise RuntimeError(f"20 GiB GPU budget reached (allocated={allocated}, reserved={reserved}, NVML delta={delta})")
        return {"peak_allocated_bytes": allocated, "peak_reserved_bytes": reserved,
                "nvml_used_bytes": self.memory.peak, "nvml_delta_bytes": delta}

    def generate(self, prompt: str, image: Path | None) -> Generation:
        from PIL import Image
        from llava.constants import IMAGE_TOKEN_INDEX
        from llava.mm_utils import process_images, tokenizer_image_token

        torch = self.torch
        rendered = render_prompt(self.template, prompt, image,
                                 getattr(self.model.config, "mm_use_im_start_end", False), self.markers)
        ids = tokenizer_image_token(rendered, self.tokenizer, IMAGE_TOKEN_INDEX,
                                    return_tensors="pt").unsqueeze(0)
        if (ids == IMAGE_TOKEN_INDEX).sum().item() != int(image is not None):
            raise RuntimeError("rendered prompt image-token count disagrees with role input")
        vision = {}
        original_dimensions = processor_dimensions = None
        torch.cuda.reset_peak_memory_stats(self.device)
        effective = []

        def capture_forward(_model, args, kwargs):
            if not effective:
                inputs = kwargs.get("inputs_embeds")
                if inputs is None:
                    inputs = kwargs.get("input_ids")
                if inputs is not None:
                    effective.append(inputs.shape[1])

        hook = self.model.register_forward_pre_hook(capture_forward, with_kwargs=True)
        try:
            with self.memory.measure(), torch.inference_mode():
                ids = ids.to(self.device)
                if image is not None:
                    with Image.open(image) as source:
                        original_dimensions = source.size
                        rgb = source.convert("RGB")
                    if self.processor == "mssbench_224":
                        rgb = rgb.resize((224, 224))
                    processor_dimensions = rgb.size
                    pixels = process_images([rgb], self.image_processor, self.model.config)
                    if isinstance(pixels, list):
                        pixels = [p.to(self.device, dtype=torch.float16) for p in pixels]
                    else:
                        pixels = pixels.to(self.device, dtype=torch.float16)
                    vision = {"images": pixels, "image_sizes": [rgb.size]}
                output = self.model.generate(ids, **vision, do_sample=False, num_beams=1,
                                             use_cache=True, max_new_tokens=self.max_new_tokens)
                torch.cuda.synchronize(self.device)
        finally:
            hook.remove()
        counters = self.measurements()
        sequence = output[0]
        if sequence.numel() >= ids.shape[1] and torch.equal(sequence[:ids.shape[1]], ids[0]):
            sequence = sequence[ids.shape[1]:]
        elif sequence.numel() and sequence[0].item() == self.tokenizer.bos_token_id:
            # The original LLaVA override calls HF generate with inputs_embeds.
            # Its returned sequence starts with a synthetic BOS, not the prompt.
            sequence = sequence[1:]
        if sequence.numel() > self.max_new_tokens:
            raise RuntimeError(
                f"unexpected continuation token accounting: output={sequence.numel()} "
                f"tokenized_input={ids.shape[1]} effective_input={effective[0] if effective else None} "
                f"output_head={sequence[:8].tolist()} input_head={ids[0, :8].tolist()}"
            )
        answer = self.tokenizer.decode(sequence, skip_special_tokens=True).strip()
        return Generation(
            answer, rendered_prompt=rendered, input_tokens=ids.numel(), output_tokens=sequence.numel(),
            effective_input_tokens=effective[0] if effective else None,
            image_dimensions=original_dimensions, processor_dimensions=processor_dimensions,
            model_load_count=self.load_count, **counters,
        )
