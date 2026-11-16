# SIJA 防御复现缺口矩阵

证据：[论文v1 §3.2、§5.4、C.1/C.3/C.4/C.5](https://arxiv.org/html/2610.23909v1)；[固定代码树](https://github.com/yexianmin/SIJA/tree/29231d7c0c5d6fad556b4f933aff353ac9bab763)。A=完整公开；B=需实现假设；C=严格复现关键缺失。

| 组件 | 原文证据 | 已知内容 | 缺失内容 | 是否阻碍复现 | 替代方案 | 可信度 |
|---|---|---|---|---|---|---|
| 输入格式 | §3.1/C.4 | Is、Tr、Ic | API具体序列化 | B 中 | 固定source、cue、text顺序 | 高 |
| 图片预处理 | C.4 | 官方推荐配置笼统说明 | resize/crop/像素预算 | B 中 | 双图各≤512²，不裁剪；记录缩放 | 高 |
| Cue组合 | §4.1/B.3 | action+spec视觉组合 | 拼图尺寸、图标资产 | C 高 | 使用发布合成cue；不重建图标 | 高 |
| Safety Guard | §3.2/§5.4/C.5 | 生成前联合判断 | **Not specified in paper**；checkpoint/revision | C 高 | 固定开源VLM作Adapted Baseline | 高 |
| 系统提示 | C.5 | safety trigger内容 | system/user role归属 | B 中 | 置system，用户只传Is/Ic/Tr | 高 |
| 用户提示 | C.4/C.5 | 原始编辑prompt | 包装格式 | B 中 | 原样Tr，不加标签 | 高 |
| 多图顺序 | C.4 | 三组件 | 具体API顺序 | B 中 | source→cue→Tr | 高 |
| 推理参数 | C.4 | Judge为bf16、thinking、do_sample=False | Guard配置缺失 | C 高 | Guard greedy，不继承Judge设置 | 高 |
| 最大输出长度 | C.5 | 结构化文本 | token上限 | B 中 | 三基线统一512；截断独立统计 | 高 |
| 温度 | C.4 | 仅Judge deterministic | Guard温度 | B 中 | do_sample=False，温度不传 | 高 |
| YES/NO | C.5 | answer标签；YES安全 | regex及大小写 | B 低 | 唯一完整标签，严格YES/NO | 高 |
| 异常处理 | 未见 | 无 | 缺失/冲突/超时策略 | B 中 | INVALID，运行时拦截，统计不算正确拒绝 | 高 |
| 拒绝策略 | C.5 | 无法肯定安全则NO；生成前拒绝 | 服务实现 | A/B 中 | NO或INVALID阻断 | 高 |
| 编辑器连接 | Table1/C.3 | Qwen-Image-Edit-2511-Safe | Guard身份、版本、调用胶水 | C 高 | 后续串行guard→editor，当前不执行 | 高 |
| 评价协议 | C.1/C.2/C.4 | ASR/HS/EV/HRR定义与Judge prompt | 防御逐例日志、重试/异常细节 | B/C 高 | 独立guard-only预注册 | 高 |

流程：联合输入→输出reference/action/specification→推断执行后内容及后果→answer YES/NO→NO拒绝，YES才进入编辑器。无需训练是提示式实现的合理解释，论文未给额外训练流程。Guard负责生成前判断；Victim负责编辑；Evaluation Judge在生成后评价，不参与guard-only判决。Gemma-4-31B-it明确是结果Judge，身份不可移植给Guard。

Author-Reported Result：93.1%危险请求拒绝率，以及另一Safe配置ASR6.92%/HRR2.35%，均非本轮结果。Faithful Reimplementation需模型及处理参数补齐，目前不成立。Adapted Baseline可用同一VLM实现公开prompt并明确假设。Independent Extension必须有基线控制和新机制证据，当前未开发。

无需等待作者即可进行适配基线研究；若目标是解释或重现93.1%，必须补齐Guard及原运行设置，代码本身不能替代这些信息。
