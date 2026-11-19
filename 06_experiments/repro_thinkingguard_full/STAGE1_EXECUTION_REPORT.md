# ThinkingGuard Stage 1 执行记录

本提交记录 CPU 阶段的可复核检查点。下载队列在该检查点之后继续核验图片。

| 阶段 | 状态 | 实证 |
|---|---|---|
| H1 历史证据和隔离 | DONE | 在独立 worktree 工作。原 K3 树中 219 个 H1 文件的 blob 和本地 SHA256 复测一致。K1 unified 复得 TP19/TN32/FP4/FN17、Accuracy 51/72、PairAcc 15/36。K0/recovery 保留各自历史状态，K2 独立复算与 K3 真实人审待开展状态均保留。 |
| 论文、代码、HF 固定版本 | DONE | 论文 PDF、TeX、作者代码和两个公开 Hub 版本具备固定记录。ACM 补件 NOT_VERIFIED。 |
| Test Manifest | PARTIAL | 36 个 CSV 与固定 Git blob 一致，覆盖 868 对和 1,736 条。CPU 检查点有 225 张通过官方 LFS SHA256 和解码，另 1,511 条仍等待图片。 |
| 模型缓存 | DONE | 四分片 LFS SHA256、750 个 tensor、118 项索引重定位、固定 processor/config blob 验证通过。 |
| 五阶段解析与 CPU 测试 | DONE | 26 项 pytest 通过。旧验证重放提取 2/4，结构 4/4。两个无效例为 `[Safe]/[Unsafe]` 占位模板。新验证队列和 A0 规则已冻结。 |
| GPU Smoke、独立验证、Pilot | NOT_RUN | CPU 检查点尚无完整 Test 图像。新预测、GPU 样本、P50/P95 和进程显存峰均未产生。 |

## 复核位置

- [数据验证](artifacts/manifests/data_validation.json) 含九类样本数、CSV SHA、可用图片和缺失名单。[泄漏审计](artifacts/manifests/leakage_audit.json) 含官方 LFS 参考范围。Train/Test 精确和规范文本交集均为 0，实际 HF 路径和官方 LFS SHA256 交集均为 0。原 CSV 图片字段的路径跨 split 重复 1,556 个，已保留原值。442 对的 CSV index 与图片编号不同。
- [来源快照](artifacts/source_snapshot.json)、[旧文件哈希复测](artifacts/legacy_immutability.json)、[旧预测复算](artifacts/legacy_results_audit.json)、[模型缓存](artifacts/model_cache_audit.json)。
- [CPU 测试](runs/cpu_preflight/pytest.log)、[preflight](runs/cpu_preflight/preflight.json)、[GPU 空闲状态快照](runs/cpu_preflight/gpu_inventory.csv)。GPU 空闲快照的整卡显存与实验进程显存使用属于不同量。

## 命令与门槛

```bash
python -m pytest -q
python scripts/audit_local_evidence.py --legacy "$legacy" --artifacts artifacts --baseline .local/legacy_before.json --model "$model"
python scripts/build_test_manifest.py --csv-root "$csv_root" --image-root images --cache "$historical_images" --frozen-tree .local/frozen_tree.json --historical-checksums .local/historical_image_checksums.json --output artifacts/manifests
python scripts/freeze_sample_queues.py artifacts/manifests/test_manifest.csv "$legacy" artifacts/sample_queues.json
CUDA_VISIBLE_DEVICES='' "$experiment_python" scripts/run_resumeable_inference.py --stage smoke --model "$model" --preflight-only
```

下载命令在 manifest 命令上增加 `--download --workers 12`。下载限定固定版本的 Test 文件，旧可用图和已通过 LFS 哈希的缓存复用。GPU 配置固定到 [A0 NF4](configs/author_five_step_nf4.yaml)，6 条 Smoke 后进行新的 36 条解析验证，随后才评估 Pilot 门槛。每个 GPU 作业以 19,000 秒预留退出时间，PyTorch 分配器 18 GiB，进程峰上限 20 GiB，运行 PID 无法归属时中止。后续 300/868 对需要真实 P95、每批加载开销、可恢复分片计划及单卡预算；本阶段未启动这些任务或训练。
