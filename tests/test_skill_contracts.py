"""Structural checks on the published skill files and README."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Split so this test file does not contain the forbidden literals itself.
FORBIDDEN = (
    "D:" + "\\MyAIWorkspace",
    "/d/" + "MyAIWorkspace",
    "D:" + "\\Users\\",
    "C:" + "\\Users\\20212",
)


def _read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


class PublishedSkillContractTests(unittest.TestCase):
    def test_worklog_frontmatter_and_modes(self) -> None:
        text = _read("worklog/SKILL.md")
        self.assertRegex(text, r"(?m)^name:\s*worklog\s*$")
        self.assertIn("description:", text)
        for needle in (
            "随手记录",
            "主动梳理",
            "需求叙事",
            "闸口",
            "禁止自问自答",
            "Claude Code",
            "Codex",
            "ZCode",
            "报告文档/需求/日志",
            "报告文档/需求/周报",
            "**需求背景**",
            "**方案**",
            "**落地**",
            "**结果**",
            "agent-team-contract.md",
        ):
            self.assertIn(needle, text)

    def test_alllog_frontmatter_configurable_root_and_modes(self) -> None:
        text = _read("alllog/SKILL.md")
        self.assertRegex(text, r"(?m)^name:\s*alllog\s*$")
        self.assertIn("ALLLOG_DATA_ROOT", text)
        self.assertIn("~/alllog", text)
        self.assertNotIn("D:" + "\\MyAIWorkspace", text)
        self.assertNotIn("/d/" + "MyAIWorkspace", text)
        for needle in (
            "随手记录",
            "主动梳理",
            "素材库",
            "闸口",
            "禁止自问自答",
            "仅用户手动 /alllog",
            "~/.claude/projects",
            "Codex",
            "ZCode",
            "**背景**",
            "**技术栈**",
            "**亮点/难点**",
            "**结果/量化**",
        ):
            self.assertIn(needle, text)

    def test_worklog_agent_contract_present(self) -> None:
        text = _read("worklog/references/agent-team-contract.md")
        self.assertIn("Agent-CC", text)
        self.assertIn("Agent-Codex", text)
        self.assertIn("Agent-Zcode", text)

    def test_test_notes_present(self) -> None:
        self.assertTrue((REPO / "worklog/test/test-worklog.md").is_file())
        self.assertTrue((REPO / "alllog/test/test-alllog.md").is_file())
        self.assertTrue((REPO / "worklog/test/fixtures/fake-cc-session.jsonl").is_file())
        self.assertTrue((REPO / "alllog/test/fixtures/fake-2026-08-01.md").is_file())

    def test_no_author_machine_paths(self) -> None:
        hits: list[str] = []
        for path in REPO.rglob("*"):
            if path.suffix.lower() in {".pyc", ".png", ".jpg"} or "__pycache__" in path.parts:
                continue
            if not path.is_file():
                continue
            if ".git" in path.parts or path.name.startswith("test_"):
                continue
            raw = path.read_text(encoding="utf-8", errors="replace")
            for pat in FORBIDDEN:
                if pat in raw:
                    hits.append(f"{path.relative_to(REPO)}: {pat}")
        self.assertEqual(hits, [])

    def test_readme_english_first_and_complete(self) -> None:
        text = _read("README.md")
        en = text.find("# worklog + alllog")
        zh = text.find("# worklog + alllog（中文）")
        self.assertGreaterEqual(en, 0)
        self.assertGreater(zh, en)
        for needle in (
            "~/.claude/skills/",
            "~/.codex/skills/",
            "/worklog",
            "/alllog",
            "ask then stop",
            "no self-answer",
            "Claude Code",
            "Codex",
            "ZCode",
            "ALLLOG_DATA_ROOT",
            "报告文档/需求",
            "timezone",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
