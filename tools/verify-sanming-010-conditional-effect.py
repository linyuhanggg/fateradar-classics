#!/usr/bin/env python3
"""Verify the source-bounded SANMINGTONGH-010 conditional effect step.

The synthetic truth table checks the *conditional* source wording. Real chart
fixtures only test entry scope: none supplies an adjudicated 有救/有情 input.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/SANMINGTONGH_010_CONDITIONAL_EFFECT_CONTRACT_20260923.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
UNKNOWN = "信息不足"
OUT_OF_SCOPE = "不适用"
GAN = set("甲乙丙丁戊己庚辛壬癸")


def scoped_value(facts: list[dict], keys: tuple[str, ...], scope: dict) -> tuple[str | None, bool]:
    values = {
        fact.get("value")
        for fact in facts
        if fact.get("key") in keys and fact.get("scope") == scope
    }
    if len(values) > 1:
        return None, True
    value = next(iter(values)) if values else None
    return (value if value in GAN else None), False


def evaluate(
    facts: list[dict], selected_year: int,
    effective_suppression: str = "undetermined",
    affinity: str = "undetermined",
) -> dict:
    """Evaluate only the 甲日 + selected 戊岁 source example.

    The two semantic inputs must come from *independent* adjudication. This
    function intentionally cannot derive them from 庚申 or 戊癸 structure facts.
    """
    statuses = {"proven", "ruled_out", "undetermined"}
    if effective_suppression not in statuses or affinity not in statuses:
        raise ValueError("invalid semantic status")
    day, day_conflict = scoped_value(
        facts, ("natal_day_gan", "gan"), {"layer": "本命", "pillar": "day"}
    )
    year_gan, year_conflict = scoped_value(
        facts, ("liunian_gan",), {"layer": "流年", "year": selected_year}
    )
    if day_conflict or year_conflict:
        return {"entryVerdict": UNKNOWN, "sourceEffectTier": UNKNOWN}
    if (day is not None and day != "甲") or (year_gan is not None and year_gan != "戊"):
        return {"entryVerdict": "不满足", "sourceEffectTier": OUT_OF_SCOPE}
    if day is None or year_gan is None:
        return {"entryVerdict": UNKNOWN, "sourceEffectTier": UNKNOWN}
    if "undetermined" in (effective_suppression, affinity):
        return {"entryVerdict": "满足", "sourceEffectTier": UNKNOWN}
    tiers = {
        ("proven", "proven"): "凶反为吉",
        ("proven", "ruled_out"): "凶半",
        ("ruled_out", "proven"): "凶半",
        ("ruled_out", "ruled_out"): "凶莫能解",
    }
    return {"entryVerdict": "满足", "sourceEffectTier": tiers[(effective_suppression, affinity)]}


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    source = contract["source"]
    source_bytes = (ROOT / source["path"]).read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == source["sha256"]
    lines = source_bytes.decode("utf-8").splitlines()
    for clause in source["clauses"]:
        assert clause["quote"] in lines[clause["line"] - 1], clause
    assert contract["status"] == "conditional_source_step_only"
    expected_ladder = {
        (row["effectiveSuppression"], row["affinity"]): row["sourceEffectTier"]
        for row in contract["conditionalLadder"]
    }
    assert len(expected_ladder) == 4

    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["bazi"]
    checked_real = 0
    for suffix in (
        "both", "same_only", "split_only", "split_and_gui", "natal_gui_only",
        "luck_gui_only", "neither", "wrong_day", "wrong_year", "unknown_luck",
    ):
        selected_year = 2017 if suffix == "wrong_year" else 2018
        verdict = evaluate(cases[f"caseP1_010_{suffix}"]["facts"], selected_year)
        want_entry = "不满足" if suffix.startswith("wrong_") else "满足"
        assert verdict["entryVerdict"] == want_entry, (suffix, verdict)
        want_effect = OUT_OF_SCOPE if want_entry == "不满足" else UNKNOWN
        assert verdict["sourceEffectTier"] == want_effect, (suffix, verdict)
        checked_real += 1

    entry_facts = cases["caseP1_010_both"]["facts"]
    for suppression, affinity in itertools.product(
        ("proven", "ruled_out", "undetermined"), repeat=2
    ):
        actual = evaluate(entry_facts, 2018, suppression, affinity)
        assert actual["entryVerdict"] == "满足"
        assert actual["sourceEffectTier"] == expected_ladder.get(
            (suppression, affinity), UNKNOWN
        )
    assert evaluate(entry_facts, 2100)["entryVerdict"] == UNKNOWN
    assert evaluate([], 2018)["entryVerdict"] == UNKNOWN
    without_day = [
        fact for fact in entry_facts
        if not (fact["key"] in {"gan", "natal_day_gan"}
                and fact.get("scope") == {"layer": "本命", "pillar": "day"})
    ]
    without_year = [
        fact for fact in entry_facts
        if not (fact["key"] == "liunian_gan"
                and fact.get("scope") == {"layer": "流年", "year": 2018})
    ]
    assert evaluate([
        *without_day, {"key": "gan", "value": "乙", "scope": {"layer": "本命", "pillar": "day"}}
    ], 2100)["sourceEffectTier"] == OUT_OF_SCOPE
    assert evaluate([
        *without_year, {"key": "liunian_gan", "value": "丁", "scope": {"layer": "流年", "year": 2018}}
    ], 2018)["sourceEffectTier"] == OUT_OF_SCOPE
    assert evaluate([
        *entry_facts, {"key": "gan", "value": "乙", "scope": {"layer": "本命", "pillar": "day"}}
    ], 2018)["entryVerdict"] == UNKNOWN
    print(f"source clauses {len(source['clauses'])}; real entry fixtures {checked_real}; synthetic ladder states 9: OK")


if __name__ == "__main__":
    main()
