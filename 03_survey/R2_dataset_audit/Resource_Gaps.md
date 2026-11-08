# Resource Gaps｜资源与标签协议缺口

日期：2026-11-08。仅供资源验收与后续实验协议设计，不含方法型创新点判断。

## 需要作者或发布方补齐

| 资源 | 缺口 | 最低核验动作 |
|---|---|---|
| DRInQ | 论文819/400与公开231无映射或完整困难集。 | 取得缺失发布文件并按官方ID/划分计数 |
| VAGUE | 核对图像可用率、字段泄漏与按原图分组划分。 | 下载公开文件并逐行/逐图比对标签与划分 |
| CodedLang | 明确可执行评测脚本、split及词项级交叉；核对发布CSV行数。 | 下载公开文件并逐行/逐图比对标签与划分 |
| Silent Signals | 16,550→16,258差292；检测100→101；消歧标签值与论文二元口径需核。 | 下载公开文件并逐行/逐图比对标签与划分 |
| FETCH! | 原始语料不可确认一键获取；静态审计记录DIRECT/recall等潜在运行问题。 | 下载公开文件并逐行/逐图比对标签与划分 |
| SeTox | 核对词项交集；作者README BibTeX与ACL正式标题、作者、页码冲突；训练搜索噪声。 | 下载公开文件并逐行/逐图比对标签与划分 |
| M3UCD | 论文规模不得写为“公开15,345”；发布链接与标签字典缺失。 | 取得缺失发布文件并按官方ID/划分计数 |
| MET-MEME | 原始10,039与第三方HF 10,030相差9；确认Kaggle实物及官方split。 | 取得缺失发布文件并按官方ID/划分计数 |
| VLSU | 论文多28条；图片实际成功率未知；not_sure及类别分布不一致。 | 下载公开文件并逐行/逐图比对标签与划分 |
| MSSBench | 1,960/1,820/724图像口径待统一；实际可运行样本数需逐条配对核验。 | 取得缺失发布文件并按官方ID/划分计数 |
| MOSSBench | 304 PNG与300标注键未一一匹配；HF contrast预览坏；需确认官方对照配对。 | 下载公开文件并逐行/逐图比对标签与划分 |
| V-FLUTE | 按图片ID/近重复和来源重分组审计；测试集阈值校准独立性。 | 下载公开文件并逐行/逐图比对标签与划分 |

## 横向标签协议风险

- **人类共识与真实意图**：DRInQ和VAGUE的GT是标注者对构造语境的判断；不应写成真实说话者已证实的心理意图。
- **词典/伪标签与逐例金标**：Silent Signals主集、FETCH!词典匹配、SeTox风险词典的证据等级不同；不能一律写“人工真值”。
- **分类与解释分离**：CodedLang的编码类别、SeTox的安全标签、MET-MEME/M3UCD的意图与冒犯、V-FLUTE的解释文本各有不同标注来源。
- **图文联合依赖**：VLSU可利用三层标签，但缺图/失效图须先统计；MSSBench和MOSSBench评估安全情境或过度拒绝，不能统一视为“图文单独安全、组合危险”。
- **泄漏须实测**：以词根、原问句、原图、meme模板、来源数据集、时间和社群为分组单位重算交叉；本轮列出的风险均为潜在风险，不宣称已发生。

## 本轮证据边界

- 本轮实读并解析：DRInQ CSV 231条/148问句；SeTox四个可返回的JSON（974、600、624、368）；MOSSBench information.json 300键。GitHub文件树核查了所有可识别官方仓库；MOSSBench图像树为304主图、244对照图。
- 既有卡实读结果：VLSU公开CSV 8,159条。本轮只确认该文件仍在仓库，未重新下载。
- 其他规模来自官方页面、数据卡或论文声明；所需图像、parquet、Kaggle包、大型训练文件均未完整下载。公开规模未知处保留“未知”。

## 使用的项目内基线

- [R0 59篇索引](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/Literature_Inventory.xlsx)；[R1任务框架](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R1_taxonomy/R1_Working_Framework_DRAFT.md)；[R2-A 32篇候选](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/R2A_Candidate_Ledger.md)。
- 既有P019/P023/P038及R2-B阅读卡仅作来源证据；本轮未修改任何阅读卡。
