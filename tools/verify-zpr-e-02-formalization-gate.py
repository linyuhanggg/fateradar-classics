"""Prove the structural FactKey preserves the narrow ZPR entry's tri-state.

Run: python3 tools/verify-zpr-e-02-formalization-gate.py
The V5 historical 43-chart projection remains locked while current V6's seven
appended Yin-month probes are checked as information-insufficient for this
single-qi entry. The source rule remains provisional.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/ZPR_E_02_SINGLE_QI_FORMALIZATION_GATE_20260923.json"
CANDIDATE = ROOT / "docs/closeout/ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
FIXTURE_SHA = "3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc"
CURRENT_FIXTURE_SHA = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"
V5_FIXTURE_REV = "fe69959fd925b8a4e26552761a49445a43a5f16a"
V6_ADDED_CASES = {
    "caseP1_ZPR_month_yin_bing_only_1969",
    "caseP1_ZPR_month_xin_jia_bing_1954",
    "caseP1_ZPR_month_xin_jia_bing_1984",
    "caseP1_ZPR_month_xin_no_jia_1979",
    "caseP1_ZPR_month_xin_jia_bing_wu_1984",
    "caseP1_ZPR_month_xin_jia_bing_meeting_1994",
    "caseP1_ZPR_month_yin_bing_wu_1979",
}
V6_ADDED_STRUCTURAL_KEYS = {
    "natal_yin_hidden_exposure_pattern",
    "natal_yin_simple_hidden_exposure_pattern",
}
FACT_SCOPE = {"layer": "本命", "pillar": "month"}
DAY_SCOPE = {"layer": "本命", "pillar": "day"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def scoped_values(facts: list[dict], key: str, scope: dict) -> list[str]:
    return [fact["value"] for fact in facts if fact.get("key") == key and fact.get("scope") == scope]


def one(values: list[str]) -> str | None:
    distinct = set(values)
    return next(iter(distinct)) if len(distinct) == 1 else None


def materialize(facts: list[dict], contract: dict) -> list[dict]:
    """Prototype only: source-neutral complete single-qi month hidden stem."""
    spec = contract["derivedStructuralFact"]
    month = one(scoped_values(facts, "zhi", FACT_SCOPE))
    month_order = one(scoped_values(facts, "yueling", FACT_SCOPE))
    if month is None or month != month_order:
        return []
    expected = spec["valueByBranch"].get(month)
    if expected is None or set(scoped_values(facts, "canggan", FACT_SCOPE)) != {expected}:
        return []
    return [{"key": spec["key"], "value": expected, "scope": FACT_SCOPE}]


def proposed_rule(contract: dict) -> dict:
    key = contract["derivedStructuralFact"]["key"]
    branches = [
        {"all_of": [
            {"key": "gan", "value": day, "scope": DAY_SCOPE},
            {"key": key, "value": officer, "scope": FACT_SCOPE},
        ]}
        for day, officer in contract["regularOfficerStemByDay"].items()
    ]
    assert len(branches) == 10
    return {"rule_id": contract["sourceRuleId"], "verified": False,
            "applicable_to": {"any_of": branches}}


def verdict(evaluator, facts: list[dict], rule: dict, contract: dict) -> str:
    derived = materialize(facts, contract)
    return evaluator.evaluate(rule, facts + derived)["verdict"]


def without(facts: list[dict], key: str, scope: dict) -> list[dict]:
    return [fact for fact in facts if fact.get("key") != key or fact.get("scope") != scope]


def v5_projection(chart: dict) -> dict:
    """Remove only the two new structural facts appended to the V5 sample."""
    projected = copy.deepcopy(chart)
    projected["facts"] = [
        fact for fact in projected["facts"]
        if fact.get("key") not in V6_ADDED_STRUCTURAL_KEYS
    ]
    return projected


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    candidate = json.loads(CANDIDATE.read_text())
    assert contract["status"] == "source_registered_v5_handoff_product_import_pending"
    assert contract["derivedStructuralFact"]["valueByBranch"] == candidate["supportedSingleQiBranches"]
    assert contract["regularOfficerStemByDay"] == candidate["regularOfficerStemByDay"]
    current_fixture_bytes = FIXTURE.read_bytes()
    assert hashlib.sha256(current_fixture_bytes).hexdigest() == CURRENT_FIXTURE_SHA
    current_charts = json.loads(current_fixture_bytes)["bazi"]
    v5_fixture_bytes = subprocess.check_output(
        ["git", "show", f"{V5_FIXTURE_REV}:tools/reports/facts-sample.json"], cwd=ROOT
    )
    assert hashlib.sha256(v5_fixture_bytes).hexdigest() == FIXTURE_SHA
    charts = json.loads(v5_fixture_bytes)["bazi"]
    assert len(charts) == 43 and len(current_charts) == 50
    assert set(current_charts) - set(charts) == V6_ADDED_CASES
    assert all(v5_projection(current_charts[case_id]) == chart for case_id, chart in charts.items())

    narrow = load_module("zpr_narrow_candidate", ROOT / "tools/verify-zpr-e-02-single-qi-month-entry.py")
    evaluator = load_module("zpr_predicate_reference", ROOT / "tools/eval-predicates.py")
    rule = proposed_rule(contract)
    registered = [item for item in yaml.safe_load(
        (ROOT / "references/books/bazi/ziping-zhenquan/rules.yaml").read_text()
    )["rules"] if item["rule_id"] == rule["rule_id"]]
    assert len(registered) == 1 and registered[0]["verified"] is False
    assert registered[0]["applicable_to"] == rule["applicable_to"]
    fact_key = contract["derivedStructuralFact"]["key"]
    results = {}
    for case_id, chart in charts.items():
        raw_facts = without(chart["facts"], fact_key, FACT_SCOPE)
        emitted = [fact for fact in chart["facts"] if fact.get("key") == fact_key]
        normalized = [{field: fact[field] for field in ("key", "value", "scope")} for fact in emitted]
        assert normalized == materialize(raw_facts, contract), (case_id, emitted)
        assert all(fact.get("derivedFrom") for fact in emitted), case_id
        actual = evaluator.evaluate(rule, chart["facts"])["verdict"]
        expected = narrow.decide(raw_facts, candidate)
        assert actual == expected, (case_id, actual, expected)
        results.setdefault(actual, []).append(case_id)
    assert {state: len(ids) for state, ids in results.items()} == {
        "满足": 4, "不满足": 7, "信息不足": 32,
    }

    current_results: dict[str, list[str]] = {}
    for case_id, chart in current_charts.items():
        actual = evaluator.evaluate(rule, chart["facts"])["verdict"]
        current_results.setdefault(actual, []).append(case_id)
    assert {state: len(ids) for state, ids in current_results.items()} == {
        "满足": 4, "不满足": 7, "信息不足": 39,
    }
    assert all(
        case_id in current_results["信息不足"]
        for case_id in V6_ADDED_CASES
    )

    positive = without(charts["caseP1_010_luck_gui_only"]["facts"], fact_key, FACT_SCOPE)
    negative = without(charts["cov2_bazi_3"]["facts"], fact_key, FACT_SCOPE)
    multicang = without(charts["caseB"]["facts"], fact_key, FACT_SCOPE)
    corrupt_hidden = copy.deepcopy(positive) + [
        {"key": "canggan", "value": "庚", "scope": FACT_SCOPE},
    ]
    conflict_day = copy.deepcopy(positive) + [
        {"key": "gan", "value": "丁", "scope": DAY_SCOPE},
    ]
    conflict_order = copy.deepcopy(positive) + [
        {"key": "yueling", "value": "子", "scope": FACT_SCOPE},
    ]
    probes = {
        "positive": (positive, "满足"),
        "negative": (negative, "不满足"),
        "missingHidden": (without(positive, "canggan", FACT_SCOPE), "信息不足"),
        "missingDay": (without(positive, "gan", DAY_SCOPE), "信息不足"),
        "missingOrder": (without(positive, "yueling", FACT_SCOPE), "信息不足"),
        "conflictHidden": (corrupt_hidden, "信息不足"),
        "conflictDay": (conflict_day, "信息不足"),
        "conflictOrder": (conflict_order, "信息不足"),
        "multiHiddenBranch": (multicang, "信息不足"),
    }
    for label, (facts, expected) in probes.items():
        actual = verdict(evaluator, facts, rule, contract)
        assert actual == expected, (label, actual, expected)

    # Demonstrate why source rules must not read bare multi-valued canggan.
    naive = {"rule_id": "naive-do-not-register", "applicable_to": {"any_of": [
        {"all_of": [
            {"key": "gan", "value": day, "scope": DAY_SCOPE},
            {"key": "canggan", "value": stem, "scope": FACT_SCOPE},
        ]}
        for day, stem in contract["regularOfficerStemByDay"].items()
    ]}}
    assert evaluator.evaluate(naive, corrupt_hidden)["verdict"] == "满足"
    assert narrow.decide(corrupt_hidden, candidate) == "信息不足"

    # The source-neutral derived key itself needs a singleton conflict guard.
    same_scope_conflict = positive + materialize(positive, contract) + [
        {"key": contract["derivedStructuralFact"]["key"], "value": "癸", "scope": FACT_SCOPE},
    ]
    if fact_key not in evaluator.SINGLE_VALUE_BAZI_FACT_KEYS:
        assert evaluator.evaluate(rule, same_scope_conflict)["verdict"] == "满足"
        guard_status = "required_not_registered"
    else:
        assert evaluator.evaluate(rule, same_scope_conflict)["verdict"] == "信息不足"
        guard_status = "registered"

    print(json.dumps({
        "status": "PASS", "sourceRuleRegistered": True,
        "derivedFactProducedByProduct": True,
        "v5FixtureSha256": FIXTURE_SHA,
        "currentFixtureSha256": CURRENT_FIXTURE_SHA,
        "v5HistoricalCharts": len(charts),
        "currentFixtureCharts": len(current_charts),
        "v5HistoricalChartStates": {state: len(ids) for state, ids in results.items()},
        "currentFixtureStates": {state: len(ids) for state, ids in current_results.items()},
        "probes": {label: expected for label, (_, expected) in probes.items()},
        "bareCangganFalsePositive": True,
        "derivedFactSingletonGuard": guard_status,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
