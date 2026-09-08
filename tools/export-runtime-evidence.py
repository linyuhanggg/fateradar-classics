#!/usr/bin/env python3
"""Export source-linked rule definitions, never chart-specific execution results."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote as url_quote

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_SPEC = importlib.util.spec_from_file_location("executable_validator", Path(__file__).with_name("validate-executable.py"))
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)


def build_export(root: Path, source_revision: str = "HEAD") -> dict:
    validation = VALIDATOR.validate(root)
    if not validation["ok"]:
        detail = "; ".join(f"{e['code']} {e['rule']}: {e['message']}" for e in validation["errors"][:8])
        raise ValueError(f"规则原文校验失败：{detail}")
    revision = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", f"{source_revision}^{{commit}}"], text=True,
    ).strip()
    originals: dict[str, list[str]] = {}
    rules = []
    for path in sorted((root / "references/executable").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        book = data["book"]
        file = book["fulltext"]
        if file not in originals:
            try:
                text = subprocess.check_output(
                    ["git", "-C", str(root), "show", f"{revision}:{file}"],
                    text=True, stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError as exc:
                raise ValueError(f"固定版本 {revision} 没有原文 {file}") from exc
            originals[file] = text.splitlines()
        lines = originals[file]
        for rule in data["rules"]:
            fragments = []
            chapters = []
            for source in rule["sources"]:
                start, end = source["start_line"], source["end_line"]
                text = "\n".join(lines[start - 1:end])
                if source["quote"] != text:
                    raise ValueError(f"固定版本 {revision} 原文与 {rule['id']} L{start}-L{end} 摘录不一致")
                headings = [re.sub(r"^#{1,6}\s+", "", line).strip() for line in lines[:start] if re.match(r"^#{1,6}\s+", line)]
                chapter = headings[-1] if headings else rule["theme"]
                if chapter not in chapters:
                    chapters.append(chapter)
                fragments.append({
                    "paragraphId": source["paragraph_id"], "file": file,
                    "startLine": start, "endLine": end, "quote": text,
                    "url": f"https://github.com/linyuhanggg/fateradar-classics/blob/{revision}/{url_quote(file, safe='/')}?plain=1#L{start}-L{end}",
                })
            rules.append({
                "id": rule["id"], "art": rule["art"], "theme": rule["theme"],
                "bookSlug": book["slug"], "book": book["title"], "chapter": rule.get("chapter") or " / ".join(chapters),
                "school": rule["school"], "page": rule["page"],
                "definitionFile": str(path.relative_to(root)),
                "quote": rule["quote"], "fragments": fragments,
                "requiredFacts": rule["required_facts"], "when": rule["when"],
                "conditionDescriptions": {
                    "satisfy": rule["satisfy_when"], "fail": rule["fail_when"], "unknown": rule["unknown_when"],
                },
                "implementationAssumption": rule["implementation_assumption"],
                "vernacularTemplate": rule["vernacular"], "verified": rule["verified"],
            })
    return {
        "version": 1, "kind": "source-linked-rule-definitions", "sourceRevision": revision,
        "note": "来源片段已核电子文本与固定提交；这些是规则定义，不是本盘命中或人工影印验证。运行适用性与计算结果必须由引擎另行提供。",
        "rules": rules,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--source-revision", default="HEAD")
    parser.add_argument("--art", choices=sorted(VALIDATOR.ARTS), help="Export only this art's source definitions")
    parser.add_argument("--output", type=Path, default=Path("dist/executable-evidence.json"))
    args = parser.parse_args()
    data = build_export(args.root, args.source_revision)
    if args.art:
        data["rules"] = [rule for rule in data["rules"] if rule["art"] == args.art]
    output = args.output if args.output.is_absolute() else args.root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    print(json.dumps({"rules": len(data["rules"]), "sourceRevision": data["sourceRevision"], "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
