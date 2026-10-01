---
name: changelog
description: "将当前对话或用户指定范围内已经实际发生的改动，整理为带序号、文件映射和证据状态的 Mentor 交接表。当用户调用 /changelog，或要求记录本次改动、比较本地与云端、查看未提交或未推送改动时使用；不要用于仅讨论或计划的总结。"
---

# Changelog

Turn the user's request into a concise handoff for a mentor. The user's intent determines the scope; the evidence determines what actually changed.

## Workflow

1. **Scope question — every invocation, mandatory, no default.** Ask the user which range this report covers: ① **本次**（本次会话的实际改动）or ② **本功能**（本功能全周期：整个事项从起点到现在的完整演进，例如「发现页改造这个事」）。Both are valid; never infer silently. For ②, anchor the effort's start from plan docs / ROADMAP / change-log when possible; ask one follow-up only if the boundary stays unclear.
2. **Granularity question — same round as step 1.** If the scope contains superseded iterations (a later version replaced an earlier one, e.g. v1 rule-scored flow replaced by v2 heat ranking), ask: main table records **only each deliverable's final state**, or **one row per iteration** (replaced versions get their own chronological rows). If no superseded iteration exists, skip.
3. Read `references/evidence-routing.md` and inspect only the relevant evidence. Always use the conversation for scope and background. Use files and Git, commits, cloud records, project records, tests, CI, or runtime logs only when the request and environment make them relevant.
4. Exclude plans, suggestions, and discussion-only decisions. Record an item only when a file, diff, commit, PR, or other change record proves that the change occurred. A conversation claim alone is not proof.
5. Read `references/output-format.md` and produce the complete handoff: scope and evidence summary, numbered main table, then file sections using the same numbers. Sort by impact and independent deliverables, not chat order. Under 全周期 scope, the "before" side of each row is the state before the effort started (not before each iteration).
   **Readability gate (hard, before delivering):** for every row ask — "can someone who did not read this conversation retell, in one plain sentence, what changed?" If not, rewrite the row before delivering. This gate is never skipped.
6. If the user asks to delete, merge, or reorder items, apply it, renumber continuously, update the file sections, and return the full clean result.
7. After delivering the report, always end with the closing question (one question, both offers): ① any items to remove (by number — applied per rule 5); ② whether to export the table as an image (ask where to save; see `references/output-format.md` for the export format). If the user declines both, the run ends.

## Boundaries

- Default to read-only. Do not write `CHANGELOG.md`, commit, push, merge, reset, checkout, or deploy.
- Never ask the user to choose evidence channels. Choose them from intent; ask only when the target project, comparison base, or access boundary is genuinely ambiguous, and include a recommendation.
- Keep delivery status separate from validation result. Do not call an item “completed” without evidence.
- If no actual change is found, use the exact no-change response in `references/output-format.md` and do not emit an empty table.
- Do not expose secrets, tokens, cookies, private URLs, personal data, or sensitive configuration values. Describe protected configuration generically.
