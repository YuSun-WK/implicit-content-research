# Stage 1 独立复审与恢复建议（2026-11-19）

## 当前裁决

**Stage 1 = PARTIAL / CPU_PREFLIGHT_DONE / GPU_NOT_RUN。** 对照最新提交 `bae960ea79b417eec2ce67c11b3488db0ab8986a` 的 `STAGE1_EXECUTION_REPORT.md`、`artifacts/manifests/data_validation.json`、`runs/cpu_preflight/transfer_and_gate_status.json` 和源码。此文件是**只读审计与下一阶段指令**，不是新推理结果。尚无新的 A0 五阶段正式 GPU 预测；历史 K1 180 条统一协议输出保留。

### 已完成并有证据的事项

- HF HEAD dataset `3ac26e778db94a282711f463f22ba6db99643bee`、model `76892f9768ce828268265171f4bbc5dfb75eafc3` 均与旧实验一致；论文 arXiv v1 PDF、TeX 和作者仓库固定快照；ACM supplement HTTP403所以 NOT_VERIFIED。
- 36 CSV 和全量 5600 条结构核验；Test 868 对/1736 条 Manifest 完成。图像累计297张经官方 LFS SHA256+PIL确认，分布：EV114/35 ready pairs、IA125/39、MIS10/4、OFF8/4、PH8/4、PRI8/4、PD8/4、RB8/4、VIO8/4；合计**102 个完整可用对**（不是独立代表性样本），剩余1439张未就绪。其中从历史缓存复用72张、本轮新增225张。
- 模型四分片、750个tensor、处理器与本地118处索引修复证据通过；v3 parser冻结；29项CPU测试通过。旧v2原文重放2/4唯一判定、2/4双标签模板INVALID，符合原始事实。旧219个Git blob受保护。
- 关键文件：`artifacts/model_cache_audit.json`、`artifacts/parser_freeze.json`、`runs/cpu_preflight/pytest.log`、`artifacts/manifests/leakage_audit.json`。模型目录存在并不表示新GPU已加载。

### 阻塞的准确性质

- 1,439张尚未就绪：`DOWNLOAD_FAILED=207`、`MISSING=1,232`。**不能说全部1,439张下载均失败：1,232张尚未尝试或没有有效传输尝试记录。**
- 首轮缺图约1664张；48/1664→432/1664之间受网络重置/超时影响，在连续48张0成功后停止。定额续传再试48张，仅3张成功。curl error主要28（timeout），另外35/16；直连、镜像和两个旧路由探测未成功。这是有时间界限的网络阻塞，并非数据集下架或权重缺失。
- `preflight.json` 只有 `data=false`，其余manifest/queues/parser/prompt/model均true；GPU Smoke、独立验证、100对Pilot一律NOT_RUN。新推理 P50/P95与显存峰没有实测。

## 必须先修复的工程问题（源码级发现）

### P0-A：过度严格的全局数据门槛阻止分阶段评测

`scripts/run_resumeable_inference.py`：
`"data": validation["gpu_data_gate"] and all(entries[uid]["run_status"] == "READY" for uid in ordered)`

当前 `gpu_data_gate` 只有1736张全部READY时才true，因此即使本轮6条Smoke或200条Pilot所需图都齐全也无法运行。这违反了阶段式下载/运行意图。应将Stage的 `data_gate` 按冻结队列中每条是否READY、图片是否官方哈希校验、成对结构是否满足要求计算；另保留 `global_test_complete` 为独立字段，**只有正式Full Test需要全局完整**。不可为放行而忽略缺图或改换冻结样本；队列缺图要先优先补齐原冻结队列。所有原始Manifest、已有SHA与全Test总分母仍保留。加单测：Full不全而Smoke队列完备→可以过Stage门槛；Smoke队列缺1张→阻止Smoke；Full Test→仍必须1736/1736就绪。

### P0-B：本地PID直接匹配host PID，历史环境已证实不适配

