# cursor-native-classics checkpoint 2026-09-10T20:30Z

Lane: `codex/cursor-classics-autonomy-state`  
Run branch: `cursor/fateradar-classics-processing-738a`  
Baseline: `d47f77d` (`origin/codex/grok-fast-corpus-3-20260910`)  
Continued from: `cab2c8b` / lease `92f6efd`  
Source: `sources/normalized/shidianguji/SK1610/text.md` sha256 `9833d244847f53b83b4e746dd8d4a49cb9a01c0a92c2dfc7b4f19cf001e39a7e`

## Package

Prompt path `references/annotations/xingming/xingxue-dacheng--shidian-SK1610.json` does not exist on the frozen baseline. SK1610 is 三命通会. Exclusive file used: `references/annotations/bazi/sanming-tonghui--shidian-SK1610.json`.

星学大成 SK1609、玉匣记、渊海 NGJ、卜筮 HY0057 were not touched. Inventory and public exports were not touched.

## Counts

| 口径 | 数 |
|---|---|
| 总条目 | 322 |
| 基线 `原文：` 模板 | 281 |
| 基线已有非模板 | 41 |
| 此前已改写 | 220 |
| 本轮逐段对照改写 | 61 |
| 累计已改写（相对基线模板） | 281 |
| 剩余 `原文：` 模板 | 0 |
| `verified=true` | 0 |
| accepted | no |

本轮 61 个 ID 见 `docs/automation/CURSOR_CLASSICS_PROGRESS.json` `package.thisRun.completedIds`。`remainingIds` 为空。

本轮范围：元理赋「两干不杂」万民英解续——格不清用神休废至土重厚载截断。火盛句末「夫」孤悬、末段「必膺大」截断标待核实，不补造下文。五行偏党无制化总束、龚胜以后说为正、日支子则非、巽居月令则非、或以天元一气解之则非，均按原文否定/订正保留。官职/古人名是原书品级语言，不是履历验收。

Lease: ordinary push `92f6efd` acquired; this checkpoint completes the 61 claimed IDs and releases.

## Tests

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-cursor-classics-lease.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-validate-annotations.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-SK1610.json --json
```

Lease 11 tests OK（含 ordinary push 不抢占、过期归还 in-progress、completed 不重领）。  
`validate-annotations`：`ok=true`，`entries=322`，`errors=[]`。注释原文：structural/source-ID only，不是语义或人工证书。

## 未决

- `原文：` 粘贴已清零，仍不得称全包语义验收或人工 verified。
- 两段待核实：火盛句末「夫」孤悬；土重厚载止于「必膺大」。
- 补本不能当主本投票；网站章节名不等于印本卷号。
- `㑹`/`㓜`/`㸔`/`㣲`/`㓙`/`劒`/`劔`/`髙`/`眀`/`邉`/`軰`/`迯`/`噐`/`卬`/`綂` 不改字。
- 趋艮/趋乾/倒冲/鼠贵/朝阳及本轮日时例只录原文所定，不补全表。
- 无 Nowledge Mem；任务状态只写仓库文件。
- 本包未 accepted，未领取新包。队列无下一份 `owner=cursor-native-classics` 授权包。
