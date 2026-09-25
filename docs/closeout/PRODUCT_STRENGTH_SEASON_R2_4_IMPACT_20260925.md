# 产品旺衰季节口径 R2-4 对 Classics 的影响（2026-09-25）

结论：已用相同 50 盘输入实际运行 `276fe07` 与 `dad1d83`。**22 盘旺衰变档，20 盘产品喜忌角色变化，13 条规则的命中名单变化。** `DITIANSUICHA-003 / 004 / DR-03` 均为 **5 → 5，但旧五盘全部退出、新五盘全部进入**。`DITIANSUICHA-051` 仍为 0 满足／0 不满足／50 信息不足，未获得正式喜行或作用裁决。

**没有回写冻结 fixture、旧 manifest、规则语义或任何开工前脏文件。** 新数字与逐盘记录在本报告及[同名 JSON](PRODUCT_STRENGTH_SEASON_R2_4_IMPACT_20260925.json)。直接调用当前产品的已有输出均无 R2-4 差异，无可单独回写的动态结果差量；本次仅新增这两份报告。

## 运行边界与来源

- 主机 `YuhangdeMac-mini.local`；正式入口 `/Users/sync/code/fateradar-classics`，分支 `main`，输入提交 `0d6d62e76add0150322361e3eb9b389c4e7361b0`。开工 38 项既有改动，已记录逐文件 SHA-256，收尾复核不变。
- 产品初始 HEAD `dad1d83a05c2e1634cd0127a9b6ac9cb23057eea`，分支 `codex/eight-arts-algorithms-notifications`。旧版使用 `git archive 276fe07` 导出到本仓 `.local/staging/r2-4-impact-20260925/product-276fe07`，依赖链接到本仓已有 `node_modules`。
- 运行中产品另有并发提交 `2cc0cd5b941e8558dd8722cf25d7395466981240`（两份 review/plan 文档）。已报告这一漂移，并核对 `src`、`scripts`、`tests`、`tsconfig.json`、`package.json`、`bun.lock` 对象 ID 与 `dad1d83` 完全相同。没有把该文档提交算入引擎差量，也没有修改产品任何文件/工作区。
- 旺衰版本：`strength-score-20260924-v1 → strength-score-20260925-v2`；纵向版本：`bazi-vertical-20260924-v16 → bazi-vertical-20260925-v17`。
- 读取 README、本机父目录 AGENTS、全局 AGENTS 与 RTK；本仓未找到额外 AGENTS/CLAUDE/GEMINI 文件。已读取 Nowledge 上下文并定向检索 P1/facts 交接历史。

## 方法与归因

两版均从产品 `scripts/dump-facts.ts` 取得原有输入，执行实际 `buildBazi`。审计适配器保留生成 `payload` 的代码，只移除写产品和 Classics fixture 的尾段，并捕获返回的 analysis/vertical；没有替换输入、四柱、阈值或求值逻辑。50 盘 ID、入参、四柱逐项相同。所有其他术数的 facts 前后相同。

冻结文件 SHA-256 为 `206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8`。它与 **R2-4 前的 `276fe07` 已有 37 盘旺衰标签不同**；本次 `276fe07 → dad1d83` 再有 22 盘变化。两段事实差异均仅涉及 `rizhu_strength`；冻结→v17合计41盘变化，37与22不能相加。37 盘是既有漂移，不记为 R2-4，也不混入提交。

`analysis.favorable` 是 `verified=false / school_convention` 的产品喜忌合参；表中“用/喜/忌”来自此处。`analysis.yongshen` 的根层 `xi/ji` 两版 50 盘全部仍为空，正式 `yongshen`、051 喜行/作用 Fact 均未出现。喜忌角色变化不能当作 Classics 已采纳了喜行合同。

529 条已提交八字/禄命规则逐盘求值；另核对工作区规则，当前未提交规则改动没有改变本次新版求值结果。选年 P1 探针按各自 `verification.year` 过滤，避免把跨年份批量命中当成选年验收。

## 规则命中数与名单

以下计数按 50 盘；“冻结”仅用于识别既有漂移。其余 516 条规则均已运行、无 R2-4 三态或名单变化；逐条计数见 JSON `ruleComparison`。051 本身 `applicable_to=[]`，不是已实现的 `rizhu_strength` 谓词。

