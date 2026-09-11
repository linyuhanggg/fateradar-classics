# 紫微斗数全书 · 识典 SDZJ0170 语义审读进度 · 2026-09-11

独占文件：`references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` 与本进度文档。未改主本 `ziwei-doushu-quanshu.json`，不碰引擎 `src/lib/engine/ziwei*`、chart、MING-110、MING-123 SK1609、MING-98 HY1521。未改源文 `sources/normalized/shidianguji/SDZJ0170/**`。

## WORK_PACKAGE_COMPLETE（CP1）

本包 CP1 索引 **0–299**（300 段）全部有实质处理：`source-reviewed` 279，`draft` 21，`verified` 全 false。不是紫微斗数全书完成，也不是人工 verified，也不是引擎包。索引 300–1069 留给后续 Multica 包。

继承：只读 corpus-1 树既有 CP1 提交 `b270c68`（不重做已完成段落）；本 Multica 分支仅保留本批 300 条，不把 corpus-1 的 CP2–CP4 整段搬进本 Issue 交付口径。corpus-1 车道已覆盖全书 1070 段（至 `dc98f2a`），后续 Multica CP 应优先迁移/继承该检查点，禁止重写。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-128`
- 分支：`codex/multica-ming-128`（基线继承 `origin/codex/multica-ming-123` @ `8def9f0`）
- `sources/normalized/shidianguji/SDZJ0170/text.md` SHA256 = `b4850fddeac0fc7b5fad40a7a93865f47c70622e348ca4f2c79b98f37a15a790`（与队列一致）
- 源层 `sourceStatus=reference-text`；`catalogComplete=false`（缺章见 provenance，未补造）
- 网站章节名不等于印本卷号；识典补本不替代主本、不作独立投票证据
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 用 `tools/source_paragraphs.py` / `paragraphs.json`；不 OCR、不抓站、不消除 1423 门槛

## 段落账本（300/300 · CP1）

| 区段 | 索引 | 起讫 paragraphId 尾 | 处理摘要 |
|---|---|---|---|
| 书名/目录/篇题 | 0–67 附近 | P…5989146 起 | 书名行、题署、目录篇题；㣲不改正文；篇题不扩成断法 |
| 太微赋注解 | 中段 | 辅弼/空亡/杀曜等 | 条件与救应分层：禄冲吉处藏凶、空亡僧道、败地金生巳救、辅弼夹帝 vs 无正曜单守离宗等 |
| 卷之三起例 | 操作步骤 | 安命身/三台八座/强弱宫/火局等 | 闰月依二月内起；大小限阴阳分法；小限只分男女；残表/缺字 draft |
| 星限吉凶诀起 | 至 299 | P…77584424997 | 男女二限值天机：照限不安减等，羊陀并巨暗才入南柯 |

ID 前缀：`ziwei-doushu-quanshu:shidian-SDZJ0170:`。

- 起始：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158859225989146`
- 本批止：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158877584424997`（索引 299）
- **nextId**：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158877584441381`（索引 300，不在本包）
- **remaining**：770（索引 300–1069；全书识典 1070 段）

## 质量要点（节录）

- 禁止模板填白话；条件/救应/反转/未知分开；`verified` 全 false
- 禄逢冲破则吉处藏凶；马遇空亡宜僧道；败地可因金生在巳母救子，亦可因禄存化禄扶持反美
- 金空则鸣、火空则发反为福；水泛木折土陷为祸
- 辅弼夹帝贪狼受制则不拘桃花；无正曜辅弼单守则离宗庶出（与夹帝富贵分层）
- 君臣庆会可被刑忌四耗同度反为奴欺主；七杀破军有制反可；杀居绝地纵有吉曜合照限临则凶
- 日月守不如照；七杀临身命须流杀并临才死；羊铃须白虎又临才刑戮
- 童限老人不宜、中年尚平和；红鸾年少婚姻、老人丧妻
- 土水长生皆起申，不据他本改水局；紫微无左右为孤君

draft 21（残表/切断/缺字/图像，不补字），含：太微赋疑脱句、纳音歌未完、流年太岁切断例、火局■、十二宫星表无庙旺、伤使祸福图未转写等。㣲/冨/㐫等异体不改正文。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json --json
```

结果：见交包评论当时输出；期望 `ok=true`，`entries=300`，`source_reviewed=279`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成。

---

## WORK_PACKAGE_COMPLETE（CP2 · MING-333）

本包 CP2 索引 **300–599**（300 段）全部有实质处理：本批 `source-reviewed` 284，`draft` 16；累计 entries=600（`source-reviewed` 563，`draft` 37），`verified` 全 false。不是紫微斗数全书完成，也不是人工 verified，也不是引擎包。索引 600–1069（remaining **470**）留给后续 Multica 包。

### 前置核验

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-333`
- 分支：`codex/multica-ming-333`（基线继承 `origin/codex/multica-ming-128` @ `1bf7a374ead5526951d6a162dea5d86e582c3c52`）
- `sources/normalized/shidianguji/SDZJ0170/text.md` SHA256 = `b4850fddeac0fc7b5fad40a7a93865f47c70622e348ca4f2c79b98f37a15a790`（与 CP1/队列一致）
- `paragraphs.json` 唯一 ID = 1070；CP1 已交 0–299 与源 ID 集合完全重合；本批差集 = 索引 300–599，**未改写 0–299**
- 继承 corpus-1 检查点 `565ee13`（CP2）/ 当前全量文件中对应切片；与本地 CP1 内容逐条一致后只追加 300–599，禁止从 CP1 再写一遍

### 段落账本（300/300 · CP2）

| 区段 | 索引 | 起讫 paragraphId 尾 | 处理摘要 |
|---|---|---|---|
| 卷之三诸星断 | 300–599 | P…77584441381 → P…82164604954 | 太阳至化忌等星性/入限/化曜；条件与救应分层；残段 draft |

- 起始：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158877584441381`（索引 300）
- 本批止：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158882164604954`（索引 599）
- **nextId**：`ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158882164621338`（索引 600，不在本包）
- **remaining**：470（索引 600–1069；全书识典 1070 段）

### 质量要点（CP2 节录）

- 天梁入限「祸必多」与「最是良」分层；化禄大限恶曜不为害；化忌入庙反佳 vs 二限家倾 vs 落陷闲宫三层并存
- 太阳夜生陷/日生庙旺；七杀遇帝为权余宫皆杀；破军梁府能制其恶；禄马交驰忌劫空
- draft 16：太阳/廉贞/天府/太阴/贪狼/巨门/天梁/七杀/破军/文曲/禄存限/擎羊/陀罗/化忌等段末截断；鿄/𠙚 等不补字；异体不改正文

### 校验（CP2 交包）

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json --json
```

结果：`{"ok": true, "books": 1, "files": 1, "entries": 600, "source_reviewed": 563, "errors": []}`。校验器只做结构与 ID，不是语义证书。
