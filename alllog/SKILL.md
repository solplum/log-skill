---
name: alllog
description: 全量挖掘 CC+Codex+ZCode+MiniMax Code 历史会话攒简历素材（随手记录+主动梳理双模式，挑选确认后落盘，按项目汇总成素材库），为简历优化做准备。仅用户手动 /alllog 触发，禁止从对话关键词自动触发。数据存 $ALLLOG_DATA_ROOT（默认 ~/alllog）。
---

# alllog 简历素材·全量记录

**仅手动触发**：用户显式输入 `/alllog`（或点名 alllog）才运行，对话中出现"素材库""记简历"等词不得自动调用本 skill。

## 闸口铁律（最高优先级，覆盖一切执行惯性）

以下闸口必须**停轮等待**：展示选项/候选后**立即结束本轮回复**，用户未回复前禁止任何扫描、深读、落盘：

| 闸口 | 时机 |
|------|------|
| ① 模式选择 | 裸调用 `/alllog` 且用户没说要做哪个 |
| ② 日期范围 | 模式 A 第 1 步 |
| ③ 项目挑选 | 模式 A 第 3 步（会话 > 50 或选"全部"时） |
| ④ 条目确认 | 模式 A 第 5 步 |

- **禁止自问自答**：同一回合内提出问题又自行回答并继续执行 = 违规（实测 Claude 会"选最近 30 天""四个项目全选"这样替用户做决定一路跑完）。
- 回答含糊（"都行""好""随便"）≠ 明确选择，必须再问；**无确认 = 0 条写入**，绝不默认全选。

裸调用 `/alllog`（无参数、未指向任何模式）→ 先闸口①问："记一条 / 挖素材 / 出素材库？"。用户话里已明确指向时直接进入："全量记一下：…"→模式 B；"全量梳理/挖简历素材"→模式 A；"素材库/汇总简历素材"→汇总。

把四个 CLI（CC/Codex/ZCode/MiniMax Code）的历史会话挖成简历素材（项目经历/技术亮点/量化成果），用户挑选后落盘，按项目汇总成简历素材库，为简历优化做准备。纯原生工具，无脚本依赖。与 worklog（周报·需求叙事）互补：worklog 记"本周做了啥给老板看"，alllog 记"值得写进简历的项目素材"，两者存储互不干扰。

## 存储布局

数据根可配置：环境变量 `ALLLOG_DATA_ROOT` 优先，未设置时默认 `~/alllog`——任意 CWD 调用都落同一处（bash 写作 `$ALLLOG_DATA_ROOT/素材/日志` 与 `$ALLLOG_DATA_ROOT/素材/整理`；仓库里 `scripts/paths.py` 是同一条解析规则的可执行副本，单测直接驱动它）：

```
$ALLLOG_DATA_ROOT/素材/
├── 日志/<YYYY-MM-DD>.md     # 原始日志：挑选落盘的素材，按记录日命名，只追加从不覆盖
└── 整理/<YYYY-MM-DD>.md     # 整理版：按项目归组的汇总快照，每次汇总生成当日新快照（同日覆盖重生成）
```

- `<YYYY-MM-DD>` = 记录/生成当天（`date +%F`），**不按周锚定**（全量积累，区别于 worklog 的周一锚定）。
- **读取语义（alllog 自身）：`日志/` 是唯一事实底账**——去重、续挖停点、汇总一律**全量读取所有日期的日志文件**，不按新旧筛选、不因快照存在而偷懒；`整理/` 是派生快照，只为下游简历制作服务，**不参与 alllog 的任何读取与判定**。旧日志不清理。
- 「制作简历只读 整理/ 最新快照」是**消费侧规则**，由 `job-tailored-resume` 的 SKILL.md 承载；本 skill 只生产，不复述、不受其约束。
- 条目格式，单行，`## MM-DD` 分节：

```markdown
## 08-16
- [项目名] 做了什么 + 用了什么技术 + 结果/量化（缺失记"待补充"，禁止编造）
```

## 数据源

| 源 | 路径 | 时间基准 |
|----|------|---------|
| CC | `~/.claude/projects/*/*.jsonl`（**所有项目目录**，一个都不能漏） | JSONL 内 `"timestamp"`（UTC） |
| Codex | 索引 `~/.codex/session_index.jsonl`（**首选**，含 thread_name + updated_at）；会话文件 `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`，归档在 **`~/.codex/archived_sessions/rollout-*.jsonl`（顶层平铺，不在 sessions/ 下）** | 索引 `updated_at`（UTC）；文件名内嵌时间戳（本地） |
| ZCode | `~/.zcode/cli/db/db.sqlite`（SQLite：`session`/`message`/`part` 三表） | `session.time_updated`（epoch 毫秒，绝对时间） |
| MiniMax Code | `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/messages.jsonl` | 行内 `message.timestamp`（epoch 毫秒，绝对时间） |

