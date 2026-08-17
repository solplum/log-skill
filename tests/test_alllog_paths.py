"""Drive the shipped alllog path resolver — not a reimplementation."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "alllog" / "scripts"))

import paths  # noqa: E402


class ResolveDataRootTests(unittest.TestCase):
    def test_env_var_wins_over_default(self) -> None:
        custom = "/tmp/resume-materials-custom"
        got = paths.resolve_data_root({paths.ENV_VAR: custom, "HOME": "/home/someone"})
        self.assertEqual(got, Path(custom))

    def test_empty_env_falls_back_to_home_alllog(self) -> None:
        got = paths.resolve_data_root({paths.ENV_VAR: "   ", "HOME": "/home/someone"})
        self.assertEqual(got, Path.home() / "alllog")

    def test_missing_env_falls_back_to_home_alllog(self) -> None:
        got = paths.resolve_data_root({})
        self.assertEqual(got, Path.home() / "alllog")

    def test_material_and_library_layout(self) -> None:
        root = Path("/data/alllog-root")
        self.assertEqual(paths.material_path("2026-08-17", root), root / "素材" / "2026-08-17.md")
        self.assertEqual(paths.library_path(root), root / "简历素材库.md")

    def test_cli_prints_resolved_root(self) -> None:
        env = os.environ.copy()
        env[paths.ENV_VAR] = str(Path("/tmp/alllog-cli-root"))
        proc = subprocess.run(
            [sys.executable, str(REPO / "alllog" / "scripts" / "paths.py")],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(proc.stdout.strip(), str(Path("/tmp/alllog-cli-root")))

    def test_cli_material_and_library(self) -> None:
        env = os.environ.copy()
        root = Path("/tmp/alllog-cli-root")
        env[paths.ENV_VAR] = str(root)
        script = str(REPO / "alllog" / "scripts" / "paths.py")
        lib = subprocess.run(
            [sys.executable, script, "--library"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        mat = subprocess.run(
            [sys.executable, script, "--material", "2026-08-01"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(lib.stdout.strip(), str(root / "简历素材库.md"))
        self.assertEqual(mat.stdout.strip(), str(root / "素材" / "2026-08-01.md"))


if __name__ == "__main__":
    unittest.main()
