# 神相全编 · 识典 SDZJ0174 语义扩写账本

独占文件：`references/annotations/physiognomy/shenxiang-quanbian--shidian-SDZJ0174.json`。  
原文只读：`sources/normalized/shidianguji/SDZJ0174/text.md`（SHA256 `00e07f58…`，与 corpus-3 队列一致）。  
段落账本：`docs/book-reviews/cursor-expand-shenxiang-quanbian-remaining.json`。

基线 `d47f77d` 的 748 条是 corpus-3 交包初稿，不是语义验收。本分支从该基线独立续写。`verified` 一律 false。电子文本锚定 ≠ 模型语义审读 ≠ 人工校勘 ≠ 相术预测有效。

## 源文实数

| 网站章节 | 段数 | 去向 |
|---|---:|---|
| 神相全编（扉页） | 3 | 题署 / 书名 / 刊记 |
| 神相全编序（倪岳序 + 十二卷目录） | 425 | 序跋目录；有目无文不补正文 |
| 神異賦 | 261 | 赋句与注连读；理论 / 规则候选 / 案例 |
| 神相全編卷之六 | 3 | 卷端题署 |
| 金鎻賦 | 5 | 长段须 subsections 覆盖父段起迄 |
| 神相全□卷之十二 | 3 | 卷端；□ 为疑文 unknown |
| 黄色吉㐫相 | 48 | 气色条例，官/庶、四季、救应分套 |
| **合计** | **748** | 以源文段落索引为准 |

本残本 `catalogComplete=false`。目录所开卷一至十二绝大多数篇目有目无文。正文目前只有神異賦、金鎻賦（夹银匙歌）和卷十二黄色吉㐫相残章。

## 已核验后的处理原则

- 目录、序跋、卷端、刊记：`序跋目录` 或 `评注或元数据`，只标去向，不升成规则。
- 神異賦、金鎻賦、黄色吉㐫相：对照原文写现代白话和成立前提；否定、例外、转折、救应与前后文同一审读单元。
- 五星六曜、十二宫、罗计、水星救护在本书是面貌部位或气色，不是紫微十二宫、不是实际七政、不是八字神煞自动查取。
- 题署麻衣、希夷、袁柳庄、许负、吕纯阳等不是已核传授史。
- 没有底本的疑文（𥙍、□、𡮢等）标准确位置和 unknown，不发明字句。
- 相法进知识库，不造八术算法规则，不改 inventory / 公共导出 / 算法 / main。

## 进度

- 本轮已完成：扉页 3 + 序与目录 425 = **428**。
- 累计完成 / 剩余：428 / 320。
- 下一轮从账本 `remainingIds` 第一条神異賦继续，不重复已完成 ID。

## 校验

`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/physiognomy/shenxiang-quanbian--shidian-SDZJ0174.json --json`

结构通过不是语义证书。未提高 `verified`。
