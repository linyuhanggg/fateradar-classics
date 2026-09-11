# cursor-native-classics checkpoint 2026-09-11T05:00Z

Lane: `codex/cursor-classics-autonomy-state`  
Run branch: `cursor/fateradar-classics-processing-a99f`  
Baseline: `d47f77d` (`origin/codex/grok-fast-corpus-3-20260910`)  
Continued from: `db0d298` / lease `4bcd596`  
Source: `sources/normalized/shidianguji/SK1610/text.md` sha256 `9833d244847f53b83b4e746dd8d4a49cb9a01c0a92c2dfc7b4f19cf001e39a7e`

Nowledge Mem MCP/`nmem` CLI unavailable; task state is in-repo only. Cursor Memories not used.

## Package

Exclusive file: `references/annotations/bazi/sanming-tonghui--shidian-SK1610.json`.  
星学大成 SK1609、玉匣记、渊海 NGJ、卜筮 HY0057、inventory、公共导出未触碰。  
队列无下一份 `owner=cursor-native-classics` 授权包，本轮不领取新包。

`remainingIds` 已空，`原文：` 模板 0 条。本轮只审查已交付范围，不重领已完成模板 ID。

## Counts

| 口径 | 数 |
|---|---|
| 总条目 | 322 |
| 基线 `原文：` 模板 | 281 |
| 剩余 `原文：` 模板 | 0 |
| 本轮改写 | 4 |
| `verified=true` | 0 |
| accepted | no |

全库 322 段对 `paragraphs.json` 一一对应；`verified=false` 322；kinds：规则候选 293、评注或元数据 12、序跋目录 6、术语 6、理论 3、待核实 2。

本轮对照源文：

- `P7426253718758293541`：`text.md` L1538 与 `original-paragraphs`、HY1521 同段均作「生己酉丑月」。白话曾改写成「生巳酉丑月」。月令三合通常是巳酉丑，己不是月支。已恢复己字，不把「巳」写入引文，不以己酉丑为可执行月令。
- `P7426253719257317385`：L1585 作「得己字長生」。庚金长生通常在巳，己不是长生地支。HY1521「得巳官字長」已残，只作他本对照。不以己为可执行长生地。
- `P7426253719257366537`：L1597 与 HY1521 同段均作「己酉丑金局」。他本未改成巳，不能当否证，也不改写引文。不以己酉丑为可执行金局门闩。
- `P7426253719349542962`：L1712 作「己酉丑栽根帶刃」。不改写成巳，不以己酉丑为可执行栽根。
- `P7426253719257333769`：L1589 仍以「欄」起；缺上字仍 unknown。
- `P7426253719907549193`：L1847 仍止于「必膺大」，无续行。
- `P7426253693126819867`：L401 仍作「化象是上」。不补土。
- `P7426253719349657650`：L1754 仍作「年支得己字」。不改写成巳。

本轮只改上述四处己/巳月令或长生误用，不发明缺字、不标 accepted。

## Tests

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-cursor-classics-lease.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-validate-annotations.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-SK1610.json --json
```

Lease 15 tests OK（ordinary push 不抢占、过期归还 in-progress、completed 不重领；欄/必膺大截断保持待核实；年支己、地支坐己、己为巽风、午己火盛、生己酉丑月、得己字长生、己酉丑金局、己酉丑栽根不改写成巳、不作「无己」门闩）。  
`validate-annotations`：`ok=true`，`entries=322`，`errors=[]`。structural/source-ID only，不是语义或人工证书。

Lease: ordinary push `4bcd596` acquired; this checkpoint reviews delivered scope then releases.

## 未决

- 本包未 accepted：无人工证书；「必膺大」「欄」仍缺字；「化象是上」「年支得己」「地支坐己」「己为巽风」「午己火盛」「生己酉丑月」「得己字长生」「己酉丑金局/栽根」字形未核。本地无影印。
- 他本不能当主本投票；不发明续字。
- 无下一授权包。停止领取。
