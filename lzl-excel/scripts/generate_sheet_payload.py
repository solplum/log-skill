#!/usr/bin/env python3
"""Validator and payload builder for lzl-excel.

Ensures all strict gates are met:
1. Column-discipline gate: 'problem_confirmation' contains NO fix words, has bare prefix, NO '都有'.
2. 1:1 Pairing gate: background items and change items have equal counts and matching numbering.
3. Delivery status gate: must be one of '未上传', '已上传', '已部署'.
4. Submission-ready gate: no forbidden internal words ('会话记录', 'AI对话', 'worktree', etc.).
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List

FORBIDDEN_WORDS = [
    "会话记录",
    "AI对话",
    "AI 对话",
    "对话中未提及",
    "worktree",
    "验证矩阵",
    "prompt",
    "同上",
    "如前所述",
    "见上文",
]

ALLOWED_STATUSES = {"未上传", "已上传", "已部署"}


def validate_row(row: Dict[str, Any], row_idx: int) -> List[str]:
    errors = []
    
    # 1. Check required fields
    for field in ["topic", "module", "problem_confirmation", "background", "changes", "status", "verification"]:
        if field not in row or not str(row[field]).strip():
            errors.append(f"Row {row_idx}: 缺失必要字段 '{field}'")

    # 2. Check forbidden words across all text fields
    full_text = " ".join(str(v) for v in row.values())
    for word in FORBIDDEN_WORDS:
        if word in full_text:
            errors.append(f"Row {row_idx}: 包含提交即终稿禁止词 '{word}'")

    # 3. Check problem_confirmation
    prob = str(row.get("problem_confirmation", ""))
    if "修复后" in prob or "优化后" in prob or "修复" in prob:
        errors.append(f"Row {row_idx}: 问题确认列违反列纪律，包含了修复相关词汇: '{prob}'")
    if "都有" in prob:
        errors.append(f"Row {row_idx}: 问题确认列禁止使用'都有'，双地点必须换行分开")
    if prob.startswith("已确认（") or prob.startswith("已确认("):
        errors.append(f"Row {row_idx}: 问题确认列应使用裸前缀（如'本地：'、'线上：'），去除'已确认（...）'外层包裹")

    # 4. Check delivery status
    status = str(row.get("status", "")).strip()
    if status not in ALLOWED_STATUSES:
        errors.append(f"Row {row_idx}: 交付状态 '{status}' 无效，必须严格为 {ALLOWED_STATUSES} 之一")

    # 5. Check 1:1 pairing between background and changes
    bg = str(row.get("background", "")).strip()
    ch = str(row.get("changes", "")).strip()
    
    # Check if numbered items exist
    bg_numbers = re.findall(r"(?:^|\n)\s*(\d+)、", bg)
    ch_numbers = re.findall(r"(?:^|\n)\s*(\d+)、", ch)
    
    if bg_numbers or ch_numbers:
        if len(bg_numbers) != len(ch_numbers):
            errors.append(
                f"Row {row_idx}: 原背景有 {len(bg_numbers)} 条编号事项，而本次改动有 {len(ch_numbers)} 条，数量必须严格 1:1 相等"
            )
        if bg_numbers != ch_numbers:
            errors.append(
                f"Row {row_idx}: 编号顺序或编号内容不一致: 背景={bg_numbers}, 改动={ch_numbers}"
            )

    return errors


def validate_sheet_data(data: Dict[str, Any]) -> List[str]:
    all_errors = []
    sheets = data.get("sheets", {})
    if not sheets:
        all_errors.append("工作簿中没有定义任何 Sheet")
        return all_errors

    for sheet_name, rows in sheets.items():
        if sheet_name == "变更日志":
            continue
        if not isinstance(rows, list):
            all_errors.append(f"Sheet '{sheet_name}' 的 rows 必须为列表")
            continue
        for idx, row in enumerate(rows, start=1):
            all_errors.extend(validate_row(row, idx))

    return all_errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python generate_sheet_payload.py <input_data.json>")
        return 1

    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = validate_sheet_data(data)
    if errors:
        print("❌ 门禁校验失败：发现以下规范违规项：", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2

    print("✅ 门禁校验通过！所有数据符合 lzl-excel 交付标准。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
