# 火珠林主本：独立审查 CP2（300–313 收口）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。工作树 `fateradar-multica-ming-309`，分支 `codex/multica-ming-309`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/huozhu-lin.md` 旧总述、未改 `huozhu-lin-cp1-review.md`、未改 inventory / 他书 / 引擎 / `chart.*`。不是历史原帙全书完成，也不是算法或产品交付，也不是人工 verified。紫微 CP6（1500–1799）已审，本岗未重做。审查岗未参与本包生产。

结论：**通过。** 本包仅 14 段（不足 15），故全读非模板对照原文；结构账本成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–299 属 [MING-307](mention://issue/01a090bc-2a96-7bbe-9a8c-69828dcd68a9)，本包不抢写。本 edition remaining 0。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-309`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/full-library-completion
git rev-parse HEAD
shasum -a 256 references/annotations/divination/huozhu-lin.json
git rev-parse HEAD:references/annotations/divination/huozhu-lin.json
git hash-object references/annotations/divination/huozhu-lin.json
shasum -a 256 sources/fulltext/divination/huozhu-lin/fulltext.md
git rev-parse HEAD:docs/book-reviews/huozhu-lin.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（与 Issue 钉死权威 SHA、本岗 HEAD、`ls-remote` 一致） |
| 注解 SHA256 | `123d24f09cee6f2710966f49aad5612cf067003da6c18d9ac7b304d968b437b2`（与 Issue 一致） |
| 注解 git blob | `ed34d63c3aa4311af4426686f60e0a11a4076a17` |
| working tree vs `HEAD` blob | 相同 |
| 源 `fulltext.md` SHA256 | `86a4af6ce11f4e983ffebf4d13ddc4e1fc2d25818c60c28100bda624cf957209` |
| 源 git blob | `3352931997ae9a96c171469d6b3aa04acd269a6d` |
| 源行数 / 字符 | 1166 行 / 22651 字符 |
| 旧总述 `huozhu-lin.md` blob | `4cc56dc6531b76fb4e1d332c34c654e8f63b11a1`（本岗未改） |
| 本岗改动文件 | 仅新增 `docs/book-reviews/huozhu-lin-cp2-review.md` |
| `huozhu-lin-cp1-review.md` | 本树不存在，未创建、未改 |

无越权文件。源层未改。注解 JSON 未改。CP1 审查文件未抢写。旧总述未改。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/huozhu-lin.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 314, "source_reviewed": 314,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

全书 314 条：`review=source-reviewed` 全 314；`verified` 全 `false`；无 `draft`。无升 verified。

kind：规则候选 209、术语 42、理论 25、案例 22、操作步骤 11、序跋目录 3、评注或元数据 2。

空白话 0、空 terms 2（均在 CP1 索引 89 / 169，本包不评）、空 notes 89。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。

CP2（300–313）14 条：`review=source-reviewed` 全 14；`verified` 全 `false`。kind：案例 9、理论 4、序跋目录 1。空白话 0、空 terms 0、空 notes 1（309）。本包无 subsections / cases / expected 字段，沿用本书既有扁平 schema（vernacular / terms / notes）。

## 4. 索引 0–299 相对权威 SHA 未改

本岗 HEAD 即权威 SHA，working tree 注解字节与 `HEAD` blob 相同，故 0–299 相对钉死 SHA 未改。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起，不评） | `huozhu-lin:L0005-L0006` |
| 注解索引 299（CP1 止，不评） | `huozhu-lin:L1107-L1107` |
| 0–299 paragraphId 集 SHA256 | `f66703665edc89996d977d08e5368e75c296f44073f49c0acb5ef9c8d6febc06` |

CP1 300 条同样 `source-reviewed` / `verified=false`。本包不评其语义，不写 `huozhu-lin-cp1-review.md`。

## 5. 索引边界（本包 300–313，本 edition 收口）

| 位置 | 实测 ID |
|---|---|
| 注解索引 300（CP2 起） | `huozhu-lin:L1111-L1114` |
| 注解索引 313（CP2 止 = 当前主本末条） | `huozhu-lin:L1163-L1166` |

起讫与 Issue 钉死 locator 一致。源文止于 L1166，其后无未纳入正文。索引 299 与 300 之间为空白与「### 占家宅」标题，未并入本包条目、也未另造 ID。本包后本 edition remaining 0。

CP2 覆盖同卦乾之离续问（宅、夫妻、子、婚姻、大小限、求官、求财、疾病、行人）及篇末「易道心性」、邵尧夫诗。节标题不单独占 ID。现包为维基文库单页整理本；remaining 0 只指该电子主文本 314 段收口，不宣称历史版本原帙全齐。

## 6. 抽样语义（14 段全读，对照原文，不凭进度摘要）

原文取 `sources/fulltext/divination/huozhu-lin/fulltext.md` 的 `start_line–end_line`。本包不足 15 段，故 300–313 全读。同卦多问的方向、否定与救应多数成立；病、婚、子嗣、寿命、归期均未转成对现实用户的医疗、婚育、死期或行程预测。下列为非模板抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L1111-L1114` | 案例 / sr | 多父取多屋、土绝取旧；甲辰旬空兼离九三日昃/火焚；壬戌高屋因甲寅财动、亢龙、鬼库、丑刑戌而毁；末有化出未土与丁未生扶、易辞吉而可复成。notes 禁止只摘破毁 | 通过 |
| 301 | `L1118-L1118` | 案例 / sr | 占夫妻：寅财动、申兄克，初夏木病金生，类数三减作二。notes 不作真实配偶人数 | 通过 |
| 302 | `L1122-L1122` | 案例 / sr | 占子：初爻甲子夏绝取一子象。notes 不是子女人数事实 | 通过 |
| 303 | `L1126-L1126` | 案例 / sr | 占婚姻：兄动克妻、财动伤翁。白话映射克财/克父，并与求财「可求」分问。不同问事未压成一个总分 | 通过 |
| 304 | `L1130-L1131` | 案例 / sr | 世上九起五年一爻阳顺：五岁世、六至十初九福德、十一至十五九二甲寅克世「命在须臾」。notes 不定寿命死期 | 通过 |
| 305 | `L1135-L1135` | 案例 / sr | 易辞吉但财伤文书、兄阻，待午官、辰印年。未把吉卦辞当官事已成 | 通过 |
| 306 | `L1139-L1139` | 案例 / sr | 九二财动可求、九五比肩阻而未得。两层同时保留 | 通过 |
| 307 | `L1143-L1143` | 案例 / sr | 问父病：午火鬼主热，九二木财伤父，九五金动制木为救应，病可痊但牵连未全脱。不作治疗或预后 | 通过 |
| 308 | `L1147-L1147` | 案例 / sr | 本应甲寅日到，兄动阻改待旬。不冒称已观测归期 | 通过 |
| 309 | `L1151-L1152` | 理论 / sr | 「易道逐心 / 大道逐性」韵语，标宗教哲理，不抽术法。notes 空，校验器允许 | 通过 |
| 310 | `L1154-L1154` | 理论 / sr | 注：吉凶在人、显明在信。不把注当作占卜因果证明 | 通过 |
| 311 | `L1156-L1157` | 理论 / sr | 诚信、虚静、无私念、果决；「自然灵验」留作自述。notes 要求果决不授权证据不足仍硬断 | 通过 |
| 312 | `L1159-L1159` | 理论 / sr | 麻衣六亲各有为主，世应日月飞伏动静，复以克合刑害墓旺空冲为八宗。总纲不是细项已校定 | 通过 |
| 313 | `L1163-L1166` | 序跋目录 / sr | 署邵尧夫诗，文学题署。notes 未独立核归属，不算新术数规则。本包止此 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 宅象多层与复成救应：L1111–L1114
- 夫妻类数减取：L1118
- 子水夏绝：L1122
- 婚姻兄克妻、财伤翁：L1126
- 五年一爻、甲寅克世须臾：L1130–L1131
- 求官待午官辰印：L1135
- 求财有而兄阻未得：L1139
- 父病金制木救、牵连末脱：L1143
- 行人甲寅改待旬：L1147
- 易道心性韵语：L1151–L1152
- 注吉凶在人：L1154
- 诚信果决自述灵验：L1156–L1157
- 六亲为主与八宗：L1159
- 篇末邵尧夫诗：L1163–L1166

## 7. source-reviewed ≠ 人工 verified

主本为维基文库单页整理本。本包 14 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了条件/救应/反转/未知去向，不是影印逐字校勘，也不是预测有效证据。病、婚、子嗣、限运、归期均无现实 expected。不得把 314 条 source-reviewed 写成已人工 verified。本包是该电子主文本收口，不是历史原帙全齐，也不是产品交付。

## 8. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| L1114「化出已未」 | 变卦九五为未土，已/己/巳未分。白话取未土与丁未生扶，未改字、未改成巳 | 疑字留存。不回改 |
| L1143「牵连末脱」 | 白话作「未全脱」。末/未未校 | 不改源、不改 JSON |
| L1157「心会神颂」 | 或为「神领」。白话只取诚信/虚静/果决 | 不补字 |
| 节标题无独立 ID | `### 占家宅` 等夹在条目之间；`## 易道心性` / `## 邵尧夫诗` 同样 | 与全书分段一致。不另造 ID |
| 309 notes 空 | `huozhu-lin:L1151-L1152` `notes=[]` | 校验器允许。不回改 |
| 同卦多问方向不同 | 301 夫妻类数、303 婚姻不吉、306 求财可求未得，同用财/兄动 | 注解已分层。不压成总分 |
| 旧总述字符口径 | `huozhu-lin.md` 写 20,635 字；本岗 `wc` 源文件 22,651 字符 | 旧总述不在本岗写出范围，不回改 |
| JSON `scopeNote` | 写「逐段阅读现主文本314段」。与 entries=314 一致 | 不回改 |

## 未决（本岗不施工）

- 本 edition 主本 314 段已全部纳入 source-reviewed；remaining 0 只指该电子文本，不是人工 verified，也不是原帙全齐。
- CP1（0–299）由 MING-307 独立审查，本包不评、不抢文件。
- 已未/末脱/神颂等疑字须另做版本或影印校核，本审查不补字。
- 本审查不把任何条目标成人工 verified。
- 不宣称火珠林全书完成，不计入最新版八术页面交付。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-309`。
