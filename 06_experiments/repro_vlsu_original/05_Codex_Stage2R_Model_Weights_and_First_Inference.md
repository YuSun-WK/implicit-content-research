# VLSU Stage 2R｜优先获取官方 Qwen 权重并跑出首批真实推理
**2026-11-20；上游 HEAD `4d243512ca31123b77d631283376a6cba92392d2`。当前首要瓶颈是权重获取，不是GPU和推理脚本。**

## 0. 当前事实（不要重做已完成事项）
- Stage0通过；Stage1图片下载器和Stage1R保留；Stage2工程脚本已提交。
- 最新CPU自动化测试：`80 passed in 7.42s`，`git diff --check`通过。
- CUDA 12.8、PyTorch 2.9.1、Transformers 4.57.3；可见RTX4090空闲卡约48,506MiB可用，BF16支持。运行时重新检查GPU，不假设仍空闲。
- 固定Qwen官方repo `Qwen/Qwen2.5-VL-7B-Instruct` revision `cc594898137f460bfe9f0759e9844b3ce807cfb5`。五个safetensors总16,584,414,560 bytes (15.44 GiB)，官方SHA256已锁定在`configs/stage2_model_files.json`。
- 当前五个shard完整校验数0/5，只有284,199,226 bytes分散partial，不足以load模型。HF Hub/LFS下载TLS EOF、short/empty response、timeout。1MiB Range probe曾成功，但尚未证明更大chunk或稳定完整下载。
- CPU真实Processor成功处理冻结的10个样本；Direct10、Binary5、CoT5 token/grid已构建；Prompt抽取哈希匹配。**真实GPU推理0条，预测0条，BF16/4bit实际峰值、latency均未知。**
- 10 UUID roster SHA256 `63e4519eb511a677e2e7e9b5aa91158d963ea3fee424b4e680c961415647c7a6`，Stage1 manifest `78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512`。真实图片/SQLite仅在私有.local，需先验证本机是否存在；不能从GitHub aggregate假造图片。
- Track A当前DNS/HTTPS gate BLOCKED，30/8159 joint UUID (0.37%)，23 image-gold UUID。不要在本轮把8k图片下载作为B线前置。Track A保持BLOCKED并提供稳定授权机器恢复说明。
- PROMPT HUMAN SIGNOFF OPEN；Stage2只能称ENGINEERING SMOKE / PARTIAL REPRODUCTION，不能声称作者复现或Table结果。

## 1. 本轮最高优先级：取得五个完整、哈希匹配的官方权重
只允许官方Hugging Face仓库和revision，禁止未经验证镜像、网盘、不明来源权重或改模型替代。

### 1A. 先盘点可复用的缓存，不做盲目重下
1. 从当前仓库分支最新HEAD开始，确认工作区无破坏性改动。读取`Run_Stage2.md`、`Stage2_Execution_Log.txt`、`model_manifest.json`、`configs/stage2_model_files.json`和本任务。
2. 查`HF_HOME`、`HF_HUB_CACHE`、`TRANSFORMERS_CACHE`、`~/.cache/huggingface/hub`、`.local/stage2/hf`和用户明确允许的模型缓存路径。使用`hf cache scan`或小范围文件清单检查；不递归扫描整个系统、不删除任何缓存、不清理.incomplete、不覆盖其他实验权重。
3. 对每个已存在shard记录真实路径、大小、SHA256、是否symlink及目标是否存在；只把精确revision且SHA256匹配的完整文件记为verified。记录剩余磁盘空间，至少确保能容纳未完成文件和传输临时空间；不要把15.44GiB模型复制多份。
4. 检查stage1私有root、10 UUID冻结roster和所有image hash。如果缺失，先按`reports/stage1r/Move_Resume_Instructions.md`迁移并核验，不得只凭公开摘要生成本地文件。

### 1B. 用官方工具优先恢复下载（限时诊断）
1. 分别做一次低频的`huggingface.co`及实际官方文件CDN的DNS/TLS/HTTP HEAD或小range诊断，记录分阶段失败，不把GitHub/example.com可访问等同HF可访问。任何token、signed URL、authorization header必须脱敏，不写入git或日志。
2. 优先复用原HF cache和标准命令，限制`--max-workers 1`，让Hugging Face客户端续传partial。先`--dry-run`/help确认本机CLI参数，再执行单次有时间上限的`hf download Qwen/Qwen2.5-VL-7B-Instruct --revision cc594898137f460bfe9f0759e9844b3ce807cfb5 --include '*.safetensors' '*.json' merges.txt --cache-dir .local/stage2/hf --max-workers 1`。不要反复启动相同失败下载；每次运行后统计真实字节增量。
3. 如果官方CLI再次TLS中断，但官方LFS Range端点可用，先对一个shard做16MiB、再64MiB单range试验，校验HTTP 206、精确Content-Range、字节长度、TLS证书、实际对端和无私网重定向；仅测试成功才可实现分块恢复。分块下载只向官方revision对应的临时signed URL发请求，signed URL过期就从官方HF接口重新获取；不得日志记录URL签名。建议16–64MiB chunk、每文件单worker或总并发<=2、有限重试、指数退避、SQLite/JSON持久化chunk bitmap、每chunk校验Content-Range、fsync和原子rename。服务器若忽略Range返回200，不得拼接；Range不稳定则停止，不无限重试。
4. 如果当前运行环境不能稳定连HF，立即停止网络空转，输出`MODEL_FETCH_BLOCKED_BY_ENVIRONMENT`。给用户一份能在**稳定且获授权网络的Linux/Windows机器**运行的官方`hf download`命令和传回实验服务器的`rsync/scp`命令；说明只传本revision的完整快照文件和必要metadata。不能要求用户把模型权重提交GitHub，也不能把私钥/token写入命令、repo或日志。
5. 可以并行检查用户/实验室已存在的同revision官方缓存或共享只读模型仓库；必须通过manifest SHA256后才能复用。不要下载别的模型或近似revision替代。

