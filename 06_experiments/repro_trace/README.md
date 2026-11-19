# TRACE Stage 0 · FHM ViT-L/14

**DATA_BLOCKED · Stage 2 BLOCKED。** 已完成固定源码、参数、环境与本地数据可用性审计，包装层通过 CPU 小型 fixture。真实 FHM smoke 和短跑均待授权原件。 [门禁决策](Gate_Decision.md) · [实验状态](100_batch_report.md)

- [固定版本及文件哈希](upstream_manifest.json) · [论文与代码证据](TRACE_Stage0_Code_Map.md) · [逐参数清单](parameter_manifest.csv)
- [Caption 可用性与来源](Caption_Availability_and_Provenance.md) · [仅统计数据清单](data_manifest_summary.json)
- [隔离环境和版本](environment_report.md) · [运行配置](repro_config.yaml)

从研究仓库目标分支的 `06_experiments/repro_trace` 目录执行。下文 `python` 指 [环境报告](environment_report.md) 中的隔离解释器。共享主机当前的上游检出位于 `/tmp/trace-s0-reference`。在新机器上可复建。

```bash
git clone https://github.com/surrey-nlp/TRACE.git /tmp/trace-s0-reference
git -C /tmp/trace-s0-reference checkout --detach 83ecb799f897fe275185e082ee9a669f7d04bfaa
mkdir -p .local
curl -fLsS https://huggingface.co/openai/clip-vit-large-patch14/raw/32bd64288804d66eefd0ccbe215aa642df71cc41/config.json -o .local/clip-config.json
CUDA_VISIBLE_DEVICES=0 python environment_probe.py
python run_stage0.py
python -m unittest -v
```

Dry-run 的 `.local/run/parameters.json` 来自 meta device，仅需固定公开配置。训练请求会校验来源声明、本地文件和上游 SHA；完整模型快照文件清单与 SHA 在 `upstream_manifest.json`。训练时 Transformers 和 Hugging Face Hub 使用离线模式，W&B 关闭。包装层复用上游分类器、collate、三候选输入、损失函数、默认 cls+rel 与 AdamW（学习率 1e-4，梯度裁剪为 1）。差异是延迟读图、显式 eager attention 和 processor 配置、单样本 relevance 目标向量兼容、单卡 AMP、按批保存与独立 Dev 阈值路径。

### 有授权原件后

先生成本地统计。也可多次使用 `--split-file SPLIT FILE` 单独检查官方标签文件。训练时需提供完成原始 Caption 对齐的合并 JSON/JSONL。将数据与权重目录保留在 Git 追踪范围之外。

```bash
python data_manifest.py --data /authorized/trace.json \
  --image-root /authorized/fhm --tokenizer /authorized/clip-snapshot \
  --output .local/fhm-summary.json
cp repro_config.yaml .local/smoke.yaml
```

在 `.local/smoke.yaml` 设 `mode: smoke`、本地 `data_path`、`image_root`、`model_dir`、`output_dir: .local/smoke-b1`。核实来源后将两个确认项设为 true。首选 `microbatch: 1`、`accumulation_steps: 1`、`precision: bf16`。只有相同 microbatch、精度和来源的 smoke 证据可用于 short。需要测 2、4、8 时各自先做一批，使用独立输出目录。

```bash
CUDA_VISIBLE_DEVICES=0 timeout -k 10s 5h59m python run_stage0.py --config .local/smoke.yaml
```

核对 `events.jsonl` 的 Loss、真实分类器权重变化、各模块梯度、冻结梯度计数、显存和 `checkpoint_restored`。全部通过后复制为 `.local/short.yaml`，设 `mode: short`、`smoke_checkpoint: .local/smoke-b1/last.pt` 和独立 `output_dir`。可设置 `accumulation_steps`、`max_batches`（≤100）与 `checkpoint_every`（≤25）。短跑从固定种子重新开始，烟雾结果用于准入。若中断，将 `resume` 指向该短跑的 `last.pt`，保持批数上限、模型、路径、种子、精度和累积设置，使用相同命令继续。Checkpoint 保存可训练权重、优化器、scaler、RNG、待累积梯度和批游标，冻结部分由已核验快照重建。保存后回读，恢复路径与重启共用。保持原图目录内容稳定。

```bash
CUDA_VISIBLE_DEVICES=0 timeout -k 10s 5h59m python run_stage0.py --config .local/short.yaml
```

默认仅训练并预设阈值 0.5。可设 `evaluate_dev: true` 记录固定阈值下的 Dev 指标，或设 `threshold: dev_f1` 仅用配置的 Dev split 校准并记录冻结阈值。Dev 校准集指标属于校准过程。日志与 checkpoint 写入忽略的 `.local/`。父进程超时命令限制单次运行，运行器同时设置 18 GiB PyTorch allocator 上限并在训练阶段记录 allocated、reserved 峰值。CUDA context 等进程开销不计入 PyTorch 指标。
