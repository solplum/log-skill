"""Resolve alllog's user-configurable data root and file layout.

The skill never hardcodes a machine path. Callers (the agent, or this
module's CLI) resolve the root the same way:

1. ``ALLLOG_DATA_ROOT`` if set and non-empty
2. otherwise ``~/alllog``

Layout under the root (``素材`` = material):

- ``素材/日志/<day>.md``  journal — append-only capture/mine output, the only source of truth
- ``素材/整理/<day>.md``  digest — per-project snapshot regenerated per day, never read back by alllog
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ENV_VAR = "ALLLOG_DATA_ROOT"
DEFAULT_DIRNAME = "alllog"


def resolve_data_root(env: dict[str, str] | None = None) -> Path:
    source = os.environ if env is None else env
    raw = (source.get(ENV_VAR) or "").strip()
    if raw:
        return Path(raw).expanduser()
    return Path.home() / DEFAULT_DIRNAME


def journal_dir(root: Path | None = None) -> Path:
    return (root or resolve_data_root()) / "素材" / "日志"


def journal_path(day: str, root: Path | None = None) -> Path:
    return journal_dir(root) / f"{day}.md"


def digest_dir(root: Path | None = None) -> Path:
    return (root or resolve_data_root()) / "素材" / "整理"


def digest_path(day: str, root: Path | None = None) -> Path:
    return digest_dir(root) / f"{day}.md"


def latest_journal_day(root: Path | None = None) -> str | None:
    """Newest ``YYYY-MM-DD`` journal file name (without extension), or None."""
    days = sorted(p.stem for p in journal_dir(root).glob("*.md"))
    return days[-1] if days else None


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = resolve_data_root()
    if args and args[0] == "--journal" and len(args) >= 2:
        print(journal_path(args[1], root))
        return 0
    if args and args[0] == "--digest" and len(args) >= 2:
        print(digest_path(args[1], root))
        return 0
    if args and args[0] == "--latest":
        day = latest_journal_day(root)
        print(day if day else "(日志/ 为空)")
        return 0
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
