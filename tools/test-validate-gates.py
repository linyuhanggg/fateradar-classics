#!/usr/bin/env python3
"""Reverse gates for validate-rules.py. Mutates nothing on success."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = "bazi/ziping-zhenquan"
YAML = ROOT / "references/books" / BOOK / "rules.yaml"
FULLTEXT = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"


def run_validate(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate-rules.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def fail(msg: str) -> None:
    print(f"GATE FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    yaml_orig = YAML.read_text(encoding="utf-8")
    ft_orig = FULLTEXT.read_text(encoding="utf-8")
    try:
        # reverse 1: wrong quote → V5 FAIL with rule_id
        mutated = yaml_orig.replace("專求月令", "專求月令X", 1)
        if mutated == yaml_orig:
            fail("could not mutate quote")
        YAML.write_text(mutated, encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        YAML.write_text(yaml_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        ids = [e.get("rule_id") for e in payload.get("errors") or []]
        if rc == 0 or "V5" not in codes:
            fail(f"wrong quote should V5 FAIL, rc={rc} codes={codes} out={out[:500]}")
        if "ZPR-01" not in ids:
            fail(f"V5 should print ZPR-01, ids={ids}")
        print("reverse1 OK V5 ZPR-01")

        # reverse 2: tweak fulltext → V4 FAIL
        lines = ft_orig.splitlines()
        if not lines:
            fail("empty fulltext")
        lines[0] = lines[0] + "X"
        FULLTEXT.write_text("\n".join(lines) + ("\n" if ft_orig.endswith("\n") else ""), encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        FULLTEXT.write_text(ft_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        if rc == 0 or "V4" not in codes:
            fail(f"fulltext tweak should V4 FAIL, rc={rc} codes={codes} out={out[:500]}")
        print("reverse2 OK V4 sha256")

        # reverse 3: fake FactKey → V7 FAIL
        fake = yaml_orig.replace(
            "applicable_to: []",
            "applicable_to:\n  - {key: not_a_fact_key, value: 七杀}",
            1,
        )
        if fake == yaml_orig:
            fail("could not inject fake key")
        YAML.write_text(fake, encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        YAML.write_text(yaml_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        if rc == 0 or "V7" not in codes:
            fail(f"fake key should V7 FAIL, rc={rc} codes={codes} out={out[:800]}")
        print("reverse3 OK V7 fake key")
    finally:
        YAML.write_text(yaml_orig, encoding="utf-8")
        FULLTEXT.write_text(ft_orig, encoding="utf-8")
    print("ALL GATES OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
