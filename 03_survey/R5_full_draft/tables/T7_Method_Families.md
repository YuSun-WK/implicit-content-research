# 表7｜横跨语用、隐晦检测与安全回应的方法族：优化对象、先验与独立证据

| 方法/正式出处 | Y与训练更新目标（不可跨任务排分） | 额外可用先验、训练/测试信息 | 作者报告的正面作用（P） | 边界与独立贡献尚未证实之处（P/S/O/H） |
|---|---|---|---|---|
| (RSA)² [@spinoso-di-piano-etal-2025-rsa]（ACL 2025 Main，CCF-A） | 给定候选意义的概率；**C1/C3** | 修辞策略、候选空间、意义先验；不新增类别微调 | 普通L0→hard策略L0整体0.73→0.85，反讽0.48→>0.8；hard L1先验均匀0.84→0.51 | 字面子群0.95→0.77；概率非Acc。[ACL正式论文Tables 2–3／Figure 4](https://aclanthology.org/2025.acl-long.1019.pdf) |
| Silent Signals [@kruk-etal-2024-silent]（ACL 2024 Main，CCF-A） | 已知词的实例编码义消歧 | 已知社群词条及编码释义、模型生成的筛样数据 | 在定义给定情形可做人审抽样Precision检查 | 主集模型筛阳，无法从中声称开放未来词或全量人审 |
| FETCH! [@sasse-etal-2025-making]（ACL 2025 Main，CCF-A） | **词项type/root回收；C1**，非实例消歧 | 参考词典约20%种子＋社群语料；近邻提取／过滤 | Balanced Table4 PREDICT P/DPR/F0.5=14.81/1.65/5.70%；Table5 DIRECT Llama2-13B=2.97/13.58/3.52% | 精度与覆盖取舍，两模型／输出预算不同；留出词典≠时间外新义；P与DPR分母见表3 |
| FA-Net [@hu2024hidden]（AAAI 2024 Technical，CCF-A） | **固定候选目标义分类**，Acc@k | 源域标签＋目标域无标文本、已定位委婉位置／类别 | 作者Table3/5报告候选义分类改善；本轮不新增未核具体分数 | 目标域可见非零样本；相似伪正对无逐对金标核验；不同于FETCH的type回收 |
| SeTox [@cui-etal-2026-new]（ACL 2026 Main，CCF-A） | 搜索辅助的输入新词毒性标签 | 检索时点、语料来源；工具轨迹SFT | 作者的有／无搜索协议下毒性判别得到改善 | 风险分类非准确恢复词义，也不能从闭集Acc声称时间外词项发现 |
| ImpCon [@kim-etal-2022-generalizable]（COLING 2022 Main，会议CCF-B） | **隐含危害分类**，对比学习 | implied statement正对／增强表达＋危害类监督 | 作者报告分类泛化提升；本轮不把它当解释DPO实验 | 正对额外语义监督；无证据据表示距离认定解释忠实 |
| SMARTER [@nghiem-etal-2026-smarter]（ACL 2026 Main，CCF-A） | **标签—解释成对DPO**，最终毒性分类；C2的监督对照 | HateCOT前序解释SFT＋目标少量标签；gold类别条件chosen/rejected | 作者报告目标少样本分类提升；本轮不新增未核消融分数 | 类别token与解释同时变，监督和token未独立匹配；不是ImpCon对比学习，也不是纯测试CoT |
| DRInQ [@arai-ren-2026-drinq]（ACL 2026 Main，CCF-A） | **五选一会话含意；C2**；冻结模型提示 | 3个in-context例；同400困难题加生成解释指令 | Table2 GPT-5-Mini .56→.62；GPT-4o .62→.63 | Sonnet-4.5 .65→.62、o3 .67→.67；均Accuracy，3次抽样，非全819题；不等token |
| VAGUE [@Nam_2025_ICCV]（ICCV 2025 Main，CCF-A） | **四选一行动意图；C2**；冻结模型CoT | 原图＋间接表达＋候选；无需测试gold direct/solution | 作者v3 Table3 GPT-4o原图64.6→66.4%，Gemini-1.5-Pro60.6→64.4% | [ICCV正式补充材料Table G4](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Nam_VAGUE_Visual_Contexts_ICCV_2025_supplemental.pdf) Qwen72B原图72.8→69.9%；作者v3 HTML编号G6；长度／格式混杂仍O |
| **ExPO-HM** [@mei2026expohm]（ICLR 2026 Main，CCF-A） | **解释后进行Hateful Meme二分类及细粒度标签**，policy SFT后课程GRPO+CDE奖励 | 政策手册、细粒度标签/训练数据、答案位置概率近似 | HatefulMemes binary macro-F1 naive GRPO 74.5→完整ExPO 81.1；相对RA-HMD直接方法80.2约+0.9pp | C2：训练课程与reward共同变化；CDE低/解释judge高不自动证明解释因果忠实；不等于严格S-S-U GT |
| DOSE [@guo-etal-2026-two]（ACL 2026 Main，CCF-A） | 新闻图文的五种反讽理解MCQ | 任务标签／提示、共享与私有LoRA专家 | 作者Table3同底座1%训练五任务均值78.90 vs LoRA77.70 | 同比例原始样本不自动等有效任务数／token；人工模态主导标签不是因果去模态结果 |
| MGMCF [@zheng2025multigranular]（AAAI 2025 Technical，CCF-A） | 图文隐喻／情绪／意图／冒犯分类 | 预计算source/target等概念输入；公开loader已固定（附录A A4） | 作者报告对象、全局—局部和双语义结构消融收益 | pkl的gold／预测来源、基线预算、正式run对应仍O |
| M3UCD [@zheng2026m3ucd]（AAAI 2026 Technical，CCF-A） | 隐喻／源目标／意图等多任务输出 | OCR、细粒度属性监督、共享LoRA | 作者报告部分任务正迁移；本轮不新增未核分数 | 亦有负迁移；新增监督量非纯架构效应，Complementary人工类别非模型去模态证据 |
| MultiMM [@yang-etal-2025-cultural]（ACL 2025 Main，CCF-A） | 情绪辅助图文隐喻检测 | 所审公开路径已固定（附录A A3），测试读CSV情绪列 | 作者论文报告情绪辅助配置收益；P与下一列S分开 | 正式run、情绪列有效来源、OCR及baseline预算对应O，不泛称源码尚未固定 |
| MCIB [@wang2026conditional]（AAAI 2026 Technical，CCF-A） | 文/音/视反讽分类／代理信息压缩目标 | KL/条件预测、数据集修订协议 | 作者报告weighted-F1=75.64，去细粒度结构为71.19 | 同参数去KL/去条件预测受控消融缺失，尚不能声称瓶颈独立消除捷径；公开路径已固定（附录A A5），真实batch shape／论文run仍O |
| **攻击样本生成** ImpForge [@zhang-etal-2026-crossguard]（ACL 2026 Main，CCF-A） | **生成隐晦联合攻击图文**，PPO优化文本改写器 | 原风险请求、安全/语义/重叠奖励和生成图像 | 作者报告改写攻击更能让被测模型不安全回答 | PPO必要性缺同预算检索/Best-of-N等控制，攻击ASR↑不等于Guard检测能力↑ |
| VLSU冻结回应评测 [@palaskar2026vlsu]（ICLR 2026，CCF-A） | **安全／有用回应；C3**，不更新参数 | 同一请求、同一模型，Harmless→Helpful指令 | Gemini-1.5 Borderline拒答62.4→10.4%；安全边界侧受益 | Unsafe拒答90.8→53.9%；QwenVL32B Borderline反23.4→30.7%；非P_in分类，不能建立跨模型统一曲线 |
| **输入Guard** CrossGuard [@zhang-etal-2026-crossguard]（ACL 2026 Main，CCF-A） | **图文输入Safe/Unsafe**，LoRA/SFT更新Guard | 混合训练来源含约12.5%联合风险样本 | SIUO中加入ImpForge后Guard ASR60.33→5.39 | FigStep0.12→0.21；改进还含训练数据量和类别组成差，非新分类架构本身唯一原因 |
| **逐步风险归因** ThinkingGuard [@zhang2026thinkingguard]（作者ACM MM 2026录用；会议CCF-A，正式Track待核） | 输入风险标签/五步解释；SA-MCTS**离线**搜轨迹→Trajectory+Step-DPO更新VLM | 生成时Key/Trigger教师元素、偏好轨迹，Step偏好主要来自Unsafe | 作者Table3完整Unsafe F1 .810 vs去Step .779 | 配对图片不保证只变Trigger；额外Unsafe监督/token预算与解释忠实性未独立控制 |
| **安全有用回应** Meerkat-VL [@zhou2026meerkatvl]（ICML 2026 Main，CCF-A） | 生成安全且有帮助回应；Cold-start SFT→同Actor NPSV评分→一致性惩罚DPCA→GRPO | 训练时user_intent/harmful_intent/safety_warning规范风险说明；评分不重看图 | 作者报告综合响应质量改善（正式具体消融尚待逐表复核） | NPSV额外答案级风险信息、同Actor自评与DPCA模块独立贡献未匹配同预算；回应Judge不等于P_in GT |

**表注。** 表内数值都是各论文作者不同Y/G/E下的**同论文协议内对比**，不得横排绝对F1/ASR获得统一SOTA。六组S级代码固定commit与行号见正文附录A；正式run对应仍O。C1–C3与§8.1.1逐行对应；作者版本与正式出版分开，未重跑作者模型。正面结果、负迁移、额外监督和所缺独立对照必须一起读。

