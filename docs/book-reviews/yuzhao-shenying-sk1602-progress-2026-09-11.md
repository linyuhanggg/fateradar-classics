# 玉照定真經 · 识典 SK1602 语义审读进度 · 2026-09-11

独占文件：`references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json` 与本进度文档。未改主本 `yuzhao-shenying.json`，不碰 SK1605/MING-102/MING-107、三命 HY1521、六壬大全/秘本、`geju-transit*`、`chart.*` 或共享 core。未改源文 `sources/normalized/shidianguji/SK1602/**`。

## WORK_PACKAGE_COMPLETE

本包 13 段全部有实质处理：`source-reviewed` 11，`draft` 2（两处版面标记无字），`verified` 全 false。剩余 ID：无。不是玉照定真經全书完成，也不是人工 verified。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-114`
- 分支：`codex/multica-ming-114`（基线继承 `origin/codex/multica-ming-107` @ `8fa7ded`）
- `sources/normalized/shidianguji/SK1602/text.md` SHA256 = `996873796425cdcd58e36c6e5971757e2de572577b5c161c9b3ba8f02e92f8bc`（与队列一致）
- 源层 `sourceStatus=reference-text`（识典待校）；电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 网站章节名不等于印本卷号；经句与张颙注、馆臣提要分层；补本不替代主文本、不计独立投票；未把主本注释复制进识典

## 段落账本（13/13）

| # | paragraphId 尾 | kind | review | 去向摘要 |
|---|---|---|---|---|
| 0 | P…1954698 | 序跋目录 | source-reviewed | 卷端「欽定四庫全書」 |
| 1 | P…1971082 | 序跋目录 | source-reviewed | 书名「玉照定真經一卷」 |
| 2 | P…1987466 | 序跋目录 | source-reviewed | 网站章节名「提要」 |
| 3 | P…2003850 | 评注或元数据 | source-reviewed | 馆臣提要：依托、江南方言疑、永乐大典辑存；外亲穿凿批评 |
| 4 | P…2020234 | 序跋目录 | source-reviewed | 总纂官题名 |
| 5 | P…2036618 | 序跋目录 | source-reviewed | 总校官题名 |
| 6 | P…2053002 | 待核实 | draft | 仅版面标记，无可转存文字 |
| 7 | P…3330954 | 序跋目录 | source-reviewed | 正文前重复馆题 |
| 8 | P…3347338 | 序跋目录 | source-reviewed | 题「玉照定真經張顒注」≠作者已考定 |
| 9 | P…3363722 | 规则候选 | source-reviewed | L68–362；subsections×15；末跨段至东王翁 |
| 10 | P…3380106 | 规则候选 | source-reviewed | L364–673；subsections×12；末跨段木入烟中 |
| 11 | P…3396490 | 规则候选 | source-reviewed | L675–1001；subsections×13；含段末图像占位不补字 |
| 12 | P…3412874 | 待核实 | draft | 仅版面标记，无可转存文字 |

ID 全称前缀：`yuzhao-shenying:shidian-SK1602:`。起讫：`P7639282082211954698`–`P7639282082213412874`。

## Multica 核源要点

对照电子原文独立写识典注解，不覆盖主本 2 段、不复制主本 vernacular 进识典。长段按完整逻辑拆 subsections，保留条件/救应/反转/未知；跨网站段未完句互相 related 连读。

关键条件（节录）：

- 生气须日时见三合长生或干长生；天德合另层；有德无合例保留
- 身命夭贱须支刑且纳音克，不是只见刑
- 干轻音重；同干丁六月可为官、五月为鬼
- 伏吟在家、返吟他处；旺气刑身才加重官事
- 墓有旺为库、无旺为墓；合须有气，败空合不算
- 丙亥丁子「不为前说」须真合条件
- 本卦须得时；失时客卦；返克另断
- 内合外合按是否本干；隔合、墓绝合、暗合分层
- 延月只胎时干合，日胎合不算
- 九宫甲子加、乙卯乘六八，算术不一保留 unknown
- 前五位推亲连读提要「外亲穿凿」批评
- 六害/六合有方向，主客不可对调后仍贴原意
- 正道歌真化须长生建旺；救神问克后有生
- 神煞劫亡非本理；天禄天马非只本禄本马
- 借气明说胎不取；旺官败鬼

疑文/残：两处版面标记 draft；三段长文跨段未完；九宫算法不一；空亡偏正含糊；段末一图未转写。𧰼/㫖/依託/附㑹等不改正文。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json --json
```

结果：`ok=true`，`entries=13`，`source_reviewed=11`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。下一 ID：无（本包收束）。
