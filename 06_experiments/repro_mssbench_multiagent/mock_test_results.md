# Mock Test Results · PASS

`CUDA_VISIBLE_DEVICES=''` 下 7 个 CPU 测试通过。测试使用合成输入、脚本化输出和真实 Prompt 拼接，适配器每次测试共享同一 MockVLM 实例。完整测试输出及 20 条 Agent 轨迹可供复核。

| 检查 | 结果 |
|---|---|
| Chat Intent 与 Caption | 两个输入探针独立变化，Safety 同时收到解析活动、Caption 与对应图片。Intent 为 text-only，Caption 无 query。父调用为 1、2。 |
| Chat QA | `Yes`、`No`、`None`、含糊判断分别走 YES、NO、NO、ELSE。NO/ELSE 保留原评估内容，两类无效判断仍被标记。 |
| Embodied | 两侧各有独立的 first-person 图与输出探针，Locator 输出进入带同侧图片、指令的 Safety Reasoning。父调用为 1。 |
| Base/CoT/QC/IC | 单次调用契约核对。双任务方向相反的 Yes/No、重复字段、答案抽取和 0–3 分流通过。 |
| 错误和恢复 | 测试缺图、空/非法输入、路径越界和软链、缺失字段、上游格式无效的停止行为。SQLite 测试失败轨迹保留、重试、完成后跳过和单写者。 |

这些证据覆盖 CPU 角色连线、路由与持久化契约。真实模型的生成、格式遵循、图片处理及正确率需要后续运行验证。

[测试日志](logs/mock_tests.log) · [逐 Agent JSONL](logs/mock_trace.jsonl) · [测试代码](test_stage0.py)
