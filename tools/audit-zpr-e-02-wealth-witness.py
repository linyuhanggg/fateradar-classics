#!/usr/bin/env python3
"""Audit real-chart *observations* for the wealth branch of ZPR-E-02.

The returned three states concern only the narrow conjunction
甲日辰月、月藏戊、戊透、丙食神透. They are NOT verdicts for 食生财、官护财,
ZPR-E-02, or a fortune prediction.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tools/reports/facts-sample.json"
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
PILLARS = ("year", "month", "time")


def values(facts: list[dict], key: str, pillar: str) -> list[str]:
    return [
        fact["value"]
        for fact in facts
        if fact["key"] == key
        and fact.get("scope", {}).get("layer") == "本命"
        and fact.get("scope", {}).get("pillar") == pillar
    ]


def stem_is(facts: list[dict], key: str, pillar: str, value: str) -> bool | None:
    observed = values(facts, key, pillar)
    if len(observed) != 1:
        return None
    return observed[0] == value


def any_stem(facts: list[dict], value: str) -> bool | None:
    seen = [stem_is(facts, "gan", pillar, value) for pillar in PILLARS]
    if True in seen:
        return True
    if None in seen:
        return None
    return False


def structural_witness(facts: list[dict]) -> str:
    # 辰中戊 is positive evidence only. An absent canggan row is not a complete
    # hidden-stem scan, so it cannot supply a negative verdict.
    month_hidden = values(facts, "canggan", "month")
    clauses: tuple[bool | None, ...] = (
        stem_is(facts, "rizhu", "day", "甲"),
        stem_is(facts, "yueling", "month", "辰"),
        True if "戊" in month_hidden else None,
        any_stem(facts, "戊"),
        any_stem(facts, "丙"),
    )
    if False in clauses:
        return "不满足"
    if None in clauses:
        return "信息不足"
    return "满足"


def project_without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    return [
        fact
        for fact in facts
        if not (
            fact["key"] == key
            and fact.get("scope", {}).get("layer") == "本命"
            and fact.get("scope", {}).get("pillar") == pillar
        )
    ]


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    assert "財喜食神以相生，生官以護財" in lines[329]
    assert "見財透食神" in lines[342]
    assert "財逢劫，而透食以化之、生官以制之" in lines[401]
    assert "財旺生官，露食則雜" in lines[616]
    cases = json.loads(CASES.read_text())["bazi"]
    main_case = cases["caseP1_ZPR_01_wu_only"]["facts"]
    no_wu = cases["caseP1_ZPR_01_no_wu"]["facts"]
    both = cases["caseP1_ZPR_01_wu_gui_both"]["facts"]
    assert structural_witness(main_case) == "满足"
    assert structural_witness(no_wu) == "不满足"
    assert structural_witness(both) == "满足"
    assert structural_witness(project_without(main_case, "gan", "year")) == "信息不足"
    assert structural_witness(project_without(project_without(main_case, "gan", "month"), "gan", "time")) == "信息不足"
    assert values(main_case, "gan", "year") == ["戊"]
    assert values(main_case, "gan", "month") == ["丙"]
    assert values(main_case, "gan", "time") == ["丙"]
    assert values(no_wu, "gan", "year") == ["辛"]  # 官与食共现，戊仍未透。
    assert values(no_wu, "gan", "time") == ["丙"]
    assert values(both, "gan", "time") == ["癸"]  # 财、印入口可并存。
    print(json.dumps({
        "claim": "仅甲辰月戊透且丙食神透的结构观察；非食生财或护财关系裁决",
        "cases": {
            "caseP1_ZPR_01_wu_only": "满足",
            "caseP1_ZPR_01_no_wu": "不满足",
            "caseP1_ZPR_01_wu_gui_both": "满足",
            "wu_only_without_year_gan": "信息不足",
            "wu_only_without_month_and_time_gan": "信息不足",
        },
        "source": "ziping-zhenquan:L0330/L0343/L0402/L0617",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
