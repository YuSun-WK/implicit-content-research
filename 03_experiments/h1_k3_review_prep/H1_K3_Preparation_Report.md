# H1-K3 第一阶段准备报告

实际报告时间：2026-11-18T03:22:55.887528+00:00。分支按用户指定保留20261117命名；本次在服务器重启后于2026-11-18 UTC续作，未重新创建或清理旧工作。

最终准备状态：**PREPARED_FOR_HUMAN_REVIEW**。

真实人类审核状态：**HUMAN_REVIEW_PENDING**。真实人审记录0；投入门槛NOT_EVALUATED，不生成研究裁决或“门槛通过”。

## 基准与工作隔离

- 工作分支：experiments/h1-k3-review-prep-20261117。
- 独立worktree：/home/ubuntu/data/project/h1-k3-review-prep，父提交e6d80b030d43918ca502091717e9334aaab5b561。
- 已读取固定提交下README、Executive Decision、Kill Test Roadmap、Counterfactual Quality Audit、36对CSV及Result Independent Audit。
- 理解并沿用PIVOT：不预设风险表示衰减成立，输入条件任务定义有混杂，下一步先独立人审。K2 A6/B12/C18非盲助手筛查没有载入审核答案或审核者材料。
- 输入固定原始0a043abbf575d6b21f8d4095dbdfba7bad880465的36对Manifest和180条预测；源Git blob读取并交叉核验，不改旧实验工作树。原目录已有未提交修改未切换、清理或覆盖。

## 本轮实际交付

1. Reviewer A/B两套匿名包，每人72个单侧输入及36组配对，单侧顺序、配对顺序和左右方向可复现且两人不同。
2. 中立指南、全部空审核表、UI schema和导出JSON Schema；无预填判断、置信度、前提或提交时间。
3. 本地HTML/JS，无框架或外部网络依赖；显式提交时间、草稿暂存、JSON备份/恢复、CSV/JSON导出及第一阶段冻结。第二阶段不会改写第一阶段。
4. 原图取得/哈希/解码/来源/失败记录，匿名映射与随机种子、恢复说明和独立私有恢复ZIP。
5. 真实完整性/泄露检查程序、CPU单元与DOM交互测试、只服务单一匿名包的本地回环服务。
6. 人审结果汇总工具：未来检查遗漏、重复、格式、身份声明与版本；单侧与配对分开统计，保留U、原分歧、跨阶段变化和裁决链；完成真实人审后才关联GT及模型，原36对与审核支持子集并列，不自动启动GPU。

## 图片与匿名化检查

**72/72张原图片SHA256通过，72/72解码通过，72张均复用现有缓存，下载0张。** 原PNG字节、尺寸、格式保持；只复制为匿名文件名，未裁剪、压缩、重绘或改缓存名称。两审核者共144个资源文件逐一匹配原Manifest，第二阶段复用相同原字节。PNG元数据检查未发现附加元数据字段。

原36个pair_id、原文字（含尾随空格）、72侧完整且唯一，180条预测完整且唯一，图像路径/哈希交叉核验通过。匿名映射可逆且只在private；随机种子不嵌入HTML、JS或导出文件。完整原路径/哈希列表位于private/image_integrity.json与source_trace.json，不公开上传。原实验Manifest、预测、模型元数据及源图字节检查一致；本轮未写旧实验目录。

HTML/资源文件名/属性/数据/空表无原pair_id、category、侧别路径、GT、模型预测或筛查等级。检查按字段与上下文区分合法的Safe/Unsafe选项和匿名anonymous_pair_id，不以简单关键词误判。真实A/B空导出的216条记录也在内存检查，所有审核字段与提交时间为空，未创建真实人审答案。

匿名资源均为本地相对路径，connect-src none，无fetch/XHR/WebSocket/外链资源。HTTP实际请求验证匿名页面/图片可读，private、.git、路径穿越与任意结果文件不可读；测试后服务关闭。

## 检查结果与未验证项

- CPU单元/HTTP测试：15项PASS；保存—重建DOM—恢复—冻结—导出实际应用代码集成PASS。
- 第一阶段冻结后第二阶段修改不会影响第一阶段；两侧同类判断可提交；错误审核包草稿被拒绝；恢复篡改过的冻结状态被拒绝。
- 完整性/泄露/ZIP CRC/私有排除PASS；同种子再次生成的3个审核ZIP哈希完全一致，已有材料未覆盖。
- SYNTHETIC记录仅在tests/SYNTHETIC/generated，真实汇总默认拒绝；测试不假充人类。
- 无真实审核输入时汇总为HUMAN_REVIEW_PENDING，模型关联和门槛均未评价。
- **未做**真实浏览器视觉/跨浏览器file://存储策略认证。已用Node+jsdom核验DOM逻辑，不把其冒充完整浏览器验证；浏览器禁用localStorage时应导出JSON或使用仅本机HTTP。
- **未做**两位真实人类的独立审核、身份/独立性现实核验、标签有效性/因果认证及科学裁决。没有任何助手筛查或模型输出充当第二名人类。

## 使用路径与分发

准备根：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep`。

- A：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/packages/ReviewerA/index.html`
- B：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/packages/ReviewerB/index.html`
- 协调人总ZIP：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/artifacts/H1_K3_Review_Materials.zip`
- 单独ZIP：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/artifacts/H1_K3_ReviewerA.zip`、`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/artifacts/H1_K3_ReviewerB.zip`
- 私有映射/种子：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/private/registry.json`、`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/private/seeds.json`
- 私有恢复说明：`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/private/RECOVERY.md`、`/home/ubuntu/data/project/h1-k3-review-prep/03_experiments/h1_k3_review_prep/private/RESTORE_STEPS.md`

可将ZIP下载到本机，分别解压交给不同审核者，打开index.html。每人按单侧→冻结→配对的顺序完成。暂存限当前浏览器/包；关闭前导出draft备份，恢复选同包draft JSON。每人私下交回stage1与stage2各一份final JSON/CSV，保留原文件名、匿名ID及原版本，不把草稿当final。

若用本地服务，只运行serve_review.py指定ReviewerA或B，绑定127.0.0.1；不把仓库或private设为网站根。本轮无驻留服务。

匿名化仅减少意外泄露；重复原文、视觉记忆、查看本地阶段二资源或刻意检索公开数据仍可能关联样本，非加密盲法或强访问控制。来源许可未重新认证，图片默认仅本地授权审核，不公开重分发。

## 汇总与投入门槛

收到两位人类的四份完整final结果并由协调人确认独立性后才统计模型关联。软件报告原始一致率、U、分歧、左右映射对齐、原36对与审核支持子集并列。可信性仍由人类审阅，程序只列一致标签下的模型错误候选及计数。

一般诊断保持≥4个可信错误、≥2类且有明确人审理由（按单侧候选计数，另报独立pair数）；11例专门子问题保持≥6/11在请求风险目标下支持Unsafe且标签对比成立。均为投入门槛，不是显著性标准，即使未来计数达到也仅提供研究者下一阶段建议，不自动运行任何实验。当前两个条件均NOT_EVALUATED。

## Git边界

本次仅提交源码、模板、中立指南、schema、锁定的开发测试依赖清单和脱敏检查报告。packages、artifacts、private、results、测试生成记录与开发依赖目录均忽略；图片、真实人审结果和映射不上GitHub。不合并main。提交SHA在发布后单独提供，避免自引用。

本轮无GPU推理、训练、Qwen/模型下载、LoRA、Probe、隐藏状态干预、MMAligner或规模扩展。停止在审核准备完成，不替代人类科学判断。
