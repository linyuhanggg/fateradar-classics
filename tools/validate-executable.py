#!/usr/bin/env python3
"""Validate executable-v2 source links; passing does not certify rule semantics."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "fateradar-executable-v2"
QUOTE_SEPARATOR = "\n[…]\n"
ARTS = {"bazi", "ziwei", "qimen", "liuren", "liuyao", "meihua", "xiaoliuren", "qizheng"}
TEXT_FIELDS = ("id", "art", "theme", "school", "page", "satisfy_when", "fail_when", "unknown_when", "rescue", "vernacular", "implementation_assumption")


def validate(root: Path) -> dict:
    errors: list[dict] = []
    rule_ids: set[str] = set()
    dependencies: list[tuple[str, str, str]] = []
    rule_count = source_count = 0
    files = sorted((root / "references/executable").glob("*.json"))

    def error(code: str, file: Path | str, rule: str, message: str) -> None:
        errors.append({"code": code, "file": str(file), "rule": rule, "message": message})

    if not files:
        error("FILES", "references/executable", "", "没有新格式规则文件")
    for path in files:
        rel = path.relative_to(root)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            error("JSON", rel, "", str(exc))
            continue
        if not isinstance(data, dict):
            error("SCHEMA", rel, "", "规则包必须是对象")
            continue
        if data.get("schema_version") != SCHEMA_VERSION:
            error("SCHEMA", rel, "", f"需要 {SCHEMA_VERSION}")
        if data.get("verified") is not False:
            error("VERIFIED", rel, "", "本批电子锚定规则没有人工影印核验，verified 必须为 false")
        book = data.get("book")
        if not isinstance(book, dict) or not all(isinstance(book.get(k), str) and book[k].strip() for k in ("slug", "system", "title", "fulltext")):
            error("BOOK", rel, "", "缺少书目或全文路径")
            continue
        try:
            ppath = root / "references/inventory/paragraphs" / book["system"] / f"{book['slug']}.json"
            inventory = json.loads(ppath.read_text(encoding="utf-8"))
            lines = (root / book["fulltext"]).read_text(encoding="utf-8").splitlines()
        except (OSError, ValueError) as exc:
            error("BOOK", rel, "", str(exc))
            continue
        if inventory.get("fulltext") != book["fulltext"]:
            error("BOOK", rel, "", "段落库与规则包不是同一份全文")
        paragraphs = {p["id"]: p for p in inventory["paragraphs"]}
        rules = data.get("rules")
        if not isinstance(rules, list) or not rules:
            error("RULES", rel, "", "rules 必须是非空数组")
            continue
        for rule in rules:
            rule_count += 1
            if not isinstance(rule, dict):
                error("FIELDS", rel, "", "规则必须是对象")
                continue
            rid = rule.get("id") if isinstance(rule.get("id"), str) else ""
            for key in TEXT_FIELDS:
                if not isinstance(rule.get(key), str) or not rule[key].strip():
                    error("FIELDS", rel, rid, f"{key} 必须是非空文本")
            if "chapter" in rule and (not isinstance(rule["chapter"], str) or not rule["chapter"].strip()):
                error("FIELDS", rel, rid, "显式 chapter 必须是已审读的非空章节说明")
            if rid in rule_ids:
                error("DUPLICATE_ID", rel, rid, "规则 ID 全库重复")
            rule_ids.add(rid)
            if rule.get("art") not in ARTS:
                error("FIELDS", rel, rid, "art 不在当前八术范围")
            if rule.get("verified") is not False:
                error("VERIFIED", rel, rid, "电子文本锚定不能自动提升 verified")
            if "paragraph_id" in rule:
                error("PARAGRAPH_ID", rel, rid, "跨段来源使用 paragraph_ids 与 sources，不能遗留旧单值字段")
            facts = rule.get("required_facts")
            if not isinstance(facts, list) or not facts or not all(isinstance(x, str) and x.strip() for x in facts):
                error("FIELDS", rel, rid, "required_facts 必须列出所需事实")
            if not isinstance(rule.get("when"), dict) or not rule["when"]:
                error("FIELDS", rel, rid, "when 必须说明适用范围")
            rescue = rule.get("rescue")
            # `none` 是第 29 批新增的取值：原文**根本没有**救应条款，本条没有可实现的救应。
            # 与 `unimplemented`（原文有救应条款、引擎尚未实现）分开，是因为把前者写成后者会把
            # 「无可实现」冒充成「待实现」，虚增未决清单。加入理由与逐条审计见
            # docs/closeout/RESCUE-LABEL-AUDIT-20260912.md。
            if isinstance(rescue, str) and rescue not in ("self", "unimplemented", "none"):
                dependencies.append((str(rel), rid, rescue))
            sources = rule.get("sources")
            if not isinstance(sources, list) or not sources:
                error("SOURCES", rel, rid, "至少需要一个来源摘录")
                continue
            expected_ids: list[str] = []
            quotes: list[str] = []
            for source in sources:
                source_count += 1
                if not isinstance(source, dict):
                    error("SOURCES", rel, rid, "来源摘录必须是对象")
                    continue
                pid = source.get("paragraph_id")
                if isinstance(pid, str) and pid not in expected_ids:
                    expected_ids.append(pid)
                paragraph = paragraphs.get(pid) if isinstance(pid, str) else None
                if paragraph is None:
                    error("PARAGRAPH_ID", rel, rid, f"段落不存在：{pid}")
                start, end = source.get("start_line"), source.get("end_line")
                quote = source.get("quote")
                if isinstance(quote, str):
                    quotes.append(quote)
                else:
                    error("QUOTE", rel, rid, "quote 必须是文本")
                if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
                    error("RANGE", rel, rid, "原文行范围无效")
                    continue
                if paragraph and not paragraph["start_line"] <= start <= end <= paragraph["end_line"]:
                    error("RANGE", rel, rid, f"L{start}-L{end} 超出段落 {pid}；跨段请拆开")
                if not isinstance(quote, str) or not quote.strip() or quote != "\n".join(lines[start - 1:end]):
                    error("QUOTE", rel, rid, f"L{start}-L{end} 摘录与电子原文不一致")
            if rule.get("paragraph_ids") != expected_ids:
                error("PARAGRAPH_IDS", rel, rid, "paragraph_ids 必须是 sources 中真实段落 ID 按顺序去重的列表")
            if rule.get("quote") != QUOTE_SEPARATOR.join(quotes):
                error("QUOTE_SUMMARY", rel, rid, "顶层 quote 必须由来源摘录用明确省略符连接，不可另行改写")
    for file, rid, target in dependencies:
        if target not in rule_ids:
            error("DEPENDENCY", file, rid, f"救应规则不存在：{target}")
    return {"ok": not errors, "files": len(files), "rules": rule_count, "source_spans": source_count, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["errors"]:
            print(f"{item['code']} {item['file']} {item['rule']}: {item['message']}")
        print(f"{'OK' if result['ok'] else 'FAIL'} {result['files']} packages, {result['rules']} source-linked rule records, {result['source_spans']} source spans")
        print("校验仅证明字段与电子文本来源相符，不证明算法完整或人工核验。")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