| 规则 | 冻结满足 | v16 满足 | v17 满足 | R2-4 结果 |
|---|---:|---:|---:|---|
| `DITIANSUICHA-003` | 8 | 5 | 5 | 已运行、有变化 |
| `DITIANSUICHA-004` | 8 | 5 | 5 | 已运行、有变化 |
| `DITIANSUICHA-DR-03` | 8 | 5 | 5 | 已运行、有变化 |
| `DITIANSUICHA-036` | 9 | 19 | 24 | 已运行、有变化 |
| `DITIANSUICHA-DR-06` | 3 | 9 | 14 | 已运行、有变化 |
| `DITIANSUICHA-051` | 0 | 0 | 0 | 已运行、无变化 |
| `SANMINGTONGH-045` | 3 | 9 | 14 | 已运行、有变化 |
| `SANMINGTONGH-054` | 50 | 50 | 50 | 已运行、无变化 |
| `SANMINGTONGH-057` | 3 | 9 | 14 | 已运行、有变化 |
| `SANMINGTONGH-058` | 50 | 50 | 50 | 已运行、无变化 |
| `SANMINGTONGH-061` | 50 | 50 | 50 | 已运行、无变化 |
| `R-04` | 17 | 24 | 29 | 已运行、有变化 |
| `SANMINGTONGH-R-04` | 9 | 19 | 24 | 已运行、有变化 |
| `SANMINGTONGH-104` | 9 | 19 | 24 | 已运行、有变化 |
| `YUANHAIZIPIN-016` | 3 | 9 | 14 | 已运行、有变化 |
| `LZ-05-03` | 33 | 26 | 21 | 已运行、有变化 |
| `LZ-05-04` | 9 | 19 | 24 | 已运行、有变化 |

`003 / 004 / DR-03` 的旧命中盘：`caseP1_ZPR_01_wu_gui_both`、`caseP1_ZPR_01_wu_only`、`caseP1_ZPR_month_xin_jia_bing_1954`、`caseP1_ZPR_month_xin_jia_bing_1984`、`cov1_bazi_5`。

新版五盘：`caseB`、`caseP1_011_proper_officer`、`cov2_bazi_1`、`cov3_bazi_10`、`cov3_bazi_9`。

其他变化规则的新增/退出名单逐项记录在 JSON `ruleComparison[].added/removed`；不因满足数相同省略名单变化。

## 50 盘旺衰与喜忌

下表固定原有 50 盘。冻＝已提交 fixture；前＝`276fe07`；后＝`dad1d83`。用/喜/忌来自产品 `analysis.favorable`；完整出生参数、score、仇/闲、候选取用路线及快照标识见 JSON `charts`。

