# 玉匣记·李淳风六壬时课：独立审查 P0（L4213–L4249）

审查对象：`origin/codex/multica-ming-197` @ `75d2cc6af41245b0765a229f67cf8f8d72a4df0e`（父 `bc798566da77c30e149abf9673c88ecc386702b2`，即 `origin/codex/full-library-completion` 基线）。工作树只读参考 `fateradar-multica-ming-197`，本岗写出仅本文件。未改注解 JSON、未改源文、未改指南/大全/秘本/折中/协纪、未改引擎/`chart.*`/`chart-defaults`/`qimen-markers`。不是《玉匣记》全书完成，也不是小六壬算法重写，也不是全项目完成。只读继承 MING-101 日数/起例结论，不重做。

结论：**通过。** 交包结构账本与 19 段对照原文成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-201`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-197
git rev-parse HEAD HEAD^
git diff HEAD^..HEAD --name-only
git diff --stat HEAD^..HEAD
shasum -a 256 sources/fulltext/selection/yuqia-ji/fulltext.md
git rev-parse HEAD^:sources/fulltext/selection/yuqia-ji/fulltext.md
git rev-parse HEAD:sources/fulltext/selection/yuqia-ji/fulltext.md
git cat-file -e HEAD^:references/annotations/selection/yuqia-ji.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-197` | `75d2cc6af41245b0765a229f67cf8f8d72a4df0e`（本岗检出点与 `ls-remote` 一致） |
| 父提交 | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 相对父提交文件 | 仅 2 个：`references/annotations/selection/yuqia-ji.json`、`docs/book-reviews/yuqia-ji-xiaoliuren-progress-2026-09-11.md` |
| diffstat | `+476`（两文件均为新增） |
| 父提交是否已有 `yuqia-ji.json` | 无（`git cat-file -e HEAD^:…` 失败）。本包新建，不是覆盖 L0003–L4209 |
| 源 `fulltext.md` SHA256 | `d75c07372dd51f74407cf29909725ea55f4a960f1dcc3d37a5e72be6181611f2`（与 Issue 一致） |
| 源 blob 父 vs 本提交 | 同为 `ec2d524483d75541b83d2ab97cc0736f6c303400`（本提交未改源层） |
| 注解 ID | 19/19 = `yuqia-ji:L4213-L4213` … `yuqia-ji:L4249-L4249` 奇数行；无 L0003–L4209 泄漏 |
| 引擎 / `chart.*` / 他书 | 本提交 name-only 无这些路径。本仓此树亦无产品 `chart.*` 文件 |

无越权文件。源层未改。引擎/`chart.*`/他书未覆盖。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-197 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/selection/yuqia-ji.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 19, "source_reviewed": 19,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

19 条：`review=source-reviewed` 全 19；`verified` 全 `false`；无 `draft` 字段。无升 verified。

kind：操作步骤 1、术语 6、规则候选 12、待核实 0。

空白话 0、空 notes 0、空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文 19/19 互不重复。

谋事日 notes 在六宫术语段复用同一句式（6 条、4 个变体），前半白话仍按宫名/时象/五行/神将分写，不是空模板。见质量账本。

## 4. 三月初五辰时原例（独立复算，不凭进度摘要）

原文 L4213：每从“大安”上起正月，月上起日，日上起时。假如三月初五日辰时，三月在“速喜”上，就“速喜”上起初一，初五在“大安”，“大安”上起子时，数至辰时是“小吉”，就以“小吉”推占。

六神序取后文 L4215→L4221→L4227→L4233→L4239→L4245：大安、留连、速喜、赤口、小吉、空亡。起点含本位（正月即大安，不先跳一宫）；日用初几；时从子起（子=0）。

独立计算：

```
spirits = 大安 留连 速喜 赤口 小吉 空亡
month_i = (3-1) % 6 = 2 → 速喜
day_i   = (2 + 5-1) % 6 = 0 → 大安
hour_i  = (0 + index(辰)=4) % 6 = 4 → 小吉
```

与原文原例及 L4213 注解一致。推占落点是时宫小吉，不是月宫/日宫投票。L4213 原文无「謀事」字样；不得因初五 ∈ {1,5,7} 把谋事日写成已证（与 MING-101 C1 同向，本岗只核对本包注解，不重做 MING-101）。

本节 L4211–L4249 无「閏/闰」。闰月取数原文未明，注解保留 unknown、不发明，成立。

## 5. 抽样语义（19 段全对照原文；要求 ≥8）

原文取 `sources/fulltext/selection/yuqia-ji/fulltext.md` 对应行。偶数行为空行，未写入本包，与 Issue 钉死 19 个奇数行 ID 一致。未发现把整段原文粘进 vernacular 冒充处理。

