---
name: lzl-alllog
description: 全量挖掘 CC+Codex+ZCode+MiniMax Code+Antigravity 五源历史会话攒简历素材（随手记录+主动梳理双模式，挑选确认后落盘，按项目汇总成素材库），为简历优化做准备。首次使用引导存储目录配置并支持全量扫描；简历视角去黑话与私有代号。触发词："全量记一下"、"挖简历素材"、"素材库"、"/lzl-alllog"、"/alllog"。数据存配置数据根（默认 ~/alllog）。
---

# lzl-alllog 简历素材·全量记录

**仅手动触发**：用户显式输入 `/lzl-alllog`、`/alllog`（或点名 lzl-alllog / alllog）才运行，对话中出现"素材库""记简历"等词不得自动调用本 skill。

## 闸口铁律（最高优先级，覆盖一切执行惯性）

以下闸口必须**停轮等待**：展示选项/候选后**立即结束本轮回复**，用户未回复前禁止任何扫描、深读、落盘：

| 闸口 | 时机 |
|------|------|
| ⓪ 存储目录确认 | 首次使用且未检测到存储配置（无环境变量且无配置文件） |
| ① 模式选择 | 裸调用 `/lzl-alllog`（或 `/alllog`）且用户没说要做哪个 |
| ② 日期范围 | 模式 A 第 1 步（**全量扫描模式直接跳过本闸口**） |
| ③ 条目确认 | 模式 A 第 4 步（面对按事情提炼的 STAR 候选清单，必须精确到条目编号） |

- **禁止自问自答**：同一回合内提出问题又自行回答并继续执行 = 违规（实测 Claude 会"选最近 30 天""四个项目全选"这样替用户做决定一路跑完）。
- 回答含糊（"都行""好""随便"）≠ 明确选择，必须再问；**无确认 = 0 条写入**，绝不默认全选。

裸调用 `/lzl-alllog`（或 `/alllog`，无参数、未指向任何模式）→ 先闸口①问："全量扫描（建初始底账） / 主动梳理挖素材 / 随手记一条 / 出简历素材库？"。用户话里已明确指向时直接进入："全量记一下：…"→模式 B；"全量扫描/全量挖掘"→模式 A（全量，跳过闸口②）；"挖简历素材/梳理素材"→模式 A；"素材库/汇总简历素材"→汇总。

把五个源（CC/Codex/ZCode/MiniMax Code/Antigravity）的历史会话挖成高质量简历素材（项目经历/技术亮点/量化成果），用户挑选后落盘，按项目汇总成简历素材库，为简历优化做准备。纯原生工具，无脚本依赖。与 lzl-worklog（周报·需求叙事）互补：lzl-worklog 记"本周做了啥给组会和老板看"，lzl-alllog 记"值得写进简历的项目经历与技术亮点"，两者存储互不干扰。

## 存储布局

数据根可配置：环境变量 `LZL_ALLLOG_DATA_ROOT`（兼容 `ALLLOG_DATA_ROOT`）优先，其次读取配置文件 `~/.config/lzl-alllog/config.json`（兼容 `~/.config/alllog/config.json`），未设置时默认 `~/alllog`——任意 CWD 调用都落同一处（bash 写作 `$ALLLOG_DATA_ROOT/素材/日志` 与 `$ALLLOG_DATA_ROOT/素材/整理`；仓库里 `scripts/paths.py` 是同一条解析规则的可执行副本，单测直接驱动它）：

### 首次使用初始化（闸口⓪，硬停轮）
若未设置环境变量，且 `~/.config/lzl-alllog/config.json` 与 `~/.config/alllog/config.json` 均不存在：
向用户展示下列选项并**立即结束本轮回复**，停轮等待用户选择：
1. **【推荐】全局统一存储**：`~/alllog`（跨项目统一记录简历素材，安全且便于按项目汇总结算，不污染代码仓库）
2. **当前项目工作区**：`./素材/`（与当前代码仓库同放，适合单项目强隔离）
3. **自定义路径**：指定任意绝对路径

用户选定后，写入 `~/.config/lzl-alllog/config.json`（格式形如 `{"data_root": "<选中路径>"}`），后续调用自动读取，不再重复询问。

### 目录结构

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
| Antigravity | 双端同构：桌面端 `~/.gemini/antigravity/` + CLI `~/.gemini/antigravity-cli/` 的 `conversation_summaries.db` 与 `brain/*/transcript.jsonl` | `last_modified_time`（UTC，ISO 8601） |

