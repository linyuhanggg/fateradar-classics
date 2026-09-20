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
ZW_BOOK = "ziwei/taiwei-fu"
ZW_YAML = ROOT / "references/books" / ZW_BOOK / "rules.yaml"


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
    zw_orig = ZW_YAML.read_text(encoding="utf-8")
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

        # reverse 4: heading quote → V13 FAIL
        old_q = (
            "八字用神，專求月令，以日干配月令地支，而生尅不同，格局分焉。"
            "財官印食，此用神之善而順用之者也；煞傷劫刃，此用神之不善而逆用之者也。"
            "當順而順，當逆而逆，配合得宜，皆爲貴格。"
        )
        heading = yaml_orig.replace(old_q, '"### 論用神"', 1)
        if heading == yaml_orig:
            fail("could not mutate heading quote")
        YAML.write_text(heading, encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        YAML.write_text(yaml_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        ids = [e.get("rule_id") for e in payload.get("errors") or []]
        if rc == 0 or "V13" not in codes:
            fail(f"heading quote should V13 FAIL, rc={rc} codes={codes} out={out[:800]}")
        if "ZPR-01" not in ids:
            fail(f"V13 should print ZPR-01, ids={ids}")
        print("reverse4 OK V13 heading quote")

        # reverse 5: blockquote prefix quote → V13 FAIL
        blockquote = yaml_orig.replace(old_q, '"> 清·金正音 辑录"', 1)
        if blockquote == yaml_orig:
            fail("could not mutate blockquote quote")
        YAML.write_text(blockquote, encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        YAML.write_text(yaml_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        ids = [e.get("rule_id") for e in payload.get("errors") or []]
        if rc == 0 or "V13" not in codes:
            fail(f"blockquote quote should V13 FAIL, rc={rc} codes={codes} out={out[:800]}")
        if "ZPR-01" not in ids:
            fail(f"V13 should print ZPR-01, ids={ids}")
        print("reverse5 OK V13 blockquote quote")

        # reverse 6: illegal ziwei palace → V15 FAIL
        needle = "  - key: ziwei_star\n    value: 天马\n"
        if zw_orig.count(needle) != 1:
            fail(f"expected unique 天马 predicate in {ZW_BOOK}, count={zw_orig.count(needle)}")
        illegal = zw_orig.replace(
            needle,
            "  - key: ziwei_star\n    value: 天马\n    scope:\n      palace: 伪宫名\n",
            1,
        )
        ZW_YAML.write_text(illegal, encoding="utf-8")
        rc, out = run_validate(["--book", ZW_BOOK, "--json"])
        ZW_YAML.write_text(zw_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        if rc == 0 or "V15" not in codes:
            fail(f"illegal palace should V15 FAIL, rc={rc} codes={codes} out={out[:800]}")
        print("reverse6 OK V15 illegal palace")

        # reverse 7..13：谓词语言 v3 的 V16 反例。用 YAML 流式写法注入，避开缩进陷阱。
        def expect_v16(tag: str, injected: str, *, want: str | None = None) -> None:
            body = yaml_orig.replace("applicable_to: []", "applicable_to: " + injected, 1)
            if body == yaml_orig:
                fail(f"{tag}: could not inject group form")
            YAML.write_text(body, encoding="utf-8")
            rc, out = run_validate(["--book", BOOK, "--json"])
            YAML.write_text(yaml_orig, encoding="utf-8")
            payload = json.loads(out[out.find("{") :]) if "{" in out else {}
            codes = [e.get("code") for e in payload.get("errors") or []]
            if rc == 0 or "V16" not in codes:
                fail(f"{tag}: should V16 FAIL, rc={rc} codes={codes} out={out[:800]}")
            if want and not any(want in (e.get("message") or "") for e in payload.get("errors") or []):
                fail(f"{tag}: V16 message should mention {want!r}, got {codes} {out[:800]}")
            print(f"{tag} OK V16")

        expect_v16(
            "reverse7",
            "{all_of: [{key: shishen, value: 七杀}], bogus_key: [{key: shishen, value: 正官}]}",
            want="未知组字段",
        )
        expect_v16(
            "reverse8",
            "{any_of: [{key: shishen, value: 七杀}], all_of: [{key: shishen, value: 正官}]}",
            want="恰好有一个",
        )
        expect_v16(
            "reverse9",
            "{any_of: [{key: shishen, value: 七杀}], same: palace}",
            want="只能出现在 all_of 内",
        )
        expect_v16(
            "reverse10",
            "{all_of: [{key: shishen, value: 七杀, scope: {gong: 3}}]}",
            want="scope.gong 仅奇门",
        )
        expect_v16(
            "reverse11",
            "{all_of: [{key: shishen, value: 七杀}, {key: shishen, value: 正官, scope: {yao: 9}}]}",
            want="scope.yao",
        )
        expect_v16(
            "reverse12",
            "{all_of: [{key: shishen, value: 七杀, scope: {pillar: 季}}]}",
            want="scope.pillar",
        )
        # 正例：合法 v3 组必须通过（否则门禁只是「一律拒绝」）
        good = yaml_orig.replace(
            "applicable_to: []",
            "applicable_to: "
            "{any_of: ["
            "{all_of: [{key: shishen, value: 七杀, scope: {pillar: month}}, "
            "{key: rizhu_strength, value: 偏弱}], same: palace}, "
            "{key: shishen, value: 正官}], "
            "none_of: [{key: kongwang, value: '*'}]}",
            1,
        )
        if good == yaml_orig:
            fail("could not inject legal v3 group")
        YAML.write_text(good, encoding="utf-8")
        rc, out = run_validate(["--book", BOOK, "--json"])
        YAML.write_text(yaml_orig, encoding="utf-8")
        payload = json.loads(out[out.find("{") :]) if "{" in out else {}
        codes = [e.get("code") for e in payload.get("errors") or []]
        if rc != 0 or codes:
            fail(f"legal v3 group should PASS, rc={rc} codes={codes} out={out[:800]}")
        print("reverse13 OK legal v3 group accepted")

        # reverse14：六壬 scope.palace 只接受课传位置（日上/辰上/初传/中传/末传）。
        LIUREN_BOOK = "san-shi/liuren-miben"
        LIUREN_YAML = ROOT / "references/books" / LIUREN_BOOK / "rules.yaml"
        lr_orig = LIUREN_YAML.read_text(encoding="utf-8")
        try:
            illegal_palace = lr_orig.replace(
                "applicable_to: []",
                "applicable_to: [{key: tianjiang, value: 青龙, scope: {palace: 伪位置}}]",
                1,
            )
            if illegal_palace == lr_orig:
                fail("reverse14: could not inject liuren palace")
            LIUREN_YAML.write_text(illegal_palace, encoding="utf-8")
            rc, out = run_validate(["--book", LIUREN_BOOK, "--json"])
            payload = json.loads(out[out.find("{") :]) if "{" in out else {}
            codes = [e.get("code") for e in payload.get("errors") or []]
            if rc == 0 or "V16" not in codes:
                fail(f"reverse14: illegal liuren palace should V16 FAIL, rc={rc} codes={codes}")
            # 正例：合法课传位置必须通过
            legal_palace = lr_orig.replace(
                "applicable_to: []",
                "applicable_to: [{key: tianjiang, value: 青龙, scope: {palace: 日上}}]",
                1,
            )
            LIUREN_YAML.write_text(legal_palace, encoding="utf-8")
            rc, out = run_validate(["--book", LIUREN_BOOK, "--json"])
            payload = json.loads(out[out.find("{") :]) if "{" in out else {}
            codes = [e.get("code") for e in payload.get("errors") or []]
            if rc != 0 or codes:
                fail(f"reverse14: legal liuren palace should PASS, rc={rc} codes={codes}")
        finally:
            LIUREN_YAML.write_text(lr_orig, encoding="utf-8")
        print("reverse14 OK V16 liuren palace (非法红／合法绿)")
    finally:
        YAML.write_text(yaml_orig, encoding="utf-8")
        FULLTEXT.write_text(ft_orig, encoding="utf-8")
        ZW_YAML.write_text(zw_orig, encoding="utf-8")
    print("ALL GATES OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
