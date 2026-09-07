# 《命理约言》来源检查与恢复

**正文知识加工尚未完成。** 当前发现的首要问题是旧“全文”只有导航，不能从它整理作者理论。

## 现有稳定段落已全部处理

`references/annotations/bazi/mingli-yueyan.json` 覆盖540/540个原ID，但内容全部是网页来源或导航用途说明：来源总说明1段，source/raw路径49段，导航标签149段，文章标题链接341段。实质命理正文0段，规则候选0段，原书命例0段。`source-reviewed`不代表这些条目变成了古籍正文。

没有照《子平真诠》改写，也没有从“看用神法”等标题推断陈素庵观点。旧rules仍不能替代原文。

## 真实恢复工作

本地有185页NLC《精选命理约言》PDF，但没有可用文本层。已全量渲染与OCR，在 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 保存185页候选，182页非空，共56,625个识别字符。

OCR稿尚有误字和读序问题，状态为ocr-draft、canonical_eligible=false、verified=false。原PDF、旧fulltext和原540个ID均不改。具体探测、方法与质量限制见同目录 `recovery-notes.md`，其中已补充源清单结论。

## 验证

```sh
python3 tools/validate-annotations.py --annotations references/annotations/bazi/mingli-yueyan.json --json
```

540条来源/导航注释通过真实ID及字段校验。此项通过只证明旧导航处理无遗漏，不证明古籍正文已经恢复或算法完成。

## 尚须完成

先核对扫描版本与实际目录，逐页处理OCR错字、小字夹注和阅读顺序，再用新的稳定ID建立理论、方法与命例注释。第1、83、163页原OCR为空，已对图确认封面/卷末页并补可辨文字；第2页部分乱码及全书夹注读序仍需校核，不能直接删除或猜补。

在可靠正文建立以前，本书不输出与《子平真诠》的流派对照、不新增运行规则、不编造历史四柱或公历日期。

## 当前逐页对照进展

逐页事实记录为 `sources/normalized/bazi/mingli-yueyan/page-reviews.json`，未列页默认OCR草稿。

- PDF18至25页主体文字已查看原图，修正并列小字串读、三干/二干、曰/日等识别错误并保留跨页句子。
- PDF24页正文、版心和页码均已校核，状态source-reviewed；它是连续正文的一页，不代表整章或整书完成。
- PDF18、19、20、21、22、23、25页保留partial，项目符号或疑字仍按记录复核；第23页日干疑字未据常识猜填。
- PDF83、163页卷末文字已对照，但没有理论内容；第1页封面仍有未辨字，第10页只抽检。

正文已有可定位恢复文本；新版本以PDF页隔离生成ID，由主任务多来源管道处理，旧540个导航ID不承载新正文。整书canonical_eligible仍为false。
