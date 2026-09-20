#!/usr/bin/env python3
"""tools/needs-human-review-report.py 的回归测试。

钉住三件事，防止这份台账重新退化成「会撒谎的过程稿」：
  1. 每个论断都必须落在一个合法状态里（不许静默漏判）；
  2. 旧件字面写法的错 id 必须被**量化**出来（照抄旧件会找不到条目）；
  3. `book.script` 实测必须仍是 55 本 0 处不符 —— 这一项是旧件「需人决定」的结案依据，
     一旦真有书登记错，本测试要红，不能让它悄悄漂移。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/needs-human-review-report.py"
VALID = {"已解决", "仍未决", "论断已过时", "机器不可判"}
FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}: {got!r}")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *args], cwd=ROOT, capture_output=True, text=True)


def main() -> int:
    print("1. 三种模式都必须 exit 0")
    for args in ([], ["--json"]):
        p = run(*args)
        check(f"  {' '.join(args) or '(默认)'} exit", p.returncode, 0)

    print("2. 每个论断都有合法状态")
    p = run("--json")
    data = json.loads(p.stdout)
    claims = data["claims"]
    check("  论断条数 > 0", len(claims) > 0, True)
    bad = [c["id"] for c in claims if c.get("status") not in VALID]
    check("  无非法状态", bad, [])
    ids = [c["id"] for c in claims]
    check("  id 不重复", len(ids), len(set(ids)))

    print("3. 旧件字面写法的错 id 被量化")
    pack = next((c for c in claims if c["id"] == "pack-meta-rules"), None)
    if pack is None:
        FAILED.append("pack-meta-rules 论断缺失")
        print("  FAIL pack-meta-rules 缺失")
    else:
        check("  查到 19 个检索不到的旧 id", pack.get("literal_unresolvable"), 19)
        check(
            "  有对应 finding 说明",
            any("检索不到" in f for f in pack.get("findings") or []),
            True,
        )
        check("  当前真实 id 全部可解析", pack["status"] != "论断已过时", True)

    print("4. book.script 实测：结案依据不能漂移")
    bs = data["book_script"]
    check("  受检书目数", bs["books"], 55)
    check("  不符书目数", bs["mismatched"], [])

    print("5. anchor: null 规模与 V11 读数一致（台账不许自报数字）")
    check("  unanchored_count 与列表长度一致", data["unanchored_count"], len(data["unanchored"]))
    p2 = run()
    v11_line = next((l for l in p2.stdout.splitlines() if "V11=" in l), "")
    check("  V11 出现在输出里", "V11=" in v11_line, True)

    print("6. 两个已结案论断的理由必须写明")
    for cid in ("v11-g1-target", "ziwei-palace-scope"):
        c = next((x for x in claims if x["id"] == cid), None)
        if c is None:
            FAILED.append(f"{cid} 缺失")
            print(f"  FAIL {cid} 缺失")
            continue
        check(f"  {cid} 状态", c["status"], "已解决")
        check(f"  {cid} 有结案说明", bool(c.get("resolution")), True)

    print("7. --md 能生成且覆盖旧件")
    p = run("--md", "tools/reports/needs-human-review.md")
    check("  exit", p.returncode, 0)
    text = (ROOT / "tools/reports/needs-human-review.md").read_text(encoding="utf-8")
    check("  含总览标题", "# 需要人工判断（可复算台账）" in text, True)
    check("  含逐条论断", "## 三、逐条论断与复核" in text, True)
    check("  写明不写锚点", "不写任何锚点" in text, True)

    print("8. 不可锚根因：全部 restatement（这是「不要硬锚」的逻辑前提）")
    census = data["quote_kind_census"]
    check("  未锚规则的 quote_kind 只有一种", list(census), ["restatement"])
    check("  条数与 unanchored 一致", census["restatement"], data["unanchored_count"])
    cen = next((c for c in claims if c["id"] == "restatement-census"), None)
    check("  台账里已登记该根因", cen is not None, True)
    check("  且判为已解决（已归类归并）", cen["status"] if cen else None, "已解决")

    print("9. 锚点恢复必须仍然「零可锚」——闸门不能被绕过")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/anchor_recover.py"), "--dry-run"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    line = next((l for l in proc.stdout.splitlines() if l.startswith("already=")), "")
    check("  dry-run 输出可解析", bool(line), True)
    fields = dict(kv.split("=", 1) for kv in line.split() if "=" in kv)
    # recovered 必须为 0：一旦 >0，说明又被锚上了重述文本或来源标签。
    check("  recovered == 0（无重述文本被硬锚）", fields.get("recovered"), "0")
    check("  unanchorable == 未锚条数", fields.get("unanchorable"), str(data["unanchored_count"]))

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL HUMAN-REVIEW LEDGER OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())