| caseId | 旺衰：冻 / 前 / 后 | v16 用／喜／忌 | v17 用／喜／忌 |
|---|---|---|---|
| `caseA` | 极强 / 偏强 / 偏强 | 火／木／水 | 火／木／水 |
| `caseB` | 极强 / 中强 / 中和 | 木／水／土 | 火／土／木 |
| `caseFlowYear` | 极强 / 偏强 / 偏强 | 火／木／水 | 火／木／水 |
| `caseFlowYearBinglin` | 中和 / 中弱 / 中弱 | 土／火／水 | 土／火／水 |
| `caseFlowYearUnknown` | 极强 / 偏强 / 偏强 | 火／木／水 | 火／木／水 |
| `caseP1_051_tiaohou_candidate` | 中和 / 中强 / 中强 | 金／土／木 | 金／土／木 |
| `caseP1_011_seven_killer` | 极强 / 极强 / 极强 | 木／水／土 | 木／水／土 |
| `caseP1_011_proper_officer` | 极强 / 偏强 / 中和 | 水／金／土 | 水／木／土 |
| `caseP1_010_both` | 中和 / 偏弱 / 极弱 | 水／木／火 | 水／木／金 |
| `caseP1_010_same_only` | 中弱 / 偏弱 / 偏弱 | 水／木／金 | 水／木／金 |
| `caseP1_010_split_only` | 中弱 / 极弱 / 极弱 | 水／木／土 | 水／木／土 |
| `caseP1_010_split_and_gui` | 中强 / 中弱 / 中弱 | 水／木／土 | 水／木／土 |
| `caseP1_010_natal_gui_only` | 中和 / 极弱 / 极弱 | 水／木／土 | 水／木／土 |
| `caseP1_010_luck_gui_only` | 极弱 / 极弱 / 极弱 | 金／土／木 | 金／土／木 |
| `caseP1_010_neither` | 极弱 / 极弱 / 极弱 | 金／土／木 | 金／土／木 |
| `caseP1_010_wrong_day` | 中强 / 中弱 / 偏弱 | 金／土／火 | 金／土／火 |
| `caseP1_010_wrong_year` | 中和 / 偏弱 / 极弱 | 水／木／火 | 水／木／金 |
| `caseP1_010_unknown_luck` | 偏强 / 极弱 / 中弱 | 火／土／木 | 水／木／火 |
| `caseP1_ZPR_01_wu_only` | 偏强 / 中和 / 极弱 | 火／土／木 | 木／水／土 |
| `caseP1_ZPR_01_no_wu` | 极强 / 中强 / 中弱 | 火／土／木 | 水／木／金 |
| `caseP1_ZPR_month_yin_bing_only_1969` | 极强 / 极强 / 偏强 | 土／火／木 | 水／金／火 |
| `caseP1_ZPR_month_xin_jia_bing_1954` | 中强 / 中和 / 偏弱 | 木／水／土 | 金／土／木 |
| `caseP1_ZPR_month_xin_jia_bing_1984` | 偏强 / 中和 / 极弱 | 木／水／土 | 土／金／火 |
| `caseP1_ZPR_month_xin_no_jia_1979` | 偏弱 / 中弱 / 极弱 | 土／金／火 | 土／金／火 |
| `caseP1_ZPR_month_xin_jia_bing_wu_1984` | 极强 / 偏强 / 偏弱 | 火／木／水 | 火／木／水 |
| `caseP1_ZPR_month_xin_jia_bing_meeting_1994` | 中和 / 极弱 / 极弱 | 土／金／火 | 土／金／火 |
| `caseP1_ZPR_month_yin_bing_wu_1979` | 极强 / 极强 / 中强 | 土／火／木 | 金／水／土 |
| `caseP1_ZPR_01_wu_gui_both` | 偏强 / 中和 / 极弱 | 火／土／木 | 木／水／土 |
| `caseP1_ZPR_02_shen_zi` | 极强 / 极强 / 极强 | 水／木／金 | 水／木／金 |
| `cov1_bazi_1` | 极弱 / 极弱 / 极弱 | 水／木／火 | 水／木／火 |
| `cov1_bazi_2` | 中和 / 中强 / 中强 | 金／土／木 | 金／土／木 |
| `cov1_bazi_3` | 偏强 / 中强 / 极强 | 木／水／土 | 土／火／水 |
| `cov1_bazi_4` | 中强 / 中强 / 极强 | 水／木／金 | 木／水／土 |
| `cov1_bazi_5` | 极强 / 中和 / 中强 | 水／木／金 | 木／水／土 |
| `cov2_bazi_1` | 极强 / 偏强 / 中和 | 木／水／金 | 木／水／金 |
| `cov2_bazi_2` | 极强 / 极强 / 极强 | 火／木／水 | 火／木／水 |
| `cov2_bazi_3` | 中弱 / 偏弱 / 偏弱 | 木／火／水 | 木／火／水 |
| `cov3_bazi_1` | 极强 / 极强 / 极强 | 金／土／火 | 金／土／火 |
| `cov3_bazi_2` | 中强 / 中弱 / 偏强 | 水／木／金 | 火／土／木 |
| `cov3_bazi_3` | 极强 / 中强 / 中强 | 火／土／木 | 火／土／木 |
| `cov3_bazi_4` | 中和 / 偏强 / 偏强 | 木／火／水 | 木／火／水 |
| `cov3_bazi_5` | 中弱 / 偏弱 / 偏弱 | 火／木／金 | 火／木／金 |
| `cov3_bazi_6` | 极强 / 极强 / 极强 | 木／水／土 | 木／水／土 |
| `cov3_bazi_7` | 极强 / 偏强 / 偏强 | 火／土／木 | 火／土／木 |
| `cov3_bazi_8` | 极强 / 中强 / 中强 | 木／水／土 | 木／水／土 |
| `cov3_bazi_9` | 中强 / 中强 / 中和 | 土／火／水 | 火／土／木 |
| `cov3_bazi_10` | 偏强 / 中强 / 中和 | 木／火／水 | 木／火／水 |
| `cov3_bazi_11` | 中强 / 极弱 / 极弱 | 土／金／水 | 土／金／水 |
| `cov3_bazi_12` | 中弱 / 极弱 / 极弱 | 金／土／木 | 金／土／木 |
| `cov3_bazi_13` | 极强 / 极强 / 极强 | 金／水／土 | 火／土／水 |

## 取用、结构候选与引用计数

