# P026｜RA-HMD — Robust Adaptation of Large Multimodal Models for Retrieval Augmented Hateful Meme Detection

> 2026-11-04 用户授权定稿上传合并。定稿指原论文方法和结果证据归档；**未做代码逐行审计或 GPU 复现**，机制未证项仍开放。

## 01 书目信息
- Mei et al., EMNLP 2025 Main (Oral), CCF-B, DOI: 10.18653/v1/2025.emnlp-main.1215。
- 正式论文：https://aclanthology.org/2025.emnlp-main.1215/；PDF：https://aclanthology.org/2025.emnlp-main.1215.pdf
- 官方仓库：https://github.com/JingbiaoMei/RGCL；作者项目：https://rgclmm.github.io/
- 直接先例：RGCL, ACL 2024 Main, CCF-A，https://aclanthology.org/2024.acl-long.291/，已提出检索引导对比学习与近邻分类。

## 02 任务与问题
输入 Meme 图像 I、叠加文本 T、二分类真值 y。目标是改善常规检测性能、跨领域分类以及专用微调后的通用视觉语言能力保留。不是一般多模态安全响应任务，也不直接证明隐含语用机制。

## 03 架构
LMM 提取最后 token 的隐藏状态 h。两条路径：h→LMH→生成类别词；h→MLP→g→LRC 分类，g 同时用于 KNN 检索。论文 §3.2 明确 RA-HMD **默认以 LRC 预测**，跨域主要使用 RKC，LMH 是辅助训练和可保留的生成路径。

## 04 两阶段损失与梯度
- Stage 1 (§3.3, Eq.1–4)：通过 LoRA/QLoRA 更新 LMM 适配器，同时更新 MLP/LRC。L1 = L_LM + L_LR。L_LM = -log P_LMH(s(y)|I,T)，s(0)=benign、s(1)=hateful；L_LR = -y log p -(1-y)log(1-p)。**同一已有类别标签**监督语言输出和分类输出；无人工 gold explanation SFT。LM Loss 与 BCE 均可更新 LMM 的 LoRA。
- Stage 2 (§3.4, Eq.5–6)：冻结 LMM，只训练 MLP 和 LRC。FAISS 找同标签高相似度正例 g+ 和异标签高相似度困难负例 g-，各 1 个。L_CL=-log{exp[cos(g,g+)]/[exp cos(g,g+)+exp cos(g,g-)]}；L2=L_CL+L_LR。该表示优化有利于标签区分，不能据此证明正确理解图文隐含关系。

## 05 RKC 推理
参考集合先编码保存 G={(g_j,y_j)}；测试 Meme 经 LMM+MLP 得 g_t，使用 FAISS 检索 K 个近邻，按 Eq.7–8 计算 sigmoid(Σ_k bar_y_k cos(g_k,g_t))，bar_y=+1 (hateful) 或 -1 (benign)，默认 K=20。举例正类近邻 .95/.90、负类 .60/.55/.50，得票 .20，Sigmoid≈.55，判正类。**不是检索文本后让 LLM 生成判决的生成式 RAG**。

## 06 数据、标签
Appendix A/Table6：HatefulMemes 8500 train/1000 test；HarMeme 3013/354；MAMI 9000/1000；Harm-P 3020/355；MultiOFF 445/149；PrideMM 5063/507。HarMeme 原有 very/partially harmful 合并为正类；其他集含 misogyny/offensiveness 等不同正类定义，跨域泛化数字含标签口径变化的潜在混杂。

## 07 基线与主实验
Table1，Qwen2-VL-7B：HatefulMemes SFT AUC 86.3→RA-HMD 91.1；HarMeme 91.8→93.2；MAMI 82.6→90.4；Harm-P Acc 85.9→91.6；MultiOFF 67.8→71.1；PrideMM 75.1→78.1。论文另比较 CLIP、HateCLIPper、RGCL 和其他 LMM/系统，不同数据集评测口径不能混用。

## 08 跨域协议与公平性
Table2：在源数据集训练，目标域训练划分的**有标签样本**构成 RKC 检索库，目标域测试划分用于评估；无需目标域梯度更新，但**不是无标签目标域泛化**。Qwen2-VL-7B：SFT+4-shot vs RA-HMD+RKC 的 HatefulMemes Acc 60.6→69.3；HarMeme 62.4→81.7。4-shot 对 K=20 检索库目标标签预算不公平；Appendix F/Table9 相同 RKC 下 SFT 67.1→RA-HMD 69.3、HarMeme 75.4→81.7，支持训练策略存在增益但远小于跨推理方式的全部差额。

## 09 消融与 LMH 为什么保留
Table3（Qwen2-VL-7B/HatefulMemes）：完整 AUC/Acc 91.1/82.1；Stage1-only 90.2/81.4；Stage2-only 84.4/74.2；三损失联合一步训练 88.9/77.8。
**Appendix H Table11：删除 Stage1 LM Loss**：HatefulMemes AUC 91.1→88.4、Acc 82.1→79.6；HarMeme Acc 88.1→85.1；跨域 HatefulMemes Acc 69.3→66.6、HarMeme 81.7→81.1。因此 LMH 不是默认最终分类器，但其标签生成监督确实帮助分类表示学习；不能称 LM Loss 多余。
**通用能力机制边界**：LM Loss 只预测标签，不是通用任务训练；MLP 将分类检索 g 与 LMH 使用的 h 分离，Stage2 冻结 LMM 避免进一步扰动生成模型（Appendix D）。作者**没有报告删除 LM Loss 后的 MMMU/GQA/SEED 结果**，所以 LM Loss 防遗忘的独立因果作用未证。

## 10 通用能力、鲁棒与解释
Table4/Appendix I（Qwen2-VL-2B：原始/SFT/RA-HMD）：MMMU 40.2/39.1/40.4；SEED 72.7/72.1/72.7；GQA 60.4/57.0/60.1，支持整套方案在所测基准上保留能力。Appendix G Table10 常规域 LMH/LRC/RKC 差距小，跨域 RKC 大幅优于 LRC。Table5 SaltPepper 攻击：LRC 原AUC91.1→84.4（-6.7），RKC90.8→86.8（-4.0）；不能声称所有模块跌幅更小。§4.9 解释：RA-HMD 在 judge 偏好比较中胜 SFT 61.5%，质量分 5.6 vs 4.9；无解释 gold SFT，不能视为 explanation faithfulness 证明。

## 11 创新性与关系
RGCL 已提供 RKC/检索引导对比学习，RA-HMD 的真正增量是面向生成式 LMM 的双路径投影、分阶段训练和较完整跨域/能力保留评测。原创性属中等、实用性较强；EMNLP CCF-B 不代表已知 A 会拒稿原因。与 P027 ExPO-HM（ICLR2026）区别：P026 优化直接分类和检索，P027 研究解释式生成/策略优化；与 P034 CrossGuard 的联合输入安全判别亦非同任务。

## 12 未证与复现建议
作者用 QLoRA、冻结视觉模块、MLP 2 层/1024维、Stage2 lr 1e-4，K20；报告单 RTX3090 两阶段约4h、Stage2约10min（Appendix B），未报告可保证的峰值显存。仓库 Stage1 LLaMA-Factory 子模块版本已更新，不能默认与论文版完全相同；**未核完整实际训练/检索代码或重跑**。
优先 Kill Test：对固定 RKC 分离 LM Loss、MLP、CL 的真实增益；补测去 LM Loss 后的 MMMU/GQA；固定目标域标签预算并控检索库规模；使用现成图文对照检验模态依赖。开放：生成能力保留的因果机制、图文捷径、标签定义冲突、参考库近重复与泛化。
