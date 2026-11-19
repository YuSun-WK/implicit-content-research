# VLSU｜加速复现双轨执行：Stage2 模型 Smoke + Stage1A 数据恢复
**2026-11-19；任务起点 `0b9a85208466612960a34f4e10225e35b63cf478`。唯一目标忠实复现 ICLR 2026 原论文；无训练、无新方法、无迁移。**

## 首先审查、不要假设已具备数据或GPU
仓库 `YuSun-WK/implicit-content-research`，分支 `repro/vlsu-original-20261119`，目录 `06_experiments/repro_vlsu_original/`。阅读 `Run_Stage0.md`、`Run_Stage1.md`、`protocol/Original_Experiment_Matrix.md`、`protocol/Output_Parsing_and_Metrics.md`、`configs/official_qwen25vl7b.yaml`、`prompts/README.md`、`reports/stage1r/DNS_Diagnosis.md`、`reports/stage1r/Stage1_Image_Coverage.md`、`reports/stage1r/Move_Resume_Instructions.md`、`scripts/stage1_manifest.py`、`scripts/stage0_metrics.py`、`scripts/stage1r_state.py`，并以正式会议 PDF Appendix D.1/D.3/D.4 为Prompt唯一原始依据。
- 作者论文8187，固定Apple CSV8159，SHA256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`，公共CSV非本地图片包。Stage1R在当前Linux worker有 DNS/HTTPS 不稳定，状态 `BLOCKED_BY_ENVIRONMENT`，实际新增图片0。
- 现在已保存28个解码成功的URL对象，覆盖30个joint UUID、23个image gold有效UUID；text-only有8159个文本标签且不要求图片。Github只有聚合报告和snapshot SHA，**真实图片/SQLite/完整Manifest在前一运行机的私有`.local/stage1/`，不能根据GitHub报告凭空生成文件**。若运行在另一机器，请用已记录私有迁移/校验流程。当前 `Stage1R` 测试76 passed。
- **重要计划调整**：Stage2可在现有少量真实可解码图像上先验证推理工程，不再因full未完成完全停摆；这些输出必须标为 `ENGINEERING SMOKE / PARTIAL REPRODUCTION`，不能作为Table2、4正式F1或作者复现对照。Stage1 full继续保持BLOCK/PARTIAL，直到可访问图片清单达到可审计覆盖。

## 双轨顺序（可按机器条件并行，不要让A阻挡B）
### Track B（最高优先级）：最快获得真实 Qwen2.5-VL-7B GPU 推理 Smoke
**B0 环境与模型门**
1. 本机核实 `nvidia-smi` GPU型号、显存总/空闲/已占、同机他人进程、CUDA、PyTorch、Transformers、Pillow、qwen-vl-utils/accelerate/bitsandbytes(若用)。绝不抢占/杀停他人的进程。单GPU预算以峰值allocated/reserved和nvidia-smi为准，16–20GiB，单作业硬上限6h；Smoke预设短作业、batch=1，达到OOM或干扰风险即停止恢复，不要无限循环。
2. 优先使用HF官方 `Qwen/Qwen2.5-VL-7B-Instruct`，固定真实本地模型、tokenizer、processor revision commit SHA，实际提交 `model_manifest.json`（无敏感token或权重）。若本机已有可信缓存，校验其revision后复用；若无权重且网络不稳定，明确模型`NOT AVAILABLE`，在稳定授权网络机器预缓存后再传/使用，不要无期限网络等待或宣称模型已跑。
3. 先尝试本地未量化BF16，**仅在确认当前免费显存足够且不妨碍其他作业时**做一次小token加载+推理；BF16资源要求达不到时**立刻停止该尝试**，改用官方相同基础权重的4-bit bitsandbytes量化加载（兼容需检查），记录backend/config、Revision、量化前后状态并标记 `RESOURCE-CONSTRAINED PARTIAL REPRODUCTION`。禁止把任何本地BF16或4bit说成作者相同精度，因作者precision UNKNOWN。不可使用论文未测模型替代后写为原论文模型。
4. 重新从固定PDF提取binary/direct/CoT prompts，校验与 `configs/official_qwen25vl7b.yaml` 的SHA256相等；尽量做独立逐字核对。人工最终review若未做，写 `PROMPT HUMAN SIGNOFF OPEN`，本轮只运行工程Smoke，不作正式论文性能声称。image-only/text-only专用Prompt若作者未公开则显式 `LOCAL ADAPTATION`，不可冒充原文。
5. 图像processor候选 `min_pixels=256*28*28, max_pixels=1280*28*28` 来源Qwen参考代码，论文写法与实际作者实现尚UNKNOWN；本地按所选候选固定并标记偏差。明确chat template、message roles、图像与文本拼接、图片是否exif orientation/RGB、patch/token数、system prompt，配置和每条输出保留生成参数。D.4 default temperature不得擅自等于0. 每个可运行variant应清楚区分作者参数已知项/本地显式选择值；不确定参数不宣称一致。
**B1 开发真正可恢复的推理与独立评分（Stage2跑前门）**
1. 建立 `scripts/stage2_qwen_smoke.py`、`scripts/stage2_roster.py`、`configs/stage2_smoke.yaml`、`protocol/Stage2_Deviation_Ledger.md`、`tests/test_stage2.py`。用户配置 `--csv`、`--stage1-root`、`--manifest`、`--model-path`，运行前必须从实际cache验证图片hash及固定CSV SHA/UUID；只选已成功解码且对应真实UUID，不能选择看过预测的样本。若图片仅在旧worker，给迁移命令且禁止假设本机存在。
2. 首先选定不超过20条有图Joint UUID（已知30可用时按固定seed、跨组合取样）；其中优先包含能进入三模态交集的样本，并记录原始模式，尽量覆盖S/B/U。预先固定同一批UUID的Joint Direct、Joint Binary、Structured CoT以确保后续配对。若图像少于10条，报告阻碍；文本单模态可使用对应UUID并独立标注，不得拿joint标签测text-only。
3. 用论文模板做真实 `joint/direct` 10条先验示范；代码端支撑 `joint/binary`、`joint/structured_cot` 各可先5–10条，视GPU预算决定；`image-only`、`text-only`在专用原Prompt不公开时必须标明local prompt adaptation，仅用于工程验证。避免为了速度只选择成功例，记录所有selected/failed/invalid UUID。
4. 测试模式不等于原论文正式指标：若需要用缩短输出token的fast debug配置，单独标 `ENGINEERING_SHORT_OUTPUT`；如使用正式原文最大长度1024/2048，需将加载配置、实际生成token计入日志。生成独立JSONL原始输出（**私有目录**）、另建parsed JSONL，记录 `run_id/uuid/input_sha256/image_sha256/prompt_sha256/model_revision/processor_revision/precision/quantization/decoding params/seed/runtime/peak_vram/status/raw_output_reference/parse_status`；对于CoT仅解析最后[Final Classification]，不从自由推理找答案。
5. 必须支持不重复执行完成行的resume；在任何GPU OOM/异常/用户中断时保存已完成记录；每个SKU/配置唯一run_id；run完成后按 `validate_predictions` 对任务固定UUID校验，未运行/失败不应“消失”。只读取已有CSV与图片、严禁训练或使用付费API。
6. 运行最少一个10条真实Joint Direct end-to-end，输出真实raw+parsed数量、有效率、token数量、p50/p95 latency、samples/s、峰值显存、实际工作GPU及是否有其他进程、cache/model revisions；进一步binary/CoT若可行再跑，不把10条准确率当论文复现F1。若GPU、缓存或权重条件缺失，本轮完成CPU/mock integration并标 `SMOKE BLOCKED`，提供最短恢复路径，不伪造推理。
**B2 实测外推并决定Stage3**
1. 基于真实Joint Direct与CoT的token、图像耗时、总吞吐和VRAM外推在有效图片规模 N 下各任务资源范围；独立报告下载覆盖不确定性，不默认8159图可用。按 6h上限给可恢复批次大小建议。
2. GPU Smoke后独立列出配置差异：权重量化、显存、prompt核对、图像budget、decoding、单模态模板、作者F1定义和作者数据版本；不得对作者Table2/4结果做未经验证的“达标/失败”结论。

### Track A（无GPU） 并行恢复图片可用性
- 不再强求当前网络不稳worker不停地探测；按 `Move_Resume_Instructions.md` 将**合法可迁移**的已有私有状态和图片对象冷拷贝至一个网络稳定、授权访问的CPU机器，先核验SQLite/哈希/完整Manifest。不可把图片上传GitHub。
- 仅在网络真实控制实验通过后，`--phase full --resume --execute --max-requests 30 --retry-environment-dns` 进行首轮有限恢复，审核状态；随后分批100/300等按实际网络和rate limits保守增加。不得绕过403/404/源版权，禁止改URL/换图/禁TLS；保留URL 8157和UUID 8159官方全集，失败/未尝试分类保持可查。
- 无可用新机器/网络gate失败：仍保持 A=BLOCKED_BY_ENVIRONMENT，给可复制的本机执行/传输说明，**并继续Track B，只要GPU、私有图像和权重已经可读**。
- 阶段末若有新数据，刷新reports/stage1*聚合和固定manifest哈希，**不可静默改变既有Smoke cohort**；形成新的Snapshot ID供Stage3。

## 结果和交付
- 文件仅放 `06_experiments/repro_vlsu_original/`，保持旧Stage0/1/R结果不覆盖。代码/测试/版本/指标汇总可提交，private `.local`内存储原图、原文本、权重和原始生成，且.gitignore。
- 运行`python -m pytest -q`（现有76 tests不能回归）及`git diff --check`；保存真实stdout/stderr，禁止写虚假PASS或手填预测结果。
- 交付 `reports/stage2/Stage2_Smoke_Audit.md`, `GPU_Environment.json`, `Inference_Run_Summary.json`, `Stage2_Execution_Log.txt`, `protocol/Stage2_Deviation_Ledger.md`, `Run_Stage2.md`；若模型未运行明确 `NOT RUN`、阻碍点及复现命令，若运行成功展示真实计数与日志证据。
- Track A 分开状态报告：当次新增下载URL/UUID、累计成功、失败/未尝试、关键模式S-S-S、S-S-U、U-S-U、B-B-U的覆盖，不能以Smoke小样本替代全量分布。
- 每次GPU job≤6h、单卡、共享GPU不干扰其它进程；严格无训练/无新模型/无API。任何正式Table1/2/4或Figure3/4/5复现均须等到足够覆盖、固定样本ID、解析/协议核对后单独Stage3/4运行。
- 提交当前分支，不合并main。最后汇报：commit SHA，Track B是否真正跑出至少10条推理、准确的显存/速度/输出有效率、模型量化与rev；Track A下载进度或外部环境阻断、下一步阶段与最短可执行命令。
