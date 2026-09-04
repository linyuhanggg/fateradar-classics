#!/usr/bin/env python3
"""Wrap remaining fulltext lines with >120 han chars, remap anchors, freeze sha256.

Reuses wrap/find helpers from p4-normalize.py. Does not change V1–V12 criteria.
Does not fetch any remote text. qimen-faqiao is only line-wrapped in the existing
MIT excerpt already in-tree — no publisher edition is retrieved.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[㐀-鿿]")
FAQIAO = "san-shi/qimen-faqiao"


def load_p4():
    path = ROOT / "tools/p4-normalize.py"
    spec = importlib.util.spec_from_file_location("p4_normalize", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def han_count(text: str) -> int:
    return len(HAN_RE.findall(text or ""))


def v12_count(text: str) -> int:
    n = 0
    for line in text.splitlines():
        if "|" in line:
            continue
        if han_count(line) > 120:
            n += 1
    return n


def iter_books():
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        key = path.parent.relative_to(ROOT / "references/books").as_posix()
        yield path, key, book, data


def replace_anchor_block(text: str, rule_id: str, start: int | None, end: int | None, file_path: str) -> str:
    """Replace the anchor field of one rule. start is None → anchor: null."""
    lines = text.splitlines()
    pat = re.compile(rf"^- rule_id:\s*{re.escape(rule_id)}\s*$")
    start_i = None
    for i, line in enumerate(lines):
        if pat.match(line):
            start_i = i
            break
    if start_i is None:
        return text
    end_i = len(lines)
    for j in range(start_i + 1, len(lines)):
        if lines[j].startswith("- rule_id:"):
            end_i = j
            break
    block = lines[start_i:end_i]
    a0 = None
    a1 = None
    for k, line in enumerate(block):
        if re.match(r"  anchor:\s*$", line) or re.match(r"  anchor:\s+null\s*$", line):
            a0 = k
            if line.strip() == "anchor: null":
                a1 = k + 1
            else:
                a1 = k + 1
                while a1 < len(block) and (block[a1].startswith("    ") or block[a1].strip() == ""):
                    if block[a1].strip() == "":
                        break
                    a1 += 1
            break
        if re.match(r"  anchor:\s+null\s*$", line):
            a0 = k
            a1 = k + 1
            break
    if a0 is None:
        return text
    if start is None or end is None:
        new = ["  anchor: null"]
    else:
        new = [
            "  anchor:",
            f"    file: {file_path}",
            f"    start_line: {start}",
            f"    end_line: {end}",
        ]
    block[a0:a1] = new
    lines[start_i:end_i] = block
    return "\n".join(lines) + "\n"


def patch_sha256(text: str, digest: str) -> str:
    new, n = re.subn(r"(fulltext_sha256:\s*)[0-9a-f]{64}", lambda m: m.group(1) + digest, text, count=1)
    if n != 1:
        raise RuntimeError("sha256 field not patched")
    return new


def main() -> int:
    p4 = load_p4()
    changed: list[str] = []
    leftover_total = 0
    for yaml_path, key, book, data in iter_books():
        ft_rel = book.get("fulltext")
        if not isinstance(ft_rel, str):
            continue
        ft = ROOT / ft_rel
        if not ft.is_file():
            print(f"skip missing fulltext {key} {ft_rel}")
            continue
        before = v12_count(ft.read_text(encoding="utf-8"))
        if before == 0:
            continue
        print(f"wrap {key} v12_before={before}")
        if ft_rel.startswith("sources/fulltext/"):
            p4.wrap_book(key)
        else:
            text = ft.read_text(encoding="utf-8")
            out: list[str] = []
            for line in text.splitlines():
                out.extend(p4.wrap_line(line))
            ft.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
            print(f"wrap excerpt {key}")
        after = v12_count(ft.read_text(encoding="utf-8"))
        leftover_total += after
        changed.append(key)

    print(f"wrapped {len(changed)} books leftover_v12={leftover_total}")

    misses: list[dict] = []
    rewritten = 0
    ok = 0
    nulled = 0
    for yaml_path, key, book, data in iter_books():
        ft_rel = book.get("fulltext")
        if not isinstance(ft_rel, str):
            continue
        ft = ROOT / ft_rel
        if not ft.is_file():
            continue
        digest = hashlib.sha256(ft.read_bytes()).hexdigest()
        text = yaml_path.read_text(encoding="utf-8")
        orig = text
        if book.get("fulltext_sha256") != digest:
            text = patch_sha256(text, digest)
        lines = ft.read_text(encoding="utf-8").splitlines()
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            rid = str(rule.get("rule_id") or "")
            anchor = rule.get("anchor")
            if not isinstance(anchor, dict):
                continue
            found = p4.find_quote(lines, rule.get("quote") or "")
            if found is None:
                text = replace_anchor_block(text, rid, None, None, ft_rel)
                nulled += 1
                misses.append({"book": key, "rule_id": rid, "reason": "quote not in fulltext after wrap"})
            else:
                start, end = found
                old_s, old_e = anchor.get("start_line"), anchor.get("end_line")
                if (start, end) != (old_s, old_e):
                    text = replace_anchor_block(text, rid, start, end, ft_rel)
                ok += 1
        if text != orig:
            yaml_path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            rewritten += 1

    report_dir = ROOT / "tools/reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "anchor-mismatch.json").write_text(
        __import__("json").dumps(misses, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"remap ok={ok} nulled={nulled} yaml_rewritten={rewritten} mismatch={len(misses)}")
    print("changed", changed)
    return 0 if leftover_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
