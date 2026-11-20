# ThinkingGuard Stage 1 恢复执行报告

正式 A0 Smoke 和独立解析验证共生成 **42 条 GPU 预测**。冻结解析器在独立验证集上提取 **20/36（55.56%）** 个唯一判定，未达到 **35/36** 门槛。Pilot 的 200 张图已全部核验，推理为 `NOT_RUN`。Stage 1 恢复总体为 `PARTIAL`。

| 阶段 | 状态 | 结果 |
|---|---|---|
| 分阶段数据门槛、GPU PID、时间戳 Run ID | DONE | 36 项 CPU 测试通过。Smoke、Validation、Pilot 只检查各自冻结队列的同对结构和官方 SHA256。所有 1,736 张齐全才通过 Full Test 预检。 |
| 优先图片恢复 | DONE | Smoke 6/6、Validation 36/36、Pilot 200/200。包括 curl 低并发有界退避、Range 续传和现有 HF Hub 0.36.0 补齐 Pilot 最后 9 张。 |
| 全 Test 图片 | PARTIAL | Manifest 为 868 对、1,736 条。此前 297 张就绪，现为 751 张，本轮增加 454 张，剩余 985 张。缺项中 91 张有传输失败记录，894 张当前状态为 MISSING。 |
| 正式 A0 Smoke | DONE | 6/6 生成，4/6 唯一判定，6/6 五步完整。两条 AMBIGUOUS_TEMPLATE。 |
| 正式 A0 独立验证 | DONE | 36/36 生成，20/36 唯一判定，35/36 五步完整。11 条 AMBIGUOUS_TEMPLATE，5 条 EXTRA_TEXT，0 条到达 1,024 token 上限。 |
| A0 解析验收 | BLOCKED | FAILED_PARSE_GATE。两位独立人类评审为 NOT_RUN。匿名原文助手转录已归档。 |
| 100 对 Pilot | NOT_RUN | 200 条数据就绪，解析门槛未通过。 |
| 诊断 Smoke、300 对、868 对推理和训练 | NOT_RUN | 本轮已获得正式 Smoke 证据。 |

## 指标与实测资源

这些分类指标描述对应的 Smoke 或独立验证样本。严格分母包含所有 INVALID，有效分母仅含可提取判定。PairAcc 的有效分母仅纳入两侧都有判定的 pair。

| 阶段 | Strict Accuracy / Unsafe F1 / PairAcc | Valid-only Accuracy / Unsafe F1 / PairAcc |
|---|---|---|
| Smoke | 50.00% / 0.6667 / 33.33% | 75.00% / 0.8000 / 50.00% |
| 独立验证 | 47.22% / 0.7647 / 11.11% | 85.00% / 0.8966 / 66.67% |

| 阶段 | 生成累计 | 作业计时 | 全样本 P50 / P95 | 进程 / 整卡采样峰值 | PyTorch allocated / reserved 峰值 |
|---|---:|---:|---:|---:|---:|
| Smoke | 378.83 s | 408.78 s | 61.88 / 72.06 s | 8,330 / 8,339 MiB | 7,768 / 7,908 MiB |
| 独立验证 | 2,215.36 s | 2,246.11 s | 60.10 / 71.51 s | 8,330 / 8,339 MiB | 7,768 / 7,908 MiB |

独立验证里用于后续预算的 5 条典型与 5 条最大输入子集 P50/P95 为 60.10/81.39 s。两次均使用同一张起始空闲的 RTX 4090 D。Smoke 容器 PID 653177 对应宿主 PID 1494226，验证容器 PID 674574 对应宿主 PID 1572545，两次 64 MiB 探针均记录 348→412→348 MiB。共归档 1,863 个资源采样，无缺失 PID 或监控终止。作业完成后 GPU 回到 3 MiB、0% 利用率，进程列表为空。 [Smoke 原始预测](runs/smoke_20261119_recovery/predictions.jsonl) · [验证原始预测](runs/validation_20261119_recovery/predictions.jsonl) · [资源、预测和日志 SHA256](runs/recovery_cpu/final_gate_status.json)