`strength.siling`（gan/state/note）、`analysis.geju`：50 盘已运行、无变化。`analysis.yongshen` 全对象变化 22 盘；`analysis.favorable` 全对象变化 32 盘，其中用/喜/忌/仇/闲角色或主路线变化 20 盘，其余是理由、候选等变化。

以下旧版→新版全部已实际求值。固定 SHA 的原验收脚本会拒绝新 fixture，表中“无变化”指独立对照计算，不冒充旧交接门禁通过。

| 候选 / 引用文件 | v16 → v17 | 处理 |
|---|---|---|
| `ZPR_E_02_FULL_ALGORITHM_CANDIDATE_20260923.*` | 整体 0/0/50 → 0/0/50；四库局部 11/37/2 → 11/37/2；20 个具名例型逐一无变化 | 脏文件只读；明细见 JSON |
| `ZPR_E_02_YIN_BING_PRINCIPAL_CANDIDATE_20260923.*` | 前提满足3；其中明确丙主2、主次未知1；前后相同 | 已运行、无变化 |
| `ZPR_E_02_XIN_YIN_JIA_BING_PRIORITY_CANDIDATE_20260923.*` | 原文字面 2/46/2；注册 P1-06 谓词 2/44/4；前后相同 | 已运行、无变化 |
| `ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.*`、`...FORMALIZATION_GATE...` | 原43盘 4/7/32；完整50盘 4/7/39；两版相同 | 43盘历史记录保留 |
| `ZPR_E_02_ZHENGGUAN_CELL_GATE_20260923.md` | 原43盘正官标签5、独立四柱4；50盘标签6、独立四柱5；两版相同 | 未出现正式用神/作用事实 |
| `ZPR_E_02_WEALTH_RELATION_AUDIT_20260923.md` | 50盘结构见证2；现代同四柱2例的财格路线/判语一致 | 已运行、无变化；脏文档不改 |
| `ZPR_L649_GUANYIN_INTERPOSITION_CANDIDATE_20260924.md` | 6真盘：来源关系3/2/1，精确谓词3/3/0；7项投影皆信息不足 | 已运行、无变化；未跟踪脚本/文档只读 |
| `DITIANSUICHA_031_SOURCE_CONTRACT_AUDIT_20260923.md` | 50盘源例结构完整命中0 → 0 | 已运行、无变化 |
| `DITIANSUICHA_051_*BOUNDARY*`、`*EFFECT*`、`*FAVORITE_RECORD*` | 含年大运15 → 15；任一列举形态8 → 8；喜木甲申/乙酉运0 → 0；戊日寅月重叠1 → 1；正式喜行/作用0 → 0 | 已运行、无变化；不升级051 |
| `SANMINGTONGH_010_*`、`SMTH_010_POST_ANCHOR_STRUCTURE_20260923.md` | 10个选年局部裁决逐项相同，整体010仍信息不足；split_only@2018仍未裁纯制 | 已运行、无变化 |
| `SANMINGTONGH_011_LITERAL_COMPANION_20260923.md` | 4个真实盘年 1/2/1 → 1/2/1；选年门禁相同 | 实际重播 PASS，两版一致 |
| 011 classification / neutral-raw-label 候选 | 6项分类投影相同；中性探针1/4/1 → 1/4/1 | 已运行、无变化 |
| `tools/reports/verification-depth.json` 的生成统计 | 八字有满足样本231、混合无满足1、全不满足1，两版一致 | 已提交文件224属更早规则数量，漂移不随本次提交 |
| 判词区分度 / executable | 零区分度53条两版一致；15包258条跨盘汇总95满足/153不满足/6未知/4缺定义，两版一致 | 已运行、无变化 |

三态顺序统一为满足／不满足／信息不足。051 的 `caseP1_051_tiaohou_candidate` 冻结“中和”在 v16 已为“中强”，v17仍“中强”；这是旧旺衰漂移，不是新季节差量。`cov3_bazi_1` 两版均极强，其字面条件重叠仍不足以裁定喜水或喜火。

## 冻结 manifest 与主题快照

7 份 manifest 均保留字节。共同记录的产品 `repoHead=93c7245…` 还需与 generator/script/fixture SHA 一起解读；历史说明明确存在当时未提交的生成输入，不能声称只 checkout 该 SHA 就能重建它。以下数字仅说明“按新引擎数字已过期”，不是重发交接。

