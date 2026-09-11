#!/usr/bin/env python3
"""Export reviewed chart-reading notes; quoted text must match its source lines."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTS = {"bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng", "meihua", "xiaoliuren"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist/readings/chart-notes.json")
    args = parser.parse_args()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    def committed_text(path):
        return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT, text=True)
    data = json.loads(committed_text("references/readings/chart-notes.json"))
    data["sourceRevision"] = revision
    seen = set()
    for note in data["notes"]:
        if note["id"] in seen or note["art"] not in ARTS:
            raise ValueError(f"Invalid or duplicate reading note: {note['id']}")
        seen.add(note["id"])
        if not note["title"].strip() or not note["body"].strip():
            raise ValueError(f"Empty reading note: {note['id']}")
        source = note["source"]
        if source["kind"] == "anchored_text":
            anchor = source["anchor"]
            lines = committed_text(anchor["file"]).splitlines()
            start, end = anchor["startLine"], anchor["endLine"]
            if not 1 <= start <= end <= len(lines):
                raise ValueError(f"Invalid source lines: {note['id']}")
            quote = "\n".join(lines[start - 1:end])
            if not source["quote"].strip() or quote != source["quote"]:
                raise ValueError(f"Quote mismatch: {note['id']}")
        elif source["kind"] != "implementation_note" or "anchor" in source or "quote" in source:
            raise ValueError(f"Invalid source kind: {note['id']}")
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Exported {len(seen)} reading notes to {output}")


if __name__ == "__main__":
    main()
