#!/usr/bin/env python3
"""Audit named *structural* observations around SMTH-010's later paragraph.

This does not evaluate 日犯岁君, 制木, 焚木, 天月德救应, or any outcome.
The case facts are real buildBazi outputs shared with the product repository.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
PILLARS = ("year", "month", "day", "time")
SEMANTIC_KEYS = {
    "rescue_condition",
    "transit_effect_semantics",
    "natal_rescue_evidence",
    "dayun_rescue_evidence",
}


def scoped_values(facts: list[dict], key: str, scope: dict) -> set[str]:
    return {f["value"] for f in facts if f["key"] == key and f["scope"] == scope}


def one(facts: list[dict], key: str, scope: dict) -> str | None:
    values = scoped_values(facts, key, scope)
    return next(iter(values)) if len(values) == 1 and "信息不足" not in values else None


def inspect(facts: list[dict], selected_year: int) -> dict:
    day = one(facts, "natal_day_gan", {"layer": "本命", "pillar": "day"})
    year = one(facts, "liunian_gan", {"layer": "流年", "year": selected_year})
    if (day is not None and day != "甲") or (year is not None and year != "戊"):
        return {"trigger": "不适用", "observations": None}
    if day is None or year is None:
        return {"trigger": "信息不足", "observations": None}

    gan = {p: one(facts, "gan", {"layer": "本命", "pillar": p}) for p in PILLARS}
    zhi = {p: one(facts, "zhi", {"layer": "本命", "pillar": p}) for p in PILLARS}
    all_gan = all(value is not None for value in gan.values())
    all_zhi = all(value is not None for value in zhi.values())
    day_de = scoped_values(facts, "shensha", {"layer": "本命", "pillar": "day"})
    natal_relations = scoped_values(facts, "natal_relation", {"layer": "本命"})
    return {
        "trigger": "甲日戊岁",
        "observations": {
            # These are only witnessed stems. Even an empty list is not 无救.
            "natalGengXinPillars": [p for p in PILLARS if gan[p] in ("庚", "辛")] if all_gan else None,
            "natalBingDingPillars": [p for p in PILLARS if gan[p] in ("丙", "丁")] if all_gan else None,
            "natalExtraJiaYiPillars": [p for p in PILLARS if p != "day" and gan[p] in ("甲", "乙")]
            if all_gan else None,
            "natalWoodSupportPillars": [p for p in PILLARS if zhi[p] in ("寅", "卯", "亥", "未")]
            if all_zhi else None,
            # Complete branch presence is distinct from 局已成、制木、焚木.
            "natalSiYouChouPresent": {"巳", "酉", "丑"}.issubset(zhi.values()) if all_zhi else None,
            "natalYinWuXuPresent": {"寅", "午", "戌"}.issubset(zhi.values()) if all_zhi else None,
            "natalMetalRelationEmitted": any("三合:巳酉丑金局@" in v for v in natal_relations),
            "natalFireRelationEmitted": any("三合:寅午戌火局@" in v for v in natal_relations),
            # No negative assertion: shensha's lack of a row is not a typed zero.
            "dayDeLabelsEmitted": sorted(day_de.intersection({"天德贵人", "月德贵人"})),
        },
    }


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    for number, phrase in (
        (1085, "假如甲日見戊年太嵗"),
        (1086, "柱中無庚辛巳酉丑金局制木丙丁火局焚木者太凶"),
        (1087, "若日干是天月徳太嵗是用神則無咎而反有獲"),
        (4061, "丙丁得寅午戌火局庚辛得巳酉丑金局"),
    ):
        assert phrase in lines[number - 1], (number, phrase)

    sample = json.loads(FIXTURE.read_text())["bazi"]
    probes = {
        "caseP1_010_both": 2018,
        "caseP1_010_split_only": 2018,
        "caseP1_010_luck_gui_only": 2018,
        "caseP1_010_neither": 2018,
        "caseP1_010_unknown_luck": 2018,
        "caseP1_010_wrong_day": 2018,
        "caseP1_010_wrong_year": 2017,
        "cov3_bazi_12": 2018,
    }
    observed = {name: inspect(sample[name]["facts"], year) for name, year in probes.items()}
    for name in probes:
        assert not ({f["key"] for f in sample[name]["facts"]} & SEMANTIC_KEYS), name

    both = observed["caseP1_010_both"]["observations"]
    split = observed["caseP1_010_split_only"]["observations"]
    luck = observed["caseP1_010_luck_gui_only"]["observations"]
    neither = observed["caseP1_010_neither"]["observations"]
    early = observed["caseP1_010_unknown_luck"]["observations"]
    assert both["natalGengXinPillars"] == ["year", "time"]
    assert both["natalBingDingPillars"] == []
    assert both["dayDeLabelsEmitted"] == ["天德贵人", "月德贵人"]
    assert split["natalGengXinPillars"] == ["year", "time"]
    assert luck["natalBingDingPillars"] == ["month"]
    assert neither["natalGengXinPillars"] == ["year", "time"]
    assert neither["dayDeLabelsEmitted"] == []  # year/time labels cannot stand in for the day
    assert early["natalYinWuXuPresent"] is True
    assert early["natalFireRelationEmitted"] is True
    assert observed["caseP1_010_wrong_day"]["trigger"] == "不适用"
    assert observed["caseP1_010_wrong_year"]["trigger"] == "不适用"
    assert observed["cov3_bazi_12"]["trigger"] == "不适用"
    # The non-applicable real chart has 巳酉丑: this must not activate 甲日戊岁.
    metal_control = sample["cov3_bazi_12"]["facts"]
    control_zhi = {one(metal_control, "zhi", {"layer": "本命", "pillar": p}) for p in PILLARS}
    assert {"巳", "酉", "丑"}.issubset(control_zhi)
    assert any(
        f["key"] == "natal_relation" and "三合:巳酉丑金局@" in f["value"]
        for f in metal_control
    )
    both_facts = sample["caseP1_010_both"]["facts"]
    missing_natal_gan = [
        f
        for f in both_facts
        if not (f["key"] == "gan" and f["scope"] == {"layer": "本命", "pillar": "year"})
    ]
    assert inspect(missing_natal_gan, 2018)["observations"]["natalGengXinPillars"] is None
    missing_selected_year = [
        f
        for f in both_facts
        if not (f["key"] == "liunian_gan" and f["scope"] == {"layer": "流年", "year": 2018})
    ]
    assert inspect(missing_selected_year, 2018)["trigger"] == "信息不足"
    print(
        json.dumps(
            {"status": "pass", "sourceLines": [1085, 1086, 1087, 4061], "cases": observed},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
