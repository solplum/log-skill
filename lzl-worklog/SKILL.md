---
name: lzl-worklog
description: 记录本周做了什么（CC+Codex+ZCode+MiniMax Code+Antigravity 五源、主动梳理+随手记录双模式），一键生成"需求叙事"周报。首次使用引导存储目录配置并支持全量扫描；汇报默认面向外部读者通俗化（杜绝自嗨与私有代号）。触发词："记录一下"、"梳理一下最近做了什么"、"周报"、"汇报"、"产出"、"站会"、"/lzl-worklog"、"/worklog"。数据存配置数据根（默认 ~/worklog 或 报告文档/需求/）。
---

# lzl-worklog 工作产出记录·汇报

记录本周做了什么（会话自动挖：CC/Codex/ZCode/MiniMax Code/Antigravity + 随手主动记），一键生成给别人看的"需求叙事"周报。纯原生工具，无脚本依赖。

## 闸口铁律（最高优先级，覆盖一切执行惯性）

以下闸口必须**停轮等待**：展示选项/候选后**立即结束本轮回复**，用户未回复前禁止任何扫描、提炼、落盘、派 agent：

| 闸口 | 时机 |
|------|------|
| ⓪ 存储目录确认 | 首次使用且未检测到存储配置（无环境变量且无配置文件） |
| ① 模式选择 | 裸调用 `/lzl-worklog`（或 `/worklog`）且用户没说要做哪个 |
| ② 日期范围 | 模式 A 第 1 步；汇报第 3 步（**全量扫描模式直接跳过本闸口**） |
| ③ 条目/清单确认 | 模式 A 第 4 步；汇报第 6 步 |

- **禁止自问自答**：同一回合内提出问题又自行回答并继续执行 = 违规（实测 Claude 会把"先问"叙述出来然后自己答掉一路跑完）。
- 回答含糊（"都行""好""随便"）≠ 明确选择，必须再问；**无确认 = 0 条写入**，绝不默认全选。

裸调用 `/lzl-worklog`（或 `/worklog`，无参数、未指向任何模式）→ 先闸口①问："全量扫描（建初始底账） / 梳理最近做了什么 / 随手记 / 出周报？"。用户话里已明确指向时直接进入："记录一下：…"→模式 B；"全量扫描/全量梳理"→模式 A（全量，跳过闸口②）；"梳理一下"→模式 A；"周报/汇报/产出/站会"→汇报。

## 存储布局

数据根 `$DATA_ROOT` 可通过环境变量 `LZL_WORKLOG_DATA_ROOT`（兼容 `WORKLOG_DATA_ROOT`）或配置文件 `~/.config/lzl-worklog/config.json` 指定。未配置时默认为当前工作区 `报告文档/需求/` 或全局 `~/worklog`。

### 首次使用初始化（闸口⓪，硬停轮）
若未设置环境变量，且 `~/.config/lzl-worklog/config.json` 不存在，且当前目录没有既有 `报告文档/需求/`：
向用户展示下列选项并**立即结束本轮回复**，停轮等待用户选择：
1. **【推荐】全局统一存储**：`~/worklog`（跨项目统一记录，不会把周报写进代码仓库，安全且便于统一统计）
2. **当前项目工作区**：`./报告文档/需求/`（与当前代码仓库同放，适合单项目强隔离）
3. **自定义路径**：指定任意绝对路径

用户选定后，写入 `~/.config/lzl-worklog/config.json`（格式形如 `{"data_root": "<选中路径>"}`），后续调用自动读取，不再重复询问。

### 目录结构
周粒度，以**本周周一日期**命名（周一为一周起始）：

```
$DATA_ROOT/  （支持 报告文档/需求/ 或 ~/worklog/）
├── 日志/<周一日期>.md        # 主动记录流水，只追加从不覆盖
└── 周报/
    ├── md形式/<起点日期>.md    # md 周报快照，可重复生成
    └── word形式/<起点日期>.docx # Word 版周报（导出时生成）
```

为保持向下兼容，默认环境与原有规则下对应 `报告文档/需求/日志` 与 `报告文档/需求/周报`。

### 周起算

```bash
DOW=$(date +%u)                                  # 1=周一 ... 7=周日
MONDAY=$(date -d "$(date +%F) -$((DOW-1)) days" +%F)   # 本周一
```

`<周一日期>` 即 `$MONDAY`。周内任意调用都用它定位同一份文件。

### 上次搜索断点

