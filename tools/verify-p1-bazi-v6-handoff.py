#!/usr/bin/env python3
"""Verify that V6 adds only the 辛寅甲丙 source pair to pinned V5."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate-p1-bazi-v6-manifest.py"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json"
RULE_ID = "ZPR-P1-06"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-product-fixture", action="store_true")
    parser.add_argument("--product-root", type=Path, default=Path("/Users/sync/code/cosmic-fortune-lab"))
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("p1_v6_generator", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual_bytes = MANIFEST.read_bytes()
    manifest = json.loads(actual_bytes)
    source_rev = manifest["classicsRev"]
    product_generator = manifest["factFixture"]["generator"]
    expected = module.make_manifest(
        source_rev, product_generator["repoHead"], product_generator["scriptSha256"]
    )
    expected_bytes = (json.dumps(expected, ensure_ascii=False, indent=2) + "\n").encode()
    assert actual_bytes == expected_bytes, "V6 differs from pinned source and fixture"
    base = json.loads(module.BASE_PATH.read_text())
    assert manifest["previousHandoff"] == {
        "path": str(module.BASE_PATH.relative_to(ROOT)),
        "sha256": module.BASE_SHA,
        "ruleCount": 14,
    }
    assert manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v6"
    assert manifest["semanticContractStatus"] == "pending"
    assert manifest["rules"][:14] == base["rules"]
    assert len(manifest["rules"]) == len({rule["ruleId"] for rule in manifest["rules"]}) == 15
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    assert manifest["topics"]["overview"]["ruleIds"] == [
        *base["topics"]["overview"]["ruleIds"], RULE_ID,
    ]
    assert all(manifest["topics"][name] == base["topics"][name]
               for name in base["topics"] if name != "overview")
    assert manifest["topics"]["overview"]["requiredFactKeys"] == [
        *base["topics"]["overview"]["requiredFactKeys"], module.FACT_KEY,
    ]

    entry = manifest["rules"][-1]
    assert entry["ruleId"] == RULE_ID and entry["sourceRuleId"] == "ZPR-E-02"
    assert entry["role"] == "source_entry_priority" and entry["primaryTopic"] == "overview"
    assert entry["secondaryTopics"] == [] and entry["applicableLayers"] == ["本命"]
    assert entry["unsupportedLayers"] == ["大运", "流年", "流月", "流日"]
    assert entry["applicableTo"] == {"all_of": [
        {"key": "gan", "value": "辛", "scope": module.DAY_SCOPE},
        {"key": module.FACT_KEY, "value": "甲丙", "scope": module.MONTH_SCOPE},
    ]}
    assert [item["key"] for item in entry["requiredFacts"]] == ["gan", module.FACT_KEY]
    assert [item["entryId"] for item in entry["sourceEntryOutputs"]] == [
        "ZPR-E-02:month-寅:hidden-甲:辛日正财",
        "ZPR-E-02:month-寅:hidden-丙:辛日正官",
    ]
    assert [(item["sourceStem"], item["tenGod"], item["localRank"], item["sourceLine"])
            for item in entry["sourceEntryOutputs"]] == [
        ("甲", "正财", "主", 435), ("丙", "正官", "兼", 435),
    ]
    assert "candidateOutput" not in entry and "candidateSources" not in entry
    assert [source["role"] for source in entry["supportingSources"]] == [
        "month_hidden_base", "paired_relation_illustration", "coexisting_entry_boundary",
    ]
    lines = (ROOT / module.SOURCE_FULLTEXT).read_text().splitlines()
    for source in entry["supportingSources"]:
        anchor = source["anchor"]
        assert source["quote"] in "\n".join(lines[anchor["startLine"] - 1:anchor["endLine"]])
    verdicts = {key: entry["verification"][key]["verdict"] for key in (
        "positive", "secondPositive", "negative", "tripleExposureUnknown",
        "meetingUnknown", "missingStructuralFact", "conflictingStructuralFact",
        "foreignLayerGuard",
    )}
    assert verdicts == {
        "positive": "满足", "secondPositive": "满足", "negative": "不满足",
        "tripleExposureUnknown": "信息不足", "meetingUnknown": "信息不足",
        "missingStructuralFact": "信息不足", "conflictingStructuralFact": "信息不足",
        "foreignLayerGuard": "信息不足",
    }
    assert entry["verification"]["allRealChartStates"] == {
        "满足": 2, "不满足": 44, "信息不足": 4,
    }
    original = next(rule for rule in json.loads((ROOT / "references/executable/ziping-zhenquan.json").read_text())["rules"]
                    if rule["id"] == "ZPR-E-02")
    assert original["rescue"] == "unimplemented" and original["verified"] is False

    if args.compare_product_fixture:
        product = args.product_root / "tests/fixtures/facts-sample.json"
        assert product.read_bytes() == (ROOT / module.FACT_FIXTURE).read_bytes()

    print(
        f"PASS 15-rule V6 handoff; sha256={hashlib.sha256(actual_bytes).hexdigest()}; "
        f"classicsRev={source_rev}; fixtureSha256={manifest['factFixture']['sha256']}"
    )


if __name__ == "__main__":
    main()
