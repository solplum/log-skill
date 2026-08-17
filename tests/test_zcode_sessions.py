"""Drive the shipped ZCode listing query against a real SQLite file."""

from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "worklog" / "scripts"))

import zcode_sessions  # noqa: E402


def _build_db(path: Path) -> None:
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE session (
            id TEXT PRIMARY KEY,
            title TEXT,
            directory TEXT,
            time_created INTEGER,
            time_updated INTEGER
        );
        CREATE TABLE message (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            data TEXT
        );
        CREATE TABLE part (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            message_id TEXT,
            data TEXT,
            time_created INTEGER
        );
        """
    )
    # in-range session
    cur.execute(
        "INSERT INTO session VALUES (?,?,?,?,?)",
        ("s-in", "login remember-me", "/workspace/demo", 1_723_449_600_000, 1_723_449_600_000),
    )
    cur.execute("INSERT INTO message VALUES (?,?,?)", ("m1", "s-in", json.dumps({"role": "user"})))
    cur.execute(
        "INSERT INTO part VALUES (?,?,?,?,?)",
        ("p1", "s-in", "m1", json.dumps({"type": "text", "text": "add remember-me checkbox"}), 1),
    )
    cur.execute(
        "INSERT INTO part VALUES (?,?,?,?,?)",
        ("p-syn", "s-in", "m1", json.dumps({"type": "text", "text": "injected", "synthetic": 1}), 2),
    )
    cur.execute(
        "INSERT INTO part VALUES (?,?,?,?,?)",
        ("p-tool", "s-in", "m1", json.dumps({"type": "tool", "tool": "Read"}), 3),
    )
    # out-of-range session
    cur.execute(
        "INSERT INTO session VALUES (?,?,?,?,?)",
        ("s-old", "old work", "/workspace/old", 1_000, 1_000),
    )
    cur.execute("INSERT INTO message VALUES (?,?,?)", ("m-old", "s-old", json.dumps({"role": "user"})))
    cur.execute(
        "INSERT INTO part VALUES (?,?,?,?,?)",
        ("p-old", "s-old", "m-old", json.dumps({"type": "text", "text": "should not appear"}), 1),
    )
    con.commit()
    con.close()


class ZcodeSessionQueryTests(unittest.TestCase):
    def test_filters_start_ms_and_synthetic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "db.sqlite"
            _build_db(db)
            lines = zcode_sessions.list_sessions(str(db), 1_723_000_000_000)
            text = "\n".join(lines)
            self.assertIn("login remember-me", text)
            self.assertIn("add remember-me checkbox", text)
            self.assertIn("Read", text)
            self.assertNotIn("should not appear", text)
            self.assertNotIn("injected", text)
            self.assertNotIn("old work", text)

    def test_zero_start_includes_all_real_user_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "db.sqlite"
            _build_db(db)
            text = "\n".join(zcode_sessions.list_sessions(str(db), 0))
            self.assertIn("login remember-me", text)
            self.assertIn("old work", text)
            self.assertNotIn("injected", text)


if __name__ == "__main__":
    unittest.main()
