"""Audit why the shared real-date charts cannot provide 051 favorite-luck decisions.

Run: python3 tools/verify-ditiansui-051-favorite-boundary.py
This is a blocking-evidence check, not a favorite-element inference engine.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md"
FACTS = ROOT / "tools/reports/facts-sample.json"

SOURCE_CUES = {
    2663: "再究司令以定真假，然后取用",
    2942: "旺则抑之，如不可抑，反宜扶之",
    2943: "弱则扶之，如不可扶，反宜抑之",
    2967: "随岁运取用",
    3211: "秋木虽弱，木根深而木亦强",
    7315: "日主元神厚者，以壬癸亥子为喜神",
    7316: "日主元神薄者，以丙丁巳午为喜神",
    8998: "木有余，以火为喜神，以金为忌神，以水为仇神，以土为闲神",
    8999: "木不足，以水为喜神，以土为忌神，以金为仇神，以火为闲神",
}

SEMANTIC_KEYS = {
    "favorite_luck_element_decision_record", "yongshen",
    "natal_favorable_context", "yongshen_effective", "jishen_empowered",
}

CASE_EXPECTED = {
    "caseP1_051_tiaohou_candidate": {
        "year": 2025, "day": "丙", "month": "子", "strength": "中和",
        "candidate_gans": {"壬", "戊"}, "luck": "癸酉",
    },
    "caseP1_011_seven_killer": {
        "year": 2031, "day": "乙", "month": "卯", "strength": "极强",
        "candidate_gans": {"丙", "癸"}, "luck": "辛亥",
    },
}


def values(facts: list[dict], key: str, scope: dict | None = None) -> set[str]:
    return {
        fact["value"] for fact in facts
        if fact.get("key") == key and (scope is None or fact.get("scope") == scope)
    }


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    for number, cue in SOURCE_CUES.items():
        assert cue in lines[number - 1], (number, cue)

    charts = json.loads(FACTS.read_text())["bazi"]
    assert len(charts) == 43, "shared fixture changed; re-audit the real-chart boundary"
    semantic_hits = {
        case_id: sorted({fact["key"] for fact in chart["facts"]} & SEMANTIC_KEYS)
        for case_id, chart in charts.items()
        if {fact["key"] for fact in chart["facts"]} & SEMANTIC_KEYS
    }
    assert not semantic_hits, semantic_hits

    observed = {}
    for case_id, expected in CASE_EXPECTED.items():
        facts = charts[case_id]["facts"]
        assert values(facts, "rizhu", {"layer": "本命", "pillar": "day"}) == {expected["day"]}
        assert values(facts, "yueling", {"layer": "本命", "pillar": "month"}) == {expected["month"]}
        assert values(facts, "rizhu_strength", {"layer": "本命"}) == {expected["strength"]}
        assert values(facts, "tiaohou_candidate_gan", {"layer": "本命"}) == expected["candidate_gans"]
        assert values(facts, "tiaohou_profile_status", {"layer": "本命"}) == {"基础候选"}
        assert values(facts, "dayun_gan_zhi", {"layer": "大运", "year": expected["year"]}) == {expected["luck"]}
        observed[case_id] = {
            "year": expected["year"], "effectiveLuck": expected["luck"],
            "candidateGans": sorted(expected["candidate_gans"]),
            "favoriteDecision": "信息不足",
        }

    print(json.dumps({
        "status": "PASS", "sourceCuesChecked": len(SOURCE_CUES),
        "realBirthCharts": len(charts), "formalDecisionFacts": 0,
        "boundaryCases": observed,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
