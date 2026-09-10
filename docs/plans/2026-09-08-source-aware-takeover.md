# 识典书源与全库开发接手 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 接续完整全库/八术开发，保全遗留成果，接入已取得的识典原文字段，收尾六壬、奇门与岁运真实消费者。

**Architecture:** 两仓继续使用 codex/full-library-completion 独立工作树。原主文本及其段落ID保持；新版本走 source-editions，识典段落使用上游ID和本地引用行号。候选新书只进入研究检索，不自动解除算法证据排除。

**Tech Stack:** Python JSON/Markdown 来源工具；TypeScript 确定性引擎；TanStack 现有页面；unittest、Vitest、ego-browser。

## Task 1: 接管与保护遗留稿
- 已保存两仓HEAD/dirty patch/相关untracked到 `/tmp/fateradar-takeover-20260908`，不包括他人的 `.claude`。
- 读取最新完整方案、实际代码和nmem；用户最新继续开发指令覆盖此前暂停。
- 文件所有权：bazi_transits拥有岁运引擎；liuren_finish拥有六壬引擎/规则/独立证据模块；qimen_finish拥有奇门局式稿/fixture；root拥有来源导入、通用导出、总索引及必要消费者。

## Task 2: 识典原文字段导入与稳定引用
Files: `tools/import-shidian.py`, `tools/test-import-shidian.py`, `tools/source_paragraphs.py`, `tools/test-source-editions.py`, `references/source-editions.json`, `sources/normalized/shidianguji/`.
1. 写失败测试：父子重复返回不重复计段；原字保留；网站译文不导入；图像不假扮文字；上游段落ID不随前章长度漂移。
2. 运行 `python3 tools/test-import-shidian.py`，确认失败来自缺实现。
3. 导入本次已取得37版本并记录范围；有对应书的版本按独立edition进入检索，短篇/相关书不冒替目标全书。
4. `source_paragraphs.py`读取明确的上游段落索引，保留主索引不变；测试来源/范围正确。
5. 《命海全编》作为未校参考书进入书房，不生成排盘规则或人工verified。

## Task 3: 遗留三术开发
- 岁运：接收externalPillars、实际before/after作用；本命与运/年位置分开；消费者使用同一结果；撤下静态喜忌分数断顺逆。
- 六壬：实算组合/位置/节令/贵人，输出计算边界与原文；root接chat统一事实。
- 奇门：固定提交导出原书案例；印刷输入不明不得自动复算；图式/附断只按已核范围登记。
- 各流先跑对应失败测试，修改真实producer并复跑；不刷新golden/verified。

## Task 4: 审读稿与固定快照出口
Files: `references/annotations/fengshui/rudi-yan-quanshu.json`, `tools/export-knowledge.py`, `tools/test-export-knowledge.py`, `references/inventory/`, 产品`src/lib/engine/generated/knowledge/`.
1. 校验入地眼126段ID/范围与已审读修正，完成书评/来源状态。
2. 新来源导出测试确保不会升级白话审读状态或让候选书进入算法。
3. 先提交古籍固定内容，再从同一revision导出产品分包，不把dirty冒充HEAD。
4. 核对新增来源和旧主ID无漂移、原文链接准确。

## Task 5: 消费者与合并验收
- 对实际改动运行对应unittest/Vitest；全体提交整合后运行产品全测、typecheck、lint:ci与生产build。
- 网页用ego：新增来源可查、未经校对标签准确、换资料/选岁运同步改变盘面和解释；不强行依赖模型服务。
- 更新 `docs/GOAL_PROGRESS.md`、两仓交接说明。现有完整方案仍是总范围；首批合格不等于全库总验收。
- 后续依实际未处理原文和算法缺口继续施工。只推自己的分支，不合main、不部署生产。
