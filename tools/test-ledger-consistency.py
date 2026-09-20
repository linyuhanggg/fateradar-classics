#!/usr/bin/env python3
"""判定台账 ↔ 规则实况的一致性闸门。

台账（`tools/reports/predicate-decisions/*.json`）是「每条未映射规则为什么没映射」的
**唯一账本**，也是 t179 那张决策表的数字来源。但它此前没有任何东西检查它是否与规则实况相符，
于是出现过一个真实的脱节：

  5 条在 t168 复核中被**撤回**的映射（`captain-audit.json` 的 `reverted`），
  其台账条目仍写着 `decision: "mapped"`，而规则里的 `applicable_to` 早已是空。
  ——台账声称映射了，规则说没有。**这正是本测试存在的理由。**

检查项（每条都对应一种「台账说谎」的方式）：

1. `decision: mapped`   ⇒ 规则 `applicable_to` 必须**非空**（否则台账过期）
2. `decision: unmapped` ⇒ 规则 `applicable_to` 必须**为空**
3. `decision: reverted` ⇒ 规则 `applicable_to` 必须**为空**，且须给出 `reason_class`
4. `captain-audit.json` 的 `reverted` 条目 ⇒ 台账里必须存在，且不得仍写 `mapped`
5. 每条**跟踪口径下未映射**的规则 ⇒ 台账里必须有条目（不许漏账）
"""

from __future__ import annotations

import glob
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "tools/reports/predicate-decisions"
KNOWN_DECISIONS = ("mapped", "unmapped", "reverted")

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def live_map() -> dict[str, object]:
    """规则 ID → applicable_to（当前树）。"""
    out: dict[str, object] = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                out.setdefault(r["rule_id"], r.get("applicable_to"))
    return out


def main() -> int:
    live = live_map()
    entries: dict[str, list[tuple[str, dict]]] = {}
    for f in sorted(glob.glob(str(DECISIONS / "*.json"))):
        name = Path(f).name
        if name == "captain-audit.json":
            continue
        for x in json.loads(Path(f).read_text(encoding="utf-8")).get("decisions") or []:
            if isinstance(x, dict) and x.get("rule_id"):
                entries.setdefault(x["rule_id"], []).append((name, x))

    print("1. decision 取值合法，且与规则实况相符")
    bad_state: list[str] = []
    bad_value: list[str] = []
    for rid, items in entries.items():
        for name, x in items:
            dec = x.get("decision")
            if dec not in KNOWN_DECISIONS:
                bad_value.append(f"{rid}（{name}）decision={dec!r}")
                continue
            if rid not in live:
                continue
            empty = not live[rid]
            if dec == "mapped" and empty:
                bad_state.append(f"{rid}（{name}）台账写 mapped，规则却是空")
            if dec in ("unmapped", "reverted") and not empty:
                bad_state.append(f"{rid}（{name}）台账写 {dec}，规则却有谓词")
    check("  decision 取值只有 mapped/unmapped/reverted", bad_value, [])
    check("  没有「台账说映射了、规则却是空」这类脱节", bad_state, [])

    print("2. reverted 条目必须给理由类别")
    missing_reason = [
        rid for rid, items in entries.items()
        for _n, x in items if x.get("decision") == "reverted" and not x.get("reason_class")
    ]
    check("  reverted 均有 reason_class", sorted(set(missing_reason)), [])

    print("3. captain-audit 的撤回项必须在台账里、且不仍写 mapped")
    audit = json.loads((DECISIONS / "captain-audit.json").read_text(encoding="utf-8"))
    reverted = [x["rule_id"] for x in audit.get("reverted") or []]
    check("  captain-audit 有撤回项", len(reverted) > 0, True)
    not_in_ledger = [r for r in reverted if r not in entries]
    still_mapped = [
        r for r in reverted
        if any(x.get("decision") == "mapped" for _n, x in entries.get(r, []))
    ]
    check("  撤回项都在台账里", not_in_ledger, [])
    check("  撤回项不仍写 mapped", still_mapped, [])
    check("  撤回项规则实况为空", [r for r in reverted if live.get(r)], [])

    print("4. 跟踪口径下每条未映射规则都要有账")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/predicate-gap-report.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True,
    )
    rows = json.loads(proc.stdout)["rows"]
    unaccounted = [r["rule_id"] for r in rows if r["rule_id"] not in entries]
    check(f"  未映射 {len(rows)} 条全部有台账条目", unaccounted, [])
    no_reason = [
        r["rule_id"] for r in rows
        if not any(x.get("reason_class") for _n, x in entries.get(r["rule_id"], []))
    ]
    check("  未映射条目都有 reason_class", no_reason, [])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL LEDGER-CONSISTENCY OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())