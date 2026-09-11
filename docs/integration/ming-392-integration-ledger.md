# MING-392 古籍集成账本（381 tip 上合入已审大六壬/秘本审查稿）

机器可读权威：`docs/integration/ming-392-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-381` @ `b21ae71538d46d64169508589ffb1a209e6466ff`（验收 MING-385 `9cd03c63` 已通过）
- 独占：`fateradar-multica-ming-392` / `codex/multica-ming-392`
- **只进 md 审查稿**，**未改** 任何 `references/annotations/**/*.json`
- **未等** MING-387 CP13
- **未升** 产品唯一线 `6c1dfa3b`

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 大六壬 CP7 | MING-372 `a05cef26` | `daliuren-daquan-cp7-review.md` | `cherry-pick -x` | `023a186` | integrated_pending_acceptance |
| 大六壬 CP8 | MING-374 `43c7d593` | `daliuren-daquan-cp8-review.md` | path-checkout（orphan tip） | `b670186` | integrated_pending_acceptance |
| 大六壬 CP9 | MING-377 `a457e9cc` | `daliuren-daquan-cp9-review.md` | `cherry-pick -x` | `221f14b` | integrated_pending_acceptance |
| 大六壬 CP10 | MING-378 `604ea3cb` | `daliuren-daquan-cp10-review.md` | `cherry-pick -x` | `bf7feaa` | integrated_pending_acceptance |
| 大六壬 CP11 | MING-383 `847fff8` | `daliuren-daquan-cp11-review.md` | `cherry-pick -x` | `bde57f7` | integrated_pending_acceptance |
| 大六壬 CP12 | MING-386 `d0a3b24` | `daliuren-daquan-cp12-review.md` | `cherry-pick -x` | `2ae7c62` | integrated_pending_acceptance |
| 秘本 CP1 | MING-379 `d5fc8bb` | `liuren-miben-cp1-review.md` | `cherry-pick -x` | `3991ca6` | integrated_pending_acceptance |
| 秘本 CP2 | MING-384 `56d1300` | `liuren-miben-cp2-review.md` | `cherry-pick -x` | `9159c94` | integrated_pending_acceptance |
| 秘本 CP3 | MING-388 `d1b8af99` | `liuren-miben-cp3-review.md` | `cherry-pick -x` | `ce36be7` | integrated_pending_acceptance |
| 381 验收稿 | MING-385 `9cd03c63` | `ming-381-acceptance-review.md` | `cherry-pick -x` | `518e155` | integrated_pending_acceptance |

合入方式：最小路径；禁止整树覆盖；CP8 为 orphan tip，仅 path-checkout 审查稿。

## 验证
- `git diff b21ae715..HEAD`：仅上述 10 个审查/验收 md + 本账本；**无** 注解 JSON 变更
- 识典 SDZJ0170 SHA256 仍 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261`（与 369 blob 全等）
- 大六壬 SHA256 仍 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`
- 秘本 SHA256 仍 `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`
- 各审查稿 blob 与源 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批触及注解文件 `verified=true`：**0**（本批未改注解）；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是大六壬/秘本全文交付；不是人工 verified。
- 未合入 MING-387 CP13。

## 交付 tip
- 内容合入 tip（10 审查/验收稿）：`b67018647300878ce5e1637cd4c14259e2a2a62b`
- 内容+账本首推 tip：`7a675fdf13a25c48f560aef4ea6d2648b2320abd`
- 账本记录 tip：`f0d76b40e9a57c624b4fb8412e5a4557d675d0e7`
- 远端 tip：`origin/codex/multica-ming-392` @ `e5bb79caebd4c2a830f36a544aad0507d18cf052`（交包时以 push 后 `git rev-parse origin/codex/multica-ming-392` 为准）
