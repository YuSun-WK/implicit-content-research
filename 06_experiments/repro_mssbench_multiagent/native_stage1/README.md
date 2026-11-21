# 原始 LLaVA Stage 1 实测档案

模型：`liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11`；视觉塔：`openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1`。固定 HF MSSBench 数据 revision 为 `12396d24157427b671d97f23a2e370fca98fdf55`。40 张 Smoke 图像沿用 [逐文件解码审计](../image_decode_audit.csv)，本轮没有重取全数据集。

| 文件 | 内容 |
|---|---|
| [weights_verified.json](weights_verified.json) | 12 个本地模型文件的官方版本、大小、哈希锁；权重本体不入库 |
| [environment_freeze.txt](environment_freeze.txt) | 独立 venv 的包版本快照 |
| [preliminary_probes.jsonl](preliminary_probes.jsonl) | 同一模型实例的文本与单图探针原始结果 |
| [model_loads.jsonl](model_loads.jsonl) | 256-token 续跑中 5 次独立进程加载、设备放置与显存 |
| [smoke_results.csv](smoke_results.csv) | 20 对 × 双侧 × 三方法的最终状态与初步标签 |
| [canonical_agent_traces.jsonl](canonical_agent_traces.jsonl) | 200 次规范调用的完整输入 Prompt、图像路径、原始输出、解析和资源数据 |
| [retry_agent_traces.jsonl](retry_agent_traces.jsonl) | 6 次因工程/格式修复而重试的调用；不计入规范 200 次 |
| [agent_traces.jsonl](agent_traces.jsonl) | 206 次保留调用的原始导出 |
| [canonical_summary.json](canonical_summary.json) | 规范调用和重试成本分列 |
| [smoke_metrics.md](smoke_metrics.md) | Chat/Embodied、Safe/Unsafe 分组及配对指标 |
| [resource_measurements.md](resource_measurements.md) | 全部保留轨迹的角色成本，包含重试 |
| [final_run.log](final_run.log) | 完成 G2 的真实运行器日志 |
| [cpu_tests.log](cpu_tests.log) | 最后一次 18 项 CPU 测试 |

[门槛、失败与协议差异](native_gate_report.md) · [下载及环境修复](retrieval_and_compatibility.md)

规范 200 次调用由 `native_stage1_export.py` 从 SQLite 导出的 CSV/JSONL 按每个方法×输入的最后终态 attempt 选取。原始 SQLite 及 15.84 GB 权重留在忽略目录 `.stage0-local/stage1`，可在服务器上续跑；入库的 JSONL 保留所有真实 Agent 中间轨迹和重试证据。

从实验目录复跑最后的 256-token 协议（先确保本地权重和图片仍在该固定路径，并按当时空闲 GPU 重新选择 UUID）：

```bash
stage=.stage0-local/stage1
gpu=GPU-5a0ba87d-2dc2-fed4-276c-8bb93dcec495
CUDA_VISIBLE_DEVICES="$gpu" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
PYTHONPATH="$PWD/$stage/LLaVA-c121f0432da27facab705978f83c4ada465e46fd" \
timeout -k 15s 21500s "$stage/native-venv/bin/python" -u stage1_smoke.py \
  --data-root "$stage/data" --model-root "$stage" \
  --official-source /tmp/mssbench-stage0-official \
  --output "$stage/native-stage1-256-acc027" --gpu-uuid "$gpu" \
  --through g2 --max-new-tokens 256
python native_stage1_export.py "$stage/native-stage1-256-acc027" native_stage1
```
