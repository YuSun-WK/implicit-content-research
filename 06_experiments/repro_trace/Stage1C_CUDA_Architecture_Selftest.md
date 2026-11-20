# TRACE-S1C · CUDA 计算路径自检

**PASS · `SYNTHETIC_COMPUTE_ONLY_NOT_DATASET_RESULT`。** 使用固定 TRACE 源码和已校验的预训练 CLIP ViT-L/14。每个进程核对 8 个缓存文件并加载模型，自检只用合成像素和固定虚拟文本。单卡 RTX 4090，BF16 autocast，seed 121，复用作者 Classifier、collate 和损失。AdamW 学习率 1e-4，梯度裁剪 1.0。开启确定性算法与 CUBLAS 确定性工作区，关闭 cuDNN benchmark。未改动上游。

| 路径 | Microbatch | 实际 AdamW 调用 | 首步 (s) | 参考续步 (s) | 恢复续步 (s) | 峰值 allocated/reserved (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `trace_text_only_diagnostic` | 1 | 3 | 1.2786 | 0.2466 | 0.2733 | 2.311 / 2.430 |
| `trace_original` | 1 | 3 | 0.9231 | 0.3688 | 0.4368 | 2.651 / 2.672 |
| `trace_text_only_diagnostic` | 2 | 3 | 0.8164 | 0.2595 | 0.2400 | 2.334 / 2.479 |

共 9 次真实 CUDA AdamW 调用。每次运行包含一次首步、一次续步参照和一次从首步 checkpoint 恢复的重放。存盘回读后逐位比对可训练权重、AdamW 状态、scaler 状态及 Python/CPU/CUDA RNG；重放后的状态和 Loss 也逐位一致。BF16 的 GradScaler 保持禁用。步时包含同步、前后向、梯度校验与 AdamW，不含权重加载、保存或回读。

| 首步梯度组 | 单候选 B1 | 三候选 B1 | 单候选 B2 |
|---|---:|---:|---:|
| `caption_scorer` | 0 | 7.33623 | 0 |
| `clip_model.text_model.encoder.layers.4` | 5.2504 | 6.18954 | 2.62095 |
| `clip_model.text_model.encoder.layers.7` | 4.32353 | 5.07107 | 2.07365 |
| `clip_model.text_model.encoder.layers.10` | 5.55847 | 6.06357 | 2.70466 |
| `image_projection` | 10.762 | 10.762 | 5.51143 |
| `text_projection` | 9.8915 | 9.8915 | 4.76246 |
| `cross_attn` | 7.1809 | 7.1809 | 3.61043 |
| `cross_attn_reverse` | 6.10927 | 6.10927 | 3.07548 |
| `pre_output` | 31.7912 | 31.7912 | 16.0959 |
| `classifier` | 13.7597 | 13.7597 | 6.67551 |
| `log_vars` | 0.11415 | 0.444454 | 0.266531 |
| `frozen_grad_count` | 0 | 0 | 0 |
| 首步总 Loss | 0.38585 | 0.456304 | 0.233469 |
| 分类器最大绝对变化 | 0.000100031 | 0.000100031 | 0.000100031 |

日志保留每步 Loss 分量、CUDA 设备级空闲量和 PyTorch 进程峰值。归档仅含数值。权重、合成张量与 Checkpoint 在本地忽略目录或仓库外。

[单候选 B1](stage1c_cuda_text.jsonl) · [三候选 B1](stage1c_cuda_three.jsonl) · [单候选 B2](stage1c_cuda_text_b2.jsonl)

```bash
CLIP_DIR="$HOME/data/trace-assets/clip/32bd64288804d66eefd0ccbe215aa642df71cc41"
CUDA_VISIBLE_DEVICES=0 timeout -k 10s 21540s /tmp/trace-s0-py310/bin/python \
  cuda_architecture_selftest.py --model-dir "$CLIP_DIR" --output-dir .local/s1c-cuda-text
```