`run_resumeable_inference.py` 的 `audit_resource()` 用 `str(os.getpid())` 与 `nvidia-smi --query-compute-apps=...pid...`直接匹配。H1-K1 `H1_K1_FORMAL_EXPERIMENT_REVIEW.md` 已实测容器 PID 150837 / host PID 4102338，直接匹配会返回null并在45秒后监控强制退出。必须参考 H1-K1 经过验证的唯一新增宿主PID绑定/可逆显存挑战；不允许以null冒充0、不允许kill他人、不允许直接关监控绕过问题。增加 mock 单测: 容器pid≠hostpid时能正确监控，绑定失败拒绝启动，已有他人PID时拒绝运行。记录进程峰和整卡峰区别。

### P1-A：阶段门槛路径与run-id参数不一致

`run_resumeable_inference.py` 接受任意 `--run-id`，但先验门槛硬编码读取 `runs/smoke/summary.json`、`runs/validation/summary.json`，并要求 `run_id=smoke`/`validation`。若Stage1实际命名 `smoke_日期` 或 `validation_日期`，后续阶段会错误认为门槛未通过。二选一：明文强制固定run-id并全程文档声明；或建立 `stage_registry.json` 以配置身份和冻结SHA定位有效前序run。建议后者且必须防止混版本。加入回归测试。

### P1-B：优先补齐冻结队列、再补全Test

`artifacts/sample_queues.json` 已固定 Smoke6条、Validation36条（18对）、Pilot200条（100对），并排除旧36对。优先从缺图名单按冻结队列 `smoke → validation → pilot` 下载（不修改抽样顺序、不挑成绩好案例），然后后台时段/网络窗口分批补齐其余Test。保留每个文件官方LFS SHA、成功与失败原因、每批下载耗时；不要破坏已有297张，也不要反复对1,232张未尝试项写成失败。建议将 `curl` 并发12降至2–4做压力比较，尝试有界指数退避、range续传和现有huggingface_hub（如果隔离环境已安装），并以成功文件的SHA而非HTTP 200作为成功判定；不能无证据认定某镜像可信或改模型来源。

### P1-C：工程诊断Smoke可以用现有102完整对，但不得充当独立验证

如正式冻结Smoke所需图片暂不能获得，可从现有完整对中另冻结 `diagnostic_smoke_ready_v1`，用于**验证模型加载、显存、解析格式、吞吐**；保留来源说明、是否与旧36对重叠、prompt/parser/config SHA。不得用该预观察、可用性偏差的队列代替A0正式预注册验证或Test全量统计；不得改旧Frozen Validation的36行要求。并须将诊断运行与正式Stage先验门槛区别记录。优先还是补齐原定Smoke6条。

## 研究验收边界

- H1-K2判断仍是PIVOT、H1-K3真实人工审查仍为0；本复现任务不因此取消，但不能把全测试模型漏检自动解释为融合作用失效、因果Pair有效或证明DPO贡献。
- Test全覆盖的目标仍是1736条、868对；本轮先尽快收集真实新A0输出、验证 `A0` 是否重现 `[Safe]/[Unsafe]` 模板歧义。A0冻结解析成功率<95%时保留FAILED_PARSE_GATE，不事后放宽；必要时独立注册A1。
- 29个CPU测试仅覆盖部分路径，没有GPU监控跨命名空间和阶段门槛回归测试。**CPU测试全部通过 ≠ 运行脚本已获正式GPU授权。**
- 分支本轮没有commit旧预测改动；为实现上述修复只能在 `06_experiments/repro_thinkingguard_full/` 新建受控后续版本，并清楚记录原先freeze的SHA变更及更新原因。

## 按顺序的Next Gate

1. **修复P0-A/P0-B并加回归测试**（CPU-only；原历史原文不可修改）。
2. 按冻结队列优先下载和哈希验证；或者仅启动明确标记的工程诊断Smoke，无独立科研结论。
3. 正式Smoke6条、独立验证36条：解析≥35/36、格式失败原文保留；两人的GT-blind审核未有就标NOT_RUN，不用单人助手称盲评。
4. 正式100对Pilot：统计九类微/宏Unsafe F1、完整分母与Valid-only、PairAcc、成对bootstrap、真实P50/P95和进程显存峰，作为300→868的预算门槛。
5. Pilot通过后再申请Stage2扩至300及868；每个GPU作业≤6h，正式分母不丢失；无公开SFT-only/Step-DPO权重不冒充训练消融。

**审计裁决：CONDITIONAL GO for targeted Stage1 recovery；NO GO for full Test GPU claim at present。**
