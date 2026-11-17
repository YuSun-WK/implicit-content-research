# K-DIR readiness：CPU交付入口

先读00结论。当前数据门未过；没有32组、没有冻结split，也没有本轮GPU预测。

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