### 时区归一（重要，防边界日漏记录）
- CC `timestamp` 是 UTC（如 `2026-08-12T02:00:00.000Z`，本地 UTC+8 → 08-12 10:00）。
- 按日期过滤"起点之后"前，统一把 CC timestamp 转本地再比较（`date -d "<TS>" +%F`）。
- 否则起点日 00:00–07:59 落地的 UTC 记录（仍是前一日日期）会被漏掉。
- Codex `session_index.jsonl` 的 `updated_at` 是 UTC（带 Z 后缀），`astimezone()` 转本地后再比较；sessions/ 目录与文件名内嵌时间戳已是本地时间，直接比较。
- ZCode 时间戳是 epoch 毫秒（绝对时间），无时区换算问题：起点转毫秒 `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))` 后直接比较；挖全部时 `$START_MS=0`。
- MiniMax Code 时间戳同为 epoch 毫秒，无换算问题，比较方式同 ZCode；**不要用目录名日期过滤**（目录名是会话创建时刻，跨天长会话按它过滤会漏，须用消息内末条 timestamp 判断，同 CC 的末条原则）。
- CC 会话日期用**末条** timestamp 判断（跨天长会话从起点前延续到起点后也算"起点后有活动"），禁用首条 timestamp 过滤（会把 08-10 开始、08-20 还在用的会话漏掉）。

## ZCode 会话查询（SQLite）

ZCode 会话存在 SQLite 库里，**必须只读打开**（ZCode 运行时正占用该库，`mode=ro` 与 WAL 并发安全，已实测）：

```bash
START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))   # $START=起点日期 YYYY-MM-DD；全部则传 0
python - "$START_MS" <<'EOF'
import sqlite3, json, sys, os, datetime, pathlib
sys.stdout.reconfigure(encoding='utf-8')   # 必须：否则 Windows 下中文标题输出 GBK 乱码（实测踩坑）
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
- `session.title` 由 CLI 维护，质量可靠，可直接作会话主题。`synthetic=1` 是系统注入，查询已排除。

## CC 会话查询（脚本给死，禁现场自由发挥）

CC 源三大坑（2026-08-21 实测踩过）：**①项目目录扫漏**（只扫一个目录漏掉其余 6 个）；**②真实用户会话认不出**（jsonl 里混着 skill 注入会话——首条 user 是 "Base directory for this skill..."——和 `last-prompt` 空壳文件，曾整批被误判"自动化空壳"跳过，实际混着真实工作）；**③乱码**（Windows 下须 reconfigure UTF-8）。扫会话头必须用下面的脚本（识别标志：`userType == 'external'` 且首条消息不以 skill 注入标记开头）：

```bash
python - "$START" <<'EOF'
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')
START = sys.argv[1]            # YYYY-MM-DD；挖全部传 0000-00-00
SKILL_INJECT = ('Base directory for this skill', 'This is a skill', '[Request interrupted')
for f in sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))):
    last = None; msgs = []
    for line in open(f, encoding='utf-8', errors='ignore'):
        try: o = json.loads(line)
        except: continue
        if o.get('timestamp'): last = o['timestamp']          # 全文件末条，跨天会话不漏
        if o.get('type') != 'user' or o.get('userType') != 'external': continue
        content = o.get('message', {}).get('content')
        if not isinstance(content, list): continue
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                t = c.get('text', '').strip()
                if t and not t.startswith(SKILL_INJECT): msgs.append(t)
    if not msgs or not last or last[:10] < START: continue    # msgs 空 = 空壳/skill 会话，跳过
    proj = os.path.basename(os.path.dirname(f))
    print(f"{last[:10]}  [{proj}]  {f}  {msgs[0][:80]}")
