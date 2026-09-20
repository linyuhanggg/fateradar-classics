#!/usr/bin/env python3
"""把《李虚中命书》六十甲子纳音象辞逐条映成「同柱干支」谓词。

背景：这批规则的 `quote` 是**整行**摘录，而源文件一行里常并列两三个甲子条目
（实测 L26 同时含「己巳地奇備乃…」与「庚午天祿承是…」）。所以

  ✗ **不能**从 quote 开头解析干支 —— 重复条目的 quote 与上一条同样以行首那个干支开头，
    照此映射会把「庚午」条锚成「己巳」。
  ✓ 正确做法：从 **statement 的象辞** 出发，在锚定行里反查它前面的干支。

源文形态是「干支 + 贵神名 + 乃/是 + 象辞」，例如
  「己巳地奇備**乃**氣勝體剛之木」「庚午天祿承**是**含輝始育之土」。
故判据：在锚定行里用 `(干)(支)[^乃是]{0,8}[乃是]?(象辞)` 反查，要求**唯一命中**。

输出谓词形态（v3）：`{all_of: [{key: gan, value: 干}, {key: zhi, value: 支}], same: pillar}`
——「某一柱的天干是 X 且地支是 Y」，即该柱为 XY。`same: pillar` 正是为此而加的绑定语义。

**不写锚点、不改 statement/quote**：只改 `applicable_to`；反查不唯一的一律跳过并登记。

    python3 tools/map-nayin-ganzhi.py --dry-run
    python3 tools/map-nayin-ganzhi.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOK = "luming-nayin/li-xuzhong-mingshu"
YAML_PATH = ROOT / "references/books" / BOOK / "rules.yaml"

spec = importlib.util.spec_from_file_location("vr_gz", ROOT / "tools/validate-rules.py")
_vr = importlib.util.module_from_spec(spec)
sys.modules["vr_gz"] = _vr
assert spec.loader is not None
spec.loader.exec_module(_vr)
fold_han = _vr.fold_han

# 古异体字：`fold_han` 走 opencc t2s，能处理繁简，但**不处理异体字形**——
# 实测 逺/㳺/蔵/隂 原样保留，于是「流远澄清之水」（statement）与「流逺澄清之水」（源文）
# 归一后仍不相等，象辞匹配失败、条目被误判成「找不到干支」。
# 只补本批实际撞到的字形，不把整张异体表搬进来。
VARIANT = {"逺": "远", "㳺": "游", "蔵": "藏", "隂": "阴", "髙": "高"}


def norm(text: str) -> str:
    out = fold_han(text)
    for bad, good in VARIANT.items():
        out = out.replace(fold_han(bad), good)
    return out

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
# 象辞签名：statement 里的「…之金／之木／之火／之水／之土」短语
XIANG_RE = re.compile(r"([\u4e00-\u9fff]{1,8}之[金木水火土])")
# 行内每个甲子条目的起点
GZ_RE = re.compile(rf"[{GAN}][{ZHI}]")


def line_entries(line: str) -> list[tuple[str, str]]:
    """把一行按甲子条目切开：[(干支, 该条目文本), ...]。

    不能用一个「干支 + 若干字 + 乃/是 + .+」的正则去扫 —— `.+` 贪婪会一口吞掉整行，
    于是**每行只有第一个干支被看到**，行内后续条目（源文一行常并列 2–3 个甲子）
    永远匹配不上。实测这会让「庚午」条被静默跳过。
    """
    marks = [m.start() for m in GZ_RE.finditer(line)]
    out: list[tuple[str, str]] = []
    for i, pos in enumerate(marks):
        end = marks[i + 1] if i + 1 < len(marks) else len(line)
        out.append((line[pos : pos + 2], line[pos:end]))
    return out


def extract_ganzhi(statement: str, line: str) -> tuple[str, str, str] | None:
    """从 statement 的象辞反查锚定行里的干支。全文唯一命中才返回。"""
    m = XIANG_RE.search(statement)
    if not m:
        return None
    xiang = norm(m.group(1))
    if len(xiang) < 3:
        return None
    hits: list[tuple[str, str]] = []
    for gz, entry in line_entries(line):
        folded = norm(entry)
        # 象辞须落在该条目开头一段内（干支 + 贵神名 + 乃/是 + 象辞；
        # 注文可能插在乃/是之前，如「庚寅地奇備不避刑衝寧辭衰敗乃五行堅實之木」，
        # 故窗口放宽到 30 字，但不得跨到下一条目——entry 已按干支切分，天然不会跨条）。
        if xiang in folded[:30]:
            hits.append((gz[0], gz[1]))
    if len(hits) != 1:
        return None
    return hits[0][0], hits[0][1], m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description="六十甲子纳音象辞 → 同柱干支谓词")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = YAML_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    rules = data["rules"]

    mapped: list[dict] = []
    skipped: list[dict] = []
    for rule in rules:
        rid = rule.get("rule_id")
        if rule.get("applicable_to"):
            continue
        stmt = rule.get("statement") or ""
        if not XIANG_RE.search(stmt):
            continue
        anchor = rule.get("anchor")
        if not isinstance(anchor, dict):
            skipped.append({"rule_id": rid, "reason": "无锚点"})
            continue
        lines = (ROOT / anchor["file"]).read_text(encoding="utf-8").split("\n")
        line = "\n".join(lines[anchor["start_line"] - 1 : anchor["end_line"]])
        got = extract_ganzhi(stmt, line)
        if got is None:
            skipped.append({"rule_id": rid, "reason": "象辞在锚定行内反查干支不唯一或未命中"})
            continue
        gan, zhi, xiang = got
        mapped.append({"rule_id": rid, "gan": gan, "zhi": zhi, "xiang": xiang})

    print(f"可映射 {len(mapped)} 条；跳过 {len(skipped)} 条")
    seq = [f"{m['gan']}{m['zhi']}" for m in mapped]
    print("干支序列:", " ".join(seq))
    dup = sorted({g for g in seq if seq.count(g) > 1})
    print("重复:", dup or "无")
    if skipped:
        print("跳过明细:")
        for s in skipped[:10]:
            print("   ", s)

    if args.dry_run:
        return 0

    # 逐条改写 applicable_to（只动这一行）
    for m in mapped:
        pred = (
            "{all_of: [{key: gan, value: %s}, {key: zhi, value: %s}], same: pillar}" % (m["gan"], m["zhi"])
        )
        rid = re.escape(m["rule_id"])
        pattern = re.compile(
            rf"(?m)^(- rule_id: {rid}\n(?:.*\n)*?  applicable_to: )\[\]$"
        )
        text, n = pattern.subn(lambda mo: mo.group(1) + pred, text, count=1)
        if n != 1:
            raise SystemExit(f"改寫失敗: {m['rule_id']}（來源不符或非空）")
    YAML_PATH.write_text(text, encoding="utf-8")
    print(f"已寫入 {YAML_PATH.relative_to(ROOT)}")
    json.dump(mapped, open(ROOT / "tools/reports/nayin-ganzhi-map.json", "w"), ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())