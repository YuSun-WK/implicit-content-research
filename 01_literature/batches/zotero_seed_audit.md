# Zotero Seed 文献与历史重复条目审计

审计日期：2026-10-26。通过 Zotero 界面及只读数据库快照交叉核对；未修改 Zotero。**数据库 `collectionItems` 保留了回收站条目的 Collection 关系，查询当前馆藏必须排除 `deletedItems`。**此前把 89 条全当作在用条目是统计错误，本文件纠正该口径。

## 当前馆藏与回收站

- 当前根 Collection 与 `01seed_papers` 均为 **32 条在用文献记录、32 篇独立论文**。在用条目类型：28 `journalArticle`、2 `preprint`、2 `conferencePaper`。没有在用的重复文献条目。
- 数据库保留 89 条历史 Collection 关系：32 条当前在用，57 条已在 Zotero 回收站（删除日期为 2026-10-14 至 2026-10-24，早于本次审计）。57 条中有 48 条与当前 32 篇重复，另 9 条属于 4 篇仅在回收站中的独立研究作品。P033–P036 的编号保留作历史追踪，不计入当前阅读任务。
- 89 条历史 PDF 附件登记中，当前在用 32 条，均有实际文件且每页可提取文本；回收站父条目下有 57 条登记，其中 56 个文件仍存在、1 个缺失。合计 88 个存在文件、37 种不同字节指纹，不能将其称为 89 篇论文。
- 当前在用条目下有 7 条笔记、50 条 PDF 批注；回收站条目下另有 3 条笔记、40 条 PDF 批注。这些都不计入 PDF 附件数。

## Seed 当前在用清单

