"""Resolve alllog's user-configurable data root.

The skill never hardcodes a machine path. Callers (the agent, or this
module's CLI) resolve the root the same way:

1. ``ALLLOG_DATA_ROOT`` if set and non-empty
2. otherwise ``~/alllog``
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


def material_dir(root: Path | None = None) -> Path:
    return (root or resolve_data_root()) / "素材"


def material_path(day: str, root: Path | None = None) -> Path:
    return material_dir(root) / f"{day}.md"


def library_path(root: Path | None = None) -> Path:
    return (root or resolve_data_root()) / "简历素材库.md"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = resolve_data_root()
    if args and args[0] == "--library":
        print(library_path(root))
        return 0
    if args and args[0] == "--material" and len(args) >= 2:
        print(material_path(args[1], root))
        return 0
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
