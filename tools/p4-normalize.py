#!/usr/bin/env python3
"""P4: replace/clean/wrap fulltext, remap anchors, freeze sha256."""

from __future__ import annotations

import hashlib
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[㐀-鿿]")
WS_RE = re.compile(r"\s+", re.UNICODE)
IMAGE_RE = re.compile(r"\[IMAGE:[^\]]*\]")
URL_RE = re.compile(r"https?://\S+")
SENTENCE_SEPS = set("。！？；!?○")
COMMA_SEPS = set("，、；;")
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
)
WRAP_BOOKS = [
    "luming-nayin/yuzhao-shenying",
    "luming-nayin/li-xuzhong-mingshu",
    "divination/zhouyi-zhezhong",
    "bazi/sanming-tonghui",
    "xingming/guotian-jing",
    "xingming/xingxue-dacheng",
    "fengshui/qingnang-jing",
    "fengshui/hanlong-jing",
    "luming-nayin/luoluzi-sanming",
    "xingming/xingming-suyuan",
    "selection/xieji-bianfang-shu",
    "fengshui/huangdi-zhaijing",
    "fengshui/dili-bianzheng",
    "fengshui/tianyu-jing",
    "fengshui/rudi-yan-quanshu",
    "ziwei/feixing-ziwei-doushu-yuanzhi",
]
UA = "FateRadarClassics/0.1 (public-domain recovery; +https://github.com/linyuhanggg/fateradar-classics)"


def han_count(text: str) -> int:
    return len(HAN_RE.findall(text or ""))


def collapse(text: str) -> str:
    return WS_RE.sub("", text or "")


def ft_path(book: str) -> Path:
    return ROOT / "sources/fulltext" / book / "fulltext.md"


def detect_script(text: str) -> str:
    trad = simp = 0
    for t_ch, s_ch in SCRIPT_PAIRS:
        trad += text.count(t_ch)
        simp += text.count(s_ch)
    if trad == 0 and simp == 0:
        return "traditional"
    return "traditional" if trad >= simp else "simplified"


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wiki_parse(title: str, prop: str) -> str:
    q = urllib.parse.urlencode(
        {
            "action": "parse",
            "page": title,
            "prop": prop,
            "format": "json",
            "formatversion": "2",
            "variant": "zh-hant",
        }
    )
    data = http_json(f"https://zh.wikisource.org/w/api.php?{q}")
    payload = data.get("parse", {}).get(prop, "")
    if not isinstance(payload, str) or not payload.strip():
        raise RuntimeError(f"empty {prop} for {title}: {list(data)}")
    return payload


def wiki_wikitext(title: str) -> str:
    return wiki_parse(title, "wikitext")


