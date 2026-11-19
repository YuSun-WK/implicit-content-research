# ThinkingGuard Stage 1 执行报告

**Stage 1 总状态 PARTIAL。GPU 数据门槛 BLOCKED。** 固定版本 Test Manifest 覆盖 868 对、1,736 条，297 张图通过官方 LFS SHA256 和解码，其中 225 张为本轮取得。仍有 1,439 张图未通过数据门槛。

| 阶段 | 状态 | 结果 |
|---|---|---|
| H1 历史证据 | DONE | 已核对 K0、K1、K2、K3。219 个 Git blob 和本地 SHA256 前后匹配，工作分支与 K3 基准的历史树一致。 |
| 固定官方来源 | DONE | 论文 PDF、TeX、作者代码、HF 数据和模型已固定。ACM 补件 HTTP 403，内容 NOT_VERIFIED。 |
| CSV、配对与图片 | PARTIAL | 36 个 CSV 官方 Git blob 一致，868 对两侧标签和文本关系通过。297/1,736 张 Test 图已验证，完整图片门槛 BLOCKED。 |
| 本地模型 | DONE | 四分片 SHA256、750 个 tensor 的索引、尺寸及头部、固定 processor/config 均通过。118 个索引位置修复具备字节级追踪。 |
| A0 parser 与 CPU | DONE | 29 项测试通过。旧原文重放 4/4 结构完整、2/4 有唯一结论，另两条保持 AMBIGUOUS_TEMPLATE。 |
| GPU Smoke、独立解析验证及 Pilot | NOT_RUN | 数据门槛未通过。新预测 0。读到 GPU 库存状态，推理 P50/P90/P95、运行进程显存和整卡峰值均为 NOT_RUN。 |

## 数据与历史核查

| 类别 | CSV 对 | CSV 条 | 已验证图 | 可用完整对 | 缺图条数 |
|---|---:|---:|---:|---:|---:|
| ethical_violations | 97 | 194 | 114 | 35 | 80 |
| illegal_activities | 96 | 192 | 125 | 39 | 67 |
| misinformation | 95 | 190 | 10 | 4 | 180 |
| offensiveness | 95 | 190 | 8 | 4 | 182 |
| physical_harm | 81 | 162 | 8 | 4 | 154 |
| privacy | 100 | 200 | 8 | 4 | 192 |
| property_damage | 100 | 200 | 8 | 4 | 192 |
| religion_belief | 90 | 180 | 8 | 4 | 172 |
| violence | 114 | 228 | 8 | 4 | 220 |

来源覆盖全部 5,600 条 CSV 记录。Train/Test 的精确文本、规范化文本、实际 HF 路径与官方 LFS SHA256 交集均为 0。原 CSV 图路径字段跨 split 重复 1,556 个。全数据 442 对的 CSV index 与图片文件编号不同，297 条 Unsafe 的原类别注释与来源文件类别有差异。图像近重合、模板语义近重合和实际训练清单仍待核验。 [数据验证](artifacts/manifests/data_validation.json) · [泄漏审计](artifacts/manifests/leakage_audit.json)

历史 K0 初始与 recovery 均无正式模型预测。K1 unified 的 180 条原始预测含 72 条图文，重得 TP19/TN32/FP4/FN17、Accuracy 51/72、Unsafe F1 0.644068、PairAcc 15/36。K2 保留 PIVOT 裁决，K3 真实人审 0、待开展。旧五步验证有两条复述 [Safe]/[Unsafe]，另两条给出明确 Unsafe，正式五步 36 对仍为 NOT_RUN。审计最初在旧工作树生成了两个临时 Python 字节码文件，已移除并改为无写盘加载，随后复测旧受保护文件逐项一致。 [旧预测复算](artifacts/legacy_results_audit.json) · [前后 SHA 对照](artifacts/legacy_immutability.json)

## 执行与门槛

默认路由多次遇到 TLS 重置和超时，一批 48 张全部失败后停止。无代理、公共镜像及两个旧 H1 独立路由均未得到通过哈希的探测样本。有时限的续传只尝试缺项，保留已校验图片和缺失清单。 [传输计数](runs/cpu_preflight/transfer_and_gate_status.json) · [下载日志](runs/cpu_preflight/image_transfer_progress.log)

```bash
python -m pytest -q
python scripts/audit_local_evidence.py --legacy "$legacy" --artifacts artifacts --baseline .local/legacy_before.json --model "$model"
python scripts/build_test_manifest.py --csv-root "$csv_root" --image-root images --cache "$historical_images" --frozen-tree artifacts/dataset_source_tree.csv --download --workers 12 --attempt-log .local/image_retry_attempts.jsonl --output artifacts/manifests
python scripts/freeze_sample_queues.py artifacts/manifests/test_manifest.csv "$legacy" artifacts/sample_queues.json
CUDA_VISIBLE_DEVICES='' "$experiment_python" scripts/run_resumeable_inference.py --stage smoke --model "$model" --preflight-only
```

GPU 预检仅数据项为 false，退出码 2。CPU 查阅固定 processor，五个结束标记在作者解码设置下均保留。旧模型权重缓存已复用。实验 Python 3.10.19、Torch 2.9.1+cu128、Transformers 4.57.3、bitsandbytes 0.48.2、accelerate 1.12.0、CUDA 12.8。 [预检](runs/cpu_preflight/preflight.json) · [CPU 测试](runs/cpu_preflight/pytest.log) · [处理器数据](runs/cpu_preflight/processor_check.json) · [GPU 库存快照](runs/cpu_preflight/gpu_inventory.csv)

原始 A0 规则和队列已固定。完整图片通过后先执行六条 Smoke，再使用 36 条独立验证，至少 35 条须有唯一结论，独立人类复核为 NOT_RUN。Pilot 为九类近均衡的 100 对。每次作业墙钟预算 19,000 秒，分配器预算 18 GiB，进程显存上限 20 GiB，无法归属 PID 时中止。100→300→868 对均需先用新实测 P95 加安全余量规划单次输入数，并保留全部分母、配置和可恢复分片。本阶段未启动 300/868 对或训练。 [A0 配置](configs/author_five_step_nf4.yaml) · [冻结记录](artifacts/parser_freeze.json)
