"""Drive the shipped change-report project-name resolver."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "change-report" / "scripts"))

import project_name  # noqa: E402


class ProjectNameTests(unittest.TestCase):
    def test_unmapped_uses_git_root_directory_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "popmart-agent"
            root.mkdir()
            self.assertEqual(project_name.resolve_project_name(root, {}), "popmart-agent")

    def test_mapping_file_wins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo-on-disk"
            root.mkdir()
            mapping_path = Path(tmp) / "_projects.json"
            mapping_path.write_text(
                json.dumps({str(root): "泡泡玛特重构"}, ensure_ascii=False),
                encoding="utf-8",
            )
            mapping = project_name.load_mapping(mapping_path)
            self.assertEqual(project_name.resolve_project_name(root, mapping), "泡泡玛特重构")

    def test_cli_prints_mapped_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            root.mkdir()
            mapping_path = Path(tmp) / "_projects.json"
            mapping_path.write_text(json.dumps({str(root): "demo-alias"}), encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(REPO / "change-report" / "scripts" / "project_name.py"),
                    str(root),
                    str(mapping_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.stdout.strip(), "demo-alias")


if __name__ == "__main__":
    unittest.main()
