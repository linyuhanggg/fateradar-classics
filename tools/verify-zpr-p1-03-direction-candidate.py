#!/usr/bin/env python3
"""Check the source chain and real-chart tri-state boundary of ZPR-P1-03."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "references/books/bazi/ziping-zhenquan/rules.yaml"
FULLTEXT = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"


def load_evaluator():
    spec = importlib.util.spec_from_file_location("eval_predicates", ROOT / "tools/eval-predicates.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    return [
        fact for fact in facts
        if not (fact["key"] == key and fact.get("scope", {}).get("layer") == "本命"
                and fact.get("scope", {}).get("pillar") == pillar)
    ]


def main() -> int:
    rules = {rule["rule_id"]: rule for rule in yaml.safe_load(RULES.read_text())["rules"]}
    entry = rules["ZPR-P1-01"]
    candidate = rules["ZPR-P1-03"]
    assert candidate["applicable_to"] == entry["applicable_to"]
    assert candidate["candidate_output"] == {
        "entry": "甲辰月透戊偏财", "category": "财", "direction": "顺用", "status": "候选"
    }
    assert candidate["verified"] is False
    lines = FULLTEXT.read_text().splitlines()
    assert candidate["quote"] in lines[327]
    assert "財官印食，此用神之善而順用之者也" in lines[327]
    assert "透戊則用偏財" in lines[543]
    assert "兼透則兼用，透而又會，則透與會並用" in lines[547]

    original = next(rule for rule in json.loads(EXECUTABLE.read_text())["rules"] if rule["id"] == "ZPR-E-02")
    assert original["verified"] is False
    assert original["rescue"] == "unimplemented"
    assert "该路线自己的喜忌" in original["satisfy_when"]

    cases = json.loads(FIXTURE.read_text())["bazi"]
    evaluator = load_evaluator()
    expectations = {
        "caseP1_ZPR_01_wu_only": "满足",
        "caseP1_ZPR_01_wu_gui_both": "满足",
        "caseP1_ZPR_01_no_wu": "不满足",
        "caseP1_ZPR_02_shen_zi": "不满足",
    }
    for name, expected in expectations.items():
        assert "上海" in cases[name]["label"]
        got = evaluator.evaluate(candidate, cases[name]["facts"])["verdict"]
        assert got == expected, (name, got, expected)

    positive = cases["caseP1_ZPR_01_wu_only"]["facts"]
    assert evaluator.evaluate(candidate, without(positive, "gan", "year"))["verdict"] == "信息不足"
    assert evaluator.evaluate(candidate, without(positive, "canggan", "month"))["verdict"] == "信息不足"
    assert evaluator.evaluate(candidate, [f for f in positive if f["key"] not in {"geju", "shishen"}])["verdict"] == "满足"
    negative = cases["caseP1_ZPR_01_no_wu"]["facts"]
    assert evaluator.evaluate(candidate, without(negative, "gan", "year"))["verdict"] == "信息不足"
    print("ZPR-P1-03: source chain L328/L544/L548; four real charts; three missing-input projections; E-02 unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