| 段 | 源行 | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| L4213 | 4213 | 操作步骤 / sr | 大安起正月→月上起日→日上起时；原例速喜→大安→小吉。闰月/日界/节气月/年干支改正月：unknown。李淳风署名不升亲撰 | 通过 |
| L4215 | 4215 | 术语 / sr | 身不动时／木／青龙；谋事主一、五、七字面可引、用法 unknown，不执行。不是四柱青龙 | 通过 |
| L4217 | 4217 | 规则候选 / sr | 事事昌；求谋在神方（未定义）；失物去不远；宅舍保安康。逗号未收束，须与下行连读 | 通过 |
| L4219 | 4219 | 规则候选 / sr | 行人身未动／病者主无妨／将军回田野／仔细与推详。将军对象不明，不作军职算法；末句限制见大安即全吉 | 通过 |
| L4221 | 4221 | 术语 / sr | 卒未妝时（疑字，不改原文）／水／玄武；谋事主二、八、十用法 unknown | 通过 |
| L4223 | 4223 | 规则候选 / sr | 事难成；求谋日示明（疑，不改字）；官事只宜缓；去者未回程。否定速成，不是已确认失败 | 通过 |
| L4225 | 4225 | 规则候选 / sr | 失物南方见；急讨方称心（条件）；防口舌；人口平平。条件未删 | 通过 |
| L4227 | 4227 | 术语 / sr | 人便至时／火／朱雀；谋事**立**三、六、九。立疑主，不另解成第二套日数法 | 通过 |
| L4229 | 4229 | 规则候选 / sr | 求财向南行；失物申未午。三支未改成泛称南方或现代钟点 | 通过 |
| L4231 | 4231 | 规则候选 / sr | 官事有福德；病者无祸侵；田定六畜吉（田定疑，不改字）；行人有信音≠人已到 | 通过 |
| L4233 | 4233 | 术语 / sr | 官事凶时／金／白虎；谋事主四、七、十用法 unknown。不是四柱白虎 | 通过 |
| L4235 | 4235 | 规则候选 / sr | 赤日主口舌（宫名赤口，疑形近，不另立赤日宫）；官非切要防；失物急去寻 | 通过 |
| L4237 | 4237 | 规则候选 / sr | 鸡犬作怪；病者出西方；更须访咒诅（访疑防，不改字）；恐染瘟癀是或然 | 通过 |
| L4239 | 4239 | 术语 / sr | 人来喜时／木／六合；谋事主一、五、七。与大安同木同事日，神将/时象不同，未并宫。原例落小吉≠断词应验 | 通过 |
| L4241 | 4241 | 规则候选 / sr | 最吉昌受下行祷上苍限制；阴人来报喜；失物坤方。坤=西南是后天八卦常读，本节未写，见 caveat | 通过结构 |
| L4243 | 4243 | 规则候选 / sr | 行人立便至；交关甚是强；病者祷上苍是救应，未祷不保证 | 通过 |
| L4245 | 4245 | 术语 / sr | 信音稀时／土／勾陈；六神空亡≠旬空≠奇门空亡。谋事日与大安小吉同，疑抄重，不据 OCR 改 | 通过 |
| L4247 | 4247 | 规则候选 / sr | 事不长；求财无利益（否定，未改成迟得）；行人有灾殃 | 通过 |
| L4249 | 4249 | 规则候选 / sr | 失物寻不见；官事有刑场；病人逢暗鬼；禳解保安康是救应，不得省略 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 起例程序与原例：L4213
- 六神序与时象/五行/神将/谋事日数字：L4215、L4221、L4227、L4233、L4239、L4245
- 神方未定义：L4217
- 仔细与推详：L4219
- 卒未妝 / 日示明：L4221、L4223
- 急讨方称心：L4225
- 谋事立三六九：L4227
- 失物申未午：L4229
- 田定：L4231
- 赤日 / 访咒诅：L4235、L4237
- 坤方、祷上苍：L4241、L4243
- 空亡日数与大安小吉同字：L4245
- 求财无利益、失物寻不见、禳解保安康：L4247、L4249

## 6. source-reviewed ≠ 人工 verified

现行锚定是维基电子文本 `sources/fulltext/selection/yuqia-ji/fulltext.md`。19 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了起例/时象/条件/否定/救应/未知去向，不是影印逐字校勘，也不是预测有效证据。标题托名李淳风，本节未提供亲撰校勘证据。不得把 19 条 source-reviewed 写成已人工 verified。本包不是玉匣记全帙，也不是产品引擎交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 谋事日 notes 套语 | 六宫术语段复用「凡謀事主／立」日数 unknown 句；L4215/L4239/L4245 另补抄重提示 | 继承 MING-101，不是空白话。不回改 |
| L4241「坤为西南」 | 源只写「失物在坤方」；西南是后天八卦常读，本节未出现 | 轻微外推。方位仍以坤方为主，未改成任意方向。不回改 |
| L4245 增广 OCR | notes 写 NA09036 空亡「三六九」残泐异文，不据 OCR 改电子本 | 与 MING-101 R3 版本分歧同向；本包未改源、未新抓站。不回改 |
| 断曰切段 | 各宫断曰分前后奇数行，中间空偶数行 | 行级 ID 如此。注解已要求连读。不回改 |
| catalog 未更新 | `references/catalog/catalog.json` 仍指向另一份 `references/fulltext/…` SHA；本提交未改 catalog | 独占范围不含 catalog。不回改 |
| 全书 remaining | inventory 主段 1779；本文件 19 条；其余约 1760 不在本包 | 进度「本包 remaining 0」成立，≠ 全书完成 |

## Caveat（不改注解，留给后续 pack）

1. **谋事日数必须保持 unknown、不执行。** 数字字面可引用；历法单位、应期程序、与月/日/时哪一宫绑定均无本节内证。原例初五只用于计数。
2. **闰月、节气月、夜子时起迄、年干支是否改正月起点**：原文未明。不得把任何实现口径写成古文。
3. **疑字不改原文**：卒未妝、日示明、谋事立、赤日、访咒诅、田定。空亡日数与大安/小吉全同，是否抄重 unknown；不得用增广 OCR 改字。
4. **L4241 坤方**：引用方位以源字「坤方」为准，不要把「西南」当成本节已校定义。
5. **李淳风署名 / 许真人托名**：未证实，不升 verified。
6. **本包 remaining 0 ≠ 全书完成。** 不写 L0003–L4209；不宣称小六壬算法或产品交付完成。

## 未决（本岗不施工）

- 谋事日数用法、闰月取数、疑字、空亡日数异文、托名：保持 unknown，不升 verified。
- 19 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同小六壬引擎已重写。
- 玉匣记其余主段（inventory 约 1779−19）不在本包；本岗不续写、不改注解。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-201`。
