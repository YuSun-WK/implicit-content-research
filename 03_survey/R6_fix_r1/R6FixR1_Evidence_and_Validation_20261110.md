# R6-Fix-R1｜定点证据与实际验证记录

> 2026-11-10；初版科学文件固定`29f225ca232a450c07b723e2678e25072f370b04`；Gate D续补科学文件固定`216c0aa4ba706cdf130913d31ecc4b3138e52127`，基线PR #61 `c125c6358c655951d07286763f3b7a3eed6e9275`。以PR #62八个Gate为范围；下列状态是实际访问／静态核对，不是独立学术终审或模型复现。

## 1. 本轮实际取得的作者公开文件

文件内容按固定commit重新读取；下列blob是接口返回的文件标识。正文附录A已自含40位commit、file#line、静态观察及O边界，六组证据不需要读者访问本私人工作库。

| 组／文件 | 固定commit | 返回Git blob SHA | 本轮状态 |
|---|---|---|---|
| RV-HATE `ppo_eval.py` | `acfe053172a7266c8dde3759551882701478cdac` | `674e9aecdcef0629a03bd782d9b564d13956aab8` | 直接核19–67与155–180行；无训练 |
| CADET `src/cadet/datasets/dataloader.py` | `1f1a25d56907c9aa83f9285ce32753a6945097f6` | `d7d63fadfb3a3db9471a20f63cfe8da1bbf92536` | 直接核119–142与257–313行 |
| CADET `src/cadet/training/cadet_trainer.py` | 同上 | `a96ceb0b5fe9dd3b025ba6172537898646c25a47` | 直接核219–252行 |
| MultiMM `code_metaphor/data_utils.py` | `33a01f111208b2ddbacdb06a667828c1246cc42b` | `2c2c297e26b5e4e6a78377b0747fb106d6ee6fce` | 直接核67–100与150–159行 |
| MGMCF `loaddata.py` | `02407e81099db63674ff27d97ee332011fcf4be0` | `ca43b0a4820eda396cc95fd81ef4c55445052212` | 直接核12–25／55–78／103–109行；未取得pkl真实来源 |
| MCIB `MCIB_trans.py` | `d1430aa7bf827731b99cf4baed73525f0fd590c3` | `2570266d66e6fca4f3e4c03e0b860db4003a4416` | 直接核110–126与194–224行；未打印真实batch |
| Meerkat-VL `verl/trainer/ppo/ray_trainer.py` | `9ecb79281492bd491ef65f72647bcef893cba4fa` | `1ea3b1d987c88f8b4eff70789b2bd6962500875d` | 直接核489–616行；正式训练有效分支对应未知 |
| VLSU `data/VLSU.csv` | `b7c1780d2d578a82fc5f11a070d93bcd50cb9e45` | `09421adeb2e68eac1d5e829dcbd48848f21a0be6` | 直接读取blob全文；CSV逻辑记录8159，均9字段；S-S-U35，image not_sure141 |

以上刊会／CCF信息分别为：RV-HATE ACL2026 Main（CCF-A）、CADET WWW2026 Main（CCF-A）、MultiMM ACL2025 Main（CCF-A）、MGMCF AAAI2025 Technical（CCF-A）、MCIB AAAI2026 Technical（CCF-A）、Meerkat-VL ICML2026 Main（CCF-A）、VLSU ICLR2026（CCF-A）。这些是论文出处，不认证代码是正式run。

## 2. 为C1–C3与协议表定点核过的论文材料

