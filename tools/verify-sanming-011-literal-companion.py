#!/usr/bin/env python3
"""Check the independent, literal 甲子/甲子 companion candidate for SMTH-011."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "tools/reports/p1-bazi-20260922/sanming-011-literal-companion-candidate.json"
PRODUCT_DEFAULT = Path("/Users/sync/code/cosmic-fortune-lab")
EXPECTED = {
    "literal_jiazi_positive": (1984, "甲子", "甲子", "是", "满足"),
    "literal_jiazi_wrong_luck": (1984, "甲子", "甲戌", "否", "不满足"),
    "literal_jiazi_no_active_luck": (1984, "甲子", None, "信息不足", "信息不足"),
    "literal_jiazi_prior_year": (1983, "癸亥", "甲子", "否", "不满足"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_facts(facts: list[dict], year: int) -> list[dict]:
    return [fact for fact in facts if fact.get("scope", {}).get("year") == year]


def one(facts: list[dict], key: str, layer: str, year: int) -> dict | None:
    matches = [fact for fact in facts if fact["key"] == key and fact.get("scope") == {"layer": layer, "year": year}]
    assert len(matches) <= 1, (key, layer, year)
    return matches[0] if matches else None


def replay_product(cases: dict, product_root: Path) -> None:
    assert product_root.is_dir(), product_root
    inputs = [{"id": case_id, **case["birth"], "selectedYear": case["selectedYear"]} for case_id, case in cases.items()]
    script = """
