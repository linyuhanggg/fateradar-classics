# 大六壬大全：独立审查主本 source-reviewed CP5（文件索引 1200–1499）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-365` / 分支 `codex/multica-ming-365`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/daliuren-daquan-cp1-review.md` / `cp2` / `cp3` / `cp4` / `daliuren-runtime.md` / 旧账本、未改秘本 / 指南 / SDZJ0170 / 子平 / 他书 / 引擎 / `chart.*`。审查岗未参与 MING-97 生产。不是全书完成，不是算法交付，不是人工 verified。本包只审注解文件索引 1200–1499（按文件顺序，不是行号排序、不是 inventory 顺序）。不重做 MING-343 已审 0–299、MING-353 已审 300–599、MING-357 已审 600–899、MING-361 已审 900–1199。

结论：**通过（有限范围）。** 结构校验与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。本包 300 条中 295 条 `source-reviewed`、5 条仍为 `draft`（订讹「水生生」/举二不足/乱首「下为尊上」/冲破「吉凶宜冲」/泆女「洛」疑字，标记正确，本岗不升）。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–1199 与 1500–6892 不在本包。

全书实测仍为 6048 `source-reviewed` + 845 `draft`（与 MING-343/353/357/361 账本一致；本 SHA 不是「6893 全 SR」）。Issue 钉死起止 `L12121-L12121`→`L12939-L12939`、约 295 SR + 5 draft、`verified` 全 false，与实测一致。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-365`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/san-shi/daliuren-daquan.json
git rev-parse HEAD:references/annotations/san-shi/daliuren-daquan.json
shasum -a 256 sources/fulltext/san-shi/daliuren-daquan/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `66db69fdf39120e4e37733cb59b5ea01a154dcd9` |
| 源 `fulltext.md` SHA256 | `e0c5cd12773bdf00a73cf2ce2e00fc8b0522b55d4855f09c0af290e155904441` |
| 源行数 | 18573 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / CP1–CP4 审查稿 / 旧运行时核对无 diff |

无越权文件。注解未改。源文未改。未抢集成 / SDZJ0170 / 子平续段 / MING-360。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/daliuren-daquan.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 6893, "source_reviewed": 6048,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`source_reviewed=6048` 不是 6893。

## 3. verified / draft 未越权提升

全书 6893 条：`verified` 全 `false`；`review` 为 source-reviewed 6048、draft 845。无 `verified=true`。

本包文件索引 1200–1499（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 295/300 |
| `review=draft` | 5/300（见下表，全部 `verified=false`） |
| `verified` | 全 `false` |
| 空白话 | 0 |
| notes 字段缺失 | 0（`notes=[]` 204 条，属无附注，不是空话） |
| 空 / 缺失 terms | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 白话全文重复组 | 1 组：索引 1208/1209 同为「阴神作元武盘图一行。待影印核。」同例盘图两行复用，不是空模板 |

kind（1200–1499）：规则候选 122、案例 101、理论 40、评注或元数据 33、术语 2、操作步骤 1、待核实 1。操作步骤 1 条（1295 `L12347`）为逃遁「先德刑后闭口」，非空模板。

本包 5 条 draft（不升 SR，不回改）：

| 索引 | paragraphId | kind | 为何仍是 draft |
|---|---|---|---|
| 1214 | `daliuren-daquan:L12149-L12169` | 规则候选 | 订讹闭口占象：日禄闭口+无禄必死合取；非六甲不必度四 vs 正文本位取阴神；「水生生」待核。不改正文、不废并行 |
| 1306 | `daliuren-daquan:L12369-L12369` | 待核实 | 「巳申寅举二」条件不足；不据本句改刑德取法 |
| 1414 | `daliuren-daquan:L12677-L12677` | 规则候选 | 自取/上门乱首分层成立；「下为尊上如首」疑「干为尊上」，改字则尊卑易位。待核。不废无发用仍名乱首 |
| 1481 | `daliuren-daquan:L12890-L12890` | 规则候选 | 冲破旺/衰墓、吉/凶将、凶空分层；「吉凶宜冲」疑「吉空宜冲」。待核。不改正文 |
| 1495 | `daliuren-daquan:L12931-L12931` | 规则候选 | 泆女＝用起天后终六合，与狡童对翻不得对调；「泆女洛」疑「泆女格」。下条例已写格，不据本行改字升 SR |

这些 draft 不是假 SR。本岗不改、不升。

## 4. 索引边界

`references/inventory/paragraphs/san-shi/daliuren-daquan.json` 全书 6893 段；注解 6893 条。本包只审**注解文件数组索引** 1200–1499。Issue 钉死起止与实测一致。本包 `paragraphId` 全部能在 inventory 按 ID 命中，`missing=0`。行号在本包内连续递进（`L12121`→`L12939`），无回跳、无跨卷大跳。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 注解文件索引 1199（CP4 止，不在本包） | `daliuren-daquan:L12119-L12119` | MING-361 已审一旬周遍格例地盘「卯 申」 |
| 注解文件索引 1200（本包起） | `daliuren-daquan:L12121-L12121` | 同例地盘「寅    酉」 |
| 注解文件索引 1202 | `daliuren-daquan:L12125-L12125` | 「阳神作元武课」盘图标题 |
| 注解文件索引 1207 | `daliuren-daquan:L12135-L12135` | 「阴神作元武课」盘图标题 |
| 注解文件索引 1295 | `daliuren-daquan:L12347-L12347` | 逃遁先德刑后闭口（操作步骤） |
| 注解文件索引 1314 | `daliuren-daquan:L12387-L12387` | 「游子课」 |
| 注解文件索引 1348 | `daliuren-daquan:L12496-L12496` | 「三交课」 |
| 注解文件索引 1411 | `daliuren-daquan:L12671-L12671` | 乱首/赘婿克向对举 |
| 注解文件索引 1420 | `daliuren-daquan:L12695-L12695` | 「赘婿课」 |
| 注解文件索引 1464 | `daliuren-daquan:L12814-L12814` | 「冲破课」 |
| 注解文件索引 1482 | `daliuren-daquan:L12892-L12892` | 「淫泆课」 |
| 注解文件索引 1495 | `daliuren-daquan:L12931-L12931` | 泆女洛（draft） |
| 注解文件索引 1499（本包止） | `daliuren-daquan:L12939-L12939` | 泆女例末传辰乘六合 |
| 注解文件索引 1500（下一包起，不在本包） | `daliuren-daquan:L12941-L12941` | 戊戌盘天将续行 |

覆盖课经连续一块：

- 一旬周遍格例盘续行 → 阳/阴神作元武捕亡 → 闭口订讹/心镜/观月经刑德 → 游子 → 三交 → 乱首/赘婿 → 冲破 → 淫泆（狡童/泆女）至 `L12939`

不要把 CP5 写成「inventory[1200–1499]」或从 `L1200` 起。

remaining 按 Issue 口径：文件索引 1500–6892 共 **5393**。其中仍有 792 draft（全书 845 − CP1 的 23 − CP2 的 7 − CP3 的 9 − CP4 的 9 − 本包 5）。另本包 5 条 draft 未升 SR，不得计入已审 SR。CP1–CP4 的 draft 亦不在本包回改范围。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/daliuren-daquan/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（覆盖七种 kind，含周遍盘续/元武捕亡/闭口/游子/三交/乱首赘婿/冲破/淫泆与全部 5 draft）。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 1200 / 1202 / 1207 | `L12121` / `L12125` / `L12135` | 案例+术语 / sr | 周遍地盘「寅酉」；阳/阴神作元武为盘图标题非另开课 | 通过 |
| 1214 | `L12149-L12169` | 规则 / **draft** | 闭密占象；度四/非六甲；水生生待核 | 通过结构（保留 draft） |
| 1218 / 1250 / 1295 | `L12185` / `L12249` / `L12347` | 理论+规则+操作 / sr | 闭口两般；阴神申 vs 订讹寻男卯方；先德刑后闭口 | 通过 |
| 1306 | `L12369` | 待核实 / **draft** | 巳申寅举二不足 | 通过结构（保留 draft） |
| 1314 / 1329 / 1330 | `L12387` / `L12428` / `L12430-L12441` | 标题+规则 / sr | 游子或旬丁或二马 vs 正文合取；破游衰游复游 | 通过 |
| 1348 / 1363 | `L12496` / `L12535` | 标题+规则 / sr | 三交三处皆仲；订讹将后雀阴合 vs 正文太阴六合 | 通过 |
| 1395 / 1397 / 1400 | `L12618-L12634` / `L12638` / `L12644-L12649` | 规则 / sr | 四正/四散；曾门两路；终传定何人；午加酉死交分占 | 通过 |
| 1411 / 1414 / 1420 | `L12671` / `L12677` / `L12695` | 规则+draft+标题 | 乱首≠赘婿克向；上门反常；下为尊上待核 | 通过（draft 保留） |
| 1464 / 1481 | `L12814` / `L12890` | 标题+规则 / sr+**draft** | 冲破≠破碎；吉凶宜冲待核 | 通过（draft 保留） |
| 1482 / 1483 / 1495 / 1499 | `L12892` / `L12894` / `L12931` / `L12939` | 标题+规则+案例 | 淫泆合取；狡童≠泆女；洛疑格；本包止于辰六 | 通过（draft 保留） |

关键源行（抽核）：L12121–12169 周遍续与闭口订讹；L12185–12347 闭口心镜/操作；L12369 举二；L12387–12441 游子；L12496–12649 三交；L12671–12695 乱首赘婿；L12814–12890 冲破；L12892–12939 淫泆至本包止；L12941 下一包起。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（维基文库整理本口径；卷次不得与 Kanripo KR3g0031 文渊阁十二卷混称）。1200–1499 中 295 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/疑字去向，不是影印逐字校勘，也不是预测有效证据，也不等于六壬算法已实现或课经 720 课已复算。5 条 draft 更不是 verified。不得把本包写成已人工 verified，也不得把全书 6893 写成已全部 source-reviewed。本包不是大六壬大全全帙交付。旧运行时核对 `daliuren-runtime.md` 仍只覆盖贵人/空亡等局部，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 全书 SR 数 | 6048/6893 | 与 CP1–CP4 一致。不回改注解 |
| 本包 5 draft | 水生生/举二/下为尊上/吉凶宜冲/泆女洛 | 正确保留。不升 SR |
| 阴神盘图白话重复 | 1208/1209 同例两行 | 同构，不是空模板。不回改 |
| 闭口度四 | 订讹非六甲不必度四 vs 正文本位取阴神 | 1214 已 draft。并行不合并 |
| 阴神申 vs 寻男卯方 | L12249 阴神申；订讹乙卯寻男正东卯 | 1250 已并行说明。不改正文 |
| 游子取法 | 订讹或旬丁或二马 vs 正文合取 | 1329 已并行。不改 adapter |
| 三交将条件 | 订讹后雀阴合 vs 正文太阴六合 vs 袖中金雀元阴合 | 三分读。不改正文 |
| 三交曾门两路 | 合阴并加日辰为用 OR 三传俱仲 | 不得删一路 |
| 乱首≠赘婿 | 日加辰受辰克 vs 辰加日被日克 | 克向相反。不得对调 |
| 上门乱首 | 更兼发用尤的；发用又名反常 | 「下为尊上」1414 draft |
| 冲破分层 | 旺衰吉凶空 | 「吉凶宜冲」1481 draft |
| 淫泆≠芜淫≠三交 | 卯酉+后合合取；并三交才浊滥 | 不得单见即名 |
| 狡童≠泆女 | 六合起天后终 vs 天后起六合终 | 1495 draft 洛字；不得对调 |

## Caveat（不改注解，留给后续 pack）

1. **文件索引 ≠ 行号/inventory 下标。** CP5 是周遍格例盘续行至淫泆泆女例的连续一块。下一独立审查包从文件索引 1500 `L12941-L12941` 起。
2. **全书并非 6893 条 source-reviewed。** 本 SHA 6048 SR / 845 draft。后续包按文件索引切，不要假设 1500+ 全是 SR。
3. **闭口捕亡交叉：** 订讹非六甲天盘即阴神 vs 正文本位上神为阴神；阴神申 vs 寻男卯方必须分读。
4. **游子：** 或见旬丁或见二马不得静默改成正文合取；破游/衰游/复游不得写成凡四季皆正格。
5. **三交：** 将条件三分读；曾门两路与死交分占不得塌成一条规则。
6. **乱首/赘婿：** 克向相反；「下为尊上」待影印；上门发用反常不废无发用仍名乱首。
7. **冲破「吉凶宜冲」** 疑吉空；不改正文。
8. **泆女「洛」** 疑格；下条例已写格，不据本行改字。狡童/泆女起终不得对调。
9. **Wikisource 十二容器 vs Kanripo 文渊阁十二卷** 卷次不能默合。本包课名是电子本标题序列，不是已考定印本卷号。

## 未决（本岗不施工）

- 上列 5 条 draft 保持 draft，不升 source-reviewed，更不升 verified。
- 295 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同六壬产品交付或 720 课金标准。
- 索引 0–1199 已由 MING-343 / MING-353 / MING-357 / MING-361 审过，本岗不重做、不回改 CP1–CP4 审查稿。
- 索引 1500–6892（起 `L12941-L12941`）留给后续独立审查包；本岗不续写、不改 JSON。
- 本审查不把任何条目标成人工 verified。
- 不宣称大六壬大全全书完成。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-365`。注解 JSON SHA256 审查前后均为 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`。
