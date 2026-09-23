"""Audit why the shared real-date charts cannot provide 051 favorite-luck decisions.

Run: python3 tools/verify-ditiansui-051-favorite-boundary.py
This is a blocking-evidence check, not a favorite-element inference engine.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md"
FACTS = ROOT / "tools/reports/facts-sample.json"
EXPECTED_FIXTURE_SHA256 = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"

SOURCE_CUES = {
    2663: "再究司令以定真假，然后取用",
    2942: "旺则抑之，如不可抑，反宜扶之",
    2943: "弱则扶之，如不可扶，反宜抑之",
    2967: "随岁运取用",
    3211: "秋木虽弱，木根深而木亦强",
    7315: (
        "如戊 土生于寅月，以寅中甲木为用神",
        "日主元神厚者，以壬癸亥子为喜神",
    ),
    7316: "日主元神薄者，以丙丁巳午为喜神",
    7317: "如身弱以寅中丙火用神",
    8998: "木有余，以火为喜神，以金为忌神，以水为仇神，以土为闲神",
    8999: "木不足，以水为喜神，以土为忌神，以金为仇神，以火为闲神",
    13402: "看喜行行何运，忌行何运",
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

ILLUSTRATIVE_PREMISE = {"day": "戊", "month": "寅"}
NATAL_PILLARS = ("year", "month", "day", "time")


def one_value(facts: list[dict], key: str, scope: dict) -> str:
    found = values(facts, key, scope)
    assert len(found) == 1, (key, scope, found)
    return next(iter(found))


def values(facts: list[dict], key: str, scope: dict | None = None) -> set[str]:
    return {
        fact["value"] for fact in facts
        if fact.get("key") == key and (scope is None or fact.get("scope") == scope)
    }


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    for number, cues in SOURCE_CUES.items():
        for cue in (cues,) if isinstance(cues, str) else cues:
            assert cue in lines[number - 1], (number, cue)

    fixture_bytes = FACTS.read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == EXPECTED_FIXTURE_SHA256, (
        "shared fixture changed; re-audit the real-chart boundary"
    )
    charts = json.loads(fixture_bytes)["bazi"]
    assert len(charts) == 50, "shared fixture changed; re-audit the real-chart boundary"
    semantic_hits = {
        case_id: sorted({fact["key"] for fact in chart["facts"]} & SEMANTIC_KEYS)
        for case_id, chart in charts.items()
        if {fact["key"] for fact in chart["facts"]} & SEMANTIC_KEYS
    }
    assert not semantic_hits, semantic_hits

    # L7315 is a conditional illustration, not a rule that every 戊日寅月
    # has 甲木为用. Identify the one real-date overlap so a tempting partial
    # match cannot be silently promoted to an adjudicated 喜行五行.
    illustrative_overlap = []
    for case_id, chart in charts.items():
        facts = chart["facts"]
        pillars = {
            pillar: one_value(facts, "gan", {"layer": "本命", "pillar": pillar})
            + one_value(facts, "zhi", {"layer": "本命", "pillar": pillar})
            for pillar in NATAL_PILLARS
        }
        assert one_value(facts, "rizhu", {"layer": "本命", "pillar": "day"}) == pillars["day"][0]
        assert one_value(facts, "yueling", {"layer": "本命", "pillar": "month"}) == pillars["month"][1]
        if pillars["day"][0] == ILLUSTRATIVE_PREMISE["day"] and pillars["month"][1] == ILLUSTRATIVE_PREMISE["month"]:
            illustrative_overlap.append({
                "caseId": case_id,
                "pillars": pillars,
                "strengthLabel": one_value(facts, "rizhu_strength", {"layer": "本命"}),
                "gejuLabel": one_value(facts, "geju", {"layer": "本命"}),
                "candidateGans": sorted(values(facts, "tiaohou_candidate_gan", {"layer": "本命"})),
                "missingAdjudications": [
                    "寅中甲木是否为所取用神", "元神厚薄或身弱转用寅中丙火的来源裁决",
                    "有余不足与原局制化", "所选年份是否随岁运取用",
                ],
                "favoriteDecision": "信息不足",
            })
    assert [item["caseId"] for item in illustrative_overlap] == ["cov3_bazi_1"], illustrative_overlap
    assert illustrative_overlap[0]["pillars"] == {
        "year": "庚戌", "month": "戊寅", "day": "戊午", "time": "己未",
    }
    assert illustrative_overlap[0]["strengthLabel"] == "极强"
    assert illustrative_overlap[0]["gejuLabel"] == "七杀格"
    assert illustrative_overlap[0]["candidateGans"] == ["丙", "甲", "癸"]

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
        "status": "PASS", "sourceCuesChecked": sum(
            1 if isinstance(cues, str) else len(cues) for cues in SOURCE_CUES.values()
        ),
        "fixtureSha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "realBirthCharts": len(charts), "formalDecisionFacts": 0,
        "illustrativePremiseMatches": len(illustrative_overlap),
        "illustrativeOverlap": illustrative_overlap,
        "boundaryCases": observed,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