### 1C. 权重验证门
- 5个shard各自大小和SHA256必须与`configs/stage2_model_files.json`完全匹配，5/5 verified；metadata/tokenizer/processor Git blob和SHA256同样验证。
- 模型目录basename必须是`cc594898137f460bfe9f0759e9844b3ce807cfb5`，所有symlink目标都必须存在。可以使用HF cache snapshot，但迁移时需包含对应blobs，或在私有目录物化完整文件。
- 生成`reports/stage2r/model_acquisition_manifest.json`和`Model_Acquisition_Log.txt`，只提交文件名、大小、hash、状态、repo/revision、工具版本和汇总；不提交权重或signed URL。
- 若未达到5/5，禁止GPU模型加载，明确缺失shard和已传字节；不能把模型metadata存在说成模型权重可用。

## 2. 权重通过后，立刻执行真实GPU推理（不要另写一套模型）
1. 复用`scripts/stage2_qwen_smoke.py`、`configs/stage2_smoke.yaml`、冻结10 UUID roster和已验证本地图片；先做`--dry-run`和Manifest/hash校验。
2. 重新运行`nvidia-smi`检查共享GPU。只选择空闲物理UUID；若被占用，换另一张空闲卡或等待，不抢占其他进程。CUDA_VISIBLE_DEVICES必须设物理GPU UUID。保持PyTorch allocator <=20GiB、batch=1、单作业<=6小时。
3. 首先BF16 Direct10，显式`--precision bf16`，使用配置中原论文max_new_tokens=1024，不做训练。命令结构：
```bash
export CUDA_VISIBLE_DEVICES=GPU-<current-idle-uuid>
python scripts/stage2_qwen_smoke.py --csv "$VLSU_PINNED_CSV" \
  --stage1-root .local/stage1 \
  --manifest .local/stage1/snapshots/78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512.json \
  --model-path .local/stage2/hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5 \
  --mode direct --precision bf16 --execute
```
如果实际使用本地物化目录，则必须目录basename仍为revision并通过完整hash。
4. 运行时遇到BF16 OOM：保存失败日志和GPU状态，结束该进程，不无限重试。再评估4-bit NF4。当前记录`accelerate`和`bitsandbytes`未安装；只有4bit确有必要时，在隔离环境安装兼容版本，不升级/破坏现有共享科研环境。4bit使用相同base revision但单独run_id，明确标`RESOURCE-CONSTRAINED PARTIAL REPRODUCTION`。
5. Direct10真实生成完整且解析链无故障后，再对相同冻结10 roster前5条跑Binary5与Structured CoT5（相同5 UUID），各自独立run_id和独立6小时限时。CoT只解析最后的`[Final Classification]`字段。Prompt逐字人工签核仍OPEN，因此只作为工程Smoke；不得宣称正式原论文性能。
6. 结果需私有保存原始输出/SQLite/parsed JSONL，公开只报聚合：真实generated数、valid/invalid、p50/p95 latency、samples/s、input/output token、image grid、峰值allocated/reserved、load时间、实际GPU UUID、精度/量化、revision、Prompt hash、run_id。断点续跑不得重复已完成UUID。

## 3. Track A不阻挡模型线
- 当前Track A在网络gate失败，保持BLOCKED。不要把本轮主要时间再次投入公共控制域重复探测。
- 若用户提供稳定授权机器，按Stage1R迁移流程核验SQLite、对象、快照，再从原root小批量resume；无新机器则本轮不下载图片。
- 不修改已有30 joint UUID roster和manifest；后续新图片形成新的snapshot及新cohort，避免Smoke队列改变。
- 仍不得把30个可用样本当成完整论文评测；Stage3分层Pilot需另行审查样本量/模式覆盖和Prompt signoff。

## 4. 自动化测试与GitHub交付
- 不重写已通过的Stage2主流程。只有真实发现bug才做最小修复，并新增针对性测试。
- 运行`python -m pytest -q`（当前80 passed基线必须保持）和`git diff --check`，保留真实输出。
- 新增`reports/stage2r/Stage2R_Model_Acquisition.md`、`model_acquisition_manifest.json`、`Model_Acquisition_Log.txt`；真实推理时更新`Inference_Run_Summary.json`并保留旧日志。
- 只提交代码、配置、聚合指标、hash和文档。绝不提交模型权重、图片、原始query、原始模型输出、SQLite、signed URL、access token或私有缓存。
- 提交到`repro/vlsu-original-20261119`，不合并main，不碰survey/H1/PR#78。

## 5. 最终状态必须诚实区分
- 权重未齐：`MODEL_FETCH_BLOCKED` / `MODEL_WEIGHTS_PARTIAL`，GPU NOT RUN。
- 权重5/5验证但尚未加载：`MODEL_READY_GPU_NOT_RUN`。
- Direct生成至少1条但未完成10条：`DIRECT_SMOKE_PARTIAL`。
- Direct10完成：`DIRECT_SMOKE_PASS`（仍非正式评测）。
- Binary5/CoT5完成：单独报告对应工程Smoke PASS。
- Track A仍单独PARTIAL/BLOCKED。
- 最后向用户报告：commit SHA；5个权重逐文件大小/hash状态；是否来自稳定机器/官方HF；真实GPU推理数；BF16/4bit；显存/速度/解析有效率；Track A状态；Stage3启动所需剩余事项。

**本轮成功的唯一核心标准：尽最大努力取得并校验官方Qwen固定revision，随后至少完成10条真实Joint Direct GPU推理。不要用更多文档、mock测试或CPU Processor通过替代这两个结果。**