| manifest | 原样本数 | 003/004/DR-03 满足：冻结→v16→v17 | DR-06 满足：冻结→v16→v17 |
|---|---:|---|---|
| `P1_BAZI_TOPIC_MANIFEST_20260921.json` | 43 | 7 → 3 → 5 | 3 → 8 → 11 |
| `P1_BAZI_TOPIC_MANIFEST_20260923.json` | 43 | 7 → 3 → 5 | 3 → 8 → 11 |
| `P1_BAZI_TOPIC_MANIFEST_20260923_V4.json` | 43 | 7 → 3 → 5 | 3 → 8 → 11 |
| `P1_BAZI_TOPIC_MANIFEST_20260923_V5.json` | 43 | 7 → 3 → 5 | 3 → 8 → 11 |
| `P1_BAZI_TOPIC_MANIFEST_20260923_V6.json` | 50 | 8 → 5 → 5 | 3 → 9 → 14 |
| `P1_BAZI_TOPIC_MANIFEST_20260924_V7.json` | 50 | 8 → 5 → 5 | 3 → 9 → 14 |
| `P1_BAZI_TOPIC_MANIFEST_20260924_V9.json` | 50 | 8 → 5 → 5 | 3 → 9 → 14 |

共同声明的 `cov1_bazi_2` 正例在 v16/v17 均不再满足 `003/004/DR-03`，这个失效早于 R2-4。本次没有重选样本、改谓词或重写固定交接。年度负例 `caseFlowYear@2026` 按 year 切片后仍不满足，不能与全年份命中混淆。

50/50 快照 ID 更新；剔除版本与快照身份后，29/50 内容仍有差异，21/50 仅版本/身份变化。六主题的内容变化盘数如下；保留事实 ID、规则状态、叙述和喜忌，不把它们当噪声消掉。

| 主题 | 内容变化盘数 |
|---|---:|
| `overview` | 28 |
| `wealth` | 28 |
| `career` | 28 |
| `relationship` | 26 |
| `personality` | 23 |
| `health` | 23 |
| `siblings_partners` | 0 |
| `children` | 0 |
| `travel` | 0 |
| `nobles` | 0 |
| `property` | 0 |
| `blessing` | 0 |
| `parents_elders` | 0 |

开工版本的 Classics 已提交文件及未跟踪 `tools/references/docs` 中，`bazi-vertical-20260924-v16` 字面引用 **0 处**。因此没有对应可修改的现有交接版本字段；本报告记录了实际产出的 v16/v17 快照。

## R2-1 / R2-2 / R2-3

`git grep --untracked` 对 `reading_lead`、`ZIWEI_CONCLUSION_VERSION`、`ziwei-conclusion-20260925-v2`、`chinaDstNotice`、`CHINA_DST_PERIODS` 的 Classics 消费者检索为 0。逐项核对产品提交：R2-1只增加聊天上下文第一屏；R2-2只调整紫微结论文案/版本；R2-3仅新增夏令时提示，未改时间输入或历法运算。`git diff 401fe9b 276fe07 -- src/lib/engine/facts/emit.ts` 为空。结论：没有发现这三项改变 Classics 消费 facts 的路径。

注意：`276fe07` 已包含 R2-1/2/3，所以这里是代码与消费者检索结论，不伪称已对三项各自做前后排盘实验。产品114例标注校准和产品UI/模型验收属于背景，本任务未复跑，未计入通过项。

## 盘点表

共 201 个相关文件，其中 63 个脚本；逐文件哈希、跟踪状态、输入绑定和保护状态见 JSON `inventory`。下列脚本逐项列出。静态 fixture 消费者既不切到旧产品 SHA，也不自动读当前引擎，必须与直接调用者区分。

