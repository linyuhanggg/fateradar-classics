#!/usr/bin/env python3
"""六爻「财官」类：把「用神为财/官」「财官持世」写成谓词（t194）。

原文（火珠林）三条都以「**财官**」作主语：

    HZL-R002  财官旺相、有辅体发动或生世为可用；休囚、克破、无辅则力薄。
    HZL-R004  财官持世虽可许，但应爻或动爻克所用辅爻则事难成。
    HZL-R005  财官出现旺相宜久远；伏藏有气虽可取，多利短时或暂成。

「财官」＝妻财／官鬼（求财、求官两路的用神）。三条各自的**分支**（旺相／休囚、出现／伏藏、
持世与否）是**断法**，不是适用范围；三条共同的适用范围就是「**本卦所取用神为财或官**」。

- R002／R005 直写平铺或：`[{liuyao_yongshen: 妻财}, {liuyao_yongshen: 官鬼}]`
  （与 t176 的单谓词平铺列表同形；用神值域 7 取 2，不恒真。）
- R004 的「财官**持世**」需要**配对**：某爻的六亲为财/官、且该爻就是世爻。
  写成枚举（6 爻 × 2 六亲）＝ 12 支，每支两句**都带取值**：

      any_of ─┬─ all_of [ {liuqin: 妻财, scope: {yao: N}},
        │                 {shiyao: <第N爻的名>, scope: {yao: N}} ]
        └─ … 6 爻 × {妻财,官鬼} …

  `shiyao` 的取值由爻位唯一确定（第 N 爻即「初爻…六爻」），所以**不需要无取值子句**——
  这是有意选的路：无取值子句算不算通配，口径尚未裁定（t179 待授权项 ①）。

判据必须命中 statement 才落盘。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAO_LABELS = ["初爻", "二爻", "三爻", "四爻", "五爻", "六爻"]


def flat_caiguan() -> str:
    """平铺或：用神为妻财或官鬼。"""
    return "[{key: liuyao_yongshen, value: 妻财}, {key: liuyao_yongshen, value: 官鬼}]"


def caiguan_chishi() -> str:
    """财官持世：枚举 6 爻 × 2 六亲，每支两句都带取值。"""
    branches = []
    for label in YAO_LABELS:
        for n, rel in ((YAO_LABELS.index(label) + 1, "妻财"), (YAO_LABELS.index(label) + 1, "官鬼")):
            branches.append(
                "{all_of: ["
                f"{{key: liuqin, value: {rel}, scope: {{yao: {n}}}}}, "
                f"{{key: shiyao, value: {label}, scope: {{yao: {n}}}}}"
                "]}"
            )
    return "{any_of: [" + ", ".join(branches) + "]}"


# rule_id → (谓词, statement 复核片段, 备注)
MAP: dict[str, tuple[str, str, str]] = {
    "HZL-R002": (
        flat_caiguan(),
        "财官旺相",
        "「旺相／休囚、有辅／无辅」是该条的**两支断法**，不是适用范围；适用范围为用神属财或官。",
    ),
    "HZL-R005": (
        flat_caiguan(),
        "财官出现旺相",
        "「出现宜久远／伏藏多短时」同上属断法；与 R002 同适用范围（原文同以「财官」起句）。",
    ),
    "HZL-R004": (
        caiguan_chishi(),
        "财官持世",
        "「虽可许，但应爻或动爻克所用辅爻则事难成」属断法；适用范围为财／官持世。",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="六爻财官类 → 谓词")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets: dict[Path, str] = {}
    found: dict[str, tuple[Path, dict]] = {}
    for p in sorted((ROOT / "references/books/divination").glob("*/rules.yaml")):
        text = p.read_text(encoding="utf-8")
        targets[p] = text
        for r in yaml.safe_load(text).get("rules") or []:
            if isinstance(r, dict) and r.get("rule_id") in MAP:
                found[r["rule_id"]] = (p, r)

    problems: list[str] = []
    done: set[str] = set()
    for rid, (pred, needle, _n) in MAP.items():
        if rid not in found:
            problems.append(f"{rid} 不存在")
            continue
        _p, r = found[rid]
        if needle not in (r.get("statement") or ""):
            problems.append(f"{rid} statement 不含复核片段「{needle}」")
        cur = r.get("applicable_to")
        if cur:
            if cur == yaml.safe_load(pred):
                done.add(rid)
            else:
                problems.append(f"{rid} 已有不同谓词，本批不应改写")
    if problems:
        for x in problems:
            print("FAIL:", x, file=sys.stderr)
        return 1
    print(f"复核通过：{len(MAP)} 条（已落实 {len(done)}，本次待写 {len(MAP) - len(done)}）")

    if args.dry_run:
        for rid, (pred, _n, _note) in MAP.items():
            print(f"  {rid}: {pred[:100]}…")
        return 0

    for rid, (pred, _needle, _note) in MAP.items():
        if rid in done:
            continue
        path, _r = found[rid]
        text = targets[path]
        pattern = re.compile(rf"(?m)^(- rule_id: {re.escape(rid)}\n(?:.*\n)*?  applicable_to: )\[\]$")
        text, n = pattern.subn(lambda mo: mo.group(1) + pred, text, count=1)
        if n != 1:
            raise SystemExit(f"改写失败: {rid}")
        targets[path] = text
    for path, text in targets.items():
        path.write_text(text, encoding="utf-8")
    print(f"已写入 {len({p for p, _ in found.values()})} 个 rules.yaml")

    ledger = [
        {
            "book": found[rid][0].relative_to(ROOT / "references/books").as_posix().replace("/rules.yaml", ""),
            "rule_id": rid,
            "applicable_to_yaml": pred,
            "evidence_from_statement": needle,
            "note": note,
        }
        for rid, (pred, needle, note) in MAP.items()
    ]
    out = ROOT / "tools/reports/liuyao-caiguan-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())