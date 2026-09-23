#!/usr/bin/env python3
"""Extend locked P1 v4 with the narrow ZPR single-qi month officer entrance."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V4.json"
BASE_SHA = "4429116dfd1aef1287406594d8fc80aa41e3fa1eda71235403ed1fcb94c76fda"
SOURCE_REV = "b5fdef36dff2b9c3d82d97ac38a6fb26f0f83df5"
SOURCE_RULES = "references/books/bazi/ziping-zhenquan/rules.yaml"
SOURCE_FULLTEXT = "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
SOURCE_VOCAB = "references/vocab/fact-vocab.json"
SOURCE_EVALUATOR = "tools/eval-predicates.py"
FACT_FIXTURE = ROOT / "tools/reports/facts-sample.json"
FACT_SHA = "3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc"
EXPORT_PATH = ROOT / "dist/rules/bazi.json"
EXPORT_SHA = "489073b00238bbb035e649c54878e7bf15d698b590244b1bc1bce96cddbab1d8"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V5.json"
RULE_ID = "ZPR-P1-04"
FACT_KEY = "natal_month_single_qi_hidden_stem"
FACT_SCOPE = {"layer": "本命", "pillar": "month"}
DAY_SCOPE = {"layer": "本命", "pillar": "day"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{SOURCE_REV}:{path}"], cwd=ROOT)


def evaluation(evaluator, rule: dict, case: dict, label: str) -> dict:
    facts = case["facts"]
    result = evaluator.evaluate(rule, facts)
    return {
        "case": label,
        "factCount": len(facts),
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "factCoverage": result["fact_coverage"],
        "missingFactKeys": result["missing_fact_keys"],
    }


def make_manifest() -> dict:
    base_bytes = BASE_PATH.read_bytes()
    assert sha256(base_bytes) == BASE_SHA
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v4"
    assert base["semanticContractStatus"] == "pending" and len(base["rules"]) == 13

    rule_bytes = committed_bytes(SOURCE_RULES)
    evaluator_bytes = committed_bytes(SOURCE_EVALUATOR)
    fixture_bytes = committed_bytes("tools/reports/facts-sample.json")
    vocab_bytes = committed_bytes(SOURCE_VOCAB)
    # V5 is a historical handoff. Later source rules and shared fixture may
    # advance; replay its own pinned revision instead of requiring HEAD to
    # remain byte-identical to the old source commit.
    assert sha256(fixture_bytes) == FACT_SHA
    vocab = json.loads(vocab_bytes)
    assert FACT_KEY in vocab["keys"]
    assert vocab["values"][FACT_KEY] == list("甲乙丙丁戊己庚辛壬癸")
    # Other work on the shared vocabulary may be dirty; source revision is the lock.
    working_vocab = json.loads((ROOT / SOURCE_VOCAB).read_text())
    assert working_vocab["values"][FACT_KEY] == vocab["values"][FACT_KEY]

    source_rules = yaml.safe_load(rule_bytes)["rules"]
    matching = [rule for rule in source_rules if rule["rule_id"] == RULE_ID]
    assert len(matching) == 1
    source = matching[0]
    assert source["verified"] is False
    assert source["anchor"] == {"file": SOURCE_FULLTEXT, "start_line": 328, "end_line": 328}
    assert source["quote"] in (ROOT / SOURCE_FULLTEXT).read_text().splitlines()[327]
    source_lines = (ROOT / SOURCE_FULLTEXT).read_text().splitlines()
    supporting = [
        ("officer_killer_mapping", 146, 149, "甲以庚爲煞，以辛爲官"),
        ("single_qi_boundary", 419, 419, "除子午卯酉外，餘皆有藏"),
        ("jia_you_officer_example", 468, 468, "甲透酉官"),
        ("bing_zi_officer_example", 470, 470, "丙生子月，癸水透"),
    ]
    for _, start, end, quote in supporting:
        assert quote in "\n".join(source_lines[start - 1:end]), (start, quote)
    assert len(source["applicable_to"]["any_of"]) == 10
    assert all(branch["all_of"][0]["key"] == "gan"
               and branch["all_of"][0]["scope"] == DAY_SCOPE
               and branch["all_of"][1]["key"] == FACT_KEY
               and branch["all_of"][1]["scope"] == FACT_SCOPE
               for branch in source["applicable_to"]["any_of"])

    current_export = json.loads(EXPORT_PATH.read_bytes())
    # V6 adds exactly P1-06. Removing that one later rule reconstructs the V5
    # export byte-for-byte; the fixed SHA below proves no older entry drifted.
    historical_export = [rule for rule in current_export if rule["ruleId"] != "ZPR-P1-06"]
    export_bytes = (json.dumps(historical_export, ensure_ascii=False, indent=2) + "\n").encode()
    assert sha256(export_bytes) == EXPORT_SHA
    export = json.loads(export_bytes)
    exported = [rule for rule in export if rule["ruleId"] == RULE_ID]
    assert len(exported) == 1
    assert exported[0]["statement"] == source["statement"]
    assert exported[0]["quote"] == source["quote"]
    assert exported[0]["applicableTo"] == source["applicable_to"]
    previous_export = [rule for rule in export if rule["ruleId"] != RULE_ID]
    old_export_sha = sha256((json.dumps(previous_export, ensure_ascii=False, indent=2) + "\n").encode())
    assert old_export_sha == base["rules"][-1]["export"]["sha256"]
    assert len(previous_export) == 451 and len(export) == 452

    evaluator = types.ModuleType("zpr_p1_evaluator")
    evaluator.__file__ = str(ROOT / SOURCE_EVALUATOR)
    sys.modules["zpr_p1_evaluator"] = evaluator
    exec(compile(evaluator_bytes, evaluator.__file__, "exec"), evaluator.__dict__)
    assert FACT_KEY in evaluator.SINGLE_VALUE_BAZI_FACT_KEYS
    cases = json.loads(fixture_bytes)["bazi"]
    assert len(cases) == 43
    probes = {
        "positive": ("caseP1_010_luck_gui_only", "满足"),
        "negative": ("cov2_bazi_3", "不满足"),
        "unknown": ("caseB", "信息不足"),
    }
    results = {}
    states = {state: 0 for state in ("满足", "不满足", "信息不足")}
    for case_id, case in cases.items():
        states[evaluator.evaluate(source, case["facts"])["verdict"]] += 1
    assert states == {"满足": 4, "不满足": 7, "信息不足": 32}
    for label, (case_id, expected) in probes.items():
        result = evaluation(evaluator, source, cases[case_id], case_id)
        assert result["verdict"] == expected, result
        results[label] = result

    positive = cases["caseP1_010_luck_gui_only"]
    missing = {"facts": [fact for fact in positive["facts"] if fact.get("key") != FACT_KEY]}
    boundary = evaluation(evaluator, source, missing, "caseP1_010_luck_gui_only_minus_single_qi_fact")
    assert boundary["verdict"] == "信息不足" and boundary["missingFactKeys"] == [FACT_KEY]
    conflict = copy.deepcopy(positive)
    conflict["facts"].append({"key": FACT_KEY, "value": "癸", "scope": FACT_SCOPE})
    conflict_result = evaluation(evaluator, source, conflict, "caseP1_010_luck_gui_only_conflicting_single_qi_fact")
    assert conflict_result["verdict"] == "信息不足"
    foreign = copy.deepcopy(missing)
    foreign["facts"].append({"key": FACT_KEY, "value": "辛", "scope": {"layer": "流年", "year": 2018}})
    foreign_result = evaluation(evaluator, source, foreign, "caseP1_010_luck_gui_only_foreign_layer_fact")
    assert foreign_result["verdict"] == "信息不足"

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v5"
    manifest["generatedBy"] = "tools/generate-p1-bazi-14-manifest.py"
    manifest["classicsRev"] = SOURCE_REV
    manifest["sourceHeadAtAudit"] = SOURCE_REV
    manifest["previousHandoff"] = {"path": str(BASE_PATH.relative_to(ROOT)), "sha256": BASE_SHA, "ruleCount": 13}
    manifest["sourceFingerprint"]["zipingRulesYamlSha256"] = sha256(rule_bytes)
    manifest["sourceFingerprint"]["evaluatorSha256"] = sha256(evaluator_bytes)
    manifest["sourceFingerprint"]["factVocabSha256"] = sha256(vocab_bytes)
    manifest["factFixture"]["sha256"] = FACT_SHA
    manifest["factFixture"]["generator"]["productFixtureSha256"] = FACT_SHA
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
        "role": "structural",
        "sourceRuleId": "ZPR-E-02",
        "statement": source["statement"],
        "quote": source["quote"],
        "anchor": {"file": SOURCE_FULLTEXT, "startLine": 328, "endLine": 328},
        "supportingSources": [
            {
                "role": role,
                "anchor": {"file": SOURCE_FULLTEXT, "startLine": start, "endLine": end},
                "quote": quote,
            }
            for role, start, end, quote in supporting
        ],
        "sourceDisplayPolicy": "主 quote 仅 L328 月令配日干；十干正官分类及单气边界需并列展示 supportingSources。Product generated bazi.json 当前仅有主锚，若界面不读取 handoff 附锚，不得把单句显示为完整出处。",
        "applicableTo": source["applicable_to"],
        "requiredFacts": [
            {"key": "gan", "scope": DAY_SCOPE, "predicateScope": [DAY_SCOPE] * 10},
            {"key": FACT_KEY, "scope": FACT_SCOPE, "predicateScope": [FACT_SCOPE] * 10},
        ],
        "factSlicePolicy": "只取本命日干和本命月柱结构键；岁运、格局标签和作用结果不能补本命月令缺项。",
        "applicableLayers": ["本命"],
        "unsupportedLayers": ["大运", "流年", "流月", "流日"],
        "semantics": {
            "satisfied": "只确认单气月支的正官原始入口；不判主格、顺用作用、救应或吉凶。",
            "notSatisfied": "完整单气月支已知但其唯一藏干不是该日干正官干；仅否定本窄入口。",
            "unknown": "结构键或日干缺失、冲突、多藏、月令与月支不一致时为信息不足；不得否定其它入口。",
        },
        "caveats": source["caveats"],
        "exceptionsAndBreaks": source["caveats"],
        "conflictNotes": ["ZPR-E-02 的完整正官格、顺用作用和救应尚未裁决；本条满足不升级整条 E-02。"],
        "verification": {
            "verified": False,
            "fixtureSource": str(FACT_FIXTURE.relative_to(ROOT)),
            **results,
            "missingStructuralFact": boundary,
            "conflictingStructuralFact": conflict_result,
            "foreignLayerGuard": foreign_result,
            "allRealChartStates": states,
            "result": "43 个真实日期盘及缺值、冲突、异层污染门禁通过；只证明来源窄入口三态，不证明完整作用或现实准确率。",
        },
        "export": {"artifact": "dist/rules/bazi.json", "classicsRev": SOURCE_REV, "sha256": EXPORT_SHA},
    })
    assert manifest["rules"][:13] == base["rules"]
    assert len(manifest["rules"]) == 14
    assert all(entry["verification"]["verified"] is False for entry in manifest["rules"])
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    manifest = make_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {args.output} rules=14")


if __name__ == "__main__":
    main()
