# P013｜Exploring Concreteness Through a Figurative Lens

> 2026-10-31 用户授权定稿、上传并合并。定稿指正式论文精读及作者公开代码的**静态审计**完成；不代表 GPU 复现或因果主张获得独立证实。

## 01 书目与来源
- Saptarshi Ghosh; Tianyu Jiang. Exploring Concreteness Through a Figurative Lens. **ACL 2026 Main（CCF-A）**，15471–15490。DOI 10.18653/v1/2026.acl-long.705。
- 正式全文：https://aclanthology.org/2026.acl-long.705.pdf （20页，2026-10-31实际读取及查看图表）；正式页：https://aclanthology.org/2026.acl-long.705/。
- 代码：https://github.com/cincynlp/concreteness-interpretability 。已静态审读 README、extract_embeddings/extract_llama_embeddings.py、diffmean_svd_1D-conc-axis/compute_diffmean.py、1D_axis_via_svd.py、1D_axis_projection.py、1D_axis_steering/steer.py。
- 标签：Concreteness、Contextual Word Meaning、Figurative Language、MLP Probe、DiffMean、SVD、Activation Steering；不是有害内容检测器。

## 02 任务与概念
- Concreteness（具体性）：词语意义能否指向可直接感知实体，例如 window 实体窗户（高） vs window of opportunity（低）。具体性与隐喻/习语/转喻相关但不等同。
- 核心研究问题：(1) LLM哪个层编码和调整具体性？(2) 是否有跨层一维几何轴？(3) 干预该方向能否改变字面和修辞表达？
- 研究对象是词语在句子中的语境义与模型内部表示；没有直接提供 implicit hate 的标签、模型或任务。

## 03 整体方法
1. 将“完整句子+目标词”输入 Decoder-only LLM，通过评分 Prompt 让模型输出1–5具体性 token；提取各层隐藏状态，训练每层 MLP Probe 预测人类静态具体性评分。
2. 以 Brysbaert(2014) 词语静态评分构造高具体性和低具体性组；每层 DiffMean = high 均值表示 − low 均值表示；论文将跨层 DiffMean 堆叠，做全局 SVD 取得一维具体性轴；通过投影评估层级分离和下游修辞分类。
3. 在推理时向选定层隐藏状态加 alpha×单位轴向量，不更新模型权重，观察修改后输出更字面/更修辞的比例。

## 04 Concreteness Token 实现详解
- 使用 Decoder-only 模型，目标词本身所在 token 不能看到完整右侧上下文；因此 Prompt 提供完整 sentence 和目标词的语境具体性问题，由末尾位置综合输入。
- 官方 Llama 提取脚本的 Prompt 结尾额外包含字符串 [MASK]；Llama 不存在与 BERT 相同的原生 mask 预测操作，这里只是输入文本。
- 核心路径：generate(max_new_tokens=1, do_sample=False) 输出一个新 token；将完整生成序列重新输入模型，output_hidden_states=True；取 outputs.hidden_states[1:]，每层选择 [batch=0,last_pos,:]，其中 last_pos=generated_ids.shape[1]-1。
- 每层记录 {word,sentence,conc,embedding}。Llama-3.1-8B 每层隐藏向量 H=4096；这些是**已经生成的评分 token 重新入模后的表示**，不是用于预测这个 token 的上一位置隐藏状态。
- **开放混杂**：该向量包含被生成评分 token 的语义信息；Probe 的相关性可能部分来自自产生的评分，而不完全是目标词语境理解。控制实验应比较：生成前 Prompt 末位置、生成后数字 token、固定占位 token、词本身位置。
- 人工真值是 Brysbaert 约40k英文词静态分数（1–5）；并非每个具体句子的 gold contextual norm。论文的合成同词高/低具体性配对只是另一评估设计，不能与静态词典监督混淆。

