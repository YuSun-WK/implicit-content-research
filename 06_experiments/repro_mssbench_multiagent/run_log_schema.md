# Run log and resume schema · PASS（CPU）

由调用端用固定 JSON 和 manifest 重建原文及图片路径，验证文本 SHA256，用 `local_image` 限制在数据根，解码后记录 actual SHA256 并与可用的 HF LFS SHA 核对。运行输出保存于 SQLite。留档 `sources.json`、本地提交 SHA、运行环境、实际输入 manifest、图像处理和模型配置。对真实输出另导出 JSONL 供审阅。

| 位置 | 字段与约定 |
|---|---|
| `attempts` | `id`、`run_key`、`config` JSON、`status`。身份字段为 dataset_revision、task、pair_id、gold_label、text_sha256、image_sha256、method、model_id、model_revision、adapter_revision、prompt_version、processor、quantization、decoding、seed。真实适配器可在 config 保留原图相对路径、像素尺寸、配置及权重清单哈希。 |
| `calls` | `attempt_id` + `call_id` 唯一定位；`trace` 含 `parent_ids`、`role`、送入适配器的 `prompt`、可选最终渲染 `rendered_prompt`、`image_attached`、`route`、`raw_answer`、`parsed` 和 `error`/`error_detail`。有图的调用从父 attempt 引用已经核对的实际 image SHA。 |
| 调用测量 | `elapsed_ms` 为适配器调用和解析的 CPU 单调时钟时长。input/output token、峰值 allocated/reserved 和 NVML used 均可空。Mock 中未知测量保留 null。真实适配器另记 token 计数方法、峰值采样窗口和 GPU 设备标识。 |
| 评测产物 | 用 attempt_id + call_id 加上 Judge 配置/版本或分类解析版本连接。输入分支写预测和 invalid；行为分支写 0–3/Unknown、原始 Judge 输出和可选人工核验。 |

幂等键从上表身份字段的排序 JSON 计算 SHA256，图像和文本哈希会在启动时核查。仅跳过 `complete`。每个 Agent 轨迹独立提交；进程中断后上次 `running` 标记 `interrupted`，失败或无效输出开启新尝试并从头重放单个输入。保留旧尝试和错误；可为重试上限另做调用层配额。一次只持有一个写者，SQLite 的唯一索引阻止同键重复完成。后续批量按输入切块，沿用原片段的设置和语义键。

[实现](journal.py) · [CPU 续跑测试](test_stage0.py)
