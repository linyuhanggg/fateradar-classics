#!/usr/bin/env python3
"""Lease, claim, and git-push concurrency tests. No live remotes required."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import cursor_classics_lease as lease


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise AssertionError(f"git {args} failed: {proc.stdout}{proc.stderr}")
    return proc


class LeaseLogic(unittest.TestCase):
    def setUp(self) -> None:
        self.now = 1_000_000.0
        self.progress = lease.empty_progress(
            package_id="demo",
            file="demo.json",
            source_hash="abc",
            remaining_ids=["A", "B", "C", "D"],
            completed_ids=[],
        )

    def test_first_holder_acquires_empty_lease(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        self.assertEqual(self.progress["lease"]["holderId"], "run-1")
        self.assertTrue(lease.lease_valid(self.progress["lease"], self.now + 10))

    def test_foreign_valid_lease_is_not_preempted(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        ok, reason = lease.can_acquire(self.progress, "run-2", self.now + 30)
        self.assertFalse(ok)
        self.assertEqual(reason, "foreign-lease-active")
        with self.assertRaises(PermissionError):
            lease.acquire_lease(self.progress, holder_id="run-2", run_branch="b2", now=self.now + 30)

    def test_same_holder_can_refresh_without_losing_in_progress(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        taken = lease.claim_ids(self.progress, "run-1", self.now, 2)
        self.assertEqual(taken, ["A", "B"])
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now + 20)
        self.assertEqual(self.progress["package"]["inProgressIds"], ["A", "B"])
        self.assertEqual(self.progress["package"]["crashRecoveredIds"], [])

    def test_expired_lease_can_be_recovered_and_returns_unfinished_ids(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now, ttl_seconds=60)
        lease.claim_ids(self.progress, "run-1", self.now, 2)
        later = self.now + 120
        ok, reason = lease.can_acquire(self.progress, "run-2", later)
        self.assertTrue(ok)
        self.assertEqual(reason, "expired-or-absent")
        lease.acquire_lease(self.progress, holder_id="run-2", run_branch="b2", now=later, ttl_seconds=60)
        self.assertEqual(self.progress["lease"]["holderId"], "run-2")
        self.assertEqual(self.progress["package"]["inProgressIds"], [])
        self.assertEqual(self.progress["package"]["remainingIds"], ["C", "D", "A", "B"])
        self.assertEqual(self.progress["package"]["crashRecoveredIds"], ["A", "B"])

    def test_stale_heartbeat_is_treated_as_crash_even_if_ttl_not_hit(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now,
                            ttl_seconds=10_000, stale_seconds=90)
        later = self.now + 120
        ok, reason = lease.can_acquire(self.progress, "run-2", later, stale_seconds=90)
        self.assertTrue(ok)
        self.assertEqual(reason, "expired-or-absent")

    def test_foreign_holder_cannot_heartbeat_or_complete(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        with self.assertRaises(PermissionError):
            lease.heartbeat_lease(self.progress, "run-2", self.now + 5)
        with self.assertRaises(PermissionError):
            lease.complete_ids(self.progress, "run-2", self.now + 5, ["A"])

    def test_completed_ids_are_not_reclaimed(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        first = lease.claim_ids(self.progress, "run-1", self.now, 2)
        lease.complete_ids(self.progress, "run-1", self.now, first)
        again = lease.claim_ids(self.progress, "run-1", self.now, 10)
        self.assertEqual(again, ["C", "D"])
        self.assertEqual(lease.claim_ids(self.progress, "run-1", self.now, 10), [])
        self.assertEqual(self.progress["package"]["completedIds"], ["A", "B"])

    def test_release_allows_next_worker(self) -> None:
        lease.acquire_lease(self.progress, holder_id="run-1", run_branch="b1", now=self.now)
        lease.release_lease(self.progress, "run-1", self.now + 1)
        lease.acquire_lease(self.progress, holder_id="run-2", run_branch="b2", now=self.now + 2)
        self.assertEqual(self.progress["lease"]["holderId"], "run-2")


class TemplateAudit(unittest.TestCase):
    def test_detector_flags_原文_dumps_only(self) -> None:
        self.assertTrue(lease.is_copy_template("元理赋节。原文：两干不杂。"))
        self.assertFalse(lease.is_copy_template("两干不杂不可一概言贵，缺格局则不定贵。"))

    def test_sk1610_completed_ids_are_not_still_templates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        path = root / "references/annotations/bazi/sanming-tonghui--shidian-SK1610.json"
        progress = json.loads((root / lease.PROGRESS_REL).read_text())
        data = json.loads(path.read_text())
        good, templates = lease.annotation_template_ids(path)
        self.assertEqual(len(data["entries"]), 322)
        self.assertEqual(len(good) + len(templates), 322)
        self.assertTrue(all(entry.get("verified") is False for entry in data["entries"]))
        completed = set(progress["package"].get("completedIds") or [])
        in_progress = set(progress["package"].get("inProgressIds") or [])
        by_id = {entry["paragraphId"]: entry for entry in data["entries"]}
        for pid in completed | in_progress:
            self.assertIn(pid, by_id)
            self.assertFalse(lease.is_copy_template(by_id[pid]["vernacular"]), pid)
        # Baseline defect was 281; this file must not silently grow templates.
        self.assertLessEqual(len(templates), 281)
        self.assertEqual(len(templates), 281 - len(completed) - len([
            pid for pid in in_progress if pid not in completed
        ]))


class Sk1610UnresolvedSource(unittest.TestCase):
    def test_page_cut_glyphs_stay_unknown_while_source_truncated(self) -> None:
        root = Path(__file__).resolve().parents[1]
        path = root / "references/annotations/bazi/sanming-tonghui--shidian-SK1610.json"
        lines = (root / "sources/normalized/shidianguji/SK1610/text.md").read_text().splitlines()
        data = json.loads(path.read_text())
        by_id = {entry["paragraphId"]: entry for entry in data["entries"]}
        lan = "sanming-tonghui:shidian-SK1610:P7426253719257333769"
        da = "sanming-tonghui:shidian-SK1610:P7426253719907549193"
        self.assertTrue(lines[1588].startswith("欄"), lines[1588][:20])
        self.assertTrue(lines[1846].endswith("必膺大"), lines[1846][-12:])
        self.assertEqual(by_id[lan]["kind"], "待核实")
        self.assertEqual(by_id[da]["kind"], "待核实")
        self.assertTrue(all(entry.get("verified") is False for entry in data["entries"]))
        self.assertNotEqual(by_id[lan].get("kind"), "规则候选")
        self.assertFalse(lease.is_copy_template(by_id[lan]["vernacular"]))
        self.assertFalse(lease.is_copy_template(by_id[da]["vernacular"]))


class GitPushCompetition(unittest.TestCase):
    def test_second_ordinary_push_loses_and_does_not_force(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            remote = base / "remote.git"
            seed = base / "seed"
            git(base, "init", "--bare", str(remote))
            git(base, "clone", str(remote), str(seed))
            git(seed, "checkout", "-b", "codex/cursor-classics-autonomy-state")
            git(seed, "config", "user.email", "seed@example.com")
            git(seed, "config", "user.name", "seed")
            (seed / "docs/automation").mkdir(parents=True)
            lease.dump_json(seed / lease.PROGRESS_REL, lease.empty_progress(
                package_id="demo", file="demo.json", source_hash="abc",
                remaining_ids=["A"], completed_ids=[],
            ))
            git(seed, "add", lease.PROGRESS_REL)
            git(seed, "commit", "-m", "seed progress")
            git(seed, "push", "-u", "origin", "codex/cursor-classics-autonomy-state")

            a = base / "a"
            b = base / "b"
            git(base, "clone", "-b", "codex/cursor-classics-autonomy-state", str(remote), str(a))
            git(base, "clone", "-b", "codex/cursor-classics-autonomy-state", str(remote), str(b))
            git(a, "config", "user.email", "lease-a@example.com")
            git(a, "config", "user.name", "lease-a")
            git(b, "config", "user.email", "lease-b@example.com")
            git(b, "config", "user.name", "lease-b")

            progress = json.loads((a / lease.PROGRESS_REL).read_text())
            lease.acquire_lease(progress, holder_id="run-a", run_branch="run-a", now=1.0)
            lease.dump_json(a / lease.PROGRESS_REL, progress)
            git(a, "add", lease.PROGRESS_REL)
            git(a, "commit", "-m", "lease a")
            status, _ = lease.try_push_state(a, "origin", "codex/cursor-classics-autonomy-state")
            self.assertEqual(status, "ok")

            other = json.loads((b / lease.PROGRESS_REL).read_text())
            lease.acquire_lease(other, holder_id="run-b", run_branch="run-b", now=2.0)
            lease.dump_json(b / lease.PROGRESS_REL, other)
            git(b, "add", lease.PROGRESS_REL)
            git(b, "commit", "-m", "lease b")
            status, message = lease.try_push_state(b, "origin", "codex/cursor-classics-autonomy-state")
            self.assertEqual(status, "non-fast-forward")
            self.assertNotIn("--force", message)
            git(b, "fetch", "origin", "codex/cursor-classics-autonomy-state")
            fetched = json.loads(git(b, "show", "origin/codex/cursor-classics-autonomy-state:" + lease.PROGRESS_REL).stdout)
            self.assertEqual(fetched["lease"]["holderId"], "run-a")
            ok, reason = lease.can_acquire(fetched, "run-b", 2.0)
            self.assertFalse(ok)
            self.assertEqual(reason, "foreign-lease-active")


if __name__ == "__main__":
    unittest.main()