| 脚本 | 执行/输入绑定 | 是否受 R2-4 影响 |
|---|---|---|
| `tools/audit-flow-year-unknown.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/audit-flow-year-yr03.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/audit-smth-010-post-anchor.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/audit-zpr-e-02-modern-twins.py` | 产品当前工作区（支持 product-root 时可选旧归档） | 直接复算见 directChecks |
| `tools/audit-zpr-e-02-wealth-witness.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/dead-reference-report.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/eval-agreement-fixture.py`（保护） | 产品当前工作区的静态文件；不调用旺衰引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/eval-executable.py`（保护） | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/eval-predicates.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/export-rules.py` | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/generate-p1-bazi-12-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/generate-p1-bazi-13-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-p1-bazi-14-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-p1-bazi-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-p1-bazi-v6-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-p1-bazi-v7-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-p1-bazi-v9-manifest.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-sanming-097-source-handoff.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/generate-zpr-p1-03-handoff-candidate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/migrate-rules.py` | 产品当前工作区的静态文件；不调用旺衰引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/predicate-gap-report.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/predicate-report.py`（保护） | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/predicate_lang.py` | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/tautology-register.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-ditiansui-051-favorite-record.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-ditiansui-051-shape-contract.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-eval-executable.py`（保护） | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-map-fixed-values.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-map-qimen-stems.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-structure-proposal.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-tautology-register.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/test-validate-gates.py` | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/test-value-provenance.py` | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/upgrade-rules-v2.py` | 产品当前工作区的静态文件；不调用旺衰引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/validate-rules.py`（保护） | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/value-provenance-report.py` | 静态规则/词表/候选输入；不调用产品引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/verification-depth-report.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-ditiansui-031-source-contract-audit.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-ditiansui-051-effect-gate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-ditiansui-051-favorite-boundary.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-p1-bazi-11-handoff.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-p1-bazi-12-handoff.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 规则/词表口径不因 R2-4 改写 |
| `tools/verify-p1-bazi-13-handoff.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-p1-bazi-14-handoff.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-p1-bazi-v6-handoff.py` | 固定 SHA/哈希交接输入；部分校验读取产品当前 fixture 或脚本，并不自动执行该 SHA 引擎 | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-010-conditional-effect.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-010-dayun-pure-suppression-audit.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-010-gengshen-branch.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-010-guiwu-affinity.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-010-l1082-branch-audit.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-011-classification-scope.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-011-literal-companion.py` | 产品当前工作区（支持 product-root 时可选旧归档） | 直接复算见 directChecks |
| `tools/verify-sanming-011-neutral-raw-label.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-sanming-011-provenance.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-semantic-contract-candidates.py`（保护） | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-formalization-gate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-full-algorithm-candidate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-single-qi-month-entry.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-xin-yin-jia-bing-priority.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-yin-bing-principal.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-e-02-zhengguan-cell-gate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |
| `tools/verify-zpr-l649-guanyin-candidate.py`（保护） | 产品当前工作区（支持 product-root 时可选旧归档） | 直接复算见 directChecks |
| `tools/verify-zpr-p1-03-direction-candidate.py` | 静态共享 fixture（当前字节有 SHA 锁）；脚本自身通常不切产品 SHA | 50 盘求值/统计见规则与候选对比；保留冻结输入 |

相关 fixture、规则、已提交结果/交接文件逐项如下。数字对比见上述对应表与 JSON；“保留”不表示其数字代表当前产品。

