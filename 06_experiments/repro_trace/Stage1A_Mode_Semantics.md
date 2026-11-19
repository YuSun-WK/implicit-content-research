# TRACE-S1A · 模式与运行方式

| 实验模式 | 候选 | 训练目标 | 真实 smoke 梯度验收 |
|---|---|---|---|
| `trace_original`（默认） | 原始文字、作者 InternVL、作者 Gemini | 原作者 Classification + Relevance，训练为 hard Gumbel 选择 | Scorer、文本块 4/7/10、两个投影和融合方向、pre-output、分类器与激活的损失权重有有限非零梯度 |
| `trace_text_only_diagnostic` | 唯一候选，官方 `text`，日志来源为 `original_text` | 仅原作者 Classification focal 分支 | 文本块 4/7/10、两个投影和融合方向、pre-output、分类器及分类损失权重有有限非零梯度，Scorer 非零梯度豁免 |

两者均复用固定上游代码的 CLIP 编码器、重复编码路径、投影、双向融合和分类器，视觉塔及其他被冻结的 CLIP 参数必须无梯度。两者使用各自的日志、Smoke 门禁和 checkpoint 签名，签名含模式、候选字段和损失配置。只用单候选时 Scorer/Gumbel 仍经过作者 cls-only 路径，选项恒定，所以没有排序损失梯度。AdamW 权重衰减仍可作用于收到零梯度张量的 Scorer 参数。CPU fixture 已验证单候选 Scorer 的任务梯度为零；真实 GPU 梯度待验。诊断保留可训练文本块和双向融合。论文 Table 4 的 projection-only CLIP baseline 是另一项实验，本轮没有实现或运行。

## 运行

从 `06_experiments/repro_trace` 执行，`python` 指 Stage 0 隔离解释器（当前机 `/tmp/trace-s0-py310/bin/python`）。采用 [S1A 数据入场](Stage1A_Data_Access_Gate.md) 和 [权重报告](Stage1A_Model_Weights_Report.md) 中的放置路径。将私有 YAML 放在 `.local/`。

```bash
FHM="$HOME/data/trace-assets/fhm"
CLIP_DIR="$HOME/data/trace-assets/clip/32bd64288804d66eefd0ccbe215aa642df71cc41"
python data_manifest.py --image-root "$FHM" --verify-images --tokenizer "$CLIP_DIR" \
  --split-file train "$FHM/train.jsonl" --split-file dev_seen "$FHM/dev_seen.jsonl" \
  --output .local/fhm-summary.json
cp repro_config.yaml .local/s1a-smoke.yaml
```

对实际提供的其他三个 split 各追加一项 `--split-file`。原件完整后，编辑 `.local/s1a-smoke.yaml`。下面为诊断模式示例，项目私有路径用绝对值，只有核实授权才设确认项。

```yaml
mode: smoke
experiment_mode: trace_text_only_diagnostic
data_path: null
split_files:
  train: /authorized/fhm/train.jsonl
  dev_seen: /authorized/fhm/dev_seen.jsonl
image_root: /authorized/fhm
model_dir: /verified/clip/32bd64288804d66eefd0ccbe215aa642df71cc41
authorization_confirmed: true
caption_provenance_confirmed: false
microbatch: 1
accumulation_steps: 1
precision: bf16
output_dir: .local/s1a-diagnostic-b1
```

严格模式使用 `experiment_mode: trace_original`，以 `data_path` 传已核对的合并文件，`split_files: null`，并在核对两列确为作者生成原件后设 `caption_provenance_confirmed: true`。或者使用每个 split 均含已核对原始两列的 split-specific 文件。

```bash
CUDA_VISIBLE_DEVICES=0 timeout -k 10s 5h59m python run_stage0.py --config .local/s1a-smoke.yaml
```

Microbatch 1 通过后，依次对 2、4 做独立一批测试；只有内存余量足够才尝试 8。每个模式和候选用独立输出目录。选定通过者后复制 YAML 为 `.local/s1a-short.yaml`，设 `mode: short`，选择与其完全匹配的 `smoke_checkpoint`，新建独立短跑目录，设 `max_batches: 100` 或更小，`checkpoint_every: 25` 或更小。默认 `threshold: fixed_0.5`，允许可选独立 Dev 校准。训练无 Test 评分入口。

```bash
CUDA_VISIBLE_DEVICES=0 timeout -k 10s 5h59m python run_stage0.py --config .local/s1a-short.yaml
```

相同短跑中断后，保留同一输出目录，设 `resume` 指向其中 `last.pt`，保持相同 seed、数据及配置。Checkpoint 包含可训练参数、pending gradients、优化器、scaler、Python/torch/CUDA RNG 和批游标。每次保存都走相同的恢复代码，短跑随后沿相同种子排序继续。日志记录每批 Loss、更新批的有效 Batch 和梯度、单步耗时及完成时 p50/p95、allocated/reserved 峰值和设备空闲。步计时含本地预处理及 GPU 同步，Checkpoint 耗时可由相邻事件时间戳区分。
