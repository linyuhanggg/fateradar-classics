#!/usr/bin/env python3
"""One-shot: convert existing rules.md packs into fateradar-rules-v1 YAML.

Does not invent new rule content. verified is always false.
Anchor is kept only when a quote can be taken from the line range.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_TERMS = Path("/Users/sync/code/cosmic-fortune-lab/src/lib/rules/terms.ts")
SCHEMA_VERSION = "fateradar-rules-v1"
VOCAB_SCHEMA = "fateradar-vocab-v1"
SEED_TERMS = [
    {"canonical": "月令", "aliases": ["提纲", "月建"], "kind": "bazi-structure"},
    {"canonical": "格局", "aliases": [], "kind": "bazi-structure"},
    {"canonical": "用神", "aliases": [], "kind": "bazi-structure"},
]
SKIP_HEADINGS = {
    "通用",
    "全书规则统计",
    "rule",
    "rules",
    "总计",
    "现代使用边界",
    "safety-redlines",
    "safety-redlines（最高级）",
    "reframe",
}

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$")
FIELD_RE = re.compile(r"^-\s+\*\*([^*]+)\*\*\s*[:：]?\s*(.*)$")
ID_TITLE_RE = re.compile(
    r"^`?([A-Za-z][A-Za-z0-9._/-]*)`?\s*[—–:：\-]\s*(.*)$"
)
ID_SPACE_RE = re.compile(r"^`?([A-Za-z][A-Za-z0-9._/-]*)`?(?:\s+|$)(.*)$")
ANCHOR_RANGE_RE = re.compile(
    r"(?:fulltext\.md\s*)?L\s*(\d+)\s*(?:[-–—]\s*L?\s*(\d+))?",
    re.IGNORECASE,
)
TERM_RE = re.compile(
    r'\{\s*canonical:\s*"([^"]+)",\s*kind:\s*"([^"]+)",\s*aliases:\s*\[([^\]]*)\]\s*\}'
)
WS_RE = re.compile(r"\s+", re.UNICODE)


def collapse(text: str) -> str:
    return WS_RE.sub("", text or "")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def book_code(slug: str) -> str:
    return slug.replace("-", "")[:12].upper()


def split_tags(raw: str) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"[；;、|/，]|, ", raw)
    out: list[str] = []
    seen: set[str] = set()
    for part in parts:
        tag = part.strip().strip("`").strip()
        if not tag or tag in seen:
            continue
        if len(tag) > 12:
            continue
        if " " in tag or "的" in tag:
            continue
        if tag in {"—", "-", "n/a", "NA"}:
            continue
        seen.add(tag)
        out.append(tag)
    return out


def parse_md_tables(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and re.search(r"^\|?\s*:?-+\s*\|", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cols = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if cols and not set("".join(cols)) <= set("-: "):
                    row = {}
                    for key, val in zip(header, cols):
                        row[key.strip().lower()] = val
                    rows.append(row)
                i += 1
            continue
        i += 1
    return rows


def parse_field_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    pending_key: str | None = None
    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            if current and (current.get("statement") or current.get("rule_id")):
                blocks.append(current)
            title = heading.group(2).strip()
            current = {"_heading": title}
            pending_key = None
            ident, rest = split_id_title(title)
            if ident:
                current["rule_id"] = ident
                if rest:
                    current["_title"] = rest
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            key = field.group(1).strip()
            val = field.group(2).strip()
            current[key] = val
            pending_key = key
            continue
        if pending_key and (line.startswith("  ") or line.startswith("\t")):
            extra = line.strip()
            if extra:
                current[pending_key] = (current.get(pending_key, "") + " " + extra).strip()
            continue
        pending_key = None
    if current and (current.get("statement") or current.get("rule_id") or current.get("rule")):
        blocks.append(current)
    return blocks


def split_id_title(heading: str) -> tuple[str | None, str]:
    heading = heading.strip()
    low = heading.split("（")[0].strip().lower()
    if low in SKIP_HEADINGS or heading.startswith("现代使用") or "统计" in heading:
        return None, heading
    m = ID_TITLE_RE.match(heading)
    if m:
        return m.group(1), m.group(2).strip()
    m = ID_SPACE_RE.match(heading)
    if m and re.search(r"\d", m.group(1)):
        return m.group(1), m.group(2).strip()
    return None, heading


def first_present(block: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        val = block.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def parse_anchor(raw: str) -> tuple[int, int] | None:
    if not raw:
        return None
    matches = list(ANCHOR_RANGE_RE.finditer(raw))
    if not matches:
        return None
    start = int(matches[0].group(1))
    end = int(matches[0].group(2) or start)
    if end < start:
        start, end = end, start
    return start, end


def pick_quote(lines: list[str], start: int, end: int) -> str:
    window = lines[start - 1 : end]
    candidates: list[str] = []
    for line in window:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith("- source") or s.startswith("source_url"):
            continue
        if s.startswith("http"):
            continue
        if re.match(r"^(秘本|欽定四庫全書|钦定|卷[一二三四五六七八九十百]+)", s):
            continue
        if "【" in s:
            s = re.sub(r"【.*?】", "", s).strip()
            if not s:
                continue
        if len(s) < 8:
            continue
        candidates.append(s)
    if not candidates:
        return ""
    return candidates[0]


def load_catalog() -> list[dict]:
    raw = json.loads((ROOT / "references/catalog/catalog.json").read_text(encoding="utf-8"))
    return raw["ready_reference_packs"]


def fulltext_for(system: str, slug: str) -> Path | None:
    primary = ROOT / "sources/fulltext" / system / slug / "fulltext.md"
    if primary.is_file():
        return primary
    excerpt = ROOT / "sources/excerpts/qimen-faqiao-chaibu-v1.md"
    if slug == "qimen-faqiao" and excerpt.is_file():
        return excerpt
    return None


def load_product_terms() -> list[dict]:
    terms: list[dict] = []
    if not PRODUCT_TERMS.is_file():
        return terms
    text = PRODUCT_TERMS.read_text(encoding="utf-8")
    for canonical, kind, alias_blob in TERM_RE.findall(text):
        aliases = [a.strip().strip('"') for a in alias_blob.split(",") if a.strip().strip('"')]
        terms.append({"canonical": canonical, "kind": kind, "aliases": aliases})
    return terms


def statement_of(block: dict[str, str]) -> str:
    text = first_present(
        block,
        [
            "statement",
            "rule",
            "rule_statement",
            "plain_language_rule",
            "conclusion",
            "preconditions",
            "decision_effect",
            "_title",
        ],
    )
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 200:
        text = text[:200]
    return text


def caveats_of(block: dict[str, str]) -> list[str]:
    raw = first_present(block, ["caveats", "safety", "stop_or_exception", "conflicts", "exceptions"])
    if not raw:
        return []
    parts = re.split(r"[；;。]", raw)
    out = [p.strip() for p in parts if p.strip()]
    return out[:8]


def applicable_of(block: dict[str, str]) -> list[str]:
    raw = first_present(block, ["applicable_to"])
    tags = split_tags(raw)
    return tags


def collect_blocks(rules_md: Path) -> list[dict[str, str]]:
    text = rules_md.read_text(encoding="utf-8")
    blocks = parse_field_blocks(text)
    for row in parse_md_tables(text):
        block = {k: v for k, v in row.items() if v}
        ident = block.get("id") or block.get("rule_id") or block.get("ruleid")
        if ident:
            block["rule_id"] = ident
        if "rule" in block and "statement" not in block:
            block["statement"] = block["rule"]
        if "title" in block and "_title" not in block:
            block["_title"] = block["title"]
        if ident or block.get("statement") or block.get("rule"):
            blocks.append(block)
    return blocks


def uniquify(preferred: str | None, code: str, seq: int, used: set[str]) -> str:
    candidates = []
    if preferred:
        cleaned = re.sub(r"[^A-Za-z0-9._-]", "-", preferred).strip("-")
        if cleaned:
            candidates.append(cleaned)
            candidates.append(f"{code}-{cleaned}")
    candidates.append(f"{code}-{seq:03d}")
    for cand in candidates:
        if cand not in used:
            used.add(cand)
            return cand
    i = 1
    while True:
        cand = f"{code}-{seq:03d}-{i}"
        if cand not in used:
            used.add(cand)
            return cand
        i += 1


def build_rule(
    block: dict[str, str],
    *,
    code: str,
    seq: int,
    used: set[str],
    fulltext_rel: str,
    lines: list[str] | None,
    mismatch: list[dict],
    book_key: str,
) -> dict | None:
    statement = statement_of(block)
    if not statement:
        return None
    preferred = first_present(block, ["rule_id", "id"])
    rule_id = uniquify(preferred or None, code, seq, used)
    quote = first_present(block, ["quote"])
    anchor_raw = first_present(block, ["source_anchor", "normalized_lines", "source_location"])
    span = parse_anchor(anchor_raw)
    anchor = None
    if span and lines:
        start, end = span
        if 1 <= start <= end <= len(lines):
            extracted = pick_quote(lines, start, end)
            if quote and collapse(quote) not in collapse("\n".join(lines[start - 1 : end])):
                mismatch.append(
                    {
                        "book": book_key,
                        "rule_id": rule_id,
                        "reason": "existing quote not in anchor window; replaced or dropped",
                    }
                )
                quote = extracted or ""
            if not quote:
                quote = extracted
            if quote and collapse(quote) in collapse("\n".join(lines[start - 1 : end])):
                anchor = {"file": fulltext_rel, "start_line": start, "end_line": end}
            else:
                mismatch.append({"book": book_key, "rule_id": rule_id, "reason": "anchor window empty"})
                anchor = None
        else:
            mismatch.append(
                {
                    "book": book_key,
                    "rule_id": rule_id,
                    "reason": f"anchor out of range {start}-{end} / {len(lines) if lines else 0}",
                }
            )
    if not quote:
        quote = statement
        anchor = None
    return {
        "rule_id": rule_id,
        "statement": statement,
        "anchor": anchor,
        "quote": quote,
        "applicable_to": applicable_of(block),
        "caveats": caveats_of(block),
        "school": None,
        "verified": False,
        "verified_by": None,
        "verified_at": None,
    }


def dump_yaml(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(
            data,
            fh,
            allow_unicode=True,
            sort_keys=False,
            width=96,
            default_flow_style=False,
        )


def main() -> int:
    packs = load_catalog()
    used_ids: set[str] = set()
    extra_tags: set[str] = set()
    mismatch: list[dict] = []
    written = 0
    rule_count = 0
    anchored = 0

    for pack in packs:
        system = pack["system"]
        slug = pack["slug"]
        title = pack["title"]
        book_key = f"{system}/{slug}"
        rules_md = ROOT / "references/books" / system / slug / "rules.md"
        ft = fulltext_for(system, slug)
        if ft is None:
            print(f"WARN no fulltext for {book_key}", file=sys.stderr)
            continue
        rel = ft.relative_to(ROOT).as_posix()
        digest = sha256_file(ft)
        lines = ft.read_text(encoding="utf-8").splitlines()
        blocks = collect_blocks(rules_md) if rules_md.is_file() else []
        code = book_code(slug)
        rules = []
        seq = 0
        for block in blocks:
            seq += 1
            rule = build_rule(
                block,
                code=code,
                seq=seq,
                used=used_ids,
                fulltext_rel=rel,
                lines=lines,
                mismatch=mismatch,
                book_key=book_key,
            )
            if rule is None:
                continue
            extra_tags.update(rule["applicable_to"])
            if rule["anchor"] is not None:
                anchored += 1
            rules.append(rule)
            rule_count += 1
        payload = {
            "schema_version": SCHEMA_VERSION,
            "book": {
                "slug": slug,
                "system": system,
                "title": title,
                "fulltext": rel,
                "fulltext_sha256": digest,
            },
            "rules": rules,
        }
        out = ROOT / "references/books" / system / slug / "rules.yaml"
        dump_yaml(payload, out)
        written += 1
        print(f"wrote {book_key} rules={len(rules)}")

    product = load_product_terms()
    seen = {t["canonical"] for t in product}
    terms = list(product)
    for seed in SEED_TERMS:
        if seed["canonical"] not in seen:
            terms.append(seed)
            seen.add(seed["canonical"])
            extra_tags.discard(seed["canonical"])
    known = set(seen)
    for t in terms:
        known.update(t.get("aliases") or [])
    for tag in sorted(extra_tags):
        if tag not in known:
            terms.append({"canonical": tag, "aliases": [], "kind": "imported"})
            known.add(tag)
    vocab = {"schema_version": VOCAB_SCHEMA, "terms": terms}
    vocab_path = ROOT / "references/vocab/terms.yaml"
    dump_yaml(vocab, vocab_path)

    report_dir = ROOT / "tools" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "anchor-mismatch.json").write_text(
        json.dumps(mismatch, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"done books={written} rules={rule_count} anchored={anchored} "
        f"terms={len(terms)} mismatches={len(mismatch)} vocab={vocab_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
