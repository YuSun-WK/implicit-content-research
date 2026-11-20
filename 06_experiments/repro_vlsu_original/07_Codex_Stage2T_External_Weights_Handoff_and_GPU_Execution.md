# VLSU Stage 2T｜停止网络空转，外部权重交接，直接开始真实GPU推理
**2026-11-20；上游真实实验提交 `4d3d24d6eeeeae5daa5981d64c002f254d2c142f`。本任务旨在完成外部机器到GPU机器的可审计交接，而非再写DNS/网络报告。**

## 一、实证状态与不能更改的实验协议
- 论文原始复现：模型 `Qwen/Qwen2.5-VL-7B-Instruct`；官方HF固定revision `cc594898137f460bfe9f0759e9844b3ce807cfb5`；五个权重sha256及size已经锁定：`configs/stage2_model_files.json`。论文/数据的审计详情见Stage0。
- 最新Stage2S结果：HF已下418,416,954字节partial；ModelScope官方同名仓库又单独下135,659,680字节smallest shard partial；**5个完整权重校验0/5**；当前服务器两条官方传输通道均失败；GPU模型加载与Direct/Binary/CoT预测均为0；80单测PASS。仅ModelScope开头7,876,447字节与HF部分相同，**不能证明完整权重或revision相同**。
- 数据线仍PARTIAL：8159公开CSV UUID/30条真实图文UUID可用（28 unique URLs）、23条image-only有合法gold；冻结10条Joint roster和Prompt SHA及Processor输入已核验。真实图片、原始CSV、private sqlite和snapshot在实验目录`.local`，不得凭GitHub报告假造。
- 当前约束：单GPU/单次<=6h、PyTorch显存使用预算20GiB、不干扰共享进程、无训练/无付费API、不改方法、不合并main。
- 用户强烈要求加快复现；**不要再次在当前服务器运行同样的不稳定HF/ModelScope下载流程**，除非独立证据显示新稳定网络已到位。不创建第3套下载器或增加无关测试；现有推理入口 `scripts/stage2_qwen_smoke.py`、`Run_Stage2.md` 即可。

