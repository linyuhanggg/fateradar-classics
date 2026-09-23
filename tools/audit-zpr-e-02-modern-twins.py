#!/usr/bin/env python3
"""Read-only Product replay of two modern dates with source-example pillars.

This verifies calendrical reproducibility and Product's current caige route.
It does not verify the historical birthday, Classics' relation semantics, or
ZPR-E-02's overall verdict.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"

REPLAY = r"""
import { buildBazi } from "./src/lib/engine/bazi";
const cases = [
  { id: "food", year: "1962", month: "2", day: "11", hour: "10", minute: "0" },
  { id: "officer", year: "1992", month: "12", day: "8", hour: "6", minute: "0" },
];
const output = cases.map((spec) => {
  const chart = buildBazi({
    name: "ZPR-E-02 modern same-pillars audit",
    gender: "男",
    year: spec.year, month: spec.month, day: spec.day,
    hour: spec.hour, minute: spec.minute,
    province: "上海", city: "上海", district: "黄浦区",
    timeBasis: "clock", dayBoundary: "zi", arts: ["bazi"],
  });
  const wealth = chart.analysis.geju.caige;
  return {
    id: spec.id,
    date: `${spec.year}-${spec.month.padStart(2, "0")}-${spec.day.padStart(2, "0")} ${spec.hour.padStart(2, "0")}:${spec.minute.padStart(2, "0")} Shanghai clock`,
    pillars: Object.values(chart.ganzhi),
    geju: chart.analysis.geju.name,
    route: wealth?.route,
    verdict: wealth?.verdict,
    monthWealth: wealth?.monthWealth.gan,
    adopted: wealth?.adopted.map((a) => ({ gan: a.gan, tenGod: a.tenGod, pillar: a.pillarIndex, purpose: a.purpose })),
    theft: wealth?.theft.state,
    unresolved: wealth?.unresolved,
  };
});
process.stdout.write(JSON.stringify(output));
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--product-root",
        type=Path,
        default=ROOT.parent / "cosmic-fortune-lab",
        help="Product checkout (read-only)",
    )
    args = parser.parse_args()
    product = args.product_root.resolve()
    if not (product / "src/lib/engine/bazi/index.ts").exists():
        parser.error(f"Product checkout missing at {product}")
    lines = SOURCE.read_text().splitlines()
    assert "壬申、壬子、戊午、乙卯" in lines[990]
    assert "壬寅、壬寅、庚辰、辛巳" in lines[995]
    result = subprocess.run(
        ["bun", "-e", REPLAY],
        cwd=product,
        check=True,
        capture_output=True,
        text=True,
    )
    rows = json.loads(result.stdout)
    assert len(rows) == 2
    food, officer = rows
    assert food["id"] == "food"
    assert food["pillars"] == ["壬寅", "壬寅", "庚辰", "辛巳"]
    assert food["geju"] == "偏财格"
    assert food["route"] == "食神生财" and food["verdict"] == "满足"
    assert food["monthWealth"] == "甲" and food["unresolved"] == []
    assert {(a["gan"], a["tenGod"], a["pillar"]) for a in food["adopted"]} == {
        ("壬", "食神", 0), ("壬", "食神", 1)
    }
    assert officer["id"] == "officer"
    assert officer["pillars"] == ["壬申", "壬子", "戊午", "乙卯"]
    assert officer["geju"] == "正财格"
    assert officer["route"] == "财生官" and officer["verdict"] == "满足"
    assert officer["monthWealth"] == "癸" and officer["unresolved"] == []
    assert officer["theft"] == "未见夺财"
    assert {(a["gan"], a["tenGod"], a["pillar"]) for a in officer["adopted"]} == {
        ("乙", "正官", 3)
    }
    assert all("制劫" not in a["purpose"] for a in officer["adopted"])
    print(json.dumps({
        "scope": "现代日期同四柱复算及 Product 当前实现判语；非历史生日或 Classics 独立语义判定",
        "productRoot": str(product),
        "cases": rows,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
