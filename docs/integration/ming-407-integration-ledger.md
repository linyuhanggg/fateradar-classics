# MING-407 古籍集成账本（392 tip 上合入已审大六壬 CP13–CP16 审查稿）

机器可读权威：`docs/integration/ming-407-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-392` @ `f94c471dfd3771830de864fe6a5d5cf11992cebd`（验收 MING-399 `1442440` 已通过）
- 独占：`fateradar-multica-ming-407` / `codex/multica-ming-407`
- **只进 md 审查稿**，**未改** 任何 `references/annotations/**/*.json`
- **未等** MING-398 CP17
- **未合入** MING-397 秘本 JSON
- **未升** 产品唯一线 `6c1dfa3b`

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 大六壬 CP13 | MING-387 `38a9cafe` | `daliuren-daquan-cp13-review.md` | `cherry-pick -x` | `bff8af7` | integrated_pending_acceptance |
| 大六壬 CP14 | MING-390 `7f2f0fdb` | `daliuren-daquan-cp14-review.md` | `cherry-pick -x` | `d04092a` | integrated_pending_acceptance |
| 大六壬 CP15 | MING-394 `f8a16667` | `daliuren-daquan-cp15-review.md` | `cherry-pick -x` | `31f81ad` | integrated_pending_acceptance |
| 大六壬 CP16 | MING-395 `0e051e2b` | `daliuren-daquan-cp16-review.md` | `cherry-pick -x` | `1c50bbd` | integrated_pending_acceptance |

合入方式：最小路径 cherry-pick；禁止整树覆盖。

## 验证
- `git diff f94c471..HEAD`：仅上述 4 个审查 md + 本账本；**无** 注解 JSON 变更
- 识典 SDZJ0170 SHA256 仍 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261`
- 大六壬 SHA256 仍 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`
- 秘本 SHA256 仍 `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（397 未合入）
- 各审查稿 blob 与源 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批触及注解文件 `verified=true`：**0**（本批未改注解）；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是大六壬全文交付；不是人工 verified。
- 未合入 MING-398 CP17；未合入 MING-397 秘本 JSON。

## 交付 tip
- 内容合入 tip（4 审查稿）：
- 内容+账本首推 tip：
- 账本 tip 指针提交：
- 远端 tip：（，施工分支，非 main）
