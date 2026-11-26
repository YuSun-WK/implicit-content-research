# GitHub 产物审计：已核查样本

| PR | 状态 | 代码 | 配置与版本 | 原始评分/预测或轨迹 | 汇总指标 | 过程日志 | 本地未上传 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [#80 ASIMOV](https://github.com/YuSun-WK/implicit-content-research/pull/80) | 关闭、未合并 | `recompute.py` | README 固定数据与模型 revision | `scores.csv` 820 行脱敏评分 | README 表格 | PR 三文件中未发现原始推理日志 | 无法确认 |
| [#81 EMBGuard](https://github.com/YuSun-WK/implicit-content-research/pull/81) | 关闭、未合并 | fetch/prepare/score/finish/replay | config/settings 和 revision | 两模型 `scores.jsonl` 各 254 条 | `metrics.json`、group results、报告 | PR 24 文件中未发现独立过程日志；`failures.csv` 为失败记录 | 无法确认 |
| [#79 MSSBench](https://github.com/YuSun-WK/implicit-content-research/pull/79) | 开放 Draft | runner、export、verify、shell 脚本 | manifest、环境、模型 revision | 256-token 结果、1,039 条轨迹；512-token 对照 | gate、metrics、cost | stage2/logs/ 下多份真实日志 | README 说明本地 SQLite journals 与图像未提交；当前服务器状态待核验 |

“未发现”仅针对对应 PR 的**变更文件列表**，不是仓库所有分支的绝对缺失结论。原始模型输出与样本内容可能涉及数据许可，不能一概要求上传。#80 的评分和脚本可复算表格，但缺少从模型输入到分数的完整运行证据。#81 有逐例分数，便于核对指标；无服务器日志不能确认实际启动机制。#79 明确区分训练（不适用）与推理日志。

**初步观察：** 上传范围由项目而异，不能推断“每次都上传/从不上传”某类文件；全量统计需要盘点其他实验 PR、main 和服务器本地。