## 二、唯一优先事项：模型文件在稳定授权机器下载、哈希验证、传输
### 路径A：现有合法缓存
- 最快路径：在用户授权的本机缓存/实验室共享权重目录检查Qwen同版模型文件，完整五个safetensors逐个SHA256；可以仅copy/link（需获授权）匹配文件到实验目录。不可扫描他人私有目录或假设存在。
- 官方HF同revision优先；ModelScope为Qwen官方发布的替代**下载渠道**，不是自动同revision。**ModelScope必须与固定HF五个SHA完全一致才可采用**。
### 路径B：用户的 Windows 电脑或者其它稳定机器下载
- 首先仅创建一次用户可复制的`reports/stage2t/USER_ACTION_WINDOWS.md`，说明在Windows Terminal/PowerShell可执行：
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U huggingface_hub
.\.venv\Scripts\hf.exe download Qwen/Qwen2.5-VL-7B-Instruct --revision cc594898137f460bfe9f0759e9844b3ce807cfb5 --include "*.safetensors" --local-dir .\qwen-vlsu --max-workers 1
```
  如该CLI版本选项不同，先使用当前安装版`hf download --help`确认并修正；不把注释写进可执行命令。ModelScope官方备选：
```powershell
.\.venv\Scripts\python.exe -m pip install -U modelscope
.\.venv\Scripts\python.exe -c "from modelscope import snapshot_download; print(snapshot_download('Qwen/Qwen2.5-VL-7B-Instruct', cache_dir=r'.\qwen-modelscope'))"
```
  从打印路径定位5个shard，同样校验HF固定hash；不能直接假设ModelScope master一致。
- 请实现一个**跨平台、标准库Python**的`scripts/stage2_verify_external_weights.py`，输入`--source-dir`和已有官方`--manifest configs/stage2_model_files.json`，逐文件流式读SHA256、比较size/hash、结果一行一文件、exit0仅当5/5，否则exit2；不要泄露私有绝对路径/用户名；给最小离线fixture测试，避免增加重复测试。优先重用现有`model_manifest()`代码，防止重复逻辑相互矛盾。若ModelScope/official HuggingFace源目录包含更多文件，不影响只读取五个shards。
- 在另一台机器5/5 PASS后，用`rsync -avP`、Windows OpenSSH`scp`或获授权SFTP工具传输到GPU机器，**只传已校验文件**。目的地路径以真实`pwd`和`Run_Stage2.md`中的HF revision snapshot为准，不能写死示例路径。说明可在Linux/Windows上分别如何转运，要求充足磁盘、传输前后sha256都PASS。绝不经GitHub上传权重。
- 若没有一台网络可下载整模型的授权机器，明确`EXTERNAL_DOWNLOAD_REQUIRED`，不做伪GPU运行，也不再循环添加诊断报告。报告用户需要的唯一操作：用可联网本机执行上述官方命令+sha校验，再传回服务器。Codex可先生成可执行命令/脚本，但不能代替用户完成外部下载。

## 三、权重到GPU机器后优先跑第一条、再10条，之后5+5
- 前置门：五个safetensors**全部**与固定HF manifest SHA/size一致；使用HF固定revision的tokenizer/processor metadata，现有`stage2_qwen_smoke.model_manifest`复验**全部**本地文件。确保只在用户指定或允许的本地目录读取；外部ModelScope若metadata不同不得替换已固定的HF文件。
- 先做dry-run检查冻结CSV/UUID/Stage1 snapshot和图片对象的真实hash；Prompt哈希一致。独立人工signoff仍OPEN。随后`nvidia-smi`选当前真正空闲GPU UUID，别沿用旧空闲状态。
- 运行现有`stage2_qwen_smoke.py` `--mode direct --precision bf16 --execute`，配置保持`configs/stage2_smoke.yaml`、完整原定max_new_tokens，batch=1，allocator 20GiB、外部timeout <=6小时。脚本是一个已冻结的Direct10队列，**先完成第一条的真实模型生成并确认落盘**（可以通过既有可恢复日志观察），再继续其他9条，不重选样本、不改标签。错误时只修最短阻断路径，不增建全新推理框架。
- 如发生BF16 OOM，保存错误、结束该GPU作业，再评估同base权重4-bit（当前bitsandbytes/accelerate未装），且标`RESOURCE-CONSTRAINED PARTIAL REPRODUCTION`；不得伪装作者设置。未发生OOM不预先量化。
- Direct10后，相同冻结队列前5条跑`--mode binary`、`--mode structured_cot`；独立run_id。原始输出和完整query仅保存在私有`.local`，提交聚合生成数、解析有效率、GPU UUID、模型rev/hash、precision、peak-vram、p50/p95、tokens和真实stdout；没有真实GPU结果不得给“准确率”“吞吐量”数值。
- Track A图片全量仍阻断且独立处理，不在此任务中重复网络下载。Stage3只有在GPU工程Smoke通过、图片覆盖达到事先定义的分层Pilot条件、数据列表冻结后启动；不得把10条作为正式Table2或Fig4/5复现。

## 四、必须消除的重复失败模式
- 不重复Stage0-2的论文精读、CSV盘点、Processor测试、80基础单测以外的无关审计。
- 不新增第三套权重下载器；在两个官方来源的当前机器网络均失败后，转外部机器是**真正的新执行条件**，不是换参数在旧网络循环。
- 任务输出只能有二种实质状态：`GPU_SMOKE_REAL_RESULTS`（权重5/5且产生真实预测）或`WAITING_FOR_EXTERNAL_VERIFIED_WEIGHTS`（尚需用户外部动作）；任何中间准备性结果必须明确NOT RUN，不以大量md/测试掩饰阻塞。

## 五、交付方式
- 同一分支 `repro/vlsu-original-20261119`，不合并main。新代码/测试可在任务必要时产生；保存`reports/stage2t/Execution_Report.md`和`USER_ACTION_WINDOWS.md`，报告只有真实执行证据（不伪造），最多一个简短的聚合json。确保旧的80测试通过且`git diff --check`。
- 若没有外部权重，交付给用户一段**不依赖猜测路径的Windows完整下载与SHA检查命令**、安全传输命令模板、Codex收到权重后可直接执行的精确GPU命令和前置检查，并明确“本轮需要用户本人完成什么”。
- 若权重已到：立即提交真实GPU结果以及Stage3 pilot的最短下一步，不需继续请示或追加文献调研。
