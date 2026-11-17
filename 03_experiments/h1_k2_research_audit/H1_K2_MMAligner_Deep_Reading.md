# MMAligner：原文、公式与实现审计

原文：[arXiv v1全文](https://arxiv.org/html/2608.05909v1)，正文§1–7及附录A–E已读取；作者为Shenyi Zhang、Keyan Guo、Zihao Wang、Xuebin Li、Lingchen Zhao、Hongxin Hu、Chao Shen、Qian Wang。作者论文出版栏与[仓库](https://github.com/shenyizg/MMAligner)均标CCS 2026，DOI[10.1145/3830454.3832599](https://doi.org/10.1145/3830454.3832599)。本轮未取得ACM最终版逐页比对，不把arXiv内容与最终出版PDF的完全一致性视为已证。

代码固定于`261c63c6b940029c4e2bc9849ba0494abf71fde9`；九个必读/辅助文件的Git blob见[来源清单](evidence/mmaligner_sources.json)。本轮只静态检查，未加载其模型、运行训练或调用Judge。

## 任务与证据概要

作者研究文本可表达的同一有害意图转为图文输入后拒答下降；其方向干预、表示校准与良性保持均服务于安全生成。主评测是拒答/输出无害性、正常任务效用，非TriggerBench输入分类或PairAcc。其训练/测试为MM-SafetyBench的200/772配对划分；另测外部安全、越狱与效用数据，四模型含LLaVA、LLaVA-NeXT、Qwen2.5-VL和Llama-V。论文报告近99%的拒答和较小效用损失，并含方向对照、约束消融和适应性攻击；这些均是作者结果，本轮未复现。[原文§3–6、附录](https://arxiv.org/html/2608.05909v1)

威胁模型允许攻击者控制图文、访问模型参数与内部状态；适应性评测包含内部steering和图像空间优化。内部hook攻击需要比仅提交图片更强的部署权限；有限步图像攻击未成功不能保证完整白盒稳健性。H1若研究输入guard，应单独规定攻击者能否绕过guard，不照搬该生成模型威胁模型。

结果定位：原文Table6中MM-SafetyBench四模型拒答分别为100.00/99.22/100.00/100.00%；这不是风险分类准确率。Table7的下/上界消融支持两项约束有不同的行为作用，但不足单独证明良性逐例项与统计项各自不可替代；需要这两项分别消融和同预算控制。外部泛化与效用图是作者证据，尚无本轮复现。

以下是基于公式与代码的独立推导、实现核查及迁移判断，不沿用作者“已定位全部根因”的措辞。

## 几何定义及数学核查

记选层输入末token表示为`h_l(x)`。实现对被文本模型拒答的Unsafe与Safe表示随机配对作差矩阵D，首右奇异向量为v；均值差归一化为方向d。**v与d不是同一个定义**，代码实际steering和loss使用d，v保存但未直接进入安全loss。SVD未先中心化，与标准中心化PCA并非无条件等价。[core](https://github.com/shenyizg/MMAligner/blob/261c63c6b940029c4e2bc9849ba0494abf71fde9/mmaligner_core.py)

选层以文本拒答Unsafe和Safe的余弦分离为依据。实现`avg_intercls_cosine`对所有跨组配对取均值，论文式11写随机匹配平均；二者并非逐次相同的估计量。需要重现选层而非硬搬LLaVA的23层到Qwen3-VL；模块编号与hidden_states最后归一化层也须验证。[step1](https://github.com/shenyizg/MMAligner/blob/261c63c6b940029c4e2bc9849ba0494abf71fde9/step1_calibrate.py)

边界估计通过对20个良性probe沿d增加激活，搜索首次拒答所需幅度，取中位数。文本与图文分别估计幅度，**共享方向不等于共享数值边界**。实现从8开始倍增至512，之后10次二分；没有成功翻转的样本被跳过。以下问题需在复现时显式检验：

1. 二分要求沿幅度的拒答判定近似单调；关键词Judge、解码变化或输出崩溃可能破坏单调性。
2. 已在零幅度拒答的良性样本未先单独处理；不能把起始8视为真正最小幅度。
3. 对每例的最小**增量**取中位数不自动等于对中心化坐标的绝对分类阈值。若probe起始坐标为`s_i`，应核查`median(s_i+alpha_i)`与`median(alpha_i)`的差异。
4. 跳过无法翻转样本可能造成可翻转子集偏差；必须报告跳过数，不能把τ解释为覆盖所有样本的严格边界。

代码训练坐标与两项loss为：

\[
s(x)=\langle h(x)-\mu_{S,mm},d\rangle,\quad \delta=s-\tau;
\quad L_U=\lambda_l E\log(1+e^{-\delta})+\lambda_u E[\max(0,\delta)^2].
\]

这里作者称“Hard Lower Bound”的softplus是**软惩罚**，不是硬可行域。独立数学核查：δ=0时下界项为log2，梯度为−1/2；δ>0仍非零，故“越过边界后惩罚消失”不严格。若权重为0.5与0.05，δ>0的单样本合成梯度为`−0.5/(1+exp(delta))+0.1*delta`，最小点在边界内部而非恰好0。实现并不保证每个训练点或任何测试点都满足δ≥0。

良性保持对逐样本表示差、batch均值差、逐维方差差作平方惩罚。实现是全向量MSE，**不是只在d的投影上保持**；MSE的维数归一化也与公式写L2平方在尺度上不同。batch1时方差项恒为0，不能把用户batch1工程设置当作统计保持原样复现。训练按Unsafe一步、Safe一步交替更新，是权重适配，不是部署时给每例直接添加向量。[core与step2](https://github.com/shenyizg/MMAligner/blob/261c63c6b940029c4e2bc9849ba0494abf71fde9/step2_train.py)

## 干预能够证明什么

方向正/负/正交的幅度匹配对照，比二维可视化或相关性更强：它支持特定内部扰动对拒答行为具有方向特异的作用。但把良性样本也推成拒答，首先证明的是**行为控制充分性**，不单独证明正确风险识别、完整原生计算路径或所有自然失败都由该变量中介。

代码hook在`generate`整个调用期间挂载，每次forward改变最后位置；通常同时涉及prefill与逐token解码。若要声称“输入级表示导致最终拒答”，必须分开prefill-only、decode-only和两者干预；不能默认这是只改一次输入末token的纯实验。还需norm匹配随机方向、多次随机方向、非目标层、相同标签但不同语义的对照，排除一般输出偏置。不存在从拒答可控性到风险分类边界可迁移的数学必然性。

正文把总体意图等价和回答涉及风险当作感知替代解释的排除依据。这些检查有价值，但外部Judge认定“涉及意图”不足以证明每个关键视觉事实或目标绑定均正确。对H1，事实问题和关系问题仍须独立测量。

## 逐文件复现性审查

| 文件 | 读到的实现与直接后果 |
|---|---|
| `mmaligner_core.py` | BF16加载、`device_map=auto`；未用NF4、无20GiB进程监控。自动设备分配可能跨设备/卸载，须新单卡入口。边界与方向代码可作为概念性对照。 |
| `step1_calibrate.py` | 重复提取四组全层状态，少于20条文本拒答就退出；缓存标签仅检查长度，不核对模型revision与样本hash。同长度错缓存风险应另修复。训练金标本身不等于拒答筛选标签。 |
| `step2_train.py` | 默认25 epoch、LR3e−4、rank8/alpha32；所有名字匹配q_proj/v_proj的模块加LoRA，未限制到选层，也可能匹配视觉塔，须打印实际可训练名单。目标层是loss读取位置，不是“只更新该层参数”。Unsafe逐例反传，Safe保留多个前向图后拼batch，峰值需单测。 |
| `step4_boundary.py` | 硬编码LLaVA与其calibration；扫幅度和统计覆盖，默认split full含校准样本。诊断可用，但full不是独立测试性能。文件没有实现论文全部方向对照或适应性攻击。 |
| `step5_eval.py` | 随机抽取test子集、固定seed0；默认Unsafe200/Safe100，README示例Safe20。生成异常写成`<err:...>`后继续判拒答，缺独立失败率汇总。只有额外API客户端存在才计算helpfulness。 |
| `mmaligner_judge.py` | 有OpenRouter GPT-4o-mini调用；无key或失败回退关键词。相同接口在有/无key时实际评审器不同，必须记录。helpfulness失败样本被跳过，需保存缺失分母。 |
| `utils.py` | 校准与边界直接用关键词Judge，词含illegal/ethical/dangerous等，可把“含风险词但仍配合”的回答判拒答。Qwen生成分支没有显式固定do_sample，须核查generation_config。全层state收集会增加内存。 |
| `requirements.txt` | torch2.1.2、transformers4.51.3、peft0.17.0，其他部分未固定；不能直接装进H1现有Qwen3环境，需隔离依赖。 |
| `README.md` | 自称LLaVA basic implementation，另需Llama-Guard-3-11B-Vision评价无害性；并非四模型所有论文表格的完整无API复现包。 |

每个文件均见固定[代码目录](https://github.com/shenyizg/MMAligner/tree/261c63c6b940029c4e2bc9849ba0494abf71fde9)及[blob清单](evidence/mmaligner_sources.json)。这些是静态风险，未声称已经运行失败。论文正文将benign正确性Judge与主要拒答Judge作不同表述，代码固定GPT-4o-mini；复制原论文结果必须锁定真实Judge版本，不能静默以关键词替代。

## 成本与20GiB可行性

论文Table18报告训练0.1 GPUh，不能外推到4090上的端到端复现：校准全层前向、文本拒答标注、20×多次搜索、评测与Judge成本应分列，该表未提供用户20GiB条件下的独立实测。7B BF16仅权重约14GB数量级，再加视觉/激活/优化器；官方代码未给满足20GiB的证据。Qwen3-VL也不是其已支持的Qwen2.5分支。**本轮不能认证官方完整训练可在20GiB内运行。**

可低成本借鉴：CPU方向/阈值数学检查；冻结模型在少量输入提取选层最后token；仅数例、小幅受控hook。以上每一项先单独测进程峰值，输入长度/分辨率保持，避免全层全token留在GPU。不可直接借鉴为“已可行”：25epoch训练、batch4多图反传、同时加载Guard大模型、完整有API效用评审。无API版本只能标为本地改编评测。

本轮进一步直接解析官方四个split JSON：Safe与Unsafe各有200条Train、772条Test；每条含`instruction/text_instruction/image_path`，即每个安全级别200个双模态格式记录，共400个训练记录、按两种模态展开为800种输入格式。不能把它说成总共只有200个输入。Train/Test的ID、图像路径和完整`text_instruction`交集均0；图文输入的短`instruction`仍有Safe2种、Unsafe11种文本跨split复用，所以README的prompt-disjoint不能理解为所有多模态文本模板逐字不重复。复用泛化模板不自动证明完整图文样本泄漏；图片字节/语义近邻仍未审计。证据见[split核算](evidence/mmaligner_split_audit.json)。

上述是训练/校准监督；H1的36个TriggerBench Test对对应72个Joint输入及180次三条件预测，是被看过的探索性测试。二者数据单位、标签目标、模态语义、输出类型与用途都不相同，不能用“36<200所以更省数据”比较。新方法不得在36对上训练再报告同集性能。

## 对H1候选创新的裁决

| 候选 | 与现有工作的覆盖 | 决策 |
|---|---|---|
| A 风险方向校准 | 与MMAligner/ShiftDC/ReSAM高度相似；改Safe/Unsafe头仍不自动新颖 | 当前否决为主贡献 |
| B 图文安全表示对齐 | TGA、CMRM、Internal Activation Revision等已有 | 方向名称不能作贡献 |
| C 风险表示恢复 | 同属恢复文本安全机制的成熟叙事 | 需完全不同可检验机制才重开 |
| D 保持Safe表示的轻约束 | MMAligner直接含逐例与统计保持 | 实质重合，否决 |
| E 反事实一致性正则 | MMAligner不等同TriggerBench翻转监督；但ThinkingGuard及一般对比/不变学习已覆盖核心套路 | 部分重叠；单加loss不足 |
| F 动态风险门控 | ASTRA及后续自适应steering已有强先例 | 必须证明显著不同的条件变量与控制对象 |

图文风险证据绑定与拒答方向校准在技术目标上不同，但**ThinkingGuard已经明确建模实体、属性、意图与关系**。可检验剩余空间是：风险判断能否对经验证的关系干预敏感、对无关干预不敏感，而不只是输出关系解释。尚不能写“此前无人研究绑定”。

图文隐含风险往往可以用完整文本描述，并非必然处于MMAligner声称的image-native范围之外。相反，H1的Image-only到Joint变化不保证语义等价，和其文本→多模态等价意图设定并不同构。不能靠这两个范围的混用制造gap。

## 是否运行baseline

当前不值得运行整套MMAligner。先过数据和统一任务门槛；若将来主张表示校准，至少加入同信息/同预算的均值方向、ShiftDC和简单线性分类头；MMAligner式loss改为分类目标后叫“MMAligner-inspired adaptation”，不冒充官方实现。只有论文涉及安全生成与拒答时，才在同模型、同数据、同输出指标下复现原方法。不能把99%拒答与70.83%分类准确率或41.67%PairAcc并排排名。

结论：MMAligner显著压缩表示恢复路线；它没有替H1证明关系绑定失败，也没有替H1认证一个新的方法问题。
