# E2 意图干预

**E2 Gold-Intent完成0次；Matched-Context完成0次。** 没有独立核验金标，禁止把已完成的draft-intent改称Gold。

额外探索：SIJA-329的SOURCE_METADATA/MACHINE_DRAFT三字段条件完成1次，answer=NO，160tokens、21.770s。自然NO→draft NO仅为原始判决一致；不能说“原错误持续”，因为意图、标签和是否错误均未可靠审核。没有可计算的Oracle修复率、四格错误转移或配对检验。

Matched任务已开始但共享GPU冲突中断，未产生完整输出；未完成Direct/Strong。中性字段形状已准备，但文本/token匹配未完成，必须在正式E2前锁定。

| 条件 | 完成数 | 可靠配对数 | 推断 |
|---|---:|---:|---|
| 真Gold | 0 | 0 | N/A |
| Matched | 0 | 0 | N/A |
| 未核验Draft | 1 | 0 | 仅NO→NO行为记录 |

未报告Wilson或McNemar数值，因为不存在可靠分母；metrics.py对零分母返回null，禁止用0%替代。
