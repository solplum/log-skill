---
name: lzl-worklog
description: 整理工作记录并生成两类周报：根据会话与日志的工作记录类，或根据云端分支实际提交的云端提交类。两类均按项目和功能主线整合各仓具体改动，不按分支排版。支持随手记录、近期梳理和五源历史建账。触发词：记录一下、梳理最近做了什么、周报、汇报、产出、站会、根据云端分支写周报、/lzl-worklog、/worklog。
---

# lzl-worklog 工作产出记录·汇报

整理工作记录，生成给 Mentor、主管或协作者看的周报。支持工作记录类和云端提交类；两类都先按项目和功能主线概括成果，再说明各实际仓库承担的具体改动，保留必要的验证和交付状态。纯原生工具，无脚本依赖。

## 两类周报

| 类型 | 主要依据 | 可以计入的内容 |
|------|----------|----------------|
| 工作记录类（默认） | 用户指定记录、日志及五源会话的实际证据 | 范围内已确认的工作，可包含本地未提交、未推送、调研及协作进展，准确标明状态 |
| 云端提交类 | 已核验云端分支可达的实际提交与代码差异 | 范围内可确认属于汇报主体的云端代码、测试及文档增量；不混入同事工作或本地未推送内容 |

- “根据这些记录”“梳理本周工作”按工作记录类；“根据云端分支”“只写已推送内容”“根据远端提交”按云端提交类。用户已经明确类型时不再问；未限定来源时默认工作记录类，只有两种口径会实质影响结果且意图无法判断时才询问。
- **来源口径不同，成稿结构相同**：云端提交类需在取证时核对多条分支，成稿将同一功能的各仓改动整合、去重后呈现，不新增分支标题或分支交付章节。分支与提交定位留在证据素材中，用户要求时再展示。
- **个人周报按本人贡献整合**：远端分支可能继承带教或同事的提交，不能将整条分支或整个功能归为本人完成。结合提交身份、父节点差异与已确认协作记录确认增量；在已有能力上适配或补充时写清“接入、复用、修复、完善”的具体部分。归属不明的改动先不计入个人已完成成果。
- 同一周分别保存两类时使用不同文件名，避免覆盖。切换类型不修改原日志，也不把一种类型的范围自动扩展给另一种。
- 生成云端提交类前读取 [references/cloud-weekly.md](references/cloud-weekly.md)；工作记录类沿用五源与日志流程。

## 闸口铁律（最高优先级，覆盖一切执行惯性）

以下闸口必须**停轮等待**：展示选项/候选后**立即结束本轮回复**，用户未回复前禁止任何扫描、提炼、落盘、派 agent：

| 闸口 | 时机 |
|------|------|
| ⓪ 存储目录确认 | 首次使用且未检测到存储配置（无环境变量且无配置文件） |
| ① 模式选择 | 裸调用 `/lzl-worklog`（或 `/worklog`）且用户没说要做哪个 |
| ② 日期范围 | 模式 A 第 1 步；汇报第 3 步（**全量扫描模式直接跳过本闸口**） |
| ③ 条目/清单确认 | 模式 A 第 4 步；汇报第 6 步 |

闸口只在相应信息缺失或尚需本次写入确认时触发，已明确的选择不重复询问。仅在聊天中展示或修改草案时，不要求初始化存储、读取无关日志、确认正式归档或询问 Word；用户随后要求保存时，按清单确认规则处理。

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
    ├── md形式/
    │   ├── <起点日期>.md             # 工作记录类，兼容既有文件名
    │   └── <起点日期>-云端提交.md     # 云端提交类
    └── word形式/                     # 导出时使用相同文件名主干及 .docx
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

## 周报结构与表达

以下规则用于记录、候选提炼和周报成稿；用户明确指定的结构优先。

