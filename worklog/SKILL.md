---
name: worklog
description: 记录本周做了什么（CC+Codex+ZCode 三源、主动梳理+随手记录双模式），一键生成"需求叙事"周报。触发词："记录一下"、"梳理一下最近做了什么"、"周报"、"汇报"、"产出"、"站会"。数据存 报告文档/需求/日志 与 报告文档/需求/周报。
---

# worklog 工作产出记录·汇报

记录本周做了什么（会话自动挖：CC/Codex/ZCode + 随手主动记），一键生成给别人看的"需求叙事"周报。纯原生工具，无脚本依赖。

## 闸口铁律（最高优先级，覆盖一切执行惯性）

以下闸口必须**停轮等待**：展示选项/候选后**立即结束本轮回复**，用户未回复前禁止任何扫描、提炼、落盘、派 agent：

| 闸口 | 时机 |
|------|------|
| ① 模式选择 | 裸调用 `/worklog` 且用户没说要做哪个 |
| ② 日期范围 | 模式 A 第 1 步；汇报第 3 步 |
| ③ 条目/清单确认 | 模式 A 第 4 步；汇报第 6 步 |

- **禁止自问自答**：同一回合内提出问题又自行回答并继续执行 = 违规（实测 Claude 会把"先问"叙述出来然后自己答掉一路跑完）。
- 回答含糊（"都行""好""随便"）≠ 明确选择，必须再问；**无确认 = 0 条写入**，绝不默认全选。

裸调用 `/worklog`（无参数、未指向任何模式）→ 先闸口①问："随手记 / 梳理最近做了什么 / 出周报？"。用户话里已明确指向时直接进入："记录一下：…"→模式 B；"梳理一下"→模式 A；"周报/汇报/产出/站会"→汇报。

## 存储布局

周粒度，以**本周周一日期**命名（周一为一周起始）：

```
报告文档/需求/
├── 日志/<周一日期>.md        # 主动记录流水，只追加从不覆盖
└── 周报/
    ├── md形式/<起点日期>.md    # md 周报快照，可重复生成
    └── word形式/<起点日期>.docx # Word 版周报（导出时生成）
```

### 周起算

```bash
DOW=$(date +%u)                                  # 1=周一 ... 7=周日
MONDAY=$(date -d "$(date +%F) -$((DOW-1)) days" +%F)   # 本周一
```

`<周一日期>` 即 `$MONDAY`。周内任意调用都用它定位同一份文件。

## 数据源

| 源 | 路径 | 时间基准 |
|----|------|---------|
| CC | `~/.claude/projects/**/*.jsonl` | JSONL 内 `"timestamp"`（UTC） |
| Codex | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` + `archived_sessions/` 兜底 | 目录/文件名（本地时间） |
| ZCode | `~/.zcode/cli/db/db.sqlite`（SQLite：`session`/`message`/`part` 三表） | `session.time_updated`（epoch 毫秒，绝对时间） |

### 时区归一（重要，防边界日漏记录）
- CC `timestamp` 是 UTC（如 `2026-08-12T02:00:00.000Z`，本地 UTC+8 → 08-12 10:00）。
- 按日期过滤"本周/起点之后"前，统一把 CC timestamp 转本地再比较（`date -d "<TS>" +%F`）。
- 否则周一 00:00–07:59 落地的 UTC 记录（仍是上周日期）会被漏掉。
- Codex 目录/文件名已是本地时间，直接比较。
- ZCode 时间戳是 epoch 毫秒（绝对时间），无时区换算问题：起点转毫秒 `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))` 后直接比较。

## ZCode 会话查询（SQLite）

ZCode 会话存在 SQLite 库里，**必须只读打开**（ZCode 运行时正占用该库，`mode=ro` 与 WAL 并发安全，已实测）。仓库里 `scripts/zcode_sessions.py` 是同一条查询的可执行副本（`python scripts/zcode_sessions.py <START_MS> [db]`）：

```bash
START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))   # $START=起点日期 YYYY-MM-DD
python - "$START_MS" <<'EOF'
import sqlite3, json, sys, os, datetime, pathlib
db = os.path.expanduser('~/.zcode/cli/db/db.sqlite')
con = sqlite3.connect(pathlib.Path(db).as_uri() + '?mode=ro', uri=True)
cur = con.cursor()
for sid, title, d, tc in cur.execute(
    "SELECT id, title, directory, time_created FROM session "
    "WHERE time_updated >= ? ORDER BY time_created", (sys.argv[1],)).fetchall():
    print(f"== {datetime.datetime.fromtimestamp(tc/1000):%m-%d %H:%M}  {title or '(无标题)'}  [{d}]")
    for (p,) in cur.execute("""SELECT p.data FROM part p JOIN message m ON p.message_id = m.id
        WHERE p.session_id = ? AND json_extract(m.data,'$.role') = 'user'
          AND json_extract(p.data,'$.type') = 'text'
          AND COALESCE(json_extract(p.data,'$.synthetic'), 0) = 0
        ORDER BY p.time_created""", (sid,)):
        t = json.loads(p).get('text', '').strip()
        if t: print('  U>', t[:120].replace('\n', ' '))
    tools = cur.execute("""SELECT DISTINCT json_extract(data,'$.tool') FROM part
        WHERE session_id = ? AND json_extract(data,'$.type') = 'tool'""", (sid,)).fetchall()
    print('  tools:', ', '.join(sorted(str(t[0]) for t in tools if t[0])))
