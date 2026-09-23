# ZPR-P1-03：P1 八字 11 条正式交接候选（2026-09-23）

古籍仓已形成可复跑的 11 条 P1 manifest，等待产品仓独立审核和导入。第 11 条 `ZPR-P1-03` 仅属于 `overview`，角色为 `source_classification`：当 `ZPR-P1-01` 所指的甲日辰月透戊偏财入口成立时，给**该入口**附 `财 → 顺用` 的来源候选分类。它不裁决唯一用神、实际顺用路线、喜忌、成格、财运作用，也不改变 `ZPR-E-02` 的 `applicable_to`、`rescue` 或 `verified=false`。

## 锁定物与此前 10 条审计

| 对象 | 固定版本／SHA-256 |
|---|---|
| 源规则提交 `CLASSICS_REV` | `b9d7bb5413f042901c8bcd4635327ba585992d66` |
| 新 manifest | `13aa085a01b40add88b4fe3582ce1ac3ea601878a09291c37c2538cd99c740d1` |
| 此前产品已锁 10 条 manifest | `c645237397039d001367ad2df6f624d0f363f1daee9ca07fdf3031b4f511d6ab` |
| 旧 10 条语义字段指纹 | `d2587a335b380fe63d152e3283f0d24c645c31dd9fd33ec244cb729a76b5b63b` |
| 两仓相同的 43-case fixture | `6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb` |

新增前，古籍仓工作树的 10 条 manifest 与产品仓已锁 `c645…` **整文件逐字节相同**；43-case fixture 逐字节相同；旧 10 条的 `statement`、`quote`、`anchor`、`applicableTo` 与产品已生成八字规则逐条一致。新增后的 generator 锁定旧 10 条 `ruleId/statement/quote/anchor/applicableTo/primaryTopic/secondaryTopics/role/status/applicableLayers/unsupportedLayers` 的规范化指纹，变化只包括新规则、版本/来源指纹、总览规则清单与 10→11 条数量。其它五个主题的规则归属不变。新 manifest 为 `fateradar-p1-bazi-topic-handoff-v2`，`semanticContractStatus=pending`、11 条均 `verification.verified=false`。

`candidateOutput` 是 `ZPR-P1-03` 满足时附在 `RuleEvaluation` 上的来源输出元数据，不是独立 `FactKey`，不能回填本规则的 `applicableTo`。不满足和信息不足均无方向输出；缺逐柱 `gan` 的真实样盘为 `信息不足`，不能降为 `不满足`。戊癸兼透样盘仍有偏财入口，但 `兼透则兼用` 不许写成独占入口。产品若展示该分类，必须同时保留三段 `candidateSources`：L328 的善而顺用分类、L544 的透戊偏财入口、L548 的兼透并用；单独的主 `anchor=L328` 不支持完整陈述。

清单里的 `exceptionsAndBreaks` 是兼容旧 10 条格式的 `caveats` 同内容别名；产品展示只取 `caveats` 一份，不把两个数组相加。第 11 条的原规则 caveat 与交接补充 caveat 已在单个数组内去重。

## 复跑与产品入口

```bash
cd /Users/sync/code/fateradar-classics
python3 tools/generate-p1-bazi-manifest.py --output docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json
python3 tools/verify-p1-bazi-11-handoff.py
python3 tools/verify-zpr-p1-03-direction-candidate.py
```

源文件和人读边界见 [`ZPR_P1_03_DIRECTION_CANDIDATE_20260923.md`](./ZPR_P1_03_DIRECTION_CANDIDATE_20260923.md)，完整机器交接见 [`P1_BAZI_TOPIC_MANIFEST_20260921.json`](./P1_BAZI_TOPIC_MANIFEST_20260921.json)。样盘正例 `caseP1_ZPR_01_wu_only` 为满足，反例 `caseP1_ZPR_01_no_wu` 为不满足，后者删去年干事实为信息不足；`caseP1_ZPR_01_wu_gui_both` 验证兼透仍满足。机器验证还逐项检查原文三锚、43-case 指纹、11 条唯一 ID、仅总览归属和旧 10 条不漂移。

产品仓目前仍锁上述 `c645…` 的 10 条 v1 manifest 和对应 10 条 generated 规则；当前产品 importer 只接受固定 10 条及其生成文件完全一致。产品审核新 v2 合同后，须同步扩展 importer 以保留 `source_classification`、`candidateOutput` 和 `candidateSources`，先对齐生成规则再消费本 manifest。新锁未导入前，不能声称产品已消费第 11 条。此次古籍侧仅本地提交，不推送或升级 E-02。
