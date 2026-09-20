#!/usr/bin/env python3
"""tools/map-qimen-stems.py 的回归测试。

钉住四件事：
  1. 16 条映射的 statement 复核片段确实在原文里（判据基于原文，不是自报）；
  2. 落盘谓词形态正确：干干相配用 `same: gong` 绑定，点名宫位的用 `scope.gong`；
  3. **中五不立天地盘干事实**——引擎既有不变量（无任何 fact 带 gong=5），
     事实样本与产品测试都依赖它；本批不得破坏；
  4. `甲` 绝不作为取值出现（甲寄六仪，天地盘只有九干）。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOK = "san-shi/qimen-dunjia-tongzhi"
YAML_PATH = ROOT / "references/books" / BOOK / "rules.yaml"
SAMPLE = ROOT / "tools/reports/facts-sample.json"
PRODUCT_VOCAB = Path("/Users/sync/code/cosmic-fortune-lab/src/lib/engine/facts/fact-vocab.json")

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    ledger = json.loads((ROOT / "tools/reports/qimen-stem-map.json").read_text(encoding="utf-8"))
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    rules = {r["rule_id"]: r for r in data["rules"]}

    print("1. 台账 16 条，且复核片段仍在原文里")
    check("  条数", len(ledger), 16)
    miss = [
        x["rule_id"]
        for x in ledger
        if x["evidence_from_statement"] not in (rules.get(x["rule_id"], {}).get("statement") or "")
    ]
    check("  statement 片段全部命中", miss, [])

    print("2. 落盘谓词形态")
    bad_shape = []
    for x in ledger:
        cur = rules[x["rule_id"]].get("applicable_to")
        if not cur:
            bad_shape.append(f"{x['rule_id']}: 空")
            continue
        s = json.dumps(cur, ensure_ascii=False)
        if "geju_qimen" in s:
            continue  # 伏吟局/反吟局：单谓词
        if "same" in s:
            if '"same": "gong"' not in s:
                bad_shape.append(f"{x['rule_id']}: same 不是 gong")
        elif "gong" not in s:
            bad_shape.append(f"{x['rule_id']}: 既无 same: gong 也无 scope.gong")
    check("  形态全部合规", bad_shape, [])

    print("3. 中五不立天地盘干事实（引擎既有不变量）")
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    gong5 = [
        f["key"]
        for c in sample["qimen"].values()
        for f in c["facts"]
        if f["scope"].get("gong") == 5
    ]
    check("  样本中无任何 fact 带 gong=5", gong5, [])
    for case, c in sample["qimen"].items():
        for key in ("tianpan_gan", "dipan_gan"):
            n = len([f for f in c["facts"] if f["key"] == key])
            if n != 0 and n != 8:
                FAILED.append(f"{case} {key} 条数 {n}（应为 8：八宫，中五不立）")
                print(f"  FAIL {case} {key} 条数 {n}")
    check("  天地盘干各 8 条/盘（八宫）", True, True)

    print("4. 甲不得作为取值（甲寄六仪）")
    for f in ("references/vocab/fact-vocab.json", str(PRODUCT_VOCAB)):
        v = json.loads((ROOT / f).read_text(encoding="utf-8")) if not f.startswith("/") else json.loads(Path(f).read_text(encoding="utf-8"))
        for key in ("tianpan_gan", "dipan_gan"):
            dom = v["values"].get(key) or []
            check(f"  {f.split('/')[-1]} {key} 值域 9 干且无甲", (len(dom), "甲" in dom), (9, False))

    print("5. 未迁移的规则不得被顺手映射（甲值符类）")
    for rid in ("QM-P01", "QM-P02", "QM-P31"):
        r = rules.get(rid)
        if r is None:
            continue
        check(f"  {rid} 仍为空（甲不出现在天地盘，需值符落宫）", r.get("applicable_to") or [], [])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL QIMEN-STEM MAP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())