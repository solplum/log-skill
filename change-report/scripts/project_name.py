"""Resolve change-report's per-repo project folder name.

``<项目>`` comes from ``报告文档/代码/_projects.json`` when that file maps
the git root path; otherwise it is the git root directory name.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_mapping(projects_json: Path | None) -> dict[str, str]:
    if projects_json is None or not projects_json.is_file():
        return {}
    data = json.loads(projects_json.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("_projects.json must be an object of path -> name")
    return {str(k): str(v) for k, v in data.items()}


def resolve_project_name(repo_root: str | Path, mapping: dict[str, str] | None = None) -> str:
    root = Path(repo_root).expanduser().resolve()
    mapping = mapping or {}
    for key, name in mapping.items():
        mapped = Path(key).expanduser()
        try:
            if mapped.resolve() == root:
                return name
        except OSError:
            pass
        if Path(key).name == root.name or str(key).replace("\\", "/").rstrip("/") == str(root).replace("\\", "/"):
            return name
    return root.name


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: project_name.py <git-root> [_projects.json]", file=sys.stderr)
        return 2
    root = args[0]
    mapping_path = Path(args[1]) if len(args) > 1 else None
    print(resolve_project_name(root, load_mapping(mapping_path)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
