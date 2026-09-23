#!/usr/bin/env python3
"""Check the source conflicts and real-chart limits of SMTH-010's full effect."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/closeout/SANMINGTONGH_010_EFFECT_AUDIT_20260923.json"
SEMANTIC_KEYS = {
    "rescue_condition", "transit_effect_semantics", "natal_rescue_evidence", "dayun_rescue_evidence",
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    assert audit["schema"] == "fateradar-smth-010-effect-audit-v1"
    assert audit["ruleId"] == "SANMINGTONGH-010" and audit["status"] == "blocked_full_effect"
    source = audit["source"]
    source_bytes = (ROOT / source["path"]).read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == source["sha256"]
    lines = source_bytes.decode().splitlines()
    assert {item["role"] for item in source["clauses"]} == {
        "literal_entry", "effective_suppression", "affinity", "conditional_ladder", "later_clause",
        "later_exception", "same_book_affinity_tension", "same_book_gengshen_countercontext",
        "broader_affinity_definition", "same_book_yongshen_exception",
    }
    for clause in source["clauses"]:
        assert clause["quote"] in lines[clause["line"] - 1], clause
    for witness in audit["editorialWitnesses"]:
        assert witness["quote"] in (ROOT / witness["path"]).read_text().splitlines()[witness["line"] - 1], witness

    boundary = audit["proposedTypedInterface"]
    assert boundary["status"] == "review_only_not_adopted"
    assert boundary["scope"] == {"layer": "流年", "year": "selected"}
    assert boundary["requestedProductKey"] == {
        "key": "rescue_condition", "values": ["成立", "不成立", "信息不足"]
    }
    assert all(values == ["proven", "ruled_out", "undetermined"] for values in boundary["independentSourceInputs"].values())
    assert len(audit["sourceDecisionsNeeded"]) == 4
    minimum = [item for item in audit["sourceDecisionsNeeded"] if item.get("minimumNextDecision")]
    assert len(minimum) == 1 and minimum[0]["id"] == "suppression_scope"
    assert minimum[0]["isolatingFixture"] == "caseP1_010_same_only@2018"

    fixture = audit["fixture"]
    fixture_bytes = (ROOT / fixture["path"]).read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == fixture["sha256"]
    cases = json.loads(fixture_bytes)["bazi"]
    effect = load_module("smth_010_conditional", ROOT / "tools/verify-sanming-010-conditional-effect.py")
    structure = load_module("smth_010_post_anchor", ROOT / "tools/audit-smth-010-post-anchor.py")
    entry = fixture["entrySatisfied"]
    outside = fixture["entryNotApplicable"]
    assert len(entry) == 8 and len(outside) == 2 and len(set(entry + outside)) == 10
    assert fixture["fullEffectUnknown"] == entry
    assert fixture["fullEffectAdjudicatedPositive"] == fixture["fullEffectAdjudicatedNegative"] == []
    for suffix in entry + outside:
        year = 2017 if suffix == "wrong_year" else 2018
        facts = cases[f"caseP1_010_{suffix}"]["facts"]
        assert not ({fact["key"] for fact in facts} & SEMANTIC_KEYS), suffix
        result = effect.evaluate(facts, year)
        observed = structure.inspect(facts, year)
        if suffix in entry:
            assert result == {"entryVerdict": "满足", "sourceEffectTier": "信息不足"}, suffix
            assert observed["trigger"] == "甲日戊岁", suffix
        else:
            assert result == {"entryVerdict": "不满足", "sourceEffectTier": "不适用"}, suffix
            assert observed["trigger"] == "不适用", suffix
    both = structure.inspect(cases["caseP1_010_both"]["facts"], 2018)["observations"]
    same_only = cases["caseP1_010_same_only"]["facts"]
    neither = structure.inspect(cases["caseP1_010_neither"]["facts"], 2018)["observations"]
    unknown_luck = cases["caseP1_010_unknown_luck"]["facts"]
    assert both["natalGengXinPillars"] == ["year", "time"]
    assert both["dayDeLabelsEmitted"] == ["天德贵人", "月德贵人"]
    assert any(f["key"] == "gan" and f["value"] == "庚" and f["scope"] == {"layer": "本命", "pillar": "year"} for f in same_only)
    assert any(f["key"] == "zhi" and f["value"] == "申" and f["scope"] == {"layer": "本命", "pillar": "year"} for f in same_only)
    assert not any(f["key"] == "gan" and f["value"] == "癸" and f["scope"].get("layer") == "本命" for f in same_only)
    assert any(f["key"] == "dayun_gan_zhi" and f["value"] == "丁亥" and f["scope"].get("year") == 2018 for f in same_only)
    assert neither["natalGengXinPillars"] == ["year", "time"]
    assert not any(f["key"] == "dayun_gan_zhi" and f["scope"].get("year") == 2018 for f in unknown_luck)
    assert structure.inspect(unknown_luck, 2018)["observations"]["natalFireRelationEmitted"] is True

    both_facts = cases["caseP1_010_both"]["facts"]
    natal_conflict = [*both_facts, {"key": "natal_day_gan", "value": "乙", "scope": {"layer": "本命", "pillar": "day"}}]
    annual_conflict = [*both_facts, {"key": "liunian_gan", "value": "丁", "scope": {"layer": "流年", "year": 2018}}]
    missing_annual = [
        fact for fact in both_facts
        if not (fact["key"] == "liunian_gan" and fact.get("scope", {}).get("year") == 2018)
    ]
    for partial in (natal_conflict, annual_conflict, missing_annual):
        assert effect.evaluate(partial, 2018) == {
            "entryVerdict": "信息不足", "sourceEffectTier": "信息不足"
        }

    rules = yaml.safe_load((ROOT / "references/books/bazi/sanming-tonghui/rules.yaml").read_text())["rules"]
    original = next(rule for rule in rules if rule["rule_id"] == "SANMINGTONGH-010")
    assert original["applicable_to"] == [] and original["verified"] is False
    print("PASS SMTH-010 effect audit: 10 real chart entries, 0 effect verdicts, 3 conflict/missing gates, 10 source clauses, 3 editorial witnesses")


if __name__ == "__main__":
    main()
