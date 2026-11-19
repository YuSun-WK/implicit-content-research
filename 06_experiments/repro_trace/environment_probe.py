"""Print versions and CUDA inventory without loading model weights."""
import importlib.metadata as metadata
import json
import platform
import subprocess

import torch


def cmd(*args):
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main():
    packages = {}
    for name in ("torch", "torchvision", "transformers", "tokenizers", "clip",
                 "huggingface-hub", "numpy", "pandas", "pillow", "scikit-learn",
                 "PyYAML", "tqdm", "safetensors"):
        try:
            packages[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            packages[name] = None
    from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
    gpus = cmd("nvidia-smi", "--query-gpu=index,name,driver_version,memory.total,memory.free",
               "--format=csv,noheader,nounits")
    print(json.dumps({
        "python": platform.python_version(),
        "packages": packages,
        "clip_implementation": CLIPModel.__module__,
        "processor": CLIPProcessor.__name__,
        "tokenizer": CLIPTokenizerFast.__name__,
        "torch_cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "cuda_visible_devices_count": torch.cuda.device_count(),
        "visible_devices": [
            {"name": torch.cuda.get_device_name(i), "capability": torch.cuda.get_device_capability(i)}
            for i in range(torch.cuda.device_count())
        ],
        "nvidia_smi_columns": ["index", "name", "driver", "total_MiB", "free_MiB"],
        "nvidia_smi": gpus.splitlines(),
    }, indent=2))


if __name__ == "__main__":
    main()
