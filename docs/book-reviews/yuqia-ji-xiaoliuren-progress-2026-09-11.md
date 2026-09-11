# 玉匣记·李淳风六壬时课（P0 19 段）· 语义审读进度 · 2026-09-11

独占文件：`references/annotations/selection/yuqia-ji.json`（仅本 19 段）与本进度文档。未改源文 `sources/fulltext/selection/yuqia-ji/fulltext.md`。不碰引擎 / `chart.*` / `chart-defaults` / `qimen-markers` / 大全秘本折中协纪 / 其他书注解。不是《玉匣记》全书完成，不是小六壬算法重写，不是人工 verified。

## WORK_PACKAGE_COMPLETE（MING-197 · P0）

本包 **19/19** 段全部有实质处理：`source-reviewed` 19，`verified` 全 false。禁止重做 L0003–L4209；全书其余段不在本包。`remaining`（本包口径）= **0**。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-197`
- 分支：`codex/multica-ming-197`（基线继承 `origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`）
- `sources/fulltext/selection/yuqia-ji/fulltext.md` SHA256 = `d75c07372dd51f74407cf29909725ea55f4a960f1dcc3d37a5e72be6181611f2`（与 Issue 一致）
- 章节：`雜占篇 李淳風六壬時課` start_line 4211–end_line 4249
- 差集：本树与基线均无既有 `references/annotations/selection/yuqia-ji.json`；本包新建且仅含下列 19 个 paragraphId
- 只读继承 [MING-101](mention://issue/01a08f05-ff48-7616-a17b-d3c8665a1f37) 日数用法与起例条件复核，不重做其结论
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 不 OCR、不抓站、不改源文

## 段落账本（19/19 · remaining 0）

| 段 | paragraphId | kind | 摘要 |
|---|---|---|---|
| 起例 | L4213 | 操作步骤 | 大安起正月→月上起日→日上起时；原例三月初五辰时→速喜→大安→小吉；闰月 unknown |
| 大安象 | L4215 | 术语 | 身不动时／木／青龙；谋事日一、五、七字面可引、用法 unknown |
| 大安断前 | L4217 | 规则候选 | 事事昌等；神方未定义；须与下行连读 |
| 大安断后 | L4219 | 规则候选 | 行人未动／病无妨／将军回田野；末句要求仔细推详 |
| 留连象 | L4221 | 术语 | 卒未妝时（疑字）／水／玄武；谋事日二八十用法 unknown |
| 留连断前 | L4223 | 规则候选 | 事难成／日示明（疑）／官事宜缓／去者未回程 |
| 留连断后 | L4225 | 规则候选 | 失物南方见；急讨方称心（条件）；防口舌 |
| 速喜象 | L4227 | 术语 | 人便至时／火／朱雀；谋事立三六九（立疑主）；用法 unknown |
| 速喜断前 | L4229 | 规则候选 | 求财向南；失物申未午 |
| 速喜断后 | L4231 | 规则候选 | 官事有福德；田定（疑）六畜吉；行人有信音 |
| 赤口象 | L4233 | 术语 | 官事凶时／金／白虎；谋事日四七十用法 unknown |
| 赤口断前 | L4235 | 规则候选 | 赤日（疑赤口）主口舌；官非切要防 |
| 赤口断后 | L4237 | 规则候选 | 病者出西方；访咒诅（疑防）；恐染瘟癀 |
| 小吉象 | L4239 | 术语 | 人来喜时／木／六合；谋事日一五七用法 unknown |
| 小吉断前 | L4241 | 规则候选 | 最吉昌受下行病者祷上苍限制；失物坤方 |
| 小吉断后 | L4243 | 规则候选 | 行人立便至；病者祷上苍（救应条件） |
| 空亡象 | L4245 | 术语 | 信音稀时／土／勾陈；≠旬空；谋事日与大安小吉同，疑抄重 |
| 空亡断前 | L4247 | 规则候选 | 求财无利益（否定）；行人有灾殃 |
| 空亡断后 | L4249 | 规则候选 | 失物寻不见；官事有刑场；禳解保安康（救应） |

- 起：`yuqia-ji:L4213-L4213`
- 止：`yuqia-ji:L4249-L4249`
- **nextId（全书口径，非本包任务）**：本包外其余主段；不写 L0003–L4209
- **remaining（本包）**：0
- **remaining（全书注解，非本包）**：约 1760 段未在本文件覆盖

### kind 分布（本包 19）

- 操作步骤 1 / 术语 6 / 规则候选 12 / 待核实 0

## 质量要点

- 三月初五辰时原例可复算为速喜→大安→小吉；起点含本位；日用初几；时从子起；推占落点是时宫
- 「凡謀事主／立」日数：数字可引用，历法单位与应期程序 **unknown**，不执行（继承 MING-101）
- 闰月规则原文未明 → **unknown**，不发明
- 疑字（卒未妝时、日示明、谋事立、赤日、访咒诅、田定）留 unknown，不 OCR、不改原文
- 断曰前后行须连读；否定与救应条件保留（急讨方称心、祷上苍、禳解保安康）
- 六神空亡 ≠ 日柱旬空；标题托名李淳风不升为已校亲撰
- 禁止模板填白话；verified 全 false

### doubtful / unknown / 待核实（本包）

| 项 | 状态 |
|---|---|
| 闰月取数 | unknown |
| 谋事日数用法 | unknown（不执行） |
| 空亡日数是否抄重 / 与增广 OCR 异文 | unknown（不据 OCR 改） |
| 卒未妝 / 日示明 / 立 / 赤日 / 访 / 田定 | 疑字保留 |
| 李淳风亲撰 | 未证实，不升 verified |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/selection/yuqia-ji.json --json
```

结果：见交包评论（目标 `ok=true entries=19 source_reviewed=19 errors=[]`）。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包。
