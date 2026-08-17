# Agent Team Contract

主线程并行派 3 个轻量 agent（Claude Code 内用 haiku），按数据源分工提炼"需求要点草稿"。**禁止编造**，未知环节标"待补充"；**禁止泄漏密钥**——素材里出现的密钥/token/密码一律脱敏或省略。

## Agent-CC
- 输入：主线程过滤后的本周 CC 会话（`~/.claude/projects/**/*.jsonl` 中 timestamp 转本地后属本周的记录）
- 职责：Read 素材 → 提炼"针对哪些需求做了什么" → Write 到 `$PREFIX-cc-draft.md`
- 输出格式：每行 `[需求名] | 背景? | 方案? | 做了什么 | 结果?`，未知用"待补充"

## Agent-Codex
- 输入：本周 Codex 会话（`~/.codex/sessions/YYYY/MM/DD/` 日期 ≥ 本周一的 rollout jsonl）
- 职责：同上，Write 到 `$PREFIX-codex-draft.md`
- 输出格式：同上

## Agent-Zcode
- 输入：主线程按 SKILL.md「ZCode 会话查询」跑出的文本（起点之后的 ZCode 会话：title + 用户消息 + 工具列表）
- 职责：同上，Write 到 `$PREFIX-zcode-draft.md`
- 输出格式：同上