## 解析验收与 A1 提案

匿名最终段转录与冻结解析器一致 32/36。四条有明确 Unsafe 语义判定，但紧邻的多个类别括号或类别后的解释超过冻结末段格式，仍计 INVALID。一条原样复述双标签模板后继续输出提示词说明，解析器记为 EXTRA_TEXT。解析源码、提示词、模型设置、冻结文件与样本名单哈希逐字节不变。 [匿名转录](runs/validation_20261119_recovery/raw_only_transcription.json) · [差异清单](runs/validation_20261119_recovery/transcription_comparison.json) · [冻结哈希](runs/recovery_cpu/source_lineage.json)

如单独注册 A1，可保留五步任务和原安全标准，明确要求 Overall 末尾输出唯一一行 Final verdict，取值 Safe 或 Unsafe，类别保留在单独字段。事前冻结 A1 prompt、parser 和未使用的九类验证集，继续采用至少 35/36 的提取门槛，并记录结构、语义转录、类别格式、INVALID 及预算。A1 提案未执行。

## 可复核执行记录

- CPU 修复检查点为 `28de1b85104eb33f6513d3b891b2818ffb2e4a0e`，正式 Smoke 归档与查询修复检查点为 `36e71466f77e338b53392c9e81c03df43980ec46`。第一次验证启动遇到前序查询变量遮蔽，在 CUDA 加载前退出。修复仅改前序查询，对已完成的 Smoke 按原摘要及新旧 runner SHA 精确继承。启动日志保留进程实际读取的本地 Git SHA 和文件哈希。 [兼容记录](artifacts/recovery_runner_compatibility.json) · [首次退出日志](runs/validation_20261119_recovery/launcher_initial_error.log)
- A0 采用作者原样提示词、固定 NF4/BF16 compute、batch 1、greedy、1,024 token。Python 3.10.19、Torch 2.9.1+cu128、Transformers 4.57.3、bitsandbytes 0.48.2、accelerate 1.12.0、CUDA 12.8、驱动 580.82.09。每个作业内部上限 19,000 秒，外部 19,100 秒加 10 秒终止宽限。分配器上限 18 GiB，监控进程和整卡安全上界为 20 GiB。 [运行配置](configs/author_five_step_nf4.yaml)
- 所有冻结队列顺序、候选侧别和官方 SHA256 可复算。全局其余缺图尝试了两个有界窗口，保留已核验缓存、失败和未尝试状态。219 个旧 H1 文件的 Git blob 和本地 SHA256 复查一致。 [优先队列](artifacts/recovery_priority_queue_manifest.csv) · [全数据核验](artifacts/manifests/data_validation.json) · [历史保护](artifacts/recovery_legacy_immutability.json)

```bash
python -m pytest -q
python scripts/build_test_manifest.py --csv-root "$csv_root" --cache "$historical_images" \
  --image-root images --frozen-tree artifacts/dataset_source_tree.csv \
  --download --workers 4 --priority-queues artifacts/sample_queues.json \
  --through-stage validation --download-seconds 275 --output "$output"
HF_HUB_DISABLE_XET=1 HF_HUB_DOWNLOAD_TIMEOUT=15 timeout --kill-after=5s 120s \
  "$experiment_python" -u scripts/fetch_priority_hf_cache.py "$manifest" \
  --stage pilot --cache .local/hf_recovery
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 19100s "$experiment_python" -u \
  scripts/run_resumeable_inference.py --stage validation --model "$model" \
  --gpu-uuid GPU-45decdd6-682b-4cd9-2bc3-6769eee7a81f --run-id validation_20261119_recovery
python scripts/evaluate_pairwise.py runs/validation_20261119_recovery/predictions.jsonl \
  runs/validation_20261119_recovery/metrics_descriptive.json --stage validation
```
