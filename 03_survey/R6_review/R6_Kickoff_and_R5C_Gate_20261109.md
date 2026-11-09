# R6 启动门槛与双轨审稿任务（2026-11-09）

## 当前状态（已在GitHub核验）
- 主仓库 `YuSun-WK/implicit-content-research` 的 PR **#54、#55、#56均已合并main**。
- **PR #57 为 Draft/Open，未合并**，分支 `survey/r5c-full-draft-figures-bib-20261109`，HEAD审核时为 `c04d6a23e864923acd64c192c8b05dc597c2bb90`，base 最新main。链接 https://github.com/YuSun-WK/implicit-content-research/pull/57。
- R5-C分支 `03_survey/R5_full_draft/` 有21份新文件：`Survey_Full_Draft.md`、摘要、5份SVG、7份Markdown表、46条文献的BibTeX、键映射、冲突台账、整合审计、开放问题、R6移交等。
- `Survey_Full_Draft.md`约61,964字符，前面正文至参考文献约44,993字符，**9章46节**；字数为源字符数并非正式排版字数。
- SVG F1–F5具备源文件和基本SVG元素，但**PR作者明确未执行真实图形渲染/中文字体、裁切与黑白打印检查**。XML可解析不等于视觉通过。
- 文末参考文献少数自动排版条目出现多余Markdown强调（如ThinkingGuard及Searle行的`**.`），需修正，不等同于出版社书目元数据已经无误。
- R5-C审计记录AUTALIC数据/作者冲突、VLSU论文vs发布版本、ThinkingGuard正式Track、MCIB瓶颈独立贡献等未闭合。**阶段建议：CONDITIONAL GO TO R6；不要直接merge #57或宣称投稿终稿**。

## 两条可以立即并行的任务

### R6-A｜Chat负责独立学术审稿（主线）
**目标**：从CCF-A Reviewer/学术综述编辑角度审查真实综述质量，不再从零写稿，不做新一轮91篇大规模精读。

**输入**：读取PR #57分支`03_survey/R5_full_draft/`全部正文和表，以及main中的R4证据矩阵、R5-E引文门槛、R2-C/R3综合、所有已定稿相关精读卡。

**审稿顺序和交付**：
1. R6-A0：文章定位、目标读者、与相关综述的实质区别、论证地图；检查“广义隐晦”界定和T1–T6不混层，判断整体投稿价值；
2. R6-A1：第1–3章，核理论、综述对照、语用/修辞方法和GT；
3. R6-A2：第4–6章，核编码义、动态词义、隐晦有害、MultiMM/MGMCF/DOSE/MCIB等机制与公平对照；
4. R6-A3：第7–9章，核输入风险vs显式判断vs行为vs输出质量、VLSU/CrossGuard/ThinkingGuard/Meerkat-VL的数字和因果归因、横向综合的独立学术价值；
5. R6-A4：正式Verdict +`P0必须修改/P1建议改善/P2排版`，每一问题必须定位`章节+原句+源论文/PDF表图/项目卡+为什么越界+精准修改指令`。严禁将“个人觉得文章不够深”替换成没有证据的长篇新章节。

**必要检查**：46条被引文献只评估本稿中真正承载的主张；重点优先核AUTALIC，VLSU，MultiMM，MGMCF，MCIB，CrossGuard，ThinkingGuard，Meerkat-VL。不要将公开代码静态风险说成作者正式实验已违规。核未全文读的候选是否被用于具体机制/数字。第6.6多图证据较薄弱可做少量定向官方全文核验，仍不可扩成新大规模精读。

**输出**：新建独立工作分支，提交`03_survey/R6_review/R6A_Overall_Verdict.md`, `R6A_Chapter_Issue_Log.md`, `R6A_Claim_Evidence_Corrections.md`，PR交用户审核，**不直接改R5-C分支**，不merge。

### R6-V｜Work负责视觉/引用工程验收（与R6-A并行）
**目标**：只修交付载体的图形、书目编排、链接与印刷可读性，不改正文科学主张。

**输入**：PR #57分支中`figures/F1–F5.svg`、`tables/T1–T7`、`references.bib`、`Citation_Key_Mapping.md`、`Survey_Full_Draft.md`、`Bibliography_Conflicts.md`、`R5C_Open_Issues.md`。

**动作**：
1. 用可靠SVG渲染器**真实打开F1–F5**，提供PNG预览和缩至论文单/双栏（及灰度）可读性的验证；检查中文字体、出界、遮挡、间距、箭头路径、黑白可区分；必要时修改原SVG并给出before/after。
2. 对T1–T7实际排版和内容检查：宽表分栏/附录拆分建议、字体和数字协议标注；不悄悄改研究结论。
3. 对46条BibTeX做可解析及`正文引用key—BibTeX条目—列表呈现—源论文`一致性审计；修复ThinkingGuard、Searle等Markdown排版残余；AUTALIC作者和ThinkingGuard出版冲突仍须单列，**不得自行编造字段**。
4. 检查Markdown内链、图表交叉编号、公式渲染、DOCX/HTML/PDF预览与标题层级。若制作PDF，需要保证内容与Markdown最新版同步且字体可嵌入、不以“文档已导出”替代实际目视。
5. 将技术修订提交**独立R6-V分支/PR**，不得在R6-A还在审稿时覆盖R5-C源文件；如果设计或内容修改可能改变学术含义，写问题而非擅自改。

**输出**：`03_survey/R6_visual/R6V_Figure_Rendering_QA.md`, `R6V_Bibliography_and_Link_QA.md`, F1–F5 PNG/SVG验收样例、对需要修改的资源提交独立分支PR（可复制而不是覆盖原件）。不自动合并。

## 收口顺序
1. **并行开始R6-A与R6-V**，两者不互改文件；
2. 汇总审查后由Chat决定P0修订，**Work执行R6-Fix**到基于最新main的整合分支（或者修改R5-C待审分支但需清晰PR关系）；
3. Chat进行R6最终证据与排版复核，确保R5-C和R6修订PR冲突处理完毕；**合并前单独审阅**。
4. 只有图形真实通过、引文与BibTeX核验、正文P0关闭且目标体例明确，才能从初稿升级为投稿准备稿。

**最小结论**：R5-C的结构性制作已完成；正式科研结论/引文质量与图形最终可用性尚未通过终审。因此，接下来是R6并行学术+视觉检查，而不是重启R0–R5或重写九章。
