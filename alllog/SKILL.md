---
name: alllog
description: 全量挖掘 CC+Codex+ZCode 历史会话攒简历素材（随手记录+主动梳理双模式，挑选确认后落盘，按项目汇总成素材库），为简历优化做准备。仅用户手动 /alllog 触发，禁止从对话关键词自动触发。数据存 $ALLLOG_DATA_ROOT（默认 ~/alllog）。
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

把三个 CLI 的历史会话挖成简历素材（项目经历/技术亮点/量化成果），用户挑选后落盘，按项目汇总成简历素材库，为简历优化做准备。纯原生工具，无脚本依赖。与 worklog（周报·需求叙事）互补：worklog 记"本周做了啥给老板看"，alllog 记"值得写进简历的项目素材"，两者存储互不干扰。

## 存储布局

数据根目录**由用户配置**，任意 CWD 调用都落同一处：

1. 若环境变量 `ALLLOG_DATA_ROOT` 已设置，用该绝对路径。
2. 否则默认 `~/alllog`（`$HOME/alllog`，Windows 为 `%USERPROFILE%\alllog`）。

不要把作者本机路径写死进 skill。首次使用前可自行指定，例如：

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
python scripts/paths.py          # prints the resolved root
```

`scripts/paths.py` is the same resolver the tests drive: env var first, else `~/alllog`.

```
$ALLLOG_DATA_ROOT/            # 默认 ~/alllog
├── 素材/<YYYY-MM-DD>.md     # 挑选落盘的简历素材，按记录日命名，只追加从不覆盖
└── 简历素材库.md            # 按项目归组的汇总视图，可重复生成，绝不改动 素材/
```

- `<YYYY-MM-DD>` = 记录当天（`date +%F`），**不按周锚定**（全量积累，区别于 worklog 的周一锚定）。
- 条目格式，单行，`## MM-DD` 分节：

```markdown
## 08-16
- [项目名] 做了什么 + 用了什么技术 + 结果/量化（缺失记"待补充"，禁止编造）
```

## 数据源

| 源 | 路径 | 时间基准 |
|----|------|---------|
| CC | `~/.claude/projects/**/*.jsonl` | JSONL 内 `"timestamp"`（UTC） |
| Codex | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` + `archived_sessions/` 兜底 | 目录/文件名（本地时间） |
| ZCode | `~/.zcode/cli/db/db.sqlite`（SQLite：`session`/`message`/`part` 三表） | `session.time_updated`（epoch 毫秒，绝对时间） |

### 时区归一（重要，防边界日漏记录）
- CC `timestamp` 是 UTC（如 `2026-08-12T02:00:00.000Z`，本地 UTC+8 → 08-12 10:00）。
- 按日期过滤"起点之后"前，统一把 CC timestamp 转本地再比较（`date -d "<TS>" +%F`）。
- 否则起点日 00:00–07:59 落地的 UTC 记录（仍是前一日日期）会被漏掉。
- Codex 目录/文件名已是本地时间，直接比较。
- ZCode 时间戳是 epoch 毫秒（绝对时间），无时区换算问题：起点转毫秒 `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))` 后直接比较；挖全部时 `$START_MS=0`。

## ZCode 会话查询（SQLite）

ZCode 会话存在 SQLite 库里，**必须只读打开**（ZCode 运行时正占用该库，`mode=ro` 与 WAL 并发安全，已实测）。仓库里 `scripts/zcode_sessions.py` 是同一条查询的可执行副本（`python scripts/zcode_sessions.py <START_MS> [db]`）：

```bash
START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))   # $START=起点日期 YYYY-MM-DD；全部则传 0
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
- `session.title` 由 CLI 维护，质量可靠，可直接作会话主题。`synthetic=1` 是系统注入，查询已排除。

## 记录 · 模式 B：随手记录

调用后用户输入形如"全量记一下：..."、"记简历：..." → 走本模式。零摩擦，用户说啥记啥。

