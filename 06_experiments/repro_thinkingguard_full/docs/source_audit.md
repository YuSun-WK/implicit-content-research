# 来源审计

GitHub 工作分支起点为 `231cab852d3f99b7428844c036de358002a5e2a7`。其祖先包含 K3 的 `4eb98bee31a6182bcf8e1ee724679460da008686`，两提交之间的 `03_experiments/` 树一致。核验时间、URL、完整 HF 文件清单和字节哈希见 [source_snapshot.json](../artifacts/source_snapshot.json)。

| 资产 | 固定版本 | 证据 |
|---|---|---|
| 作者代码 | `8c9426ea1025ffa69034e9f5ce07647bd3e72dc4` | 固定树仅列 README、示意图和推理示例。分别取得 main 和固定版本的 `inference.py`，字节完全一致。 |
| TriggerBench | `3ac26e778db94a282711f463f22ba6db99643bee` | 公开、无需 gated 访问。API HEAD 与 H1 版一致，列出 5,637 个文件含 36 个 CSV，仓库树中无 README 数据卡。 |
| ThinkingGuard-8B | `76892f9768ce828268265171f4bbc5dfb75eafc3` | 公开、无需 gated 访问。API HEAD 与 H1 版一致，14 个文件的 blob、大小和 LFS 信息与历史元数据逐项一致。模型卡提供基座与五阶段示例。 |
| 论文 | arXiv:2609.36562v1 | 取得 9 页 PDF 和 TeX 包，分别记录 SHA256。ACM 相关 DOI 为 `10.1145/3767308.3835707`。 |
| 正式补充材料 | NOT_VERIFIED | ACM supplementary 入口返回 HTTP 403，arXiv PDF 和 TeX 包未包含独立补件。 |

作者论文 §4 第 4–6 页描述五阶段归因、过程奖励、搜索回传及轨迹和关键步两类偏好监督。§5.1 第 6 页报告 Qwen3-VL-8B-Instruct、TriggerBench-Train、4×A100-80GB 约 90 分钟、LoRA rank/alpha 8/16、学习率 3e-5、批量 32、DPO β=0.1、全轨迹和关键步 2:1。公开仓库固定树中未发现训练器、搜索器、奖励实现或作者评测解析器。奖励提示词、剪枝阈值和具体评测规则的补充证据仍为 NOT_VERIFIED。 [论文正文](https://arxiv.org/html/2609.36562v1) · [作者代码树](https://github.com/FroggyChen/ThinkingGuard/tree/8c9426ea1025ffa69034e9f5ce07647bd3e72dc4)

- Table 1（第 7 页）的 TriggerBench 九类 Unsafe F1/Recall 等权平均为 0.764/0.866。九类分别为 PH .740/.951、IA .781/.875、PRI .697/.700、PD .757/.980、EV .766/.876、RB .711/.767、OFF .720/.705、MIS .881/.947、VIO .821/.982。 [Table 1](https://arxiv.org/html/2609.36562v1#S5.T1)
- Table 2（第 7 页）报告 MSSBench Accuracy .718、USB .927、MMSafetyBench .924、JailbreakV-28K-mini .914，以及作者环境下 3.5 秒和 352 输出 token。 [Table 2](https://arxiv.org/html/2609.36562v1#S5.T2)
- Table 3（第 8 页）按 benchmark 组汇总完整方法与四种消融。Implicit Hazards 的 Full 为 Acc .784、F1-Unsafe .810、Recall .749。 [Table 3](https://arxiv.org/html/2609.36562v1#S5.T3)

Hub 自动 ImageFolder 预览的 11,200 行是独立表示，本轮按作者论文 split 和原始 36 个 CSV 建立配对 manifest。两种 HF HEAD 都与历史版一致，因而无需跨 revision 差异表。归档 CSV 仍逐文件与固定树 Git blob 比对。 [数据集卡页面](https://huggingface.co/datasets/Sandy124/TriggerBench) · [模型卡](https://huggingface.co/Sandy124/ThinkingGuard-8B)
