#!/usr/bin/env python3
"""谓词语言表达力审计的回归测试（t207）。

审计本身是判断，但其中**能被机器检查的那部分**要钉住：

1. 台账结构完整（每类都有 id／name／status／evidence／demand）；
2. **计数类候选仍然未被映射** —— 若哪天有人把它们映射了（说明计数语义做出来了），
   这条断言会红，提醒把审计结论一起改掉；
3. 台账里「已消化」的三类，其证据指向的工具/台账文件仍在；
4. 台账里的候选 id 在真实语料里存在（不是抄错的 id）。

不检查关键词扫描的计数——t207 已证明那种扫法会把需求夸大（见台账 method 字段）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "tools/reports/expressiveness-audit.json"
FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def _rules_by_id() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in (ROOT / "references/books").glob("*/*/rules.yaml"):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for r in data.get("rules") or []:
            if isinstance(r, dict) and r.get("rule_id"):
                out.setdefault(r["rule_id"], r)
    return out


def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    classes = data["classes"]

    print("1. 台账结构完整")
    check("  类别数 ≥ 8", len(classes) >= 8, True)
    check(
        "  每类都有 id/name/status/evidence/demand",
        [c.get("id") for c in classes if not all(c.get(k) for k in ("id", "name", "status", "evidence", "demand"))],
        [],
    )
    check("  结论非空", bool(data.get("conclusion")), True)

    print("2. 计数类候选仍然未被映射（若已映射，说明计数语义做出来了）")
    counting = next(c for c in classes if c["id"] == "counting")
    check("  候选非空", len(counting["candidates"]) > 0, True)
    rules = _rules_by_id()
    for cand in counting["candidates"]:
        rid = cand["rule_id"]
        check(f"  {rid} 存在于语料", rid in rules, True)
        check(f"  {rid} 仍未映射", not (rules.get(rid) or {}).get("applicable_to"), True)

    print("3. 「已消化」三类的证据工具/台账仍在")
    for tool in (
        "tools/map-qimen-lin-pairs.py",
        "tools/map-liuyao-caiguan.py",
        "tools/map-bazi-tougan.py",
        "tools/map-liuyao-kong.py",
        "tools/reports/liuren-selection-map.json",
        "tools/reports/tautological-mappings.json",
    ):
        check(f"  {tool} 存在", (ROOT / tool).exists(), True)

    print("4. status 取值在已知集合内")
    known = {
        "supported",
        "solved-by-enumeration",
        "solved-by-none-of",
        "supported-with-risk",
        "MISSING",
        "little-applicability-demand",
        "expressible-but-explosive",
        "engine-side",
    }
    check("  未知 status", sorted({c["status"] for c in classes} - known), [])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL EXPRESSIVENESS-AUDIT OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())