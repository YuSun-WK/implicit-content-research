# Repair Log · PASS

A 为论文设计，B 为固定作者代码，C 为面向论文调用链的修复，D 为本地执行和评测协议。表中的落点是隔离实现或后续适配器要求。B 快照的来源 SHA 见 [sources.json](sources.json)，本表与代码的变更 SHA 可由 `git log -1 -- repair_log.md` 查询。轨迹中的 `call_id` 在单次尝试内编号。

| ID · B 源位置 | 可重现问题或差异 | 落点及方法影响 | 验证 / 状态 |
|---|---|---|---|
| R01 · multiagent L14；data L11；inference L7 | 多 Agent 无法编译，基础导入链也会触发 | C 使用独立 `pipeline.py` 入口。角色提示由 AST 读取官方常量。 | 原版编译和隔离导入，Mock 管线通过 |
| R02 · multiagent L8 | 包上下文找不到 `prompts` | C 从固定路径读取 SHA256 校验后的常量。 | 只修原缩进后复现缺模块，新管线测试通过 |
| R03 · multiagent L11–30、L65–71 | 缺 `model`/图像绑定，记录还可能沿用上一个 Chat 图像变量 | C 单个模型实例注入，每次处理单个 manifest 输入，两侧独立绑定路径。 | 隔离执行复现三个 NameError，Embodied Mock 核对两步各自用图 |
| R04 · multiagent L40–44；prompts L65–67 | Intent 输出未进 Safety，原版 Intent 还收到图 | C Intent 仅接 query，Safety 接解析活动与对应 image。 | Chat trace 1→3，四个互异探针 |
| R05 · multiagent L40–47；prompts L64–78 | 无 Visual Agent 和 Caption 传播 | C 增加 A.7 Caption 文本，把返回字符串传进 Safety；附加字段名 `Image caption:` 为本地渲染选择。 | Chat trace 2→3 |
| R06 · multiagent L11–18、L46–50；prompts L69–73 | QA 用裸 query，分支模板与判定丢失，保存的只是 IF 模板 | C 严格解析单一 Yes/No；A.7 B/C 分支追加原判断，A 走普通问答提示。精确 `None` 走 B，其他无效输出走 C；记录 invalid。 | Chat trace 3→4；验证四种路由 |
| R07 · multiagent L21–28 | unsafe 定位用 safe 图，第二步能收到该错误状态 | C 两步复用本输入图；把解析的定位输出写入 Safety Reasoning。 | 隔离原函数和 Embodied trace 1→2 |
| R08 · multiagent L57–59、L75–80；data L61–62、L98–101 | 输出路径建错类型、直接覆盖以及可选参数仍必需 | D SQLite 逐调用提交，持久化失败与重试。一次处理一个输入。 | 原版 IsADirectoryError/TypeError、续跑及单写者测试 |
| R09 · inference L26、L34；prompts L45–62 | CoT/Multi-Agent 无入口；数据文件名差一个字母 | C 显式切换方法，使用固定 SHA 的 `combined.json`。 | 一步 Base/CoT 入口与数据展开已运行 |
| R10 · data L34–46、L69–86 | 单边 Chat GT 描述、无 Self Caption、Embodied 实际两侧文本可能不同，zip 可截断 | C 记录两侧索引和文本哈希并强制列表等长。Caption/GT 诊断在矩阵列为后续独立配置。 | 数据脚本、非法输入测试；Caption 诊断待实现 |
| R11 · data L101；gpt4_eval L1–23、L96–196 | 顶层 Azure 依赖，所有方法统一调用回答 Judge，异常丢整对 | C/D 标签及行为分流。保留发布聚合规则；本地 Judge 为独立 D 协议。 | 缺包实证及 CPU 评分测试；Judge 未运行 |
| R12 · 各模型适配器，见源码矩阵 | 导入副作用、版本未锁、依赖网络和设备，LLaVA 图像预处理不统一 | D 适配器在后续独立实现；先明确原版 224 路径、精度和缓存约束。 | 静态与环境记录；完整适配器待实现 |

缺失或重复的 Intent/环境状态会停止本输入，避免传递空值。该无效输出处理策略由本轮实现定义。见 [Mock 输入输出](logs/mock_trace.jsonl)。
