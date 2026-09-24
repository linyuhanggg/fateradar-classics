#!/usr/bin/env python3
"""Derive the complete V9 P1 candidate from V7 and the pinned 097 source fix."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V7.json"
BASE_SHA = "f3d689cf0c24ca61685548ee4246461701bf1436191d3580c461a3c6e068f306"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V9.json"
SOURCE_REV = "f23b129"
OLD_SOURCE_REV = "4434c43e7c729c1547f49897bb227870b8d402a0"
SOURCE_PATH = "references/books/bazi/sanming-tonghui/rules.yaml"
FULLTEXT_PATH = "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
RULE_ID = "SANMINGTONGH-097"
FIXTURE_PATH = "tools/reports/facts-sample.json"
FIXTURE_SHA = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"
SOURCE_DELTA_PATH = "docs/closeout/SANMINGTONGH_097_SOURCE_HANDOFF_20260924.json"
SOURCE_DELTA_SHA = "7cdea905b3eb8236234fa3c87c5b2736790e5c3a7cf6ae562ea97a2f8f46a4a1"
FINGERPRINT_PATHS = {
    "zipingRulesYamlSha256": "references/books/bazi/ziping-zhenquan/rules.yaml",
    "zipingFulltextSha256": "sources/fulltext/bazi/ziping-zhenquan/fulltext.md",
    "ditiansuiRulesYamlSha256": "references/books/bazi/ditiansui-chanwei/rules.yaml",
    "ditiansuiFulltextSha256": "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md",
    "sanmingRulesYamlSha256": SOURCE_PATH,
    "sanmingFulltextSha256": FULLTEXT_PATH,
    "yuanhaiRulesYamlSha256": "references/books/bazi/yuanhai-ziping/rules.yaml",
    "yuanhaiFulltextSha256": "sources/fulltext/bazi/yuanhai-ziping/fulltext.md",
    "exporterSha256": "tools/export-rules.py",
    "evaluatorSha256": "tools/eval-predicates.py",
    "factVocabSha256": "references/vocab/fact-vocab.json",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(path: str, rev: str = SOURCE_REV) -> bytes:
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], cwd=ROOT)


def load_evaluator():
    path = ROOT / "tools/eval-predicates.py"
    assert path.read_bytes() == pinned("tools/eval-predicates.py")
    spec = importlib.util.spec_from_file_location("p1_v9_predicates", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evaluation(ev, rule: dict, facts: list[dict], case: str) -> dict:
    result = ev.evaluate(rule, facts)
    return {
        "case": case,
        "factCount": len(facts),
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "factCoverage": result["fact_coverage"],
        "missingFactKeys": result.get("missing_fact_keys", []),
    }


def build() -> dict:
    base_bytes = (ROOT / BASE_PATH).read_bytes()
    fixture_bytes = (ROOT / FIXTURE_PATH).read_bytes()
    assert sha(base_bytes) == BASE_SHA, "historical V7 manifest changed"
    assert sha(fixture_bytes) == FIXTURE_SHA, "50-case fixture changed"
    assert sha((ROOT / SOURCE_DELTA_PATH).read_bytes()) == SOURCE_DELTA_SHA, "097 source delta changed"
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v7"
    assert base["classicsRev"] == OLD_SOURCE_REV and len(base["rules"]) == 15
    assert base["semanticContractStatus"] == "pending"
    assert all(item["verification"]["verified"] is False for item in base["rules"])

    source_bytes = pinned(SOURCE_PATH)
    assert (ROOT / SOURCE_PATH).read_bytes() == source_bytes, "097 source differs from pinned commit"
    old_source = {item["rule_id"]: item for item in yaml.safe_load(pinned(SOURCE_PATH, OLD_SOURCE_REV))["rules"]}
    new_source = {item["rule_id"]: item for item in yaml.safe_load(source_bytes)["rules"]}
    assert set(old_source) == set(new_source)
    assert all(old_source[key] == value for key, value in new_source.items() if key != RULE_ID), (
        "another Sanming source rule changed since V7"
    )
    for key, path in FINGERPRINT_PATHS.items():
        current = pinned(path)
        if path != SOURCE_PATH:
            assert current == pinned(path, OLD_SOURCE_REV), f"V7 carryover source changed: {path}"
            assert sha(current) == base["sourceFingerprint"][key]
    fulltext = pinned(FULLTEXT_PATH).decode().splitlines()
    rule = new_source[RULE_ID]
    assert rule["verified"] is False
    assert rule["anchor"] == {"file": FULLTEXT_PATH, "start_line": 1761, "end_line": 1761}
    assert rule["quote"] in fulltext[1760]

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v9"
    manifest["generatedBy"] = "tools/generate-p1-bazi-v9-manifest.py"
    manifest["classicsRev"] = subprocess.check_output(
        ["git", "rev-parse", SOURCE_REV], cwd=ROOT, text=True
    ).strip()
    manifest["sourceHeadAtAudit"] = manifest["classicsRev"]
    manifest["sourceFingerprint"] = {key: sha(pinned(path)) for key, path in FINGERPRINT_PATHS.items()}
    manifest["previousHandoff"] = {"path": BASE_PATH, "sha256": BASE_SHA, "ruleCount": 15}
    manifest["handoffStatus"] = "candidate_pending_product_v9_import_and_remote_publication"
    manifest["priorScopeCorrection"] = manifest.pop("scopeCorrection")
    manifest["exportState"] = {
        "candidateOnly": True,
        "sourceRuleYamlChanged": True,
        "classicsDistChanged": False,
        "note": "097 is corrected in the pinned rules.yaml. Existing export metadata on other rules remains historical; 097 has no current dist export. Product V8 is unchanged.",
    }

    old_entry = next(item for item in base["rules"] if item["ruleId"] == RULE_ID)
    entry = next(item for item in manifest["rules"] if item["ruleId"] == RULE_ID)
    assert entry["primaryTopic"] == "personality" and entry["secondaryTopics"] == ["overview"]
    entry["primaryTopic"] = "overview"
    entry["secondaryTopics"] = []
    entry["statement"] = rule["statement"]
    entry["quote"] = rule["quote"]
    entry["anchor"] = {"file": FULLTEXT_PATH, "startLine": 1761, "endLine": 1761}
    entry["applicableTo"] = rule["applicable_to"]
    day_scope = {"layer": "本命", "pillar": "day"}
    entry["requiredFacts"] = [
        {"key": key, "scope": day_scope, "predicateScope": [day_scope]}
        for key in ("gan", "zhi")
    ]
    entry["semantics"] = {
        "satisfied": "本命日干、日支完整一致且同柱属于 L1761 八日名单；只识别名单，不推出性格或吉凶。",
        "notSatisfied": "本命日干、日支完整一致，但该日柱不在 L1761 八日名单；只否定此名单成员身份。",
        "unknown": "本命日干或日支缺失、同柱冲突或只有其它时间层事实时，保留信息不足。",
    }
    entry["caveats"] = rule["caveats"]
    entry["exceptionsAndBreaks"] = list(rule["caveats"])
    entry["conflictNotes"] = [
        "L1761 八日名单与 L9713 十二支干同类、L3808 四日专禄旺核心分别立论；不得混为同一谓词。"
    ]
    entry.pop("export", None)

    fixture = json.loads(fixture_bytes)["bazi"]
    assert len(fixture) == 50
    ev = load_evaluator()
    positive = fixture["cov1_bazi_3"]["facts"]
    negative = fixture["caseA"]["facts"]
    missing_day_branch = [
        fact for fact in positive
        if not (fact.get("key") == "zhi" and fact.get("scope") == day_scope)
    ]
    wrong_layer = [
        {"key": "gan", "value": "戊", "scope": {"layer": "流年", "pillar": "day"}},
        {"key": "zhi", "value": "戌", "scope": {"layer": "流年", "pillar": "day"}},
    ]
    conflicting_day_gan = [
        *positive,
        {"key": "gan", "value": "壬", "scope": day_scope},
    ]
    probes = {
        "positive": (positive, "cov1_bazi_3", "满足"),
        "negative": (negative, "caseA", "不满足"),
        "boundary": (missing_day_branch, "cov1_bazi_3_minus_natal_day_zhi", "信息不足"),
        "foreignLayerGuard": (wrong_layer, "synthetic_other_layer_only", "信息不足"),
        "conflictingNatalDayGan": (conflicting_day_gan, "cov1_bazi_3_conflicting_day_gan", "信息不足"),
    }
    results = {}
    for label, (facts, case, expected) in probes.items():
        result = evaluation(ev, rule, facts, case)
        assert result["verdict"] == expected, (label, result)
        results[label] = result
    counts = Counter(ev.evaluate(rule, case["facts"])["verdict"] for case in fixture.values())
    old_counts = Counter(
        ev.evaluate({"applicable_to": old_entry["applicableTo"]}, case["facts"])["verdict"]
        for case in fixture.values()
    )
    assert old_counts == {"满足": 12, "不满足": 38}
    assert counts == {"满足": 10, "不满足": 40}
    entry["verification"] = {
        "verified": False,
        "fixtureSource": FIXTURE_PATH,
        **results,
        "allRealChartStates": {state: counts[state] for state in ("满足", "不满足", "信息不足")},
        "result": "L1761 八日名单的三态样盘通过；不证明性格、关系、旺衰、吉凶或现实预测准确率。",
    }
    assert manifest["topics"]["overview"]["ruleIds"].count(RULE_ID) == 1
    assert manifest["topics"]["personality"]["ruleIds"].count(RULE_ID) == 1
    manifest["topics"]["personality"]["ruleIds"].remove(RULE_ID)
    manifest["topics"]["personality"]["blockers"] = [
        "现有性格主题规则尚无已接受的个人倾向作用合同；097 仅是 L1761 日柱名单，不支持性格归属。"
    ]
    manifest["sourceCorrection"] = {
        "ruleId": RULE_ID,
        "sourceRevision": manifest["classicsRev"],
        "sourceDelta": {"path": SOURCE_DELTA_PATH, "sha256": SOURCE_DELTA_SHA},
        "priorV7Counts": {state: old_counts[state] for state in ("满足", "不满足", "信息不足")},
        "candidateV9Counts": entry["verification"]["allRealChartStates"],
        "topicChange": "personality -> overview-only neutral structural evidence",
        "effectStatus": "no personality or other personal effect contract",
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify candidate bytes against pinned inputs")
    args = parser.parse_args()
    encoded = (json.dumps(build(), ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        assert OUTPUT.read_bytes() == encoded, "V9 candidate differs from pinned inputs"
        print(f"PASS V9 candidate sha256={sha(encoded)}")
    else:
        OUTPUT.write_bytes(encoded)
        print(f"Wrote {OUTPUT.relative_to(ROOT)} sha256={sha(encoded)}")


if __name__ == "__main__":
    main()
