# SIJA 防御独立复现可行性与研究条件审计

日期2026-11-16；结论 **CONDITIONAL GO**，范围限低成本Guard-only可证伪验证。SIJA为2026 arXiv预印本、ICLR2027 under review，不是已录用CCF-A论文。公开证据能支持提示式适配实现，不能支持严格重现作者结果。

## 项目状态

读取00_project规范、papers.csv/sources.csv及主目录；main固定`985901a5c4830ac1f46dcad4884fbeee7bb82102`。PR [#73](https://github.com/YuSun-WK/implicit-content-research/pull/73)实测open、merged=false；head `e37ea2a9774b3f5fb669063a0d12fd00dc60cf77`，阅读卡从该分支只读获取，main无P042。未重建编号、未覆盖卡片或索引。独立分支`audit/sija-defense-feasibility-20261116`从main建立。遵循data_schema的`06_experiments/`，因此不采用建议的04_experiments目录；已有研究不受覆盖。

## 官方代码公开状态

[官方仓库](https://github.com/yexianmin/SIJA)实际git clone及ls-tree核实，仅README.md。默认main、最新commit `29231d7c0c5d6fad556b4f933aff353ac9bab763`，2026-10-20T17:44:40+08:00；ls-remote仅main无tag，官方Releases接口返回空列表。GitHub原始API部分限流，使用git传输与连接器交叉核实。不是仅看README得出的结论。

| 组件 | 是否公开 | 文件位置 | 足以复现 | 缺失 | 证据 |
|---|---|---|---|---|---|
| README | 是 | README.md | 否 | 仅介绍与将发布声明 | [固定树](https://github.com/yexianmin/SIJA/tree/29231d7c0c5d6fad556b4f933aff353ac9bab763) |
| 防御代码/模型接口 | 否 | 无 | 否 | Guard、推理、连接实现 | 同上 |
| requirements/environment | 否 | 无 | 否 | 依赖锁定 | 同上 |
| 数据处理/评估/Judge | 否 | 无 | 否 | 拼Cue、评分脚本与日志 | 同上 |
| 配置/Release/其它公开branch | 未发现 | 仅main，release空 | 否 | 完整配置 | [releases](https://github.com/yexianmin/SIJA/releases) |

## 数据、方法和资源

详见[数据审计](SI2ESBench_Data_Audit.md)、[缺口矩阵](SIJA_Reproduction_Gap_Matrix.md)、[环境计划](SIJA_Environment_and_Model_Plan.md)。元数据确为766条；已合成Cue可按id结构关联，但独立图标和规格图路径不完整，不能称B.3格式忠实完整。没有下载敏感图片，无内容级质量承诺。

核查[原文](https://arxiv.org/html/2610.23909v1) §3.2/§5.4/C.1/C.3/C.4/C.5：Guard在生成前恢复r/a/s，推断结果并YES/NO门控；Victim执行编辑；Judge评价输出。Guard模型 **Not specified in paper**。无需额外Judge即可做Guard-only；C.4的Gemma-4-31B-it确定用于结果判分，不能补全Guard身份。原prompt实现见scripts，新增解析和消息角色均明确为适配选择。

93.1%为作者危险请求拒绝率，不是正常准确率或HRR；另一Qwen-Image-Edit-2511-Safe报告ASR6.92%、HRR2.35%，不跨实验合并。没有运行编辑器就不能报告ASR/HRR/EV/HS。论文未报告误拒、三元组准确率或反事实一致性，不等于这三项已存在缺陷。

资源具备硬件候选条件，但本地唯一可见15G缓存未确认可直接加载；4B官方权重未下载。选择不运行GPU Smoke，避免以不完整或已安全训练模型混淆基础基线。环境未修改，无依赖安装。

## 公平比较与研究判断

[Kill Tests](SIJA_Research_Gap_Kill_Tests.md)规定同VLM三prompt、标签隔离、异常独立计数、匹配良性输入和停止条件。现有SI2ESBench不足以独自评价误拒。MagicBrush可支持小规模普通编辑政策诊断，但多图Cue转换是尚未解决的条件。SafeGuard-VL、UVR等已有更直接安全竞争机制；不能把原论文已有的意图重建重新包装为创新。

本轮CPU Smoke只测试目录关联、消息白名单和解析边界，没有VLM预测。结构核查日志不计正式766模型评价。未进行训练、生成、攻击、付费API或全包下载。

最终十项决策与必须解决的阻碍见[Verdict](SIJA_Feasibility_Verdict.md)。先解决小样本语义映射、基础模型资源实测与良性输入形式匹配；若这些条件无法满足，终止方法开发投入。
