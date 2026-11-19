# MSSBench Multi-Agent Stage 0

CPU 阶段交付已完成。**Smoke STOP**，详见 [Stage 0 Gate Report](stage0_gate_report.md)。此目录保留项目启动规范，并新增可复建的审计与 Mock 管线。官方仓库固定在 [sources.json](sources.json)，本地实现遵循论文角色信息流，所有量化、processor、输出存储和 Judge 的本地选择另行注明。

| 交付 | 状态 |
|---|---|
| [Source Code Audit](source_code_audit.md) · [Repair Log](repair_log.md) | PASS |
| [Data Audit](data_audit.md) · [输入 manifest](manifest.csv) · [Smoke 图片清单](smoke_images.csv) | PARTIAL |
| [Model Compatibility](model_compatibility.md) | PARTIAL |
| [Resource Budget](resource_budget.md) · [Experimental Matrix](execution_matrix.csv) | PASS |
| [Evaluation Protocol](eval_protocol.md) · [Run schema](run_log_schema.md) | PASS |
| [Mock Test Results](mock_test_results.md) · [日志](logs/) | PASS |
| [Stage 0 Gate Report](stage0_gate_report.md) | FAIL |

## CPU 复建命令

在本目录执行。使用 Python 3.10+。官方隔离导入探针需要 `tqdm`，本机默认环境已有。数据命令只在缺少本地锁定副本时获取单个 JSON 和文件树元数据。默认 Python 无 HF CLI，故使用固定 URL 和大小上限；脚本在读入前核对 SHA256。

```bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES=''
export PYTHONDONTWRITEBYTECODE=1
stage0_tmp=$(mktemp -d)
export MSSBENCH_OFFICIAL_SOURCE="$stage0_tmp/official"
git init -q "$MSSBENCH_OFFICIAL_SOURCE"
git -C "$MSSBENCH_OFFICIAL_SOURCE" fetch --depth 1 \
  https://github.com/UCSB-AI/MSSBench.git 1602193f49cb6925bfa3751be157d0bbf5439779
git -C "$MSSBENCH_OFFICIAL_SOURCE" checkout --detach FETCH_HEAD
revision=12396d24157427b671d97f23a2e370fca98fdf55
curl -fsSL --max-filesize 1000000 \
  "https://huggingface.co/datasets/kzhou35/mssbench/resolve/$revision/combined.json" \
  -o "$stage0_tmp/combined.json"
curl -fsSL --max-filesize 1000000 \
  "https://huggingface.co/api/datasets/kzhou35/mssbench/tree/$revision?recursive=true&expand=false" \
  -o "$stage0_tmp/hf-tree.json"
python inspect_source.py "$MSSBENCH_OFFICIAL_SOURCE"
python audit_data.py --dataset "$stage0_tmp/combined.json" --tree "$stage0_tmp/hf-tree.json"
MSSBENCH_MOCK_TRACE="$stage0_tmp/mock_trace.jsonl" python -m unittest -v test_stage0
python inspect_environment.py
```

`manifest.py`、`pipeline.py`、`evaluation.py`、`journal.py` 提供展开、单模型契约、评分分流和续跑骨架。正式模型接入仍需实现 VLM adapter。数据资产、权重和输出数据库应保存在应用配置指定的位置。
