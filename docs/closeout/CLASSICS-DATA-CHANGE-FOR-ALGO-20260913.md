# 给算法任务的数据变更说明（古籍专项滚交）

- 仓：`https://github.com/linyuhanggg/fateradar-classics`
- **精确版本**：`31554216cb4097819b3f4a088cd2ce01b4d749ed`（父提交 `e90da1abd98fb3e71dfe3210500305d05ba19940`；合入 main 后以远端 SHA 为准）
- 本批 **不改** `references/executable/**`、**不改** `references/cases/source-cases.json`

## 奇门 308–311（消费方必须改读法）

- 正式源：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md` PDF第308–311页
- 映射：`docs/closeout/evidence/qimen-308-311-column-map-20260914.md`
- **不要**再把 310 最右「戌日五不遇…」当无时支，它是 309 甲寅续文（文字在 310）。
- **不要**再把 311 最右「門辛伏吟…」当辛酉；它是 310 庚申续文。
- 311 辛酉断语从「寅刑己」起；壬戌从「休坤制」起；癸亥从「門星伏吟」起。
- 甲寅／庚申在标题页只有行标宫数，不是「该时无断语」。
- 311 仅三时支是原页事实，不是缺页。
- `canonical_eligible` 仍 false；不得当已核算法输入。

## 分型

- 總鈐残格消费集合 **664**（`daliuren-daquan` 且行号 ≥ L1040），不是 666。
- `daliuren-daquan:L1010-L1010`、`L1038-L1038` 是十二月神煞疑字，**禁止**当总钤残格。
- 39 条麻衣识典图像占位：无图内文字，禁止当相法条件。
- t24–t27 所升均为记录性锚点，`verified=false`，不得当课体/庙旺/择日/相法判断输入。

## 其它

- 注解：`source-reviewed` 60,108；`verified` 全 false
- 22 条 `implementation-gap` 与证据未决仍在 `references/executable` 的 `named_gaps`；实现属算法任务
- 产品 pin 由算法/Web 任务改
