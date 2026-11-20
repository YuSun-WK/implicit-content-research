# Stage 2S｜VLSU 原论文复现加速：官方来源切换与首批真实 GPU 推理
**2026-11-20；基于 `7e6f00bdaaaa8da2a3109674b40f2a9e304c0d35`。本轮首要交付是模型5/5权重完整与真正的10条Joint Direct生成；失败时只报告可验证的阻断及用户可执行的最快转移路径。**
 
## 1. 基线事实（不要回到常规审计循环）
- `YuSun-WK/implicit-content-research` 分支 `repro/vlsu-original-20261119`，工作目录 `06_experiments/repro_vlsu_original/`。先读取 `Run_Stage2.md`、`reports/stage2/Stage2_Smoke_Audit.md`、`reports/stage2r/Stage2R_Model_Acquisition.md`、`reports/stage2r/model_acquisition_manifest.json`、`configs/stage2_model_files.json`、`configs/stage2_smoke.yaml`、`scripts/stage2_qwen_smoke.py`、`protocol/Stage2_Deviation_Ledger.md`。
- Stage2R模型下载仍失败：五个完整safetensors 0/5；私有partial字节合计418,416,954 / 16,584,414,560，HF官方16/64MiB Range 206曾成功但后续curl 28/35；CPU测试80通过，GPU真实生成0条，图像解码可用30个Joint UUID。你必须严格报告事实，不能因CPU Processor PASS写成GPU PASS。
- Qwen官方HF固定仓库/版本：`Qwen/Qwen2.5-VL-7B-Instruct`，revision `cc594898137f460bfe9f0759e9844b3ce807cfb5`。这套文件的SHA/size精确记录在 `configs/stage2_model_files.json`。模型文件不可提交GitHub。
- 新可用的**Qwen官方推荐渠道**：`https://modelscope.cn/models/Qwen/Qwen2.5-VL-7B-Instruct`。Qwen自己的HF模型卡推荐ModelScope的`snapshot_download`。该ModelScope仓库的默认版本是否字节等同HF锁定revision **尚未验证**；必须通过逐文件SHA验收，而非只比较模型名。
- 以前已验证的HF metadata、processor/tokenizer文件可直接复用。Stage2模型完整性校验还会检查这些metadata的Git blob；ModelScope若返回不同metadata，**保留锁定的HF metadata，仅用逐SHA完全相同的权重文件填补HF目录**。若任一权重不匹配，停止，记录为`SOURCE_CONTENT_MISMATCH`，不得替换或悄悄放宽约束。

## 2. 唯一核心任务：换渠道取完整模型，不再无效地长时间网络诊断
### A. 缓存/共享盘优先（最省网络）
- 在现有用户授权目录、小范围检查同revision的HF/ModelScope缓存、实验室共享模型盘。不得扫描他人的私有文件或修改他人任务。
- 只要文件SHA256与`stage2_model_files.json`中五个目标完全一致，就可复用，记录来源/路径；保留已有418MB HF partial原样，避免破坏恢复线索。
- 检查可用磁盘和HF snapshot目录 symlink/目标完整性；不能以symlink名称匹配代替数据SHA。
### B. **立即测试Qwen官方ModelScope**（本轮新路线）
- 若当前Python环境没有`modelscope`，在隔离下载环境安装，不破坏已通过80 tests的运行环境；先检查ModelScope官方repo访问和小文件下载稳定性。
- 按ModelScope当前CLI/help确认参数，在私有目录执行等价代码：
```python
from modelscope import snapshot_download
model_dir = snapshot_download("Qwen/Qwen2.5-VL-7B-Instruct", cache_dir="/private/vlsu-modelscope-cache")
print(model_dir)
```
  不得将ModelScope的`master`误当HF revision的commit。
- 如果大文件能持续下载，保留且恢复下载，不需要再探索其他网络工具；完成后按**五个官方HF SHA256**逐文件审计。如果分片命名不同，先判定是否可证明与HF文件一致；无法证明则不合并，不推理。
- 校验5/5通过后，把文件放入已有HF锁定snapshot目录 `.../models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5/`，保留从HF固定revision取得的metadata/tokenizer/processor，重新运行已有`model_manifest()`严格检查。不要使用较新的模型版本 metadata。
### C. 如果ModelScope仍因当前机网络阻断
- 不再无限重跑失败的HF Range/curl；只允许有界验证、记录准确阻断。提供**两套具体终端命令**：稳定机器上的HF固定revision下载，以及稳定机器上的Qwen官方ModelScope下载（ModelScope返回文件仍需全部匹配HF五个SHA）；随后经用户授权的`rsync -avP`或`scp`把校验通过的5个权重传到实验服务器。传输完成后在目标机复验SHA。
- 对Windows下载机提供Python`snapshot_download`和校验方式，给对应Windows到Linux的安全传输建议；无需询问用户即可给出操作说明，但不能宣称你控制了其Windows电脑。
- 不使用不明镜像站点、未经验证第三方模型/权重、付费API或新的模型替代。任何凭证/signed URL不得入GitHub或公开log。
- 该分支必须给出明确`EXTERNAL_DOWNLOAD_REQUIRED`，指出唯一人工依赖是什么（如需用户在稳定机器执行），不能继续提交仅诊断的新轮任务。

