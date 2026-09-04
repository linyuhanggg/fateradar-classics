# 需要人工判断

机器已把能在原文唯一（或目录+正文双处）定位的规则补上锚点。下列条目保持 `anchor: null`，不要硬锚。全部 `verified` 仍为 `false`。

## 著作权 / 无全文

- `san-shi/qimen-faqiao` QM-P26、QM-P36：仓库无 fulltext，禁止抓现代出版社整理本。

## Pack 元规则（不在书中）

statement 含「安全改写 / reframe / 不替代 / 并读 / 调用本 pack」等，原文无对应句：

- `bazi/shenfeng-tongkao` R01–R05
- `luming-nayin/lantai-miaoxuan` M01、R01–R07
- `divination/bushi-zhengzong` R01–R06
- `xingming/xingming-suyuan` XINGMINGSUYU-042 不替代子平、XINGMINGSUYU-043 旁证层

## 原文多次出现、无法唯一落点

- `xingming/xingming-suyuan` 五曜连珠（4 处）、度主为正、飞廉、转生、闌干煞、流年三方对照
- `divination/meihua-yishu` 乾兑属金（五行配卦多次）
- `divination/zhouyi-zhezhong` 「形而上者谓之道」「见几而作」等经文多次
- `luming-nayin/wuxing-jingji` 纳音 / 华盖单字标题过短

## 现代概括，书中无对应命题

- `divination/huangji-jingshi` HR-01 元会运世换算、HUANGJIJINGS-007/020/021「非占断 / 非国运 / 非个人命术」
- `xingming/xingming-suyuan` 卷四后篇案例总述

## P7 恢复名单

从 `0abcf1e` 恢复 33 条（原名单 34 条里 `LZ` 已撤回）。`FZ` 仍为 `anchor: null`。

- `LZ`（`physiognomy/liuzhuang-xiangfa`）quote 是 `source_base:` 元数据，P7 恢复名单误列，已改回 `anchor: null`。
- `FEIXINGZIWEI-008` 对应度 0.140、`ZIWEIDOUSHUQ-ZW-05` 对应度 0.106，V14 WARN。本机 `fold_han` 用 opencc t2s（无 zhconv），未改 quote、未再降级。

## P6 灰区（对应度 0.15–0.30）

任务书要求机器不动这一档，留人抽检。不要为了覆盖率把任务 5 已降级的 `<0.15` 填回去。

完整降级清单见 `tools/reports/p6-downgrade.md`。ZPR-03 等已按 P7 名单恢复。

本机未找到 `/Users/yuhanglin/sync/code/FATERADAR_CLASSICS_P6_GOAL.md`，任务 0→8 按 nmem 会话 `claude-code-ddeb375d-2209-4b50-a61d-7776ccd62cfd` 的任务书摘要施工。

## V11 与 G1

G1 要求 V11 < 50，当前约 112（未锚 paraphrase + 已锚原文与 `book.script` 不一致）。

- 未锚规则的 quote 仍是现代概括，若清空会触发 V9 错误；若做简繁转换则改动 quote，均未做。
- 已锚规则 quote 取自 fulltext，与 `book.script` 登记不符时未改 script、未放宽 V11。

需人决定：是否按 fulltext 实际用字改正 `book.script`，或接受 V11 残留。

## P10 任务 3：七政格局 / 行限未加 FactKey

任务书 3a 要求加 `qizheng_geju`、`xingxian`。按 3c：引擎必须从**已有排盘结果**取出；取不到就回退、不许为产出事实改排盘。

实测 `buildQizheng` / `emitQizhengFacts` 只有 `stars`（宫位、宿度、庙旺、顺逆）和 `palaces`，没有格局名或行限宫位字段。从黄经现算「五曜连珠 / 二星合璧 / 洞微百六限」等于新写分析算法。按 3c 不加这两个 key。约 35 条七政未映射规则本轮仍空。

紫微侧可取：`decadal.accent` 的 `palace` → `daxian`（emit 改为当前大限宫位名）；当前年柱地支 → `liunian_taisui`。未改 `ziwei.ts` 排盘。`daxian` 词表暂保持开放数组：关闭成十二宫会让既有「宫名 N–M」谓词无法通过 `isLegalFactValue`（产品仓 89 测红）。等任务 4 改完 yaml 后再关。