## 05 DiffMean/随机重复抽样/SVD
- 正式论文§4.1：25,000 Wikipedia sentences；词静态分数≥4的 high 2256句，≤2的 low 2116句。每层 w^(l)=mean(h_high^(l))−mean(h_low^(l))，堆叠所有层 w^(l) 得 W ∈ R^{L×H}，SVD(W)=UΣV^T；取首个右奇异向量作为 global/layer-independent concreteness axis u∈R^H。
- 投影：对同一模型、同一维度隐藏表示 h，s=h·u 是标量。一维轴是表示空间中的方向，而非新的神经元。
- **公开 DiffMean 脚本的额外抽样**：SAMPLES_PER_SET=250，REPEATS=10，SEED=42；在每层对 high/low 各250条无放回随机抽样，计算高低均值差、L2归一化；10轮彼此可抽中重复数据；结果矩阵为 [10,H]。计算10个差向量间45个独立向量对余弦相似度并平均，评估方向的抽样稳定性。重复抽样既没有扩充训练数据，也没有训练10个模型。
- **论文/代码不一致**：公开 1D_axis_via_svd.py 逐层读取 [10,H] repeated diffmeans，先中心化 D=dms−row_mean(dms)，再对每层 D 做 SVD，保存 per-layer basis。[10,H]逐层中心化 SVD并不等价于论文 [L,H]跨层全局 SVD。
- **机制影响**：中心化可能移除10次抽样共同的 high-low 差异方向，使首奇异向量主要反映抽样波动。示意：若3次 diffmeans 为 [3,1,0]、[3.1,.9,0]、[2.9,1.1,0]，中心化后主方向 [1,−1,0] 而非原均值[3,1,0]。这一点不能直接判定论文结果错误；可能是公开代码和论文实验版本未对齐，必须作者说明或运行核实。
- 文件接口也不同：SVD 脚本保存 subspace_1/layer_i_concreteness_basis_k1.npy；投影脚本默认读取 subspace_k1.npy；steering 脚本读取 global_concreteness_basis_k1.npy。公开仓库所读脚本未自动产生这些全局文件。README 中部分脚本名称与真实文件不同。

## 06 Probe/分离/修辞分类实验
- MLP每层从目标提示的隐藏状态回归词静态具体性分数；Pearson/Spearman与误差体现信息可读性，不等于严格证明模型掌握隐含语义的因果表征。
- 在合成同词 literal/figurative 数据中，计算不同层相对于该词静态具体性评分的偏移；早层已经显现分离，但静态真值和句子因素仍需控制。
- Table4（Llama-3.1-8B，AUROC百分数）：MAGPIE idiom 95.2 vs 全维训练98.5；EPIE 95.3 vs99.2；VUA metaphor95.7 vs97.6；MUNCH93.2 vs95.1；ConMeC metonymy60.2 vs62.6；MetFuse85.7 vs96.3。转喻更难，不能将一维轴解释为统一覆盖所有修辞。
- 投影脚本允许 80%有标签训练子集选择最大F1阈值，在20%测试集报告 F1/Accuracy/AUROC；AUROC是投影标量的无阈值可分性。“zero-shot”主要指轴/基础模型未经下游修辞任务训练，不是绝对无需标签调阈值。

## 07 Steering机制与结果
- 论文 §5：选择 Llama层20、Qwen层25、Gemma层27、GPT-OSS层15；对输入“Rewrite the following sentence clearly and naturally”推理时修改 h'_l=h_l+αu，α>0 指向高具体性/字面，α<0 指向抽象/修辞。论文 α=±40。
- Table6：Llama literal→figurative 0→12/100，figurative→literal42→71；Qwen0→10、45→68；Gemma0→9、52→67；GPT-OSS0→15、39→75。由两名独立人工评判；提升明显不对称，生成新修辞比还原字面困难。
- 公开 steer.py 使用 forward hook 注册指定 model.model.layers[TARGET_LAYER]，在层输出 [batch,seq,H] 加 αu，影响**所有当前 token 位置**，再经后续层解码；do_sample=True, temp=.7, top_p=.9，max_new_tokens=50；执行后删除 hook。不修改权重。
- **代码差异/风险**：默认 ALPHA=20，不等于论文±40；SVD u的符号在数学上任意，代码未显式用 high-low 均值纠正正负号，所以“正alpha一定更字面”未由代码保证。每层 SVD basis 文件可能是 [H,1]，steer.py 未 flatten，而直接与 [B,T,H] 相加可能出现维度问题；forward hook 假设层 output 是 tuple，版本兼容性待核验。
- 解码是随机采样，代码未明确固定随机 seed，实验需要配对控制随机性与比较多档α。

