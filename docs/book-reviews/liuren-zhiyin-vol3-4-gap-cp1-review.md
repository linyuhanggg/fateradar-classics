# 六壬指南 · annotated-vol3-4：独立审查差集续写 L3005–L3604

审查对象：`origin/codex/multica-ming-158` @ `e25d525505c6452cd1cbba027aabaccbbd39bccb`（父 `c86a06ed9ae22f513cd8b2ef02ef4523b3afbb23`，corpus-2 / checkpoint-5 基线，已有 SR 1500 / L0003–L3003）。工作树只读参考 `fateradar-multica-ming-158`，本岗写出仅本文件。未改注解 JSON、未改源文、未改大全/秘本/九宗门、HY1521、引擎 `liuren*`、`chart.*`、MING-136 CP1 产物。不是六壬指南全书完成，也不是人工 verified。禁止重做 corpus-2 的 1500 / L0003–L3003，禁止重做 MING-136 的 0–299。

结论：**通过。** 相对父提交仅新增差集 300 条；`validate-annotations` `ok=true entries=1800 errors=[]`；`verified` 全 false；≥15 段新写对照源文非模板成立。`source-reviewed` 不是人工 `verified`；golla 补缺对照层不是陈公献未注原典。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。L3606 起 remaining 167 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-164`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-158
git rev-parse HEAD HEAD^
git diff HEAD^..HEAD --name-only
git diff --stat HEAD^..HEAD
shasum -a 256 sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md
git rev-parse HEAD^:sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md
git rev-parse HEAD:sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-158` | `e25d525505c6452cd1cbba027aabaccbbd39bccb`（本岗 HEAD 与 `ls-remote` 一致） |
| 父提交 | `c86a06ed9ae22f513cd8b2ef02ef4523b3afbb23` |
| 相对父提交文件 | 仅 2 个：`references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json`、`docs/book-reviews/liuren-zhiyin-vol3-4-progress-2026-09-11.md` |
| diffstat | `+4668`（进度文档新增；注解在父文件基础上追加差集条目） |
| 源 `supplemental-annotated-golla-vol3-4.md` SHA256 | `2d03b731c84ad3a0f26c02bd1a3bdac860e7984632136c203d3daf4bc85012ae`（与 Issue / 进度一致） |
| 源 blob 父 vs 本提交 | 同为 `f1e6d2a7e4ba346b38c8a129eca49d4b6874eb2b`（本提交未改源层） |
| 父注解 entries | 1500；本提交 entries | 1800（+300） |
| 首 1500 条相对父 | 逐条 JSON 规范化比对 **0 变更**（SHA256 `1785270c2e651498…` 一致） |
| 新增 paragraphId | 恰好 300，范围 `L3005`–`L3604`，无越出、无删除父 ID |
| 继承止 / 本批起止 / nextId | `L3003` → `L3005`…`L3604`；`L3606` 未注解 |

无越权文件。源层未改。大全/秘本/引擎/`chart.*` 未覆盖。`scopeNote` 已写明 golla 补缺对照、张注/后加史注/增补课例不能冒充陈公献原断；`source-reviewed` 仅对照本电子原文。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-158 活树施工）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 1800, "source_reviewed": 1800,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

全文件 1800 条：`review=source-reviewed` 全 1800；`verified` 全 `false`。新 300 条同：无 `draft`、无升 verified。

新 300 kind：术语 128、案例 113、规则候选 50、评注或元数据 7、序跋目录 1、待核实 1。

空白话 0；无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。`notes` 在新 300 均为空数组 `[]`（内容在 vernacular / terms / sourceAttribution / relatedParagraphIds；与多数旧条一致）。白话全文精确重复组仅 1 组×2（两段盘式残行可见神将同为「戌、后」），属同源残行标签，不是整段粘贴模板。

## 4. 差集边界与 remaining

