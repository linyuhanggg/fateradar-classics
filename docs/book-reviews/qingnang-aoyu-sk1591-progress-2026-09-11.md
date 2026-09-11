# 青囊奧語 · 识典 SK1591 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json`（新建）与本进度文档。未改源文 `sources/normalized/shidianguji/SK1591/**`。禁止改主本 `references/annotations/fengshui/qingnang-aoyu.json`（现 3 条 `qingnang-aoyu:L####`）。不碰撼龙 SK1589、协纪 SK1619/主本、引擎、`chart.*`。

## WORK_PACKAGE_COMPLETE

本包索引 **0–2**（全量 3 段）全部有实质处理：`source-reviewed` 3，`verified` 全 false。不是《青囊奥语》全书他本完成，也不是主本 L 行号包，也不是引擎/排盘接入；remaining 索引口径 **0** ≠ 人工 verified。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-212`
- 分支：`codex/multica-ming-212`（基线只读权威树 `fateradar-classics-grok-full-library` / `origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`）
- `sources/normalized/shidianguji/SK1591/paragraphs.json` SHA256 = `f0da58e34eca279bb49d889210d34556b357e0db032c470e8c97ffdd8ddf0c0c`（3 段，与 Issue 一致）
- `sources/normalized/shidianguji/SK1591/text.md` SHA256 = `ab9b36f0e7547366cfee1345551cce66cc422e70a8c7bf42380a9b784f606d60`
- 稳定 ID 与 `tools/source_paragraphs.py` / `references/source-editions.json` 中 `shidian-SK1591` 对齐
- 网站章节名 ≠ 印本卷号核定；不 OCR、不抓站
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 差集：源 3、既有识典注解 0 → 从索引 0 新建 primary 识典注解

## 段落账本（3/3）

| 区段 | 索引 | paragraphId | 处理摘要 |
|---|---|---|---|
| 四库卷端 | 0 | `qingnang-aoyu:shidian-SK1591:P7429803488521076771` | 钦定四库全书著录行 |
| 题署 | 1 | `qingnang-aoyu:shidian-SK1591:P7429803488521109539` | 书名与唐杨筠松题署（≠已考定） |
| 口诀正文 | 2 | `qingnang-aoyu:shidian-SK1591:P7429807485487366179` | 干支星曜、阴阳元空、十项观察、倒杖放水与进退生克 |

- 起始：`qingnang-aoyu:shidian-SK1591:P7429803488521076771`
- 本批止：`qingnang-aoyu:shidian-SK1591:P7429807485487366179`（索引 2）
- **nextId**：无（全量完成）
- **remaining**：0（索引口径）

## 质量要点

- 禁止模板填白话；条件/救应/反转/未知分开；`verified` 全 false
- 不与主本 `L####`、SK1589/SK1619 混写；不替代主文本投票
- 本补本用字（元空、左右行度、破軍㢲断句等）按识典原文保留；与主本维基全文差异只记 notes，不改源
- 当前产品没有宅形/龙砂穴水输入，不写成已接入风水排盘
- 官阶、财宝、灾祸等旧象不作现实验证

### doubtful / unknown（本包保留对照）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `…P7429807485487366179` | 2 | 「破軍㢲，辰亥」断句/异体与通行「破軍；巽辰亥」对照未定；左右阴阳干支区间与主本不同；若干用字异文照录，不补造改正 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json --json
```

结果：见交包评论（目标 `ok=true`，`entries=3`，`errors=[]`）。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书他本完成，也不是引擎包。
