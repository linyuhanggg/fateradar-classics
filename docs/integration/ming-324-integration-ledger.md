# MING-324 古籍集成账本（首批）

机器可读权威：`docs/integration/ming-324-integration-ledger.json`。

## 基线
- 集成基础：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`
- 说明：该线是 Multica 古籍审查权威快照；与 `origin/main` 无共同祖先，**不以 main 为古籍交付线**。

## 本批已合入（待独立验收）
| Pack | Source | Review | entries / sr | 状态 |
|---|---|---|---|---|
| HY1521 | MING-98 `9e2f2f2` | MING-130 `71a41755` | 2340 / 2338 | integrated_pending_acceptance |
| SK1605 | MING-102 `5f9a25a` | MING-107 `8fa7dedd` | 16 / 15 | integrated_pending_acceptance |
| SK1573 | MING-168 `a4c1eda` | MING-174 (+CP1 MING-163) | 670 / 670 | integrated_pending_acceptance |

校验：三包 + 全库 `validate-annotations.py --json` 均 `ok=true`；本批 paragraphId 交叉重复 0；未覆盖 `wuxing-jingji.json`。

## 明确未合
- 待审：MING-315/316/318/319
- 已审仍缺基线文件：六壬大全/秘本、SK1602、SK1609、SDZJ0170 等（见 JSON）
- 产品 MING-320/321/322 不在本批

source-reviewed ≠ 人工 verified。不宣称全库/产品完成。

## 远端核验
- batch1 merge: `de2105601a59f5afa18b63cc16dc4e5b7cb57fff`
- branch tip after ledger pin: `1552362ff324566eda86ef2c13c1a37ae2baf9d0`
- remote: `origin/codex/multica-ming-324`
