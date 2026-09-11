# MING-415 古籍集成账本（407 tip 上合入已审大六壬 CP17–CP21 与秘本 CP7/CP9 审查稿）

机器可读权威：`docs/integration/ming-415-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-407` @ `e371f3a83b1d160915817cc1b0e757675419dfc4`（验收 MING-411 `b935d17` 已通过）
- 独占：`fateradar-multica-ming-415` / `codex/multica-ming-415`
- **只进 md 审查稿**，**未改** 任何 `references/annotations/**/*.json`
- **未等** CP8 / CP22 / CP23
- **未合入** MING-397 秘本 JSON；**未抢** MING-406 CP8
- **未升** 产品唯一线 `6c1dfa3b`

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 大六壬 CP17 | MING-398 `307f4ed0` | `daliuren-daquan-cp17-review.md` | `cherry-pick -x` | `5562e90` | integrated_pending_acceptance |
| 大六壬 CP18 | MING-402 `aafe566a` | `daliuren-daquan-cp18-review.md` | `cherry-pick -x` | `ac5f38c` | integrated_pending_acceptance |
| 大六壬 CP19 | MING-404 `d6d7aa25` | `daliuren-daquan-cp19-review.md` | `cherry-pick -x` | `4829e89` | integrated_pending_acceptance |
| 大六壬 CP20 | MING-405 `7c99eabd` | `daliuren-daquan-cp20-review.md` | `cherry-pick -x` | `2c1598b` | integrated_pending_acceptance |
| 大六壬 CP21 | MING-410 `b82e6074` | `daliuren-daquan-cp21-review.md` | `cherry-pick -x` | `0753f04` | integrated_pending_acceptance |
| 秘本 CP7 | MING-401 `9df671c0` | `liuren-miben-cp7-review.md` | `cherry-pick -x` | `1bae97d` | integrated_pending_acceptance |
| 秘本 CP9 | MING-408 `c7eb6be4` | `liuren-miben-cp9-review.md` | `cherry-pick -x` | `ea1572a` | integrated_pending_acceptance |

合入方式：最小路径 cherry-pick；禁止整树覆盖。

## 验证
- `git diff e371f3a..contentImportTip`：仅上述 7 个审查 md；**无** 注解 JSON 变更（账本另计）
- 识典 SDZJ0170 SHA256 仍 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261`
- 大六壬 SHA256 仍 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`
- 秘本 SHA256 仍 `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（397 未合入）
- 各审查稿 blob 与源 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批触及注解文件 `verified=true`：**0**（本批未改注解）；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是大六壬全文交付；不是人工 verified。
- 未合入 MING-406 CP8；未合入 MING-397 秘本 JSON；未等 CP22/CP23。

## 交付 tip
- 内容合入 tip（7 审查稿）：`ea1572ada7f9a11d78d36bfc904a6efddaedb8d6`
- 内容+账本 tip：以交包评论中 `git rev-parse origin/codex/multica-ming-415` 为准（施工分支，非 main）
