# 柳庄相法 · 主本语义审读进度 · 2026-09-11

独占文件：`references/annotations/physiognomy/liuzhuang-xiangfa.json` 与本进度文档。未改源文 `sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md`。不碰青囊/撼龙/协纪/引擎/`chart.*`、麻衣/神相全编/冰鉴注解。

## WORK_PACKAGE_COMPLETE

本包主本 inventory **2/2** 段一次性语义审读完成：`source-reviewed` 2，`verified` 全 false。长段 `L0007-L0933` 以 **135** 个具名子节覆盖上册章题与中册永乐百问，非子节模板填空。不是相法全书校勘，不是影印人工 verified，不是八术算法覆盖。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-210`
- 分支：`codex/multica-ming-210`（继承 `origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`）
- `sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md` SHA256 = `d94f837fd8fb1e3f636d9cf21d73fdf6300c7cc61669c9a8f0015da4eb72adfe`
- inventory：`references/inventory/paragraphs/physiognomy/liuzhuang-xiangfa.json` 仅 2 段；权威差集：注解文件本包新建前不存在
- NLC PDF 仅影印锚点，未逐页 OCR；不抓站
- 电子语义阅读升 `source-reviewed` ≠ 人工 verified

## 段落账本（2/2）

| paragraphId | kind | 处理摘要 |
|---|---|---|
| `liuzhuang-xiangfa:L0003-L0005` | 评注或元数据 | CTP Wiki / 影印锚点 / 高风险断语声明 |
| `liuzhuang-xiangfa:L0007-L0933` | 理论 | 上册部位·十二宫·贵贱清单 + 中册永乐百问；135 子节 |

- **nextId**：无（本 inventory 段落集已尽）
- **remaining**：0（相对本注解文件 paragraphId 集合）
- 不宣称识典短篇或其他相法书完成

### 子节结构（长段）

| 区段 | 子节约略 | 行范围 |
|---|---|---|
| 上册标记与胎产婴幼 | S001–S019 | L7–94 |
| 五行五官荣枯寿夭 | S020–S026 | L95–156 |
| 五官五星分论与精神血气 | S027–S041 | L157–211 |
| 乾坤赋女相 | S042 | L212–258 |
| 头面项背全身部位 | S043–S072 | L259–397 |
| 满庭芳·十二宫·十八贵 | S073–S077 | L398–527 |
| 女男清单与寒通气色 | S078–S089 | L528–775 |
| 行坐卧食语笑与五行形赋 | S090–S096 | L776–834 |
| 中册永乐百问 | S097–S135 | L835–933 |

## 质量要点

- `verified` 全 false；非人工校勘
- 禁止把七十二贱/刑克/性部位/民族形貌词用于现实歧视或预测
- 同名「三停」「三阳」「五官」按节分层，不与紫微十二宫自动合并
- 相法可检索 ≠ 已接入八术 / 算法覆盖 / 预测有效

### doubtful / unknown（保留，不改正文）

| 位置 | 处理 |
|---|---|
| 「临盆可定曰期」 | 曰/日疑，保留 |
| 「夷相法」等用字 | 保留 |
| 兰台「延慰/廷尉」 | 异写并存 |
| 七十二贱「舅油」 | 疑讹 |
| 寒通「气色定行年」 | 疑脱文 |
| 古望人「孟堂君夜津阔津」 | 疑文 |
| 五行赋末句 | 拗口疑脱讹 |
| 「办有重瞳」 | 办字疑讹 |
| 五反「挂紫友」等 | 疑脱讹 |
| 南北条地理表述 | 文本问题保留 |
| 得妻财反穷文末「出嫁夫」 | 疑截断，不补造 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/physiognomy/liuzhuang-xiangfa.json --json
```

结果：`ok=true`，`entries=2`，`source_reviewed=2`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。本包完成主本 2 段注解，不是相法类全书完成。
