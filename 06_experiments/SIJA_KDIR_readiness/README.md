# K-DIR readiness：CPU交付入口

最新先读07内容验收：ACCESS_REQUIRED；00保留RN2历史数据门结论。当前数据门未过；没有32组、没有冻结split，也没有本轮GPU预测。

- `02_Candidate_Group_Manifest.csv`：4份匿名资料的可用性，不是合格四格组。
- `templates/review_template.html`与`scripts/build_review_pack.py`：用合法私有dossiers及图片构建第一阶段离线HTML，检查asset hash，拒绝预测字段。
- `review_schema.json`及`templates/group_template.json`：后续双人审定完整组的记录规格。HTML导出为单人答复，应在独立二审/分歧处理后人工整合为组记录；不会自动把REVIEWED变HUMAN_VERIFIED。
- `scripts/kdir_core.py`：完整manifest/恢复键、白名单、严格四状态解析、组级指标和组bootstrap。只提供CPU准备，不加载模型。
- `scripts/validate_freeze.py --groups 私有组记录.json --output 私有freeze.json`：强制8+24、独立审核/无争议/文件哈希和泄漏隔离；资料未通过则拒绝冻结。
- `scripts/build_stage2.py`：冻结后才可单独生成带预测的第二阶段页面，第一阶段不得提前显示模型答案。
- `python scripts/check_cpu.py`：CPU合成边界检查，非安全实验。

前瞻恢复示例：先build_manifest获得canonical manifest与hash，把整个manifest写入私有日志；仅当同hash的execution_status=COMPLETED记录存在时跳过。同键重复完成应报错，换图片顺序/字节、模型revision、policy/prompt/processor/解码配置不得跳过。已完成INVALID也不应自动重采；重试需新attempt标识并保留旧结果。未知执行后端/processor实际版本应阻止运行冻结，而非填写“latest”。

配置共4个CP条件及独立作者政策提示；全为本轮NOT_RUN。旧75的双尖括号、状态字符串与分数保留在原提交；本目录仅澄清并版本化后续设计。指标按冻结condition/run manifest分组计算，不混不同模型输出。

本地私有审核包路径与填写方法见03，Git中不含图片/全文模型输出/私有标注。最终交付链接另在会话中提供，避免公开绝对私有路径。

RN3新增：check_rn3.py执行50个反例、旧布尔缺陷回归、schema/指标/冻结及python -O检查；需要已有jsonschema及FormatChecker。check_review_storage.js仅是Node状态测试，不冒充浏览器点击。review_storage.js必须与index.html同目录（build_review_pack.py自动复制）。旧无fingerprint答复不自动迁移。

冻结字段迁移：新增er_instruction_origin、er_log_reference、er_on_Is_evidence、remaining_violations_evidence，拒绝字符串布尔及无效时间。作者执行轨道的来源必须AUTHOR_EXECUTION_LOG；RESEARCHER_DRAFT要另拟协议，不能补个标记就自动进入旧实验。程序仅验证供给记录，不认证审核者/标签真实。SafeEdit_Content_Acceptance.csv本轮0行真实验收。
