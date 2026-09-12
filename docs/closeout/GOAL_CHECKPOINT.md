# FateRadar 全库古籍目标检查点

更新：2026-09-12（DSH 接续会话 `session-79674fcd-44e5-4073-bb53-a719afce6cc9`）

## 当前提交

- `dsh/full-library-classics` **`27892fc`**（已推送）
- `origin/main` **`4cb96e3`**（未合）
- 产品对应 `dsh/full-library-product` **`d33a9e1`**（已推送）
- 工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`

## 全库真实计数（由脚本实测，不引用旧文档）

- 注解文件 79 个；注解条目 **62,839**（未增删）
- `source-reviewed` **60,008** / `draft` **2,831**（本轮 2905 → 2831）
- executable 规则定义 **258** 条 / 15 文件（本轮新增 6 条小六壬）
- `verified` 仍全部 false；本轮没有任何条目被设为 verified

## 本轮关闭的缺口

1. **小六壬 executable 定义为 0** → 已接 6 条（`be4896d`）。
   来源《玉匣记》雜占篇「李淳風六壬時課」L4213-L4245。带 5 个已知疑字
   （卒未妝時／求謀日示明／凡謀事立三六九／赤日主口舌／更須訪咒詛），照录不改，
   在 `references/executable/SOURCE_REVIEW.md` 第十三包一节逐条登记。
2. **draft 2905 → 2831**，两批：
   - `5c35601`：多版本互校 6 文件，**35 条** draft→source-reviewed（217 条逐条互校后）。
   - `27892fc`：大六壬大全，**39 条**（812 条中）。
   两条都由 captain 独立复算 diff 后提交（见验证一节），member 自述不作为依据。
3. **`GAP_LEDGER.json` 的 `drafts_by_file` 与 counts 按真实对象重写**（`be4896d`）。
   原值 daliuren 845 / yuqia 267 / xingli-kaoyuan 185 与文件实际 812 / 180 / 1 不符。
   `rules[].level` 仍是旧快照，以产品侧由代码生成的缺口矩阵为准。

## 独立验证（captain 复算，不用 member 报告）

- `verify_t3.py`：条目集不变（7021）、draft→source-reviewed 恰好 35、notes-only 182、
  其他字段改动 0、`verified==true` 0。
- `verify_t2.py`：条目集不变（6893）、升 39、notes-only 773、其他字段改动仅
  `vernacular` 39（即被升条目）+ `terms` 9、**引文原文零改动**、`verified==true` 0。
- `python3 tools/validate-annotations.py` → 53 books / 62839 entries / 0 errors。
- `python3 tools/validate-executable.py --json` → ok，15 文件 / 258 规则 / 525 来源跨度 / 0 errors。
- `git status` 全程确认写入只发生在 `/Users/yuhanglin/fateradar-goal-20260912/classics`。

## 仍未完成

| 项 | 数量 | 为什么不能标完成 |
|---|---|---|
| draft 合计 | **2831** | 奇门 nlc-layouts 1261（ocr-draft，校验器禁止仅凭 review 升级）、大六壬 773、玉匣记 180、约言 162 等 |
| 大六壬总钤残格 | **666** | 电子本把表头抽进单元格流，列归属不可复原；仓内无《大六壬大全》影印 → 需外部影印页 |
| 非总钤 draft | 107 | 已逐条写缺什么/已查来源/下一步 |
| 影印校勘 | 未做 | 全库 `source-reviewed` 只表示对照电子文本，不等于逐段影印精校 |
| 合 main | 未合 | 见产品检查点：CI 门槛本轮才刚转绿 |

## 恢复命令

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
export PATH="$HOME/.bun/bin:$HOME/.local/bin:$PATH"
python3 tools/validate-annotations.py
python3 tools/validate-executable.py --json
```
