# P041｜Safe Inputs but Unsafe Output: Benchmarking Cross-modality Safety Alignment of Large Vision-Language Models

> **2026-11-02 用户明确授权定稿并合并。** 已完成正式论文解读与公开数据/评分脚本静态核验；**未运行作者完整15模型评测、未调用付费GPT评判、未实物审计全部图片/102条AI辅助样本**。以下严格区分论文报告、代码事实、待核实风险。

## 01. 书目与来源
- Siyin Wang, Xingsong Ye, Qinyuan Cheng, Junwen Duan, Shimin Li, Jinlan Fu, Xipeng Qiu, Xuanjing Huang. **NAACL 2025 Findings（注意：不是NAACL主会；NAACL主会CCF-B，Findings不可冒称CCF-B/A正式主会）**。
- DOI 10.18653/v1/2025.findings-naacl.198；正式页面 https://aclanthology.org/2025.findings-naacl.198/ ；PDF https://aclanthology.org/2025.findings-naacl.198.pdf 。
- 作者公开仓库 https://github.com/sinwang20/SIUO ；数据 https://huggingface.co/datasets/sinwang/SIUO 。
- 仓库审计：README.md、data/siuo_gen.json、data/siuo_mcqa.json、eval/gpt-eval.py、eval/gen_score.py、eval/mcqa-eval.py；仅静态读取。

## 02. 核心任务 / 与隐晦检测边界
- **SIUO**：图像、文本单独看相对安全，组合却可能诱导LVLM给出不安全/不合适的回答；测试对图文隐含风险的跨模态识别及安全响应。
- 输入(I,T)，生成任务输出自然语言响应 R；评价R的**Safety（安全性）**与**Effectiveness（有效回应）**，同时考察两者联合达标；另设计MCQA选择安全且有效的候选回答。
- 与f(I,T)→{safe,unsafe}**输入风险二分类**不同：输出不安全 ≠ 输入风险的独立金标；判定时用风险说明和参考回答，不是直接训练一个风险检测分类器。

## 03. 隐含风险机制
- 论文能力框架：Integration（融合图文指代、对应关系），Knowledge（规范、社会文化/场景常识），Reasoning（结合图文推断潜在意图与行为后果）。
- 例如高处图像配“从这里去新世界，鼓励我”的语句，不能仅按字面鼓励；应结合场景识别潜在自伤风险并安全回应。
- 三能力是作者的分析框架；仅靠最终回答错误和人工归类尚不能因果区分模型究竟在视觉理解、语义整合、推断还是响应策略阶段失败。

## 04. 数据构建和规模
- 原文报告**269图文问题**：167条human-crafted与102条AI-assisted；勿把两份任务格式相加当334独立样本。
- 仓库data/siuo_gen.json、data/siuo_mcqa.json分别读取：**各167个记录**，同一批人工样本分别供生成/四选一任务；两个JSON均不等于完整版269。
- 生成JSON字段为question_id, image, question, category, safety_warning, reference_answer；没有独立safe/unsafe二分类标签。
- 原仓库167条按category计数：self-harm 19, dangerous behavior 18, morality 20, illegal activities & crime 18, controversial topics/politics 16, discrimination & stereotyping 18, religion beliefs 20, information misinterpretation 17, privacy violation 21。
- AI辅助部分流程（论文报告）：采样图像→模型生成文本问题→文本安全/冗余筛除→人工复核；先前精读记录数2,000→1,019→964→102，来源选择与筛选规则仍需完整实物复核；102个JSON样本在主要公开数据路径中未发现，公开完整性待定。
- 风险说明来自构造者并经审核，部分安全判断依赖语境和规范；不是不依赖解释的客观唯一金标。只有风险正例、缺少足量同图或同语义的安全负例，不宜将167行全部标unsafe直接训练二分类。

