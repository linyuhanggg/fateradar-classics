# 撼龍經合刊 · 识典 SK1589 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/fengshui/hanlong-jing--shidian-SK1589.json`（新建）与本进度文档。未改源文 `sources/normalized/shidianguji/SK1589/**`。禁止改主本 `references/annotations/fengshui/hanlong-jing.json`（现仅 6 条 `hanlong-jing:L####`）。不碰青囊、协纪主本/SK1619、折中、指南、引擎、`chart.*`、SK1591。

## WORK_PACKAGE_COMPLETE

本包索引 **0–85**（全量 86 段）全部有实质处理：`source-reviewed` 86（其中 `待核实` 1：残句跨段），`verified` 全 false。不是《撼龙经》全书他本完成，也不是主本 L 行号包，也不是引擎/排盘接入；remaining 索引口径 **0** ≠ 人工 verified。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-204`
- 分支：`codex/multica-ming-204`（基线只读权威树 `fateradar-classics-grok-full-library` @ `1fd3a37`）
- `sources/normalized/shidianguji/SK1589/paragraphs.json` SHA256 = `7b83cd6f40c5c734cdb6fb8a7240d6a5a1253c5610bdbe5815fb5139d7b242b0`（86 段，与 Issue 一致）
- `sources/normalized/shidianguji/SK1589/text.md` SHA256 = `a7aa4b66010d8cacfb28764a76bb3ff812d533277e70f97519b419040df02320`
- 稳定 ID 与 `tools/source_paragraphs.py` / `references/source-editions.json` 中 `shidian-SK1589` 对齐
- 网站章节名 ≠ 印本卷号核定；不 OCR、不抓站
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 差集：源 86、既有识典注解 0 → 从索引 0 新建 primary 识典注解

## 段落账本（86/86）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 四库卷端 / 提要 / 馆臣 | 0–4 | `…P7351705562645561382`–`…P7351705562645626918` | 著录行、合刊类目、提要作者考据与三书概要、总纂总校 |
| 撼龙经题署 | 5–7 | `…P7351705562645643302`–`…P7351705562645676070` | 四库行、书名、杨筠松题署（≠已考定） |
| 撼龙正文：干脉平洋→九星→穴形末歌 | 8–53 | `…P7637913202204950574`–`…P7637913442221470766` | 须弥干枝/平洋、北辰九星、贪巨禄文廉武破辅弼及罗星官鬼、末歌与三盖总纲 |
| 疑龙经上/中篇 | 54–60 | `…P7637913445089998871`–`…P7637913445090230323` | 卷端题署、上篇干枝迎送关局、中篇背面缠护明堂 |
| 葬法倒杖 | 61–85 | `…P7639188276951138342`–`…P7639188276951531558` | 认太极、分两仪、倍八卦十二倒杖及盖粘倚撞斩截坠正求折挨并斜插专释 |

- 起始：`hanlong-jing:shidian-SK1589:P7351705562645561382`
- 本批止：`hanlong-jing:shidian-SK1589:P7639188276951531558`（索引 85）
- **nextId**：无（全量完成）
- **remaining**：0（索引口径）

## 质量要点

- 禁止模板填白话；条件/救应/反转/未知分开；末歌简断与正文变形护送例外分层，不互相覆盖
- `verified` 全 false；非人工校勘；不与主本 `L####`、SK1619/SK1591 混写
- 九星官鬼空亡在本书为形势术语，不套八字六爻或现代天文同名字段
- 当前产品没有宅形/龙砂穴水输入，不写成已接入风水排盘
- 官阶、科第、疾病、败国等旧象不作现实验证

### doubtful / unknown（本包 1 处）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `hanlong-jing:shidian-SK1589:P7639188276951466022` | 81 | `待核实`；仅残句「须傍藉生生之气，借资化」，与 82 挨法专释跨段相续；保留 unknown，不补造原文 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/hanlong-jing--shidian-SK1589.json --json
```

结果：见交包评论（目标 `ok=true`，`entries=86`，`errors=[]`）。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书他本完成，也不是引擎包。