### 时区归一（重要，防边界日漏记录）
- CC `timestamp` 是 UTC（如 `2026-08-12T02:00:00.000Z`，本地 UTC+8 → 08-12 10:00）。
- 按日期过滤"起点之后"前，统一把 CC timestamp 转本地再比较（`date -d "<TS>" +%F`）。
- 否则起点日 00:00–07:59 落地的 UTC 记录（仍是前一日日期）会被漏掉。
- Codex `session_index.jsonl` 的 `updated_at` 是 UTC（带 Z 后缀），`astimezone()` 转本地后再比较；sessions/ 目录与文件名内嵌时间戳已是本地时间，直接比较。
- ZCode 时间戳是 epoch 毫秒（绝对时间），无时区换算问题：起点转毫秒 `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))` 后直接比较；挖全部时 `$START_MS=0`。
- MiniMax Code 时间戳同为 epoch 毫秒，无换算问题，比较方式同 ZCode；**不要用目录名日期过滤**（目录名是会话创建时刻，跨天长会话按它过滤会漏，须用消息内末条 timestamp 判断，同 CC 的末条原则）。
- CC 会话日期用**末条** timestamp 判断（跨天长会话从起点前延续到起点后也算"起点后有活动"），禁用首条 timestamp 过滤（会把 08-10 开始、08-20 还在用的会话漏掉）。
- Antigravity 时间戳为 UTC ISO 8601 字符串（如 `2026-10-15 08:22:44+00:00`），转本地再比较。**桌面端（IDE / 2.0）与 CLI（agy）物理路径不同源，但底层表与 transcript 结构完全同构**，统一双端扫描合并。

## 外部读者视角与简历通俗化（去黑话与去自嗨铁律）

**简历素材库最终是给面试官、HR、技术委员会或跨团队评审看的，严禁直接照搬只有作者自己懂的内部代号与调试流水账。**

提炼候选（第 4 步）、用户确认（第 5 步）、生成简历素材库（汇总）必须严格遵守以下消歧与提炼规则：

1. **私有代号与内部工具通用化（杜绝自嗨孤立词）**：
   - 严禁出现未加解释的内部代号、私有工具、自研系统简称（如 `Mimosa`、自写脚本名、内部特定平台缩写）。
   - **替换为行业通用工程/业务语言**：
     - 例：`Mimosa 提交门禁` / `Mimosa 安全钩子` → 改为 `Git 代码提交静态安全合规门禁` 或 `代码提交规范检查钩子`。
     - 若确实需要保留专有名词，必须采用 **"通用工程职能（内部代号）"** 形式，如 `代码安全合规门禁系统（Mimosa）`、`数仓自动化同步服务`，确保任何面试官都能一眼看懂其业务职能。
2. **聚焦业务价值与工程成果，拒绝个人调试流水账**：
   - 严禁把“被内部钩子拦截查原因”当作简历亮点（如“排查被 Mimosa 拦截的原因及分类”）。
   - 必须按规范提炼为业务价值：“完善集群数仓代码提交规范与静态安全检查规则，解除门禁拦截并形成排查指引”。
3. **严格抹除 AI 执行痕迹**：
   - 严禁出现“开辟子 Agent 开展全篇结构审计”、“结合多轮逻辑审查对话调整记录”等 AI 工具链自身的执行过程；必须转换为使用者本人推进的技术与工程成果。
4. **简历 STAR 提炼规范（结构化成果）**：
   - 简历视角优先：可量化成果 > 技术难点攻克 > 核心架构决策 > 业务系统重构。
   - 提炼结构：
     - **背景/痛点**：解决了什么业务瓶颈或工程低效；
     - **技术动作/亮点**：采用了何种架构方案、核心算法或关键技术；
     - **结果/量化**：产生了什么性能提升、稳定性收益或业务成效（缺失记"待补充"，禁止编造）。

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

调用后用户输入形如"全量记一下：..."、"记简历：..." → 走本模式。零摩擦，用户说啥记啥。

1. 取今天 `$TODAY=$(date +%F)`。
2. 定位 `$ALLLOG_DATA_ROOT/素材/日志/$TODAY.md`，不存在则创建（含目录）。
3. 以 `## MM-DD` 分节，追加 `- [项目名] <一句话>`（或按 STAR 提炼）。
4. 当天节已存在则在其下追加；**只追加，绝不覆盖或改动历史条目**。

## 记录 · 模式 A：主动梳理（挖简历素材）

调用后用户输入形如"全量梳理"、"挖简历素材"、"全量扫描" → 走本模式；裸调用未带内容时不直接进入，先走闸口①模式选择。

