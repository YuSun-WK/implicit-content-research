# R6-Fix-R1｜Gate D正式PDF定点核验续补

> 2026-11-10；问题P1-12／Gate D。前一次修订因正式PDF访问超时，仅完成作者版交叉检查；本次已成功取得正式PDF并直接查看Figure5和Figure18，原访问阻塞已消除。科学修订固定commit：`216c0aa4ba706cdf130913d31ecc4b3138e52127`。**执行完成不等于独立学术审稿CLOSED。**

## 1. 固定来源与实际访问

VLSU，ICLR 2026 Conference（CCF-A）：[正式出版页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)，[正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)。PDF首页标记为正式会议论文，文件共44页，6,636,319字节；本次取得的文件SHA-256为：

`b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8`

本次既读取正文／图注文本，也直接查看了PDF第8页和第39页的实际图像。以下页码为PDF从1开始的页序，与印刷页码一致；不将摘要页的泛化表述当作模型汇总统计。出版页仍写11模型，正式PDF写17模型的既有版本差异继续保留。

## 2. Figure5：模型与条件分母

| 要核的内容 | 正式PDF直接证据 | 稿件应如何写 |
|---|---|---|
| 哪个模型 | [第8页Figure5](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf#page=8)饼图内标题明确标Qwen2.5-VL-32B | 指定这一模型示例，不能写为17模型统一结果 |
| 图的对象 | Figure5图注为“Error breakdown of combination errors by types”；同页§5说明把joint图文分类错误拆为四类 | 分母是该模型joint三分类已经错误的集合 |
| 33.8%的分子 | 图内Both Correct扇区为33.8%；§5将其定义为图像单独与文本单独分类均正确、联合分类仍错误 | 分子是joint错误集合中两个单模态各自预测正确的样本 |
| 其余类别 | 图内另列Image Wrong 32.3%、Text Wrong 25.9%、Both Wrong 7.9%；四项因显示舍入合计99.9% | 这是错误构成分布，不是全数据集发生率，也不是严格S-S-U漏检率 |

用评测符号表达，该图33.8%对应作者报告的条件比例：

\[
\frac{\#\{\hat y_J\ne y_J,\;\hat y_I=y_I,\;\hat y_T=y_T\}}
{\#\{\hat y_J\ne y_J\}}.
\]

此式是综述对作者错误分组的记录方式，不是作者新损失函数；本次没有获得逐例预测并重算该比例。不能由舍入饼图反推出精确错误条数，不能用8,187／8,159或S-S-U的37／35替代上述分母。

## 3. Figure18：不同模型分别统计

正式PDF第38页附录E.3明确把Figure5扩展到其他模型；[第39页Figure18](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf#page=39)分别展示GPT-4o、Gemini-1.5、Gemini-2.5（R）、Qwen2.5VL 7B／32B／72B六个面板，各面板的错误构成不相同。该页Qwen32B面板的Both Correct显示为取整后的34%，与Figure5的33.8%舍入相容；不能把六个面板或全部17个模型不加权合并后仍称33.8%。

同页Table12亦直接核到正文C3已用的Gemini与Qwen双侧拒答数字，因而C3的这一来源已改链至正式PDF，而不是仅指向作者v2。该表是回应行为结果，不是图文风险分类F1。

## 4. 实际修改及余留边界

- 正文§7.2固定第377行：引用正式PDF第8／39页，明确图内模型名、错误分母及分模型扩展；移除“正式PDF未打开”的过期状态。
- 表6第8行及版本注同步；正文C3的VLSU行为证据改链至正式E.4 Table12。
- 八项台账、来源／验证记录、原R6-Fix数据审计与总台账、PR #63状态同步为“8项已实施，待独立复审”。
- 未改变固定CSV重计8159／35／141；PDF与CSV差28条原因、图像实际可达性／授权、原模型逐例预测仍O。
- 这是正式原文P级证据核验，不是模型复现，也不独立证明模型内部推理的因果失败。R6-V书目与渲染工程验收、两项P0的学术终裁仍独立进行。

后续独立复审只需按原Gate D要求核对所列正式页及修订措辞，不再需要用户补传原PDF；不自动合并任何PR。