| Paper ID | Zotero Item Key | 题名 | DOI（馆藏） | PDF |
|---|---|---|---|---|
| P001 | `ZCDZZRNF` | ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection | 10.18653/v1/2022.acl-long.234 | 可逐页提取文本 |
| P002 | `B5AV8KVF` | Computational Approaches to the Detection of Lesser-Known Rhetorical Figures: A Systematic Survey and Research Challenges | 10.48550/arXiv.2406.16674 | 可逐页提取文本 |
| P003 | `HVRC2RT6` | Cultural Bias Matters: A Cross-Cultural Benchmark Dataset and Sentiment-Enriched Model for Understanding Multimodal Metaphors | 未填 | 可逐页提取文本 |
| P004 | `LQ666R8A` | Detection and Safeguarding of Chinese Toxic Content from Users and LLMs: A Survey | 10.21203/rs.3.rs-10778020/v1 | 可逐页提取文本 |
| P005 | `VDCGXL7U` | A Survey of Machine Learning Models and Datasets for the Multi-label Classification of Textual Hate Speech in English | 10.1145/3820778 | 可逐页提取文本 |
| P006 | `VQAAHEZ5` | Cross-lingual Offensive Language Detection: A Systematic Review of Dataset, Approach and Challenge | 10.1145/3801736 | 可逐页提取文本 |
| P007 | `CCIRF3ED` | Recent Advances in Online Hate Speech Moderation: Multimodality and the Role of Large Models | 10.18653/v1/2024.findings-emnlp.254 | 可逐页提取文本 |
| P008 | `SQT4MZS6` | Decoding Fake News and Hate Speech: A Survey of Explainable AI Techniques | 10.1145/3711123 | 可逐页提取文本 |
| P009 | `P3HCRLZM` | A Survey on Stereotype Detection in Natural Language Processing | 10.1145/3770754 | 可逐页提取文本 |
| P010 | `FJ8KC5VL` | Spoken in Jest, Detected in Earnest: A Systematic Review of Sarcasm Recognition—Multimodal Fusion, Challenges, and Future Prospects | 10.1109/TAFFC.2025.3612205 | 可逐页提取文本 |
| P011 | `IGDADHE7` | Pragmatics in the Era of Large Language Models: A Survey on Datasets, Evaluation, Opportunities and Challenges | 未填 | 可逐页提取文本 |
| P012 | `6999AQFP` | Computational Humor Modeling: A Survey on the State of the Art | 10.1145/3778357 | 可逐页提取文本 |
| P013 | `54553WUD` | Exploring Concreteness Through a Figurative Lens | 未填 | 可逐页提取文本 |
| P014 | `AWJLGTIC` | Ambiguity-aware Multi-level Incongruity Fusion Network for Multi-Modal Sarcasm Detection | 未填 | 可逐页提取文本 |
| P015 | `NRFM5Q9V` | LLMs in Sarcasm Detection? It’s elementary! (Or is it?) | 未填 | 可逐页提取文本 |
| P016 | `VGCGFHXT` | Easy as PIE? Identifying Multi-Word Expressions with LLMs | 未填 | 可逐页提取文本 |
| P017 | `PS2J8SBE` | In-Context Representation Hijacking | 未填 | 可逐页提取文本 |
| P018 | `S6RI8VD4` | Comparative Study of Multilingual Idioms and Similes in Large Language Models | 未填 | 可逐页提取文本 |
| P019 | `UPVJUK7E` | Understanding Figurative Meaning through Explainable Visual Entailment | 未填 | 可逐页提取文本 |
| P020 | `BNZW7ZET` | (RSA)2: A Rhetorical-Strategy-Aware Rational Speech Act Framework for Figurative Language Understanding | 未填 | 可逐页提取文本 |
| P021 | `4CKEC2S8` | Dying or Departing? Euphemism Detection for Death Discourse in Historical Texts | 未填 | 可逐页提取文本 |
| P022 | `M6CK6F6X` | Revisitinga Pain in the Neck: A Semantic Reasoning Benchmark for Language Models | 未填 | 可逐页提取文本 |
| P023 | `SYFQRQJA` | “Newspaper Eat” Means “Not Tasty”: A Taxonomy and Benchmark for Coded Language in Real-World Chinese Online Reviews | 未填 | 可逐页提取文本 |
| P024 | `KLF2SUWU` | Analyzing Offensive Language Dataset Insights from Training Dynamics and Human Agreement Level | 未填 | 可逐页提取文本 |
| P025 | `STHI3QUA` | HVGuard: Utilizing Multimodal Large Language Models for Hateful Video Detection | 未填 | 可逐页提取文本 |
| P026 | `YRSLRTDX` | Robust Adaptation of Large Multimodal Models for Retrieval Augmented Hateful Meme Detection | 未填 | 可逐页提取文本 |
| P027 | `3YXYW3UY` | EXPO-HM: LEARNING TOEXPLAIN-THEN-DETECT FORHATEFULMEMEDETECTION | 未填 | 可逐页提取文本 |
| P028 | `DG6KGASE` | ImpliHateVid: A Benchmark Dataset and Two-stage Contrastive Learning Framework for Implicit Hate Speech Detection in Videos | 未填 | 可逐页提取文本 |
| P029 | `UC7ZVITY` | RV-HATE: Reinforced Multi-Module Voting for Implicit Hate Speech Detection | 未填 | 可逐页提取文本 |
| P030 | `DQMRPCBL` | SMARTER: A Data-efficient Framework to Improve Toxicity Detection with Explanation via Self-augmenting Large Language Models | 未填 | 可逐页提取文本 |
| P031 | `PS3EI65S` | AmpleHate: Amplifying the Attention for Versatile Implicit Hate Detection | 未填 | 可逐页提取文本 |
| P032 | `Y8EAPG6Z` | Generalizable Implicit Hate Speech Detection Using Contrastive Learning | 未填 | 可逐页提取文本 |

## 回收站历史分组

以下 Item Key 是历史追踪信息，不代表当前 Collection 中还存在重复记录；既有 `zotero_mapping.csv` 保留每条 Key 及其当前/回收站状态。

