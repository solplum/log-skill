# worklog + alllog

Two complementary [Claude Code](https://claude.ai) / [Codex](https://github.com/openai/codex) agent skills. They read your local coding-agent session history and turn it into files you can actually use: a weekly **demand-narrative report** (`worklog`), and a growing **resume-material library** (`alllog`).

They are instruction skills (`SKILL.md` + fixtures). There is no server to run. After you copy a skill folder into your agent’s skills directory, the agent follows the file when you invoke it.

| Skill | Job | Trigger style | Storage grain |
| --- | --- | --- | --- |
| **worklog** | What did I do this week, written for a manager? | Auto-route from everyday phrases, or `/worklog` | One week, named by **Monday** |
| **alllog** | What is worth putting on a résumé, grouped by project? | **Manual `/alllog` only** | All time, named by **record day** |

They never share files. worklog writes under your workspace `报告文档/需求/`. alllog writes under a **user-configurable** data root (`ALLLOG_DATA_ROOT`, default `~/alllog`).

[中文说明](#worklog--alllog中文)

---

## Table of contents

- [What each skill is](#what-each-skill-is)
- [How they differ](#how-they-differ)
- [Install](#install)
- [Slash commands and trigger phrases](#slash-commands-and-trigger-phrases)
- [Modes](#modes)
- [Confirmation gates](#confirmation-gates)
- [Storage layout](#storage-layout)
- [Session sources and timezone](#session-sources-and-timezone)
- [Limits](#limits)
- [Repository layout](#repository-layout)
- [Tests](#tests)

---

## What each skill is

### worklog — weekly demand-narrative report

worklog answers “what did I ship this week?” It can:

1. **Quick-capture** a one-liner you dictate (`记录一下：…`).
2. **Mine** recent Claude Code / Codex / ZCode sessions and propose numbered candidates. Nothing is written until you pick rows.
3. **Render** an append-only weekly log into a “demand narrative” report: background → design → what landed → result. Optional Word export if a `docx` skill is installed. Standup wording (`站会` / `晨会`) appends Scrum’s three questions.

Logs are **append-only**. Regenerating a report writes under `周报/` and never rewrites `日志/`.

### alllog — résumé material, full history

alllog answers “what from my agent history belongs on a résumé?” It can:

1. **Quick-capture** a project one-liner (`全量记一下：…` / `记简历：…`).
2. **Mine** the same three session sources, cluster by project directory when the set is large, and wait for you to pick both projects and individual bullets.
3. **Roll up** every `素材/*.md` file into `简历素材库.md` (overwrite the rollup only; never touch `素材/`).

**alllog never starts from casual chat.** The words “素材库” or “记简历” in a normal conversation must not auto-invoke it. You have to type `/alllog` (or name the skill explicitly).

---

## How they differ

| | worklog | alllog |
| --- | --- | --- |
| Audience | Manager / standup / weekly review | Future you writing a résumé |
| Who may start it | Everyday phrases or `/worklog` | Only `/alllog` / an explicit name |
| Time grain | This week (Monday-based file name) | All time (today’s date on each capture file) |
| Dedup | Same `[需求名]` tag in **this week’s** log is skipped | Same project **and** same point across **all** `素材/` files is skipped; extra points for the same project are kept |
| Output shape | One demand per section: 背景 / 方案 / 落地 / 结果 | One project per section: 背景 / 技术栈 / 亮点 / 结果 / 素材记录 |
| Data root | Workspace-relative `报告文档/需求/` | `$ALLLOG_DATA_ROOT` (default `~/alllog`) |

Use both. worklog is “what I owe this week.” alllog is “what I want to keep for years.”

---

## Install

Clone this repository, then **copy each skill directory** into the skills folder of every agent CLI you use. Do not copy the repo root; copy `worklog/` and `alllog/` so each folder has its own `SKILL.md` at the top.

### Claude Code

```bash
git clone https://github.com/2021291696/worklog-alllog.git
mkdir -p ~/.claude/skills
cp -R worklog-alllog/worklog ~/.claude/skills/worklog
cp -R worklog-alllog/alllog  ~/.claude/skills/alllog
```

Windows PowerShell:

```powershell
git clone https://github.com/2021291696/worklog-alllog.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force worklog-alllog\worklog "$env:USERPROFILE\.claude\skills\worklog"
Copy-Item -Recurse -Force worklog-alllog\alllog  "$env:USERPROFILE\.claude\skills\alllog"
```

### Codex

```bash
git clone https://github.com/2021291696/worklog-alllog.git
mkdir -p ~/.codex/skills
cp -R worklog-alllog/worklog ~/.codex/skills/worklog
cp -R worklog-alllog/alllog  ~/.codex/skills/alllog
```

Windows PowerShell:

```powershell
git clone https://github.com/2021291696/worklog-alllog.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force worklog-alllog\worklog "$env:USERPROFILE\.codex\skills\worklog"
Copy-Item -Recurse -Force worklog-alllog\alllog  "$env:USERPROFILE\.codex\skills\alllog"
```

Restart the CLI after copying so it reloads skills.

Optional: set alllog’s data root before the first run (any absolute path you own):

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
```

```powershell
$env:ALLLOG_DATA_ROOT = "$env:USERPROFILE\Documents\resume-materials"
```

If you skip this, alllog uses `~/alllog` (`%USERPROFILE%\alllog` on Windows).

---

## Slash commands and trigger phrases

### worklog

| You type | Mode |
| --- | --- |
| `/worklog` with no extra words | Gate ① — agent asks: quick note / mine recent work / weekly report? |
| `记录一下：…` / `记一下：…` | Mode B — quick capture |
| `梳理一下最近做了什么` / `梳理一下` | Mode A — mine sessions |
| `周报` / `汇报` / `产出` / `站会` / `晨会` | Report (standup adds Scrum’s three questions) |

### alllog

| You type | Mode |
| --- | --- |
| `/alllog` with no extra words | Gate ① — agent asks: one line / mine material / build the library? |
| `全量记一下：…` / `记简历：…` | Mode B — quick capture |
| `全量梳理` / `挖简历素材` | Mode A — mine sessions |
| `素材库` / `汇总简历素材` / `出简历素材库` | Rollup (only after `/alllog` is already running) |

Phrases in the alllog table are **arguments to `/alllog`**, not global auto-triggers.

---

## Modes

### worklog Mode B — quick capture

1. Compute this week’s Monday (`date +%u`, Monday = 1).
2. Open or create `报告文档/需求/日志/<Monday>.md`.
3. Append under today’s `## MM-DD`:

```markdown
## 08-12
- [记住我] 设计了登录勾选逻辑 + 30 天 token 续期
```

Never overwrite an older bullet.

### worklog Mode A — mine recent work

1. **Gate ②:** this Monday–now / last 7 days / custom range. Ask, then stop.
2. Scan Claude Code + Codex + ZCode (skip a source that is missing).
3. Show a **numbered** candidate list. Do not write yet.
4. **Gate ③:** “which rows?” Ask, then stop.
5. Append only the rows you named. Reply with what was written and what was left out.

### worklog report

1. Read this week’s log.
2. **Gate ②** for the scan window (same three choices). The start date becomes the report file name.
3. Optionally spawn three light agents (see `worklog/references/agent-team-contract.md`) for the three sources.
4. Draft the demand-narrative report. **Gate ③:** show the numbered demand list, ask which to keep, then stop.
5. Write `报告文档/需求/周报/md形式/<start>.md` and delete the three draft files.
6. Offer Word export to `报告文档/需求/周报/word形式/<start>.docx` if a docx skill exists.

Template:

```markdown
# 产出汇报（<start> ~ <end>）

## 需求：<name>
- **需求背景**：…
- **方案**：…
- **落地**：…
- **结果**：…   # missing → 待补充, never invent a number
```

### alllog Mode B — quick capture

1. `$TODAY=$(date +%F)`.
2. Open or create `$ALLLOG_DATA_ROOT/素材/$TODAY.md`.
3. Append `- [项目名] …` under `## MM-DD`.

### alllog Mode A — mine résumé material

1. **Gate ②:** all sessions / last 30 days / custom. Ask, then stop.
2. Scan the three sources.
3. **Gate ③:** if more than 50 sessions or you chose “all”, cluster by `directory` first and ask which projects. Ask, then stop. Do not default to “all projects.”
4. Rank bullets for a résumé: measurable result > hard technical win > architecture call > routine fix.
5. **Gate ④:** numbered list, “which rows?” Ask, then stop.
6. Append only the rows you named.

### alllog rollup

Read every `素材/*.md`, group by `[项目名]`, overwrite `$ALLLOG_DATA_ROOT/简历素材库.md`. If `素材/` is empty, tell you to capture or mine first.

```markdown
# 简历素材库（生成于 <YYYY-MM-DD HH:MM>，共 <N> 项目 <M> 条）

## 项目：<name>
- **背景**：…
- **技术栈**：…
- **亮点/难点**：…
- **结果/量化**：…   # missing → 待补充
- **素材记录**：
  - <MM-DD original lines>
```

---

## Confirmation gates

Highest priority in both skills. After the agent shows options or candidates it must **ask then stop**. It must not scan, mine, write, or spawn helpers until you answer in a later turn.

| | worklog | alllog |
| --- | --- | --- |
| ① Mode | Bare `/worklog` | Bare `/alllog` |
| ② Date range | Mode A step 1; report step 3 | Mode A step 1 |
| ③ Pick work | Mode A candidates; report demand list | Project cluster when the set is large |
| ④ | — | Individual résumé bullets |

Rules that are easy to violate and are therefore written in the skills:

- **No self-answer.** Asking “last 30 days or all?” and then choosing “last 30 days” in the same reply is a bug.
- Vague replies (`都行`, `好`, `随便`, “sure”, “whatever”) are **not** a choice. Ask again.
- **No confirmation = 0 rows written.** There is no implicit “select all.”

---

## Storage layout

### worklog (workspace-relative)

```
报告文档/需求/
├── 日志/<Monday>.md
└── 周报/
    ├── md形式/<start>.md
    └── word形式/<start>.docx
```

Monday is computed as:

```bash
DOW=$(date +%u)   # 1 = Monday
MONDAY=$(date -d "$(date +%F) -$((DOW-1)) days" +%F)
```

Any call during the week hits the same log file.

### alllog (user-configurable)

```
$ALLLOG_DATA_ROOT/          # default ~/alllog
├── 素材/<YYYY-MM-DD>.md
└── 简历素材库.md
```

Resolve the root the same way the shipped helper does:

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
python alllog/scripts/paths.py              # prints the root
python alllog/scripts/paths.py --library
python alllog/scripts/paths.py --material 2026-08-17
```

Put data **outside** the skill folder so a later `git pull` / recopy cannot wipe it.

---

## Session sources and timezone

Both skills read the same three local stores. A missing store is skipped with a note.

| Source | Path | Clock |
| --- | --- | --- |
| Claude Code (CC) | `~/.claude/projects/**/*.jsonl` | `"timestamp"` in the JSONL, **UTC** |
| Codex | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` plus `archived_sessions/` | folder / file name, **local** |
| ZCode | `~/.zcode/cli/db/db.sqlite` (`session` / `message` / `part`) | `session.time_updated`, epoch **milliseconds** |

Timezone (this is what drops Monday-morning work if you skip it):

- Convert each Claude Code UTC timestamp to local (`date -d "<TS>" +%F`) **before** comparing it to “this week” or “since START.”
- Example: `2026-08-12T02:00:00.000Z` is `2026-08-12 10:00` in UTC+8. If you compare the raw `Z` date, 00:00–07:59 local land on the previous calendar day and disappear from the filter.
- Codex names are already local.
- ZCode is absolute milliseconds: `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))`. “All history” in alllog uses `0`.

Open the ZCode database **read-only** (`mode=ro`). The CLI keeps it open; a write handle will fight WAL. The same query lives in each `SKILL.md` and in `*/scripts/zcode_sessions.py` (used by the unit tests).

User messages in those logs sometimes contain tokens or passwords. Candidates and written files must redact or drop them.

---

## Limits

- These are agent instructions, not a hosted app. Quality depends on the model actually stopping at each gate.
- Date math in the skills uses GNU `date -d`. On macOS, use `gdate` or an equivalent.
- worklog’s report agents are specified as haiku-class on Claude Code. Other CLIs should use their cheapest capable sub-agent.
- Word export needs a separate `docx` skill. If it is missing, the agent should say so and stop.
- alllog may mention `job-tailored-resume` as a possible next skill. That skill is **not** in this repository.
- Do not commit real weekly reports, résumé files, or live `jsonl` / SQLite dumps. Fixtures under `*/test/fixtures/` are fake.
- Author machine paths (Windows drive-letter home or workspace folders) do not belong in a published copy. alllog’s root is an env var, not a hardcoded drive.

---

## Repository layout

```
worklog/                     # copy this folder into ~/.claude/skills/ and ~/.codex/skills/
  SKILL.md
  references/agent-team-contract.md
  scripts/zcode_sessions.py
  test/test-worklog.md
  test/fixtures/
alllog/
  SKILL.md
  scripts/paths.py           # ALLLOG_DATA_ROOT resolver
  scripts/zcode_sessions.py
  test/test-alllog.md
  test/fixtures/
tests/                       # pytest/unittest checks for this repo
```

---

## Tests

From the repo root (Python 3.10+ , standard library only):

```bash
python -m unittest discover -s tests -v
```

The suite calls the shipped `paths.py` and `zcode_sessions.py` entry points, and checks that both `SKILL.md` files still name the modes, gates, three sources, and output templates.

Manual agent walkthroughs (fixtures only, no live sessions) are in `worklog/test/test-worklog.md` and `alllog/test/test-alllog.md`.

---

## License

MIT. See [LICENSE](./LICENSE).

---

# worklog + alllog（中文）

两个互补的 Claude Code / Codex 技能：从本机编程助手会话里，整理出**给别人看的周报**（worklog）和**给简历用的项目素材**（alllog）。

它们是 `SKILL.md` 指令技能，没有后台服务。把技能目录拷进 agent 的 skills 文件夹后，用对应斜杠命令即可。

| 技能 | 干什么 | 怎么触发 | 时间粒度 |
| --- | --- | --- | --- |
| **worklog** | 本周做了什么，写成需求叙事周报 | 日常口令或 `/worklog` | 按**本周一**归档 |
| **alllog** | 哪些内容值得写进简历，按项目归组 | **只能手动 `/alllog`** | 按**记录当天**追加，全量积累 |

两者文件互不干扰。worklog 写在当前工作区的 `报告文档/需求/`；alllog 写在你自己配置的数据根（环境变量 `ALLLOG_DATA_ROOT`，默认 `~/alllog`）。

---

## 各自是什么

**worklog** 回答「这周交差写什么」。三种用法：你口述一句就记（随手记）；扫描 CC / Codex / ZCode 会话，列出编号候选，你点名才写入（主动梳理）；把本周日志收成「需求背景 / 方案 / 落地 / 结果」周报，需要的话再导出 Word。日志只追加；重跑周报只动 `周报/`，不动 `日志/`。

**alllog** 回答「哪些能写进简历」。三种用法：口述一条项目素材；挖历史会话（量大先按目录聚项目）；把 `素材/` 汇总成 `简历素材库.md`。对话里出现「素材库」「记简历」**不得**自动启动本技能，必须先打 `/alllog`。

---

## 两者差别

| | worklog | alllog |
| --- | --- | --- |
| 读者 | 老板 / 站会 / 周报 | 以后写简历的自己 |
| 谁能启动 | 口令或 `/worklog` | 只有 `/alllog` 或点名 |
| 时间 | 本周，文件名是周一 | 全量，文件名是今天 |
| 去重 | 本周日志里相同 `[需求名]` 跳过 | 整个 `素材/` 里「同项目且同要点」才跳过，同项目不同要点保留 |
| 成稿 | 每个需求四段：背景 / 方案 / 落地 / 结果 | 每个项目五段：背景 / 技术栈 / 亮点 / 结果 / 素材记录 |
| 落盘位置 | 工作区相对路径 `报告文档/需求/` | `$ALLLOG_DATA_ROOT`（默认 `~/alllog`） |

---

## 安装

先 clone，再把 **技能目录本身** 拷进各 CLI 的 skills 目录（目录顶层要有 `SKILL.md`）。

### Claude Code

```bash
git clone https://github.com/2021291696/worklog-alllog.git
mkdir -p ~/.claude/skills
cp -R worklog-alllog/worklog ~/.claude/skills/worklog
cp -R worklog-alllog/alllog  ~/.claude/skills/alllog
```

Windows PowerShell：

```powershell
git clone https://github.com/2021291696/worklog-alllog.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force worklog-alllog\worklog "$env:USERPROFILE\.claude\skills\worklog"
Copy-Item -Recurse -Force worklog-alllog\alllog  "$env:USERPROFILE\.claude\skills\alllog"
```

### Codex

```bash
git clone https://github.com/2021291696/worklog-alllog.git
mkdir -p ~/.codex/skills
cp -R worklog-alllog/worklog ~/.codex/skills/worklog
cp -R worklog-alllog/alllog  ~/.codex/skills/alllog
```

Windows PowerShell：

```powershell
git clone https://github.com/2021291696/worklog-alllog.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force worklog-alllog\worklog "$env:USERPROFILE\.codex\skills\worklog"
Copy-Item -Recurse -Force worklog-alllog\alllog  "$env:USERPROFILE\.codex\skills\alllog"
```

拷完后重启 CLI，让它重新加载 skill。

可选：第一次用 alllog 前指定数据根（任意你自己的绝对路径）：

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
```

```powershell
$env:ALLLOG_DATA_ROOT = "$env:USERPROFILE\Documents\resume-materials"
```

不设则使用 `~/alllog`（Windows 上是 `%USERPROFILE%\alllog`）。

---

## 斜杠命令与触发词

### worklog

| 你输入 | 进入 |
| --- | --- |
| 裸 `/worklog` | 闸口①：随手记 / 梳理 / 出周报？ |
| `记录一下：…` / `记一下：…` | 模式 B 随手记 |
| `梳理一下最近做了什么` / `梳理一下` | 模式 A 主动梳理 |
| `周报` / `汇报` / `产出` / `站会` / `晨会` | 汇报（站会/晨会会加 Scrum 三问） |

### alllog

| 你输入 | 进入 |
| --- | --- |
| 裸 `/alllog` | 闸口①：记一条 / 挖素材 / 出素材库？ |
| `全量记一下：…` / `记简历：…` | 模式 B 随手记 |
| `全量梳理` / `挖简历素材` | 模式 A 挖素材 |
| `素材库` / `汇总简历素材` / `出简历素材库` | 汇总（必须已经在 `/alllog` 流程里） |

alllog 表里的中文口令是 **`/alllog` 的参数**，不是全局自动触发词。

---

## 三种模式（细则）

**worklog 随手记**：算本周一 → 打开 `报告文档/需求/日志/<周一>.md` → 在当天 `## MM-DD` 下追加 `- [需求] 一句话`。只追加。

**worklog 主动梳理**：闸口②选范围（本周一至今 / 近七天 / 自定义）后**停轮** → 扫三源 → 给出编号候选（不落盘）→ 闸口③问「记哪几条」后**停轮** → 只写你点名的条目。

**worklog 汇报**：读本周日志 → 闸口②选扫描起点（文件名用这个起点）→ 可按 `references/agent-team-contract.md` 派三个轻量 agent → 按需求叙事模板起草 → 闸口③展示编号清单，问「全部写入还是删哪几条」后**停轮** → 写入 `周报/md形式/<起点>.md` 并删掉三份草稿 → 再问要不要 Word。

**alllog 随手记**：`$TODAY` → `$ALLLOG_DATA_ROOT/素材/$TODAY.md` → 追加 `- [项目名] 一句话`。

**alllog 挖素材**：闸口②选范围（全部 / 近 30 天 / 自定义）后停轮 → 扫三源 → 会话 > 50 或选了「全部」时先按 `directory` 聚项目，闸口③问挖哪些，禁止自行全选 → 按简历优先级提炼编号候选 → 闸口④问记哪几条 → 只写点名条目。

**alllog 汇总**：读全部 `素材/*.md`，按项目归组，覆盖写 `简历素材库.md`，绝不改 `素材/`。目录为空则提示先记或先挖。

---

## 闸口铁律

展示选项或候选后必须 **ask then stop（先问再停轮）**。用户还没在下一轮明确回答之前，禁止扫描、深读、落盘、派 agent。

- **禁止自问自答（no self-answer）**：同一回合里提出「近 30 天还是全部？」然后自己答「近 30 天」并继续跑，算违规。
- 「都行 / 好 / 随便」不是选择，必须再问。
- **无确认 = 0 条写入**，绝不默认全选。

worklog 三道闸口：①模式 ②日期 ③条目/周报清单。alllog 四道：①模式 ②日期 ③项目（量大时）④条目。

---

## 存储

worklog（相对当前工作区）：

```
报告文档/需求/
├── 日志/<周一日期>.md
└── 周报/
    ├── md形式/<起点日期>.md
    └── word形式/<起点日期>.docx
```

alllog（用户可配置）：

```
$ALLLOG_DATA_ROOT/          # 默认 ~/alllog
├── 素材/<YYYY-MM-DD>.md
└── 简历素材库.md
```

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
python alllog/scripts/paths.py
```

数据不要放在 skill 目录里，避免以后覆盖安装时丢掉素材。

---

## 三个会话源与时区

| 源 | 路径 | 时间 |
| --- | --- | --- |
| Claude Code（CC） | `~/.claude/projects/**/*.jsonl` | JSONL 里的 `"timestamp"`，**UTC** |
| Codex | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` 以及 `archived_sessions/` | 目录/文件名，**本地时间** |
| ZCode | `~/.zcode/cli/db/db.sqlite`（`session` / `message` / `part`） | `session.time_updated`，epoch **毫秒** |

缺哪个源就跳过并提示。CC 的 UTC 必须先转本地再和「本周 / 起点」比较，否则时区东八区周一 00:00–07:59 的记录会算成上周而被漏掉。ZCode 库必须只读打开（`mode=ro`）。查询原文在各 `SKILL.md`，可执行副本在 `*/scripts/zcode_sessions.py`。

会话里出现过的密钥 / token / 密码，候选和落盘都要脱敏或省略。

---

## 限制

- 这是给模型看的说明书，不是托管服务；闸口能不能停住取决于模型是否遵守。
- 技能里的日期命令按 GNU `date -d` 写；macOS 请用 `gdate` 或等价写法。
- 周报子代理在 Claude Code 里指定用 haiku 量级；其他 CLI 用它自己最便宜且能用的子代理。
- 导出 Word 需要另外的 `docx` skill，没有就停下来告诉你。
- alllog 文末可能提到 `job-tailored-resume`，那个技能不在本仓库。
- 不要把真实周报、简历或线上会话 `jsonl` / SQLite 提交进 git。`*/test/fixtures/` 里是假数据。
- 发布副本里不能出现作者本机盘符路径。alllog 的根目录用环境变量，不用写死某台机器上的绝对路径。

---

## 许可

MIT，见 [LICENSE](./LICENSE)。
