#!/usr/bin/env python3
"""Cross-run lease and paragraph-claim helpers for cursor-native-classics.

Concurrency is enforced by ordinary git fast-forward pushes, not by prompt
assumptions. A valid foreign lease is never preempted. Crash recovery only
happens after TTL expiry or a stale heartbeat.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any

WORKER = "cursor-native-classics"
STATE_BRANCH = "codex/cursor-classics-autonomy-state"
PROGRESS_REL = "docs/automation/CURSOR_CLASSICS_PROGRESS.json"
QUEUE_REL = "docs/automation/CURSOR_CLASSICS_QUEUE.json"
DEFAULT_TTL_SECONDS = 3 * 60 * 60
DEFAULT_STALE_SECONDS = 90 * 60
FORBIDDEN_FILES = (
    "references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json",
    "references/annotations/selection/yuqia-ji.json",
    "references/annotations/selection/yuqia-ji--shidian-DZ1480.json",
    "references/annotations/bazi/yuanhai-ziping--shidian-NGJ892411999032112149610.json",
    "references/annotations/divination/bushi-zhengzong--shidian-HY0057.json",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_copy_template(vernacular: str) -> bool:
    text = vernacular or ""
    return "原文：" in text or text.lstrip().startswith("原文")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def lease_valid(lease: dict[str, Any] | None, now: float, stale_seconds: int = DEFAULT_STALE_SECONDS) -> bool:
    if not isinstance(lease, dict):
        return False
    if lease.get("status") != "active":
        return False
    expires = lease.get("expiresAt")
    heartbeat = lease.get("heartbeatAt")
    if not isinstance(expires, (int, float)) or now >= float(expires):
        return False
    if not isinstance(heartbeat, (int, float)) or now - float(heartbeat) >= stale_seconds:
        return False
    return True


def same_holder(lease: dict[str, Any] | None, holder_id: str) -> bool:
    return isinstance(lease, dict) and lease.get("holderId") == holder_id


def can_acquire(progress: dict[str, Any], holder_id: str, now: float,
                stale_seconds: int = DEFAULT_STALE_SECONDS) -> tuple[bool, str]:
    lease = progress.get("lease")
    if not lease_valid(lease, now, stale_seconds):
        return True, "expired-or-absent"
    if same_holder(lease, holder_id):
        return True, "same-holder-refresh"
    return False, "foreign-lease-active"


def acquire_lease(progress: dict[str, Any], *, holder_id: str, run_branch: str, now: float,
                  ttl_seconds: int = DEFAULT_TTL_SECONDS, stale_seconds: int = DEFAULT_STALE_SECONDS,
                  extra: dict[str, Any] | None = None) -> dict[str, Any]:
    ok, reason = can_acquire(progress, holder_id, now, stale_seconds)
    if not ok:
        raise PermissionError(reason)
    lease = {
        "status": "active",
        "worker": WORKER,
        "holderId": holder_id,
        "runBranch": run_branch,
        "acquiredAt": now if reason != "same-holder-refresh" else progress["lease"].get("acquiredAt", now),
        "heartbeatAt": now,
        "expiresAt": now + ttl_seconds,
        "ttlSeconds": ttl_seconds,
        "staleSeconds": stale_seconds,
        "acquireReason": reason,
    }
    if extra:
        lease.update(extra)
    if reason != "same-holder-refresh":
        # Crash recovery: unfinished claims return to remaining.
        package = progress.setdefault("package", {})
        in_progress = list(package.get("inProgressIds") or [])
        remaining = list(package.get("remainingIds") or [])
        completed = set(package.get("completedIds") or [])
        returned = [pid for pid in in_progress if pid not in completed and pid not in remaining]
        package["remainingIds"] = remaining + returned
        package["inProgressIds"] = []
        package["crashRecoveredIds"] = returned
    progress["lease"] = lease
    progress["worker"] = WORKER
    progress["updatedAt"] = now
    return progress


def heartbeat_lease(progress: dict[str, Any], holder_id: str, now: float,
                    ttl_seconds: int = DEFAULT_TTL_SECONDS) -> dict[str, Any]:
    lease = progress.get("lease")
    if not same_holder(lease, holder_id):
        raise PermissionError("not-holder")
    if not lease_valid(lease, now, lease.get("staleSeconds", DEFAULT_STALE_SECONDS)):
        raise PermissionError("lease-not-valid")
    lease["heartbeatAt"] = now
    lease["expiresAt"] = now + ttl_seconds
    progress["updatedAt"] = now
    return progress


def release_lease(progress: dict[str, Any], holder_id: str, now: float) -> dict[str, Any]:
    lease = progress.get("lease")
    if not same_holder(lease, holder_id):
        raise PermissionError("not-holder")
    lease["status"] = "released"
    lease["releasedAt"] = now
    progress["updatedAt"] = now
    return progress


def claim_ids(progress: dict[str, Any], holder_id: str, now: float, limit: int) -> list[str]:
    if not same_holder(progress.get("lease"), holder_id) or not lease_valid(progress.get("lease"), now):
        raise PermissionError("need-valid-own-lease")
    package = progress.setdefault("package", {})
    completed = set(package.get("completedIds") or [])
    in_progress = list(package.get("inProgressIds") or [])
    remaining = [pid for pid in (package.get("remainingIds") or []) if pid not in completed and pid not in in_progress]
    taken = remaining[: max(0, int(limit))]
    package["remainingIds"] = remaining[len(taken):]
    package["inProgressIds"] = in_progress + taken
    progress["updatedAt"] = now
    return taken


def complete_ids(progress: dict[str, Any], holder_id: str, now: float, ids: list[str]) -> list[str]:
    if not same_holder(progress.get("lease"), holder_id):
        raise PermissionError("not-holder")
    package = progress.setdefault("package", {})
    completed = list(package.get("completedIds") or [])
    in_progress = list(package.get("inProgressIds") or [])
    remaining = list(package.get("remainingIds") or [])
    done: list[str] = []
    for pid in ids:
        if pid in completed:
            continue
        completed.append(pid)
        done.append(pid)
        if pid in in_progress:
            in_progress.remove(pid)
        if pid in remaining:
            remaining.remove(pid)
    package["completedIds"] = completed
    package["inProgressIds"] = in_progress
    package["remainingIds"] = remaining
    progress["updatedAt"] = now
    return done


def annotation_template_ids(path: Path) -> tuple[list[str], list[str]]:
    data = load_json(path)
    good: list[str] = []
    templates: list[str] = []
    for entry in data.get("entries") or []:
        pid = entry.get("paragraphId")
        if not isinstance(pid, str):
            continue
        if is_copy_template(entry.get("vernacular") or ""):
            templates.append(pid)
        else:
            good.append(pid)
    return good, templates


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)


def try_push_state(cwd: Path, remote: str, branch: str) -> tuple[str, str]:
    """Ordinary push only. Never force. Non-fast-forward means a concurrent worker."""
    pushed = run_git(["push", remote, f"HEAD:{branch}"], cwd)
    if pushed.returncode == 0:
        return "ok", pushed.stdout + pushed.stderr
    combined = (pushed.stdout + pushed.stderr).lower()
    if "non-fast-forward" in combined or "fetch first" in combined or "rejected" in combined:
        return "non-fast-forward", pushed.stdout + pushed.stderr
    return "error", pushed.stdout + pushed.stderr


def empty_progress(*, package_id: str, file: str, source_hash: str, remaining_ids: list[str],
                   completed_ids: list[str] | None = None) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "worker": WORKER,
        "lease": None,
        "package": {
            "id": package_id,
            "file": file,
            "assignedPathHint": "references/annotations/xingming/xingxue-dacheng--shidian-SK1610.json",
            "status": "in_progress",
            "accepted": False,
            "sourceHash": source_hash,
            "completedIds": list(completed_ids or []),
            "inProgressIds": [],
            "remainingIds": list(remaining_ids),
            "crashRecoveredIds": [],
        },
        "testEvidence": [],
        "notes": [],
        "updatedAt": None,
    }