| 文件 | 类型与绑定 | 处理 |
|---|---|---|
| `docs/CLASSICS_STATUS.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/GOAL_PROGRESS.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/KNOWLEDGE_SEARCH_INTERFACE.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/PREDICATE-LANGUAGE-V3.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T168-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T170-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T172-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T186-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T187-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T192-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T193-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T194-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T195-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T197-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T199-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T200-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T201-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T204-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T205-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T206-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T208-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T209-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T210-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T211-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T212-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T214-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T215-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T217-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS-DATA-CHANGE-T218-FOR-ALGO.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/DITIANSUICHA_031_SOURCE_CONTRACT_AUDIT_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/DITIANSUICHA_051_EFFECT_CONTRACT_GATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/DITIANSUICHA_051_FAVORITE_DECISION_BOUNDARY_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/DITIANSUICHA_051_FAVORITE_RECORD_CANDIDATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/DITIANSUICHA_051_LISTED_SHAPE_CONTRACT_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/P1_BAZI_SINGLE_VALUE_CONFLICT_SCOPE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/P1_BAZI_TOPIC_HANDOFF_20260921.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V4.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V5.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V7.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V9.json` | pinned_manifest；固定 product repoHead + generator/fixture SHA；非当前工作区引擎 | 按新引擎数字已过期；保留字节，见 manifestComparison |
| `docs/closeout/P1_RELEASE_CANDIDATE_CHECKLIST_20260922.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/SANMINGTONGH_010A_13_RULE_HANDOFF_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_CONDITIONAL_EFFECT_CONTRACT_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_CONDITIONAL_EFFECT_CONTRACT_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_DAYUN_PURE_SUPPRESSION_AUDIT_20260924.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_DAYUN_PURE_SUPPRESSION_AUDIT_20260924.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_EFFECT_AUDIT_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_EFFECT_BLOCKER_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_GENGSHEN_BRANCH_ADJUDICATION_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_GUIWU_AFFINITY_ADJUDICATION_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_010_L1082_BRANCH_AUDIT_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_011A_12_RULE_HANDOFF_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SANMINGTONGH_011_CLASSIFICATION_PROVENANCE_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SANMINGTONGH_011_CLASSIFICATION_SCOPE_CONTRACT_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SANMINGTONGH_011_LITERAL_COMPANION_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_011_NEUTRAL_RAW_LABEL_CANDIDATE_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SANMINGTONGH_011_SOURCE_AND_TRISTATE_FIX_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SANMINGTONGH_097_SOURCE_HANDOFF_20260924.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/SANMINGTONGH_097_SOURCE_SCOPE_AUDIT_20260924.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/SMTH_010_POST_ANCHOR_STRUCTURE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_FULL_ALGORITHM_CANDIDATE_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_E_02_FULL_ALGORITHM_CANDIDATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_E_02_SEMANTIC_BOUNDARY_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_E_02_SINGLE_QI_FORMALIZATION_GATE_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_SINGLE_QI_FORMALIZATION_GATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_WEALTH_RELATION_AUDIT_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_E_02_XIN_YIN_JIA_BING_PRIORITY_CANDIDATE_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_XIN_YIN_JIA_BING_PRIORITY_CANDIDATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_YIN_BING_PRINCIPAL_CANDIDATE_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_YIN_BING_PRINCIPAL_CANDIDATE_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_E_02_ZHENGGUAN_CELL_GATE_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/ZPR_L649_GUANYIN_INTERPOSITION_CANDIDATE_20260924.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_P1_01_HANDOFF_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_P1_02_HANDOFF_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_P1_03_11_RULE_HANDOFF_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 保护：他人改动；只读 |
| `docs/closeout/ZPR_P1_03_DIRECTION_CANDIDATE_20260923.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/ZPR_P1_03_HANDOFF_CANDIDATE_20260923.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_P1_04_14_RULE_HANDOFF_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_P1_06_15_RULE_HANDOFF_20260923.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `docs/closeout/ZPR_P1_06_V7_SCOPE_HANDOFF_20260924.md` | fixture_or_handoff_report；冻结候选/来源审计文档；无自动当前产品引擎读取 | 相关结构统计已复算无R2-4变化；保留历史/冻结记录 |
| `docs/closeout/review/INDEPENDENT-REVIEW-A6-BATCH-20260913-reviewer-2.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/review/INDEPENDENT-REVIEW-A6-BATCH-20260913.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.json` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.md` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `docs/review/2026-09-05-foundation-audit.json` | historical_report；历史提交/历史样本记录；非当前工作区结果 | 不重写历史数字；依赖事实的现值见本次全规则重算 |
| `references/books/bazi/ditiansui-chanwei/rules.yaml` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/books/bazi/sanming-tonghui/rules.yaml` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/books/bazi/yuanhai-ziping/rules.yaml` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/books/luming-nayin/luoluzi-sanming/rules.yaml` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/executable/daliuren-daquan.json` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/executable/ziping-zhenquan.json` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `references/vocab/fact-vocab.json` | rule_or_contract；静态语义；未绑定运行 SHA | 保护：他人改动；只读 |
| `references/vocab/terms.yaml` | rule_or_contract；静态语义；未绑定运行 SHA | 条件不变；以新旧产品事实实际求值，见 ruleComparison/executableComparison |
| `tools/reports/dead-predicates.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/executable-across.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/executable-definition-gaps.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/facts-sample.json` | frozen_fixture；固定 50 盘，多个候选/manifest 锁定 SHA 206638e1… | 冻结→旧版有更早漂移；R2-4 另增22盘旺衰变档。保留原件；新数值在本报告 |
| `tools/reports/fixed-value-map.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/fne-residue-inventory.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/liuyao-structure-proposal.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260921/round50-schema-before.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260921/shensha-scope-proof.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/ditiansui-051-shape-examples.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/ditiansui-051-shape-examples.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/flow-year-unknown.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/flow-year-yr03.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/sanming-011-classification-scope-candidate.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/sanming-011-literal-chart-fixture.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/sanming-011-literal-companion-candidate.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/sanming-011-neutral-raw-label-candidate.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/p1-bazi-20260922/semantic-contract-candidate-audit.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/semantic-contract-candidates.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/semantic-contract-candidates.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/semantic-contract-request.json` | static_audit；静态映射或合同请求；不调用当前引擎 | 保护：他人改动；只读 |
| `tools/reports/p1-bazi-20260922/semantic-gap-audit.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/predicate-decisions/bazi-core.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/bazi-luming.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/captain-audit.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/liuren.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/liuyao.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/meihua-yili.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/qimen.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/qizheng.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/predicate-decisions/ziwei.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/qimen-stem-map.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/shensha-position-map.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/tautological-mappings.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/unmapped-predicates.md` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/value-equivalences.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |
| `tools/reports/value-provenance.json` | static_audit；静态映射或合同请求；不调用当前引擎 | R2-4 不改语义与映射数 |
| `tools/reports/verification-depth.json` | fixture_or_handoff_report；读取/引用冻结事实或候选合同；不自动重算产品当前引擎 | 统计见候选/manifest 重算；文档和锁定字节保留 |

