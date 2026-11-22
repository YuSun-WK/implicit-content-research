"""Read Python metadata and import torch with CUDA hidden; no GPU initialization."""

from importlib.metadata import PackageNotFoundError, version
import os
import sys

print("python", sys.version.split()[0])
print("CUDA_VISIBLE_DEVICES", repr(os.getenv("CUDA_VISIBLE_DEVICES")))
for package in ("torch", "torchvision", "transformers", "accelerate", "bitsandbytes",
                "huggingface-hub", "Pillow", "openai", "tqdm", "sentencepiece", "llava",
                "nvidia-cuda-runtime-cu12"):
    try:
        installed = version(package)
    except PackageNotFoundError:
        installed = "missing"
    print(package, installed)
if os.getenv("CUDA_VISIBLE_DEVICES") != "":
    raise SystemExit("run with CUDA_VISIBLE_DEVICES=''")
try:
    import torch
except ModuleNotFoundError as exc:
    print(exc)
else:
    print("torch runtime CUDA build", torch.version.cuda)
    print("torch CUDA initialized", torch.cuda.is_initialized())
    assert not torch.cuda.is_initialized()
