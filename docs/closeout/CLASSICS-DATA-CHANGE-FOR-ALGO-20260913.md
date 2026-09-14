# 古籍消费方数据版本（2026-09-14）

仓：`linyuhanggg/fateradar-classics`
精确数据版本：`d3d3cdc9d3c1c293f7abc46a982a7ad8cc449716`。本轮不改executable、source-cases或产品pin。

- 新增奇门PDF300–307，原source段落ID保持；新增68个page-scoped段落。使用 `nlc-layout-page-reviews.json` 区分已核段与5个疑字段。
- 302甲戌的断语在303页；305辛卯在306页续；306丁酉在307页续。301戊辰短文在302页重见，不另增一个时辰。注释以relatedParagraphIds连接。
- 303乙亥仍属甲己日；乙庚日从丙子开始。305丙辛日从戊子开始，307丁壬日从庚子开始。
- 麻衣39段新增figureEvidenceIds；`figure-transcriptions.json`给出题字、画面、未决及本地图像。text.md用「插图校读」标记编辑文字，不能当古籍正文断法。保留上游附着，不保证插图与同段正文一一对应。
- 麻衣题字14图转写、10图未见可辨题字、15图内部未决；所有父段未因取图自动升级。
- 14条注释完成电子续接；使用其relatedParagraphIds，尤其皇极己酉记事不得错误归入戊申。
- source-reviewed60,173是电子/指定原图范围审读，不等于全部影印verified、算法准确率或产品交付率。仍有1,182条实质未决及封面1条。
- 308–311既有跨页映射仍有效；canonical_eligible仍false。