1. **项目 → 功能主线 → 各仓具体改动**：以项目为主标题，先识别并概括读者关心的功能或工作主线，说明完成或完善了什么，再在同一功能下按实际涉及的仓库或模块说明各自的具体行为。例如在“AI 解读”下分别写 Web 页面、Server 解读能力，在“环境权限授权”下分别写各端职责。零散修复和验证归入相应功能，不抢占主线；独立事项单列。只写实际涉及的仓库，单仓或非代码项目按真实模块、交付物灵活组织；多个项目分别成节。
2. **每条信息适中**：用简短功能名加一至三句，说明改了什么、影响哪个行为，以及需要保留的关键细节。合并同一事项的多轮修改，保留不同功能的差异。避免只有“优化体验、提升稳定性”等结论，也避免逐文件、逐命令、逐测试复述过程；不以固定条数或字数凑内容。
3. **不强制叙事标签**：不要求每条都有“痛点问题—关键改动—实际效果”，也不换成另一套固定三段或四段。背景确有解释作用时融入一句；验证、提交或部署状态可放在条目末或各仓结尾，避免逐条重复。用户要求分析需求背景或业务价值时，再按需展开。
4. **仓库归属准确**：跨仓功能分别说明各仓承担的实际改动，如命令行入口、服务端权限校验、前端授权反馈；不把同一个整体验证结果在各仓重复算作独立成果。维护在线表等协作事项可用简短附注承接，不为凑分类新增仓库。
5. **事实与时间准确**：请求、计划、调查结论和实际修复分别陈述；未知不补造。区分工作发生日期、会话活跃日期和补录日期，不能把上周工作因本周补录而计成本周新增。区分本地验证、本地提交、推送分支、发布安装包和部署；技能发现与离线测试不能替代真实业务验收。
6. **术语服务于准确表达**：保留读者需要辨认的项目、仓库、模块和功能名；陌生私有代号首次出现时补充职能说明。不要把具体功能过度泛化成空泛业务价值，也不要将“排查提交拦截原因”拔高成未经证实的“完善规则并解除阻塞”。省略 AI 调度、工具调试流水账及密钥等敏感内容。
7. **附加章节按需**：不默认添加“下周重点与协作项”、风险清单或无依据的“暂无阻碍”。用户要求计划、记录里已有明确安排或站会场景需要时再写；建议与已确认安排分别标明。

### 记录与汇报的衔接

- 新记录和扫描素材尽量保留项目、仓库、实际发生日期、具体改动、验证与交付状态；未知归属不猜测，只有影响分组或结论时才询问。
- 历史日志中的三段式仍可作为事实材料读取，不为套用新格式回写旧日志。
- 用户已给出项目、日期、资料或已确认条目时直接沿用；工作记录类优先使用指定记录，不为凑五源重新全量扫描。云端提交类可用日志定位相关仓库、分支和本人工作范围，但成果本身必须由云端提交支持。只有资料不足以判断归属或完成状态时才补证。
- 用户只要求修改已展示草案时，直接按反馈重写；正式归档仍遵守清单确认闸口，不重复索要已明确的范围与结构。

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
3. 以当天日期 `MM-DD` 分节，追加具体改动。保留项目/仓库归属、已知发生日期和必要交付状态，不要求补齐痛点或效果标签；用户只提供一句事实时可单行记录：

```markdown
## 08-12
### [集群数仓-命令行-输出格式] 统一费用查询的 CSV 输出
- 命令行工具：将费用查询结果统一为可解析的 CSV，补齐字段转义和错误退出码；已完成本地回归，尚未推送。
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
3. **提炼候选（按项目与仓库分组，仅供展示，禁止直接落盘）**：
   - 轻读各源真实用户消息、工具调用及结果，合并同一事项的重复记录。按项目、实际仓库分组，保持候选连续编号；每条写具体改动、必要细节及可证实的验证/交付状态，不强制补写背景或效果：
     ```markdown
     集群数仓相关开发 / 命令行工具
     1. **统一查询输出**：修复 CSV 转义和错误退出码，完成本地回归；尚未推送。
     集群数仓相关开发 / 服务端
     2. **补充凭证接口校验**：校验操作人身份与目标集群，保留权限不足提示；真实授权待配套环境验收。
     ```
   - 按「周报结构与表达」保持具体、适度；保留必要仓库与功能名，省略 AI 调度、调试流水账及密钥。记录实际发生日期，勿将会话活跃时间直接当成全部工作的发生日期。
4. **用户确认（闸口③，硬停轮，必须精确到条目）**：展示编号候选 + "要记哪几条？"（如"记 1、3"或"只记第 2 条"）后立即结束本轮回复。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
5. **落盘（只写用户确认的条目）**：严格按用户确认的编号/条目，将具体改动及项目/仓库归属、已知发生日期和必要交付状态追加到 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`）。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 去重与防丢失

### 去重（两种模式落盘前都执行）
1. 读 `$DATA_ROOT/日志/$MONDAY.md`（默认 `报告文档/需求/日志/$MONDAY.md`）现有条目，提取所有 `[需求名]` 标签（`- [XX] ...`）。
2. 新条目 `[需求名]` 已存在 → 跳过并提示"该需求已记录，跳过"，不重复追加。
3. 语义相近但标签不同 → 模式 A 由用户确认时人工去重；模式 B 提示用户"是否合并到已有条目"。

### 防丢失
- 日志文件**只追加从不覆盖**；生成周报只写 `周报/`，绝不改动 `日志/`。
- 模式 A 定期（阶段完成时）捞会话兜底，与随手记录互为备份。

## 汇报（触发词：周报 / 汇报 / 产出 / 站会）

