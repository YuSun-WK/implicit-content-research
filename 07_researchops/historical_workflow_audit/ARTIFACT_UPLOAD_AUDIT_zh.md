# GitHub 产物对账

统计对象为六个仓库内代表实验族：ASIMOV、EMBGuard、MSSBench、TRACE、VLSU、H1-K0。表中“已上传”只表示对应分支/PR 有文件，不等于其内容足以完整复现；“未发现”只表示检查范围内未见。外部 HumanShift/PA Kill Test 未纳入仓库上传分母。[E020,E022,E023,E024,E026,E027]

| 实验 | 远端 | 代码/配置 | 汇总及原始指标 | 预测/轨迹 | 日志 | 本地与远端差异 |
| --- | --- | --- | --- | --- | --- | --- |
| ASIMOV | PR #80，关闭未合并，3 文件 | 仅 recompute.py，模型运行代码未见 | scores.csv 820 行及 README | 评分可复算；原始生成输出未见 | worker 过程日志未上传 | 历史会话有日志路径；当前项目目录未找到 |
| EMBGuard | PR #81，关闭未合并，24 文件 | fetch/prepare/score/finish/replay 与 config | metrics.json、group_results.csv、两个 scores.jsonl 各 254 行 | 逐例评分已上传 | 独立 worker/pilot 过程日志未见 | 历史命令有日志路径；当前目录未找到 |
| MSSBench | PR #79，Draft，164 文件 | 脚本/config | results_256/512.csv | traces_256/512.jsonl | 多份 stage2/logs 已上传 | SQLite 与中间日志仍私有 |
| TRACE | repro/trace 分支，117 相关文件 | 包装层/配置/报告 | events、summary，精确重算一致 | 样本级预测未发现 | events 和下载/运行摘要已上传 | 私有 Caption、Checkpoint、权重合理未上传 |
| VLSU | repro/vlsu 分支，82 相关文件 | 有 | Stage2 摘要为 NOT RUN | 正式 Stage2 预测不适用 | 准备阶段记录 | 不能报告正式推理成绩 |
| H1-K0 | experiments/h1-k0 分支，168 相关文件 | 有 | 多 JSON/metrics | 12 JSONL | 31 日志 | 本地 h1-cf-killtest 还有 runs/模型快照；逐文件精确 SHA 未对账 |

[E020,E022,E023,E024,E025,E026,E027] PR #80 的分数复算不等于重跑模型；PR #81 的逐例评分可复核聚合，但原始模型推理过程缺日志。MSSBench 的完整轨迹与日志提供较强过程审计。TRACE 私有 events 与公开 events 的 SHA256 一致，运行 summary 与重算一致，但没有公开预测，不能独立重算 AUROC。Checkpoint 与原始数据、私有 Caption/模型权重因体积或许可保留本地合理；应在 manifest 记录哈希和路径角色，而非上传内容。[E020,E021,E022,E023,E026]

## 覆盖统计

下表按六个代表实验族计数，训练日志对纯推理项目按推理日志处理；缺失状态以当前已核查目录和远端分支为限。精确逐项状态见 [CSV](artifact_completeness_matrix.csv)。

| 产物类别 | 适用 | 已上传 | 仅服务器 | 未发现 | 无法确认 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 代码 | 6 | 6 | 0 | 0 | 0 |
| 配置 | 6 | 5 | 0 | 0 | 1 |
| 自然语言报告 | 6 | 6 | 0 | 0 | 0 |
| 程序汇总指标 | 5 | 4 | 0 | 0 | 1 |
| 原始逐 Run/Step 指标 | 5 | 4 | 0 | 0 | 1 |
| 样本级预测/评分/轨迹 | 5 | 3 | 0 | 1 | 1 |
| 过程日志 | 6 | 3 | 0 | 2 | 1 |
| 完整运行命令 | 6 | 3 | 0 | 0 | 3 |
| 精确运行版本/manifest | 6 | 2 | 0 | 0 | 4 |

“仅服务器”数为 0 仅指这些行所定义的公开产物类别，绝不表示私有 SQLite、Checkpoint、Caption 或 H1 模型快照已经上传。后者单列在矩阵 server_only 字段。原始逐例内容不上传时，GitHub 上的 Chat 审计能力有边界。[E019,E020,E023,E027]
