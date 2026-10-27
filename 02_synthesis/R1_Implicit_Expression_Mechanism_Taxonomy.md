# R1｜广义隐晦表达：概念与多维机制分类（定稿）

- 状态：2026-10-27 经用户确认定稿；属于**概念综合报告**，不是已验证的新语言理论。
- 依据：[P011 ACL 2025](https://aclanthology.org/2025.acl-long.425/)、[P023 ACL 2026](https://aclanthology.org/2026.acl-long.426/)、[P020 ACL 2025](https://aclanthology.org/2025.acl-long.1019/)；原文结论与下述研究者分类需区别。对应卡片见 01_literature/cards/。
- 目的：避免把机制、社会语言变体、交际策略和 ML 任务当作互斥类别。

## 1. 总体边界

**Implicit Meaning** 指直接断言之外依赖惯例或交际推理获得的信息；**Figurative Language** 指隐喻、反讽、夸张等多种修辞现象；**Coded Language** 在 P023 主要指有意构造的编码形式。这三者相互交叉，不互相等同。信息不透明 ≠ 故意隐藏 ≠ 有害。Context-dependent Meaning 包括指示词与语境消歧，未必属于隐含命题。

## 2. 概念表（研究层级不可混用）

| 概念 | 定义与核心机制 | 主要归属 |
|---|---|---|
| Implicit Meaning | 未直接断言但依赖语境、常规含义或推理获得的内容 | 意义属性 |
| Figurative Language | 隐喻、反讽、夸张等修辞表达集合 | 现象集合 |
| Metaphor | 源域—目标域的选择性概念映射；已惯例化隐喻未必每次需要主动推理 | 语义机制 |
| Irony / Sarcasm | 表达与立场、评价、预期之间的反差；sarcasm 更常带挖苦/评价目标 | 语用/修辞机制 |
| Euphemism | 以缓和的替代表达涉及敏感主题；未必刻意隐藏 | 词汇/社会语用 |
| Indirect Speech Acts | 句子形式与主要交际行动不同，如能力问句用于请求 | 语用机制 |
| Presupposition | 将某信息作为背景前提；预设可投射、亦受语境制约，不自动是真实事实 | 语义/语用 |
| Implicature | 通过交际惯例/推理理解未直接断言的信息；会话含义通常可撤销 | 语用机制 |
| Coded Language | 表达形式或内容与被编码对象存在转换或约定映射；P023 对故意编码采取操作性定义 | 编码现象 |
| Dogwhistle | 对不同受众存在差异化解释或效果；不一定存在显式谐音代码或有害内容 | 受众定向交际 |
| Coded Hate | 编码表达承载仇恨、贬损或针对群体的敌意；与 dogwhistle 不同义 | 内容+编码属性 |
| Slang | 社群内非正式词汇/惯常用法；可能逐渐词汇化 | 社会词汇变体 |
| Meme | 模板、互文和传播变体构成的文化表达；可携带反讽/编码 | 文化传播形式 |
| Dialect | 地域/社会群体的系统性语言变体；不是天生编码 | 社会语言变体 |
| Context-dependent Meaning | 指称、词义、交际解释取决于语境 | 解释属性 |
| Deliberate Obfuscation | 主动降低特定受众或检测系统可识别性的策略；仅凭异常词形无法证明动机 | 意图/交际策略 |

## 3. 多维编码本体（研究者提出；不是三篇论文的联合标签）

- **D1 Surface Encoding**：音系、字形、拼音、Emoji、跨语言或约定代码映射。
- **D2 Semantic Transformation**：概念映射、词义延伸、惯用意义。
- **D3 Pragmatic Inference**：反讽、含义、预设、言语行为及语境立场。
- **D4 Socio-cultural Grounding**：文化、方言、平台及社群共享知识（主要是解释条件，不一定是转换算子）。
- **D5 Communicative Strategy**：礼貌、嘲讽、受众定向、规避等功能和目的；实际心理动机通常不可直接观察。
- **D6 Conventionality & Dynamics**：临时创造、社群惯例、词汇化、共时多义和历时语义变化。
- **D7 Task & Ground Truth**：检测、分类、解码、意图和有害性等预测目标；不是语言产生机制。

D1–D6 非独立因果变量，既可以叠加，也可以互为条件。D7 必须与语言机制分离。

## 4. 两种 Strategy 的关系

- **P023 Encoding Strategy**：七个操作性类别——Ambiguous Homophone（合法词组谐音，如“炒鸡→超级”）、Non-Lexical Homophone（非规范词形谐音，如“灰常→非常”）、Phonetic Substitution、Emoji Substitution、Orthographic Substitution、Cross-Lingual Phonetic Encoding、Cipher。主要属于 D1；多步骤表达可叠加机制。P023 Cipher 并非均有独立可靠解码。
- **P020 Rhetorical Strategy**：在语境下，话语与目标意义相容的修辞关系，如 irony、hyperbole、understatement、pragmatic halo 及 literal 控制条件；主要关联 D2/D3，并受 D5 调节。
- 关系：形式编码不等于修辞意义变化；编码后的表达可以被反讽使用，隐喻也可逐渐固化为社群代码。不存在必须“先编码后修辞”或相反的全局顺序。

## 5. 实例诊断（分析示例，非论文原始样本）

1. “这家店炒鸡好吃”：谐音 D1，亦可能属于惯例化网络表达 D6；不能据此断言故意规避。
2. 代码崩溃时说“真棒”：主要为 D3 反讽；不要求恢复编码原词。
3. “他是团队的发动机”：D2 隐喻的概念映射；非字形/音系编码。
4. 失控时发送“This is fine”表情包：D4 Meme 知识+D3 可能的反讽，不必是 D1。
5. “他又迟到了”：预设存在先前迟到，不代表该背景已被现实核实。
6. “俺明儿去”：语言变体与指称语境，不可单凭方言判为 coded。

## 6. 已有证据、研究推断与争议

- **原文支持**：P011 将语用现象与评测任务区分；P023 的七类是面向中文编码评论的操作性分类；P020 将修辞策略作为意义推断条件。
- **研究者综合**：D1–D7 分类、机制共存的组织方式，尚未对跨现象数据集验证其可标注性与独立性。
- **争议/待核验**：Irony 与 Sarcasm 的标签外延；Dogwhistle 是否需双重可意识到的意义；Slang 与刻意编码的边界；P023 Cipher 的解码状态；真正心理意图是否可复核。

**移交 R2：** 比较论文的方法、数据及实验时，必须记录相同名词在不同论文的操作定义，不能跨任务直接比较分数。
