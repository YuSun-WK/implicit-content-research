# R5-A｜引文对照与待核事项（第3–5章）

> 2026-11-09。此文件服务于本轮正文的可追溯引证与后续 BibTeX 统一；不是新的综述框架，也不替代正式论文。R5-A 只改 03_survey/R5_draft/。每条正文引文采用原 P/T/R2A 编号，正式出版页为书目依据，项目阅读卡或审计是论断核对记录。P=论文作者直接报告；S=项目对公开代码/数据的静态观察；H=综述作者跨研究推断；O=未证或待核。数字只按指定论文表格、图或节解释，不跨 Ground Truth 排名。

## 一、正文引文及证据定位

| 编号 | 正式论文及发表信息 | 本轮实际使用的证据定位 | 现有核对记录与等级 |
|---|---|---|---|
| P015 | [LLMs in Sarcasm Detection?](https://aclanthology.org/2026.acl-long.1346/)；ACL 2026 Main，CCF-A | §2–5、Tables 1–3、附录表和表示/扰动图；真人/合成二分类的协议差异 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md)；P+S，混杂解释为H |
| P020 | [(RSA)²](https://aclanthology.org/2025.acl-long.1019/)；ACL 2025 Main，CCF-A | §3–5、策略函数与 L0/S1/L1、Tables 1–3；候选意义概率和先验消融 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P020_RSA2.md)；P（arXiv v1 方法与ACL元数据交叉），正式PDF逐页式号O |
| P022 | [SemanticQA](https://aclanthology.org/2026.acl-long.210/)；ACL 2026 Main，CCF-A | §3–5、Tables 3/5；原子与一次输出的顺序组合、解释评分 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md)；P+S |
| P035 | [EmoBi](https://aclanthology.org/2025.acl-long.23/)；ACL 2025 Main，CCF-A | §3–4、Fig. 2、Tables 1–2；情绪/源目标/交互/再判断 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)；P+S |
| R2A-001 | [DRInQ](https://aclanthology.org/2026.acl-long.1597/)；ACL 2026 Main，CCF-A | §3–5、Table 2、Fig. 6；固定问句变语境，困难集五选一 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md)；P+S |
| R2A-003 | [Negation vs Implicature](https://aclanthology.org/2024.acl-long.33/)；ACL 2024 Main，CCF-A | §3–6、Tables 1–3；生成变体、三元组距离与常规意图指标 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_03_Negation_vs_Implicature.md)；P |
| R2A-004 | [Rhetorical Questions](https://aclanthology.org/2026.acl-long.5/)；ACL 2026 Main，CCF-A | §3–7、Figs. 1–4；反问探针可分性与方向/排序差异 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_04_Rhetorical_Questions_Linear_Probing.md)；P+S |
| P003 | [MultiMM](https://aclanthology.org/2025.acl-long.1275/)；ACL 2025 Main，CCF-A | 第3章仅援引测试信息预算线索，不作多模态效果主张 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P003_MultiMM.md)；S，正式运行路径O |
| P023 | [CodedLang](https://aclanthology.org/2026.acl-long.426/)；ACL 2026 Main，CCF-A | §3–5、Tables 1–4、Fig. 3；七类策略、评论标签与星级任务 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P023_CodedLang.md)；P+S |
| R2A-006 | [Silent Signals](https://aclanthology.org/2024.acl-long.675/)；ACL 2024 Main，CCF-A | §3–6、Table 1–2、Fig. 2–3、Appendix C/F；已知定义下消歧 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_01_Silent_Signals.md)；P+S |
| R2A-007 | [FETCH!](https://aclanthology.org/2025.acl-long.284/)；ACL 2025 Main，CCF-A | §3–5/9、Fig. 2、Tables 2–5、Appendix G；词典20/80留出与词项回收 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_02_FETCH.md)；P+S |
| R2A-008 | [FA-Net / Hidden Chasm](https://ojs.aaai.org/index.php/AAAI/article/view/29786)；AAAI 2024 Technical Track，CCF-A | 方法式1–6、Fig. 3、Tables 2–5；固定候选解码与目标域无标签适应 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_03_Hidden_Chasm_FA_Net.md)；P，伪正对错配率O |
| R2A-010 | [SeTox](https://aclanthology.org/2026.acl-long.1602/)；ACL 2026 Main，CCF-A | 方法/数据/消融节；工具轨迹SFT、检索开关、新词与普通词分项 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_01_SeTox.md)；P+S，时间污染O |
| T017 | [Latent Hatred](https://aclanthology.org/2021.emnlp-main.29/)；EMNLP 2021 Main，CCF-B | 第5章只作为隐式仇恨/隐含陈述的基础基准背景；未写具体训练机制和数字 | [R4-02候选分配](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_02_Paper_Allocation.md)；官方页+索引，全文机制O |
| P001 | [ToxiGen](https://aclanthology.org/2022.acl-long.234/)；ACL 2022 Main/Long Papers，CCF-A | §3–5、Tables 2/4；示例提示、ALICE解码、人审与外部人写测试 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P001_ToxiGen.md)；P |
| P032 | [ImpCon](https://aclanthology.org/2022.coling-1.579/)；COLING 2022 Main，CCF-B | §3–5；原文—隐含陈述对比与跨数据集分类 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P032_ImpCon.md)；P+S，解释忠实性O |
| P030 | [SMARTER](https://aclanthology.org/2026.acl-long.1584/)；ACL 2026 Main，CCF-A | Algorithm 1、§4–6、Table 1/5、Fig. 3；辅助SFT、DPO与低K评测 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P030_SMARTER.md)；P+S |
| P029 | [RV-HATE](https://aclanthology.org/2026.acl-long.2104/)；ACL 2026 Main，CCF-A | §3–4、Tables 1–3；四模块、固定权重PPO与公开脚本审计 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P029_RV-HATE.md)；论文P、当前代码S、发表版本关联O |
| P033 | [CADET](https://doi.org/10.1145/3774904.3792669)；WWW 2026 Main，CCF-A | §4–5、Tables 2–3；表示分支、反事实/重建与跨风格协议 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P033_CADET.md)；论文P、当前代码S、版本关联O |
| R2A-011 | [When People are Floods](https://aclanthology.org/2025.acl-long.398/)；ACL 2025 Main，CCF-A | §3–5；七类预设源域、人工隐喻认同与阈值化AUC | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_02_When_People_are_Floods.md)；P；独立危害GT不存在 |
| R2A-012 | [Sheep’s Skin, Wolf’s Deeds](https://aclanthology.org/2025.acl-long.814/)；ACL 2025 Main，CCF-A | §2–4、Table 2；合成改写、人审与单/多轮正侧评测 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_03_Sheeps_Skin_Wolfs_Deeds.md)；P，失败独立归因O |
| R2A-013 | [AUTALIC](https://aclanthology.org/2025.acl-long.1022/)；ACL 2025 Main，CCF-A | §3–4、Table 2–3、Figs. 1/3/5、Appendix A.1；相邻句语境与三人标签 | [R3-B定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_01_AUTALIC_FINAL.md)、[三争议审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)；P+S，CSV分布O |

跨章方法与任务边界依 [R4-01](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_01_Formal_Outline.md)、[R4-07](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)；图表标签参考 [R4-03](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_03_Figures_and_Tables.md)。本轮未制作 F3/T3/T4 图表成品。

## 二、尚待核事项与正文已采取的处理

1. **P020 版本**：已读卡的公式/表号主要按 arXiv v1 核对，ACL 正式 PDF 未逐页对齐；正文以机制和表内方向性结论表述，转换 BibTeX/最终页码前对照正式版。
2. **P015 与 P035 机制归因**：P015 真人/合成样本多因素共同变化；P035 核验增加调用预算，当前代码“隐喻先行”与论文双向描述有差异。正文仅称作者协议下的分类效果，不把可视化或自我核验等同语义因果。
3. **R2A-001 数据版本**：论文 819/400 与当前公开 CSV 231 行口径不同；正文只谈论文明确的 400 道困难集，不写公开全量复现。
4. **P023 数据与评测**：词典扩展的覆盖偏差、官方固定 split/测试词项交叉尚未核；正文未把 900/7,744 写成自然基准率，亦未将星级改善直接认作解码成功。
5. **R2A-006/007**：Silent Signals 论文与公开主集数量不同、主集非全量人审；FETCH! 主实验是已有词典留出，真实时间外、词典外语境人审金标不足。正文未作开放世界已解决主张。
6. **R2A-008/010**：FA-Net 跨域伪正对类别一致率未独立核实；SeTox 训练测试词项交集、实时检索时点/来源及 model-unknown 的时间含义未核。正文将错配/污染标为风险，未写成既有实证事实；SeTox 书目采用 ACL 正式页，暂不复制作者 README BibTeX。
7. **R2A-011/012**：Flood 只有源域隐喻人工 GT、没有逐例非人化或仇恨 GT；Sheep 合成审核者可见原句，单轮主要为正例，多轮混有响应策略。正文分别写作源域测量和受控风险压力测试。
8. **R2A-013 AUTALIC**：论文总 2,400 与正负分项算术冲突，CSV 未重计；三名标注者为受训高年级本科志愿者，无同模型删语境消融，数据授权有限制。正文不报冲突分项、不量化语境增益。
9. **P029/P033 发表结果与公开代码**：RV-HATE 当前脚本在 test 标签上寻权；CADET 当前代码用目标 test 作验证，反事实/循环实现与文述不同。正文将其记为静态审计风险，不推定正式发表实验实际由同一代码版本生成。
10. **T017 与非核心候选**：T017 本轮仅官方出版页和既有分配索引，未当作机制/数值强证据。P016/P021 等书目信息或全文未核的候选未承载正文核心论断。

## 三、自审结论

- 三章分别包含 3.1–3.5、4.1–4.6、5.1–5.6，与 R4-01/R4-07 对齐；正文未重写第1、2章或其他窗口资产。
- 每节以问题、代表方法、论文间比较、可定位实验及边界组织；综述判断不当作论文作者结论。所有保留数字均能回到上表所列正式论文位置或明确标为项目静态审计；无跨异质 GT 的 F1/Accuracy 排名。
- 已核官方出版页、项目精读与 R2/R3 综合；未进行模型重跑、全量新文献检索或完整 BibTeX 编排。待核事项不阻断本轮正文，可在后续审稿与统一参考文献阶段逐项关闭。
