# TRACE Stage 0 代码与梯度审计

固定上游 `83ecb799f897fe275185e082ee9a669f7d04bfaa`。下面的行号对应固定源码。参数清单来自实际构造的 Hugging Face CLIP 配置和作者分类器，使用 CPU 主机上的 PyTorch meta device，权重未加载。梯度作用范围来自源码和计算图，真实 FHM 的梯度仍待测。 [固定源码](https://github.com/surrey-nlp/TRACE/tree/83ecb799f897fe275185e082ee9a669f7d04bfaa)

## 数据、特征与 Caption 选择

- `clip_vitL_14_ft.py:35–98,290–341,426–448` 读合并 JSON。训练使用 `train`，旧验证合并 `dev_seen` 和 `dev_unseen`，作者随后分别评估两个 test split。样本由相对路径 `img`、二元 `label`、`split` 和按原顺序排列的 `text`、`ivl_8b_new_caption`、`gemini_caption` 组成。作者在固定私有路径下预加载图像，缺图时 collate 会跳过。缺列默认保留 `No caption`，Pandas 的缺失值可能变成 `nan`。真空字符串被移除。包装层在 Train/Dev 上检查来源声明、图片、标签及三条有效候选，按需读取图片。
- 批输入像素 `[B,3,224,224]`，token IDs 和注意力掩码 `[B,C,77]`，标签 `[B]`。每条合法输入的候选数 `C=3`。作者 collate 对变长候选补零。在 `utils/loss_functions.py:302–397`，掩码由每条候选的 token 注意力和是否正数得到，整列无效时跳过。无效分数在采样前乘零，采样后再乘掩码并归一化。硬采样若抽中零分的无效项，该行可变成全零。严格门禁排除了这种变长输入。
- `utils/loss_functions.py:319–377,482–503,558–572` 中 vision pooler `[B,1024]`、text pooler `[B,C,768]`；CLIP 自带 projection 另给 `[B,768]` 和 `[B,C,768]`。`get_image_features` 重跑一次视觉塔，`get_text_features` 对每个候选重跑一次文本塔，默认对比损失关闭时仍会运行。训练直接调用 `calculate_loss_gs` 和作者子模块。`CLIPClassifier.forward` 自己也有重复编码（L269–287）。
- `utils/loss_functions.py:381–397,482–503` 默认模式使用 Scorer，训练用 hard straight-through Gumbel-Softmax，评估用普通 softmax 加权。cls-only 训练仍用 Scorer，cls-only 推理改用余弦。cls+cont 使用余弦，三项全开使用 Scorer。改变 loss 开关同时会影响选 Caption 的条件。
- `utils/caption_selection.py:104–226,228–348,404–427` 是独立离线辅助函数。优先 Scorer 的 sigmoid argmax，其次使用图文投影余弦 argmax；cls-only 此处仍用 Scorer。辅助函数跳过整列 padding，若 argmax 超出该样本的候选范围则回退第一条。作者训练/验证预选调用被注释，测试辅助调用的返回值未被 `calculate_loss_gs` 消费（训练脚本 L545–567、L621–653）。辅助函数的 argmax 与实际推理的 softmax 混合是两条路径。

## 参数、张量与梯度

`clip_vitL_14_ft.py:101–237` 冻结整个 CLIP，再开启 12 层文本 tower 的零基第 4、7、10 block（L122–130）。词嵌入、文本末端 LayerNorm、CLIP 内建双塔 projection、温度参数和整个视觉塔冻结。共 **445,480,710** 参数，其中 **39,127,813** 可训练，约 **8.78%**。逐参数名称、形状和 `requires_grad` 见 [parameter_manifest.csv](parameter_manifest.csv)。

| 模块名或参数前缀 | 可训练参数 |
|---|---:|
| `clip_model.text_model.encoder.layers.{4,7,10}` | 每层 7,087,872 |
| `caption_scorer` | 3,421,697 |
| `image_projection` | 1,051,648 |
| `text_projection` | 789,504 |
| `cross_attn`、`cross_attn_reverse` | 各 4,198,400 |
| `pre_output` | 4,203,520 |
| `classifier` | 1,025 |
| `log_vars` | 3 |

`clip_vitL_14_ft.py:140–267` 的 Scorer 是 768→1024→1024→1024→512→1 MLP，含 LayerNorm、GELU、dropout 及部分 Linear 的 weight normalization。TRACE 自有投影映射两个 pooler 到 1024，双向 8-head attention 的 Q/K/V 均为 `[B,1,1024]`。单 key softmax 恒为 1，理论上 Q/K 对选择权重的导数为零；V/out 有梯度通路。带残差的双路拼成 `[B,2048]`，经过三层 pre-output、分类器，得到 `[B]` logits。检查融合梯度应按模块汇总。

| 损失与出处 | 计算与梯度可达范围 |
|---|---|
| 分类 `loss_functions.py:558–586` | 分类 logits 与标签做 focal。更新分类器、pre-output、两路 TRACE projection、attention 的 V/out、所选文本特征上游和 `log_vars[0]`。Scorer 选择分支中，梯度又沿 straight-through 权重到 Scorer 和文本 block。余弦选择时梯度经冻结的 CLIP 文本 projection 回到可训练文字 block。 |
| Relevance `loss_functions.py:623–649` | 有效候选的**原始 Scorer logits 均值**与同一条 meme 二元标签做 focal。绕过 Gumbel 权重、融合和分类器，直接到 Scorer、文本 block、`log_vars[1]`。标签监督单位是样本。上游 `.squeeze()` 在 `B=1` 将标签变成标量并导致 BCE shape 错误。CPU fixture 实测复现。 |
| Contrastive `loss_functions.py:588–621` | ViT-L 路径对归一化图像投影与选定文本投影计算 `[B,B]` 相似度矩阵（温度 0.07），双向交叉熵更新文本 block、选权路径和 `log_vars[2]`。只有启用 relevance 的 Scorer 选择路径才使对比梯度到 Scorer。无融合或分类器梯度。单样本矩阵只有一个类别，CE 梯度为零，梯度累积也不会产生跨 microbatch 负例。默认禁用。 |

有效项各加 `exp(-s_i)*L_i + 0.5*s_i`。Focal（L11–57）为带 logits 的 BCE 乘焦点因子和类权重，另混入 0.1 的原 BCE 项（目标未作显式平滑）。冻结视觉塔可提供输入特征，参数不会收到梯度。

## 代码与论文差异

- 论文 §3.2 描述 BCE 和按 Gumbel 概率之和写出的 relevance 项。归一化概率之和恒为 1，公式按字面无法表达随候选改变的监督。实际代码对原始分数均值做 focal，并学习损失权重。论文 Table 5 对 ViT-L/14 给出最后四层 T(-4) 的结果，固定脚本开启三个不相邻块。论文的物理 batch 为 64、有效 batch 可达 512；脚本为 128×4，最多 30 epochs。此处保留源码层位和损失，Stage 0 固定首 epoch 温度 1.0。 [AAAI 论文](https://ojs.aaai.org/index.php/AAAI/article/view/41220) · [作者扩展版 §3.2–3.3、Table 5](https://arxiv.org/html/2504.17902v2)
- `vg_caption_gen.py:23–33,49–134,205–301,358–405,448–515,546–597,685–794` 中 RAM++ 依赖未随仓库发布的 `ram_plus_swin_large_14m.pth`，基于标签运行 `IDEA-Research/grounding-dino-base`（框阈值 0.4，文本阈值 0.3）。Gemini 路径把图像和 GroundingDINO 标签、框及置信度写入模型请求；入口尝试补合并 JSON 缺项。脚本通过 `google.generativeai` 和环境密钥调用 `gemini-2.0-flash-exp`；论文报告 Gemini-2.5-Flash 与 InternVL-2.5-8B。InternVL2.5 模型加载及主循环调用在固定脚本中被注释。源代码无法独立证明私有 Caption 文件出自哪个模型修订。
- `clip_vitL_14_ft.py:343–397,502–522,596–647` 原始评价在传入 split 的标签上选择 PR 曲线最大 F1 阈值，覆盖 test。PR 精确率/召回率数组末端没有对应阈值，极端时可能索引越界。脚本按 Dev AUROC 监控，`best_model.pth` 每次走到保存处都被覆盖，恢复后又重置 `best_val_auc`，测试使用末次内存模型。Stage 0 包装使用固定 0.5 或独立 Dev PR 校准并记录冻结阈值，训练包装无 test scoring 入口。`benco_eval.py:15–18,171–176,192–211,284–290` 另依赖未随仓库提供的旧导入路径和 XLM-R 权重，按伪索引分组且在 test 标签上拟合阈值。