EOF
```

- `~/.zcode/cli/db/db.sqlite` 不存在 → 跳过该源并提示。
- `session.title` 由 CLI 维护（`title_source` 字段），质量可靠，可直接作会话主题（不像 CC 的 thread_name 实测多为"你好"）。
- `synthetic=1` 的 part 是系统注入（如 TodoWrite 提醒），不是真实用户输入，查询已排除。

## 记录 · 模式 B：随手记录

触发词："记录一下：..."、"记一下：..."。零摩擦，用户说啥记啥。

1. 计算本周一 `$MONDAY`（见"周起算"）。
2. 定位 `报告文档/需求/日志/$MONDAY.md`，不存在则创建（含目录）。
3. 以当天日期 `MM-DD` 分节，追加 `- [需求] <一句话>`。格式：

```markdown
## 08-12
- [记住我] 设计了登录勾选逻辑 + 30 天 token 续期
```

4. 当天节已存在则在其下追加；**只追加，绝不覆盖或改动历史条目**。

## 记录 · 模式 A：主动梳理

触发词："梳理一下最近做了什么"、"梳理一下"。在功能完成/阶段性完成时使用。

1. **选日期范围（闸口②，硬停轮）**：展示下列选项后立即结束本轮回复，用户明确选择后再扫描：
   - A. 本周一-现在（默认）——本周已有日志时起点取日志最后一个 `## MM-DD` 节，跳过已记录项
   - B. 七天前-现在
   - C. 自定义——向用户要起止日期
2. **扫最近会话**：
   - CC：`~/.claude/projects/**/*.jsonl`，按 JSONL 内 `"timestamp"`（转本地时区）筛选 ≥ 起点。
   - Codex：`~/.codex/sessions/YYYY/MM/DD/*.jsonl`（本地时间）+ `archived_sessions/` 兜底，目录/文件名日期 ≥ 起点。`~/.codex/` 不存在则跳过该源并提示。
   - ZCode：`~/.zcode/cli/db/db.sqlite` 按「ZCode 会话查询」小节执行，`time_updated >= $START_MS` 筛选。库不存在则跳过该源并提示。
3. **提炼候选（仅供展示，禁止直接落盘）**：轻读每个会话的用户消息/工具调用，产出**编号**列表 `1. 日期 + 主题 + 2-3 要点`（不依赖 `session_index.jsonl` 的 thread_name，实测多为"你好"；ZCode 会话可直接用 `session.title` 作主题）。用户消息里可能贴过密钥/token/密码（实测存在），候选与落盘一律脱敏或省略，敏感串不得出现在任何输出中。
4. **用户确认（闸口③，硬停轮，必须精确到条目）**：展示编号候选 + "要记哪几条？"（如"记 1、3"或"只记第 2 条"）后立即结束本轮回复。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
5. **落盘（只写用户确认的条目）**：严格按用户确认的编号/条目，逐条按模式 B 格式追加到 `报告文档/需求/日志/$MONDAY.md`。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 去重与防丢失