源非空行约 1971；本层 edition 进度称 1967 段（计数口径略异，不改验收）。父提交后差集非空行 **468**（进度文写 467，差 1，见 caveat）；本包覆盖其中 300（`L3005`–`L3604` 内容行全覆盖，空白行不建条）；**remaining 167**，首条非空为 **`L3606`**（`醜 戌 醜 戌`），与 Issue / 进度 nextId 一致。

| 位置 | 实测 ID |
|---|---|
| 继承末（未改） | `liuren-zhiyin:annotated-vol3-4:L3003-L3003` |
| 本批起 | `liuren-zhiyin:annotated-vol3-4:L3005-L3005` |
| 本批止 | `liuren-zhiyin:annotated-vol3-4:L3604-L3604` |
| 下一包起（不在本包） | `liuren-zhiyin:annotated-vol3-4:L3606-L3606` |

区段与进度一致：占验三张注续 `L3005`–`L3019`；兵占验四至十三 `L3021`–`L3207`；三合章第三十 `L3209`–`L3231`；神煞指南 `L3233`–`L3604`。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md` 的行号（paragraphId `L####` = 源行）。张注标 `mixed-in`、golla 现代层标 `modern-commentary`；盘式残行挂 `relatedParagraphIds` 起例。下列为非模板抽核。

| 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|
| `L3005` | 规则 / sr | 「初傳為攻，末傳為守，中傳為守御陣地。」张注总法，挂占验三 | 通过 |
| `L3007` | 规则 / sr | 丁壬日游都在巳、忌临畏地、困兽犹斗、发用为敌为攻 | 通过 |
| `L3009` | 规则 / sr | 中传戌为城墙，受支丑刑、辰时冲，主城破 | 通过 |
| `L3011` | 规则 / sr | 末传卯生初巳内奸、卯克戌偷降；白话「坯守」字形笔误，义仍跟「破坏城守」 | 通过结构；见 caveat |
| `L3013` | 规则 / sr | 交车合/铸印本主紧闭，却干支互冲、铸印冲破、旺气在外故不守。条件分路 | 通过 |
| `L3015` / `L3017` | 规则 / sr | 占时冲破铸印应极速；戌为州城牢狱冲克则城陷狱开 | 通过 |
| `L3019` | 待核实 / sr | 勾陈克日上、屠城放狱「不知何因，请高明指教」——标存疑，不作定论 | 通过 |
| `L3021` | 案例 / sr | 占验4：戊子二月乙亥癸未，兴化台中李少文、汪宁牛湾园虑金兵东下；重审曲直 | 通过 |
| `L3045` / `L3085` | 案例 / sr | 盘式残行「虎亥午贵…」「常巳辰卯寅后」；列可见神将，挂起例，不单行取象 | 通过结构 |
| `L3125` | 案例 / sr | 占验9断：白虎驿马临干、中末俱空、辛日南征灭没、抽兵而退；跟源断全文条件 | 通过 |
| `L3165` | 规则 / sr | 「贵德临身消万祸」须其余地方皆吉，否则仍以鬼论；本课全吉分路 | 通过 |
| `L3207` | 案例 / sr | 占验13云断：墓神覆日、虎符朝支、丧吊、游都幽燕、三月十九；史验跟源 | 通过 |
| `L3209` | 序跋 / sr | 「三合章第三十」——注者分章，不是原书卷次 | 通过 |
| `L3215` / `L3231` | 案例 / sr | 潍坊吴学亮占例（错课正断）及应验纪要；`modern-commentary`，不冒充陈公献 | 通过 |
| `L3233–L3234` | 评注 / sr | HTML source 注释 +「卷四 大六壬神煞指南」镜像标记 | 通过 |
| `L3306` / `L3566` | 术语 / sr | 门煞/午死气等表行；标须与全图同看，不单行取象 | 通过结构 |
| `L3406` | 规则 / sr | 太阳至尊/青龙/赶煞；源行以逗号截断，白话同步截断，不补造下句 | 通过 |
| `L3498` / `L3500` / `L3502` | 规则+案例 / sr | 浴盆天目义例 +「凡占宅天目中支」起例 + 1998 李某宅例；现代课例分层 | 通过 |
| `L3592` | 规则 / sr | 生气解凶；雨煞加旺相有雨 | 通过 |
| `L3604` | 案例 / sr | 现代例盘式残行「常后」；本包止此 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 初攻末守中阵地：L3005
- 忌临畏地 / 困兽犹斗：L3007
- 戌城刑冲、内奸偷降、交车合/铸印冲破：L3009–L3013
- 勾陈屠城放狱自疑：L3019
- 占验4 金兵东下起例：L3021
- 盘式残行挂起例：L3045、L3085、L3604
- 占验9 抽兵而退：L3125
- 贵德临身条件分路：L3165
- 占验13 三月十九：L3207
- 三合章题 / 潍坊现代例：L3209、L3215、L3231
- 神煞指南分卷标记：L3233–L3234
- 门煞表行 / 太阳义例截断：L3306、L3406
- 天目宅例与雨煞：L3498–L3502、L3592
- 本包止盘式残行：L3604；下一包起：L3606

