# 数据可用性与逐源核查

日期2026-11-17 UTC。优先本地只读盘点，再元数据/小文件；未执行生成流水线、未提交授权申请或代用户分享个人信息。

| 来源 | 固定版本/访问 | 实际观察 | 四格阻碍与处置 |
|---|---|---|---|
| 私有FA2缓存 | PR75 aa317426；SIJA HF 4087764c55ea76946bac6634aa4d63b2ad7bb5a0 | 4源图+4cue；329/310已见预测；Cue仅2种哈希 | 无已有风险去除目标图/指令，不把换图当逆编辑；329/310仅历史探索 |
| [SafetyPairs官方代码](https://github.com/apple-aiml-research/ml-safetypairs/tree/4e1b2457e3946c54905735f43027698dfc95347d) | tree 4e1b2457e3946c54905735f43027698dfc95347d，公开，代码ASCL | 实查递归树，metadata.jsonl/图片未在tree；loader要求original.png/final.png、edit_instruction，本地路径由环境变量指定；官方README为生成流水线 | 官方成品数据入口未找到；HF按safetypairs检索返回空不证明全网不存在。代码可见不等于1510对成品可取得；未运行生成或付费GPT |
| [SafeEditBench](https://huggingface.co/datasets/tyodd/SafeEditBench) | a254fa5ea367839be72e8db39041a7a5a43633c1；gated=auto；CC-BY-4.0 | 元数据和997文件目录可见，总88,477,779 B；test_images有66原图、62个同名edited对，共128图；601为政策实例，不是601独立对 | 无缓存token；test.jsonl与单图读取遭网络错误/超时，未取得内容。页面明确须授权；不绕过门禁。卡片字段无编辑指令，不能仅靠文件名认定指令/四格完备 |
| SIJA v2正常控制 | PDF v2，31页，C.5 Table14 | 作者报告100条正常split-intent控制、generic/relaxed和成本；官方Git tree仍29231d7…仅README；HF仍旧revision，ZIP原有1535 entries无正常控制专包或编辑输出 | 本轮未发现逐例正常控制公开；作者结果不等于数据已分发；也不自动适配去风险四格 |
| [MagicBrush](https://huggingface.co/datasets/osunlp/MagicBrush) | 元数据6c254560879df7851233ea0fd2ae2a62764d0ef2，CC-BY-4.0 | 复用4源图缓存，刷新viewer目标链接后2目标图解码成功，2失败；6张图哈希记录于CSV/私有包 | viewer响应未带commit字节绑定，来源revision仅元数据声明；2完整普通编辑对不含已核实Iu/er；全部PENDING，不作安全标签 |

候选资料在任何本轮预测之前确定，沿用缓存4条dev记录，不按模型结果挑样。公开CSV为4份资料而非4个合格四格组；2份缺目标，另2份在CODEX观察下属于普通背景/对象编辑，不能据此人为设风险。没有凭数据集名字分配ALLOW/BLOCK。

重复隔离：同源与原始编辑对的两侧必须同split；已对6个可用图片做字节SHA256及dHash(9×8,阈值6)筛查，跨资料近重复标记见logs/candidate_availability.json。dHash仅筛查，不替代语义审核，冻结前还需两人查看。源对/近重复连通分量不得跨dev/test；Cue复用独立统计，不把Cue相同或ID不同算独立机制。当前未冻结任何split。

er在Is上语义、完整风险移除、en确实保留风险、其它残留违规与授权背景均未得到证实，因此没有四格标签。审核包提供实际图像/来源指令与空表，允许逐项排除，不要求审核者“创造”风险。

访问失败与数据未发布严格分开：本轮SafeEdit是gating+网络阻碍；SafetyPairs是未定位成品入口；不能把两者写成永久不可获得。SafeEdit约84.4MiB的整个当前树仍在2GiB以内，但未授权且缺指令证据，故不下载整包。
