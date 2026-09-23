#!/usr/bin/env python3
"""Append the source-named 辛寅甲丙 two-entry case to the locked V5 handoff."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT.parent / "cosmic-fortune-lab"
BASE_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V5.json"
BASE_SHA = "7ea7b0214f1150c522273133febf3575f8821bc5fddd7c4d2cca1e3b2a36d802"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json"
SOURCE_RULES = "references/books/bazi/ziping-zhenquan/rules.yaml"
SOURCE_FULLTEXT = "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
SOURCE_VOCAB = "references/vocab/fact-vocab.json"
SOURCE_EVALUATOR = "tools/eval-predicates.py"
SOURCE_EXPORTER = "tools/export-rules.py"
FACT_FIXTURE = "tools/reports/facts-sample.json"
EXPORT_PATH = ROOT / "dist/rules/bazi.json"
RULE_ID = "ZPR-P1-06"
FACT_KEY = "natal_yin_simple_hidden_exposure_pattern"
DAY_SCOPE = {"layer": "本命", "pillar": "day"}
MONTH_SCOPE = {"layer": "本命", "pillar": "month"}
PROBES = {
    "positive": ("caseP1_ZPR_month_xin_jia_bing_1954", "满足"),
    "secondPositive": ("caseP1_ZPR_month_xin_jia_bing_1984", "满足"),
    "negative": ("caseP1_ZPR_month_xin_no_jia_1979", "不满足"),
    "tripleExposureUnknown": ("caseP1_ZPR_month_xin_jia_bing_wu_1984", "信息不足"),
    "meetingUnknown": ("caseP1_ZPR_month_xin_jia_bing_meeting_1994", "信息不足"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_bytes(rev: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], cwd=ROOT)


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def evaluation(evaluator, rule: dict, facts: list[dict], case: str) -> dict:
    result = evaluator.evaluate(rule, facts)
    return {
        "case": case,
        "factCount": len(facts),
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "factCoverage": result["fact_coverage"],
        "missingFactKeys": result["missing_fact_keys"],
    }


def minus_key(facts: list[dict], key: str) -> list[dict]:
    return [fact for fact in facts if fact.get("key") != key]


def make_manifest(source_rev: str, product_head: str, product_script_sha: str) -> dict:
    base_bytes = BASE_PATH.read_bytes()
    assert sha256(base_bytes) == BASE_SHA
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v5"
    assert len(base["rules"]) == 14 and base["semanticContractStatus"] == "pending"

    files = (SOURCE_RULES, SOURCE_FULLTEXT, SOURCE_VOCAB, SOURCE_EVALUATOR,
             SOURCE_EXPORTER, FACT_FIXTURE)
    committed = {path: committed_bytes(source_rev, path) for path in files}
    for path in files:
        if path == SOURCE_VOCAB:
            # A separate Liuren vocabulary edit is intentionally left dirty.
            current = json.loads((ROOT / path).read_text())
            pinned = json.loads(committed[path])
            assert current["values"][FACT_KEY] == pinned["values"][FACT_KEY]
            continue
        assert (ROOT / path).read_bytes() == committed[path], path
    fixture_sha = sha256(committed[FACT_FIXTURE])
    cases = json.loads(committed[FACT_FIXTURE])["bazi"]
    assert len(cases) == 50
    vocab = json.loads(committed[SOURCE_VOCAB])
    assert FACT_KEY in vocab["keys"]
    assert vocab["values"][FACT_KEY] == ["无", "甲", "丙", "戊", "甲丙", "甲戊", "丙戊"]

    source_rules = yaml.safe_load(committed[SOURCE_RULES])["rules"]
    matching = [rule for rule in source_rules if rule["rule_id"] == RULE_ID]
    assert len(matching) == 1
    source = matching[0]
    assert source["verified"] is False
    assert source["anchor"] == {"file": SOURCE_FULLTEXT, "start_line": 435, "end_line": 435}
    assert source["applicable_to"] == {"all_of": [
        {"key": "gan", "value": "辛", "scope": DAY_SCOPE},
        {"key": FACT_KEY, "value": "甲丙", "scope": MONTH_SCOPE},
    ]}
    lines = committed[SOURCE_FULLTEXT].decode().splitlines()
    assert source["quote"] in lines[434]
    supporting = [
        ("month_hidden_base", 419, "即以寅論，甲爲本主"),
        ("paired_relation_illustration", 452, "辛生寅月，甲丙並透，財與官相生，兩相得也"),
        ("coexisting_entry_boundary", 548, "兼透則兼用，透而又會，則透與會並用"),
    ]
    for _, line, quote in supporting:
        assert quote in lines[line - 1], (line, quote)
    outputs = source["source_entry_outputs"]
    assert len(outputs) == 2
    assert [(item["entryId"], item["sourceStem"], item["tenGod"], item["localRank"])
            for item in outputs] == [
        ("ZPR-E-02:month-寅:hidden-甲:辛日正财", "甲", "正财", "主"),
        ("ZPR-E-02:month-寅:hidden-丙:辛日正官", "丙", "正官", "兼"),
    ]

    evaluator = load_module(ROOT / SOURCE_EVALUATOR, "p1_v6_eval")
    exporter = load_module(ROOT / SOURCE_EXPORTER, "p1_v6_export")
    assert FACT_KEY in evaluator.SINGLE_VALUE_BAZI_FACT_KEYS
    assert FACT_KEY in evaluator.COMPLETE_PILLAR_FACT_KEYS
    exported = exporter.convert(source, art="bazi", title="子平真诠", slug_path="bazi/ziping-zhenquan")
    assert exported["applicableTo"] == source["applicable_to"]
    assert exported["sourceEntryOutputs"] == outputs
    export_bytes = EXPORT_PATH.read_bytes()
    matching_export = [entry for entry in json.loads(export_bytes) if entry["ruleId"] == RULE_ID]
    assert matching_export == [exported]

    results = {}
    for label, (case_id, verdict) in PROBES.items():
        result = evaluation(evaluator, source, cases[case_id]["facts"], case_id)
        assert result["verdict"] == verdict, result
        results[label] = result
    states = {state: 0 for state in ("满足", "不满足", "信息不足")}
    for case in cases.values():
        states[evaluator.evaluate(source, case["facts"])["verdict"]] += 1
    assert sum(states.values()) == 50 and states["满足"] == 2

    positive_facts = cases[PROBES["positive"][0]]["facts"]
    missing = evaluation(evaluator, source, minus_key(positive_facts, FACT_KEY), "positive_minus_simple_pattern")
    assert missing["verdict"] == "信息不足"
    conflict_facts = [*positive_facts, {"key": FACT_KEY, "value": "丙", "scope": MONTH_SCOPE}]
    conflict = evaluation(evaluator, source, conflict_facts, "positive_conflicting_simple_pattern")
    assert conflict["verdict"] == "信息不足"
    foreign_facts = [*minus_key(positive_facts, FACT_KEY),
                     {"key": FACT_KEY, "value": "甲丙", "scope": {"layer": "流年", "year": 2018}}]
    foreign = evaluation(evaluator, source, foreign_facts, "positive_foreign_layer_pattern")
    assert foreign["verdict"] == "信息不足"

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v6"
    manifest["generatedBy"] = "tools/generate-p1-bazi-v6-manifest.py"
    manifest["classicsRev"] = source_rev
    manifest["sourceHeadAtAudit"] = source_rev
    manifest["previousHandoff"] = {
        "path": str(BASE_PATH.relative_to(ROOT)), "sha256": BASE_SHA, "ruleCount": 14,
    }
    manifest["sourceFingerprint"].update({
        "zipingRulesYamlSha256": sha256(committed[SOURCE_RULES]),
        "zipingFulltextSha256": sha256(committed[SOURCE_FULLTEXT]),
        "exporterSha256": sha256(committed[SOURCE_EXPORTER]),
        "evaluatorSha256": sha256(committed[SOURCE_EVALUATOR]),
        "factVocabSha256": sha256(committed[SOURCE_VOCAB]),
    })
    manifest["factFixture"].update({"sha256": fixture_sha, "caseCount": len(cases)})
    manifest["factFixture"]["generator"].update({
        "repoHead": product_head,
        "scriptSha256": product_script_sha,
        "productFixtureSha256": fixture_sha,
        "workingTreeInputs": "Product 真实日期盘由脚本生成；以脚本指纹、50 盘 fixture 字节和本 sourceRev 锁定。",
    })
    manifest["factFixture"]["differenceFromClassicsHead"] = (
        "50 个八字样盘来自 Product 机械排盘；旧 43 盘除新增结构 Fact 外逐项不变。"
    )
    manifest["topics"]["overview"]["ruleIds"].append(RULE_ID)
    manifest["topics"]["overview"]["requiredFactKeys"].append(FACT_KEY)
    manifest["statusSummary"]["adopted"] = sorted([*base["statusSummary"]["adopted"], RULE_ID])
    manifest["rules"].append({
        "ruleId": RULE_ID,
        "art": "bazi",
        "book": "bazi/ziping-zhenquan",
        "primaryTopic": "overview",
        "secondaryTopics": [],
        "status": "adopted_as_provisional_evidence",
        "role": "source_entry_priority",
        "sourceRuleId": "ZPR-E-02",
        "statement": source["statement"],
        "quote": source["quote"],
        "anchor": {"file": SOURCE_FULLTEXT, "startLine": 435, "endLine": 435},
        "supportingSources": [
            {"role": role, "anchor": {"file": SOURCE_FULLTEXT, "startLine": line, "endLine": line},
             "quote": quote}
            for role, line, quote in supporting
        ],
        "sourceDisplayPolicy": "L435 单句只支持辛寅甲丙例型的局部主兼；L452 另支持财官相生的原文例型。两句均不证明任一真实盘的整盘成格、纯杂或实际作用。",
        "applicableTo": source["applicable_to"],
        "sourceEntryOutputs": outputs,
        "requiredFacts": [
            {"key": "gan", "scope": DAY_SCOPE, "predicateScope": [DAY_SCOPE]},
            {"key": FACT_KEY, "scope": MONTH_SCOPE, "predicateScope": [MONTH_SCOPE]},
        ],
        "factSlicePolicy": "只消费本命日干与完整寅月的清楚暴露形态；流年干和旧格局标签不参与。",
        "applicableLayers": ["本命"],
        "unsupportedLayers": ["大运", "流年", "流月", "流日"],
        "semantics": {
            "satisfied": "仅输出甲正财主、丙正官兼这两枚局部来源入口，不判整盘成败或作用。",
            "notSatisfied": "完整清楚形态已知但非辛日寅月甲丙并透；只否定本窄例型。",
            "unknown": "三枚月藏干同透、寅午戌全会、缺键、冲突或异层事实不能定本例型主兼。",
        },
        "caveats": source["caveats"],
        "exceptionsAndBreaks": source["caveats"],
        "conflictNotes": ["L435 不裁己日甲丙、丙戊兼透、三透或透而又会的整盘主兼；原 ZPR-E-02 仍未验收。"],
        "verification": {
            "verified": False,
            "fixtureSource": FACT_FIXTURE,
            **results,
            "missingStructuralFact": missing,
            "conflictingStructuralFact": conflict,
            "foreignLayerGuard": foreign,
            "allRealChartStates": states,
            "result": "50 个真实日期盘及缺键、冲突、异层门禁复核；仅为来源局部入口，不证明完整作用或现实准确率。",
        },
        "export": {"artifact": "dist/rules/bazi.json", "classicsRev": source_rev,
                   "sha256": sha256(export_bytes)},
    })
    assert manifest["rules"][:14] == base["rules"]
    assert len(manifest["rules"]) == 15
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-rev", required=True)
    parser.add_argument("--product-head", required=True)
    parser.add_argument("--product-script-sha", required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    manifest = make_manifest(args.source_rev, args.product_head, args.product_script_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {args.output} rules=15")


if __name__ == "__main__":
    main()
