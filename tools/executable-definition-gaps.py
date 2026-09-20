#!/usr/bin/env python3
"""executable 层「命名定义」的**可得性**登记册（t183）。

`eval-executable.py` 把 `when` 是 `{definition: X}` / `{interference.id: …}` 的记录
单列为「未提供定义表」——共 12 条。本脚本回答一个具体问题：

    **这些名字，在我们自己的语料里到底有没有定义？**

做法是**逐名检索全文**，把结果分成三态，并留下可复核的证据：

  · `defined-sourced`  语料里有一句话直接给出该名的构成 → 可以据它写定义（附锚点行）
  · `mention-only`     只在别门（`guotian-jing` 星命）散文里被提到，**不是构成定义**
  · `absent`           全文 0 次 → **不能定义**；写出来就是编造

**本脚本只登记、不写定义、不改 executable 记录。** 按贯穿契约「原文没写就不写」，
`absent` 与 `mention-only` 两类必须留空。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXECUTABLE = ROOT / "references/executable"
FULLTEXT = ROOT / "sources/fulltext"

# ⚠ 语料是**繁体**，而 executable 记录里的名字是**简体**：`月朗天门` vs `月朗天門`、
# `贪火相逢` vs `貪火相逢`。初版直接按名字检索，于是把好几个**其实有定义**的名字
# 误判成「全文 0 次」。必须两边都折成简体再比。沿用 validate-rules 的 fold_han（opencc t2s）。
_vr_spec = importlib.util.spec_from_file_location("vr_fold", ROOT / "tools/validate-rules.py")
_vr = importlib.util.module_from_spec(_vr_spec)
sys.modules["vr_fold"] = _vr
assert _vr_spec.loader is not None
_vr_spec.loader.exec_module(_vr)
fold_han = _vr.fold_han


def named_definitions() -> list[dict]:
    out: list[dict] = []
    for f in sorted(EXECUTABLE.glob("*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")).get("rules") or []:
            when = r.get("when") or {}
            if "definition" in when:
                out.append({"kind": "definition", "name": when["definition"], "record": r["id"], "book": f.name})
            elif "interference.id" in when:
                ids = when["interference.id"]
                for i in ids if isinstance(ids, list) else [ids]:
                    out.append({"kind": "interference.id", "name": i, "record": r["id"], "book": f.name})
    return out


_FOLDED_CACHE: dict[Path, list[str]] = {}


def _folded_lines(p: Path) -> list[str]:
    """整份文件**只折一次**并缓存。

    初版对每一行、每一个名字都调一次 opencc —— 13 个名字 × 全语料行数 = 上百万次转换，
    直接被 60 秒超时杀掉。折叠是纯函数，缓存即可。
    """
    if p not in _FOLDED_CACHE:
        _FOLDED_CACHE[p] = [fold_han(x) for x in p.read_text(encoding="utf-8").split("\n")]
    return _FOLDED_CACHE[p]


def search(name: str) -> list[dict]:
    """繁简折半后检索：名字与语料都走 fold_han，避免「月朗天门」搜不到「月朗天門」。

    ⚠ 两个已踩的坑：
    1) 初版对每一行都调 opencc → 上百万次转换 → 超时（已改为整文件折一次并缓存）；
    2) **纯 ASCII 的名字**（如 `month-chong`）被 opencc 折成**空串**，`"" in line` 恒真
       → 报出 22 万处命中。非中文名不做折叠，改为按原文比较。
    """
    hits = []
    has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in name)
    folded = fold_han(name) if has_cjk else name
    for p in sorted(FULLTEXT.rglob("fulltext.md")):
        raw = p.read_text(encoding="utf-8").split("\n")
        lines = _folded_lines(p) if has_cjk else raw
        for i, line in enumerate(lines, 1):
            if folded in line:
                hits.append({
                    "book": p.parent.name,
                    "line": i,
                    "quote": (raw[i - 1] if i - 1 < len(raw) else line).strip()[:120],
                    "rel": p.relative_to(ROOT).as_posix(),
                })
    return hits


def classify(name: str, hits: list[dict], books_with_hits: set[str]) -> tuple[str, str]:
    if not any("\u4e00" <= ch <= "\u9fff" for ch in name):
        return "engine-id", "非语料名（引擎关系 id），不属于「从原文找定义」的范畴"
    if not hits:
        return "absent", "全文 0 次"
    # 本门（紫微斗数全书）里出现 = 可能是构成定义；别门散文提到 = 不算定义
    return "mention-only", f"仅在 {'／'.join(sorted(books_with_hits))} 出现 {len(hits)} 处（非本门构成定义）"


def main() -> int:
    ap = argparse.ArgumentParser(description="executable 命名定义的可得性登记册")
    ap.add_argument("--out", default="tools/reports/executable-definition-gaps.json")
    args = ap.parse_args()

    defs = named_definitions()
    n_files = len(list(FULLTEXT.rglob("fulltext.md")))
    entries = []
    for d in defs:
        hits = search(d["name"])
        books = {h["book"] for h in hits}
        status, why = classify(d["name"], hits, books)
        # 特例：本门（ziwei 书）里出现且句式是「X 是/是也」= 构成定义
        # 本门术语表体例是「名稱 構成…是也。」——**行首即名字**。
        # 初版只用 `者` 之类宽松正则，会把散文句也算成定义；改为「行首+是也/即是」。
        sourced = []
        fn = fold_han(d["name"])   # 注意：此处在 main 的循环里，名字是 d["name"]
        for h in hits:
            if not h["book"].startswith("ziwei"):
                continue
            fl = fold_han(h["quote"]).strip()
            if "见前批注" in fl or "見前批註" in fl:
                continue  # 互见条目：把定义推给别人，本身没有构成
            entry_style = fl.startswith(fn) and ("是也" in fl or "即是" in fl)
            # 别名体例：「月落亥宮 月在亥守命是也，**又名月朗天門**。」
            # 行首是别名所指的真名，本条名只作为「又名/一名」出现——但定义确实给出。
            alias_style = ("又名" in fl or "一名" in fl) and ("是也" in fl or "即是" in fl)
            if entry_style or alias_style:
                sourced.append({**h, "style": "glossary-entry" if entry_style else "alias"})
        if sourced:
            status, why = "defined-sourced", "本门原文给出构成（见 evidence_sourced）"
        entries.append({
            **d,
            "status": status,
            "why": why,
            "hits": len(hits),
            "evidence_sourced": sourced,
            "evidence_mentions": hits[:3] if status == "mention-only" else [],
        })

    counts: dict[str, int] = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1

    out = {
        "report": "executable 层命名定义的可得性（只登记，不写定义）",
        "generated_by": "t183",
        "method": f"逐名检索 sources/fulltext 下 {n_files} 份全文；本门=ziwei 书。",
        "contract": ("按「原文没写就不写」：`absent` 与 `mention-only` 两类**必须留空**，"
                     "不得据别门散文或常识补写定义。"),
        "unrelated_gap": {
            "liuyao.structure": {
                "status": "undefined-everywhere",
                "why": ("17 条 executable 记录以 {exists: \"liuyao.structure\"} 为 when，"
                        "但该名在**两个仓**里都只被使用、从未被定义（古籍仓与产品仓均无定义处；"
                        "归档的早期 worktree 里同样只是使用）。"),
                "why_not_guessed": ("其 17 个使用者各自的 required_facts 已列出具体子事实，"
                                    "其中 liuyao.node.element（爻五行）与 liuyao.node.state（爻旺衰／空墓）"
                                    "**引擎未产出** —— 故今天连「如实定义它」都构造不出来。"),
                "disposition": "保持未定义；不猜。需要定义者给出它到底指哪些事实。",
            }
        },
        "counts": {"total": len(entries), **counts},
        "entries": entries,
    }
    path = ROOT / args.out
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{path.relative_to(ROOT)}：{len(entries)} 条命名定义")
    print("  三态:", counts)
    for e in entries:
        if e["status"] == "defined-sourced":
            print(f"    ★ 可据原文定义：{e['name']}（{e['record']}）→ {e['evidence_sourced'][0]['rel']} L{e['evidence_sourced'][0]['line']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())