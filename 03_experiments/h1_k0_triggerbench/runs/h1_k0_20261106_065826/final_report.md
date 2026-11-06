# H1-K0 第一轮 Kill Test：中止报告

状态：**按六小时总预算停止于 Stage 0C / 0D；未进行 GPU 推理。** 运行目录创建于 2026-11-06 06:58 UTC，停止记录于 2026-11-06 10:33 UTC。后续整理与验证不包含模型运行。

## A. 数据情况

- CSV：36 份（Train 18、Test 18），共 5,600 行。Train Safe/Unsafe 各 1,932 行；Test 各 868 行。
- 配对：Train 1,932 对，Test 868 对，合计 2,800 对。每对恰有一条 Safe、一条 Unsafe，且两侧文本严格一致；CSV 层面无无效配对。论文的 3,864 Train、1,736 Test 对应**行数**，不是配对数。
- Test 九类配对数：ethical_violations 97；illegal_activities 96；misinformation 95；offensiveness 95；physical_harm 81；privacy 100；property_damage 100；religion_belief 90；violence 114。
- 用种子 20261105 按类抽样 4 对，共 36 对。候补顺序已保存，未补样。
- 72 张目标图片中，70 张下载并由 Pillow 验证；35 对两侧完整。`test/misinformation/45` 的 Safe 和 Unsafe 两张图片因 TLS 连接错误未下载成功。70 张已下载图片中未发现相同 SHA256。
- Train/Test 无严格相同文本；Train 内有 1 个重复文本的配对 ID。全量图像字节级重复与视觉近重复未验证。
- 数据异常：442 对的 CSV `index` 与图片文件编号不同；按 CSV 原始图片文件名和 split/category 显式映射后，仓库列表中全部可定位。297 条 Unsafe 的 `category` 注释与 CSV 所在类别的规范写法或语义不同；保留源值，不将其当作 Safe/Unsafe 金标。Train 的 `region_belief` 与 Test 的 `religion_belief` 命名不同。
- Stage 0A 与 CSV 配对审计通过；Stage 0C 未通过完整图片下载，**整体 Stage 0 未通过**。所有对照图的审核状态仍为 `pending_review`。

## B. 模型情况

- 计划顺序：`Sandy124/ThinkingGuard-8B`，revision `76892f9768ce828268265171f4bbc5dfb75eafc3`；随后 `Qwen/Qwen3-VL-8B-Instruct`，revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`。
- 独立 venv 可导入 PyTorch 2.9.1+cu128、Transformers 4.57.3、bitsandbytes 0.48.2、accelerate 1.12.0、huggingface_hub 0.36.0；`Qwen3VLForConditionalGeneration` 可用。NF4 配置已写入代码，但**未加载任何模型**。
- ThinkingGuard 权重下载反复发生 HF CAS 解码错误、HTTP TLS 错误及超时；权重不完整。Qwen 8B 因时间停止条件未开始下载。
- 峰值模型显存、推理速度、输出解析率及 CPU Offload：**均无实测值**。本次 GPU 推理占用为零。

## C. 实验结果

36 对 Joint / Text-only / Image-only 推理均未运行。所有 Accuracy、Unsafe Precision/Recall/F1、误报漏报、PairAcc、风险翻转、四象限、Wilson 区间、模型配对 Bootstrap 及确定性复测均不可计算。`predictions.jsonl` 为空；不得将缺失结果解释为模型表现。

主要工程失败 ID：`test/misinformation/45`（两张图片下载失败）。模型下载故障详见 `failures.jsonl` 和 `../model_download.log`、`../model_download_http.log`、`../shard_download.log`。

## D. 科研审计

**已验证：** CSV 数量、配对关系、文本严格一致、Test 类别分布、仓库图片路径存在、固定抽样顺序、70 张图片可解码及其 SHA256。

**未验证：** 缺失的两张图片、全部图片字节/视觉重复、图片是否构成可信因果反事实、模型加载显存和任何分类效果。

**异常：** CSV 行 index 与图片编号不一致、Train/Test 类别命名差异、Unsafe `category` 注释不统一、公开文件下载不稳定。

**尚不能得出：** 反事实图片具有因果效度、ThinkingGuard 优于基座、36 对或更大样本的泛化性能。

## E. 下一步建议

**暂不扩展到 90 对。** 先完成当前 36 对的两张缺失图片与模型权重下载，并在同一预注册样本顺序上完成最小推理和人工图片审核。

## 文件与检查

- CSV 审计：`../../data/manifests/dataset_schema.json`、`pair_manifest.csv`、`data_audit.json`、`data_audit.md`、`invalid_pairs.csv`。
- 抽样与图片：`sampling_order.csv`、`sample_manifest.csv`、`image_audit.json`、`contact_sheets/`。
- 运行记录：`run_config.yaml`、`environment.json`、`model_revisions.json`、`dataset_revision.json`、`predictions.jsonl`、`metrics.json`、`metrics.md`、`failures.jsonl`、`gpu_usage.csv`、`stdout.log`、`audit_summary.md`。
- 静态检查：`python3 -m compileall -q scripts` 通过；`.venv/bin/python -m pip check` 无依赖冲突；数据不变量断言通过。模型推理脚本未进行运行时验证。
