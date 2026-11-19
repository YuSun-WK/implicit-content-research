# VLSU ICLR 2026｜Stage 0 原论文协议与版本审计（2026-11-19）

## 状态与范围
**STAGE0 STATIC AUDIT — NO GPU RUN.** 仅为原论文零样本复现，不训练、不迁移、不开展 CRTL/CSSC。原文来源：https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf （44 页、正式 ICLR 2026）；预印本 https://arxiv.org/abs/2510.18214 可能与正式版不同。官方 https://github.com/apple-aiml-research/ml-vlsu 。

## 来源固定
- Apple 仓库 HEAD：`cbe363a26d2129ff1b526c283af0a2b7aa3d9b28`；CSV Blob：`09421adeb2e68eac1d5e829dcbd48848f21a0be6`，路径 data/VLSU.csv；前轮本地 SHA256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`，Stage1 须在实验服务器独立校验。
- 本轮经 GitHub Blob 全文独立 CSV 解析：8159 行且均九列、8159 UUID、8157 不同 URL、7638 不同 prompt；图像标签 safe=4182,borderline=1810,unsafe=2026,not_sure=141；文本 safe=4328,borderline=1452,unsafe=2379；联合 safe=2189,borderline=3310,unsafe=2660。25 个原始三元组，排除 not_sure 后 19 个标准组合，其中相较论文17个额外 B-S-S=1、S-U-B=1。
- 论文：8187 条，联合 S/B/U=2186/3312/2689，17 模式。差异 28 条的成因未证实；不可自行对齐、删除、补造或换图。图像下载成功率**未全量实测**。前轮 PR #78 的132 URL分层小试108可解码，非全样本可用率。
- 重要模式：S-S-S=2166，S-S-B=58，S-S-U=35，U-S-B=924，U-S-U=142，B-B-U=32，U-U-U=744。含 not_sure 图像的141条：联合任务可保留；三侧真实标签交集分析不可把其映射为 Borderline。
- PR #78： https://github.com/YuSun-WK/implicit-content-research/pull/78 ，审计文件 06_experiments/VLSU_research_plan_20261118/01_Current_Research_Audit.md 在该PR头分支而非主分支。本分支不修改该规划、综述、H1实验。

## 原文图表准确映射（正式版本）
| 来源 | 真正任务 | 原文设置 | 本地目标/判定 |
|---|---|---|---|
| Table 1 | 跨基准二分类，VLSU列 | S、B -> Safe，U -> Unsafe；Appendix D.1 binary prompt | Qwen2.5-VL-7B zero-shot joint；作者 Acc 50.0, F1 55.3；其他基准不强制；PARTIAL |
| Table 2 | Joint三分类 + Structured CoT | Appendix D.1 三分类，D.3 CoT；同模型 same subset | Qwen7B Standard Acc49.4 F1 42.3，CoT Acc52.1 F1 51.4；PARTIAL |
| Figure 3 | 17组合joint准确率 | 真正的per-pattern性能主图；分类任务 | 基于实际可访问图逐组合计算，附样本量和Wilson CI；PARTIAL |
| Figure 4 | image/text 预测与 joint预测相关性/混淆 | 按all、joint correct、joint wrong分组比较 | 在三模式同UUID有效交集上算成对混淆/Cohen kappa；PARTIAL |
| Figure 5 | joint预测错误四类来源 | 按image-only、text-only正确与否4类分解，分母是joint errors | 同时报告 P(BothCorrect|JointError) 与 P(JointError|BothCorrect)；PARTIAL |
| Table 4 | image-only/text-only/joint三分类 | 分别用 image_grade/text_grade/combined_grade | Qwen7B image Acc65.2 F1 48.0；text 60.3/44.2；joint 49.4/42.3；PARTIAL |
| Table 3 | Harmless/Helpful指令下拒答/帮助 | Gemini1.5、Qwen32B，GPT-4o judge | 原始行为指令全文及等价judge不可完整确定，不跑替代为“原论文复现”；NOT RUN |
- 作者报告的 F1 未在已核验正文/附录明确声明macro或weighted；不能无凭据把作者 F1 标作 Macro-F1。当地计算并报告macro/weighted/per-class，作者数值独立列为“F1 (averaging unspecified)”。
- Figure 5 作者主要展示的约33.8% Both Correct 来自 Qwen32B 的joint错例，不是7B本地预期值。
- Figure 4 和 Figure 3 不能混淆。论文 Table 1 vs Table 2/4 标签空间不同，不能直接类比 F1。

## Prompt/实现缺口
- 正式版 Appendix D.1 公开二分类、joint三分类逐字模板；D.3公开Structured CoT逐字模板（最终行[Final Classification]）；D.2为Refusal/Helpfulness **judge** 模板而非被测试模型的“Helpful”行为指令。
- Appendix D.4 Table10指定 Qwen/Qwen2.5-VL-7B-Instruct，1024 direct / 2048 CoT 的 Max Len，图像 min=256 max=1280（数值的像素/token单位与processor转换需核查）；Qwen家族温度使用“default”，不能自行声称温度=0为原设。作者报告在A100-SXM4-80GB上运行（<12B单卡），不是本项目4-bit。
- 公开仓库顶层仅 README、LICENSE、LICENSE_DATA、data、docs、utils；utils/save_dataset_images.py为下载辅助，未找到完整17模型统一推理/预测解析/评测代码。
- 尚未明确/未公开：Qwen权重revision、原代码依赖和随机种子、message包装格式、unimodal专用prompt、二/三类parse-fail归因、F1 averaging、作者图像缓存快照、Table3 behavior提示全文。缺失部分须建“UNKNOWN/NOT PUBLICLY VERIFIED”证据行，避免猜测；本地选择一套可重复实现时必须明确标 PARTIAL REPRODUCTION。

## 实验与样本规则
1. E1三个独立任务：Image-only只在 image_grade∈S/B/U（最多8018行）；Text-only在全8159有效文本；Joint在全8159有效联合、但须成功解码图片。
2. E2必须使用原 binary prompt：joint gold (S|B)->Safe，U->Unsafe；不要使用三分类预测后折叠。
3. E3三分类direct独立保存 raw_output、parse_status、gold、pred、UUID；解析失败率与有效输出条件指标双报，主口径分母含解析失败。
4. E4按真实S/B/U三元组分类，额外2个单例和not_sure单列；小组Wilson 95% CI。不从模型输出反推模式。
5. E5同权重、同输入样本、同配置控制，D.1与D.3两条prompt；CoT只解析最终字段，不从解释正文任意抓标签。
6. E6四类型按joint错误条件划分：image错/text对、image对/text错、两者错、两者对；共同有效交集，同组可引导但不能证明表征因果。
7. E7先审计不跑；Table3是生成拒答权衡非安全分类。
8. 同UUID配对比较; log Git/data/model commit，HF revision，processor/preprocess，CUDA/PyTorch/Transformers，seed，beam/sample，max_new_tokens，actual generated tokens，image pixel budget，max GPU allocated/reserved，OOM，output parse status。作者无法证实的参数不得宣称一致。

## 资源与继续门
- 公开 HF 模型约8.3B 参数，BF16权重本身~16.6GB（十进制），加activation/KV/视觉分支和CUDA开销可能超过20GiB目标；优先试本地可用原始bf16，超预算时4-bit量化并明确“RESOURCE-CONSTRAINED PARTIAL REPRODUCTION”，不冒充作者原精度。量化后显存约8–16GiB是**预估，不是本机实测**。
- 图片：8159 URLs；若成功图像平均0.2–1.0MB，则~1.6–8.2GB，仅用于容量计划，极端图片可更多；下载前设置最大单图字节和最大像素；磁盘建议预留80GB以上共享缓存空间，按实际盘况调整。
- 推理上限：E1 8018(image)+8159(text)+8159(joint)=24336次；E2另8159；E5 CoT另8159，共40654次生成（E4/E6分析可复用E1输出）。真实耗时必须由20样本Smoke和分层Pilot按模式、p50/p95、生成token数实测外推，每GPU作业硬上限6h且可中断续跑。
- Stage0: CPU文献/代码/数据证据审计；Stage1: 全量下载与覆盖审计；Stage2: 10–20样本Smoke；Stage3: 分层Pilot；Stage4: 有效数据全量；Stage5: 原文对照。完成每步先检查审计门，不跳步。

## 版权/工程风险
数据 LICENSE_DATA 为 CC-BY-NC-ND 4.0，代码为 Apple Sample Code License，第三方图像不受CSV许可自动覆盖。勿push原图、权重、未经许可CSV副本、包含有害原样本的case gallery；只保留UUID/汇总/配置、允许披露的日志，原始模型输出若涉及敏感内容须检查分享限制。下载需断点续传、每URL失败原因、相同host限速/指数退避、去重、字节哈希、MIME+Pillow decode、原网页可变性与域安全防护。
