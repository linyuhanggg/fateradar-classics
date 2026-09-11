# MING-424 古籍集成账本（415 tip 上合入 397 秘本 JSON 与 CP8/22/23 及本轮审查稿）

机器可读权威：`docs/integration/ming-424-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-415` @ `065af4177522e59152afdbd1c0fc8f54f80ce703`（独立验收 MING-419 `e788977f` 通过）
- 独占：`fateradar-multica-ming-424` / `codex/multica-ming-424`
- 合入方式：最小路径 `cherry-pick -x`；禁止整树覆盖；`verified` 保持 false
- **未升** 产品唯一线 / main / 部署

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 秘本 CP4 vern 修复 | MING-397/403 `6f9ae513` | `liuren-miben.json`（仅 L5920/22/24/26） | `cherry-pick -x` | `85b65a3` | integrated_pending_acceptance |
| 秘本 CP8 | MING-406 `8197f92` | `liuren-miben-cp8-review.md` | `cherry-pick -x` | `8b7c5ce` | integrated_pending_acceptance |
| 大六壬 CP22 | MING-412 `f40840fd` | `daliuren-daquan-cp22-review.md` | `cherry-pick -x` | `6973215` | integrated_pending_acceptance |
| 大六壬 CP23 | MING-413 `75b9e2ba` | `daliuren-daquan-cp23-review.md` | `cherry-pick -x` | `f50a95b` | integrated_pending_acceptance |
| 皇极 SK1573 CP3 | MING-416 `a66d5d96` | `huangji-jingshi-sk1573-cp3-review.md` | `cherry-pick -x` | `800e09e` | integrated_pending_acceptance |
| 飞星 CP1 | MING-417 `19fb31b` | `feixing-ziwei-doushu-yuanzhi-cp1-review.md` | `cherry-pick -x` | `62bef5a` | integrated_pending_acceptance |
| 飞星 CP2 | MING-418 `21d06e60` | `feixing-ziwei-doushu-yuanzhi-cp2-review.md` | `cherry-pick -x` | `fd4106a` | integrated_pending_acceptance |

## 验证
- `git diff 065af417..contentImportTip`：仅 `liuren-miben.json` + 上述 6 个审查 md（账本另计）
- 识典 SDZJ0170 SHA256 仍 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261`
- 大六壬 SHA256 仍 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`
- 秘本 SHA256：`30b9b2b9…` → `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347`（与 403 对象一致）
- 秘本相对 415 仅 4 条 paragraphId 变更：`L5920` / `L5922` / `L5924` / `L5926`（vernacular/notes）；其余 2639 条全等
- 飞星原旨 / 皇极 SK1573 注解 JSON blob 与 415 **全等**
- 各审查稿 blob 与源 tip **全等**；秘本 JSON blob 与 `6f9ae513` **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批触及注解 `verified=true`：**0**；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是大六壬/秘本/皇极/飞星全书人工 verified。
- source-reviewed ≠ 人工 verified。

## 交付 tip
- 内容合入 tip（JSON + 6 审查稿）：`fd4106ac33e19d32c93d34b9eb4a018f86c0b09f`
- 账本核对基线 tip（首次 push）：`b3850048a9b0261ddf8b01521a0fe9215fdf16dd`
- 远端 tip：以交包评论中 `git rev-parse origin/codex/multica-ming-424` / `git ls-remote` 为准（施工分支，非 main）
