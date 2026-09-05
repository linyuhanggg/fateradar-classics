#!/usr/bin/env python3
"""Validate fateradar-rules-v2 packs. Stdlib + PyYAML only."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    sys.exit(1)

SCHEMA_VERSION = "fateradar-rules-v2"
VOCAB_SCHEMA = "fateradar-vocab-v1"
SYSTEMS = {
    "bazi",
    "ziwei",
    "san-shi",
    "divination",
    "xingming",
    "fengshui",
    "luming-nayin",
    "physiognomy",
    "selection",
}
SCRIPTS = {"traditional", "simplified"}
KINDS = {"doctrine", "procedure"}
BOOK_FIELDS = ("slug", "system", "title", "script", "fulltext", "fulltext_sha256")
RULE_FIELDS = (
    "rule_id",
    "kind",
    "statement",
    "anchor",
    "quote",
    "applicable_to",
    "caveats",
    "school",
    "verified",
    "verified_by",
    "verified_at",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
WS_RE = re.compile(r"\s+", re.UNICODE)
HAN_RE = re.compile(r"[㐀-鿿]")
SCRIPT_PAIRS = (
    ("專", "专"),
    ("國", "国"),
    ("無", "无"),
    ("這", "这"),
    ("個", "个"),
    ("時", "时"),
    ("為", "为"),
    ("與", "与"),
    ("後", "后"),
    ("來", "来"),
    ("過", "过"),
    ("對", "对"),
    ("發", "发"),
    ("經", "经"),
    ("關", "关"),
    ("麼", "么"),
    ("說", "说"),
    ("義", "义"),
    ("書", "书"),
    ("門", "门"),
    ("開", "开"),
    ("體", "体"),
    ("餘", "余"),
    ("歲", "岁"),
    ("萬", "万"),
    ("學", "学"),
    ("當", "当"),
    ("從", "从"),
    ("還", "还"),
    ("氣", "气"),
    ("裏", "里"),
    ("並", "并"),
    ("於", "于"),
    ("卻", "却"),
    ("論", "论"),
    ("殺", "杀"),
    ("財", "财"),
    ("傷", "伤"),
    ("順", "顺"),
    ("陽", "阳"),
    ("陰", "阴"),
    ("龍", "龙"),
    ("祿", "禄"),
    ("權", "权"),
    ("數", "数"),
    ("術", "术"),
    ("會", "会"),
    ("實", "实"),
    ("業", "业"),
    ("點", "点"),
    ("殺", "杀"),
    ("剋", "克"),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def collapse(text: str) -> str:
    return WS_RE.sub("", text or "")


def han_count(text: str) -> int:
    return len(HAN_RE.findall(text or ""))


HEADING_QUOTE_RE = re.compile(r"^#{1,6}(?:\s|$)")
META_QUOTE_RE = re.compile(r"(?m)^(?:-\s*)?(raw_file|section_note|source_base)\s*:")
ATTRIB_QUOTE_RE = re.compile(r"(?:唐|宋|元|明|清)[·\s]*[一-鿿]{2,6}\s*(?:撰|輯|編|著述|辑录|輯錄)")
JUDOU_RE = re.compile(r"[。！？；!?]")
T2S_TABLE = str.maketrans({t: s for t, s in SCRIPT_PAIRS if len(t) == 1 and len(s) == 1})


def fold_han(text: str) -> str:
    src = text or ""
    try:
        from zhconv import convert as _zh_convert
        folded = _zh_convert(src, "zh-cn")
    except ImportError:
        conv = getattr(fold_han, "_opencc", None)
        if conv is None:
            import opencc as _opencc
            conv = _opencc.OpenCC("t2s")
            fold_han._opencc = conv
        folded = conv.convert(src)
    return "".join(HAN_RE.findall(folded))


def v13_bad_quote(quote: str, book_title: str = "") -> str | None:
    """客观劣质 quote：标题行、pack 元数据、卷首署名。仅用于已锚规则。"""
    q = (quote or "").strip()
    if not q:
        return None
    if HEADING_QUOTE_RE.match(q):
        return "quote 是 markdown 标题行，不能作为断辞"
    if q.startswith(">"):
        return "quote 以 > 开头，是引用/批注标记行，不能作为断辞"
    if META_QUOTE_RE.search(q):
        return "quote 是 pack 元数据，不是原文断辞"
    if ATTRIB_QUOTE_RE.search(q) and han_count(q) <= 40:
        return "quote 是卷首署名，不是原文断辞"
    quote_h = fold_han(q)
    if not JUDOU_RE.search(q) and han_count(q) <= 24:
        for part in re.split(r"[/／|]", book_title or ""):
            title_h = fold_han(part)
            if title_h and (quote_h == title_h or quote_h.endswith(title_h)):
                return "quote 是书名/卷首行，不是原文断辞"
    return None


def correspondence(statement: str, quote: str) -> float:
    """statement↔quote 繁简归一后的汉字集合对应度（statement 侧召回）。"""
    stmt_h = fold_han(statement)
    if not stmt_h:
        return 1.0
    sa, sb = set(stmt_h), set(fold_han(quote))
    return len(sa & sb) / len(sa)


def load_yaml(path: Path):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, f"V1 {path}: YAML 无法解析: {exc}"
    return data, None


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def script_scores(text: str) -> tuple[int, int]:
    trad = simp = 0
    for t_ch, s_ch in SCRIPT_PAIRS:
        trad += (text or "").count(t_ch)
        simp += (text or "").count(s_ch)
    return trad, simp


def load_catalog(root: Path) -> dict[tuple[str, str], str]:
    catalog_path = root / "references" / "catalog" / "catalog.json"
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    titles: dict[tuple[str, str], str] = {}
    for pack in raw.get("ready_reference_packs", []):
        titles[(pack["system"], pack["slug"])] = pack["title"]
    return titles


def load_fact_vocab(root: Path) -> tuple[set[str], dict[str, list[str]], str, list[str]]:
    path = root / "references" / "vocab" / "fact-vocab.json"
    errors: list[str] = []
    if not path.is_file():
        return set(), {}, "*", [f"V7 {path}: fact-vocab.json 不存在"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return set(), {}, "*", [f"V7 {path}: JSON 无法解析: {exc}"]
    keys = {k for k in data.get("keys") or [] if isinstance(k, str)}
    values = data.get("values") or {}
    if not isinstance(values, dict):
        values = {}
        errors.append(f"V7 {path}: values 应为 mapping")
    any_token = data.get("any") if isinstance(data.get("any"), str) else "*"
    if not keys:
        errors.append(f"V7 {path}: keys 为空")
    return keys, values, any_token, errors


def load_terms(root: Path) -> list[str]:
    path = root / "references" / "vocab" / "terms.yaml"
    if not path.is_file():
        return [f"V7 {path}: 术语表不存在"]
    data, err = load_yaml(path)
    if err:
        return [err]
    if not isinstance(data, dict) or data.get("schema_version") != VOCAB_SCHEMA:
        return [f"V7 {path}: schema_version 应为 {VOCAB_SCHEMA}"]
    if not isinstance(data.get("terms"), list) or not data["terms"]:
        return [f"V7 {path}: terms 应非空"]
    return []


def iter_rule_files(root: Path, book: str | None) -> list[Path]:
    base = root / "references" / "books"
    if book:
        path = base / book / "rules.yaml"
        return [path]
    return sorted(base.glob("*/*/rules.yaml"))


def legal_pred_value(key: str, value: str, values: dict[str, list[str]], any_token: str) -> bool:
    if value == any_token:
        return True
    allowed = values.get(key)
    if allowed is None:
        return False
    if allowed == []:
        return isinstance(value, str) and value != ""
    return value in allowed


class Reporter:
    def __init__(self) -> None:
        self.errors: list[dict[str, str]] = []
        self.warnings: list[dict[str, str]] = []

    def add(self, code: str, message: str, *, rule_id: str = "", book: str = "") -> None:
        self.errors.append({"code": code, "book": book, "rule_id": rule_id, "message": message})

    def warn(self, code: str, message: str, *, rule_id: str = "", book: str = "") -> None:
        self.warnings.append({"code": code, "book": book, "rule_id": rule_id, "message": message})

    @property
    def ok(self) -> bool:
        return not self.errors


def as_str_list(value, *, field: str, loc: str, reporter: Reporter, rule_id: str, book: str) -> list[str]:
    if value is None:
        reporter.add("V2", f"{loc}: 缺失字段 {field}", rule_id=rule_id, book=book)
        return []
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        reporter.add("V2", f"{loc}: 字段 {field} 应为字符串列表", rule_id=rule_id, book=book)
        return []
    return value


def validate_predicates(
    raw,
    *,
    loc: str,
    reporter: Reporter,
    rule_id: str,
    book: str,
    system: str,
    fact_keys: set[str],
    fact_values: dict[str, list[str]],
    any_token: str,
) -> None:
    if raw is None:
        reporter.add("V2", f"{loc}: 缺失字段 applicable_to", rule_id=rule_id, book=book)
        return
    if not isinstance(raw, list):
        reporter.add("V2", f"{loc}: 字段 applicable_to 应为谓词列表", rule_id=rule_id, book=book)
        return
    for j, pred in enumerate(raw):
        ploc = f"{loc} applicable_to[{j}]"
        if not isinstance(pred, dict):
            reporter.add("V2", f"{ploc}: 应为 {{key, value}} mapping", rule_id=rule_id, book=book)
            continue
        key = pred.get("key")
        value = pred.get("value")
        if not isinstance(key, str) or not key:
            reporter.add("V2", f"{ploc}: key 应为非空字符串", rule_id=rule_id, book=book)
            continue
        if not isinstance(value, str) or not value:
            reporter.add("V2", f"{ploc}: value 应为非空字符串", rule_id=rule_id, book=book)
            continue
        if key not in fact_keys:
            reporter.add("V7", f"{ploc}: 未登记的 FactKey {key!r}", rule_id=rule_id, book=book)
            continue
        if not legal_pred_value(key, value, fact_values, any_token):
            reporter.add(
                "V7",
                f"{ploc}: value {value!r} 不在 FACT_VALUES[{key}] 内（通配仅允许 {any_token!r}）",
                rule_id=rule_id,
                book=book,
            )
        scope = pred.get("scope")
        if scope is not None and not isinstance(scope, dict):
            reporter.add("V2", f"{ploc}: scope 应为 mapping", rule_id=rule_id, book=book)
            continue
        if isinstance(scope, dict) and "palace" in scope:
            palace = scope.get("palace")
            if system != "ziwei":
                reporter.add(
                    "V15",
                    f"{ploc}: 只有 ziwei 规则可以写 scope.palace",
                    rule_id=rule_id,
                    book=book,
                )
                continue
            allowed = fact_values.get("ziwei_palace") or []
            if not isinstance(palace, str) or palace not in allowed:
                reporter.add(
                    "V15",
                    f"{ploc}: palace {palace!r} 不在 ziwei_palace 取值内",
                    rule_id=rule_id,
                    book=book,
                )


def validate_fulltext_lines(ft_path: Path, *, book_key: str, loc: str, reporter: Reporter) -> None:
    try:
        lines = ft_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        reporter.add("V4", f"{loc}: 无法读取 fulltext: {exc}", book=book_key)
        return
    for i, line in enumerate(lines, 1):
        if "|" in line:
            continue
        n = han_count(line)
        if n > 120:
            reporter.warn(
                "V12",
                f"{loc}: fulltext L{i} 汉字数 {n} > 120",
                book=book_key,
            )


def validate_book(
    path: Path,
    root: Path,
    catalog: dict[tuple[str, str], str],
    fact_keys: set[str],
    fact_values: dict[str, list[str]],
    any_token: str,
    reporter: Reporter,
    id_index: dict[str, Path],
) -> None:
    rel = path.relative_to(root).as_posix()
    book_key = path.parent.relative_to(root / "references" / "books").as_posix()
    data, err = load_yaml(path)
    if err:
        reporter.add("V1", err, book=book_key)
        return
    if not isinstance(data, dict):
        reporter.add("V1", f"V1 {rel}: 根节点必须是 mapping", book=book_key)
        return
    if data.get("schema_version") != SCHEMA_VERSION:
        reporter.add(
            "V1",
            f"V1 {rel}: schema_version 应为 {SCHEMA_VERSION}，实际 {data.get('schema_version')!r}",
            book=book_key,
        )

    book = data.get("book")
    if not isinstance(book, dict):
        reporter.add("V2", f"{rel}: 缺失字段 book", book=book_key)
        return
    for field in BOOK_FIELDS:
        if field not in book:
            reporter.add("V2", f"{rel}: 缺失字段 {field}", book=book_key)
    slug = book.get("slug")
    system = book.get("system")
    title = book.get("title")
    script = book.get("script")
    fulltext = book.get("fulltext")
    digest = book.get("fulltext_sha256")
    if not isinstance(slug, str) or not isinstance(system, str) or not isinstance(title, str):
        reporter.add("V2", f"{rel}: book.slug/system/title 应为字符串", book=book_key)
        return
    if system not in SYSTEMS:
        reporter.add("V2", f"{rel}: book.system 非法: {system}", book=book_key)
    if not isinstance(script, str) or script not in SCRIPTS:
        reporter.add("V2", f"{rel}: book.script 应为 traditional|simplified", book=book_key)
        script = ""
    if path.parent.name != slug:
        reporter.add(
            "V3",
            f"{rel}: book.slug={slug!r} 与目录名 {path.parent.name!r} 不一致",
            book=book_key,
        )
    if path.parent.parent.name != system:
        reporter.add(
            "V3",
            f"{rel}: book.system={system!r} 与目录 {path.parent.parent.name!r} 不一致",
            book=book_key,
        )
    expected_title = catalog.get((system, slug))
    if expected_title is None:
        reporter.add("V3", f"{rel}: catalog.json 中不存在 {system}/{slug}", book=book_key)
    elif expected_title != title:
        reporter.add(
            "V3",
            f"{rel}: book.title={title!r} catalog.title={expected_title!r}",
            book=book_key,
        )

    if not isinstance(fulltext, str):
        reporter.add("V2", f"{rel}: book.fulltext 应为路径字符串", book=book_key)
        return
    ft_path = root / fulltext
    if not ft_path.is_file():
        reporter.add("V4", f"{rel}: fulltext 不存在: {fulltext}", book=book_key)
    else:
        actual = sha256_file(ft_path)
        if not isinstance(digest, str) or not SHA_RE.match(digest):
            reporter.add("V2", f"{rel}: book.fulltext_sha256 应为 64 位十六进制", book=book_key)
        elif actual != digest:
            reporter.add(
                "V4",
                f"{rel}: sha256 期望 {digest} 实际 {actual}",
                book=book_key,
            )
        validate_fulltext_lines(ft_path, book_key=book_key, loc=rel, reporter=reporter)

    rules = data.get("rules")
    if not isinstance(rules, list):
        reporter.add("V2", f"{rel}: 缺失字段 rules（应为列表）", book=book_key)
        return

    for i, rule in enumerate(rules):
        loc = f"{rel} rules[{i}]"
        if not isinstance(rule, dict):
            reporter.add("V2", f"{loc}: 条目应为 mapping", book=book_key)
            continue
        for field in RULE_FIELDS:
            if field not in rule:
                reporter.add("V2", f"{loc}: 缺失字段 {field}", book=book_key)
        rule_id = rule.get("rule_id") if isinstance(rule.get("rule_id"), str) else ""
        statement = rule.get("statement")
        quote = rule.get("quote")
        kind = rule.get("kind")
        if not isinstance(rule_id, str) or not rule_id:
            reporter.add("V2", f"{loc}: 字段 rule_id 应为非空字符串", book=book_key)
            rule_id = f"<missing:{i}>"
        else:
            prev = id_index.get(rule_id)
            if prev is not None:
                reporter.add(
                    "V6",
                    f"重复 rule_id {rule_id}: {prev.relative_to(root).as_posix()} 与 {rel}",
                    rule_id=rule_id,
                    book=book_key,
                )
            else:
                id_index[rule_id] = path

        if kind not in KINDS:
            reporter.add("V10", f"{loc}: kind 应为 doctrine|procedure，实际 {kind!r}", rule_id=rule_id, book=book_key)

        if not isinstance(statement, str):
            reporter.add("V2", f"{loc}: 字段 statement 应为字符串", rule_id=rule_id, book=book_key)
            statement = ""
        if not isinstance(quote, str):
            reporter.add("V2", f"{loc}: 字段 quote 应为字符串", rule_id=rule_id, book=book_key)
            quote = ""
        if len(statement) > 200:
            reporter.add(
                "V9",
                f"{loc}: statement 长度为 {len(statement)}，超过 200 字",
                rule_id=rule_id,
                book=book_key,
            )
        if not quote.strip():
            reporter.add("V9", f"{loc}: quote 为空", rule_id=rule_id, book=book_key)

        if script and quote.strip():
            trad, simp = script_scores(quote)
            if script == "traditional" and simp > trad and simp > 0:
                reporter.warn(
                    "V11",
                    f"{loc}: quote 简体特征字 {simp} > 繁体 {trad}，与 book.script=traditional 不一致",
                    rule_id=rule_id,
                    book=book_key,
                )
            elif script == "simplified" and trad > simp and trad > 0:
                reporter.warn(
                    "V11",
                    f"{loc}: quote 繁体特征字 {trad} > 简体 {simp}，与 book.script=simplified 不一致",
                    rule_id=rule_id,
                    book=book_key,
                )

        validate_predicates(
            rule.get("applicable_to"),
            loc=loc,
            reporter=reporter,
            rule_id=rule_id,
            book=book_key,
            system=system,
            fact_keys=fact_keys,
            fact_values=fact_values,
            any_token=any_token,
        )
        as_str_list(
            rule.get("caveats"),
            field="caveats",
            loc=loc,
            reporter=reporter,
            rule_id=rule_id,
            book=book_key,
        )

        school = rule.get("school")
        if school is not None and not isinstance(school, str):
            reporter.add("V2", f"{loc}: 字段 school 应为 null 或字符串", rule_id=rule_id, book=book_key)

        verified = rule.get("verified")
        if not isinstance(verified, bool):
            reporter.add("V2", f"{loc}: 字段 verified 应为布尔值", rule_id=rule_id, book=book_key)
            verified = False
        verified_by = rule.get("verified_by")
        verified_at = rule.get("verified_at")
        if verified:
            if not (isinstance(verified_by, str) and verified_by.strip()):
                reporter.add("V8", f"{loc}: verified=true 时 verified_by 必填", rule_id=rule_id, book=book_key)
            if not (isinstance(verified_at, str) and verified_at.strip()):
                reporter.add("V8", f"{loc}: verified=true 时 verified_at 必填", rule_id=rule_id, book=book_key)
        else:
            if verified_by not in (None, ""):
                reporter.add("V2", f"{loc}: verified=false 时 verified_by 应为 null", rule_id=rule_id, book=book_key)
            if verified_at not in (None, ""):
                reporter.add("V2", f"{loc}: verified=false 时 verified_at 应为 null", rule_id=rule_id, book=book_key)

        anchor = rule.get("anchor")
        if anchor is None:
            continue
        if not isinstance(anchor, dict):
            reporter.add("V2", f"{loc}: 字段 anchor 应为 null 或 mapping", rule_id=rule_id, book=book_key)
            continue
        a_file = anchor.get("file")
        start = anchor.get("start_line")
        end = anchor.get("end_line")
        if not isinstance(a_file, str) or not isinstance(start, int) or not isinstance(end, int):
            reporter.add(
                "V2",
                f"{loc}: anchor.file 应为字符串，start_line/end_line 应为整数",
                rule_id=rule_id,
                book=book_key,
            )
            continue
        a_path = root / a_file
        if not a_path.is_file():
            reporter.add("V5", f"{loc}: 锚点文件不存在: {a_file}", rule_id=rule_id, book=book_key)
            continue
        lines = a_path.read_text(encoding="utf-8").splitlines()
        if start < 1 or end < start or end > len(lines):
            reporter.add(
                "V5",
                f"{loc}: 锚点行区间非法 start={start} end={end} 文件行数={len(lines)}",
                rule_id=rule_id,
                book=book_key,
            )
            continue
        window = collapse("\n".join(lines[start - 1 : end]))
        needle = collapse(quote)
        if not needle or needle not in window:
            preview = window[:200]
            reporter.add(
                "V5",
                f"{loc}: quote 去空白后不是锚点区间子串。quote={quote!r} 锚点区前 200 字={preview!r}",
                rule_id=rule_id,
                book=book_key,
            )

        reason = v13_bad_quote(quote, title)
        if reason:
            reporter.add(
                "V13",
                f"{loc}: {reason}。quote={quote!r}",
                rule_id=rule_id,
                book=book_key,
            )
        score = correspondence(statement, quote)
        if score < 0.15:
            reporter.warn(
                "V14",
                f"{loc}: statement/quote 对应度 {score:.3f} < 0.15",
                rule_id=rule_id,
                book=book_key,
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate fateradar-rules-v2 YAML")
    parser.add_argument("--book", help="仅校验 references/books/<system>/<slug>")
    parser.add_argument("--json", action="store_true", help="机读输出")
    args = parser.parse_args(argv)

    root = repo_root()
    reporter = Reporter()
    files = iter_rule_files(root, args.book)
    if args.book and (not files or not files[0].is_file()):
        reporter.add("V1", f"找不到 references/books/{args.book}/rules.yaml")
    catalog = load_catalog(root)
    fact_keys, fact_values, any_token, vocab_errors = load_fact_vocab(root)
    for msg in vocab_errors:
        reporter.add("V7", msg)
    for msg in load_terms(root):
        reporter.add("V7", msg)

    id_index: dict[str, Path] = {}
    all_yaml = sorted((root / "references" / "books").glob("*/*/rules.yaml"))
    if args.book:
        for other in all_yaml:
            if not files or other.resolve() == files[0].resolve():
                continue
            data, err = load_yaml(other)
            if err or not isinstance(data, dict):
                continue
            for rule in data.get("rules") or []:
                if isinstance(rule, dict) and isinstance(rule.get("rule_id"), str):
                    id_index[rule["rule_id"]] = other

    for path in files:
        if not path.is_file():
            reporter.add("V1", f"V1 {path}: 文件不存在")
            continue
        validate_book(
            path,
            root,
            catalog,
            fact_keys,
            fact_values,
            any_token,
            reporter,
            id_index,
        )

    payload = {
        "ok": reporter.ok,
        "files": len(files),
        "errors": reporter.errors,
        "warnings": reporter.warnings,
    }
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        shown: dict[str, int] = {}
        hidden: dict[str, int] = {}
        for item in reporter.warnings:
            code = item["code"]
            shown[code] = shown.get(code, 0) + 1
            if shown[code] <= 20:
                extra = f" {item['rule_id']}" if item["rule_id"] else ""
                print(f"WARN {item['code']}{extra}: {item['message']}", file=sys.stderr)
            else:
                hidden[code] = hidden.get(code, 0) + 1
        for code, n in hidden.items():
            print(f"WARN {code}: …另有 {n} 条同类警告未展开", file=sys.stderr)
        if reporter.ok:
            print(f"OK  {len(files)} file(s), {len(reporter.warnings)} warning(s)")
        else:
            for item in reporter.errors:
                extra = f" {item['rule_id']}" if item["rule_id"] else ""
                print(f"{item['code']}{extra}: {item['message']}", file=sys.stderr)
            print(
                f"FAIL  {len(reporter.errors)} error(s), {len(reporter.warnings)} warning(s) in {len(files)} file(s)",
                file=sys.stderr,
            )
    return 0 if reporter.ok else 1


if __name__ == "__main__":
    sys.exit(main())