模式 A 与汇报的日期范围选项「从上次搜索-现在」依赖一个断点文件：

```
$DATA_ROOT/.last-scan    # 一行，YYYY-MM-DD，= 上次执行会话扫描当天的日期（默认 报告文档/需求/.last-scan）
```

- **写入时机**：模式 A 第 2 步五源扫描完成后、汇报第 3 步五源挖完后，执行 `date +%F > "$DATA_ROOT/.last-scan"`。只记录"扫描动作发生的日期"，与本次扫描选的范围起点无关。
- **读取**：用户选「从上次搜索-现在」时 `$START=$(cat "$DATA_ROOT/.last-scan" 2>/dev/null)`；文件不存在或为空 → 告知无上次搜索记录，重新展示其余选项（仍在闸口②停轮语义内）。
- 断点按天粒度衔接：上次扫描当天的新会话会被重扫一次，由「去重」小节兜底跳过，不产生重复条目。

## 数据源

| 源 | 路径 | 时间基准 |
|----|------|---------|
| CC | `~/.claude/projects/**/*.jsonl` | JSONL 内 `"timestamp"`（UTC） |
| Codex | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` + `archived_sessions/` 兜底 | 目录/文件名（本地时间） |
| ZCode | `~/.zcode/cli/db/db.sqlite`（SQLite：`session`/`message`/`part` 三表） | `session.time_updated`（epoch 毫秒，绝对时间） |
| MiniMax Code | `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/messages.jsonl` | 行内 `message.timestamp`（epoch 毫秒，绝对时间） |
| Antigravity | 双端同构：桌面端 `~/.gemini/antigravity/` + CLI `~/.gemini/antigravity-cli/` 的 `conversation_summaries.db` 与 `brain/*/transcript.jsonl` | `last_modified_time`（UTC，ISO 8601） |

### 时区归一（重要，防边界日漏记录）
- CC `timestamp` 是 UTC（如 `2026-08-12T02:00:00.000Z`，本地 UTC+8 → 08-12 10:00）。
- 按日期过滤"本周/起点之后"前，统一把 CC timestamp 转本地再比较（`date -d "<TS>" +%F`）。
- 否则周一 00:00–07:59 落地的 UTC 记录（仍是上周日期）会被漏掉。
- Codex 目录/文件名已是本地时间，直接比较。
- ZCode 时间戳是 epoch 毫秒（绝对时间），无时区换算问题：起点转毫秒 `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))` 后直接比较。
- MiniMax Code 时间戳同为 epoch 毫秒，无换算问题，比较方式同 ZCode；**不要用目录名日期过滤**（跨天长会话会漏，须用消息内末条 timestamp 判断）。
- Antigravity 时间戳为 UTC ISO 8601 字符串（如 `2026-10-15 08:22:44+00:00`），转本地再比较。**桌面端（IDE / 2.0）与 CLI（agy）物理路径不同源，但底层表与 transcript 结构完全同构**，统一双端扫描合并。

## 外部读者视角与术语通俗化（去黑话铁律）

**周报最终是给 Mentor、上级主管、跨组团队或外部评审看的，严禁直接照搬只有作者自己懂的内部代号与调试流水账。**

提炼候选（第 3 步）、用户确认（第 4 步）、合成周报草案（第 5 步）必须严格遵守以下消歧规则：

1. **私有代号与内部工具通用化（杜绝自嗨孤立词）**：
   - 严禁出现未加解释的内部代号、私有工具、自研系统简称（如 `Mimosa`、自写脚本名、内部特定平台缩写）。
   - **替换为行业通用工程/业务语言**：
     - 例：`Mimosa 提交门禁` / `Mimosa 安全钩子` → 改为 `Git 代码提交静态安全合规门禁` 或 `代码提交规范检查钩子`。
     - 若确实需要保留专有名词，必须采用 **"通用工程职能（内部代号）"** 形式，如 `代码安全合规门禁系统（Mimosa）`、`数仓自动化同步服务`，确保任何外人都能一眼看懂其业务职能。
2. **聚焦业务价值与工程成果，拒绝个人调试流水账**：
   - 严禁把“被内部钩子拦截查原因”当作工作成果（如“排查被 Mimosa 拦截的原因及分类”）。
   - 必须按规范提炼为业务价值：“完善集群数仓代码提交规范与静态安全检查规则，解除门禁拦截并形成排查指引”。
3. **第三方库与工具适度泛化说明**：
   - 遇到技术包名（如 `@larksuite/cli`），说明其业务职能（如“集成飞书开放平台 CLI 工具，打通飞书在线交付表格创建流程”）。

## ZCode 会话查询（SQLite）

ZCode 会话存在 SQLite 库里，**必须只读打开**（ZCode 运行时正占用该库，`mode=ro` 与 WAL 并发安全，已实测）：

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
- 仓库里 `scripts/zcode_sessions.py` 是同一条查询的可执行副本（`python scripts/zcode_sessions.py <START_MS> [db]`），单测直接驱动它。

## MiniMax Code 会话查询

MiniMax Code（ZCode 系内核）会话按日期分层存 `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/`，核心是 `messages.jsonl`，每行一个消息对象：`message.role`（user/assistant）+ `message.content[]`（text 块）+ `message.timestamp`（epoch 毫秒）。扫描脚本：

```bash
START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))   # $START=起点日期 YYYY-MM-DD
python - "$START_MS" <<'EOF'
import json, glob, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')   # 必须：Windows 下中文输出防 GBK 乱码
START_MS = int(sys.argv[1])
SKIP_PREFIX = ('<system-reminder', 'Base directory for this skill', 'This is a skill', '<background-task-finished', '[Request interrupted')
for f in sorted(glob.glob(os.path.expanduser('~/.minimax/v2/sessions/*/*/*/*-session_*/messages.jsonl'))):
    last_ms = 0; msgs = []
    for line in open(f, encoding='utf-8', errors='ignore'):
        try: o = json.loads(line)
        except: continue
        m = o.get('message') or {}
        ts = m.get('timestamp')
        if ts: last_ms = max(last_ms, ts)                      # 全文件末条，跨天会话不漏
        if m.get('role') != 'user': continue
        c = m.get('content', [])
        if not isinstance(c, list): continue
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'text':
                t = x.get('text', '').strip()
                if t and not t.startswith(SKIP_PREFIX): msgs.append(t)
    if not msgs or last_ms < START_MS: continue                # msgs 空 = 纯注入会话，跳过
    print(f"{datetime.datetime.fromtimestamp(last_ms/1000):%Y-%m-%d}  {f}  {msgs[0][:80]}")
