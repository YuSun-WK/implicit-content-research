# H1-K0 TriggerBench 实验完整性审计

审计对象：唯一运行 `h1_k0_20261106_065826`。状态：**中途中断的 Stage 0 运行**；不存在已完成的模型实验或可合并的其他运行。审计仅读取现有文件，未调用 GPU、下载或修改原始结果。

## 已实际完成

- 36 份 CSV 的结构审计；2800 个配对键，其中 Test 868 对、Train 1932 对。Safe/Unsafe 两侧均存在且文本严格一致。论文的 3864/1736 是行数。
- Test 分层固定抽取 36 对，每类 4 对，种子 20261105；36 个 `pair_id` 唯一，均属于 `test`。抽样及候补顺序保存在 `sampling_order.csv`。
- 70/72 张目标图片下载并经 Pillow 解码；35/36 对两侧图片完整。70 张 SHA256 均不同。9 张 contact sheet 在本地生成，图片审核状态均为 `pending_review`。
- 独立 Python 环境完成静态架构和依赖检查；`Qwen3VLForConditionalGeneration` 可导入。

## 部分完成

- `test/misinformation/45` 的 Safe/Unsafe 图片下载失败；未静默补样。
- ThinkingGuard 8B 权重下载反复出现 CAS、TLS 与超时错误，权重未完整取得。
- NF4、分类提示及评估代码已编写，但没有模型加载或推理运行记录。

## 未执行

- 实际运行模型：**无**；实际模型权重版本：**无运行中的版本**。`model_revisions.json` 只记录拟用 revision 与下载状态，不能当作模型运行证明。
- Joint、Text-only、Image-only 的实际预测数量：均为 **0**。ThinkingGuard 与 Qwen3-VL 8B 对照：**未完成**。
- `predictions.jsonl` 存在但为空，因而没有原始模型输出、解析成功率或 INVALID 预测。没有 OOM 记录；也没有模型加载可证明显存满足上限。
- Accuracy、Unsafe F1、PairAcc、FNR、FPR、正确风险翻转率、Wilson 区间及配对 Bootstrap：**均未计算**。`metrics.json` 明确为 `not_run`。
- 官方五步提示补充推理、重复输入稳定性检查、人工因果反事实审核：未执行。

## 静态一致性检查

- `pair_manifest.csv`：2800 个唯一 `pair_id`，每对有 Safe/Unsafe CSV 引用；选样的 36 个 ID 均能关联到该清单。Test/Train 由 `split` 区分，样本仅来自 Test。
- 预测文件 0 行，因此不存在可观察的重复预测、模型混合、提示词混合、INVALID 强制改标，或将 Text-only/Image-only 当独立金标准确率的**已发生**问题。也不能据此证明未来运行会避免这些问题。
- 评估代码按 `pair_id` 聚合 Joint Safe/Unsafe，Wilson 计算在代码中；未运行，统计实现没有结果级验证。
- 运行配置含 seed、NF4、batch size、最大生成 token 等参数；推理脚本定义三种提示和 `prompt_id`。没有执行日志证明这些参数曾被使用。
- 全部 JSON、JSONL、CSV 可解析；Python 文件通过语法检查。原始预测和失败记录未改动。

## 实现存在疑点

1. `run_inference.py` 未自动执行主协议解析成功率低于 95% 的停止门槛，也未实现官方五步提示及重复输入确定性检查。因未运行，这些是代码缺口，不是实验失败率。
2. `evaluate.py` 对重复的同一模型、同一 pair、同一 side 的 Joint 记录会在字典构建时覆盖，未显式拒绝重复。当前预测文件为空，未发生覆盖。
3. 图片映射依赖 CSV 原始 `image_path` 的文件名。442 对 CSV `index` 与图片编号不同；需人工核验这种映射确实对应同一反事实配对。
4. 全量图像的字节级重复、感知近重复和因果可信度未验证；70 张已下载图片无相同 SHA256 不能外推到全量。
5. 297 条 Unsafe `category` 注释与文件类别的规范写法或语义不同。类别从 CSV 文件名获得，Safe/Unsafe 金标从文件名后缀获得；需确认此规则与数据集发布者意图一致。

## 需要 ChatGPT 进一步核验

1. 442 个 `index`/图片编号不一致的映射规则和抽样中对应图片的语义配对。
2. `test/misinformation/45` 缺图对本轮固定抽样完整性及后续补齐记录的影响。
3. 推理脚本在实际运行前需补上的解析率停止门槛、重复输入检查和官方提示实现。
4. 评估脚本对重复预测、INVALID、pair 为统计单位的处理。
5. `pending_review` 图片对是否真的只改变风险相关视觉因素。

## 上传边界

仓库归档只包含代码、配置、CSV/JSON 文本清单、空预测文件、`not_run` 指标、审计报告及脱敏日志摘要。原始图片、contact sheets、模型权重、缓存、虚拟环境和原始异常堆栈不上传。原始文件仍保留在本地运行目录。
