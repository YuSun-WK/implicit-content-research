# 表7｜横跨语用、隐晦检测与安全回应的方法族：优化对象、先验与独立证据

| 方法/正式出处 | Y与训练更新目标（不可跨任务排分） | 额外可用先验、训练/测试信息 | 作者报告的正面作用（P） | 边界与独立贡献尚未证实之处（P/S/O/H） |
|---|---|---|---|---|
| (RSA)² [@spinoso-di-piano-etal-2025-rsa]（ACL 2025 Main，CCF-A） | 给定候选意义的概率／选择，不是风险Guard | 修辞策略、候选空间和先验 | 特定语境下正确义分配概率总体相对L0提高 | 字面子群有反方向现象；额外先验不是零信息的递归机制独立效应 |
| Silent Signals [@kruk-etal-2024-silent]（ACL 2024 Main，CCF-A） | 已知词的实例编码义消歧 | 已知社群词条及编码释义、模型生成的筛样数据 | 在定义给定情形可做人审抽样Precision检查 | 主集模型筛阳，无法从中声称开放未来词或全量人审 |
| FETCH! [@sasse-etal-2025-making]（ACL2025 Main，CCF-A） | 社群编码root/type的候选发现，P/DPR/F0.5 | 20%词典种子、检索语料、根词匹配 | 作者Table4 EarShot-PREDICT Realistic(P,DPR,F0.5)=**(10.00,1.47,4.63)**；同篇DIRECT LLaMa-8B F0.5=1.17（不同策略/阈值） | DPR只统计语料中出现的参考root；词典留出≠现实时间外未知词，低DPR为反例 |
| FA-Net [@hu2024hidden]（AAAI2024 Technical，CCF-A） | 固定候选目标义的Acc@1/2/3，而非type发现 | 有标源域+无标目标域文本及候选目标类 | 作者Table3相对BERT报告Acc@1提高（逐域绝对值本轮未重新固定，保留定性P） | 源/目标相似度构造伪正对未逐对人审，不能叫完全不见目标域的零样本 |
| SeTox [@cui-etal-2026-new]（ACL 2026 Main，CCF-A） | 搜索辅助的输入新词毒性标签 | 检索时点、语料来源；工具轨迹SFT | 作者的有／无搜索协议下毒性判别得到改善 | 风险分类非准确恢复词义，也不能从闭集Acc声称时间外词项发现 |
| ImpCon [@kim-etal-2022-generalizable]（COLING2022，会议CCF-B） | 隐含有害文本二分类监督/对比，优化分类Y | 原句—implied statement配对与增广文本 | 作者报告自家实验协议下分类收益；本轮未按同标签预算重算具体差值 | 解释配对有助表示不等于解释忠实；不同语料的GT仍不统一 |
| SMARTER [@nghiem-etal-2026-smarter]（ACL2026 Main，CCF-A） | 隐含有害标签—解释联结的DPO，监督标签Y和解释文本 | gold类别条件偏好答案、已有HateCOT解释SFT、目标域少样本 | 作者报告目标少样本毒性检测改善（正式同预算逐项值本轮O） | chosen/rejected可能同时更改类别token，解释与标签收益难拆；不等于没有既有解释监督 |
| **ExPO-HM** [@mei2026expohm]（ICLR 2026 Main，CCF-A） | **解释后进行Hateful Meme二分类及细粒度标签**，policy SFT后课程GRPO+CDE奖励 | 政策手册、细粒度标签/训练数据、答案位置概率近似 | HatefulMemes binary macro-F1 naive GRPO 74.5→完整ExPO 81.1；相对RA-HMD直接方法80.2约+0.9pp | 训练课程与reward共同变化；CDE低/解释judge高不自动证明解释因果忠实；不等于严格S-S-U GT |
| 多任务与融合 [@guo-etal-2026-two; @zheng2025multigranular; @zheng2026m3ucd]（ACL 2026/AAAI 2025/2026均CCF-A） | 反讽MCQ／隐喻与语义属性分类 | 来源/目标概念、任务提示、OCR/细粒度人工属性 | DOSE 1%预算五任务均值78.90 vs LoRA77.70，M3UCD有部分任务正迁移 | 同论文亦有负迁移；gold辅标或新标签数量不等于架构独立贡献，GT模态主导归属≠模型因果依赖 |
| MCIB [@wang2026conditional]（AAAI 2026 Technical，CCF-A） | 文/音/视反讽分类／代理信息压缩目标 | KL/条件预测、数据集修订协议 | 作者报告weighted-F1=75.64，去细粒度结构为71.19 | 已固定[公开MCIB@d1430a](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L110-L126)静态损失行；真实batch与正式run仍O；同参数去KL/去条件预测受控消融缺失，不能称瓶颈独立消除捷径 |
| **攻击样本生成** ImpForge [@zhang-etal-2026-crossguard]（ACL 2026 Main，CCF-A） | **生成隐晦联合攻击图文**，PPO优化文本改写器 | 原风险请求、安全/语义/重叠奖励和生成图像 | 作者报告改写攻击更能让被测模型不安全回答 | PPO必要性缺同预算检索/Best-of-N等控制，攻击ASR↑不等于Guard检测能力↑ |
| **输入Guard** CrossGuard [@zhang-etal-2026-crossguard]（ACL 2026 Main，CCF-A） | **图文输入Safe/Unsafe**，LoRA/SFT更新Guard | 混合训练来源含约12.5%联合风险样本 | SIUO中加入ImpForge后Guard ASR60.33→5.39 | FigStep0.12→0.21；改进还含训练数据量和类别组成差，非新分类架构本身唯一原因 |
| **逐步风险归因** ThinkingGuard [@zhang2026thinkingguard]（作者ACM MM 2026录用；会议CCF-A，正式Track待核） | 输入风险标签/五步解释；SA-MCTS**离线**搜轨迹→Trajectory+Step-DPO更新VLM | 生成时Key/Trigger教师元素、偏好轨迹，Step偏好主要来自Unsafe | 作者Table3完整Unsafe F1 .810 vs去Step .779 | 配对图片不保证只变Trigger；额外Unsafe监督/token预算与解释忠实性未独立控制 |
| **安全有用回应** Meerkat-VL [@zhou2026meerkatvl]（ICML 2026 Main，CCF-A） | 生成安全且有帮助回应；Cold-start SFT→同Actor NPSV评分→一致性惩罚DPCA→GRPO | 训练时user_intent/harmful_intent/safety_warning规范风险说明；评分不重看图 | 作者报告综合响应质量改善（正式具体消融尚待逐表复核） | NPSV额外答案级风险信息、同Actor自评与DPCA模块独立贡献未匹配同预算；回应Judge不等于P_in GT |

**表注。** 表内数值都是各论文作者不同Y/G/E下的**同论文协议内对比**，不得横排绝对F1/ASR获得统一SOTA。六组代码固定SHA的公开来源直接列于正文§8.6；**S已固定不等于正式run已核**，未固定的公开数据精确S级数值降为O。正面结果、负迁移、额外监督和所缺独立对照必须一起读。
