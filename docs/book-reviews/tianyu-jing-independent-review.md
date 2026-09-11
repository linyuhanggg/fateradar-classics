# 天玉经：独立审查主本 source-reviewed 全量（文件索引 0–223）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-426` / 分支 `codex/multica-ming-426`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/tianyu-jing.md`、未抢 MING-421/422/423 文件、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–223（224 条，全量）。

结论：**通过（有限范围）。** 结构校验 ok；224/224 `source-reviewed`、`verified` 全 `false`；inventory 与注解 `paragraphId` 一一对应且同序；≥15 段（实际抽核 20+）对照原文语义成立；后 59 段混入撼龙 / 现代解说归属字段保留且可复核。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-426`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/tianyu-jing.json
git rev-parse HEAD:references/annotations/fengshui/tianyu-jing.json
shasum -a 256 sources/fulltext/fengshui/tianyu-jing/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `bb830ea2b8ce2567cbfef56d0127fbab9f70ff74d99efb4a6ac050eace39930b`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `5176f81655f5cf7b8b5b6c373c86b8587b7949cf` |
| 源 `fulltext.md` SHA256 | `b25ce875934df450437a29fe4f5830114a6b5692998a6c811b33dfc01193a763` |
| 源行数 | 1231 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `tianyu-jing.md` 无 diff |

无越权文件。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/tianyu-jing.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 224, "source_reviewed": 224,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–223，224 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 224/224 |
| `review=draft` | 0 |
| `verified` | 全 `false`（布尔） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| `notes=[]` | 152（无附注，不是空话） |
| 空 `terms` | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |

kind 分布：理论 85、重复 56、规则候选 49、待核实 12、操作步骤 9、术语 9、评注或元数据 3、序跋目录 1。

`sourceAttribution`：**59** 条（索引 165–223）：

| relation / work | 条数 | 起止 |
|---|---|---|
| `mixed-in` / 撼龙经 | 58 | `tianyu-jing:L0486-L0493` … 至末段前若干 |
| `modern-commentary` / 撼龙经相关现代解说 | 1 | 索引 199 `tianyu-jing:L0931-L0931` |

抽核：仓内 `sources/fulltext/fengshui/hanlong-jing/fulltext.md` 可定位「須彌山是天地骨」「貪狼真骨氣」等同文（忽略标点简繁）；L0931「山形如果象瓜」确为现代白话插入，归属正确。混入段 kind 多为「重复」，与“非天玉独立证据、对应撼龙主段”一致，不把它们升成第二份天玉经证。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/tianyu-jing.json` 224 段；注解 224 条。`paragraphId` 全部命中，`missing=0`，顺序与 inventory 一致。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 注解文件索引 0（起） | `tianyu-jing:L0005-L0005` | 与 Issue 钉死一致 |
| 注解文件索引 164 | `tianyu-jing:L0481-L0484` | 天玉相关经注收束；编者删重与顺逆异说 |
| 注解文件索引 165 | `tianyu-jing:L0486-L0493` | 无新标题转入撼龙；首条 `sourceAttribution` |
| 注解文件索引 199 | `tianyu-jing:L0931-L0931` | 现代解说 |
| 注解文件索引 223（止） | `tianyu-jing:L1220-L1231` | 与 Issue 钉死一致 |

结构分段：前 165 条（0–164）为天玉经注层；后 59 条（165–223）为撼龙混入 + 1 条现代解说。不要把全书 224 段都写成纯《天玉经》正文。

本包后该书 SR 审查 remaining **0**。既有 `docs/book-reviews/tianyu-jing.md`（生产侧账本）不覆盖、不回改。

## 5. 抽样语义（≥15，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/tianyu-jing/fulltext.md` 的行范围。下列为非模板抽核（覆盖理论 / 规则 / 术语 / 操作 / 待核实 / 评注 / 序跋 / 重复·混入 / 现代解说）：

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0005` | 理论 / SR | 「江東一勢」；notes 记识典「一卦」异文，未改正文 | 通过 |
| 1 | `L0007-L0012` | 规则候选 / SR | 三卦、二父母、四龙分组与「八掉」疑字保留 | 通过 |
| 5 | `L0020-L0020` | 规则候选 / SR | 南北八位 + 贪巨武应局，非单凭朝向 | 通过 |
| 10 | `L0037-L0037` | 操作步骤 / SR | 天卦前兼后、支从干、挨星顺逆 | 通过 |
| 11 | `L0039-L0039` | 术语 / SR | 天卦=水之用/四经之祖，标为本注定义 | 通过 |
| 40 | `L0131-L0131` | 理论 / SR | 正神百步 vs 零神不拘长短 | 通过 |
| 41 | `L0133-L0133` | 待核实 / SR | 注家自留「姑存之」两说，未单采前半 | 通过 |
| 50 | `L0156-L0162` | 规则候选 / SR | 本父母官旺优先，外卦六秀只作暂利 | 通过 |
| 65 | `L0202-L0206` | 规则候选 / SR | 批评小游年/小玄空混用主局 | 通过 |
| 80 | `L0250-L0250` | 理论 / SR | 戒支水但留寅申巳亥例外 | 通过 |
| 121 | `L0342-L0342` | 序跋目录 / SR | 授诀劝德收束，秘传≠可复算证明 | 通过 |
| 146 | `L0427-L0427` | 待核实 / SR | 命地配合缺取命法；不换日主五行 | 通过 |
| 160 | `L0467-L0473` | 规则候选 / SR | 救贫黄泉来吉去凶；故事不作已核实灾例 | 通过 |
| 164 | `L0481-L0484` | 评注或元数据 / SR | 删重重编 + 顺逆异说并存 | 通过 |
| 165 | `L0486-L0493` | 重复 / SR + 撼龙 mixed-in | 须弥山开篇，仓内撼龙可定位 | 通过 |
| 172 | `L0560-L0587` | 重复 / SR + mixed-in | 剥换、罗城罗星条件清楚 | 通过 |
| 199 | `L0931-L0931` | 评注 / SR + modern-commentary | 「山形如果象瓜」现代白话，非古籍第二证 | 通过 |
| 200 | `L0933-L0943` | 重复 / SR + mixed-in | 破军走旗与三台六曜变形 | 通过 |
| 215 | `L1192-L1192` | 重复 / SR + mixed-in | 入穴须称，反弓伸颈否定 | 通过 |
| 223 | `L1220-L1231` | 重复 / SR + mixed-in | 七星剥换收束歌，非天玉三般卦水法 | 通过 |

抽核未发现把混入撼龙段冒充天玉水法、把 `verified` 置 true、或空模板白话。坏文 / 疑字段（如 L0133、L0427、L0686）保持待核实或 notes 说明，未默补。

## 6. 明确非结论

- 本包 **不** 证明影印已校或传统断语经验证。
- 本包 **不** 把任何条升为人工 `verified`。
- 本包 **不** 表示风水材料已接入 FateRadar 八术页面。
- 本包 **不** 覆盖或取代已有 `docs/book-reviews/tianyu-jing.md`。
- 识典 SK1592 异文仅作提示（见索引 0 notes），不改正文。

## 7. 交付

| 项 | 值 |
|---|---|
| Issue | MING-426 |
| 分支 | `codex/multica-ming-426` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/tianyu-jing-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后可将本 Issue `done`；无需重做 0–223；无需回改注解。
