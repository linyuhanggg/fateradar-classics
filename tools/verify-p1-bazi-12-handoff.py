#!/usr/bin/env python3
"""Verify the formal 12-rule P1 handoff and its locked 011A source shape."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate-p1-bazi-12-manifest.py"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923.json"
COMPANION_VERIFIER = ROOT / "tools/verify-sanming-011-literal-companion.py"
EXPECTED_ID = "SANMINGTONGH-P1-011A"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-product", action="store_true")
    parser.add_argument("--product-root", type=Path, default=Path("/Users/sync/code/cosmic-fortune-lab"))
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("p1_12_generator", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = (json.dumps(module.make_manifest(), ensure_ascii=False, indent=2) + "\n").encode()
    actual = MANIFEST.read_bytes()
    assert actual == expected, "v3 manifest differs from reproducible generator output"
    manifest = json.loads(actual)
    assert manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v3"
    assert manifest["semanticContractStatus"] == "pending"
    assert manifest["classicsRev"] == module.SOURCE_REV
    assert len(manifest["rules"]) == len({rule["ruleId"] for rule in manifest["rules"]}) == 12
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    old = json.loads(module.BASE_PATH.read_text())
    assert manifest["rules"][:11] == old["rules"]
    assert manifest["previousHandoff"]["sha256"] == module.BASE_SHA
    assert manifest["topics"]["overview"]["ruleIds"][-1] == EXPECTED_ID
    assert all(EXPECTED_ID not in item["ruleIds"] for name, item in manifest["topics"].items() if name != "overview")
    rule = manifest["rules"][-1]
    assert rule["ruleId"] == EXPECTED_ID and rule["sourceRuleId"] == "SANMINGTONGH-011"
    assert rule["applicableLayers"] == ["流年"] and rule["unsupportedLayers"] == ["本命", "大运", "流月", "流日"]
    assert rule["anchor"]["startLine"] == rule["anchor"]["endLine"] == 1084
    assert rule["quote"] in (ROOT / rule["anchor"]["file"]).read_text().splitlines()[1083]
    assert [item["key"] for item in rule["requiredFacts"]] == ["liunian_gan_zhi", "suiyun_binglin"]
    assert all(item["scope"] == {"layer": "流年", "year": "selected"} for item in rule["requiredFacts"])
    assert {key: rule["verification"][key]["verdict"] for key in ("positive", "negative", "boundary", "wrongYear")} == {
        "positive": "满足", "negative": "不满足", "boundary": "信息不足", "wrongYear": "不满足"
    }
    assert rule["verification"]["boundary"]["missingFactKeys"] == ["suiyun_binglin"]
    assert "选定" in rule["factSlicePolicy"]
    export = ROOT / rule["export"]["artifact"]
    assert export.exists(), "run python3 tools/export-rules.py first"
    assert hashlib.sha256(export.read_bytes()).hexdigest() == module.BAZI_EXPORT_SHA
    exported = json.loads(export.read_text())
    matching = [item for item in exported if item.get("ruleId") == EXPECTED_ID]
    assert len(matching) == 1
    assert matching[0]["quote"] == rule["quote"]
    assert matching[0]["anchor"] == rule["anchor"]
    assert matching[0]["applicableTo"] == rule["applicableTo"]

    command = ["python3", str(COMPANION_VERIFIER)]
    if args.replay_product:
        command += ["--replay-product", "--product-root", str(args.product_root)]
    subprocess.run(command, cwd=ROOT, check=True)
    print(f"PASS 12-rule handoff; sha256={hashlib.sha256(actual).hexdigest()}; classicsRev={module.SOURCE_REV}")


if __name__ == "__main__":
    main()