| 材料／刊会与CCF | 实际可读来源和新使用位置 | 版本与未做的事情 |
|---|---|---|
| FETCH!；ACL2025 Main，CCF-A | [正式PDF](https://aclanthology.org/2025.acl-long.284.pdf) §3.4、Tables4–5；已核Balanced P/DPR/F0.5两管线数字及type/root分母 | 未重新运行输出列表与去重实现；Precision与DPR统计单位分别记录，不泛化时间外新义 |
| DRInQ；ACL2026 Main，CCF-A | [正式PDF](https://aclanthology.org/2026.acl-long.1597.pdf) §3–4、Table2；Mini／Sonnet的解释提示正反数，400题、3次抽样 | 未把引言76%等其他口径混为困难集；未下载并重建全部400题 |
| DOSE；ACL2026 Main，CCF-A | [正式PDF](https://aclanthology.org/2026.acl-long.319.pdf) §3／5、Table3、Table4；五任务MCQ、1%训练与其余评测、78.90等数据 | 不把同原始比例视作有效实例／token完全匹配，未运行训练 |
| (RSA)²；ACL2025 Main，CCF-A | [作者v1 HTML](https://arxiv.org/html/2506.09301v1) Tables2–3、Figure4；正确候选概率及字面子群反向效应 | 正式PDF因体积取读失败，故不声称本轮会议版逐页对应。正文明确数值定点阅读版 |
| VAGUE；ICCV2025 Main，CCF-A | [作者v3 HTML](https://arxiv.org/html/2411.14137v3) §3–5、Table3、附录G TableG6、H/I；CoT正反、1677总分母及拒答计错 | CVF正式PDF端点403；会议版附录表号／逐页一致性O；未使用旧3993条版本 |
| VLSU；ICLR2026，CCF-A | [正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)共44页；直接读取第8页Figure5图内模型名、饼图比例、图注／§5，以及第38页E.3、第39页Figure18与Table12 | 上轮超时已消除；正式PDF SHA-256 `b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8`；未重跑模型，数字是作者报告P；详见[Gate D记录](R6FixR1_GateD_Formal_PDF_Verification_20261110.md) |
| Ma；ACL2025 Main，CCF-A；Farabi；IJCAI2024 Survey Track，会议CCF-B；Hee；EMNLP2024 Findings，会议CCF-B、非Main | 作者正式出版页／摘要与项目既有对照交叉使用；已承认任务／数据／评测与跨模态、检测／解释／响应已有覆盖 | 本轮不伪称逐表全篇竞品穷尽审计；第1章矩阵是分析单位对比，非覆盖率优先权证明 |
| Ye；arXiv:2502.14881v1，预印本，CCF不适用 | [作者摘要](https://arxiv.org/abs/2502.14881v1)与HTML章节目录；只为新增近邻安全综述定位 | 未核正式发表状态，未声称全篇审阅或纳入其Janus-Pro实验作方法效果证据 |

ExPO-HM（ICLR2026 Main，CCF-A）的完整配置74.5／81.1和RA-HMD80.2来自已通过P0-03的原稿证据，保持其组合干预／非严格S-S-U界限；没有因为本轮重排C2就声称完成新的独立复现。

## 3. 实际检查与保护性比较

运行`python 03_survey/R6_fix_r1/verify_r1.py`返回：

```text
PASS: main text/Bib/manual references/inventory = 49 unique keys
PASS: table keys and widths; nine chapters; six immutable public source groups
PASS: stale private-only code references and unpinned release integers removed
PASS: Gate D official PDF page/model/denominator citations synchronized
LIMIT: no BibTeX compiler, publisher-field certification, rendering or model reproduction
```

另运行`git diff --check`无空白错误。旧48条Bib内容逐字为新Bib前缀，只增加Ye一条。表1／2／4逐字未改；九章结构保留。定点比较§2.4、§2.5、§6.1、§6.2、§6.3及第9章引导未改；审阅第9章全部研究议程及ExPO原§7.3、CrossGuard／ThinkingGuard已通过段落，无科学重写。六组公开链接中所有保留的代码事实均附正式run对应O；MCIB仅为有条件形状风险。

MMSafeAware／Silent Signals／MOSSBench的高精度发布差异没有本轮固定版本链，因此从稿件与相关表中撤去精细整数。这是缩窄不可证声明，并不等于证明发布差异不存在，也不否定作者论文P。

## 4. 本轮边界与下一次复审

- **八项均已实改待独立复审**：P0-01、P0-02、P1-01、P1-03、P1-05、P1-08、P1-12、P1-16。P1-12的正式PDF Figure5图题／模型／分母已直接核，前轮部分完成状态已被本续补替代。
- 独立复审按原24个去重单元，不增造问题编号；原16 CLOSED的裁决不由执行者覆盖。
- 未运行新GPU实验、下载全部图像、取得受限AUTALIC CSV、认证正式代码run或编译／渲染最终投稿文件；R6-V继续承担工程验收。
- 新PR以PR #61修订分支为base，不合并PR #57–#62，不修改R6-A／R6-V／R6-Fix-Review审稿文件；不自动合并本PR。
