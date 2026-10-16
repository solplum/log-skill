"""Drive the shipped alllog path resolver — not a reimplementation."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "lzl-alllog" / "scripts"))

import paths  # noqa: E402


class ResolveDataRootTests(unittest.TestCase):
    def test_env_var_wins_over_default(self) -> None:
        custom = "/tmp/resume-materials-custom"
        got = paths.resolve_data_root({paths.ENV_VAR: custom, "HOME": "/home/someone"})
        self.assertEqual(got, Path(custom))

    def test_primary_env_var_wins_over_fallback(self) -> None:
        primary = "/tmp/resume-materials-primary"
        fallback = "/tmp/resume-materials-fallback"
        got = paths.resolve_data_root({
            paths.PRIMARY_ENV_VAR: primary,
            paths.ENV_VAR: fallback,
            "HOME": "/home/someone",
        })
        self.assertEqual(got, Path(primary))

    def test_empty_env_falls_back_to_home_alllog(self) -> None:
        got = paths.resolve_data_root({paths.ENV_VAR: "   ", "HOME": "/home/someone"})
        self.assertEqual(got, Path.home() / "alllog")

    def test_missing_env_falls_back_to_home_alllog(self) -> None:
        got = paths.resolve_data_root({})
        self.assertEqual(got, Path.home() / "alllog")

    def test_journal_and_digest_layout(self) -> None:
        root = Path("/data/alllog-root")
        self.assertEqual(paths.journal_path("2026-08-17", root), root / "素材" / "日志" / "2026-08-17.md")
        self.assertEqual(paths.digest_path("2026-08-17", root), root / "素材" / "整理" / "2026-08-17.md")

    def test_cli_prints_resolved_root(self) -> None:
        env = os.environ.copy()
        env[paths.ENV_VAR] = str(Path("/tmp/alllog-cli-root"))
        proc = subprocess.run(
            [sys.executable, str(REPO / "lzl-alllog" / "scripts" / "paths.py")],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(proc.stdout.strip(), str(Path("/tmp/alllog-cli-root")))

    def test_cli_journal_and_digest(self) -> None:
        env = os.environ.copy()
        root = Path("/tmp/alllog-cli-root")
        env[paths.ENV_VAR] = str(root)
        script = str(REPO / "lzl-alllog" / "scripts" / "paths.py")
        jr = subprocess.run(
            [sys.executable, script, "--journal", "2026-08-01"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        dg = subprocess.run(
            [sys.executable, script, "--digest", "2026-08-01"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(jr.stdout.strip(), str(root / "素材" / "日志" / "2026-08-01.md"))
        self.assertEqual(dg.stdout.strip(), str(root / "素材" / "整理" / "2026-08-01.md"))

    def test_latest_journal_day_reads_only_journal_files(self) -> None:
        with __import__("tempfile").TemporaryDirectory() as tmp:
            root = Path(tmp)
            journal = paths.journal_dir(root)
            journal.mkdir(parents=True)
            (journal / "2026-08-01.md").write_text("a", encoding="utf-8")
            (journal / "2026-08-09.md").write_text("b", encoding="utf-8")
            self.assertEqual(paths.latest_journal_day(root), "2026-08-09")
            empty = Path(tmp) / "empty-root"
            (paths.journal_dir(empty)).mkdir(parents=True)
            self.assertIsNone(paths.latest_journal_day(empty))


if __name__ == "__main__":
    unittest.main()
