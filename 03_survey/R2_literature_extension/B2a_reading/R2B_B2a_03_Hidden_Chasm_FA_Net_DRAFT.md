# R2-B / B2a-03｜Uncovering and Mitigating the Hidden Chasm（FA-Net）— 精读工作稿

> **状态：WORKING DRAFT，等待用户学术确认；不合并main。** 2026-11-08；临时编号 R2A-008；保留全部原始P/T编号。  
> **证据分层**：A=AAAI 2024正式论文及表图公式；B=SelfEDI（IEEE S&P 2021）公开仓库README关于数据来源/可获取性；C=本项目研究者分析。没有找到可确认属于这篇 AAAl FA-Net 论文的作者官方代码仓库；**未复现**、未对原语料逐条核验。正式PDF文本已提取检查；在线截图接口受限，图像细部未逐像素确认。  
> **会议**：AAAI 2024 Technical Track，CCF-A；非 Findings / Workshop。**论文范围的 euphemism 是面向敏感/非法语义词项的英语替代表达子域，不能代表一般礼貌委婉语全部现象，更不能等同所有 coded language/hate speech。**

## 1. 元数据、研究问题、主要主张
- 完整标题：**Uncovering and Mitigating the Hidden Chasm: A Study on the Text-Text Domain Gap in Euphemism Identification**。
- 作者：Yuxue Hu, Junsong Li, Mingmin Wu, Zhongqiang Huang, Gang Chen, Ying Sha。
- Proceedings of the AAAI Conference on Artificial Intelligence, 38(16), 18270–18278, 2024（2024-03-24官方上线）；DOI 10.1609/aaai.v38i16.29786。
- [AAAI官方页](https://ojs.aaai.org/index.php/AAAI/article/view/29786) / [官方PDF](https://ojs.aaai.org/index.php/AAAI/article/download/29786/31358)。
- **研究问题**：依靠直白目标词（heroin / cocaine等）句子构造可自动标注训练集，但真正评测/应用是隐藏的委婉语（ice / weed等）句子。两类句子上下文语体不同，造成**同为文本的source→target分布差异**，直接导致“根据上下文预测被遮蔽目标意义”的性能下降。
- **方法**：提出 FA-Net，三项训练约束——IC-net同域类内判别；HC-net基于跨域相似度伪正例的对比；EM-net无标签目标域预测熵最小化——附加到LSTM、CNN、BERT特征提取器/分类头上。核心不是一个新的BERT架构，不是词表外开放发现。
- **结果**：BERT Acc@1 在 Drug/Weapon/Sexuality 分别由0.24/0.38/0.38提升到0.35/0.47/0.50（Table3）；与自监督词袋SelfEDI相比提升分别0.15/0.14/0.18**绝对百分点**。三个模块联合在Table5中最优，但不能仅凭该表证实锥效应为性能瓶颈的唯一因果机制。

## 2. 任务界定：不是“找出文本中的委婉词”
**目标是 Euphemism Identification（意义指派），不是 Euphemism Detection（先判断是否出现委婉语）。**
- 事先有**可用的候选目标词/目标意义类别集合** T = {t1,...,tK}（Drug K=33、Weapon 9、Sexuality 12）；测试句中委婉词的位置须已知并遮蔽（如“XXX vendors of [MASK] ...”）。
- 输入 X：一个从上下文移除了目标词或委婉词的句子 + 固定候选类别表；输出 Y：每个候选目标意义的概率/排序，Top-k是否包括既有字典指定的目标词。
- 研究者任务记号 **非原论文新增公式**：source Ds={(mask(x_i,target_keyword), y_i)}, y_i是目标词类；target Dt={mask(x_j,euphemism)} 无训练标签；推断 \hat y_j=argmax_{t∈T} p_\theta(t|masked_context_j)；标注目标是一对一归属的预定义类别。
- 不是在原句里做span detection、自由自然语言解释、词典外意义生成、无候选概念识别，也不输出 hate/offensive/unsafe 分类。
- 所谓self-supervised训练更准确是**从显性目标词语料自动抽取有标签代理任务**：将直白词遮蔽后，原直白词本身成为监督标签；既不需要人工逐样本训练标签，也不等于模型“无监督”。
- **关键域定义**：source=显性目标词出现的句子（遮蔽后）；target=委婉表达出现的句子（遮蔽后）。二者“同模态不同表达分布”，不是语言对语言翻译，也不是文本 vs 图像。

## 3. 数据集与 Ground Truth
§Experiment/Table2沿用SelfEDI（Zhu et al., IEEE S&P 2021，CCF-A）的 Drug/Weapon/Sexuality，分别约：
| Dataset | 全部语料句子数 Entries | 类别数 K | 含直白目标词的句子 Key Entries |
|---|---:|---:|---:|
| Drug | 1,271,907 | 33 | 4,566 |
| Weapon | 3,108,988 | 9 | 19,003 |
| Sexuality | 2,894,869 | 12 | 7,215 |
- 语料来自 Reddit、Gab 等；包括含目标词、含委婉词和其余背景句。**百万级Entries不是百万条人工标注有效训练/测试样本**；真正有直接源域监督信号的Key Entries仅几千/数万，目标域委婉语测试需要另查数量。
- 训练/验证：source端“遮蔽显性目标词”样本按8:2划分。目标域无标签“遮蔽委婉语”样本**参与FA-Net的HC、EM训练**，最终在这类样本上评价；这是**无监督域适应（可能是transductive）**，不能说“训练时从不接触测试域文本”。
- 测试标签：既有委婉语→目标关键词对应表，而非直接人工读取每条句子判别该次词义；Drug基于DEA slang/code word词典，Weapon依赖 Online Slang Dictionary、Slangpedia、Urban Thesaurus，Sexuality依赖 Online Slang Dictionary。作者明确承认词典不可能覆盖全域、可能出错；**一对一意义假设未建模同词多义或上下文歧义**。
- 类别语义可能合并近义目标关键词；作者声称评测列表只在评价时用，不参与训练（除既定目标词列表）；但**候选目标意义表 T 参与训练与推理，是任务强先验**。
- 原始完整语料实际可获取性有限：[SelfEDI官方仓库 README](https://github.com/WanzhengZhu/Euphemism/blob/master/README.md)写明Drug原始Reddit数据需向作者申请；Weapon要求从多个来源申请/重建；Sexuality为历史Gab语料；仓库提供用于运行的 sample，但声明样本不能代表可靠结果。不能将“AAAI论文使用公开来源”写成“无需申请的一键下载金标”。

## 4. “Text-Text Domain Gap”到底是什么？
- **现象**：Fig.1来源（训练）和目标（测试）的t-SNE/UMAP分布区分；Fig.2以 SelfEDI 和 BERT 的句向量相似性支持分布集中在不同高维区域；训练/验证的相对高性能不能迁移到目标。
- **作者解释**：显性目标词语境较直白；委婉词语境往往带不同文体、语用和隐含线索。因此分类器在source学到的决策边界在target不稳；作者借用Liang et al. (NeurIPS 2022，CCF-A)“cone effect”解释两分布聚为不同高维锥形区域。
- **研究者严格评估**：t-SNE/UMAP只能支持分布差异的视觉证据，Fig.2的锥形几何/高维表面积计算是解释性论证，**不足以证明所谓cone effect造成分类失败或FA-Net通过特定锥几何修复**。替代机制还有话题频率、词典覆盖、句法/风格与类别不平衡。作者后续Fig.4给出适应后的分布视觉及A-distance下降，仍不能独立区分每个机制因果归因。

## 5. FA-Net 方法（§Feature Alignment Network; Eq.1–6; Fig.3）
基准模型基于masked上下文x，经特征提取器 E 得到 h=E(x)，分类头在已知候选意义 T 上输出概率p_\theta(y|x)；source 有标签可训练普通 CE。论文附加三种对齐损失：

### IC-net: In-domain contrastive learning
- 只在**source有标签批次** Bs 上：同类目标词上下文作为正样本，不同类作为负/竞争对；拉近同类、分开异类。
- 公式核心（研究者结构化转录论文Eq.2，忽略对多正对的外层均值排版细节）：
  L_IC^s = -(1/|Bs|) \sum_{i,j∈Bs} 1[y_i^s=y_j^s] log{exp(sim(h_i^s,h_j^s)/τ) / Σ_{k∈Bs}exp(sim(h_i^s,h_k^s)/τ)}.
- sim为余弦；τ为温度。**这不是目标域真标签监督**。

### HC-net: Hard cross-domain contrastive learning
- 对无标签target样本和有标签source样本两两计算相似度；若 sim(h_i^t,h_j^s)>γ，把这一对视作伪正例并拉近；两个方向target→source和source→target。
- Eq.3/4在两种方向分别使用跨域InfoNCE分母；Eq.5结合为
  L_HC=α L_HC^{t→s}+(1−α)L_HC^{s→t}，α为可学习的方向权重（论文称总体无“额外参数”，与α学习存在术语边界）。
- **最重要的假设**：距离近→在目标词意义上也相近。论文没有目标域真标签用于筛选对应类，**相似并不保证同一隐藏意义**，可能跨域误配；γ=0.6是论文Fig.5所示的较优配置，仍不保证伪标签可靠。

### EM-net: Entropy minimization
- 在**无标签target批次**上，使用预测分布熵正则：概念表达 H(p)=-Σ_{c∈T}p(c|x)log p(c|x)，使输出更确定；原文Eq.6仅简记为样本层Σ P(T_i)log P(T_i)，**类别求和/符号下标书写不够透明，不能据此精确还原源码**。
- 没有新金标，梯度来自模型自身预测；若当前预测错误，熵约束也可能增加错误自信。作者发现第1 epoch就加EM不理想，因此在后续epoch才启用，Drug上η=15较优，各数据最佳η不同。

### 总体训练
- “基础模型源域交叉熵 + 同域对比 + 跨域对比 + 目标域熵约束”的联合优化。**原论文主要展示Eq.1–6分项，没有公开可逐项照抄的统一损失系数/训练调度代码**，因此这里不发明作者从未明确报告的完整加权损失公式。
- 测试：给遮蔽了委婉词的目标域文本，用训练好的分类器在固定T中排序输出。**不需要真正重新生成委婉词或将原词编辑成直白词**。

## 6. 实验对照和数值（Tables 3–4）
主要指标Acc@1、@2、@3（候选词意义排序Top-k是否命中唯一参考目标）。论文表：
| Baseline | Drug @1 | Weapon @1 | Sexuality @1 |
|---|---:|---:|---:|
| Word2Vec | .07 | .10 | .17 |
| SelfEDI（IEEE S&P 2021, CCF-A） | .20 | .33 | .32 |
| LSTM | .11 | .20 | .24 |
| LSTM+FA | .13 | .24 | .28 |
| CNN | .12 | .23 | .25 |
| CNN+FA | .15 | .27 | .31 |
| BERT | .24 | .38 | .38 |
| **BERT+FA** | **.35** | **.47** | **.50** |
- 相对同一BERT的绝对增加 **+0.11/+0.09/+0.12**，比较SelfEDI为 **+0.15/+0.14/+0.18**。不能与相对增幅30.3%-75%混淆。
- Table4给出该时点的 StableLM、mPLUG、Llama2、GPT-3.5 等LLM Prompt baseline：GPT-3.5在Drug/Weapon/Sexuality分别.33/.17/.42；BERT+FA为.35/.47/.50。部分LLM拒绝回答敏感词，模型规模和输入/拒答协议不等价；**不能外推到2026年LLM或认为普通领域适用性优于全部大模型**。
- 作者服务器 Tesla V100 32G；BERT max length 128、batch 32、lr 5e-5、AdamW+warmup；另有BERT源域MLM领域适配预训练（文章写max length512、batch64、iteration3；含糊，复现需要进一步核验）。**无作者FA-Net官方代码可审**，不能保证单卡16–20GiB完整端到端在≤6h复现。

## 7. 消融：哪些贡献得到独立支持？（Table5 Acc@1）
| 配置 | Drug | Weapon | Sexuality |
|---|---:|---:|---:|
| BERT | .24 | .38 | .38 |
| BERT+IC | .27 | .39 | .41 |
| BERT+HC | .29 | .42 | .43 |
| BERT+EM | .27 | .38 | .40 |
| BERT+IC+HC | .34 | .45 | .47 |
| BERT+IC+EM | .30 | .40 | .42 |
| BERT+HC+EM | .33 | .43 | .45 |
| **BERT+IC+HC+EM** | **.35** | **.47** | **.50** |
- **模块消融成立的范围**：相同实验设定下三个项联合优于删减项。HC单独增幅较明显，IC+HC协同强；EM在Weapon单独**不提升**（.38→.38），不能说“三项任一单独都显著改善每个数据集”。
- **未证明项**：使用真实target标签辅助的Oracle对照、语体混杂控制、无target语料（source-only）与target-test adaptation分离、相同预算的MMD/DANN/other UDA baselines、各伪正例实际同义比例、标签错误影响、跨时间/文化迁移、统计多随机种子置信区间。Table5只说明加入模块有用，不证明cone effect是唯一根因。
- **实验协议额外风险**：论文语句“以获得最好结果的参数进行对比”、γ与η对每个领域的最优配置，是否基于同一个target test进行选择并不完全透明；需核实是否有独立target验证集。不可在无证据下直接认定发生评测泄漏。

## 8. 创新性与综述定位
- **机制层创新**：把“文本→文本的域差异”作为委婉语识别中的显式诊断对象，并用同域监督对比、跨域相似伪正例、目标域熵最小化组合训练。单个模块（对比学习、UDA、熵最小化）在机器学习领域已有大量先例；**不是从零发明对比学习或领域适应**。
- **使用范围**：主要是敏感主题（Drug/Weapon/Sexuality）的固定候选目标意义恢复；不是一般语言中的所有委婉语或谐音、dog whistle、所有有害类别。
- **与Silent Signals（ACL2024 Main, A）**：后者给**已知编码词项+编码定义**做实例级普通义/编码义消歧；本文**已知候选直白目标词列表**、已经定位并遮蔽的委婉语位置，做固定类别映射，而且允许无标签target训练，二者不能简单比较指标。
- **与FETCH!（ACL2025 Main,A）**：FETCH发现新的词项类型（词典held-out recall），FA-Net预测**已定位词项的预设意义类别**。前者词项类型GT，后者语义映射GT；均未证明开放世界新词的唯一语义。
- **与P023 CodedLang（ACL2026 Main,A）**：P023观察中文真实编码策略，含形音和跨语言转换、片段级人工解码；FA-Net英语敏感词委婉语多类别映射，侧重源目标语体错位，不能把两文的“编码操作”同义化。
- **与P020 (RSA)²（ACL2025 Main,A）**：前者监督+无监督域对齐固定分类，后者以修辞策略r和潜在说话者/听者概率建模非字面意义；不是同一推断对象和相同loss。
- **与 T012 JointEDI（ACL 2024 Findings，不能当ACL Main/CCF-A）**：同组作者另提出双语委婉语检测+识别的统一生成任务，并提供BME数据；说明FA-Net **不应被写成统一Span Detection + Open-Ended Decoding**。
- **综述价值**：在“意义理解/解码T2”中作为**自监督代理训练数据域偏差**的标志性案例，关联T1发现与T2意义恢复，但以T2为主；横向机制章在“社群表达/词义替代”的一类实例，证据章论述词典型GT与target无标签接触、伪正例可靠性。

## 9. 公开资源及待核验清单
- **正式PDF**：[AAAI下载](https://ojs.aaai.org/index.php/AAAI/article/download/29786/31358)；稿件本身无明确FA-Net官方GitHub URL。定向查询没找到能确认是此项工作的官方仓库。作者相关公开仓库 [FFI](https://github.com/DHZ68/FFI) 对应WWW 2024另一论文，不能冒充FA-Net实现。
- **基线可复用性**：[SelfEDI项目](https://github.com/WanzhengZhu/Euphemism) 提供原任务代码、样例、部分drug GT，但README明确全部Drug/Weapon/Sexuality原语料并非直接分发，许多需申请/重建。只复现SelfEDI源码不等于复现FA-Net。
- **高优先级检查**：(1) 三数据的target evaluation真实样本数、实例级多义误差与时间划分；(2) target训练无标签数据是否与最终testing的句子重复、部署是否transductive；(3) pseudo positive sim>γ的错配率及EM确认偏差；(4) γ、η是否在目标测试集选最优；(5) 完整联合loss系数、学习率/epochs/初始化/种子与训练源码；(6) cone effect独立因果证据及普通UDA对照；(7) 旧词典与现代新义覆盖、跨时间及社群；(8) 可复现全量原语料访问与许可证。
- **静态核验状态**：论文原文/表格已核；未访问完整代码/原始语料，未实施GPU运行。Figure 1/2/3/4/5的视觉描述依据官方PDF文本、caption及叙述，当前在线截图功能返回错误，**细粒度图像数字不可视作已核验**。

**一句话（工作版）**：AAAI 2024 FA-Net研究的不是定位或生成委婉语，而是“在有限直白目标词集合内，根据已遮蔽的委婉语上下文恢复具体目标义”；发现源域显性表达与目标域委婉表达的文本分布差异，并通过源域类别对比、无标签目标域跨域对比与熵最小化改善候选意义排序。其强性能依赖固定词义集合、可接触目标域无标签语料和词典型测试GT，不能直接证明开放式隐晦意图理解或未知编码发现。