EOF
```

- **时间基准是消息内 `timestamp`，不是目录名日期**（目录名是会话创建时刻，跨天长会话按它过滤会漏掉末条之后的日期）。
- `<system-reminder>`/skill 注入开头的 user 消息是系统注入不是真实输入，脚本已排除；全被排除的会话跳过。
- `manifest.json` 有 `createdAtMs`/`updatedAtMs` 但**无标题与工作目录**，会话主题只能用首条真实用户消息。
- `~/.minimax/` 不存在 → 跳过该源并提示。

## Antigravity 会话查询（桌面端 + CLI 双端全覆盖）

Antigravity（AGY）提供独立 IDE/桌面端与 `agy` 命令行 CLI。**桌面端与 CLI 物理存储不同源（桌面端保存在 `~/.gemini/antigravity/`，CLI 保存在 `~/.gemini/antigravity-cli/`），但两者底层架构完全同构**：均由 `conversation_summaries.db` 管理元数据，`brain/<id>/.system_generated/logs/transcript.jsonl` 保存完整轨迹。脚本执行双端探测与合并：

```bash
python - "$START" <<'EOF'
import sqlite3, os, sys, datetime, pathlib, json
sys.stdout.reconfigure(encoding='utf-8')
START = sys.argv[1]            # YYYY-MM-DD；全量传 0000-00-00
dirs = [
    ('IDE', os.path.expanduser('~/.gemini/antigravity')),
    ('CLI', os.path.expanduser('~/.gemini/antigravity-cli')),
]
seen = set()
for label, base in dirs:
    db = os.path.join(base, 'conversation_summaries.db')
    if not os.path.exists(db): continue
    try:
        con = sqlite3.connect(pathlib.Path(db).as_uri() + '?mode=ro', uri=True)
        cur = con.cursor()
        for cid, title, lmt, uris in cur.execute(
            "SELECT conversation_id, title, last_modified_time, workspace_uris "
            "FROM conversation_summaries ORDER BY last_modified_time DESC"):
            if not lmt or cid in seen: continue
            dt_local = datetime.datetime.fromisoformat(lmt).astimezone()
            if dt_local.strftime('%Y-%m-%d') >= START:
                seen.add(cid)
                # 尝试轻读第一条真实用户输入作为补充说明
                prompt = ''
                tr = os.path.join(base, 'brain', cid, '.system_generated', 'logs', 'transcript.jsonl')
                if os.path.exists(tr):
                    for line in open(tr, encoding='utf-8', errors='ignore'):
                        try:
                            o = json.loads(line)
                            if o.get('type') == 'USER_INPUT' and o.get('content'):
                                t = o['content'].strip().replace('\n', ' ')
                                if not t.startswith('<system-reminder'):
                                    prompt = t[:80]; break
                        except Exception: pass
                print(f"[{label}] {dt_local:%Y-%m-%d %H:%M}  {title or '(无标题)'}  {prompt}")
    except Exception: pass
