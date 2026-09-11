# 六壬指南 · annotated-vol3-4：独立审查差集剩余 L3606–L3938

审查对象：`origin/codex/multica-ming-167` @ `386fa69622842d6dc41ea9920f034c41e4d8233b`（父 `origin/codex/multica-ming-158` @ `e25d525505c6452cd1cbba027aabaccbbd39bccb`，已有 SR 1800 / L0003–L3604）。工作树只读参考 `fateradar-multica-ming-167`，本岗写出仅本文件。未改注解 JSON、未改源文、未改大全/秘本/九宗门、HY1521、引擎 `liuren*`、`chart.*`、MING-158/MING-164 产物。不是六壬指南全书完成，也不是人工 verified。禁止重做 corpus-2 的 1500 / L0003–L3003，禁止重做 MING-158 的 L3005–L3604（审查已是 MING-164）。

结论：**通过。** 相对父提交仅新增差集 167 条；`validate-annotations` `ok=true entries=1967 errors=[]`；`verified` 全 false；≥15 段新写对照源文非模板成立。`source-reviewed` 不是人工 `verified`；`remaining 0` 只指本 edition 差集，不是全书。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-173`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-167
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
| `origin/codex/multica-ming-167` | `386fa69622842d6dc41ea9920f034c41e4d8233b`（本岗起点与 `ls-remote` 一致） |
| 父提交 | `e25d525505c6452cd1cbba027aabaccbbd39bccb` |
| 相对父提交文件 | 仅 2 个：`references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json`、`docs/book-reviews/liuren-zhiyin-vol3-4-progress-2026-09-11.md` |
| diffstat | `+2745 / -21`（进度文档更新；注解在父文件基础上追加差集条目） |
| 源 `supplemental-annotated-golla-vol3-4.md` SHA256 | `2d03b731c84ad3a0f26c02bd1a3bdac860e7984632136c203d3daf4bc85012ae`（与 Issue / 进度一致） |
| 源 blob 父 vs 本提交 | 同为 `f1e6d2a7e4ba346b38c8a129eca49d4b6874eb2b`（本提交未改源层） |
| 父注解 entries | 1800；本提交 entries | 1967（+167） |
| 首 1800 条相对父 | 逐条 JSON 规范化比对 **0 变更**（SHA256 `2008fc5afbf8babb…` 一致） |
| 新增 paragraphId | 恰好 167，范围 `L3606`–`L3938`，与源非空行集合一致，无越出、无删除父 ID |
| 继承止 / 本批起止 / nextId | `L3604` → `L3606`…`L3938`；本 edition 差集 remaining **0**；无 nextId |

无越权文件。源层未改。大全/秘本/引擎/`chart.*` 未覆盖。`scopeNote` 已写明 golla 补缺对照、不能冒充陈公献未注原典；`source-reviewed` 仅对照本电子原文。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-167 活树施工）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 1967, "source_reviewed": 1967,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

全文件 1967 条：`review=source-reviewed` 全 1967；`verified` 全 `false`。新 167 条同：无 `draft`、无升 verified。

新 167 kind：规则候选 88、术语 66、案例 7、序跋目录 4、评注或元数据 2。

空白话 0；无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。精确白话重复组 0。`notes` 在新 167 中 166 条为 `[]`；仅 `L3938` 有一条说明「source-reviewed 仅确认电子语义阅读；不等于影印校勘或人工 verified。」——合法，不是升 verified。

`sourceAttribution`：161 条 `modern-commentary`；6 条盘式残行 `None`（与前包盘式残行惯例一致，挂 `relatedParagraphIds`→`L3596`）。

## 4. 差集边界与 remaining

源自 `L3606` 起非空行恰好 **167**，止 `L3938`；与新增注解 ID 集合完全一致。本包后剩余非空未注行 **0**。`remaining 0` = 本 edition 差集收尽，**不是**六壬指南 canonical 全书完成，也不是人工 verified。

| 位置 | 实测 ID |
|---|---|
| 继承末（未改） | `liuren-zhiyin:annotated-vol3-4:L3604-L3604` |
| 本批起 | `liuren-zhiyin:annotated-vol3-4:L3606-L3606` |
| 本批止 | `liuren-zhiyin:annotated-vol3-4:L3938-L3938` |
| nextId | 无（本 edition 差集已尽） |

区段与进度一致：雨雪例盘式+断 `L3606`–`L3618`；月煞丑–戌续表 `L3620`–`L3672`；正五九季起神煞 `L3674`–`L3770`；天马皇恩与单双月 `L3772`–`L3808`；天德月德与四时神 `L3810`–`L3848`；旬煞/乾煞/支煞 `L3850`–`L3934`；神煞辨讹 `L3936`–`L3938`。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md` 的行号（paragraphId `L####` = 源行）。盘式残行挂 `relatedParagraphIds`→雨例起例 `L3596`；义例/表行/节题标 `modern-commentary`。下列为非模板抽核。

