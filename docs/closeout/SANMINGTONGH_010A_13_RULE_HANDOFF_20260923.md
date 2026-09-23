# 《三命通会》010A：甲日戊岁字面入口交接

`SANMINGTONGH-P1-010A` 已作为 `provisional`、`verified=false` 的独立来源结构规则进入 [v4 机器 manifest](P1_BAZI_TOPIC_MANIFEST_20260923_V4.json)，只归 `overview`，只适用于**所选流年**。它仅确认《论太岁》[L1081](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1081) 举出的本命甲日遇戊流年字面入口。原 `SANMINGTONGH-010` 保持 `applicable_to=[]`、`verified=false`；v4 的 `semanticContractStatus` 仍为 `pending`。

来源原句是“日犯嵗君如甲日尅戊年為偏財”。规则以本命日柱 `gan=甲`，以及所选年 `liunian_gan_zhi` 属于六个戊干支（戊子、戊寅、戊辰、戊午、戊申、戊戌）求值。用已有干支事实的六值析取，避免引入尚未列入 Fact Vocab 的 `liunian_gan` 谓词。求值时保留本命日柱事实，流年事实只取 `scope.year=selectedYear`。本条的“不满足”仅否定这个字面示例；“信息不足”涵盖本命日柱干或所选年干支缺失。有效大运未知不妨碍确认**入口**，但无法因此判断完整 010 的作用。

共享的 43 盘 [`facts-sample.json`](../../tools/reports/facts-sample.json) 字节不变，SHA-256 `6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb`。`caseP1_010_both@2018` 是甲日戊岁正例，`wrong_day@2018` 是错日反例，`wrong_year@2017` 是同盘错年反例；`unknown_luck@2018` 确认仅入口能满足而作用仍未知。从正例删去所选年干支或本命日柱干，均须返回“信息不足”。未经年份切片的 `wrong_year` 整袋还含 2018 戊岁，会误报满足；验证器专门要求切片后为“不满足”。这些测试只证明来源形态和三态，并非现实吉凶准确率。

本条不将原文“偏财”“日犯岁君”的其它干支情形推广成通用算法，不推断同柱庚申或癸戊合已经“有救”“有情”，更不输出“凶半”“凶莫能解”或任何现实事件。条件式作用阶梯仍见[010 合同](SANMINGTONGH_010_CONDITIONAL_EFFECT_CONTRACT_20260923.md)，L1085–1087 的庚辛、金局、火局及天月德仍是[中性审计](SMTH_010_POST_ANCHOR_STRUCTURE_20260923.md)；完整 010 缺独立定值的作用正例、排除反例与缺键盘。

验证命令：

```sh
python3 tools/validate-rules.py --book bazi/sanming-tonghui --json
python3 tools/verify-p1-bazi-13-handoff.py --compare-product-fixture
python3 tools/verify-sanming-010-conditional-effect.py
python3 tools/audit-smth-010-post-anchor.py
```

产品侧可按 v3→v4 的追加交接导入 `dist/rules/bazi.json` 和本 manifest；前 12 条规则对象完全不变，导出只新增 `SANMINGTONGH-P1-010A`。消费方必须在 overview 流年求值时同时保留本命 `gan@day` 与所选流年 `liunian_gan_zhi`，不得把 `SANMINGTONGH-010` 标为已完成或把入口状态写成作用结论。
