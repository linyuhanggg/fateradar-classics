# 独立复核 t24 annotations（2026-09-13）

- 工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`
- 只读重算，未改文件，未 commit/push，未碰 `/Users/sync/code/**`
- **结论：PASS**

## 1. 8 条状态

`references/annotations/san-shi/daliuren-daquan.json` 各 1 条唯一：全部 `review=source-reviewed` 且 `verified=false`。全库 annotations 79 文件、62,839 条中 `verified=true` 计数 = 0。

## 2. 引号内字符串 vs 源行（含空格）

| paragraphId | quote==src | repr |
|---|---|---|
| L9463-L9463 | True | `'勾        常'`（勾 + 8×U+0020 + 常） |
| L9469-L9469 | True | `'空'` |
| L9479-L9479 | True | `'贵'` |
| L9495-L9495 | True | `'玄'` |
| L9503-L9503 | True | `'寅    未 贵'`（寅 + 4×U+0020 + 未 + 空格 + 贵） |
| L9505-L9505 | True | `'空丑    申'`（空丑 + 4×U+0020 + 申） |
| L9521-L9521 | True | `'后'` |
| L9529-L9529 | True | `'申    丑 贵'`（申 + 4×U+0020 + 丑 + 空格 + 贵） |

notes 中「吉凶」均在否定句「不支持…吉凶判断」。t2 旧注仍写「保留 draft」，当前 `review` 已是 source-reviewed；不构成 FAIL。

## 3. 抽查 3 条 t24 未决 draft

均 `review=draft`、`verified=false`，notes 含「缺什么证据」与「解锁条件」：L9171 矿决、L9920 亥/寅初传、L6507 已亥。

## 4. 校验器

`python3 tools/validate-annotations.py` → 53 books, 62839 entries, 0 errors；exit 0。

FAIL findings：无。
