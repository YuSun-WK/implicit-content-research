# Stage 2｜可重跑命令与私有资产边界

从本目录运行。下列路径是本机实际使用的位置；`~/data/trace-assets/` 与 `.local/` 均不提交 Git。既有固定模型已校验时不重新下载。单卡 GPU 作业串行，单次命令以 `21540s` 限制在 5 小时 59 分钟以内。

本页保留 **2026-11-21 Stage 2 历史运行命令**。Stage 2.1 增加了正式训练前的 Manifest SHA 硬门禁；今后运行这些 `--phase formal` 命令还须加入 `--expected-caption-sha256` 和 `--defer-test`，值取已验收 Manifest 的实际 SHA。两种子完成后以 `--evaluate-best --peer-run-dir` 分别评估 Test。当前 `repaired_v2` 因 5 条 Caption 未通过长度检查，不能启动正式训练。

```bash
PY=/tmp/trace-s0-py310/bin/python
DATA="$HOME/data/trace-assets/multioff"
ASSETS="$HOME/data/trace-assets/stage2-models"
CAPTIONS="$DATA/trace_internvl_only"
RAM_SOURCE=/tmp/trace-s2-ram-source-v2
export CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
```

若迁移到新机器，先由 [固定资产下载器](stage2_fetch_assets.py) 逐组获取 `ram_plus`、`grounding_dino`、`internvl`、`openclip_roberta`、`bert_tokenizer`，核对其 `asset_manifest.json` 和 [脱敏资产清单](Stage2_Model_Asset_Manifest.json)。RAM 源码固定于 Git 提交 `7cb804a8609e9f4b1a50b7f31436d2df40bb9481`；作者 TRACE 源码固定于 `83ecb799f897fe275185e082ee9a669f7d04bfaa`。隔离解释器 `/tmp/trace-s0-py310/bin/python` 已安装 [清单](Stage2_Model_Asset_Manifest.json)中的版本。InternVL 生成命令须将隔离的 Transformers 4.49.0 / Tokenizers 0.21.4 覆盖层置于 `PYTHONPATH`。

按 10、50、740 依序执行；每一阶段先 RAM++、再 GroundingDINO、最后 InternVL。再次运行会验证原图 SHA 并跳过私有清单中成功的条目。

```bash
for LIMIT in 10 50 740; do
  for STAGE in tags grounding; do
    timeout -k 10s 21540s "$PY" stage2_caption.py \
      --stage "$STAGE" --limit "$LIMIT" --data-dir "$DATA" \
      --assets-dir "$ASSETS" --ram-source "$RAM_SOURCE" --output-dir "$CAPTIONS"
  done
  PYTHONPATH=/tmp/trace-s2-internvl-libs timeout -k 10s 21540s "$PY" stage2_caption.py \
    --stage caption --limit "$LIMIT" --max-new-tokens 256 \
    --data-dir "$DATA" --assets-dir "$ASSETS" \
    --ram-source "$RAM_SOURCE" --output-dir "$CAPTIONS"
done
"$PY" stage2_coverage.py --data-dir "$DATA" --manifest "$CAPTIONS/records.json" \
  --tokenizer-dir "$ASSETS/openclip_roberta/e22e1c12b0a1ba4af9fb6474626585351ea0da25" \
  --output Stage2_Caption_Coverage_Manifest.json
```

训练前核对覆盖确为 Train/Dev/Test 444/148/148。下面是本轮实际选择的短跑与正式训练参数；每个输出目录第一次运行时必须不存在，恢复时只对同一目录加 `--resume`。

```bash
timeout -k 10s 21540s "$PY" stage2_train.py \
  --data-dir "$DATA" --caption-manifest "$CAPTIONS/records.json" --assets-dir "$ASSETS" \
  --phase smoke --microbatch 2 --accumulation 1 --output-dir .local/s2-smoke-b2
timeout -k 10s 21540s "$PY" stage2_train.py \
  --data-dir "$DATA" --caption-manifest "$CAPTIONS/records.json" --assets-dir "$ASSETS" \
  --phase short --microbatch 32 --accumulation 4 --max-batches 100 \
  --stop-after 50 --output-dir .local/s2-short-b32
timeout -k 10s 21540s "$PY" stage2_train.py \
  --data-dir "$DATA" --caption-manifest "$CAPTIONS/records.json" --assets-dir "$ASSETS" \
  --phase short --microbatch 32 --accumulation 4 --max-batches 100 \
  --resume --output-dir .local/s2-short-b32
timeout -k 10s 21540s "$PY" stage2_train.py \
  --data-dir "$DATA" --caption-manifest "$CAPTIONS/records.json" --assets-dir "$ASSETS" \
  --phase formal --seed 42 --microbatch 32 --accumulation 4 \
  --output-dir .local/s2-formal-seed42
timeout -k 10s 21540s "$PY" stage2_train.py \
  --data-dir "$DATA" --caption-manifest "$CAPTIONS/records.json" --assets-dir "$ASSETS" \
  --phase formal --seed 121 --microbatch 32 --accumulation 4 \
  --output-dir .local/s2-formal-seed121
```

GPU 0 为本轮启动时可用的 RTX 4090；其他机器须先查空闲设备再设置 `CUDA_VISIBLE_DEVICES`。正式训练从固定预训练权重重新装配，短跑 Checkpoint 只作稳定性门禁。日志导出仅包含聚合数值、模型版本与哈希；私有 `records.json` 含 Caption，Checkpoint 含权重，均不可提交。
