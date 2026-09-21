#!/usr/bin/env python3
"""八字「月令藏干透干」类 → 枚举配对谓词（t195）。

原文两条（三命通会／渊海子平）同说一件事：

    月令所藏天干分本气、中气、余气，按节气分日数分配司令；
    **取格优先看本气透干，本气不透看中气、余气**。

「透干」＝某个藏干**也出现在天干上**（藏与透同值）。要的是「跨键取值相等」，
与前几轮同一件东西；这里用**枚举十天干**＋不写 `same` 的配对写出来：

    {any_of: [
      {all_of: [{key: canggan, value: 甲, scope: {pillar: month}},   # 月令藏甲
                {key: gan, value: 甲}]},                              # 任一天干为甲
      … 十支 … ]}

第二句不带 scope → 任一天干皆可；两句取值相同即「透」。**全域无通配。**

适用范围取「**月令藏干有透干者**」——即该条所处理的那种局面（本气透或中气余气透）。
「本气不透且完全无透干」时本式不成立，属**子集**，已在台账披露。

前提：`canggan`（藏干，逐柱，**本气在前**）由 t195 起产出——
`calendar.ts` 的 `PillarFact.hidden` 本就注明该顺序，`emitBaziFacts` 也早在读它算十神，
只是没把藏干本身当事实产出。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]


def encode() -> str:
    branches = [
        "{all_of: ["
        f"{{key: canggan, value: {s}, scope: {{pillar: month}}}}, "
        f"{{key: gan, value: {s}}}"
        "]}"
        for s in STEMS
    ]
    return "{any_of: [" + ", ".join(branches) + "]}"


MAP: dict[str, tuple[str, str, str]] = {
    "SANMINGTONGH-R-02": (
        encode(),
        "取格优先看本气透干",
        "适用范围＝月令藏干有透干者（本气透或中气余气透）；"
        "「按节气分日数分配司令」属取格细则，未表达；完全无透干的情形不在本式内（子集）。",
    ),
    "YUANHAIZIPIN-008": (
        encode(),
        "取格优先看本气透干",
        "与 SANMINGTONGH-R-02 同文同式（两书同说取格先看透干）。",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="八字透干类 → 枚举配对谓词")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets: dict[Path, str] = {}
    found: dict[str, tuple[Path, dict]] = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
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
            "encoding": "enumerated-value-pairing-over-ten-stems",
            "fact_contract": "canggan(scope.pillar) 与 gan 取值相同即「透」；全式无通配、无 same。",
            "disclosed": "适用范围为「月令藏干有透干者」；完全无透干的情形不在本式内（子集）。",
            "note": note,
        }
        for rid, (pred, needle, note) in MAP.items()
    ]
    out = ROOT / "tools/reports/bazi-tougan-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())