## 3. 权重5/5通过后，马上执行真正的10条GPU推理
- 复用已通过CPU验证的10 UUID名单与Stage1 snapshot：roster SHA `63e4519eb511a677e2e7e9b5aa91158d963ea3fee424b4e680c961415647c7a6`，Stage1 manifest SHA `78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512`。先读取本机私有真实图片和校验hash，不凭GitHub聚合摘要假设文件存在。
- 当前GPU环境曾发现空闲RTX4090约48.5GiB，**实际执行时重新检查**是否仍空闲。只用一张不被占用的卡，显存allocator上限20GiB，作业≤6小时，不干扰他人进程。
- 首先以HF锁定revision、BF16、batch=1、原论文Direct prompt、完整配置max_new_tokens=1024尝试10条真实Joint Direct；优先使用 `Run_Stage2.md` 现有命令，只有真实BUG才能最小修改脚本；若显存OOM，则保存真实错误并单独评估官方同底座4-bit NF4，标记`RESOURCE-CONSTRAINED PARTIAL REPRODUCTION`。
- Direct完成后，同一固定前5个UUID做Binary5/Structured CoT5；不合并三种Prompt的运行日志和样本分母。推理的原始内容、完整query、生成文本必须只留私有`.local`，聚合json/报告入GitHub。Prompt人工逐字signoff仍是OPEN，不把Smoke的准确率直接同作者Table1/2/4比较。
- 公开必须报告真实：`model_5of5_verified`, `direct_generated / direct_valid`, `binary_generated`, `cot_generated`, `precision`, `gpu_uuid`, `peak_allocated/reserved`, `load_time`, `p50/p95 latency`, `output_token distribution`, `resume_check`, `run_id`, `model_sha`, `prompt_sha`，以及失败/未运行样本。不得伪造推理。
- 如果全部权重到位而推理代码失败，聚焦修复阻塞第一条真实模型推理的Bug，优先一条通过，然后十条，不回到系统级工程改造。
- 完成后给Stage3的可运行短批Pilot资源计划；分层正式Pilot仍需要图片可用性进一步扩大，不因为30条测试集就宣称正式复现完成。

## 4. 并行数据线：不拖慢模型
- Stage1R Track A仍`BLOCKED_BY_ENVIRONMENT`，已有30 Joint / 23 image-gold，8159 text-only eligible。只在稳定授权机器上从原SQLite/缓存恢复下载，现有30样本的Snapshot不变，新图片对应新的Snapshot。不得硬把Stage1全量图片作为本轮B线前置。
- 如果Stable ModelScope下载机器也具备数据抓取许可和安全措施，可建议同步跑Stage1A低并发图片任务，但不得因此耽误模型下载和GPU Smoke。

## 5. GitHub交付、最短闭环
- 仅写本项目目录，提交`reports/stage2s/Model_Source_Switch.md`、`Model_SHA_Audit.json`、`Execution_Log.txt`、`Run_Stage2S.md`。若真实GPU推理发生，加入`Stage2S_GPU_Smoke.md`及聚合metrics。模型重量、完整图片、私有URL/query/输出/SQLite不入GitHub。
- 复跑`python -m pytest -q`，现有80项基线不回归，执行`git diff --check`，保留实际结果。无新BUG不要新造大量测试。
- 原分支`repro/vlsu-original-20261119`提交，不合并main、不碰综述/H1/PR#78。
- 最终输出唯一关键状态：`MODEL_READY_AND_DIRECT_SMOKE_PASS`、`MODEL_READY_BUT_INFERENCE_BLOCKED`、或`EXTERNAL_DOWNLOAD_REQUIRED`；说明下一步由Codex自动可做的事情和**仅有的用户人工动作**。明示究竟有多少条真实GPU预测，及下一步最短可执行命令。
- **完成标准**：这轮不以写更多文档为成果，而以五个真正匹配的权重及至少10条真实Joint Direct GPU结果为主。资源/网络无法满足时及时停止，给出行动路径而不是重复写“BLOCKED”。
