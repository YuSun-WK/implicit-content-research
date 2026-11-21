# SIJA-RN3：SafeEditBench 内容验收与指令溯源

执行日期2026-11-18 UTC。**最终状态：ACCESS_REQUIRED。** 当前不能报告PAIR_DATA_UNSUITABLE、CANDIDATES_PENDING_REVIEW或ORIGINAL_TRIPLES_AVAILABLE，因为真实SafeEditBench图像对取得0、原始指令取得0、内容验收0。合格四格组和人工核验均仍0，K-DIR未运行，TGSV仍NO-GO。

## 1. 固定证据与访问结果

PR77固定afe2ea86b949805fc26debd58e44bd19de80e537，执行前/重启后刷新均无新提交；本地文件树与该提交相同后追加修改。读取其结论/候选CSV/访问日志/审核模板/core/冻结/CPU测试；PR76固定4bb68ea…的00/04/05/07/08/10六份报告亦已读。main仍985901a…；仓库递归树与工作区祖先未发现AGENTS.md。本轮不修改历史FA2输出、解析或分数。

目标固定revision `a254fa5ea367839be72e8db39041a7a5a43633c1`。[官方数据页](https://huggingface.co/datasets/tyodd/SafeEditBench)仍要求登录并同意账户信息共享后访问内容。本地官方客户端未发现已配置登录；不读取/输出Token内容，不代用户同意条件。

只尝试同一小型schema parquet两次，关闭库级自动重试。分别ReadTimeout 8.142s、ConnectionError 6.923s；无可解释的HTTP401/403。因此**传输结果是NETWORK_INCONCLUSIVE，不是服务器明确拒绝授权**。总体ACCESS_REQUIRED来自“无已配置合法登录+页面gating”，不是由超时推导。请求总计约15.1s，远低于30分钟上限；不再反复探测。

用户需自行在上述数据页登录目标账户、审阅并接受访问条件，再在服务器合法配置该账户的HF登录。不要在会话粘贴凭据。仅有网络可达不能证明gating授权；本轮未改代理、sing-box或隧道。

保留`logs/rn3_access.json`。新增受限文件/图片字节0；未下载任何权重、未启动GPU/训练/生成或付费API。

## 2. 原始指令追踪

固定官方仓库commit `a21cdfe3cc2a8932ccd9ae72a1cb02220acb0025`，[safe_edit.py](https://github.com/adorableChowhound/SafeGuard-VL/blob/a21cdfe3cc2a8932ccd9ae72a1cb02220acb0025/data/safe_edit/safe_edit.py)实际已读，blob=77ecb538…；字节hash与函数定位见`logs/rn3_instruction_trace.json`。

- `process_single` L102–133：unsafe成功分支记录image/safety/edit_instruction/edited；safe或error分支没有edit_instruction。因此不是每条results记录都必有指令。
- `main` L136–176：在output_dir写results.jsonl。该脚本是定义，不是已取得的执行日志；本轮未执行。
- 输出路径为`{stem}_safe.png`，而发布说明使用`x_edited.jpg`。可能涉及命名/重编码，但没有可靠映射，不能据相似文件名认定执行来源。
- 脚本可在edited文件已存在时跳过实际编辑，仍重新生成安全评估文本；所以即便取得日志，也需核查该文本与该次图片是否真实对应。它不保存每对的图像hash、API版本或完整执行配置；结果文件以写模式打开，亦需关注运行版本。

查找范围：官方main递归目录的13个blob名称/大小、实际脚本与README资源链接、固定HF文件目录997项和公开schema、当前项目自己的私有缓存/`results.jsonl`文件名。公开main无results.jsonl或数据对；固定HF目录未发现results/instruction文件。公开schema声明只有image/image_path/safety_label/policy_name/policy，**不是原始编辑指令**。受限test.jsonl未取得，不能断言其真实内容没有额外字段。未在自有缓存找到对应作者日志；FA2模型输出不算作者日志。以上是范围内“未找到”，不声称永久不存在。

## 3. 证据等级与验收边界

| 级别 | 含义 | 本轮实际取得 | 可用于什么 |
|---|---|---:|---|
| A AUTHOR_EXECUTION_LOG | 作者原始执行指令+日志+可靠图片映射 | 0条 | 原始三元组追溯仍不可做 |
| B SOURCE_PAIR_LABEL | 来源提供图像对/政策标签 | 内容0对；只有公开目录/schema | 不能把601政策实例算601独立对，或直接贴CP标签 |
| C RESEARCHER_DRAFT | 针对已查看真实图对新设计诊断er/en | 0条 | 未来须独立审核、单独修订协议；不冒充作者执行或效果监督 |
| D CODEX_DRAFT / MODEL_DRAFT | Codex/模型观察或建议 | 仅可用性判断 | 不等于HUMAN_VERIFIED |

尚无可看SafeEdit图片，故不凭空起草er/en，也不能判哪些对确有风险移除。L1–L5是不同政策，不能搬用其标签作CP-v1金标。脚本的宽泛安全评估提示也不是CP-v1；即使之后取得A级日志，仍须独立重审其操作是否移除CP-v1目标风险。任何实际验收须逐对检查配对/事实改变/其它变化/残留违规/歧义/er在Is的语义。

`SafeEdit_Content_Acceptance.csv`仅表头、真实验收行0；这是未执行，不是零失败实验。`logs/rn3_selection_plan.json`预先按数值stem升序列最多8个检索项，来源目录有62个同名对，只用于检索计划。无图像hash/解码结果的目录项不是已取得图对。授权后先读取小文件去重政策记录，再取该固定顺序，不按预测挑样。

缺日志的[作者询问信草稿](templates/Author_Data_Inquiry_Draft.md)已交付，仅询问已有results、指令和图片映射，**没有发送**。

## 4. 两项审核修复与验证

**准入类型/证据：** `qualification_errors()`统一供eligible/组指标/冻结入口使用。布尔必须是真正bool且明确True，拒绝字符串"false"、数字等；要求非空指令/风险/政策/四格后果、图像路径与字节hash、Is上可执行依据、残留违规依据。审核者需两个不同非空编号，每人有有效RFC3339时间及timezone，不接受伪日期/未来时间；分歧处理需显式True。schema与冻结共享这些结构和语义约束，JSON Schema使用FormatChecker；跨字段时间数量与未来时间还由同一核心函数校验。

为防新设计诊断指令混入原始执行轨道，新增er_instruction_origin/er_log_reference；RN2原始轨道只有AUTHOR_EXECUTION_LOG可准入，RESEARCHER_DRAFT不能因补齐字段就通过。若日后采用C级诊断路线，须另立明确修订，不放松此门。旧记录要补证据后迁移；不是重写旧审核/结果。冻结入口改为显式ValueError，python -O不能移除检查。

程序只验证“所提供记录是否完整一致”，**不能证明真实发生人工审核或标签真实正确**。本轮测试中HUMAN_VERIFIED只是CPU合成元数据，真实人工核验仍0。

**盲审隔离：** 不再自动读取package_id旧存储；按审核者+资料fingerprint+政策hash隔离。更换编号清空当前表，只有主动加载才读取该编号；提供干净副本、仅删除本审核者草稿，以及导出后主动导入同编号JSON。跨审核者/政策/资料导入拒绝。旧全局草稿不会自动迁移。

50条有意义反例通过eligible/schema/组指标；同时检查完整合成正例及冻结入口、python -O拒绝伪布尔。Node测试保存、重新创建会话不自动加载、第二审核者看不到首评、JSON导出读回、错误编号导入拒绝、定向清空。环境无浏览器可操作，**实际填写/按钮点击/下载交互测试NOT_RUN**，不能用Node状态测试冒充。日志见rn3_validation_checks/rn3_storage_checks。

## 5. 私有包、竞争登记与决策

复用RN2同一框架和私有资料，生成`KDIR_RN3_isolated_review_pack.zip`修正版。仍为旧4份MagicBrush普通资料/6图，不含新的SafeEditBench候选，也不要求用户重复审核这些资料来延长研究。该包用于隔离修复后的操作核查；不要用旧RN2 zip作独立盲审。当前没有SafeEdit内容需要签核，先解决合法访问和原始日志。

[MMAligner](https://arxiv.org/abs/2608.05909)已登记为直接竞争与后续表征校准对照：作者提出将多模态表示校准到既有拒绝区域，含下界/上界及良性保持；本轮仅核一手摘要/元数据，未训练或复现。arXiv comments标注将发表于CCS2026，不冒充本轮已独立核实正式出版。它不能替代编辑方向金标，也不能用拒绝率替代GAcc；具体对照待数据门后确定。

**当前不值得继续凑32组或继续无数据的准备轮次。暂停这条操作效果主路线的新增投入。** 这不是图对不适用的内容结论或机制NO-GO：若用户完成合法访问且作者提供已有日志/映射，再做最多8对真实验收；若只有B级图对，另评C级诊断路线，不能宣传原始操作效果监督。只有出现真实可审核候选后才估计能否扩到8+24和二审成本；目前无依据线性保证62个文件名对可产32组合格数据。