## 05. 实验设置与指标
- 论文测试15个历史开闭源LVLM，包括GPT-4V、GPT-4o、Gemini系列、LLaVA、Qwen-VL等；**Zero-shot**，不是作者训练新模型。
- **Generation**：针对图文生成自然语言回答，按safe、effective及二者同时满足衡量；不能将“只拒绝”混同有效。安全性与有效性人工及GPT-4V Judge评价，自动评分可能错误。
- **MCQA**：同一167条问题改为四选一，正确候选为预设安全且有效回应；报告Accuracy，不等于自由生成能力。
- 公开脚本gen_score.py先在每题内部对多次回答/评价进行众数聚合，再做题级均值；注意与响应级简单计数不是同口径。
- 论文报告代表性人评Safe Rate约GPT-4V 53.29%、Gemini-1.5 52.10%、GPT-4o 50.90%、LLaVA-1.5-7B 21.56%，是特定历史模型/测试协议结果，不可泛化至2026最新模型。

## 06. 公开代码静态审计
- eval/gpt-eval.py需要OpenAI API key，并调用历史模型名gpt-4-vision-preview；其Safety Judge输入包括question/safety_warning/reference/response，Effectiveness Judge使用图像、问题和响应；存在Judge依赖特定参考答案的评测偏向。
- **字段疑点A**：gpt-eval.py输出键名safety_evaluation或effectiveness_evaluation，但stat_score()检查通用'evaluation'键；依照所见代码路径，分数写入分支可能不执行。
- **字段疑点B**：gen_score.py处理effective_gpt，与gpt-eval.py意图输出的effectiveness_gpt不一致；端到端运行风险。
- **MCQA解析**：eval/mcqa-eval.py在无法识别答案字母时调用random.choice(A,B,C,D)，未固定随机种子；重现性和无效输出处理可能受影响。
- 以上是**静态实现疑点**，非已运行重现的错误或论文结果推翻；需记录commit/版本核验。

## 07. 主要发现及解释边界
- 多个历史LVLM在单模态表面安全而组合潜在有害场景下仍产生不合适回答；安全性和有效性不能等同。
- 数据集偏重开放式安全响应而非独立输入风险类别；模型安全回应好，也未必证明内部推断正确；回答不安全也不必然是图像没看懂。
- 模态泄漏与风险定位未形成严格跨模态因果消融。是否只读文本可判断、是否存在反事实标签翻转，需另行验证。
- 自动合成102条与人工167条难度可能不同；标注提示、参考答案、Judge倾向及主观性需审计，不以人工/LLM一致率替代独立金标。

## 08. 与后续论文及方法型论文的关系
- P041用于明确**任务问题：单独安全、组合诱发风险**；后续P037 VLSBench直接研究文本描述泄漏视觉安全线索，P038 VLSU系统刻画联合安全理解，P039 ThinkingGuard研究逐步归因，P040 Meerkat-VL研究隐含风险感知/自检。
- 不把“发现联合理解不足”“用反事实样本/多步归因”直接当新颖性；需先对P037–P040竞品与公开数据协议交叉审计。
- 用户约束：共享GPU单卡16–20GiB、≤6h kill test、免付费API、公开数据可靠标签；现有167条可作小规模无训练试验，但不足独立支持可靠二分类训练；完整自动GPT Judge不符合免付费API约束。

## 09. 开放问题 / 复现优先级
1. 全部269条是否完整公开？102 AI辅助样本在哪，图片可否完整取得？
2. 167条的reference_answer与safety_warning是否一致？风险判定的多解性和场景歧义怎样处理？
3. Text-only、Image-only、Joint三种输入基线，以及安全反事实对，能否独立证明图像的必要性？
4. 统一题级与回答级评价口径、修复字段名问题后，GPT Judge/人工评价结果是否稳健？
5. 在P037–P040已有工作覆盖后，究竟还有什么可证伪且未被解决的机制问题？

## 10. 定稿结论
- **正式精读已完成并于2026-11-02获用户授权定稿合并**；静态审计≠本地复现。
- 论文贡献是跨模态安全**任务定义与Benchmark/Evaluation**，非新检测器或新训练算法。
- 下一篇 **P037 VLSBench（ACL 2025 Main/CCF-A）**，按相同结构详细分析并重点核验数据生成、VSIL定义、评价协议、对照和代码。