1. 取今天 `$TODAY=$(date +%F)`。
2. 定位 `$ALLLOG_DATA_ROOT/素材/$TODAY.md`（未设置环境变量时 `$ALLLOG_DATA_ROOT` = `~/alllog`），不存在则创建（含目录）。
3. 以 `## MM-DD` 分节，追加 `- [项目名] <一句话>`。
4. 当天节已存在则在其下追加；**只追加，绝不覆盖或改动历史条目**。

## 记录 · 模式 A：主动梳理（挖简历素材）

调用后用户输入形如"全量梳理"、"挖简历素材" → 走本模式；裸调用未带内容时不直接进入，先走闸口①模式选择。

1. **选日期范围（闸口②，硬停轮）**：展示下列选项后立即结束本轮回复，用户明确选择后再扫描：
   - A. 全部会话（默认；量大时先聚类，见第 3 步）
   - B. 最近 30 天
   - C. 自定义——向用户要起止日期
2. **扫会话**：CC/Codex/ZCode 三源，筛选与查询方式同上（任一源探测不到则跳过并提示）。
3. **量大先聚项目（闸口③，硬停轮）**：会话总数 > 50 或选"全部"时，先只列会话头（日期 + 标题 + directory），按 `directory` 聚类成项目清单（目录名 + 会话数 + 时间跨度），展示后问"挖哪些项目？"并立即结束本轮回复；用户选定后**只深读所选项目的会话**（避免全量深读拖垮会话），禁止自选"全部项目"。
4. **提炼候选（仅供展示，禁止直接落盘）**：轻读所选会话的用户消息/工具调用，产出**编号**列表 `1. 日期 + 项目/主题 + 2-3 要点（技术栈/难点/结果）`。简历视角优先：可量化成果 > 技术难点攻克 > 架构决策 > 日常修复。用户消息里可能贴过密钥/token/密码（实测存在），候选与落盘一律脱敏或省略，敏感串不得出现在任何输出中。
5. **用户确认（闸口④，硬停轮，必须精确到条目）**：展示编号候选 + "要记哪几条？"（如"记 1、3"）后立即结束本轮回复。**用户未明确选择的条目，一律不得写入。** 回答含糊（"都行""好"）≠ 选择，必须再次询问，不得默认全选。
6. **落盘（只写用户确认的条目）**：逐条按模式 B 格式追加到 `素材/$TODAY.md`。落盘后回执："已写入 N 条：<条目列表>"；未写入的候选列出提醒（可改天再记）。

## 去重与防丢失

### 去重（两种模式落盘前都执行，跨整个 素材/ 目录）
1. 读 `素材/` 下**所有** `.md` 的既有条目，提取每条的 `[项目名]` 与要点。
2. 新条目与既有条目"项目名相同且要点语义相同" → 跳过并提示"该要点已记录，跳过"。
3. 项目名相同但要点不同 → 正常追加（简历素材按项目累积，同项目多条合法，区别于 worklog 的按需去重）。

### 防丢失
- `素材/` 只追加从不覆盖；汇总只写 `简历素材库.md`，绝不改动 `素材/`。
- 梳理时捞会话兜底，与随手记录互为备份。

## 汇总（调用后用户说"素材库" / "汇总简历素材" / "出简历素材库" → 走本模式）

1. 读 `素材/` 全部 `.md`，按文件名日期升序排列。为空 → 提示先"全量记一下"或"全量梳理"。
2. 主线程直接合成（只读本地文件，无需派 agent）：按 `[项目名]` 归组，组内按日期排序，写 `$ALLLOG_DATA_ROOT/简历素材库.md`（覆盖重生成，不动 `素材/`）。
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

4. 生成后回执：项目数、素材条数、文件路径。
5. 提示可衔接 `job-tailored-resume` skill：用素材库直接定制简历（含 STAR 改写、岗位关键词对齐）。