1. **选日期范围（闸口②，硬停轮；全量扫描模式直接跳过本步）**：
   - **穿透闸口②规则**：若在闸口①选择了「全量扫描」，或用户指令明确包含「全量扫描」「全量挖掘」「建初始底账」等全量意图，**意图已锁定为全部历史，严禁再次询问日期范围，直接将起点设为全部（`$START=0000-00-00`，`$START_MS=0`），立即开始第 2 步扫描**！
   - 若用户进入的是普通梳理，展示下列选项后立即结束本轮回复，用户明确选择后再扫描：
     - A. 全部会话
     - B. 从上次抓取至今（**续挖，最常用**）：上次停点 = `ls -1 "$ALLLOG_DATA_ROOT/素材/日志/" | sort | tail -1 | cut -d. -f1`，起点 = 停点 +1 天（`date -d "$LAST +1 day" +%F`）；`日志/` 为空 → 等同 A
     - C. 最近 30 天
     - D. 自定义——向用户要起止日期
     - 用户说"接着上次挖/从上次停的地方继续"等续挖语义 → 直接选 B，不再反问。
2. **扫会话（五源探测）**：CC/Codex/ZCode/MiniMax Code/Antigravity 五源，**分别用上文「CC 会话查询」「Codex 会话查询」「ZCode 会话查询」「MiniMax Code 会话查询」「Antigravity 会话查询」五段给死的脚本**，不许现场自造解析方法（任一源探测不到则跳过并提示）。扫描结果先留底（含被排除会话的计数），供覆盖度回执用。
3. **按事情提炼候选（严禁按磁盘路径分类，直出结构化 STAR 候选）**：
   - **分类铁律：绝对禁止以文件物理路径、工作区根目录（如 `~/workspace`、`/private/tmp`）作为分类维度！**
   - 必须结合五源会话头（标题 `title`、首条核心提问 `prompt`）及研发轨迹，**按真实事情、核心功能模块或工程专题归并提炼**（如 `【集群数仓专项 - 后端服务优化】`、`【代码合规门禁体系】`、`【工程效能工作流工具链】`）。
   - 产出**编号**列表 `1. [项目/系统名称 - 具体业务成果方向] + STAR 结构化要点`：
     - **背景/痛点**：解决了什么业务阻碍或工程瓶颈；
     - **技术动作/亮点**：采用了何种架构方案、关键技术或优化动作；
     - **结果/量化**：产生了什么性能提升、稳定性收益或业务成效（缺失标"待补充"，禁止编造）。
   - **严格执行去自嗨与去黑话铁律**：严禁出现内部未公开代号（如 Mimosa 替换为“Git 代码提交静态安全合规门禁”），严禁出现 AI 工具链自身调试痕迹（如“开辟子 Agent 开展全篇结构审计”等）；
   - 用户消息里可能贴过密钥/token/密码，候选与落盘一律脱敏或省略，敏感串不得出现在任何输出中。
   - **展示候选时必须同屏附「五源覆盖度回执」（见下文铁律），让用户看见五源各挖了多少、漏没漏。**
4. **用户确认（闸口③，硬停轮，一次性按真实事实勾选）**：展示编号候选 + "要记哪几条？"（如"全部"、"记 1、3"）后**立即结束本轮回复**。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
5. **落盘（只写用户确认的条目）**：逐条按模式 B 格式追加到 `素材/日志/$TODAY.md`。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 覆盖度回执（硬性要求）

**每次向用户展示闸口③编号候选清单时，必须同屏附带五源覆盖表**，缺一不可。禁止静默缩水或漏源。

格式：

```
| 源 | 扫描数 | 纳入 | 排除（原因拆分） |
|----|--------|------|------------------|
| CC | N | N | 空壳 N / skill 注入 N / 日期外 N |
| Codex | N | N | 日期外 N |
| ZCode | N | N | 日期外 N |
| MiniMax Code | N | N | 纯注入 N / 日期外 N |
| Antigravity | N | N | 日期外 N / 系统注入 N |
```

- 纳入数为 0 的源**必须写明**是"真空"（该时段用户确实没用过）还是"方法失败/未深挖"，禁止静默放弃。
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
3. 严格遵循「外部读者视角与简历通俗化」去黑话铁律，采用 STAR 结构生成素材库：

```markdown
# 简历素材库（生成于 <YYYY-MM-DD HH:MM>，共 <项目数> 项目 <素材数> 条）

## 项目：<项目名>
- **背景**：<为什么做/业务痛点，缺失标"待补充">
- **技术栈**：<从条目提炼，去重>
- **亮点/难点**：<攻克了什么技术难点与核心架构动作，杜绝自嗨与私有代号>
- **结果/量化**：<性能提升/稳定性收益/业务成效；缺失标"待补充"，禁止编造>
- **素材记录**：
  - <MM-DD 各条目原文>
```

4. 生成后回执：项目数、素材条数、文件路径，并注明"制作简历只需读这份最新整理快照"。
5. 提示可衔接 `job-tailored-resume` skill 定制简历（含 STAR 改写、岗位关键词对齐）；素材读取规则由该 skill 自行约束。
