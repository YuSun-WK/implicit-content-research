# 重要决定记录

## 2026-10-26：仓库与编号

- 目标仓库初始为空。先在默认分支创建说明性 README 以建立首个提交，再在 `initialize-research-knowledge-base` 分支提交知识库文件并通过 PR 审查；未创建替代仓库。
- 固定 P001–P003；P004–P032 按 Seed Collection 现有顺序分配给其他独立论文，P033–P036 保留给仅在回收站的四篇历史作品，不计入当前馆藏。编号一经提交不随排序改变。

## 2026-10-26：文献身份与版本

- 同题之外还核对 DOI、作者、arXiv 标识、Venue 和 PDF SHA-256。历史 `collectionItems` 中有 36 组作品、89 条关系；其中当前在用仅 32 组/32 条，另 57 条已在回收站。全部 Item Key 连同状态保留于映射表。Zotero 内不作合并或修改。
- P002 当前馆内三份 PDF 是同一 2024 arXiv 预印本；已知的 2025 ACM 正式版另记一条 Source，正式版全文与差异仍待核验。
- 刻板印象检测综述两种 PDF 哈希的提取正文仅差一个换行；同 DOI 与作者，暂按同版重复条目管理。PDF 标 2025 年 11 月、Zotero 标 2026 年 4 月，年份在索引中显式保留冲突。
- 当前馆藏仅三篇既有卡片标为“已分析”，其余 29 篇标为“待分析”；P033–P036 仅作回收站历史追踪。

## 2026-10-26：导入与存储

- 导入原有三张卡片及总表；保留原有证据边界，仅去除绝对本地 PDF 路径。未重写其科研结论。
- 不将 PDF、Zotero 数据库、缓存、数据集、权重、账号信息或密钥提交到 GitHub。

## 2026-10-26：纠正回收站统计口径

- 初版审计直接统计 `collectionItems`，误将 57 条回收站记录列为当前根 Collection 条目；Zotero 界面与 `deletedItems` 交叉核对后纠正。当前根 Collection 与 Seed 都是 32 条在用文献。
- 57 条回收站历史条目中，有 48 条与当前作品重复、9 条属于 4 篇仅在回收站的作品；不自动永久删除。
- 回收站条目 `HQW62KKI` 的附件虽缺失文件，却保有 40 条独有批注，直接清空回收站会丢失研究记录。

## 2026-10-27：恢复、合并与清理

- 按用户授权将四篇缺席作品恢复到根 Collection，沿用 P033–P036；`01seed_papers` 仍为原 32 篇。
- P004 将 `HQW62KKI` 的附件 `8J4X7BZI` 与 40 条独有批注保留在主条目 `LQ666R8A` 下；其缺失 PDF 由同篇另一附件补回并核对字节哈希。主条目原有 `H89242KM` 与 47 条批注亦保留。
- P009 将 `JEYUUSBY` 下字节不同的 PDF `R78ASLE5` 移至主条目 `P3HCRLZM`；主条目原有 `I73WUKL3` 保留。两种 PDF 提取正文仅有换行差异，但仍保留两份附件供版本核验。
- 永久清理前逐项检查回收站，55 个对象均可追溯到目标 Collection 中的重复条目或其附件，且无待删除批注。随后通过 Zotero 桌面界面清空回收站。当前 36 个主文献 Key 全部可查，回收站为 0。
- 历史 Item Key 保留在 `zotero_mapping.csv` 供审计，但标记为永久清理，不作为可访问的馆藏条目。未直接修改 Zotero 数据库或日志；手动附件改动仅为 `8J4X7BZI` 补回缺失 PDF 文件，并已核对哈希。


## 2026-11-19：图文联合隐含风险检测 Framework-Transfer Idea Discovery（严格初筛）

- **Decision / target correction:** 本轮唯一目标是**图文联合隐含风险检测**，不是 Social Bot Detection；此前同窗口输出的 SBD 候选、No-Go 与 IDEA-011 建议全部不适用于本任务。以输入风险分级/分类为主，和自由生成响应的拒答/ASR分开评测。
- **Verified fact / existing evidence:** 已有 P037 VLSBench（ACL 2025 Main）、P038 VLSU（ICLR 2026）、P034 CrossGuard（ACL 2026 Main）、P039 ThinkingGuard（ACM MM 2026）、P040 Meerkat-VL（ICML 2026）。按 P038 存档的公开 CSV 静态审计，严格 Safe-Safe-Unsafe 35 条；广义联合风险升级 179 条（不是全部样本）。
- **Verified fact / fresh collision boundary:** 
  - *EviSafe: Evidence-Grounded Safety Evaluation for Vision-Language Models*（2026-08 arXiv preprint，**非已核实顶会录用**）：已有图文证据标注、自然行为、风险证据反事实一致性评测；https://arxiv.org/abs/2608.23313 。
  - *MTMCS-Bench*（ACL 2026 **Findings**）：已有成对安全/不安全多轮图文情境与风险升级/切换协议；https://aclanthology.org/2026.findings-acl.96/ 。
  - *CMIE*（EMNLP 2026 Main）：已将有害图文交互本身定义为安全遗忘对象；https://aclanthology.org/2026.emnlp-main.2220/ 。
  - *Transfer Safety Awareness for Cross-Modal Safety Drift*（EMNLP 2026 **Findings**）：冻结主干、安全方向迁移的直接先例；https://aclanthology.org/2026.findings-emnlp.638/ 。
  - *ConceptGuard*（EMNLP 2026 Main）：图文联合隐含风险预检测与概念级安全处理已存在；https://aclanthology.org/2026.emnlp-main.2308/ 。其作者公开仓库仅有 README、requirements、权重等少量文件，不能当成完整训练/评测 release：https://github.com/Ruize-Ma/ConceptGuard 。
  - *SingGuard*（2026 arXiv 技术报告，未核验正式 A 会）：政策输入、自适应图文风险判别已有直接竞品；当前 GitHub 缺少完整训练/评测实现：https://github.com/inclusionAI/SingGuard 。
- **Verified fact / source-framework static code audit:** NeurIPS 2025 D&B *SpuriVerse* 官方代码有数据构建/推理/微调接口，但完整构造依赖人工核验和多种 API，当前复现代价较高（https://github.com/Anderson-Lee-Git/SpuriVerse）；NeurIPS 2025 Main *ARDS* 官方代码有 worst-subgroup 检索、选择、LLaVA 训练/评测，但训练数据与原始工程较重（https://github.com/xyang583/ARDS）；EMNLP 2026 Findings *Counterfactual Tests for Measuring Chain-of-Thought Faithfulness in Visual Language Models* 有代码/分析脚本，但不附原始及编辑后的图片（https://github.com/neuralisa/cct-vlm）。
- **Interpretation:** “联合风险首次被发现”“有风险归因/反事实即创新”“动态政策+图文评测即创新”“换一套 worst-group 数据采样即新任务”目前都存在显著直接或近邻 novelty collision；VLSU 严格联合升级小样本、作者协议/图片可达性等问题使部分源框架无法满足低成本可信验证门槛。
- **Decision:** 本轮**未选出新的 Scientific GO / Weak GO shortlist**；不是对所有研究空间的穷尽性否定。不生成新方法、不启动 Codex、不做训练，不用 SBD 结论覆盖本项目。若未来重开某候选，首先证明 (i) 独立金标和充分数量的目标样本，(ii) 与前述 2025–26 直接竞品的明确差异，(iii) 源仓库训练/评测主路径及单卡预算，(iv) 预注册负对照和 24–48h kill gate。工程易行与科学可发表必须分别判定。
