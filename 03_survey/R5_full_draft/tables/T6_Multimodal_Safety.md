# 表6｜多模态风险真值、响应行为与指标

| 论文 | 输入风险 GT / 版本 | 显式判断 P_in | 行为与输出指标 | 限制 |
|---|---|---|---|---|
| Hateful Memes [@kiela2020hateful] | 图文仇恨二分类 | 分类模型 | 非响应任务 | 困难样本不保证全为严格 S-S-U |
| VLSBench [@hu-etal-2025-vlsbench] | 视觉安全线索/泄漏评测 | 依协议 | 拒答/危险回答 | 响应指标不是三条件风险真值 |
| MMSafeAware [@wang-etal-2025-cant] | 联合 Safe/Unsafe；所查公开图片口径待核 | 显式二分类 | 非主要响应任务 | 2:1类别比需报双侧召回 |
| VLSU [@palaskar2026vlsu] | 图/文/联合 Safe/Borderline/Unsafe；PDF 8187，公开CSV 8159 | 三条件分类 | 另有拒答/帮助评审 | 严格 S-S-U 为论文37、公开35；PDF17模型/摘要11模型 |
| MSSBench [@zhou2025situational] | 情境安全；论文1960图文对 | 部分显式诊断 | IF Judge行为 | Oracle环境状态需单列 |
| MOSSBench [@li2025oversensitive] | 300条安全图文请求 | 无统一三等级分类 | 正常请求误拒/配合 | 误拒行为不等于输入误报 |
| CrossGuard [@zhang-etal-2026-crossguard] | 合成/真实图文安全协议 | 二元 Guard 分类 | 攻击者、Guard、回应 ASR 分别计 | Fig4差异含训练构成变化 |
| ThinkingGuard [@zhang2026thinkingguard] | 作者配对 TriggerBench；待独立复核 | 风险类别/安全标签 | 步骤轨迹与偏好 | ACM最终书目/Track待核 |
| Meerkat-VL [@zhou2026meerkatvl] | 隐含风险训练数据 | 风险感知监督 | 安全/帮助性生成 | 自验证并非独立重新读图保证 |

**表注。** G_in、P_in、R_beh、Q_out 四层不可混用；ASR 必注明攻击主体、分母与 Judge。VLSU 的 34% 是联合预测错误样本中的条件比例，非全库或 S-S-U 子集漏检率。