| Paper ID | 当前在用 Key | 回收站 Key | 状态 |
|---|---|---|---|
| P001 | `ZCDZZRNF` | `M29WZENG` | 与当前馆藏重复，已在回收站 |
| P002 | `B5AV8KVF` | `XMDUI8IY`; `44SHKI82` | 与当前馆藏重复，已在回收站 |
| P003 | `HVRC2RT6` | `TGCSSWNW` | 与当前馆藏重复，已在回收站 |
| P004 | `LQ666R8A` | `HQW62KKI`; `3H3ESQBL`; `CDUJZIV7`; `8T5YS7UF` | 与当前馆藏重复，已在回收站 |
| P005 | `VDCGXL7U` | `W8RC4LX7`; `3RQKACAT` | 与当前馆藏重复，已在回收站 |
| P006 | `VQAAHEZ5` | `TSPYUCMF`; `49DIJ2XQ` | 与当前馆藏重复，已在回收站 |
| P007 | `CCIRF3ED` | `6M3GSRSK`; `FIFBUN3K` | 与当前馆藏重复，已在回收站 |
| P008 | `SQT4MZS6` | `QGNYJ8JV`; `A8738D3P` | 与当前馆藏重复，已在回收站 |
| P009 | `P3HCRLZM` | `6K87G2UJ`; `HTPFKVZV`; `VJCYGLIV`; `JEYUUSBY`; `ZDMEAWTE` | 与当前馆藏重复，已在回收站 |
| P010 | `FJ8KC5VL` | `DVG6EMFA`; `Y423GXPV` | 与当前馆藏重复，已在回收站 |
| P011 | `IGDADHE7` | `QCMZPQ3T`; `KIHWX52N` | 与当前馆藏重复，已在回收站 |
| P012 | `6999AQFP` | `CIIV9258`; `H93KD8U3` | 与当前馆藏重复，已在回收站 |
| P013 | `54553WUD` | `WFJLX7Y8`; `NLDYKRAU` | 与当前馆藏重复，已在回收站 |
| P014 | `AWJLGTIC` | `W6KWBAB2` | 与当前馆藏重复，已在回收站 |
| P015 | `NRFM5Q9V` | `RWPDI5JG` | 与当前馆藏重复，已在回收站 |
| P016 | `VGCGFHXT` | `VGUAAJ49` | 与当前馆藏重复，已在回收站 |
| P017 | `PS2J8SBE` | `V5GCZSET` | 与当前馆藏重复，已在回收站 |
| P018 | `S6RI8VD4` | `V5XT3W8A` | 与当前馆藏重复，已在回收站 |
| P019 | `UPVJUK7E` | `6IWB7ZHW` | 与当前馆藏重复，已在回收站 |
| P020 | `BNZW7ZET` | `GWAM3XL7` | 与当前馆藏重复，已在回收站 |
| P021 | `4CKEC2S8` | `SER45MBL` | 与当前馆藏重复，已在回收站 |
| P022 | `M6CK6F6X` | `SP9IZ7WW` | 与当前馆藏重复，已在回收站 |
| P023 | `SYFQRQJA` | `N3WT9W8T` | 与当前馆藏重复，已在回收站 |
| P024 | `KLF2SUWU` | `JQA5VD9K` | 与当前馆藏重复，已在回收站 |
| P025 | `STHI3QUA` | `YV2YS342` | 与当前馆藏重复，已在回收站 |
| P026 | `YRSLRTDX` | `9R2Z8PQ2` | 与当前馆藏重复，已在回收站 |
| P027 | `3YXYW3UY` | `KQS3EIUI` | 与当前馆藏重复，已在回收站 |
| P028 | `DG6KGASE` | `6YCPRT6B` | 与当前馆藏重复，已在回收站 |
| P029 | `UC7ZVITY` | `VQ8YFRPH` | 与当前馆藏重复，已在回收站 |
| P030 | `DQMRPCBL` | `CNPPAN8E` | 与当前馆藏重复，已在回收站 |
| P031 | `PS3EI65S` | `44JJIRLQ` | 与当前馆藏重复，已在回收站 |
| P032 | `Y8EAPG6Z` | `GLHZFRYH` | 与当前馆藏重复，已在回收站 |
| P033 | 无 | `IRSJBJEZ`; `D6BUXKDP` | 仅回收站历史作品 |
| P034 | 无 | `WCUKSY67`; `9I7DDMTU` | 仅回收站历史作品 |
| P035 | 无 | `2PU8MPJ4`; `5SAFEDCE`; `BE6ZILBY` | 仅回收站历史作品 |
| P036 | 无 | `KE4QTLKB`; `YGW7NCNH` | 仅回收站历史作品 |

## 不应直接清空回收站的原因

- 回收站中的 `HQW62KKI` 关联附件 `8J4X7BZI`；该 PDF 文件虽缺失，附件记录仍保有 **40 条独有批注**。当前在用的同篇论文条目 `LQ666R8A` 有另 47 条批注，不能把回收站那 40 条当作冗余。永久删除前须先安全迁移并核验。
- 回收站还有 4 篇当前馆藏没有的独立作品，不能把全部 57 条一概当作重复文件。
- Zotero 官方建议通过合并重复文献条目保留 Collection、标签和引用关系，而不是直接删除。当前在用的 32 条已无重复；如需永久清理回收站，须先排除独有批注与独立作品。
- P002 馆内 PDF 均为 2024 arXiv 预印本；2025 ACM 正式版另列 Source，未沿用预印本页码。刻板印象综述两种 PDF 字节不同、提取正文仅差一个换行，出版日期冲突待核验。
