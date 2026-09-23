"""Verify the source-scoped 辛寅甲丙 主正财/兼正官 candidate.

Run: python3 tools/verify-zpr-e-02-xin-yin-jia-bing-priority.py
This is a source classification audit, not a completed ZPR-E-02 or 财格 effect.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/ZPR_E_02_XIN_YIN_JIA_BING_PRIORITY_CANDIDATE_20260923.json"
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"
SOURCE_CUES = {
    328: "八字用神，專求月令",
    349: "月令無用神者",
    350: "如木生寅卯",
    351: "然終以月令爲主",
    419: "不透甲而透丙",
    426: "辛生寅月，逢丙而化財爲官",
    435: "辛生寅月，透丙化官，而又透甲，格成正財，正官乃其兼格也",
    452: "辛生寅月，甲丙並透，財與官相生，兩相得也",
    542: "透干會支，取其清者用之",
    548: "兼透則兼用，透而又會，則透與會並用",
}
GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")
PILLARS = ("year", "month", "day", "time")
EXPOSED = ("year", "month", "time")
UNKNOWN = "信息不足"


def scoped_values(facts: list[dict], key: str, pillar: str) -> set[str]:
    scope = {"layer": "本命", "pillar": pillar}
    return {str(fact["value"]) for fact in facts if fact.get("key") == key and fact.get("scope") == scope}


def one(facts: list[dict], key: str, pillar: str) -> str | None:
    values = scoped_values(facts, key, pillar)
    return next(iter(values)) if len(values) == 1 else None


def decide(facts: list[dict]) -> str:
    # Require the full natal chart before making this narrow two-entry claim.
    stems = {pillar: one(facts, "gan", pillar) for pillar in PILLARS}
    branches = {pillar: one(facts, "zhi", pillar) for pillar in PILLARS}
    if any(stem not in GAN for stem in stems.values()):
        return UNKNOWN
    if any(branch not in ZHI for branch in branches.values()):
        return UNKNOWN
    order = one(facts, "yueling", "month")
    if order != branches["month"]:
        return UNKNOWN
    if branches["month"] != "寅" or stems["day"] != "辛":
        return "不满足"
    if scoped_values(facts, "canggan", "month") != {"甲", "丙", "戊"}:
        return UNKNOWN

    visible = {stems[pillar] for pillar in EXPOSED}
    if not {"甲", "丙"} <= visible:
        return "不满足"
    if "戊" in visible or {"寅", "午", "戌"} <= set(branches.values()):
        return UNKNOWN
    return "满足"


def without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    scope = {"layer": "本命", "pillar": pillar}
    return [fact for fact in facts if fact.get("key") != key or fact.get("scope") != scope]


def pillars(facts: list[dict]) -> dict[str, str]:
    return {pillar: one(facts, "gan", pillar) + one(facts, "zhi", pillar) for pillar in PILLARS}


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    assert contract["status"] == "classics_provisional_ZPR-P1-06_product_pending"
    assert contract["formalRuleId"] == "ZPR-P1-06"
    assert contract["scope"] == {"layer": "本命"}
    assert contract["source"]["lines"] == sorted(SOURCE_CUES)
    assert contract["output"]["alwaysUnknown"] == [
        "wholeChartCompletion", "wholeChartPurity", "actualRelationEffect", "rescue",
        "auspiciousOutcome", "selectedYearEffect",
    ]
    assert contract["inputs"]["monthHiddenStems"]["completeExactSet"] == ["甲", "丙", "戊"]
    assert contract["inputs"]["exposedStems"]["conservativeNoExtraMonthHiddenStem"] == "戊"
    assert contract["inputs"]["fullYinWuXuMeeting"]["policy"] == "if_all_present_keep_priority_unknown"
    assert contract["output"]["whenSatisfied"]["entrySet"] == [
        {"entryId": "ZPR-E-02:month-寅:hidden-甲:辛日正财", "sourceStem": "甲", "tenGod": "正财", "localRank": "主"},
        {"entryId": "ZPR-E-02:month-寅:hidden-丙:辛日正官", "sourceStem": "丙", "tenGod": "正官", "localRank": "兼"},
    ]
    lines = SOURCE.read_text().splitlines()
    for number, cue in SOURCE_CUES.items():
        assert cue in lines[number - 1], (number, cue)

    rule = next(r for r in json.loads(EXECUTABLE.read_text())["rules"] if r["id"] == "ZPR-E-02")
    assert rule["rescue"] == "unimplemented" and rule["verified"] is False
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == contract["fixture"]["sha256"]
    shared = json.loads(FIXTURE.read_text())["bazi"]
    assert len(shared) == contract["fixture"]["baziCases"] == 50

    results: dict[str, str] = {}
    for probe in contract["realDateProbes"]:
        facts = shared[probe["fixtureCaseId"]]["facts"]
        assert pillars(facts) == probe["pillars"], probe["id"]
        actual = decide(facts)
        assert actual == probe["caseState"], (probe["id"], actual)
        results[probe["id"]] = actual
        if probe["id"] == "xin_yin_jia_bing_1984":
            positive = facts

    assert decide(without(positive, "gan", "year")) == UNKNOWN
    assert decide(without(positive, "canggan", "month")) == UNKNOWN
    assert decide(positive + [
        {"key": "gan", "value": "庚", "scope": {"layer": "本命", "pillar": "year"}}
    ]) == UNKNOWN
    assert decide(positive + [
        {"key": "zhi", "value": "午", "scope": {"layer": "本命", "pillar": "year"}}
    ]) == UNKNOWN
    # Neither transit stems nor legacy Product geju labels are source truth.
    assert decide(positive + [
        {"key": "gan", "value": "戊", "scope": {"layer": "流年", "pillar": "year", "year": 2018}},
        {"key": "geju", "value": "正官格", "scope": {"layer": "本命"}},
    ]) == "满足"
    assert decide(shared["caseB"]["facts"]) == "不满足"  # 己日, not a 辛日 priority ruling.

    shared_yin = {
        case_id: decide(chart["facts"])
        for case_id, chart in shared.items()
        if one(chart["facts"], "zhi", "month") == "寅"
    }
    assert len(shared_yin) == 12
    assert {case_id for case_id, verdict in shared_yin.items() if verdict == "满足"} == {
        "caseP1_ZPR_month_xin_jia_bing_1954",
        "caseP1_ZPR_month_xin_jia_bing_1984",
    }
    print(json.dumps({
        "status": "PASS", "sourceCues": len(SOURCE_CUES),
        "fixtureSha256": contract["fixture"]["sha256"],
        "sharedRealDateCharts": len(shared), "sharedYinMonthCharts": shared_yin,
        "sharedNamedProbes": results,
        "fullZprE02Delivered": False,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