| 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|
| `L3606` / `L3608` / `L3610` | 案例 / sr | 盘式残行「丑戌…」「戌未戌丁」「申酉戌亥」；列可见干支，挂 L3596，不单行取象 | 通过结构 |
| `L3618` | 案例 / sr | 断：太阴水将发用又为雨师主雪；中末土不久；应丑时辰被戌冲开；果验。golla 课例分层 | 通过 |
| `L3620` | 术语 / sr | 丑位血支/天坑/佛煞/天牛/坟墓表行；白话点名并指向下句义例 | 通过 |
| `L3622` | 规则 / sr | 血支血光产孕忌针灸；天坑忌出行损蹄轮；佛煞/天牛/坟墓分路 | 通过 |
| `L3630` / `L3650` / `L3680` | 术语 / sr | 鼠视捕追良、月害阴空竹、鬼吏长绳天咒接等表行；套语否定单行取象 | 通过结构 |
| `L3674` | 术语 / sr | 「正五九 二六十 七冬四四八臘」月份分组起例；白话归一为三合季表 | 通过结构；见 caveat |
| `L3750` | 规则 / sr | 「阳煞主阳人口舌」——跟源短义例 | 通过 |
| `L3780` | 规则 / sr | 天马朝廷印信+炎煞速动+传送白虎必动/克日失脱；皇恩诏命迁转 | 通过 |
| `L3810` | 规则 / sr | 天德月德起例密句与二德合凶消福进；跟源切段 | 通过 |
| `L3850` / `L3858` | 序跋 / sr | 「旬煞」「乾煞」——注本分类标题，非独立断语 | 通过 |
| `L3876` | 评注 / sr | 庄按：五行长生 vs 十干长生、丙戊/丁己同宫、土寄改正；方法说明分层 | 通过 |
| `L3900` | 规则 / sr | 恩赦吉；羊刃静吉动凶血光；飞刃；进神/退神不可退/进 | 通过 |
| `L3910` | 规则 / sr | 三刑八向分路（寅巳…卯子）——条件分向跟源 | 通过 |
| `L3920` / `L3932` | 规则 / sr | 墓主暗昧不通；驿马详见岁月煞、白衣入翰林吉祥 | 通过 |
| `L3934` | 术语 / sr | 「以上支煞载方圆图下列」——结句提示图表，非断语 | 通过 |
| `L3936` / `L3938` | 序跋+评注 / sr | 「神煞辨讹」节题 + 庄广之取位正讹自识（天喜/大煞/雷风/耳目/方圆图掌诀） | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 雨雪例盘式挂起例 L3596：L3606–L3616
- 雨师主雪 / 中末土不久 / 丑时冲开：L3618
- 血支天坑佛煞义例：L3620–L3622
- 表行排布格不单行取象：L3630、L3650、L3680、L3700、L3720
- 正五九季起月份分组：L3674
- 阳煞 / 天马皇恩：L3750、L3780
- 天德月德密句：L3810
- 旬煞/乾煞节题：L3850、L3858
- 庄按长生改正：L3876
- 恩赦羊刃进退神 / 三刑 / 墓：L3900、L3910、L3920
- 方圆图结句 / 神煞辨讹自识：L3934、L3936–L3938

## 6. source-reviewed ≠ 人工 verified

本层为 golla 补缺对照（含注者重编、后加史地注、增补课例与庄广之神煞辨讹），不能冒充陈公献未注原典。167 条电子语义阅读升 `source-reviewed`，只表示对照电子行落实了层次/条件/分向/挂接/节题，不是影印逐字校勘，也不是预测有效证据。神煞表行套语后缀（「须与全图…不单行取象」）与盘式残行套语是否定外推，不是空白话，也不等于已核验占断。不得把本批 167 条（或全文件 1967 条）source-reviewed 写成已人工 verified。`remaining 0` 只清本 edition 差集，不是六壬指南全帙，也不是产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 首 1800 SR | 相对父提交字节级一致，0 改动 | 差集续写成立。不回改 |
| 神煞表行白话后缀 | 59 条末句「须与全图及干支神将刑克同看，不单行取象。」 | 套语后缀，前半有具体表行内容。不是空模板。不回改 |
| 盘式残行白话后缀 | 6 条「须与起例、整盘及断语同看…」并挂 L3596 | 同上。不回改 |
| `notes` 空数组 | 166/167 为 `[]`；仅 L3938 有一条非升 verified 说明 | 结构合法。不回改 |
| L3674 月份分组归一 | 源「七冬四四八臘」；白话写「三七十一 / 四八腊」 | 电子归一表述，义未反。见 caveat。不回改 |
| 精确白话重复 | 0 组 | — |
| remaining / nextId | 0 / 无 | 与 Issue 一致。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **L3674**：源「七冬四」白话归一为「三七十一」；接入时以源月份标签为准，勿只剪白话。
2. **神煞表行 / 盘式残行套语**：否定单行取象成立；若要抽可执行神煞规则，须回源全图与起例。
3. **现代增补雨雪课例**（L3596 起例 + L3606–L3618）：`modern-commentary` / 挂接分层，不得并称陈公献原验。
4. **庄广之《神煞辨讹》**（L3936–L3938）与庄按（L3876）：注者方法订正，不是原书未注断语，也不是预测证书。
5. **密句义例**（如 L3810）：跟源残密切段，不单抽为完整可执行算法。

## 未决（本岗不施工）

- 神煞取位百家异说：保持 unknown，不升 verified。
- 电子阅读待校；1967 条 source-reviewed 不是人工 verified，也不是预测有效。
- 本审查不把任何条目标成人工 verified。
- canonical 九宗门与其他 edition 不在本包范围。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-173`（自 `386fa696` 分出）。
