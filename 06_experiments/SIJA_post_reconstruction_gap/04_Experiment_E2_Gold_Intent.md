# E2 意图干预

**真Gold完成0次；Matched-Context探索条件完成2次。** 独立HUMAN_VERIFIED=0，不能把draft-intent重命名Gold。

额外SOURCE_METADATA/MACHINE_DRAFT条件完成2次，均NO。两例natural→draft→matched均NO。没有可靠错误金标，不能称“错误持续”或“Oracle失效”。没有可计算的错误四格表或修复率。

| 条件 | 完成调用 | 可靠配对分母 | 可得结论 |
|---|---:|---:|---|
| Gold | 0 | 0 | N/A |
| Matched | 2 | 0 | 两例均NO，行为记录 |
| Draft-intent | 2 | 0 | 两例均NO，非Oracle证据 |
| Direct / Strong | 各2 | 0 | Direct 2个NO；Strong 1个NO、1个INVALID |

首次Matched中断，后续从成功记录恢复执行，失败过程保留。310的draft/matched实际input_tokens为707/727，长度接近但未做到严格相等；329早期draft缺input-token日志，不事后冒充实测。输入预算/政策/模型混杂未完全排除，不能作纯因果解释。没有Wilson/McNemar机制结果，因为可靠分母为0。
