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

## V11 与 G1

G1 要求 V11 < 50，当前 113（未锚 paraphrase 75 + 已锚原文与 `book.script` 不一致 38）。

- 未锚规则的 quote 仍是现代概括，若清空会触发 V9 错误；若做简繁转换则改动 quote，均未做。
- 已锚规则 quote 取自 fulltext，与 `book.script` 登记不符时未改 script、未放宽 V11。

需人决定：是否按 fulltext 实际用字改正 `book.script`，或接受 V11 残留。