## 实际命令、失败证据与验证范围

完整命令、退出码、适配器源码/哈希及原始输出路径见 JSON `commands`、`replayScripts`、`failures`。本地证据收尾归档到 `/Users/sync/code/fateradar-classics/.local/workspace-archive/20260925/r2-4-impact`，恢复方法见该目录 README。核心命令如下（为实际执行时路径）：

```sh
git -C /Users/sync/code/cosmic-fortune-lab archive 276fe07 | tar -x -C .local/staging/r2-4-impact-20260925/product-276fe07
python3 .local/staging/r2-4-impact-20260925/replay.py
python3 .local/staging/r2-4-impact-20260925/compare.py
python3 .local/staging/r2-4-impact-20260925/manifests.py
python3 .local/staging/r2-4-impact-20260925/extra.py
python3 .local/staging/r2-4-impact-20260925/run-direct.py
python3 .local/staging/r2-4-impact-20260925/run-checks.py
python3 tools/eval-executable.py --all --across --facts .local/staging/r2-4-impact-20260925/old-facts.json --json
python3 tools/eval-executable.py --all --across --facts .local/staging/r2-4-impact-20260925/new-facts.json --json
```

`validate-delivery.py` 已通过：逐盘入参/四柱/旺衰、529条规则计数及新增退出集合、7份清单探针、候选一致性、盘点文件哈希、38个保护文件、冻结fixture、产品状态/运行代码及空白检查。

核心两版排盘、529规则对照、候选纯函数对照、manifest对照、15包执行层对照均 exit 0。原样/输入重定向校验共 71 次，42 次 exit 0；失败逐次保留，不能写成全绿。直接产品校验另8次，其中6次通过、2次旧v3源码锁失败。

- 新旧 facts 的完整哈希必然与冻结值不同。051、031、ZPR全算法/寅丙/辛寅/单气门禁、SMTH 010等相应原始验收拒绝替换输入；没有更改预期值、禁用断言或解除锁。独立纯函数对照提供新数字，不能替代新交接审批。
- 开工现状已失败：`verify-zpr-e-02-single-qi-month-entry.py`、`verify-zpr-e-02-zhengguan-cell-gate.py` 仍锁43盘哈希，当前是50盘；`predicate-report.py --check-open-values --check-art-keys` 的 `ART_EMIT_KEYS` 未同步5种已用结构键。该脚本已有他人改动，本次不触碰。
- `verify-p1-bazi-12-handoff.py --replay-product` 在两版都先失败于 `generate-p1-bazi-12-manifest.py:76` 的历史源码字节锁，未进入该整体交接验收；其独立 literal-companion 实际产品重播两版均通过。
- 可恢复的路径/命令探测错误已改正；最终数字只取成功解析的实际排盘及求值输出。未执行推送、部署、PR、产品修改、语义/原文/锚点/fulltext改动。

## 处理与待决事项

新增并本地提交本 MD 和同名 JSON；已有结果文件重写 **0**。实时读产品的已提交候选投影无R2差量；锁定输入、历史报告和脏文件全部保留。完整新数字已经生成，无需为让旧门禁通过而混合两个旺衰口径。

1. 重审 `003/004/DR-03` 新五盘及 `DR-06` 变动名单，明确它们在 P1 健康/性格/总览中的适用边界。
2. 若重发 P1，须联合冻结产品版本、共享 fixture、manifest 与正反例；同时独立处理37盘既有漂移。本次不代替发布裁定、不自动改旧正例。
3. 051仍需来源裁决的喜行与岁运作用合同；产品喜忌角色不能补成正式事实。
4. 上述历史验收失败需另行收尾；涉及38项他人改动的文件，须由其任务接续。本次影响计算已完成，新的P1交接验收尚未发生。