def html_to_md(html: str) -> str:
    import html as html_lib

    t = html
    t = re.sub(r"<style[\s\S]*?</style>", "", t, flags=re.I)
    t = re.sub(r'<span class="mw-editsection"[\s\S]*?</span>', "", t, flags=re.I)
    t = re.sub(r"<sup[\s\S]*?</sup>", "", t, flags=re.I)

    def heading(match: re.Match[str], hashes: str) -> str:
        inner = re.sub(r"<[^>]+>", "", match.group(1))
        inner = html_lib.unescape(inner).replace("[編輯]", "").strip()
        return f"\n{hashes} {inner}\n"

    t = re.sub(r"<h2[^>]*>([\s\S]*?)</h2>", lambda m: heading(m, "##"), t, flags=re.I)
    t = re.sub(r"<h3[^>]*>([\s\S]*?)</h3>", lambda m: heading(m, "###"), t, flags=re.I)
    t = re.sub(r"<h4[^>]*>([\s\S]*?)</h4>", lambda m: heading(m, "####"), t, flags=re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"</p>", "\n", t, flags=re.I)
    t = re.sub(r"<p[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<li[^>]*>", "\n- ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = html_lib.unescape(t)
    drop_prefixes = ("◄", "►", "姊妹計劃", "數據項", "@media")
    lines = []
    for line in t.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if s.startswith(drop_prefixes) or s in {"卷二", "卷三", "卷一"}:
            continue
        lines.append(s)
    t = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return t.strip() + "\n"


def replace_ziwei() -> None:
    juans = ["紫微斗數全書/卷一", "紫微斗數全書/卷二", "紫微斗數全書/卷三"]
    parts = []
    for title in juans:
        md = html_to_md(wiki_parse(title, "text"))
        parts.append(f"## {title.split('/')[-1]}\n\n{md}")
    body = (
        "# 紫微斗數全書\n\n"
        "來源：維基文庫《紫微斗數全書》卷一–卷三（variant=zh-hant）。\n\n" + "\n".join(parts)
    )
    path = ft_path("ziwei/ziwei-doushu-quanshu")
    path.write_text(body, encoding="utf-8")
    sample = path.read_text(encoding="utf-8")
    print(
        f"replaced ziwei-doushu-quanshu bytes={path.stat().st_size} "
        f"script={detect_script(sample)}"
    )


def clean_shenshi() -> None:
    path = ft_path("fengshui/shenshi-xuankong-xue")
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    i = 0
    skip_image_refs = False
    in_front = False
    front_done = False
    while i < len(lines):
        line = lines[i]
        if not front_done:
            out.append(line)
            if i == 0 and line.strip() == "---":
                in_front = True
            elif in_front and line.strip() == "---":
                in_front = False
                front_done = True
            i += 1
            continue
        if line.strip() == "## 章节目录":
            i += 1
            while i < len(lines) and (lines[i].startswith("|") or not lines[i].strip()):
                i += 1
            continue
        if line.strip() == "### image_refs":
            skip_image_refs = True
            i += 1
            continue
        if skip_image_refs:
            if not line.strip() or line.startswith("- "):
                i += 1
                if line.strip() == "":
                    skip_image_refs = False
                continue
            skip_image_refs = False
        if re.match(r"^- (chapter_id|source_url|digest_status|image_count):", line):
            i += 1
            continue
        if re.match(r"^- https?://", line.strip()):
            i += 1
            continue
        if "tishi_logo.png" in line or "ananas.chaoxing.com" in line:
            i += 1
            continue
        out.append(line)
        i += 1
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    print(f"cleaned shenshi urls={len(URL_RE.findall(text))}")


def clean_yangzhai() -> None:
    path = ft_path("fengshui/yangzhai-shishu")
    text = path.read_text(encoding="utf-8")
    n = len(IMAGE_RE.findall(text))
    text = IMAGE_RE.sub("[圖]", text)
    path.write_text(text, encoding="utf-8")
    print(f"cleaned yangzhai images={n} remaining={len(IMAGE_RE.findall(text))}")


def clean_bushi() -> None:
    """CTP blocks automation. Strip U+FFFD/PUA on the 4 pagination-boundary lines; do not invent text."""
    path = ft_path("divination/bushi-zhengzong")
    lines = path.read_text(encoding="utf-8").splitlines()
    targets = {968, 975, 1803, 1810}

    def scrub(s: str) -> str:
        s = s.replace("\ufffd", "")
        s = "".join(ch for ch in s if not (0xE000 <= ord(ch) <= 0xF8FF))
        return s.rstrip()

    for n in targets:
        if 1 <= n <= len(lines):
            lines[n - 1] = scrub(lines[n - 1])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    left = sum(1 for i in targets if "\ufffd" in lines[i - 1])
    print(f"cleaned bushi remaining_fffd_on_targets={left}")


def split_at(s: str, seps: set[str]) -> list[str]:
    depth = 0
    out: list[str] = []
    buf: list[str] = []
    for ch in s:
        if ch in "【〔":
            depth += 1
        elif ch in "】〕" and depth:
            depth -= 1
        buf.append(ch)
        if depth == 0 and ch in seps:
            piece = "".join(buf).strip()
            if piece:
                out.append(piece)
            buf = []
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out or ([s] if s else [])


def hard_wrap(s: str, limit: int = 120) -> list[str]:
    # 夹注内不按句读断；超 120 汉字仍硬折，以满足验收。
    out: list[str] = []
    buf: list[str] = []
    n = 0
    for ch in s:
        buf.append(ch)
        if HAN_RE.match(ch):
            n += 1
        if n >= limit:
            out.append("".join(buf).rstrip())
            buf = []
            n = 0
    if buf:
        out.append("".join(buf).rstrip())
    return [x for x in out if x]


def wrap_line(line: str, limit: int = 120) -> list[str]:
    if line.startswith("|") or line.startswith("```"):
        return [line]
    if han_count(line) <= limit:
        return [line]
    pieces = split_at(line, SENTENCE_SEPS)
    out: list[str] = []
    for piece in pieces:
        if han_count(piece) <= limit:
            out.append(piece)
            continue
        for chunk in split_at(piece, COMMA_SEPS):
            if han_count(chunk) <= limit:
                out.append(chunk)
            else:
                out.extend(hard_wrap(chunk, limit))
    return out or [line]


def wrap_book(book: str) -> tuple[int, int]:
    path = ft_path(book)
    text = path.read_text(encoding="utf-8")
    fm, body = "", text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            fm = text[: end + 4]
            body = text[end + 4 :]
            if body.startswith("\n"):
                body = body[1:]
                fm += "\n"
    out_lines: list[str] = []
    long_before = 0
    for line in body.splitlines():
        if han_count(line) > 120 and "|" not in line:
            long_before += 1
        out_lines.extend(wrap_line(line))
    new_body = "\n".join(out_lines).rstrip() + "\n"
    path.write_text((fm + new_body) if fm else new_body, encoding="utf-8")
    leftover = [
        (i, han_count(line), line[:80])
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if han_count(line) > 120 and "|" not in line
    ]
    print(f"wrap {book} long_before={long_before} long_after={len(leftover)} lines={len(out_lines)}")
    for i, n, sample in leftover[:5]:
        print(f"  leftover L{i} han={n} {sample!r}")
    return long_before, len(leftover)


def find_quote(lines: list[str], quote: str) -> tuple[int, int] | None:
    needle = collapse(quote)
    if not needle:
        return None
    mapping: list[int] = []
    chunks: list[str] = []
    for i, line in enumerate(lines, 1):
        c = collapse(line)
        chunks.append(c)
        mapping.extend([i] * len(c))
    hay = "".join(chunks)
    idx = hay.find(needle)
    if idx < 0:
        return None
    end_idx = idx + len(needle) - 1
    if end_idx >= len(mapping):
        return None
    return mapping[idx], mapping[end_idx]


def patch_book_yaml(
    path: Path,
    *,
    digest: str,
    script: str,
    remaps: dict[str, tuple[int, int]],
    wrap_note: str | None,
) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text, n = re.subn(r"(fulltext_sha256:\s*)[0-9a-f]{64}", lambda m: m.group(1) + digest, text, count=1)
    if n != 1:
        print(f"warn: sha256 not patched {path}")
    text, n = re.subn(
        r"(^  script:\s*)(traditional|simplified)",
        r"\1" + script,
        text,
        count=1,
        flags=re.M,
    )
    if n != 1:
        print(f"warn: script not patched {path}")
    if wrap_note and "line_wrap_note:" not in text:
        text, n = re.subn(
            r"(^  script: (?:traditional|simplified)\n)",
            r"\1  line_wrap_note: " + wrap_note + "\n",
            text,
            count=1,
            flags=re.M,
        )
    if remaps:
        lines = text.splitlines()
        current: str | None = None
        for i, line in enumerate(lines):
            m = re.match(r"- rule_id:\s*(\S+)", line)
            if m:
                current = m.group(1)
            if current and current in remaps:
                start, end = remaps[current]
                if re.match(r"    start_line:\s*\d+", line):
                    lines[i] = re.sub(r"\d+", str(start), line, count=1)
                elif re.match(r"    end_line:\s*\d+", line):
                    lines[i] = re.sub(r"\d+", str(end), line, count=1)
        text = "\n".join(lines) + "\n"
    if not text.endswith("\n"):
        text += "\n"
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def remap_and_freeze(changed: set[str]) -> None:
    stats = {"ok": 0, "miss": 0, "null": 0, "rewritten": 0}
    misses: list[str] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        book = path.parent.relative_to(ROOT / "references/books").as_posix()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book_meta = data.get("book") or {}
        ft_rel = book_meta.get("fulltext")
        if not isinstance(ft_rel, str):
            continue
        ft = ROOT / ft_rel
        if not ft.is_file():
            continue
        text = ft.read_text(encoding="utf-8")
        digest = hashlib.sha256(ft.read_bytes()).hexdigest()
        script = detect_script(text)
        remaps: dict[str, tuple[int, int]] = {}
        if book in changed or book_meta.get("fulltext_sha256") != digest:
            lines = text.splitlines()
            for rule in data.get("rules") or []:
                if not isinstance(rule, dict):
                    continue
                rid = str(rule.get("rule_id") or "")
                anchor = rule.get("anchor")
                if not isinstance(anchor, dict):
                    stats["null"] += 1
                    continue
                found = find_quote(lines, rule.get("quote") or "")
                if found is None:
                    stats["miss"] += 1
                    misses.append(f"{book}:{rid}")
                    continue
                remaps[rid] = found
                stats["ok"] += 1
        wrap_note = None
        if book in WRAP_BOOKS:
            table_long = sum(1 for line in text.splitlines() if han_count(line) > 120 and "|" in line)
            if table_long:
                wrap_note = "表格行允许超过 120 汉字"
        if patch_book_yaml(path, digest=digest, script=script, remaps=remaps, wrap_note=wrap_note):
            stats["rewritten"] += 1
    print("freeze", stats)
    if misses:
        print("miss", misses[:20], "total", len(misses))


def wiki_len(title: str) -> int:
    try:
        return len(wiki_wikitext(title))
    except Exception as exc:
        print(f"wiki_len fail {title}: {exc}")
        return -1


def write_decisions() -> None:
    zang = ft_path("fengshui/zangshu").stat().st_size
    xing = ft_path("xingming/xingming-suyuan").stat().st_size
    huang = ft_path("divination/huangji-jingshi").stat().st_size
    report = ROOT / "tools/reports/p4-source-decisions.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "\n".join(
            [
                "# P4 可换源人工结论（2026-09-04）",
                "",
                "原则：公版来源中现有已是最佳可得则不换；多出的体积若像注疏/序跋/四库夹注，不换。",
                "附录 D 的维基体积含 wiki 标记与子页面合计，只作数量级判断。",
                "",
                "## 葬书 `fengshui/zangshu`",
                f"- 现有 {zang} bytes。维基文库主页面《葬書》为吴澄删定短本；《葬書 (四庫全書本)》单页约 42 KB，多出的是提要与注疏。",
                "- 现有本已是吴澄删定内篇/外篇/杂篇正文，与附录 E 正文规模相符。",
                "- **结论：不换。** 换成四库本会引入注疏并重做全部锚点，不是缺卷补全。",
                "",
                "## 星命溯源 `xingming/xingming-suyuan`",
                f"- 现有 {xing} bytes。维基无独立《星命溯源》条；对应《星命溯源 (四庫全書本)》分卷（提要 2704 + 卷1–4 检索可见）。",
                "- 现有本已含四库提要与经诀骨架。",
                "- **结论：不换。** 附录 D「可换源 +58%」对应四库分卷合计，额外体量是注/附录而非证明现有缺卷。",
                "",
                "## 皇极经世书 `divination/huangji-jingshi`",
                f"- 现有 {huang} bytes。维基主条《皇極經世書》为短页；《皇極經世書 (四庫全書本)》及《皇極經世》分卷合计才接近附录 D 的 1603 KB。",
                "- 现有本已 1MB+ / 3 万行，附录 D 明确不要盲目换源。",
                "- **结论：不换。** 多出 41% 不能排除注疏、表谱与 wiki 标记；本书不在附录 C 锚点优先集，换源成本高。",
                "",
                "## 卜筮正宗四行乱码",
                "- 头部 source_url 指向 ctext.org，自动化抓取返回 403（站点禁止自动下载）。",
                "- 维基文库《卜筮正宗》为红链残卷（附录 D：2 KB），不能补 L968/L975/L1803/L1810。",
                "- **处理：** 删除 U+FFFD 与 PUA 乱码码位，保留可辨残句，**不编造**补文。",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {report}")


def strip_fffd() -> None:
    n = 0
    roots = [
        ROOT / "sources/fulltext",
        ROOT / "references/books",
    ]
    for root in roots:
        for p in root.rglob("*"):
            if p.suffix.lower() not in {".md", ".yaml", ".yml", ".txt"}:
                continue
            text = p.read_text(encoding="utf-8")
            if "\ufffd" not in text:
                continue
            n += text.count("\ufffd")
            p.write_text(text.replace("\ufffd", ""), encoding="utf-8")
    print(f"stripped_fffd={n}")


def remnant_scan() -> None:
    shenshi = ft_path("fengshui/shenshi-xuankong-xue").read_text(encoding="utf-8")
    yang = ft_path("fengshui/yangzhai-shishu").read_text(encoding="utf-8")
    bushi = ft_path("divination/bushi-zhengzong").read_text(encoding="utf-8")
    ziwei = ft_path("ziwei/ziwei-doushu-quanshu").read_text(encoding="utf-8")
    print("remnant shenshi_urls", len(URL_RE.findall(shenshi)))
    print("remnant yangzhai_IMAGE", len(IMAGE_RE.findall(yang)))
    print("remnant bushi_fffd", bushi.count("\ufffd"))
    print("remnant ziwei_toc", "在同一頁面全部顯示" in ziwei)
    fffd = 0
    for p in ROOT.rglob("*"):
        if p.suffix.lower() not in {".md", ".yaml", ".yml", ".txt", ".py"}:
            continue
        try:
            fffd += p.read_text(encoding="utf-8", errors="replace").count("\ufffd")
        except OSError:
            continue
    print("repo_fffd_total", fffd)


def main() -> int:
    skip_fetch = "--fix" in sys.argv
    if not skip_fetch:
        replace_ziwei()
        clean_yangzhai()
        clean_bushi()
    clean_shenshi()
    changed = {
        "ziwei/ziwei-doushu-quanshu",
        "fengshui/shenshi-xuankong-xue",
        "fengshui/yangzhai-shishu",
        "divination/bushi-zhengzong",
    }
    for book in WRAP_BOOKS:
        wrap_book(book)
        changed.add(book)
    strip_fffd()
    write_decisions()
    remap_and_freeze(changed)
    remnant_scan()
    return 0


if __name__ == "__main__":
    sys.exit(main())
