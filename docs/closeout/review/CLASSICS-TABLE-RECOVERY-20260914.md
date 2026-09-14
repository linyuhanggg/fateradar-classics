# 2026-09-14 总钤与奇门连续施工记录

本记录只验收此批数据改动，不代表全部古籍完成。基线：860f0bd80c7c1ad9340d6c4312a93079a7da338b。

## 实际恢复

- 四库《六壬大全》PDF16–25，每页12格，共120格。逐格保存页码、图位、格头左右字、小字分组和三字串；原图重复字照录。影印SHA256在`siku-zongqian-cells.json`可复算。
- 120格分别有稳定段ID、解释及精确审读范围；11条现代编辑说明保持draft，未计作古文。
- 旧电子总钤664条失去格位的碎片保留原文、ID和draft状态，仅归档关联完整总表索引。没有声称664条逐字校准、没有建立猜测的字→格映射。原全文与基线字节相同。
- 奇门PDF308–311补32条注释：21条source-reviewed，8条现代说明与3条疑字正文保持draft。309己酉修复跨列断句，庚戌补回原图“地丙傷乾制”；戊癸日组从壬子起。3处疑字段同步撤销源层已审读覆盖，避免导出状态矛盾。

## 独立复核

三个只读审校员分别完成16–18、19–20、21–25原图转录及交叉复核。Judge A（qimen_source_scout）与Judge B（qimen_later_scout）均接受最终120格及其JSON→Markdown→段ID→注释→reviewRanges的一致性。19–20另由qimen_candidate_judge独立对图接受24格。

664碎片归档由qimen_source_scout和qimen_candidate_judge独立核对基线，均接受；限定为历史转写归档，不把旧残字改称正文已核。

奇门先由qimen_candidate_judge拒绝：白话擅补天字、遗留未决notes、疑字段reviewRanges过宽。全部修复后，qimen_candidate_judge与qimen_later_scout均接受最终三文件差异。未经核实的字不因同页其他段通过而升级。

## 验证

- `python3 tools/validate-annotations.py`：53 books、63070 entries、0 errors。
- `python3 tools/test-source-editions.py`：6 tests pass。
- `python3 tools/test-validate-annotations.py`：12 tests pass。
- `python3 tools/test-zongqian-layouts.py`：3 tests pass。
- `git diff --check`：通过。
- 直接调用`export-knowledge.build_export`读取候选工作树：55本、81120段；逐项核实120已审格、664归档链接及奇门3处疑字未核状态均进入实际导出。

## 继续施工范围

本批没有完成其他书的全部校读。须继续审查旧待审队列及无注释段的实际去向。导出代码已经包含所有注册正文；无annotation段的状态是`unreviewed`，不能误称“没有入库”，也不能因为已有章节包done就称逐段审读完成。短干支全文相同不足以迁移其所属年月、格位或规则语义。
