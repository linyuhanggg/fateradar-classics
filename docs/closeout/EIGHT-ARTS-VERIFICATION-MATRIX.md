# 八术能力、规则与案例验证清单（实测汇总）

> 本表**只做汇总，不产生新统计**：规则数来自 classics `references/executable/*.json`，
> 探针/断言来自 product `art-verdict-judgment-gap-matrix.json`（已在最新 HEAD 重生成），
> 案例数来自 classics `references/cases/source-cases.json`。
> **本表不是验收结论**；每术是否可用以 `DELIVERY_ACCEPTANCE.json` 的 A1–A8 为准。
> 生成：2026-09-13 captain 脚本汇总。

| 术 | 可执行规则 | 救应 self/unimpl/none/交叉 | 矩阵行 | 有探针 | 已断言三态分支 | 原书案例 | 其中可复算 |
|---|---:|---|---:|---:|---:|---:|---:|
| bazi | 183 | 82/22/74/5 | 183 | 183 | 183 | 849 | 774 |
| ziwei | 12 | 0/3/9/0 | 12 | 12 | 12 | 178 | 178 |
| qimen | 6 | 0/0/6/0 | 6 | 6 | 6 | 1920 | 1919 |
| liuren | 23 | 14/1/8/0 | 23 | 23 | 23 | 0 | 0 |
| liuyao | 21 | 21/0/0/0 | 21 | 21 | 21 | 14 | 14 |
| meihua | 1 | 0/0/1/0 | 1 | 1 | 1 | 5 | 5 |
| xiaoliuren | 6 | 0/1/5/0 | 0 | 0 | 0 | 0 | 0 |
| qizheng | 6 | 0/3/3/0 | 6 | 6 | 6 | 1 | 1 |
| **合计** | **258** | | **252** | | | **3568** | |

## 八术主要能力与当前已知缺口（逐术，引用账本原文）

- **八字**：12 入口已接免费解释（`src/lib/engine/bazi/free-reading.ts`）；规则数最多（183）。
- **紫微**：本轮修掉「运限层串层」（页面流星年、解释写大限）实证缺陷，已加 `scope` 显式传层名；流年年份控件与 reading-report 回读 UI 待浏览器复验。
- **奇门**：批次2 结构化复算 1,919 条中 1,554 条有差异，**最大宗 `starPalaceRaw`（1,543）尚未分类**（t10）；captain 已证伪「恒定值 bug」并给出量纲假设（第1数=值符星落宫、第2数=值使门落宫）。
- **六壬**：信息不足分支 gap 8 条（DLD-E-02～E-09）无断言（A4）。
- **六爻**：本轮修掉「点开一爻后出处/导出断链、盘级规则点丢失」，逐爻焦点 1→8 点，已加负例断言。
- **梅花**：algo-impl 正在补 `meihua-source-components` 结构化样本（t6）。
- **小六壬**：pack13 起有 6 条可执行定义（YXJ-E-01～06）并接真实输出。
- **七政**：时制/时间基准修正已记（E2-QIZHENG-TIME-BASIS-FIX）；排盘口径控件与裸 URL 信息不足态待浏览器复验。

## 三类案例必须分开统计（不得互相折算）

| 类别 | 数量 | 位置 |
|---|---:|---|
| 原书可复算案例 | 3568（其中可复算 3476） | classics `references/cases/source-cases.json` |
| 独立已知盘 | 140 个 `BIRTH_*` fixture（24 案例文件） | product `src/engine/art-verdict-judgment-cases-*.ts` |
| 合成边界 | 见 `art-boundary-unknowns-cases-*.ts` 与 `tests/engine/calendar-boundaries*` | product |

> 任何一类都不能当预测准确率；测试通过不提升 `verified`/`golden`。