### 去重（两种模式落盘前都执行）
1. 读 `报告文档/需求/日志/$MONDAY.md` 现有条目，提取所有 `[需求名]` 标签（`- [XX] ...`）。
2. 新条目 `[需求名]` 已存在 → 跳过并提示"该需求已记录，跳过"，不重复追加。
3. 语义相近但标签不同 → 模式 A 由用户确认时人工去重；模式 B 提示用户"是否合并到已有条目"。

### 防丢失
- 日志文件**只追加从不覆盖**；生成周报只写 `周报/`，绝不改动 `日志/`。
- 模式 A 定期（阶段完成时）捞会话兜底，与随手记录互为备份。

## 汇报（触发词：周报 / 汇报 / 产出 / 站会）

1. 计算本周一 `$MONDAY`。
2. 读 `报告文档/需求/日志/$MONDAY.md`（主动记录）。
3. **询问日期范围（闸口②，硬停轮）**：展示 A. 本周一-现在（默认）/ B. 七天前-现在 / C. 自定义后立即结束本轮回复；用户明确选择后再按所选范围挖三源会话：CC（timestamp 转本地后属所选范围）＋ Codex（目录日期 ≥ 所选起点）＋ ZCode（db.sqlite 按「ZCode 会话查询」，`time_updated` ≥ 起点）。任一源探测不到则跳过并提示。选定后记扫描起点 `$START`（周报文件名据此）：
   - A → `$START=$MONDAY`
   - B → `$START=$(date -d "-6 days" +%F)`（含今天共 7 天）
   - C → `$START=` 用户给的起始日期
4. 并行派 3 个轻量 agent（Claude Code 内用 haiku；ZCode 内用其子代理机制。契约见 `references/agent-team-contract.md`）：Agent-CC → `md形式/$START-cc-draft.md`；Agent-Codex → `md形式/$START-codex-draft.md`；Agent-Zcode → `md形式/$START-zcode-draft.md`。
5. 主线程合成草案（暂不落盘）：主动记录 + 三份草稿 → 按"需求叙事"模板整理出完整周报内容，附"将写入 N 条需求"的编号清单（每条一句话）。
6. **清单确认（闸口③，硬停轮）**：展示编号清单，问"全部写入，还是删掉哪几条？"后立即结束本轮回复。用户确认后才写入；点名删除的条目剔除；含糊回答必须再问，无确认不写。
7. 写入 `报告文档/需求/周报/md形式/$START.md`，随后删除三份中间草稿（`$START-cc-draft.md`、`$START-codex-draft.md`、`$START-zcode-draft.md`），`md形式/` 只留最终周报。
8. 触发词含"站会/晨会" → 末尾附 Scrum 三问（完成/计划/阻塞）。

### 需求叙事模板

```markdown
# 产出汇报（<起点> ~ <终点>）

## 需求：<需求名>
- **需求背景**：<为什么做>
- **方案**：<怎么设计>
- **落地**：<实际做了啥>
- **结果**：<数据/效果；缺失标"待补充"，禁止编造>
```

9. 输出后告知：日期、周报路径、本周有无记录/会话。无记录无会话时提示先"记录一下"或"梳理一下"。
10. 询问用户是否需要把周报导出 Word。需要则查本地 docx 相关 skill（Claude Code 双路径 `~/.claude/skills/` + `.claude/skills/`；ZCode 内用 Skill 工具的 `docx` / `document-skills:docx`），调用它把 `报告文档/需求/周报/md形式/$START.md` 转成 Word，输出到 `报告文档/需求/周报/word形式/$START.docx`；查不到则告知用户并询问替代方案。
