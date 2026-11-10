# R6-Final-Integration｜独立差异审核（2026-11-10）

**结论：科学主版本与结构验收 PASS，可合并为`main`的R6整合候选稿；投稿排版终验仍OPEN。**

## 一、核查对象与来源

- PR #67：`survey/r6-final-integration-20261110`，以已合并PR #57/#58/#60/#65/#66的`main`为基线；科学稿以PR #63 `80bad7e668a5510f7897b8ee117d7851ebaa8114`为唯一主版本，不吸收已关闭#64的C1–C3。
- 本次独立通过GitHub connector读取#63和#67两版`Survey_Full_Draft.md`，按LF归一后作逐行LCS比较。**只有11组有限变化**：稿件状态说明、Mao先行综述一行与相关定位、C1/C3改用ACL正式(RSA)²，C2改用VAGUE正式补充材料Table G4、引文用途附录B、手工参考新Mao第50条，以及正式(RSA)²标题的数学字形修正。**C1–C3的实验数值和条件H结论未改。**
- 独立检查正式VAGUE ICCV2025补充材料：**Table G4 Qwen2.5-VL-Instruct 72B VLM 72.8、VLM+CoT 69.9**；与#67修复一致。ACL2025正式(RSA)²出版页存在，已替换原异常arXiv HTML来源。未把其他未复核论文指标自判为新实测。
- 独立对GitHub #60 main与#67两个ref读取F1–F5五份SVG：**5/5 blob SHA完全相等**，保留R6-V改动。没有新的图形变更。
- 独立从#67读取正文、Bib、七表：49→**50条Bib头，50唯一且无重键**；九章科学正文引用**50键，全部存在Bib且Bib全被正文使用**；手工参考**50条**；七表全部列宽一致且无游离键。与`verify_final.py`报告方向一致。
- `render_validation.json`记录45页A4、5SVG加载、7独立附表+正文5表、无检测到溢出。**本独立审查未取得二进制PDF页面进行逐页视觉复检**（GitHub连接器不返回该>1MB的PDF正文），故这些是Work实际运行的检查记录而非独立视觉认证。

## 二、定点工程发现与处理

1. **旧`R6_fix_r1/verify_r1.py`把49硬编码**：移植50引文后原脚本运行会误报失败。本PR已更新为根据Mao键有无选择历史49/整合50的期望值，并指向当前正式`R6_final_integration/verify_final.py`。这不改科学事实，仅避免旧脚本与新稿不一致。
2. **HTML/PDF数学排版尚非正式期刊质量**：`render_preview.js`使用基础Markdown渲染，无KaTeX/MathJax插件。本轮独立查看HTML源发现`\\mathrm{Task}`等LaTeX控制序列作为可见文字出现，数个\( \)公式未数学排版。这不会改变源稿`Survey_Full_Draft.md`，但**预览不能直接视为最终投稿版**。正式期刊模板导出前应为数学表达式增加稳定的KaTeX/MathJax/LaTeX渲染，重新执行PDF逐页视觉检查并保留截图/证据。
3. **跨平台预览复现**：`render_preview.js`的Edge执行文件固定为Windows绝对路径；在Linux环境重新执行需将浏览器路径改为可配置，记录Node包版本/lockfile。原本在Windows Work环境生成的PDF不因此无效。
4. **版面风险**：`render_validation.json`的横向溢出0只证明元素宽度检测；不能验证单元格内文本适读、中文字体子集嵌入、灰度打印、表7分页和目标刊会双栏版式。50条Bib通过自定义语法解析不等于50条出版元数据已逐字段官方核对。AUTALIC作者、ThinkingGuard正式Track、VLSU版本等继续按`Bibliography_Conflicts.md`保持OPEN。

## 三、下一步

- **合并判断：GO FOR MAIN INTEGRATED CANDIDATE**，因为九章科学稿、关键引文和保留#60图形均通过；GitHub合并是版本定稿归档，**不是学术投稿批准**。
- 合并后将PR #61/#63作“内容已由#67完整整合”的历史归档关闭，不再叠加合并（否则可能冲掉R6-V图形）。
- 后续只做**一次目标投稿渠道版式适配／公式渲染／书目冲突最终校样**，再把PDF和图表打印样张送人工终验。请勿新开R6学术大修或重新精读全部50篇。