## 08 创新贡献与证据边界
- 贡献是“layer probe→跨层低维几何分析→不训练的内部干预”一条链路，重点不是新的 Transformer 结构或隐晦有害内容检测算法。
- 论文提供干预与输出变化的证据，但**不能证明一维方向只表示具体性，更不能证明检测器必然因果使用该属性**。随机方向/正交方向、直接 DiffMean vs SVD、词频/词形/词类控制、控制强度和采样、解释语义保持评估不足。
- Probe可读性、投影可分性、干预可改变输出、下游安全能力提升是四类不同命题，不能混推。
- 即使方向在10次抽样中很稳定，也不能排除它稳定地编码词汇频率/风格/语义相关性。
- 论文正式版与当前GitHub代码的差异属于静态审计发现，并非已有训练复现或学术不端判定。

## 09 与博士研究的关联与竞争审计
- 广义隐晦信息检测可能需要从字面词义追踪隐喻/习语/转喻的语用含义；本文提供冻结模型 Probe/steering 工具，但没有任何直接 evidence 表明这一维轴能识别 implicit harm、dog whistle或图文组合恶意。
- 可与 P019 V-FLUTE 的修辞视觉蕴含、P027 ExPO-HM 的解释奖励训练、P034 CrossGuard 的组合模态安全评测进行机制比较，但**任务与标签不一致**，不能直接拼接多数据集做统一分类。
- 不将“把DiffMean+steering用于隐式仇恨”直接认定顶会新意，须先查现有 representation steering 及安全方法竞争工作。

## 10 低成本验证优先级
1. 无GPU：验证论文 global SVD 与公开 per-layer centered SVD 的向量差别、SVD符号、basis形状、脚本文件名/输入CSV/数据分割。
2. 冻结少量模型：prompt-last vs generated-score-token 的 Probe 对照；固定seed和数据，防止数字答案本身泄漏评分特征。
3. 同标注任务：global SVD、per-layer centered、raw DiffMean、random/orthogonal 在固定划分同预算下比 AUROC。
4. Steering：匹配随机方向、正负方向校正、多个α、固定采样/贪心、语义保真，验证强度-效应关系。
5. 此前均未本地运行；单卡16–20GiB应先做少量量化或低规模推理，不能把8B fp16权重占用≈16GiB当作全流程峰显存。

## 11 对今后精读的教学要求
- 先大框架“是什么/为什么”，再真实输入输出、张量维度、公式、代码对应，最后完整数值例子；不默认读者懂 DiffMean/SVD、decoder causal attention、forward hook或投影评分。
- 论文论述、代码事实、审稿推断分别标注。用户要求：如无法实际读取原始PDF，必须明确请求上传，不得凭摘要和印象进行详细精读。

## 12 定稿与后续
- 用户2026-10-31明确授权 P013 正式定稿合并，允许保留未闭合复现/因果疑点。
- 下一篇 **P022 Revisiting a Pain in the Neck: A Semantic Reasoning Benchmark for Language Models**（ACL 2026 Main，CCF-A），已定位并成功打开官方 24 页 PDF https://aclanthology.org/2026.acl-long.210.pdf；下一篇之后按 P035→P036 顺序继续。
