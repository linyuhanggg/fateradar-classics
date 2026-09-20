#!/usr/bin/env python3
"""tools/map-nayin-ganzhi.py 的回归测试。

核心断言是**一条机器可验的自证**：把 60 条纳音象辞各自映到的干支排起来，
必须**恰好等于六十甲子的规范序列（顺序、无重复、无缺漏）**。
任何一条映错，序列里就会出现重复或缺号——所以这条断言比逐条人眼核对更强。

同时钉住：
  · 只能改 `applicable_to`（其余字段与 HEAD 逐字相同）；
  · 生成的谓词形态必须是 v3 的 `{all_of: [gan, zhi], same: pillar}`；
  · 反查判据不许退化成「取引文开头那个干支」——那会把「庚午」条锚成「己巳」。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/map-nayin-ganzhi.py"
BOOK = "luming-nayin/li-xuzhong-mingshu"
YAML_PATH = ROOT / "references/books" / BOOK / "rules.yaml"

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
# 六十甲子规范序列
CANON = [GAN[i % 10] + ZHI[i % 12] for i in range(60)]

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    print("1. 台账已记录 60 条反查结果")
    p = subprocess.run(
        [sys.executable, str(TOOL), "--dry-run"], cwd=ROOT, capture_output=True, text=True
    )
    check("  dry-run exit（已映射后应为 0 条可映射）", p.returncode, 0)
    ledger = json.loads((ROOT / "tools/reports/nayin-ganzhi-map.json").read_text(encoding="utf-8"))
    seq = [x["gan"] + x["zhi"] for x in ledger]
    check("  台账条数 60", len(seq), 60)
    check("  台账条目各带象辞依据", all(x.get("xiang") for x in ledger), True)

    print("2. 自证：必须是六十甲子规范序列（顺序／无重复／无缺漏）")
    check("  与规范序列逐位相同", seq, CANON)
    check("  无重复", len(set(seq)), 60)

    print("3. 落盘形态：v3 组 + same: pillar")
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    mapped = {}
    for r in data["rules"]:
        ap = r.get("applicable_to")
        if isinstance(ap, dict) and "all_of" in ap:
            leaves = ap["all_of"]
            if len(leaves) == 2 and {x["key"] for x in leaves} == {"gan", "zhi"}:
                mapped[r["rule_id"]] = (
                    next(x["value"] for x in leaves if x["key"] == "gan")
                    + next(x["value"] for x in leaves if x["key"] == "zhi"),
                    ap.get("same"),
                )
    check("  带该形态的规则数 60", len(mapped), 60)
    check("  全部 same=pillar", {v[1] for v in mapped.values()}, {"pillar"})
    check("  落盘干支集 = 规范序列", sorted(v[0] for v in mapped.values()), sorted(CANON))

    print("4. 只改 applicable_to（对照 HEAD 逐字段）")
    head = subprocess.run(
        ["git", "show", f"HEAD:{YAML_PATH.relative_to(ROOT)}"], cwd=ROOT, capture_output=True, text=True
    ).stdout
    if not head:
        print("  (跳过：HEAD 无此文件)")
    else:
        old = yaml.safe_load(head)
        om = {r["rule_id"]: r for r in old["rules"]}
        nm = {r["rule_id"]: r for r in data["rules"]}
        check("  book block 相同", old.get("book"), data.get("book"))
        check("  rule set 相同", set(om), set(nm))
        viol = [
            f"{rid}.{k}"
            for rid in om
            for k in set(om[rid]) | set(nm[rid])
            if k != "applicable_to" and om[rid].get(k) != nm[rid].get(k)
        ]
        check("  非 applicable_to 字段变动", viol, [])

    print("5. 判据不许退化成「引文开头那个干支」")
    # 反例：LIXUZHONGMIN-007 的 statement 是庚午象辞，但引文以己巳开头。
    # 按引文开头解析会得到己巳；正确反查必须得到庚午。
    rec = json.loads((ROOT / "tools/reports/nayin-ganzhi-map.json").read_text(encoding="utf-8"))
    by_id = {x["rule_id"]: x["gan"] + x["zhi"] for x in rec}
    check("  007 反查为庚午（不是引文开头的己巳）", by_id.get("LIXUZHONGMIN-007"), "庚午")
    check("  006 反查为己巳（其象辞「气胜体刚之木」属己巳条）", by_id.get("LIXUZHONGMIN-006"), "己巳")

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL NAYIN-GANZHI MAP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())