# R2-B/B2b-01｜SeTox 精读定稿

状态：定稿（2026-11-08）；保留未关闭核验问题。临时编号 R2A-010，不占用 P/T 正式编号。

## 出版信息与任务
[New Terms, New Toxicity: Consensus-based Chinese Neologism Toxicity Detection via Search-Augmented LLMs](https://aclanthology.org/2026.acl-long.1602/)，ACL 2026 Main，CCF-A。正式书目信息以 ACL Anthology 为准；官方代码 README 内 BibTeX 与正式页面存在不一致，不能直接复制。

任务为中文新兴词语场景的毒性/安全分类（T4），同时涉及词项定位（T1）和语义解释（T2）。编码、隐喻、新词、毒性不能互换标签；敏感话题、成人内容也不天然等于仇恨或毒性。

## 方法与监督
SeTox 使用搜索增强 LLM，输入句子，模型识别潜在新词、决定是否搜索、接收检索结果后输出安全标签与解释。训练采用工具调用轨迹的监督微调而非 PPO/DPO。训练记录包含原句、目标词、检索结果、标签与解释；解释生成涉及 Qwen3-Max。联合训练兼顾新词工具使用与普通安全样本。

## 数据与评测
作者报告词典 974 条，训练集 1,595 条（995 新词样本、600 普通样本），新词测试 624 条，普通测试 368 条。新词测试的 model-known 319 / model-unknown 305，unknown 是相对于指定基础模型的解释能力定义，**不等于训练阶段未见词项，也不等于严格时间外推**。作者报告 SeTox-7B 的 DR=92.86、UDR=94.07、新词测试准确率=94.07（%）；无搜索消融 DR=87.63、UDR=85.19。结果仅为作者报告，尚未独立复现。分类指标不能直接证明语义理解或解释忠实性。

## 代码与数据
官方仓库 https://github.com/thu-coai/Setox ；数据 https://huggingface.co/datasets/thu-coai/SeTox ；模型 https://huggingface.co/thu-coai/SeTox-Qwen2.5-3B 和 https://huggingface.co/thu-coai/SeTox-Qwen2.5-7B 。仓库提供推理、评测、训练配置与数据文件；实时检索使用 Serper API Key，另有 static/none/mock 路径。README 披露原始词典 7 个重复 source id、训练搜索结果噪声。未做 GPU 复现。

## 与 B2a 的联系
FETCH! 侧重词项发现，Silent Signals 侧重给定编码义的语境消歧，FA-Net 侧重有限候选目标意义指派；SeTox 侧重有害性判断。外部搜索提供证据不等于恢复真实交际意图，也不保证恢复完整隐含意义。

## 开放核验（不因定稿而关闭）
1. train/test 是否有相同新词词项，需直接按发布数据做词项级交集审计。
2. model-unknown 与时间新颖性、词典外未知词是否对应；论文没有严格时间外推证据。
3. 检索信息与数据标注过程的潜在循环依赖；解释质量不等于忠实性。
4. 五类风险中话题类别与行为伤害类别混用的标签有效性。
5. README BibTeX 与 ACL 正式出版信息冲突；复现依赖与搜索噪声需进一步实测。

## 综述可用结论
论文支持“检索增强有助于新兴网络词语的安全分类”，但不足以断言“模型已可靠理解开放世界全新词义”。保留 R1 的 T1/T2/T4 分离框架。