import { buildBazi } from './src/lib/engine/bazi';
const inputs = INPUTS;
const out = Object.fromEntries(inputs.map(input => {
  const birth = input;
  const subject = { ...birth, name: input.id, arts: ['bazi'],
    year: String(birth.year), month: String(birth.month), day: String(birth.day),
    hour: String(birth.hour), minute: String(birth.minute) };
  const chart = buildBazi(subject, input.selectedYear, undefined, { buildVertical: false });
  const active = chart.dayun.find(x => x.startYear <= input.selectedYear && input.selectedYear <= x.endYear);
  const facts = chart.facts.filter(f => f.scope?.year === input.selectedYear &&
    ['liunian_gan_zhi', 'dayun_gan_zhi', 'suiyun_binglin'].includes(f.key));
  return [input.id, { pillars: chart.ganzhi, qiyun: chart.meta.qiyun,
    activeLuck: active ? { ganzhi: active.ganzhi, startYear: active.startYear, endYear: active.endYear } : null,
    facts }];
}));
console.log(JSON.stringify(out));
""".replace("INPUTS", json.dumps(inputs, ensure_ascii=False))
    result = subprocess.run(
        ["bun", "-"], input=script, text=True, capture_output=True, cwd=product_root, check=True
    )
    observed = json.loads(result.stdout)
    for case_id, case in cases.items():
        for field in ("pillars", "qiyun", "activeLuck", "facts"):
            assert observed[case_id][field] == case[field], (case_id, field)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-product", action="store_true")
    parser.add_argument("--product-root", type=Path, default=PRODUCT_DEFAULT)
    args = parser.parse_args()

    manifest = json.loads(CANDIDATE.read_text())
    assert manifest["status"] == "candidate_only"
    base = manifest["baseHandoff"]
    base_path = ROOT / base["path"]
    assert sha256(base_path) == base["sha256"]
    locked = json.loads(base_path.read_text())
    assert len(locked["rules"]) == base["ruleCount"] == 11
    assert locked["semanticContractStatus"] == "pending"

    rule = manifest["rule"]
    assert rule["ruleId"] not in {entry["ruleId"] for entry in locked["rules"]}
    assert manifest["sourceRuleId"] == "SANMINGTONGH-011"
    assert rule["status"] == "candidate_only" and rule["verified"] is False
    assert rule["primaryTopic"] == "overview" and rule["secondaryTopics"] == []
    assert rule["role"] == "structural" and rule["applicableLayers"] == ["流年"]
    assert rule["anchor"]["startLine"] == rule["anchor"]["endLine"] == 1084
    source_line = (ROOT / rule["anchor"]["file"]).read_text().splitlines()[1083]
    assert rule["quote"] in source_line
    assert "甲子日見甲子太嵗" in source_line  # Adjacent clause must not be included in the predicate.
    assert rule["applicableTo"] == {"all_of": [
        {"key": "liunian_gan_zhi", "value": "甲子", "scope": {"layer": "流年"}},
        {"key": "suiyun_binglin", "value": "是", "scope": {"layer": "流年"}},
    ]}

    source_rules = yaml.safe_load((ROOT / "references/books/bazi/sanming-tonghui/rules.yaml").read_text())["rules"]
    original = next(item for item in source_rules if item["rule_id"] == "SANMINGTONGH-011")
    assert original["applicable_to"] == [] and original["verified"] is False
    assert rule["ruleId"] not in {item["rule_id"] for item in source_rules}

    fixture_ref = manifest["fixture"]
    fixture_path = ROOT / fixture_ref["path"]
    assert sha256(fixture_path) == fixture_ref["sha256"]
    cases = json.loads(fixture_path.read_text())["cases"]
    assert set(cases) == set(EXPECTED)

    spec = importlib.util.spec_from_file_location("predicate_evaluator", ROOT / "tools/eval-predicates.py")
    assert spec and spec.loader
    evaluator = importlib.util.module_from_spec(spec)
    sys.modules["predicate_evaluator"] = evaluator
    spec.loader.exec_module(evaluator)
    simple_rule = {"rule_id": rule["ruleId"], "book": rule["book"], "applicable_to": rule["applicableTo"], "verified": False}
    for case_id, (year, annual, luck, shape, verdict) in EXPECTED.items():
        case = cases[case_id]
        assert case["selectedYear"] == year
        assert case["birth"]["timeBasis"] == "clock"
        assert case["birth"]["city"] == "上海"
        facts = selected_facts(case["facts"], year)
        assert len(facts) == len(case["facts"]), case_id
        annual_fact = one(facts, "liunian_gan_zhi", "流年", year)
        luck_fact = one(facts, "dayun_gan_zhi", "大运", year)
        shape_fact = one(facts, "suiyun_binglin", "流年", year)
        assert annual_fact and annual_fact["value"] == annual and "liunian" in annual_fact["derivedFrom"]
        assert (luck_fact["value"] if luck_fact else None) == luck
        assert shape_fact and shape_fact["value"] == shape
        if luck_fact:
            assert "dayun.selected" in luck_fact["derivedFrom"]
            assert case["activeLuck"] and case["activeLuck"]["ganzhi"] == luck
            assert shape == ("是" if annual == luck else "否")
        else:
            assert case["activeLuck"] is None and shape == "信息不足"
        output = evaluator.evaluate(simple_rule, facts)
        assert output["verdict"] == verdict, (case_id, output)
        if verdict == "信息不足":
            assert output["missing_fact_keys"] == ["suiyun_binglin"]

    # No static predicate can express a dynamic selected year with these two
    # leaves. A foreign-year positive must be removed before evaluation.
    positive_shape = one(cases["literal_jiazi_positive"]["facts"], "suiyun_binglin", "流年", 1984)
    assert positive_shape
    foreign = {**positive_shape, "scope": {"layer": "流年", "year": 1983}}
    contaminated = cases["literal_jiazi_no_active_luck"]["facts"] + [foreign]
    assert evaluator.evaluate(simple_rule, contaminated)["verdict"] == "满足"
    assert evaluator.evaluate(simple_rule, selected_facts(contaminated, 1984))["verdict"] == "信息不足"

    if args.replay_product:
        replay_product(cases, args.product_root)
    print("PASS SANMINGTONGH-P1-011A literal companion: 4 real chart years, selected-year gate, 11-rule lock unchanged")


if __name__ == "__main__":
    main()
