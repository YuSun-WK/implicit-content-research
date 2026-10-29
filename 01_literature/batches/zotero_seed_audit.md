# Zotero Seed 与重复记录清理审计

更新：2026-10-27。数据取自 Zotero 本机界面、只读数据库快照及 PDF 文件核验。

## 数量与清理范围

- 初始历史 `collectionItems` 有 89 条文献关系，包含 32 条当时在用记录和 57 条当时已在回收站的历史记录；它们不是 89 篇独立论文，也不是 89 份当前可访问的 PDF。
- 57 条历史回收站文献中，48 条与原有 32 篇重复，9 条属于四篇当时缺席的独立作品。四篇各恢复一条主记录后，其余共 53 条重复文献记录被永久清理。
- 清理前回收站的 55 个对象包括 53 条文献记录及 2 个无批注的附件。清理后回收站为 0，根 Collection 有 36 篇独立论文，`01seed_papers` 有 32 篇。
- 当前 36 篇均有 PDF，共 38 个 PDF 附件；P004 与 P009 各保留两份。PDF 文件均存在，可逐页提取文本。已分析 7 篇，待分析或暂缓定稿 29 篇。

## 当前在用文献

| Paper ID | 范围 | Zotero Item Key | 题名 | DOI（馆藏） | PDF 附件 |
|---|---|---|---|---|---|
| P001 | Seed | `ZCDZZRNF` | ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection | 10.18653/v1/2022.acl-long.234 | `5MZGYWHV` |
| P002 | Seed | `B5AV8KVF` | Computational Approaches to the Detection of Lesser-Known Rhetorical Figures: A Systematic Survey and Research Challenges | 10.48550/arXiv.2406.16674 | `8ZDSA4ZT` |
| P003 | Seed | `HVRC2RT6` | Cultural Bias Matters: A Cross-Cultural Benchmark Dataset and Sentiment-Enriched Model for Understanding Multimodal Metaphors | 10.18653/v1/2025.acl-long.1275 | `3EWZQ7PB` |
| P004 | Seed | `LQ666R8A` | Detection and Safeguarding of Chinese Toxic Content from Users and LLMs: A Survey | 10.21203/rs.3.rs-10778020/v1 | `H89242KM; 8J4X7BZI` |
| P005 | Seed | `VDCGXL7U` | A Survey of Machine Learning Models and Datasets for the Multi-label Classification of Textual Hate Speech in English | 10.1145/3820778 | `VMKMBUQX` |
| P006 | Seed | `VQAAHEZ5` | Cross-lingual Offensive Language Detection: A Systematic Review of Dataset, Approach and Challenge | 10.1145/3801736 | `HGFRRKCZ` |
| P007 | Seed | `CCIRF3ED` | Recent Advances in Online Hate Speech Moderation: Multimodality and the Role of Large Models | 10.18653/v1/2024.findings-emnlp.254 | `26L8QB7W` |
| P008 | Seed | `SQT4MZS6` | Decoding Fake News and Hate Speech: A Survey of Explainable AI Techniques | 10.1145/3711123 | `Y8IS3H93` |
| P009 | Seed | `P3HCRLZM` | A Survey on Stereotype Detection in Natural Language Processing | 10.1145/3770754 | `I73WUKL3; R78ASLE5` |
| P010 | Seed | `FJ8KC5VL` | Spoken in Jest, Detected in Earnest: A Systematic Review of Sarcasm Recognition—Multimodal Fusion, Challenges, and Future Prospects | 10.1109/TAFFC.2025.3612205 | `ZQJ773VJ` |
| P011 | Seed | `IGDADHE7` | Pragmatics in the Era of Large Language Models: A Survey on Datasets, Evaluation, Opportunities and Challenges | 10.18653/v1/2025.acl-long.425 | `W8P65748` |
| P012 | Seed | `6999AQFP` | Computational Humor Modeling: A Survey on the State of the Art | 10.1145/3778357 | `K6PIZKGD` |
| P013 | Seed | `54553WUD` | Exploring Concreteness Through a Figurative Lens | 未填 | `FMSX2LCE` |
| P014 | Seed | `AWJLGTIC` | Ambiguity-aware Multi-level Incongruity Fusion Network for Multi-Modal Sarcasm Detection | 未填 | `V8XT63LV` |
| P015 | Seed | `NRFM5Q9V` | LLMs in Sarcasm Detection? It’s elementary! (Or is it?) | 未填 | `32J5I3HQ` |
| P016 | Seed | `VGCGFHXT` | Easy as PIE? Identifying Multi-Word Expressions with LLMs | 未填 | `UNXSRVF4` |
| P017 | Seed | `PS2J8SBE` | In-Context Representation Hijacking | 未填 | `5F5PAUTP` |
| P018 | Seed | `S6RI8VD4` | Comparative Study of Multilingual Idioms and Similes in Large Language Models | 未填 | `U8LYVVP5` |
| P019 | Seed | `UPVJUK7E` | Understanding Figurative Meaning through Explainable Visual Entailment | 未填 | `5XE7EXST` |
| P020 | Seed | `BNZW7ZET` | (RSA)²: A Rhetorical-Strategy-Aware Rational Speech Act Framework for Figurative Language Understanding | 10.18653/v1/2025.acl-long.1019 | `3EY26ZML` |
| P021 | Seed | `4CKEC2S8` | Dying or Departing? Euphemism Detection for Death Discourse in Historical Texts | 未填 | `WZRRYVM9` |
| P022 | Seed | `M6CK6F6X` | Revisitinga Pain in the Neck: A Semantic Reasoning Benchmark for Language Models | 未填 | `SGATNEYB` |
| P023 | Seed | `SYFQRQJA` | “Newspaper Eat” Means “Not Tasty”: A Taxonomy and Benchmark for Coded Language in Real-World Chinese Online Reviews | 10.18653/v1/2026.acl-long.426 | `2MRBMJH2` |
| P024 | Seed | `KLF2SUWU` | Analyzing Offensive Language Dataset Insights from Training Dynamics and Human Agreement Level | 未填 | `7M48T9C5` |
| P025 | Seed | `STHI3QUA` | HVGuard: Utilizing Multimodal Large Language Models for Hateful Video Detection | 未填 | `MSAWKS82` |
| P026 | Seed | `YRSLRTDX` | Robust Adaptation of Large Multimodal Models for Retrieval Augmented Hateful Meme Detection | 未填 | `FS2L6FPV` |
| P027 | Seed | `3YXYW3UY` | EXPO-HM: LEARNING TOEXPLAIN-THEN-DETECT FORHATEFULMEMEDETECTION | 未填 | `9GIQHJG8` |
| P028 | Seed | `DG6KGASE` | ImpliHateVid: A Benchmark Dataset and Two-stage Contrastive Learning Framework for Implicit Hate Speech Detection in Videos | 未填 | `I26SJ6YD` |
| P029 | Seed | `UC7ZVITY` | RV-HATE: Reinforced Multi-Module Voting for Implicit Hate Speech Detection | 未填 | `LX7GRQ83` |
| P030 | Seed | `DQMRPCBL` | SMARTER: A Data-efficient Framework to Improve Toxicity Detection with Explanation via Self-augmenting Large Language Models | 未填 | `R4ZBTGND` |
| P031 | Seed | `PS3EI65S` | AmpleHate: Amplifying the Attention for Versatile Implicit Hate Detection | 10.18653/v1/2025.emnlp-main.1469 | `ADHZTLIM` |
| P032 | Seed | `Y8EAPG6Z` | Generalizable Implicit Hate Speech Detection Using Contrastive Learning | 未填 | `KF6SAXUU` |
| P033 | 根 Collection | `D6BUXKDP` | Causality Guided Representation Learning for Cross-Style Hate Speech Detection | 10.1145/3774904.3792669 | `XYH33ZE4` |
| P034 | 根 Collection | `9I7DDMTU` | CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks | 未填 | `HAD4VET7` |
| P035 | 根 Collection | `2PU8MPJ4` | Enhancing Hyperbole and Metaphor Detection with Their Bidirectional Dynamic Interaction and Emotion Knowledge | 未填 | `X4YCZCWW` |
| P036 | 根 Collection | `YGW7NCNH` | StealthGraph: Exposing Domain-Specific Risks in LLMs through Knowledge-Graph-Guided Harmful Prompt Generation | 未填 | `3LRDFLK4` |

