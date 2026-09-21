#!/usr/bin/env python3
"""`tools/reports/expressible-residue.json` 的一致性检查。

该台账记的是「`predicate-gap-report.py` 的 classify() 机械判为『本可表达』，
但经逐条复核仍**不**映射」的 30 条。它必须与两处保持一致：

  1. **仍未被映射**：台账里的规则 `applicable_to` 必须还是空。一旦有人映射了它，
     台账条目就过期了——本测试会红，提示把该条从台账移除（不是改台账去迁就）。
  2. **仍是机械命中**：它们应当仍出现在 classify() 的 single-pair /
     multi-pair-same-key / multi-key 三类里。若不再出现，说明判据或数据变了。

另检查台账自洽：理由类别都在表里、无重复 rule_id、条数与两处对得上。
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "tools/reports/expressible-residue.json"
MECHANICAL = ("single-pair", "multi-pair-same-key", "multi-key")

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = data["entries"]
    classes = data["reason_classes"]

    print("1. 台账自洽")
    check("  条数 29（t197 新增一条「取值无样盘覆盖」）", len(entries), 29)
    ids = [(e["art"], e["rule_id"]) for e in entries]
    check("  无重复", len(ids), len(set(ids)))
    check("  理由类别都在表里", [e["reason_class"] for e in entries if e["reason_class"] not in classes], [])
    check("  每类都有中文理由", all(classes.values()), True)

    print("2. 仍未被映射（台账不得过期）")
    idx = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        k = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                idx[(k, r["rule_id"])] = r
    mapped = []
    missing = []
    for e in entries:
        hit = [r for (k, rid), r in idx.items() if rid == e["rule_id"]]
        if not hit:
            missing.append(e["rule_id"])
            continue
        if hit[0].get("applicable_to"):
            mapped.append(e["rule_id"])
    check("  台账里的规则都存在", missing, [])
    check("  全部仍未被映射（被映射即应从台账移除）", mapped, [])

    print("3. 仍是机械命中（判据/数据未漂移）")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/predicate-gap-report.py"), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    rows = json.loads(proc.stdout)["rows"]
    mech = {r["rule_id"]: r["kind"] for r in rows if r["kind"] in MECHANICAL}
    check("  机械命中条数 == 台账条数", len(mech), len(entries))
    check(
        "  台账与机械命中的 rule_id 集合一致",
        sorted(mech),
        sorted(e["rule_id"] for e in entries),
    )
    check(
        "  triage_kind 与实测一致",
        sorted(
            e["rule_id"] for e in entries if mech.get(e["rule_id"]) != e["triage_kind"]
        ),
        [],
    )

    print("4. 理由分布与三类占比（供文档引用）")
    dist = Counter(e["reason_class"] for e in entries)
    print("     " + " ".join(f"{k}={v}" for k, v in dist.most_common()))
    kinds = Counter(e["triage_kind"] for e in entries)
    check("  三类合计 29", sum(kinds.values()), 29)
    print("     " + " ".join(f"{k}={v}" for k, v in kinds.most_common()))

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL EXPRESSIBLE-RESIDUE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())