# Stage 2｜InternVL 单生成器 Caption 来源与流程

模型名称：**TRACE-InternVL-only-MultiOFF-2caption**。生成数据仅位于 Git 外的私有目录 `~/data/trace-assets/multioff/trace_internvl_only/`；本仓库只保存聚合统计和模型哈希。

## 固定来源

- TRACE 作者代码：`surrey-nlp/TRACE@83ecb799f897fe275185e082ee9a669f7d04bfaa` 的 `MultiOFF/multioff_cap_gen.py`。作者默认运行路径使用 Gemini，InternVL 加载与调用被注释；存在固定 `cuda:1`、作者机器绝对路径，以及三份 CSV `concat` 后重复索引用 `df.loc[i]` 写回的错配风险。来源：[作者固定脚本](https://github.com/surrey-nlp/TRACE/blob/83ecb799f897fe275185e082ee9a669f7d04bfaa/MultiOFF/multioff_cap_gen.py)。
- RAM++：`xinyu1205/recognize-anything@7cb804a8609e9f4b1a50b7f31436d2df40bb9481`、官方 `ram_plus_swin_large_14m.pth` 固定 Hugging Face revision。
- GroundingDINO：`IDEA-Research/grounding-dino-base@12bdfa3120f3e7ec7b434d90674b3396eccf88eb`。
- InternVL：`OpenGVLab/InternVL2_5-8B@e9e4c0dc1db56bfab10458671519b7fa3dd29463`，四个 BF16 权重分片及全部 `trust_remote_code` Python 文件来自该固定 revision。[逐文件 SHA-256 与字节数](Stage2_Model_Asset_Manifest.json)。

## 实际生成路径

[独立包装层](stage2_caption.py) 按官方 CSV 各自枚举原行号，用 `split + 原CSV行号 + image_name + image_sha256` 构成稳定键。只纳入有可解码原图的 444/148/148 条。RAM++ 提取标签，GroundingDINO 以作者的 0.4/0.3 门限定位对象；三模型分进程串行占用单卡。InternVL 使用 448 像素的作者预处理、视觉定位置信度提示、原始 Meme 文字和作者的主要语义提示；提示词明确要求避免直接给出 offensive/non-offensive 标签。**真实分类标签未进入提示词。** 输出必须有 `Caption:` 标记且非空。每 25 条以内原子更新私有清单，重启时按稳定键与原图 SHA 核对并跳过成功项。

作者生成配置的 `max_new_tokens=4096` 在本轮设为 **256**，`do_sample=False`，BF16、无量化。由于当前 Transformers 4.57 的生成缓存与固定 InternVL 代码不兼容，生成进程使用隔离的 Transformers **4.49.0** 与 Tokenizers **0.21.4**；训练进程仍使用原隔离环境的 Transformers 4.57.3。RAM 与新版库的旧导入位置，以及 GroundingDINO 的 `box_threshold` 参数名称，均在包装层作接口适配；作者上游文件未更改。

## 真实结果

先运行 10 条，再运行 50 条 pilot，最后补齐全部 740 条。50 条 pilot 中 50/50 非空、无原文直接复制，Caption 生成中位数 **3.15 秒**，峰值 PyTorch reserved **17.02 GiB**。全量 740/740 非空、无原文直接复制；Train/Dev/Test 为 **444/148/148**。全量生成中位数 **2.86 秒**、p95 **4.66 秒**；InternVL 进程峰值 allocated **16.53 GiB**、reserved **17.22 GiB**。生成过程没有使用 Gemini 或付费 API。[50 条 pilot](stage2_caption50_pilot.json) · [全量覆盖与分词统计](Stage2_Caption_Coverage_Manifest.json)。

OpenCLIP RoBERTa 的 77-token 输入限制下，**334/740** 条增强 Caption 超限，正式训练时被分词器截断。作者提示虽要求低于 77 token，实际生成未全部遵守。本轮保留统一生成配置并在结果解释中保留这一差异。自动检查覆盖、空值、占位和原文复制；没有将主观语义质量打分伪装为人工标注。
