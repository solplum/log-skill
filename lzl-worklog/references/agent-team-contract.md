# Agent Team Contract

主线程按需并行派最多 5 个轻量 agent（Claude Code 内用 haiku；其他环境用等价轻量代理），按数据源分工提炼"需求要点草稿"。
**禁止编造**，未知环节标"待补充"；**禁止泄漏密钥**——素材里出现的密钥/token/密码一律脱敏或省略。某数据源本次被跳过时不派对应 agent，不产出空草稿。

## 外部可读性铁律（所有 Agent 必遵）
输出是给 Mentor、主管和外部人员看的周报素材：
1. **抹除 AI 自身执行痕迹**：严禁出现“子 Agent 审计”、“多轮逻辑审查”、“执行脚本调整”等 AI 工具调试流水账，必须提炼为真实业务动作与成效；
2. **去黑话与代号通用化**：严禁使用外人无法理解的私有代号、自研内部工具名（如 Mimosa、内部特定 hook/脚本），必须翻译为行业通用业务/工程术语（如"代码提交静态安全检查门禁"）或附带说明"业务职能（内部代号）"；
3. **人话三段式叙事**：聚焦“解决了什么痛点问题、采取了什么关键改动、带来什么实际效果”。

## Agent-CC
- 输入：主线程过滤后的本周 CC 会话（`~/.claude/projects/**/*.jsonl` 中 timestamp 转本地后属本周的记录）
- 职责：Read 素材 → 按人话三段式提炼成果 → Write 到 `$PREFIX-cc-draft.md`
- 输出格式：每行 `[动宾成果标题] | 痛点问题 | 关键改动 | 实际效果`，未知用"待补充"

## Agent-Codex
- 输入：本周 Codex 会话（`~/.codex/sessions/YYYY/MM/DD/` 日期 ≥ 本周一的 rollout jsonl）
- 职责：同上，Write 到 `$PREFIX-codex-draft.md`
- 输出格式：同上

## Agent-Zcode
- 输入：主线程按 SKILL.md「ZCode 会话查询」跑出的文本（起点之后的 ZCode 会话：title + 用户消息 + 工具列表）
- 职责：同上，Write 到 `$PREFIX-zcode-draft.md`
- 输出格式：同上

## Agent-Minimax
- 输入：主线程按 SKILL.md「MiniMax Code 会话查询」跑出的文本（起点之后的 MiniMax Code 会话：末条日期 + 文件路径 + 首条真实用户消息；深读时含全部用户消息）
- 职责：同上，Write 到 `$PREFIX-minimax-draft.md`
- 输出格式：同上

## Agent-Antigravity
- 输入：主线程按 SKILL.md「Antigravity 会话查询」跑出的文本（起点之后桌面端与 CLI 的 Antigravity 会话：title + 工作区 + 用户消息摘要）
- 职责：同上，Write 到 `$PREFIX-antigravity-draft.md`
- 输出格式：同上
