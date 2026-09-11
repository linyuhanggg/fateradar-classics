# 珞琭子三命消息赋注 · 识典 SK1605 语义审读进度 · 2026-09-11

独占文件：`references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json` 与本进度文档。未改主本 `luoluzi-sanming.json`，不碰大全/秘本、三命 HY1521、九宗门及其他书。

## WORK_PACKAGE_COMPLETE

本包 16 段全部有实质处理：`source-reviewed` 15，`draft` 1（版面标记无字），`verified` 全 false。剩余 ID：无。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-102`
- 分支：`codex/multica-ming-102`（基线继承只读 corpus-1 `f34b296`，注解祖先提交 `218f436`）
- `sources/normalized/shidianguji/SK1605/text.md` SHA256 = `a5b639ad155b4de2b12ac23a8e37028c46d07923bc5a16a4f406eed8855b97c8`（与队列一致）
- 源层 `source_status=reference-text`（识典待校）；电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 网站章节名不等于印本卷号；赋文与题徐子平注、馆臣提要分层；补本不替代主文本、不计独立投票

## 段落账本（16/16）

| # | paragraphId 尾 | kind | review | 去向摘要 |
|---|---|---|---|---|
| 0 | P…9357962 | 序跋目录 | source-reviewed | 卷端「欽定四庫全書」馆题 |
| 1 | P…9374346 | 序跋目录 | source-reviewed | 网站章节名「提要」 |
| 2 | P…9390730 | 评注或元数据 | source-reviewed | 馆臣提要：作者依托、八字晚出、永乐大典辑二卷；《三命通会》异文伪中之伪 |
| 3 | P…9407114 | 序跋目录 | source-reviewed | 总纂官题名 |
| 4 | P…9423498 | 序跋目录 | source-reviewed | 总校官题名 |
| 5 | P…9439882 | 待核实 | draft | 仅版面标记，无可转存文字 |
| 6 | P…0111626 | 序跋目录 | source-reviewed | 卷上前重复馆题 |
| 7 | P…0128010 | 序跋目录 | source-reviewed | 卷上题名 |
| 8 | P…0144394 | 序跋目录 | source-reviewed | 题署宋徐子平撰≠作者已考定 |
| 9 | P…0160778 | 规则候选 | source-reviewed | 卷上长段；subsections×5 |
| 10 | P…0177162 | 规则候选 | source-reviewed | 紧用/闻喜不喜等；subsections×4 |
| 11 | P…7911214 | 序跋目录 | source-reviewed | 卷下前馆题 |
| 12 | P…7927598 | 序跋目录 | source-reviewed | 卷下题名 |
| 13 | P…7943982 | 序跋目录 | source-reviewed | 卷下题署 |
| 14 | P…7960366 | 规则候选 | source-reviewed | 卷下长段；生月带禄≠建禄；subsections×5 |
| 15 | P…7976750 | 规则候选 | source-reviewed | 三宫元吉/仁而不仁等；subsections×5 |

ID 全称前缀：`luoluzi-sanming:shidian-SK1605:`。起讫：`P7640185840559357962`–`P7640185856267976750`。

## Multica 核源要点

继承 corpus-1 已有注解后逐段对照电子原文，确认否定/救应/分层未被模板抹平。本轮实质修订：卷下「仁而不仁」电子源作「甲见巳 / 乙见巳 / 六巳日 / 戊巳」，白话与 notes 不再径改「己」，保留巳/己字形争议。

关键条件（节录）：

- 时干居旺相则佳，死囚见多而晚成
- 甲六月下旬有官、上旬/中气无官；年月时申巳酉丑再运行西方却有官
- 将星扶德而本主休囚只虚名；根元无官印则运临亦不发
- 紧用不可受害；不损外尊则克战逢灾自愈
- 闻喜不喜：金囚休虽见不成庆；十月十一月火无气不能制金
- 建禄不富 ≠ 生月带禄（甲乙秋、丙丁冬、戊己春、庚辛夏、壬癸四季）
- 三宫元吉则凶运祸迟；始末皆凶则吉运灾速
- 身克杀轻（不贵），杀克身重（官来克我为贵）

疑文/残：段 5 无字 draft；段 9/10、14/15 跨段未完句；干推两重注云「此论未详」；段 15 末图像未转写。𧰼/㐫/已瘧編/𦂳用等不改正文。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json --json
```

期望：`ok=true`，`entries=16`，`source_reviewed=15`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓观象斋、不消除 1423 转录门槛、不改九宗门或其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。
