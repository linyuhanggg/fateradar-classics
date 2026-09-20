#!/usr/bin/env python3
"""`tools/audit-contract.py` 的回归测试。

审计本身也要被审计：**一个从不报错的审计等于没有审计**。
所以这里既跑正例（当前树必须通过），也跑反例（故意破坏后必须报红）——

  1. 正例：当前树 → exit 0，且 applicable_to 变动全部有出处；
  2. 反例 A：改一条 `statement` → 必须报「受保护字段违规」；
  3. 反例 B：把一条 `applicable_to` 改成台账里没有的谓词 → 必须报「无台账出处」；
  4. 反例 C：基线引用不存在 → 必须**报错退出**，不得静默把基线当空文件
     （这正是本工具初版的缺陷：绝对路径传给 `git show` 取不到内容，
     于是报出「55 份 book 块都变了、新增 1356 条规则」这种全盘失真结果）。

所有破坏都在 `finally` 里还原，并与原字节比对。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools/audit-contract.py"
# 选一条**已映射**规则做反例：它的 applicable_to 在台账里有出处，便于精确制造「无出处」。
TARGET = ROOT / "references/books/bazi/sanming-tonghui/rules.yaml"

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def run(*args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(AUDIT), *args], cwd=ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def run_json(*args: str) -> dict:
    _rc, out = run("--json", *args)
    start = out.find("{")
    return json.loads(out[start:]) if start >= 0 else {}


def main() -> int:
    print("1. 正例：当前树必须通过")
    rc, out = run()
    check("  exit 0", rc, 0)
    rep = run_json()
    check("  受保护字段违规 0", rep.get("protected_violations"), [])
    check("  无台账出处的变动 0", rep.get("untraced_changes"), [])
    check("  新增/删除规则 0/0", (len(rep.get("rules_added") or []), len(rep.get("rules_removed") or [])), (0, 0))
    check("  verified:true 行数 0", rep.get("verified_true_lines"), 0)
    check("  applicable_to 变动数 > 100（确有施工）", rep.get("applicable_to_changed", 0) > 100, True)

    print("2. 反例 A：改 statement → 必须报受保护字段违规")
    orig = TARGET.read_text(encoding="utf-8")
    try:
        TARGET.write_text(orig.replace("statement:", "statement: （被审计测试改过）", 1), encoding="utf-8")
        rep = run_json()
        hit = [v for v in rep.get("protected_violations") or [] if ".statement 变了" in v]
        check("  报出 statement 变动", len(hit) >= 1, True)
        rc, _ = run()
        check("  exit 非 0", rc != 0, True)
    finally:
        TARGET.write_text(orig, encoding="utf-8")
    check("  已还原（逐字节相同）", TARGET.read_text(encoding="utf-8") == orig, True)

    print("3. 反例 B：applicable_to 改成台账没有的谓词 → 必须报无出处")
    try:
        TARGET.write_text(
            orig.replace(
                "  applicable_to: {any_of: [{all_of: [{key: zhi, value: 申}, {key: zhi, value: 子}, {key: zhi, value: 辰}]}",
                "  applicable_to: [{key: zhi, value: 亥}]\n  # 故意破坏\n  _x: {any_of: [{all_of: [{key: zhi, value: 申}, {key: zhi, value: 子}, {key: zhi, value: 辰}]}",
                1,
            ),
            encoding="utf-8",
        )
        rep = run_json()
        check("  报出台账不一致或无出处", rc if False else bool(rep.get("untraced_changes") or rep.get("ledger_mismatches")), True)
    finally:
        TARGET.write_text(orig, encoding="utf-8")
    check("  已还原", TARGET.read_text(encoding="utf-8") == orig, True)

    print("4. 反例 C：基线引用不存在 → 必须报错退出，不得静默当空文件")
    rc, out = run("--base", "deadbeefdeadbeef")
    check("  exit 非 0", rc != 0, True)
    check(
        "  有明确报错信息",
        any(k in out for k in ("基线引用不存在", "无内容", "基线引用或路径不对")),
        True,
    )

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL CONTRACT-AUDIT OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())