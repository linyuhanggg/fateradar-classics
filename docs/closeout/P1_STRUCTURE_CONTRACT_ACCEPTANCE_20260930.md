# P1 八字结构类合同：接受记录（2026-09-30）

本记录补在裁决书 `P1_STRUCTURE_CONTRACT_ADJUDICATION_20260930.md`（`4807723`，未改动；复算器钉住其字节）之后，写明合同为何从 `pending_product_fixture` 改为 `accepted`。仍是受托裁决（Claude，`claude-opus-5-5`，用户委托、无人工复核），不得引用为人工出处核验。

## 接受依据

- **合同**：`docs/closeout/P1_BAZI_STRUCTURE_CONTRACTS_20260930.json`，`status: accepted`、`verified: true`、`verificationMethod: delegated_adjudication`。四条合同的编号、锚点、模板与裁决书第 10 节一致（C1 提交 `508cb14` 起未改语义，本次只填夹具声明、翻转状态、改写第四项核验说明）。
- **产品实现**：cosmic-fortune-lab `b50be4b`（分支 `codex/r1-structure-20260930`）的 `src/lib/rules/structure-contracts.ts`，按裁决书独立实现，不读本仓 Python。
- **真排盘夹具**：`tools/reports/p1-bazi-20260930/structure-contract-fixture.json`，由产品 `scripts/eval/dump-structure-contract-fixture.ts` 真排盘生成，与产品仓 `tests/fixtures/bazi-structure-contract-fixture.json` 逐字节相同；SHA-256 `e00d268a84c1e74e7e3aff30ed9a567c899fe97a6df7f2bc9d402149b8ae16fb`；780 行：coverage388 388 行（88 张大赛盘与 300 张固定种子合成盘）、named 2 行（1968-04-24 12:30 上海真太阳时男“戊申 丙辰 甲子 庚午”，1990-04-09 08:30 上海真太阳时男“庚午 庚辰 甲辰 戊辰”）、time_removed 390 行（以上各盘删去时柱全部事实）。夹具只存本命干、支、藏干事实与求值结果，不存姓名与出生输入。
- **双实现一致**：`python3 tools/verify-p1-structure-contracts-20260930.py` → `PASS: 42361 checks, 29 synthetic cases, productFixture=verified`。逐行比对三态、柱位、未知柱与缺键、冲突、是否显示与未显示原因、显示次序与正文句，全部一致；每条满足的正文与折叠都过了产品文案闸快照。
- **测试**：`python3 tools/test-verify-p1-structure-contracts-20260930.py` 22 项通过（含：accepted 而无夹具必须失败、干跑外部夹具不写文件、夹具任一字段不符必须失败）；`tools/validate-rules.py`、`tools/test-predicate-lang.py`、`tools/test-eval-predicates.py` 通过；`sources/` 与各书 `rules.yaml` 相对 `672aabc` 未改。

## 覆盖（按盘去重，只是显示策略的统计，不是准确率）

| 样本 | 盘数 | 至少一句 | 两句 | 三合 | 子午 | 卯酉 | 甲日辰月 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coverage388 | 388 | 67 | 1 | 16 | 23 | 27 | 2 |
| named | 2 | 2 | 1 | 1 | 1 | 0 | 2（1 句因上限未显示） |

删去时柱后（time_removed）三合、子午、卯酉分别有 171、142、147 盘转为信息不足，甲日辰月 4 盘；页面对信息不足不出句子。当前产品排盘入口都要求四柱齐全，这一组只验证“未知柱可补位”的逻辑。

## 之后

- 产品重新导入本合同后，命格总览本命视图才会显示结构句；上线、浏览器验收与发布记录在产品仓。
- 对裁决书或合同的任何改动都要同时改合同、复算器里钉住的提交号，并重新生成夹具、重跑双实现比对。