EOF
```

- 任一目录不存在则跳过该目录；两端均不存在则跳过该源并提示。
- `title` 由高精度模型生成，质量极佳，可直接作为候选主题。

## 记录 · 模式 B：随手记录

触发词："记录一下：..."、"记一下：..."。零摩擦，用户说啥记啥。

1. 计算本周一 `$MONDAY`（见"周起算"）。
2. 定位 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`），不存在则创建（含目录）。
3. 以当天日期 `MM-DD` 分节，追加 `- [需求] <一句话>`。格式：

```markdown
## 08-12
- [记住我] 设计了登录勾选逻辑 + 30 天 token 续期
```

4. 当天节已存在则在其下追加；**只追加，绝不覆盖或改动历史条目**。

## 记录 · 模式 A：主动梳理

触发词："梳理一下最近做了什么"、"梳理一下"、"全量扫描"、"全量梳理"。在功能完成/阶段性完成或首次建账时使用。

1. **选日期范围（闸口②，硬停轮；全量扫描模式直接跳过本步）**：
   - **穿透闸口②规则**：若在闸口①选择了「全量扫描」，或用户指令明确包含「全量扫描」「全量梳理」「建初始底账」等全量意图，**意图已锁定为全部历史，严禁再次询问日期范围，直接将起点设为全部（`$START=0000-00-00`，`$START_MS=0`），立即开始第 2 步扫描**！
   - 若用户进入的是普通梳理，展示下列选项后立即结束本轮回复，用户明确选择后再扫描：
     - A. 本周一-现在（默认）——本周已有日志时起点取日志最后一个 `## MM-DD` 节，跳过已记录项
     - B. 七天前-现在
     - C. 从上次搜索-现在——起点读「上次搜索断点」（见「上次搜索断点」小节）；无断点记录时告知用户"没有上次搜索记录"并重新展示其余选项等其选择
     - D. 全部历史——全量挖掘历史全部会话（`$START=0000-00-00`，`$START_MS=0`）
     - E. 自定义——向用户要起止日期
2. **扫最近/全量会话（五源探测）**：
   - CC：`~/.claude/projects/**/*.jsonl`，按 JSONL 内 `"timestamp"`（转本地时区）筛选 ≥ 起点（全量时不作起点过滤）。
   - Codex：`~/.codex/sessions/YYYY/MM/DD/*.jsonl`（本地时间）+ `archived_sessions/` 兜底，目录/文件名日期 ≥ 起点（全量时扫全部日期）。`~/.codex/` 不存在则跳过该源并提示。
   - ZCode：`~/.zcode/cli/db/db.sqlite` 按「ZCode 会话查询」小节执行，`time_updated >= $START_MS` 筛选（全量时 `$START_MS=0`）。库不存在则跳过该源并提示。
   - MiniMax Code：`~/.minimax/v2/sessions/*/*/*/*-session_*/messages.jsonl` 按「MiniMax Code 会话查询」小节执行，消息内 timestamp（epoch 毫秒）≥ `$START_MS` 筛选（全量时 `$START_MS=0`）。目录不存在则跳过该源并提示。
   - Antigravity：按「Antigravity 会话查询」小节同时扫描桌面端 `~/.gemini/antigravity` 与 CLI `~/.gemini/antigravity-cli`，`last_modified_time` 转本地时区 ≥ 起点（全量时不作过滤）。两端均不存在则跳过该源并提示。
   - 五源扫完后执行「上次搜索断点」小节的写入动作。
