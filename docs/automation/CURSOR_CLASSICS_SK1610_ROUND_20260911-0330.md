# cursor-native-classics checkpoint 2026-09-11T03:30Z

Lane: `codex/cursor-classics-autonomy-state`  
Run branch: `cursor/fateradar-classics-processing-b252`  
Baseline: `d47f77d` (`origin/codex/grok-fast-corpus-3-20260910`)  
Continued from: `f060d67` / lease `1ed1576`  
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
| 本轮改写 | 1 |
| `verified=true` | 0 |
| accepted | no |

全库 322 段对 `paragraphs.json` 一一对应；`verified=false` 322；kinds：规则候选 293、评注或元数据 12、序跋目录 6、术语 6、理论 3、待核实 2。

本轮对照源文：

- `P7426253719349657650`：`text.md` L1754 与 `original-paragraphs` 均作「年支得己字」。年支不能是天干己。仓库全文与 HY1521 作「巳」，只作他本对照，不写入引文。已从白话去掉「年无己则不取」，年支字形保持 unknown。
- `P7426253693126819867`：L401「化象是上」。仓库 fulltext 同；HY1521 作「土」。不补土。
- `P7426253719257333769`：L1589 仍以「欄」起；`figures.json` 空。缺上字仍 unknown。
- `P7426253719907549193`：L1847 仍止于「必膺大」，无续行。他本「貴」不写入引文。
- `P7426253719341236234`：水木春生须遇土金；非春或不遇则公侯不取。
- `P7426253719341350922`：火盛无水济才暴夫；「夫」按本段已有字连读，不另补。
- `P7426253719349641266`：月建申、年/时子才师卦；日支子则非。
- `P7426253719412408329`：龚胜忠节以后说煞旺印刃为正；前句日干健旺印刃相扶是订正对象。

本轮只改上述年支己误用，不发明缺字、不标 accepted。

## Tests

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-cursor-classics-lease.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-validate-annotations.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-SK1610.json --json
```

Lease 13 tests OK（ordinary push 不抢占、过期归还 in-progress、completed 不重领；欄/必膺大截断保持待核实；年支己不改写成巳、不作「年无己」门闩）。  
`validate-annotations`：`ok=true`，`entries=322`，`errors=[]`。structural/source-ID only，不是语义或人工证书。

Lease: ordinary push `1ed1576` acquired; this checkpoint reviews delivered scope and releases.

## 未决

- 本包未 accepted：无人工证书；「必膺大」「欄」仍缺字；「化象是上」「年支得己」字形未核。本地无影印。
- 他本不能当主本投票；不发明续字。
- 无下一授权包。停止领取。
