# MSSBench Stage 1

G0 图片及 CPU 测试通过，模型资产和环境未就绪。G1/G2 未执行。正式任务书是 [04_CODEX_STAGE1_PROMPT.md](04_CODEX_STAGE1_PROMPT.md)，执行结论见 [Gate Report](stage1_gate_report.md)。

| 交付 | 路径 |
|---|---|
| 版本对账、图片门槛与逐张审计 | [Table 1](table1_reconciliation.md) · [图片门槛](smoke_image_gate.md) · [CSV](image_decode_audit.csv) |
| 原生环境、渲染差异、代码 | [环境](model_environment_lock.md) · [Adapter](model_adapter_review.md) · [权重核验工具](stage1_weights.py) · [G1/G2 Runner](stage1_smoke.py) |
| 实测证据与状态 | [CPU tests](logs/stage1/tests.log) · [资源](resource_measurements.md) · [指标状态](smoke_metrics.md) |

## 命令

在实验目录中执行。资产目录仅属本实验，提交只含代码、核验结果和日志。已有 JSON 和文件先按锁复核再复用。图片获取按清单限定 40 个文件。

```bash
stage=.stage0-local/stage1
export MSSBENCH_STAGE1_DATA="$stage/data"
export MSSBENCH_OFFICIAL_SOURCE=/tmp/mssbench-stage0-official
export MSSBENCH_NATIVE_SOURCE="$stage/LLaVA-c121f0432da27facab705978f83c4ada465e46fd"
export CUDA_VISIBLE_DEVICES='' PYTHONDONTWRITEBYTECODE=1

python stage1_data.py --data-root "$MSSBENCH_STAGE1_DATA" --out image_decode_audit.csv --download
python -m unittest -v test_stage0 test_stage1

"$stage/native-venv/bin/python" -m pip install -r stage1_native_requirements.txt
curl -fsSL 'https://huggingface.co/api/models/liuhaotian/llava-v1.6-vicuna-7b/revision/deae57a8c0ccb0da4c2661cc1891cc9d06503d11?blobs=true' -o "$stage/native.metadata.json"
curl -fsSL 'https://huggingface.co/api/models/openai/clip-vit-large-patch14-336/revision/ce19dc912ca5cd21c8a653c79e251e808ccabcd1?blobs=true' -o "$stage/clip.metadata.json"
python stage1_weights.py "$stage"
```

固定源路径可由 Stage 0 [复建说明](README.md) 和 [原生源码](https://github.com/haotian-liu/LLaVA/tree/c121f0432da27facab705978f83c4ada465e46fd) 准备，需要 Python 3.10 且该解释器支持 ensurepip 才可创建 venv。下面命令仅在 G0 全部通过、重新确认目标卡空闲后运行。GPU UUID 是本轮遥测候选值。

```bash
gpu=GPU-79ea6ee8-2e76-d1508-7813c1589ec1
CUDA_VISIBLE_DEVICES="$gpu" HF_HUB_OFFLINE=1 PYTHONPATH="$MSSBENCH_NATIVE_SOURCE" \
  "$stage/native-venv/bin/python" stage1_smoke.py --data-root "$MSSBENCH_STAGE1_DATA" \
  --model-root "$stage" --official-source "$MSSBENCH_OFFICIAL_SOURCE" \
  --output "$stage/experiment" --gpu-uuid "$gpu" --through g1
```

`--through g2` 先验证 G1 全部轨迹及保守用时外推，再用同一设置补齐 20 对。相同输出路径可复用 SQLite 结果，每次进程至多加载一个模型实例；失败或中断留存记录。成功后导出逐调用 JSONL、结果 CSV、分组指标和资源测量，不调用外部 Judge。