3. **提炼候选（仅供展示，禁止直接落盘）**：轻读各源会话的用户消息/工具调用，产出**编号**列表 `1. 日期 + 主题 + 2-3 要点`。**必须严格执行「外部读者视角与术语通俗化」铁律**：严禁出现外部读者看不懂的内部代号/私有工具名（如 Mimosa 须泛化为"代码提交静态安全检查门禁"），聚焦业务与工程价值，严禁堆砌自嗨流水账。用户消息里的密钥/token/密码一律脱敏或省略，敏感串不得出现在任何输出中。
4. **用户确认（闸口③，硬停轮，必须精确到条目）**：展示编号候选 + "要记哪几条？"（如"记 1、3"或"只记第 2 条"）后立即结束本轮回复。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
5. **落盘（只写用户确认的条目）**：严格按用户确认的编号/条目，逐条按模式 B 格式追加到 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`）。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 去重与防丢失

### 去重（两种模式落盘前都执行）
1. 读 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`）现有条目，提取所有 `[需求名]` 标签（`- [XX] ...`）。
2. 新条目 `[需求名]` 已存在 → 跳过并提示"该需求已记录，跳过"，不重复追加。
3. 语义相近但标签不同 → 模式 A 由用户确认时人工去重；模式 B 提示用户"是否合并到已有条目"。

### 防丢失
- 日志文件**只追加从不覆盖**；生成周报只写 `周报/`，绝不改动 `日志/`。
- 模式 A 定期（阶段完成时）捞会话兜底，与随手记录互为备份。

## 汇报（触发词：周报 / 汇报 / 产出 / 站会）

1. 计算本周一 `$MONDAY`。
2. 读 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`，主动记录）。
3. **询问日期范围（闸口②，硬停轮）**：展示 A. 本周一-现在（默认）/ B. 七天前-现在 / C. 从上次搜索-现在（无断点记录时说明并重新展示其余选项）/ D. 自定义后立即结束本轮回复；用户明确选择后再按所选范围挖五源会话：CC（timestamp 转本地后属所选范围）＋ Codex（目录日期 ≥ 所选起点）＋ ZCode（db.sqlite 按「ZCode 会话查询」，`time_updated` ≥ 起点）＋ MiniMax Code（messages.jsonl 按「MiniMax Code 会话查询」，timestamp ≥ 起点）＋ Antigravity（双端按「Antigravity 会话查询」，本地日期 ≥ 起点）。任一源探测不到则跳过并提示。五源挖完后执行「上次搜索断点」小节的写入动作。选定后记扫描起点 `$START`（周报文件名据此）：
   - A → `$START=$MONDAY`
   - B → `$START=$(date -d "-6 days" +%F)`（含今天共 7 天）
   - C → `$START=` 断点文件里存的日期
   - D → `$START=` 用户给的起始日期
4. 并行派最多 5 个轻量 agent（Claude Code 内用 haiku；其他环境用等价轻量代理。契约见 `references/agent-team-contract.md`）：Agent-CC → `md形式/$START-cc-draft.md`；Agent-Codex → `md形式/$START-codex-draft.md`；Agent-Zcode → `md形式/$START-zcode-draft.md`；Agent-Minimax → `md形式/$START-minimax-draft.md`；Agent-Antigravity → `md形式/$START-antigravity-draft.md`。某源本次被跳过时不派对应 agent，不产出空草稿。
5. 主线程合成草案（暂不落盘）：主动记录 + 各源草稿 → 严格按「外部读者视角与术语通俗化」去黑话后，按"需求叙事"模板整理出完整周报内容，附"将写入 N 条需求"的编号清单（每条一句话）。
6. **清单确认（闸口③，硬停轮）**：展示编号清单，问"全部写入，还是删掉哪几条？"后立即结束本轮回复。用户确认后才写入；点名删除的条目剔除；含糊回答必须再问，无确认不写。
7. 写入 `$DATA_ROOT/周报/md形式/$START.md`（默认 `报告文档/需求/周报/md形式/$START.md`），随后删除全部中间草稿（`$START-cc-draft.md`、`$START-codex-draft.md`、`$START-zcode-draft.md`、`$START-minimax-draft.md`、`$START-antigravity-draft.md` 等本次实际产出的），`md形式/` 只留最终周报。
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
10. 询问用户是否需要把周报导出 Word。需要则查本地 docx 相关 skill（Claude Code 双路径 `~/.claude/skills/` + `.claude/skills/`；ZCode 内用 Skill 工具的 `docx` / `document-skills:docx`），调用它把 `$DATA_ROOT/周报/md形式/$START.md`（默认 `报告文档/需求/周报/md形式/$START.md`）转成 Word，输出到 `$DATA_ROOT/周报/word形式/$START.docx`（默认 `报告文档/需求/周报/word形式/$START.docx`）；查不到则告知用户并询问替代方案。