## 6. source-reviewed ≠ 人工 verified

本层为 golla 补缺对照（含注者重编、张注、后加史地注与增补课例），不能冒充陈公献未注原典。300 条电子语义阅读升 `source-reviewed`，只表示对照电子行落实了层次/条件/救应/反转/存疑/镜像标记，不是影印逐字校勘，也不是预测有效证据。盘式残行与神煞表行的套语后缀（「须与整盘同看 / 不单行取象」）是否定外推，不是空白话，也不等于已核验占断。不得把本批 300 条（或全文件 1800 条）source-reviewed 写成已人工 verified。本包不是六壬指南全帙，也不是产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 首 1500 SR | 相对父提交字节级一致，0 改动 | 差集续写成立。不回改 |
| 神煞表行白话后缀 | 128 条末句「须与全图及干支神将刑克同看，不单行取象。」 | 套语后缀，前半有具体表行内容。不是空模板。不回改 |
| 盘式残行白话后缀 | 79 条「须与起例、整盘及断语同看，不单行取象或外推。」 | 同上；并挂 related 起例。不回改 |
| `notes` 空数组 | 新 300 全为 `[]` | 语义在 vernacular。结构合法。不回改 |
| L3011「坯守」 | 源「破壞城守」；白话「偷降坯守」 | 字形笔误。义未反。不回改 |
| 进度差集 467 vs 实测 468 | 父后非空差集 468；本包后 remaining 167 与 nextId L3606 仍正确 | 进度口径差 1。以 remaining/nextId 为准。不回改 |
| L3406 截断 | 源行以「若克乾支，」收束；白话同步截断 | 电子切段，不补邻句。不回改 |
| 精确白话重复 | 2 条盘式残行 vern 同为「可见 戌、后…」 | 源行神将相同。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **L3011**：白话「坯守」宜读作「坏守/破守」；接入时以源「破壞城守」为准。
2. **神煞表行 / 盘式残行套语**：否定单行取象成立；若要抽可执行神煞规则，须回源全图与起例，不能只剪套语前的表字串。
3. **现代增补课例**（三合章潍坊例、天目宅例等）：`sourceAttribution=modern-commentary`，不得并称陈公献原验。
4. **进度「差集 467」**：独立计数父后非空差集为 468；**remaining 167 / nextId L3606** 与 Issue 一致，后续包从 L3606 起，不要从 L3604 重做。
5. **L3406 等截断行**：跟源残句，不单抽为完整命题。

## 未决（本岗不施工）

- L3019 屠城放狱自疑、巳/字形、史地名后加注：保持 unknown，不升 verified。
- 电子阅读待校；1800 条 source-reviewed 不是人工 verified，也不是预测有效。
- 差集 remaining 167（自 L3606）留给后续包；本岗不续写、不重做 L0003–L3003 / MING-136。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-164`。