1. 计算本周一 `$MONDAY`，依据「两类周报」确定来源口径，沿用用户已选类型。
2. 工作记录类优先使用用户指定材料，需要补充主动记录时再读 `$DATA_ROOT/日志/$MONDAY.md`。云端提交类先按 [references/cloud-weekly.md](references/cloud-weekly.md) 核验仓库、远端引用和范围内实际差异；不把会话中的“已推送”声明直接当作云端证据。仅展示草案且给定材料已足够时，不要求先读取存储配置或无关日志。
3. **确定日期与材料范围**：用户已明确“本周”等日期或指定“这些记录”时直接沿用；范围不明时才进入闸口②，展示 A. 本周一-现在（默认）/ B. 七天前-现在 / C. 从上次搜索-现在（无断点记录时说明并重新展示其余选项）/ D. 自定义后立即结束本轮回复。先核对实际工作日期，剔除只在本周补录的上周工作；前期成果的本周整合、验证和交付可如实记录为本周进展。材料已足够时无需再扫描。工作记录类需要补证时读取范围内相关会话源；云端提交类依据云端流程核对提交日期、基线与引用，不强制扫描五源。任一源不可读则披露，不当作没有工作。只有实际会话扫描才更新会话搜索断点，云端核验不更新该断点。记范围起点 `$START`（周报文件名据此）：
   - A → `$START=$MONDAY`
   - B → `$START=$(date -d "-6 days" +%F)`（含今天共 7 天）
   - C → `$START=` 断点文件里存的日期
   - D → `$START=` 用户给的起始日期
4. 材料较多或需要补证时，按需并行派代理提炼素材（契约见 `references/agent-team-contract.md`），受宿主并发能力约束。工作记录类可按五源分工；云端提交类宜按仓库分工，提供范围、相关分支和取证边界。代理可直接返回素材或写到指定中间文件。被跳过的源不派代理、不产空草稿；已有材料足够时不重复派任务。
5. 主线程合成草案（暂不落盘）：按选定类型的证据提炼成果，按「周报结构与表达」先概括项目的功能主线，再说明各仓具体改动。云端提交类将多分支的同一改动整合去重，不按分支列标题、不混入未推送工作；互斥实现不假装已经合为同一版本。跨仓事项说明各自承担部分，保留必要状态，不泛化为空泛价值，不强制三段式或下周计划。附简短编号清单用于正式归档确认，可引用正文已有编号，不重复整份内容。
6. **正式归档前的清单确认（闸口③，硬停轮）**：需要正式保存且尚无本次内容确认时，展示编号清单，问"全部写入，还是删掉哪几条？"后立即结束本轮回复。用户确认后才写入；点名删除的条目剔除；含糊回答必须再问，无确认不写。仅展示或修改草案时直接返回正文，不为归档另行提问。
7. 正式保存时确定 `$REPORT_STEM`：工作记录类为 `$START`，云端提交类为 `${START}-云端提交`；写入 `$DATA_ROOT/周报/md形式/$REPORT_STEM.md`。只清理本次实际生成的中间草稿，不删除另一类周报或既有成果。
8. 触发词含"站会/晨会" → 内容自动对齐 Scrum 节奏，直接作为站会发言稿。

### 周报模板（项目 → 功能主线 → 各仓具体改动）

两类共用以下结构；按实际功能、涉及的仓库和用户要求调整。正式正文保留读者需要的具体改动，来源定位留在素材中；云端取证时涉及的分支不成为正文副标题。

```markdown
# <项目名称及本周工作，如：集群数仓相关开发>

时间：<起点>—<终点>

## 一、<功能主线>

<简要概括功能及其用户可见行为。>

- **Web — <具体改动>**：<页面或交互的实际变化>。
- **Server — <具体改动>**：<接口、校验或数据处理的实际变化>。
- **CLI — <具体改动>**：<命令行实际承担的变化>。

<必要时集中说明验证及交付状态。>

## 二、<另一功能主线>

- **<实际涉及的仓库或模块> — <具体改动>**：<说明具体行为>。

<如有必要，用短句附注交付表或协作资料更新；不默认添加下周计划。>
```

9. 正式写入后告知日期、周报路径与材料覆盖情况；仅展示草案时不宣称已保存。无记录无会话时提示先"记录一下"或"梳理一下"。
10. 正式周报写入后，可询问用户是否需要导出 Word；仅展示或修改聊天草案时不追加此问题。需要则查本地 docx 相关 skill，将本次 `$DATA_ROOT/周报/md形式/$REPORT_STEM.md` 转为 `$DATA_ROOT/周报/word形式/$REPORT_STEM.docx`，两类文件不互相覆盖；查不到则告知用户并询问替代方案。
