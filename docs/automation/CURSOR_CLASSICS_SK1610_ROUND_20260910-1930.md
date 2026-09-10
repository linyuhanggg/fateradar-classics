# cursor-native-classics checkpoint 2026-09-10T19:30Z

Lane: `codex/cursor-classics-autonomy-state`  
Run branch: `cursor/fateradar-classics-processing-fde6`  
Baseline: `d47f77d` (`origin/codex/grok-fast-corpus-3-20260910`)  
Continued from: `a12fbdb` / lease `c015d4f`  
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
| 此前已改写 | 148 |
| 本轮逐段对照改写 | 36 |
| 累计已改写（相对基线模板） | 184 |
| 剩余 `原文：` 模板 | 97 |
| `verified=true` | 0 |
| accepted | no |

本轮 36 个 ID 见 `docs/automation/CURSOR_CLASSICS_PROGRESS.json` `package.thisRun.completedIds`。剩余 ID 见同文件 `remainingIds`。

本轮范围：巫咸撮要收束 15 段（含《玉井奥诀》题记作序跋目录），再进入元理赋「两干不杂」万民英解 21 段。赋末「万不失一」与《真宝赋》题署分别标评注/序跋，不把原书自称当验收。

Lease: ordinary push `c015d4f` acquired; this checkpoint completes the 36 claimed IDs and releases.

## Tests

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-cursor-classics-lease.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/test-validate-annotations.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-SK1610.json --json
```

Lease 11 tests OK（含 ordinary push 不抢占、过期归还 in-progress、completed 不重领）。  
`validate-annotations`：`ok=true`，`entries=322`，`errors=[]`。注释原文：structural/source-ID only，不是语义或人工证书。

## 未决

- 97 段仍是 `原文：` 粘贴，不得称语义完成。
- 补本不能当主本投票；网站章节名不等于印本卷号。
- `𦂳` 按紧读、`䕶`/`㫁`/`㓜`/`�按紧读、`䕶`/`㫁`/`㓜`/`䧟`/`㓙`/`䘮`/`夲` 不改字；十恶名单依道藏经不补造；河井只录丙子/癸未/癸丑；鬼啸「无辛不可言甲去生丙」保留。
- 华盖/日德/尘埃庶士、假合同居、刑主等原文截断处不补字。
- 孤鸾/八专/败地只录原文所给日支，不补全表。
- 无 Nowledge Mem；任务状态只写仓库文件。
- 本包未 accepted，未领取新包。