EOF
```

- 输出列：末条日期 | 项目目录 | **文件全路径**（深读按它回找）| 首条真实用户消息（即标题）。
- **深读**：同一脚本把 `msgs[0][:80]` 改为逐条打印全部 `msgs`（每条截 200 字），并只处理选中的文件路径。
- 图占位（`[Image #1]`）开头的消息是真实用户输入，不算 skill 注入，保留。

## Codex 会话查询（索引优先）

扫会话头**首选索引**（比扫目录可靠，thread_name 即标题）：

```bash
python - "$START" <<'EOF'
import json, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
START = sys.argv[1]            # YYYY-MM-DD；挖全部传 0000-00-00
idx = os.path.expanduser('~/.codex/session_index.jsonl')
if not os.path.exists(idx): print('(无 Codex 索引，跳过该源)'); sys.exit()
for line in open(idx, encoding='utf-8'):
    try: o = json.loads(line)
    except: continue
    u = o.get('updated_at', '')
    if not u: continue
    local = datetime.datetime.fromisoformat(u.replace('Z', '+00:00')).astimezone()
    if local.strftime('%Y-%m-%d') >= START:
        print(f"{local:%Y-%m-%d}  [{o.get('id','')[:8]}]  {o.get('thread_name','(无标题)')[:60]}")
EOF
```

- **深读定位文件**：按会话 id 前缀 glob 两处：`~/.codex/sessions/*/*/*/rollout-*<id>*.jsonl` 和 `~/.codex/archived_sessions/rollout-*<id>*.jsonl`（归档在顶层，别去 sessions/ 下找）。
- 索引不存在时才退化到扫 `sessions/YYYY/MM/DD/` 目录（文件名内嵌本地时间戳 `rollout-YYYY-MM-DDTHH-MM-SS`）。

## MiniMax Code 会话查询（脚本给死，禁现场自由发挥）

MiniMax Code（ZCode 系内核）会话按日期分层存 `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/`，核心是 `messages.jsonl`，每行一个消息对象：`message.role`（user/assistant）+ `message.content[]`（text 块）+ `message.timestamp`（epoch 毫秒）。目录名日期是会话创建时刻，**过滤必须用消息内末条 timestamp**（同 CC 的末条原则）。扫会话头用下面的脚本：

```bash
START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))   # $START=起点日期 YYYY-MM-DD；挖全部传 0
python - "$START_MS" <<'EOF'
import json, glob, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')   # 必须：Windows 下中文输出防 GBK 乱码
START_MS = int(sys.argv[1])
SKIP_PREFIX = ('<system-reminder', '<background-task-finished', 'Base directory for this skill', 'This is a skill', '[Request interrupted')
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

- 输出列：末条日期 | **文件全路径**（深读按它回找）| 首条真实用户消息（即标题）。
- **深读**：同一脚本把 `msgs[0][:80]` 改为逐条打印全部 `msgs`（每条截 200 字），并只处理选中的文件路径。
- `<system-reminder>`/skill 注入开头的 user 消息是系统注入不是真实输入，脚本已排除；全被排除的会话跳过。
- `manifest.json` 有 `createdAtMs`/`updatedAtMs` 但**无标题与工作目录**，会话主题只能用首条真实用户消息。
- `~/.minimax/` 不存在 → 跳过该源并提示。

## 记录 · 模式 B：随手记录

调用后用户输入形如"全量记一下：..."、"记简历：..." → 走本模式。零摩擦，用户说啥记啥。

1. 取今天 `$TODAY=$(date +%F)`。
2. 定位 `$ALLLOG_DATA_ROOT/素材/日志/$TODAY.md`，不存在则创建（含目录）。
3. 以 `## MM-DD` 分节，追加 `- [项目名] <一句话>`。
4. 当天节已存在则在其下追加；**只追加，绝不覆盖或改动历史条目**。

## 记录 · 模式 A：主动梳理（挖简历素材）

调用后用户输入形如"全量梳理"、"挖简历素材" → 走本模式；裸调用未带内容时不直接进入，先走闸口①模式选择。

1. **选日期范围（闸口②，硬停轮）**：展示下列选项后立即结束本轮回复，用户明确选择后再扫描：
   - A. 全部会话（量大时先聚类，见第 3 步）
   - B. 从上次抓取至今（**续挖，最常用**）：上次停点 = `ls -1 "$ALLLOG_DATA_ROOT/素材/日志/" | sort | tail -1 | cut -d. -f1`，起点 = 停点 +1 天（`date -d "$LAST +1 day" +%F`）；`日志/` 为空 → 等同 A
   - C. 最近 30 天
   - D. 自定义——向用户要起止日期
   - 用户说"接着上次挖/从上次停的地方继续"等续挖语义 → 直接选 B，不再反问。
2. **扫会话**：CC/Codex/ZCode/MiniMax Code 四源，**分别用上文「CC 会话查询」「Codex 会话查询」「ZCode 会话查询」「MiniMax Code 会话查询」四段给死的脚本**，不许现场自造解析方法（任一源探测不到则跳过并提示）。扫描结果先留底（含被排除会话的计数），供覆盖度回执用。
3. **量大先聚项目（闸口③，硬停轮）**：**四源纳入会话数合计** > 50 或选"全部"时，先只列会话头（日期 + 标题 + directory），按 `directory` 聚类成项目清单（目录名 + 会话数 + 时间跨度），展示后问"挖哪些项目？"并立即结束本轮回复；用户选定后**只深读所选项目的会话**（避免全量深读拖垮会话），禁止自选"全部项目"。**判断是否超 50 必须用四源合计数，禁止单看一个源就下结论**（2026-08-21 实测：只按 ZCode 的 16 个判断"未超 50"直接出候选，实际 CC 还有一批没统计）。MiniMax Code 会话无 directory，聚类时以会话主题关键词归入项目。
4. **提炼候选（仅供展示，禁止直接落盘）**：轻读所选会话的用户消息/工具调用，产出**编号**列表 `1. 日期 + 项目/主题 + 2-3 要点（技术栈/难点/结果）`。**展示候选时必须同时附「覆盖度回执」（见下文铁律），让用户看见四源各挖了多少、漏没漏。**简历视角优先：可量化成果 > 技术难点攻克 > 架构决策 > 日常修复。用户消息里可能贴过密钥/token/密码（实测存在），候选与落盘一律脱敏或省略，敏感串不得出现在任何输出中。
5. **用户确认（闸口④，硬停轮，必须精确到条目）**：展示编号候选 + "要记哪几条？"（如"记 1、3"）后立即结束本轮回复。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
6. **落盘（只写用户确认的条目）**：逐条按模式 B 格式追加到 `素材/日志/$TODAY.md`。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 覆盖度回执（硬性要求）

**每次向用户展示候选清单（闸口③聚类清单或闸口④编号候选）时，必须同屏附带四源覆盖表**，缺一不可。2026-08-21 实测教训：第一轮候选实际只深读了 ZCode 一个源，CC 源静默放弃、Codex 源误判为空，且候选展示时未向用户交代——用户被迫反问"只有这几天的吗"才暴露。

格式：

```
| 源 | 扫描数 | 纳入 | 排除（原因拆分） |
|----|--------|------|------------------|
| CC | N | N | 空壳 N / skill 注入 N / 日期外 N |
| Codex | N | N | 日期外 N |
| ZCode | N | N | 日期外 N |
| MiniMax Code | N | N | 纯注入 N / 日期外 N |
```

- 纳入数为 0 的源**必须写明**是"真空"（该时段用户确实没用过，如 Codex 08-14 后无会话）还是"方法失败/未深挖"，禁止静默缩水。
- 起止日期（本次挖的时间范围）必须写在表前。

## 去重与防丢失

### 去重（两种模式落盘前都执行，跨整个 日志/ 目录）
1. 读 `素材/日志/` 下**所有** `.md` 的既有条目，提取每条的 `[项目名]` 与要点。`整理/` 是派生快照，不参与去重判定。
2. 新条目与既有条目"项目名相同且要点语义相同" → 跳过并提示"该要点已记录，跳过"。
3. 项目名相同但要点不同 → 正常追加（简历素材按项目累积，同项目多条合法，区别于 worklog 的按需去重）。

### 防丢失
- `日志/` 只追加从不覆盖；汇总只写 `整理/` 当日快照（同日覆盖重生成），绝不改动 `日志/`。
- `整理/` 旧快照保留作历史；去重与汇总只认 `日志/` 全量，与快照新旧无关。
- 梳理时捞会话兜底，与随手记录互为备份。

## 汇总（调用后用户说"素材库" / "汇总简历素材" / "出简历素材库" → 走本模式）

1. 读 `素材/日志/` 全部 `.md`，按文件名日期升序排列。为空 → 提示先"全量记一下"或"全量梳理"。
2. 主线程直接合成（只读本地文件，无需派 agent）：按 `[项目名]` 归组，组内按日期排序，写 `$ALLLOG_DATA_ROOT/素材/整理/<$TODAY>.md`（当日快照覆盖重生成，不动 `日志/`）。
3. 模板：

```markdown
# 简历素材库（生成于 <YYYY-MM-DD HH:MM>，共 <项目数> 项目 <素材数> 条）

## 项目：<项目名>
- **背景**：<为什么做，缺失标"待补充">
- **技术栈**：<从条目提炼，去重>
- **亮点/难点**：<攻克了什么>
- **结果/量化**：<数据/效果；缺失标"待补充"，禁止编造>
- **素材记录**：
  - <MM-DD 各条目原文>
```

4. 生成后回执：项目数、素材条数、文件路径，并注明"制作简历只需读这份最新整理快照"。
5. 提示可衔接 `job-tailored-resume` skill 定制简历（含 STAR 改写、岗位关键词对齐）；素材读取规则由该 skill 自行约束。
