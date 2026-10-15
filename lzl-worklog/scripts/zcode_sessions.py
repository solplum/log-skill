"""Read-only ZCode session listing — same query the skill embeds.

Usage:
    python zcode_sessions.py <START_MS> [db_path]
"""

from __future__ import annotations

import datetime
import json
import os
import pathlib
import sqlite3
import sys


def default_db_path() -> str:
    return os.path.expanduser("~/.zcode/cli/db/db.sqlite")


def list_sessions(db_path: str, start_ms: int) -> list[str]:
    lines: list[str] = []
    con = sqlite3.connect(pathlib.Path(db_path).as_uri() + "?mode=ro", uri=True)
    cur = con.cursor()
    for sid, title, d, tc in cur.execute(
        "SELECT id, title, directory, time_created FROM session "
        "WHERE time_updated >= ? ORDER BY time_created",
        (start_ms,),
    ).fetchall():
        lines.append(
            f"== {datetime.datetime.fromtimestamp(tc / 1000):%m-%d %H:%M}  "
            f"{title or '(无标题)'}  [{d}]"
        )
        for (p,) in cur.execute(
            """SELECT p.data FROM part p JOIN message m ON p.message_id = m.id
            WHERE p.session_id = ? AND json_extract(m.data,'$.role') = 'user'
              AND json_extract(p.data,'$.type') = 'text'
              AND COALESCE(json_extract(p.data,'$.synthetic'), 0) = 0
            ORDER BY p.time_created""",
            (sid,),
        ):
            t = json.loads(p).get("text", "").strip()
            if t:
                lines.append("  U> " + t[:120].replace("\n", " "))
        tools = cur.execute(
            """SELECT DISTINCT json_extract(data,'$.tool') FROM part
            WHERE session_id = ? AND json_extract(data,'$.type') = 'tool'""",
            (sid,),
        ).fetchall()
        lines.append(
            "  tools: " + ", ".join(sorted(str(t[0]) for t in tools if t[0]))
        )
    con.close()
    return lines


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    start_ms = int(args[0]) if args else 0
    db = args[1] if len(args) > 1 else default_db_path()
    if not os.path.exists(db):
        print(f"skip: {db} not found", file=sys.stderr)
        return 0
    for line in list_sessions(db, start_ms):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
