# Stage 2.1–2.2｜审稿门禁决策

**总判定：`NO-GO / CAPTION_GATE_BLOCKED`。** 禁止在当前 `repaired_v2` Manifest 上开展正式 TRACE 训练。未合格的 5 条不能通过 tokenizer 自动截断或人工假定通过。

| Gate | 结果 | 证据 |
|---|---|---|
| 官方数据与固定模型 | PASS | MultiOFF 444/148/148、旧 Manifest SHA 和固定模型资产；[历史资产审核](Stage2_Model_Asset_Manifest.json) |
| 334 条筛选、406 条保留 | PASS | 真实 OpenCLIP Tokenizer 计数，406/406 原样保留；[修复审计](Stage2_1_Caption_Repair_Audit.json) |
| InternVL 改写与来源 | PARTIAL | 329/334 成功；5 条在各 3 次尝试后拒绝，细节按稳定 key 脱敏记录；[修复报告](Stage2_1_Caption_Repair_Report.md) |
| 740/740 ≤77 tokens | **FAIL** | 新版 5 条仍超限；Train 4、Dev 1；训练前置门禁确实返回异常 |
| 无分类标签词 | **未完全满足** | 本轮 4 条失败输出含标签词；旧版 406 条须保留项中 6 条含该类词，实际分类标签未提供给生成模型 |
| CPU 测试与代码 | PASS | 17 项通过；训练包装层在模型加载前检查全量长度与 Manifest SHA |
| 修复版 Smoke、双种子正式训练和 Test | **BLOCKED** | 每个种子 0 训练批、0 更新、无新 Checkpoint 或新指标 |

下一步应先**预先固定**解决 5 条失败 Caption 的新处理协议，并澄清 6 条旧合格 Caption 标签词与“逐字保留”要求的优先关系。随后使用新的私有版本目录重新验收 740/740，才可依照 [固定配置](Stage2_2_Repaired_Training_Config.yaml)启动两个种子的训练。不得用历史 Test 表现选择新 Prompt、学习率、阈值或模型。
