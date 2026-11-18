# 当前研究审计

## 项目与证据

读取研究仓库 main 快照 `985901a5c4830ac1f46dcad4884fbeee7bb82102` 的项目目标、工作流、进展、P037–P041、P026/P027 和多模态安全综述相关材料，交叉读取 H1-K1 实验、H1-K2 审计、H1-K3 准备报告。前置聊天“论文精读总结分析”明确聚焦图文输入 S/B/U 分类，以及 VLSU 源域到目标二分类的迁移。实验位于同一仓库的独立分支，目录为 03_experiments。SIJA 是另一个编辑意图和编辑风险实验，现有技术试跑对本任务没有分类机制证据。仓库读取时显示 public。 [项目快照](https://github.com/YuSun-WK/implicit-content-research/tree/985901a5c4830ac1f46dcad4884fbeee7bb82102) · [P038 定稿](https://github.com/YuSun-WK/implicit-content-research/blob/985901a5c4830ac1f46dcad4884fbeee7bb82102/01_literature/cards/P038_VLSU.md)

| 证据 | 内容 | 可以支持的主张 |
|---|---|---|
| 项目已有实测 H1-K1 | ThinkingGuard-8B，36 对 TriggerBench Test，统一协议 180 条输出。Joint 51/72 正确，Unsafe F1 0.6441，成对全对 15/36 | 同协议下有错误，量化 8B 单模型小样本；原五步完整 36 对未执行 |
| 项目已有 H1-K2 独立日志核对 | TP19、TN32、FP4、FN17。11 个 image-only Unsafe→joint Safe 的条件变化中，助手非盲筛查 A0/B6/C5。全 36 对 A6/B12/C18 | image-only 图像风险与 joint 协助请求的后果风险混合。两个输出不同不足以定位表征衰减，筛查等级是探索判断 |
| 项目已有 H1-K3 | 两套盲审材料就绪，准备报告时真实人审 0 | 对正式机制主张仍无新增金标。复用作者数据可做常规分类，无需把重新盲审设成普遍前提 |
| 本轮 | 正式论文与附录、CSV、许可证、下载说明、132 个 URL 小样本；TriggerBench 全量清单 | 统计与可达性快照。没有新模型性能或图像语义真值 |

[H1-K1](https://github.com/YuSun-WK/implicit-content-research/blob/0a043abbf575d6b21f8d4095dbdfba7bad880465/03_experiments/h1_k0_triggerbench/H1_K1_FORMAL_EXPERIMENT_REVIEW.md) · [H1-K2](https://github.com/YuSun-WK/implicit-content-research/blob/e6d80b030d43918ca502091717e9334aaab5b561/03_experiments/h1_k2_research_audit/H1_K2_Executive_Decision.md) · [H1-K3](https://github.com/YuSun-WK/implicit-content-research/blob/experiments/h1-k3-review-prep-20261117/03_experiments/h1_k3_review_prep/H1_K3_Preparation_Report.md)

**本轮独立重算 TriggerBench 结构。** H1 固定版 pair_manifest 含 2,800 个同文的 Safe/Unsafe 配对。Train 有 3,864 边、5,795 节点、1,931 分量，Test 有 1,736 边、2,604 节点、868 分量，二者精确路径身份环秩均为 0。两侧图片路径总计 5,600、复用为 0。由同文配对得到的二类差分可控制该文本，但不能作为同时消除图和文主效应的闭环实验。原图内容身份或近重复仍未全量核验。 [H1 固定清单](https://github.com/YuSun-WK/implicit-content-research/blob/0a043abbf575d6b21f8d4095dbdfba7bad880465/03_experiments/h1_k0_triggerbench/data/manifests/pair_manifest.csv)

## VLSU 正式论文与附录

- **任务与标注**。正式版 ICLR 2026，44 页，§2–3 定义政策语义上的 Safe/Borderline/Unsafe。Borderline 常涉及讨论方式、语境与请求目的。数据是检索得到的真实图片与 Gemini/DSPy 生成文本、再经人审。生成目标、实际标注和模型输出是三个变量。附录 B.1/B.4 中图像由一位有经验作者判级，文本和联合由多位标注者评分，92.4% 三人、其余两人。总体 Krippendorff α=0.806、配对原始一致率 86.9%。Table 9 中 S-S-U 为 82.5%（126 个标注者配对比较），B-B-U 为 54.1%（231 个比较）。标签分歧应纳入解释范围。公开 CSV 无逐个标注者投票。
- **评测协议**。Table 1 为横向比较使用二类提示，Borderline 归至 Safe。Table 2、4 及附录 D/E 处理三分类、模型设置和提示。Figure 5 中 Qwen2.5-VL-32B 的 33.8% 是全部联合错例里的 Both Correct 占比。另报告 P(联合错误 | 两侧输出皆对)，两者分母不同。两侧等级预测正确说明等级判断成功，仍允许人物关系、动作目标、指代或决策阈值出错。
- **项目假设核对**。§4.2/Figure 4 支持作者所测模型的强单侧线索与弱组合组别之间有性能差。S-S-U 等模式可作为抽样代理，仅凭模式无法知道图文两边是否都必要。§5 的文本主导是作者对组别错误的解释，需以同标签任务和强文本基线核验。作者将部分错误归因为融合，输出统计无法单独确定内因。
- **结构化提示与拒答**。Table 2，GPT-4o 的 F1 45.8→54.4、Qwen2.5-VL 7B 42.3→51.4、32B 63.5→62.7。Table 3，Gemini-1.5 从 Harmless 到 Helpful 时 Borderline 拒答 62.4%→10.4%、Unsafe 拒答 90.8%→53.9%。这些是生成行为指标。附录 D.2 的帮助性判定提示属于 Judge，不能用来重建被测模型的完整 Helpful 指令。
- **发布口径**。§3/A.3 Table 7 的联合 S/B/U 计数为 2,186/3,312/2,689。Appendix F.2 明确仅有 test split。Figure 9 的 17 模式是论文版本，P038 的正式图复核记 S-S-U=37。Table 9 的配对比较数与 Figure 9 样本数口径有差异，成因未确认。附录 C/D/F 分别记录生成流程、提示与适用范围。论文正文也有类别层统计口径，不能与发布字段非空数混用。 [正式论文与附录](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)

## 固定发布快照实测

Apple 仓库 HEAD `cbe363a26d2129ff1b526c283af0a2b7aa3d9b28`，数据 Git blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`，本地 CSV SHA-256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`。严格 CSV 解析，全部 8,159 行九列齐全。

| 字段 | 本轮审计 |
|---|---|
| prompt, web_path, uuid | 均非空。8,159 UUID、8,157 原始 URL、7,638 prompt。NFKC+casefold+压缩空格后仍为 7,638；HTTP 875、HTTPS 7,284，2,944 主机名 |
| image_grade | S 4,182 / B 1,810 / U 2,026 / not_sure 141 |
| consensus_text_grade | S 4,328 / B 1,452 / U 2,379 |
| consensus_combined_grade | S 2,189 / B 3,310 / U 2,660 |
| image_category, text_category, combined_category | 三列空值分别为 4,319 / 4,360 / 2,211。联合类别空值含 S 2,149、B 36、U 26；类别字段是标签侧元数据 |
| 精确重复 | 2 个 URL 重复组共 4 行；217 个规范化文本重复组共 738 行，其中 6 组 text_grade 不一致 |

图像—文本—联合标签的全量实计数如下。问号表示 image_grade=not_sure，星号表示公开 CSV 中额外出现的两个标准三元组。

| 模式 | n | 模式 | n | 模式 | n |
|---|---:|---|---:|---|---:|
| S-S-S | 2166 | B-S-S* | 1 | U-S-B | 924 |
| S-S-B | 58 | B-S-B | 878 | U-S-U | 142 |
| S-S-U | 35 | B-S-U | 45 | U-B-B | 201 |
| S-B-S | 10 | B-B-B | 266 | U-B-U | 15 |
| S-B-B | 897 | B-B-U | 32 | U-U-U | 744 |
| S-B-U | 9 | B-U-U | 588 | ?-S-S | 12 |
| S-U-B* | 1 | ?-B-B | 21 | ?-S-B | 64 |
| S-U-U | 1006 | ?-B-U | 1 | ?-S-U | 3 |
| ?-U-U | 40 | | | | |

- **本轮新实测，图支持**。将 URL 原串与 NFKC/casefold/空白标准化后的全文作为二部节点，8159 个唯一边、15795 节点、7636 连通分量，最大分量 35 顶点，环秩 8159−15795+7636=0。按发布字段的精确身份无闭环。URL 异名同图、裁切图、OCR/模板、语义近邻仍需另查。近似聚类依据不足以将原行当成严格交叉配对。
- **本轮新实测，小规模旁证与近重复**。固定规范化文本及两个单侧等级、要求至少两个不同 URL 且联合标签不同，共 4 组 9 行。3 组 (S,S) 变化仅为 S/B，另 1 组为 (U,S)。这些是备选的复核候选，尚未做语义和原图配对验证。对不同规范化文本以正则词元组成连续三词集合，在两侧均 ≥8 个词时，Jaccard ≥0.8 查得 9 对、共 18 个文本。此数确认字面近重复存在，窄阈值不是模板泄漏上限，也未判断实际跨 split 污染。
- **本轮新实测，捷径参照**。8,018 个标准三元组上，“每个真实 (yI,yT) 组总猜其最大频数联合类”的同表经验上限为 7,670/8,018=95.66%，条件熵 0.2384 bit。取两侧最大等级的朴素规则 6,702/8,018=83.59%。前者用真实模态标签并在同表选择多数类，属于诊断参照。S-S-S 占 S-S-* 的 2,166/2,259，U-S-B 占 U-S-* 的 924/1,066。严格升级共 179 条。总体准确率容易被多数条件吸收。
- **本轮新实测，图片可达小样本**。北京时间 11-18，每个原始模式按 UUID 排序、固定 Python 随机种子 20261118、不放回取最多 6 条，按模式名排序依次抽样。Windows 单次 GET，代理/网络取决于当前机器环境，5 秒 socket 超时、6 MiB 上限，Pillow 实际解码。132 次中 108 成功，9 个 URLError，7 个 404，6 个 403，2 个超时。关键子组 S-S-U 5/6、S-S-B 5/6、U-S-B 6/6、U-S-U 4/6、B-B-U 4/6。成功样本无相同字节哈希。各模式抽样比例不同，108/132 描述这批样本，不估计总体成功率。图像是否与原文语义相符、完整近重复率与原图版权仍待核验。
- **版本差异与划分**。公开比论文少 28 行，联合分布有增有减，原因未确认。保留全部发布样本和论文 17 对齐子集的独立口径。141 张 uncertain 的联合标注仍有效，令图像辅助监督缺失；不映射为 B。两个单例仅附录计数，稀有组不强制三分。对监督复用只考虑独立的 VLSU-GroupSplit，无法沿用官方零样本名称。详细控漏见 [07](07_Experimental_Roadmap_and_Kill_Tests.md)。

[发布 CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28/data/VLSU.csv) · [下载说明](https://github.com/apple-aiml-research/ml-vlsu/tree/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28/utils)

## 许可与研究边界

发布 CSV 为 CC BY-NC-ND 4.0，§2(a)(1) 对许可范围内的非商业使用允许复制许可材料、制作和复制改编材料，公开分享改编材料受限。代码另为 Apple Sample Code License。图片 URL 指向第三方，CSV 许可不自动覆盖原图。内部非商业训练需同时核实图像来源与本机构政策。公开仅交付审计、取得许可的代码及本地划分脚本，数据副本、标注改版、图像、特征和检查点按各自权利与合同另行确认。CC 许可文字本身没有解决模型权重是否构成改编的具体判断。 [Apple 数据许可](https://github.com/apple-aiml-research/ml-vlsu/blob/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28/LICENSE_DATA) · [CC BY-NC-ND 4.0 法律文本](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en)
