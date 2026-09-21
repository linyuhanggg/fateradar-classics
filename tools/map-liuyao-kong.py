#!/usr/bin/env python3
"""六爻「用神旬空」→ 枚举配对谓词（t197）。

原文（增删卜易）：**用神旬空——空而不空（动 / 旺 / 临日月）则不空；真空——出旬即应；
旬空亦可冲实。**

其**适用范围**是「用神所在之爻旬空」。要表达它得把三样东西配起来：
用神的**名**（六亲之一）→ 该名出现在哪一爻 → 那一爻是否旬空。

    {any_of: [
      {all_of: [{key: liuyao_yongshen, value: 妻财},          # 用神是妻财
                {key: liuqin, value: 妻财, scope: {yao: N}},   # 第 N 爻的六亲是妻财
                {key: liuyao_kong, value: 空, scope: {yao: N}}]},  # 且第 N 爻旬空
      … 5 个六亲 × 6 爻 = 30 支 …
    ]}

**每支三句都带取值、都带 scope**，不需要无取值子句。

**如实披露**：用神也可能是「世爻／应爻」（非六亲），那几种不在本式内——属**子集**。
另外后文「空而不空／真空／冲实」是**断法**，不是适用范围。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RELATIVES = ["父母", "兄弟", "子孙", "妻财", "官鬼"]
YAO_INDEXES = [1, 2, 3, 4, 5, 6]


def encode(relatives: list[str] = RELATIVES, yaos: list[int] = YAO_INDEXES) -> str:
    branches = []
    for rel in relatives:
        for n in yaos:
            branches.append(
                "{all_of: ["
                f"{{key: liuyao_yongshen, value: {rel}}}, "
                f"{{key: liuqin, value: {rel}, scope: {{yao: {n}}}}}, "
                f"{{key: liuyao_kong, value: 空, scope: {{yao: {n}}}}}"
                "]}"
            )
    return "{any_of: [" + ", ".join(branches) + "]}"


MAP: dict[str, tuple[str, str, str]] = {
    "ZENGSHANBUYI-ZR-08": (
        encode(),
        "用神旬空",
        "适用范围＝「用神所在之爻旬空」；用神为世爻/应爻（非六亲）的情形不在本式内（子集）。"
        "「空而不空（动/旺/临日月）则不空；真空出旬即应；旬空亦可冲实」是断法，未表达。",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="六爻用神旬空 → 枚举配对谓词")
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
            print(f"  {rid}: {pred[:110]}…")
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
            "encoding": "enumerated-pairing-over-five-relatives-x-six-yao",
            "facts": ["liuyao_yongshen", "liuqin(scope.yao)", "liuyao_kong(scope.yao)"],
            "disclosed": "用神为世爻/应爻（非六亲）的情形不在本式内（子集）。",
            "note": note,
        }
        for rid, (pred, needle, note) in MAP.items()
    ]
    out = ROOT / "tools/reports/liuyao-kong-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())