## 历史重复记录与保留内容

| Paper ID | 当前主条目 | 已清理的历史 Item Key |
|---|---|---|
| P001 | `ZCDZZRNF` | `M29WZENG` |
| P002 | `B5AV8KVF` | `XMDUI8IY`; `44SHKI82` |
| P003 | `HVRC2RT6` | `TGCSSWNW` |
| P004 | `LQ666R8A` | `HQW62KKI`; `3H3ESQBL`; `CDUJZIV7`; `8T5YS7UF` |
| P005 | `VDCGXL7U` | `W8RC4LX7`; `3RQKACAT` |
| P006 | `VQAAHEZ5` | `TSPYUCMF`; `49DIJ2XQ` |
| P007 | `CCIRF3ED` | `6M3GSRSK`; `FIFBUN3K` |
| P008 | `SQT4MZS6` | `QGNYJ8JV`; `A8738D3P` |
| P009 | `P3HCRLZM` | `6K87G2UJ`; `HTPFKVZV`; `VJCYGLIV`; `JEYUUSBY`; `ZDMEAWTE` |
| P010 | `FJ8KC5VL` | `DVG6EMFA`; `Y423GXPV` |
| P011 | `IGDADHE7` | `QCMZPQ3T`; `KIHWX52N` |
| P012 | `6999AQFP` | `CIIV9258`; `H93KD8U3` |
| P013 | `54553WUD` | `WFJLX7Y8`; `NLDYKRAU` |
| P014 | `AWJLGTIC` | `W6KWBAB2` |
| P015 | `NRFM5Q9V` | `RWPDI5JG` |
| P016 | `VGCGFHXT` | `VGUAAJ49` |
| P017 | `PS2J8SBE` | `V5GCZSET` |
| P018 | `S6RI8VD4` | `V5XT3W8A` |
| P019 | `UPVJUK7E` | `6IWB7ZHW` |
| P020 | `BNZW7ZET` | `GWAM3XL7` |
| P021 | `4CKEC2S8` | `SER45MBL` |
| P022 | `M6CK6F6X` | `SP9IZ7WW` |
| P023 | `SYFQRQJA` | `N3WT9W8T` |
| P024 | `KLF2SUWU` | `JQA5VD9K` |
| P025 | `STHI3QUA` | `YV2YS342` |
| P026 | `YRSLRTDX` | `9R2Z8PQ2` |
| P027 | `3YXYW3UY` | `KQS3EIUI` |
| P028 | `DG6KGASE` | `6YCPRT6B` |
| P029 | `UC7ZVITY` | `VQ8YFRPH` |
| P030 | `DQMRPCBL` | `CNPPAN8E` |
| P031 | `PS3EI65S` | `44JJIRLQ` |
| P032 | `Y8EAPG6Z` | `GLHZFRYH` |
| P033 | `D6BUXKDP` | `IRSJBJEZ` |
| P034 | `9I7DDMTU` | `WCUKSY67` |
| P035 | `2PU8MPJ4` | `5SAFEDCE`; `BE6ZILBY` |
| P036 | `YGW7NCNH` | `KE4QTLKB` |

- P004 的主条目 `LQ666R8A` 下保留 `H89242KM`（47 条批注）和 `8J4X7BZI`（40 条批注）；两份 PDF 字节相同，补回缺失文件后均可读取。
- P009 的主条目 `P3HCRLZM` 下保留 `I73WUKL3` 与 `R78ASLE5`。两份 PDF 哈希不同，提取正文仅有一处换行差异，保留供后续核验。
- P002 与 P033 在已清理历史条目中的笔记与当前主条目笔记哈希一致；没有删除独有笔记或 PDF 批注。
- P002 的正式期刊版与预印本仍作为不同来源记录，未将正式版全文或页码与馆内预印本混用。
