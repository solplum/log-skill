# worklog + alllog + change-report + changelog

🌐 **English** ｜ **[中文说明（直达中文版 README）](#worklog--alllog--change-report--changelog中文)**

Four complementary agent skills for [Claude Code](https://claude.ai) / [Codex](https://github.com/openai/codex) / ZCode-style CLIs. Two of them read your local coding-agent session history (`worklog`, `alllog`). One reads **git history only** (`change-report`). The fourth (`changelog`) turns what actually changed — proven by files, diffs, commits, tests, or cloud records — into a numbered handoff table a mentor can read without reading your conversation.

They are instruction skills (`SKILL.md` + references + fixtures). There is no server to run. Copy a skill folder into your agent's skills directory and the agent follows the file when you invoke it.

| Skill | Job | Trigger style | Storage grain |
| --- | --- | --- | --- |
| **worklog** (`lzl-worklog`) | What did I do this week, written for a manager? | Auto-route from everyday phrases, or `/lzl-worklog` / `/worklog` | One week, named by **Monday** |
| **alllog** (`lzl-alllog`) | What is worth putting on a résumé, grouped by project? | **Manual `/lzl-alllog` / `/alllog` only** | All time, named by **record day** |
| **change-report** | What did this git range change, written for a manager? | Everyday phrases or `/change-report` | One git range, named by the **oldest commit date** |
| **changelog** (`lzl-changelog`) | What actually changed, as a numbered mentor handoff table? | `/lzl-changelog` / `/changelog` or everyday phrases | **Nothing on disk by default** (optional image export) |

They never share files. worklog writes under your workspace `报告文档/需求/` (or global `~/worklog`). change-report writes under workspace `报告文档/代码/<project>/`. alllog writes under a **user-configurable** data root (`LZL_ALLLOG_DATA_ROOT` / `ALLLOG_DATA_ROOT`, default `~/alllog`, with first-use interactive onboarding). changelog prints to the conversation and only writes anything (a PNG) if you ask for the export.

**Prefer pictures over prose?** Each skill has a dedicated ELI5 explainer page, in both Chinese and English — the links below go to the rendered pages served by **GitHub Pages**. (The `eli5/*.html` files in the repo are the same sources; GitHub's file view shows HTML as code, not as a page.)

| Explainer | Skill | What it covers |
| --- | --- | --- |
| [中文](https://solplum.github.io/log-skill/eli5/worklog.html) · [English](https://solplum.github.io/log-skill/eli5/worklog.en.html) | worklog | four-source mining → numbered candidates → gate confirmation → demand-narrative weekly report |
| [中文](https://solplum.github.io/log-skill/eli5/alllog.html) · [English](https://solplum.github.io/log-skill/eli5/alllog.en.html) | alllog | full-history résumé mining, coverage receipt, journal/digest layout |
| [中文](https://solplum.github.io/log-skill/eli5/change-report.html) · [English](https://solplum.github.io/log-skill/eli5/change-report.en.html) | change-report | pick a range → formal memo, read-only git, honest status labels |
| [中文](https://solplum.github.io/log-skill/eli5/changelog.html) · [English](https://solplum.github.io/log-skill/eli5/changelog.en.html) | changelog | 本次 vs 本功能 scope, final-state vs per-iteration, readability gate, three-value delivery status |

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
- [License](#license)
- [中文说明（Chinese README）](#worklog--alllog--change-report--changelog中文)

---

## What each skill is

### worklog — weekly demand-narrative report (lzl-worklog)

worklog (packaged as `lzl-worklog`) answers "what did I ship this week?" It can:

1. **First-time onboarding:** prompt for storage directory selection (recommended `~/worklog` global store vs workspace `./报告文档/需求/`) and persist it.
2. **Quick-capture** a one-liner you dictate (`记录一下：…`).
3. **Full scan / Mine:** choose full scan to mine all historical sessions directly without re-prompting for date ranges, or mine recent Claude Code / Codex / ZCode / MiniMax Code sessions and propose numbered candidates. Nothing is written until you pick rows.
4. **Render** an append-only weekly log into a "demand narrative" report: background → design → what landed → result. Optional Word export if a `docx` skill is installed. Standup wording (`站会` / `晨会`) appends Scrum's three questions.

A **scan checkpoint** (`.last-scan`, one date line) lets the next mine start "from last scan" instead of re-asking you for a window. Logs are **append-only**; regenerating a report writes under `周报/` and never rewrites `日志/`.

The report step can spawn up to four light agents — one per source (Agent-CC / Agent-Codex / Agent-Zcode / Agent-Minimax, see `lzl-worklog/references/agent-team-contract.md`). A skipped source spawns no agent and produces no empty draft.

### alllog (`lzl-alllog`) — résumé material, full history

alllog (in this repository `lzl-alllog`) answers "what from my agent history belongs on a résumé?" It features:

- **Storage onboarding (Gate ⓪):** Prompts on first use if not configured, suggesting global `~/alllog` (recommended) or workspace `./素材/`, saved to `~/.config/lzl-alllog/config.json`.
- **Full-scan mode:** One-click full scan that bypasses date range questions and starts from the beginning of history.
- **Five-source mining:** Scans CC, Codex, ZCode, MiniMax Code, and **Antigravity** (both IDE and CLI), with a five-source **coverage receipt** attached to candidates.
- **External reader & STAR résumé standards:** Eliminates private internal codenames (like Mimosa) and AI debugging artifacts (like sub-agent audits), framing work as clear STAR achievements (background / technical highlight / measurable result).
- **Quick-capture (Mode B):** `全量记一下：…` / `记简历：…`.
- **Roll up:** Aggregates `素材/日志/` into a structured per-project digest snapshot (`素材/整理/<today>.md`).

**alllog never starts from casual chat.** The words "素材库" or "记简历" in a normal conversation must not auto-invoke it. You have to type `/lzl-alllog` or `/alllog` (or name the skill explicitly).

### change-report — manager-facing git change memo

change-report answers "what did this git range change, in language a manager can read?" It is **read-only on git** (`status` / `log` / `diff`). It never commits, pushes, or resets.

1. **Pick a range** (uncommitted / unpushed / pushed-but-unmerged, or `--record` / `--range` / `--commit`). Ask, then stop. Do not default to "last N commits" without saying so.
2. Optionally read `docs/change-log.md` for background.
3. Draft a short formal report: one-line goal, background, themed change bullets (file/place + what changed + why it matters), file list, verification.
4. Show the draft. Ask, then stop. Do not write until you confirm, especially the "why."
5. Append one line to `变更记录.md`, write the markdown report, and ask a `docx` skill to render Word.

Status labels are honest: `draft` (dirty tree), `local-commit`, `pushed`, or `unknown`. The skill will not invent a git state to make a workflow look complete.

It is also **composable and resumable** — the V3 execution model, which outranks any conflicting rule in the skill: you may invoke it before a commit, before a push, after a push, or retroactively to backfill a record; there is no required order. Re-invoking the same range shows or updates the markdown draft and re-renders it; the md source stays in `md形式/`. An optional local state index may record `reported` and the output paths, but neither the index nor the report content is ever auto-committed or auto-pushed.

### changelog — mentor handoff table

changelog answers "what actually changed — and can a mentor who skipped this conversation understand each row?" It reads the **conversation plus the smallest relevant evidence set** (files, git, commits, PRs, tests, CI, cloud records, runtime logs — routed by intent, see `changelog/references/evidence-routing.md`).

1. **Scope gate, every invocation:** 本次 (this conversation's actual changes) or 本功能 (the whole lifecycle of the named effort). Never inferred silently.
2. **Granularity gate** when the scope contains superseded iterations: final-state-only rows, or one row per iteration.
3. Build a **numbered main table** — 改动事项 / 原背景 / 本次实际改动 / 交付状态 / 验证结果 — then a per-item file mapping section with the same numbers.
4. **Readability gate (hard):** every row must be retellable in one plain sentence by someone who did not read the conversation ("以前…；现在…" style, jargon glossed). Rewritten before delivery, never skipped.
5. **Delivery status has exactly three values:** 未上传 (local only) → 已上传 (pushed) → 已部署 (live). Validation must name its environment (本地 / CI / 云端 / 线上) — a local E2E pass never backs an online deployment. When deployment depends on a third party rebuilding, the row stays 已上传 and the report appends one 部署说明 line naming who must pull which branch and rebuild before it goes live.
6. After delivering, end with one closing question: remove any items (by number) and/or export the table as a PNG.

Proof rule: a plan, a suggestion, or a discussion-only decision is never an item. If nothing provable changed, the skill prints exactly `本次未发现已经落实的改动，不生成变更表格。` and emits no empty table.

---

## How they differ

| | worklog | alllog | change-report | changelog |
| --- | --- | --- | --- | --- |
| Audience | Manager / standup / weekly review | Future you writing a résumé | Manager / "what shipped in this diff" | Mentor receiving a handoff |
| Input | Agent session logs + your notes | Agent session logs + your notes | **Git only** (`status` / `log` / `diff`) | Conversation + smallest relevant evidence (git / PR / tests / CI / cloud) |
| Who may start it | Everyday phrases or `/worklog` | Only `/alllog` / an explicit name | Everyday phrases or `/change-report` | `/changelog` or everyday phrases |
| Time grain | This week (Monday-based file name) | All time (today's date on each journal file) | One git range (oldest commit date) | This conversation or the effort's full lifecycle (本次 / 本功能) — asked, never guessed |
| Dedup | Same `[需求名]` tag in **this week's** log is skipped | Same project **and** same point across **all** journal files is skipped | Same theme in that project's `变更记录.md` is skipped | Evidence decides: no record, no row |
| Output shape | One demand: 背景 / 方案 / 落地 / 结果 | One project: 背景 / 技术栈 / 亮点 / 结果 / 素材记录 | One memo: 一句话目标 / 背景 / 本次改动 / 改动文件 / 验证结果 | Numbered table: 改动事项 / 原背景 / 本次实际改动 / 交付状态 / 验证结果 + file sections |
| Persistence | Workspace `报告文档/需求/` | `$ALLLOG_DATA_ROOT` (default `~/alllog`) | Workspace `报告文档/代码/<project>/` | Conversation only; optional PNG export |

Use all four. worklog is "what I owe this week." change-report is "what this git range did." changelog is "what actually changed, in mentor-readable rows." alllog is "what I want on a résumé."

---

## Install

Clone this repository, then **copy each skill directory** into the skills folder of every agent CLI you use. Do not copy the repo root; copy `lzl-worklog/` (or `worklog/`), `lzl-alllog/` (or `alllog/`), `change-report/`, and `changelog/` so each folder has its own `SKILL.md` at the top.

### Claude Code

```bash
git clone https://github.com/solplum/log-skill.git
mkdir -p ~/.claude/skills
cp -R log-skill/lzl-worklog    ~/.claude/skills/lzl-worklog
cp -R log-skill/lzl-alllog     ~/.claude/skills/lzl-alllog
cp -R log-skill/change-report  ~/.claude/skills/change-report
cp -R log-skill/changelog      ~/.claude/skills/changelog
# Optional backwards compatibility symlinks:
ln -s ~/.claude/skills/lzl-worklog ~/.claude/skills/worklog
ln -s ~/.claude/skills/lzl-alllog  ~/.claude/skills/alllog
```

Windows PowerShell:

```powershell
git clone https://github.com/solplum/log-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force log-skill\lzl-worklog "$env:USERPROFILE\.claude\skills\lzl-worklog"
Copy-Item -Recurse -Force log-skill\lzl-alllog  "$env:USERPROFILE\.claude\skills\lzl-alllog"
Copy-Item -Recurse -Force log-skill\change-report "$env:USERPROFILE\.claude\skills\change-report"
Copy-Item -Recurse -Force log-skill\changelog     "$env:USERPROFILE\.claude\skills\changelog"
```

### Codex

```bash
git clone https://github.com/solplum/log-skill.git
mkdir -p ~/.codex/skills
cp -R log-skill/lzl-worklog    ~/.codex/skills/lzl-worklog
cp -R log-skill/lzl-alllog     ~/.codex/skills/lzl-alllog
cp -R log-skill/change-report  ~/.codex/skills/change-report
cp -R log-skill/changelog      ~/.codex/skills/changelog
# Optional backwards compatibility symlinks:
ln -s ~/.codex/skills/lzl-worklog ~/.codex/skills/worklog
ln -s ~/.codex/skills/lzl-alllog  ~/.codex/skills/alllog
```

Windows PowerShell:

```powershell
git clone https://github.com/solplum/log-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force log-skill\lzl-worklog "$env:USERPROFILE\.codex\skills\lzl-worklog"
Copy-Item -Recurse -Force log-skill\lzl-alllog  "$env:USERPROFILE\.codex\skills\lzl-alllog"
Copy-Item -Recurse -Force log-skill\change-report "$env:USERPROFILE\.codex\skills\change-report"
Copy-Item -Recurse -Force log-skill\changelog     "$env:USERPROFILE\.codex\skills\changelog"
```

Restart the CLI after copying so it reloads skills.

Optional: set alllog's data root before the first run (any absolute path you own):

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
```

```powershell
$env:ALLLOG_DATA_ROOT = "$env:USERPROFILE\Documents\resume-materials"
```

If you skip this, alllog uses `~/alllog` (`%USERPROFILE%\alllog` on Windows).

---

## Slash commands and trigger phrases

### worklog (lzl-worklog)

| You type | Mode |
| --- | --- |
| First run | Gate ⓪ — pick storage location (`~/worklog` recommended vs `./报告文档/需求/`) |
| `/lzl-worklog` or `/worklog` with no extra words | Gate ① — agent asks: full scan / mine recent work / quick note / weekly report? |
| `全量扫描` / `全量梳理` / `建初始底账` | Mode A — full scan all history (skips Gate ② directly) |
| `记录一下：…` / `记一下：…` | Mode B — quick capture |
| `梳理一下最近做了什么` / `梳理一下` | Mode A — mine sessions |
| `周报` / `汇报` / `产出` / `站会` / `晨会` | Report (standup adds Scrum's three questions) |

### alllog

| You type | Mode |
| --- | --- |
| `/alllog` with no extra words | Gate ① — agent asks: one line / mine material / roll up the library? |
| `全量记一下：…` / `记简历：…` | Mode B — quick capture |
| `全量梳理` / `挖简历素材` | Mode A — mine sessions |
| `接着上次挖` / `从上次停的地方继续` | Mode A with "resume from last stop point" pre-selected |
| `素材库` / `汇总简历素材` / `出简历素材库` | Rollup (only after `/alllog` is already running) |

Phrases in the alllog table are **arguments to `/alllog`**, not global auto-triggers.

### change-report

| You type | Mode |
| --- | --- |
| `/change-report` with no extra words | Gate ① — pick a git range (uncommitted / unpushed / pushed-unmerged, or a SHA / range / record id) |
| `提交报告` / `改动报告` / `给上级的报告` / `这次改了什么` / `change report` | Same skill; still stops at the range gate unless you already named a range |
| `本周工作总结` | Same skill if you mean a **git** memo. If you mean a weekly narrative from sessions, use `/worklog` instead |

You can also pass `--record <ID>`, `--range <base>..<head>`, or `--commit <SHA>` so the agent skips the range picker.

### changelog

| You type | What happens |
| --- | --- |
| `/changelog` | Scope gate first: 本次 or 本功能? Then granularity if iterations were superseded |
| `记录本次改动` / `比较本地与云端` / `有哪些还没提交` / `有哪些还没推送` | Same skill; the scope gate still applies unless your wording already pins the scope (e.g. a cloud comparison) |
| `这个 PR 改了什么` / `今天改了什么` | Routed to the named evidence set; conversation scope still asked when ambiguous |
| `发现页改造这个事做得怎么样` | 本功能全周期: effort lifecycle from its anchored origin to now |

`changelog` (this skill) is a **report**, not a `CHANGELOG.md` writer: it never creates or edits that file, never commits, pushes, merges, resets, or deploys.

---

## Modes

### worklog Mode B — quick capture

1. Compute this week's Monday (`date +%u`, Monday = 1).
2. Open or create `报告文档/需求/日志/<Monday>.md`.
3. Append under today's `## MM-DD`:

```markdown
## 08-12
- [记住我] 设计了登录勾选逻辑 + 30 天 token 续期
```

Never overwrite an older bullet.

### worklog Mode A — mine recent work

1. **Gate ②:** this Monday–now (default; if this week's log already exists, the start resumes from its last `## MM-DD` section so recorded items are skipped) / last 7 days / **from last scan** (reads the `.last-scan` checkpoint; if absent, says so and re-offers the other options) / custom range. Ask, then stop.
2. Scan all four sources (skip a missing one with a note). After scanning, write today's date into `报告文档/需求/.last-scan`.
3. Show a **numbered** candidate list. Do not write yet. Redact any tokens or passwords found in user messages.
4. **Gate ③:** "which rows?" Ask, then stop.
5. Append only the rows you named. Reply with what was written and what was left out.

### worklog report

1. Read this week's log.
2. **Gate ②** for the scan window (same four choices; the start date becomes the report file name). After mining the four sources, update the `.last-scan` checkpoint.
3. Spawn up to four light agents in parallel — one per available source (see `worklog/references/agent-team-contract.md`). A skipped source spawns no agent and produces no empty draft.
4. Draft the demand-narrative report. **Gate ③:** show the numbered demand list, ask which to keep, then stop.
5. Write `报告文档/需求/周报/md形式/<start>.md` and delete all intermediate drafts (`<start>-cc-draft.md`, `-codex-`, `-zcode-`, `-minimax-`).
6. Offer Word export to `报告文档/需求/周报/word形式/<start>.docx` if a docx skill exists.

Template (humanized 3-stage narrative, ready to speak in meetings):

```markdown
# 产出汇报（<start> ~ <end>）

## 1. <action-driven result title>
- **痛点问题**：…   # previous pain point or friction
- **关键改动**：…   # key actions taken (no low-level config/command clutter)
- **实际效果**：…   # outcome / missing → 待补充, never invent

## 下周重点与协作项
- **下周规划**：…
- **需要协调**：…
```

### alllog Mode B — quick capture

1. `$TODAY=$(date +%F)`.
2. Open or create `$ALLLOG_DATA_ROOT/素材/日志/$TODAY.md`.
3. Append `- [项目名] …` under `## MM-DD`.

### alllog Mode A — mine résumé material

1. **Gate ②:** all sessions / **resume from last stop point** (newest journal file name + 1 day; empty journal falls back to "all") / last 30 days / custom. (If you choose **Full scan** in Gate ①, Gate ② is automatically skipped and scanning starts immediately from the beginning of history).
2. Scan all **five** sources with the exact scripts embedded in `lzl-alllog/SKILL.md` (CC session scan, Codex index-first, ZCode SQLite read-only, MiniMax Code messages.jsonl, and Antigravity dual-end IDE/CLI scan). Keep exclusion counts for the receipt.
3. Extract candidates directly by **business initiatives and facts** (strictly forbidden to cluster by file paths or machine directories) and frame as STAR achievements following the **no-jargon rule** (eliminate private codenames like Mimosa, scrub internal AI debugging traces). Attach the **coverage receipt** (five-source scanned/included/excluded table).
4. **Gate ③:** numbered list, "which rows to record?" Ask, then stop.
5. Append only the rows you named to `素材/日志/`.

### alllog rollup

Read every `素材/日志/*.md` (the journal is the only source of truth), group by `[项目名]`, and write `$ALLLOG_DATA_ROOT/素材/整理/<today>.md` (today's digest; same-day regeneration overwrites, the journal is never touched). If the journal is empty, tell you to capture or mine first. After writing, report the project count, the entry count and the file path, and note that résumé-making only needs this newest digest.

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

### change-report — git range memo

1. Confirm the cwd is a git work tree. If not, stop.
2. Confirm there is something to report (`git status --short` or commits on the trunk). If not, stop.
3. **Gate ①:** show candidate ranges. Ask, then stop. Trunk is the first of `origin/main` → `main` → `master`. Only if none exist, fall back to the last 5 commits **and say so**.
4. Optionally read `docs/change-log.md`.
5. Draft from `git diff --stat`, selected file diffs, and `git log <trunk>..HEAD`. Missing "why" → `原因待确认`. Missing tests → `未验证`. Never invent either.
6. **Gate ②:** show the draft, ask you to confirm / fill in the reasons. Ask, then stop.
7. Append to `变更记录.md` (append-only). Write `md形式/<range-start>.md`. Ask a `docx` skill for `word形式/<range-start>.docx`. Keep the markdown source; if rendering fails, say so and leave the md for a manual retry. Finish by reporting the .docx path plus a short digest (one-line goal + theme list).

`<range-start>` is `git show -s --format=%cs <oldest-in-range>`. Uncommitted-only ranges use today. If the target file already exists, confirm before overwrite.

Template:

```markdown
# 变更报告 · YYYY-MM-DD
## 一句话目标
本次完成了<什么>，达成了<什么>。

## 背景
<1–2 formal sentences>

## 本次改动
**<theme>**
原因：<problem this theme fixes>
- <file/place + what changed + effect>

## 改动文件
<paths only, grouped by module>

## 验证结果
- <how + result, or 未验证>
```

Rules the skill will not bend:

- Formal written Chinese (or the language you asked for). No "I changed / why I changed" chat voice.
- File/place + change + effect only. **No code, line numbers, or commands** in the report.
- No credentials, tokens, or internal addresses.
- At most 1–3 themes. More than that → ask to merge or cut.
- One page of prose; every line ≤ 25 characters; sub-points ordered by dependency chain (design/DB → backend → frontend).
- The file list comes from `git diff --name-only <trunk>..HEAD`, grouped by module — paths only, one per line.

### changelog — mentor handoff table

1. **Scope gate (every invocation):** 本次 (this conversation's attributable changes) or 本功能 (the effort's whole lifecycle; anchor its start from plan docs / ROADMAP / change-log when possible). Ask, then stop.
2. **Granularity gate (same round):** only if superseded iterations exist — final-state rows vs one row per iteration.
3. Route to the smallest relevant evidence set per `changelog/references/evidence-routing.md` (conversation for scope/reason; files, git, PR, tests, CI, cloud records, runtime logs only where the request makes them relevant). A conversation claim alone never proves a file changed.
4. Produce scope + evidence summary, the numbered main table, and per-item file sections. 全周期 rows compare against the state **before the effort started**.
5. Apply the **readability gate** row by row before delivering.
6. Handle edits on request (`删除 2、4` / `合并 2 和 3` / `把 5 放到最前面`): apply, renumber continuously, update file sections, return the full clean report.
7. Close with one question: ① remove any items by number; ② export the main table as a PNG (title + meta + table only; render via styled HTML → browser screenshot over a temporary local server). Decline both and the run ends.

Cloud comparison (`相比云端有哪些改动`) splits the table into `本地未提交改动` / `本地独有改动` / `云端独有改动` with a `比较概览` count line and a `云端状态` header stating whether fresh remote metadata was actually obtained.

---

## Confirmation gates

Highest priority in all four skills. After the agent shows options or candidates it must **ask then stop**. It must not scan, mine, write, or spawn helpers until you answer in a later turn.

| | worklog | alllog | change-report | changelog |
| --- | --- | --- | --- | --- |
| ① | Bare `/worklog` (which mode?) | Bare `/alllog` (which mode?) | Which git range? | Scope: 本次 or 本功能? (+ granularity when iterations were superseded) |
| ② | Date range | Date range | Confirm the draft (especially "why") | — (evidence routed by intent, not chosen by you) |
| ③ | Which log / report rows? | Which projects (when the set is large)? | — | — |
| ④ | — | Which résumé bullets? | — | — |
| closing | — | — | — | Remove items / export PNG |

Rules that are easy to violate and are therefore written in the skills:

- **No self-answer.** Asking "last 30 days or all?" and then choosing "last 30 days" in the same reply is a bug.
- Vague replies (`都行`, `好`, `随便`, "sure", "whatever") are **not** a choice. Ask again.
- **No confirmation = 0 rows written.** There is no implicit "select all."

---

## Storage layout

### worklog (workspace-relative)

```
报告文档/需求/
├── .last-scan               # scan checkpoint, one YYYY-MM-DD line
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
└── 素材/
    ├── 日志/<YYYY-MM-DD>.md    # append-only journal — the only source of truth
    └── 整理/<YYYY-MM-DD>.md    # per-project digest snapshot, regenerated per day
```

Resolve the root the same way the shipped helper does:

```bash
export LZL_ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
python lzl-alllog/scripts/paths.py                    # prints the root
python lzl-alllog/scripts/paths.py --journal 2026-08-17   # journal file for that day
python lzl-alllog/scripts/paths.py --digest  2026-08-17   # digest file for that day
python lzl-alllog/scripts/paths.py --latest               # newest journal day (resume-from stop point)
```

Put data **outside** the skill folder so a later `git pull` / recopy cannot wipe it.

### change-report (workspace-relative, per git repo)

```
报告文档/代码/
├── _projects.json           # optional { "<git-root-path>": "<folder-name>" }
└── <project>/
    ├── 变更记录.md
    ├── md形式/<range-start>.md
    └── word形式/<range-start>.docx
```

`<project>` is the mapped name in `_projects.json`, or the git root directory name. Same rule as the shipped helper:

```bash
python change-report/scripts/project_name.py /path/to/repo 报告文档/代码/_projects.json
```

### changelog (nothing by default)

changelog writes **nothing** to disk. The table lives in the conversation; the only file it may ever create is the PNG you explicitly request at the closing question, saved where you tell it.

---

## Session sources and timezone

worklog and alllog read the same four local stores. A missing store is skipped with a note. change-report does **not** read these stores; it only reads git. changelog reads them only when the routed evidence calls for it.

| Source | Path | Clock |
| --- | --- | --- |
| Claude Code (CC) | `~/.claude/projects/**/*.jsonl` | `"timestamp"` in the JSONL, **UTC**. alllog dates a whole session by its **last** timestamp (multi-day sessions are not dropped); worklog filters individual records |
| Codex — alllog | `~/.codex/session_index.jsonl` preferred (thread name + `updated_at`), folder scan as fallback | index `updated_at`, **UTC** |
| Codex — worklog | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` + `archived_sessions/` (flat, top level). **Does not read the index** — in real runs its `thread_name` is usually a useless "你好" | file/folder names, **local** |
| ZCode | `~/.zcode/cli/db/db.sqlite` (`session` / `message` / `part`) | `session.time_updated`, epoch **milliseconds** |
| MiniMax Code | `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/messages.jsonl` | last `message.timestamp` in the file, epoch **milliseconds** — never the folder date |
| Antigravity (lzl-worklog) | Desktop (`~/.gemini/antigravity/`) + CLI (`~/.gemini/antigravity-cli/`) `conversation_summaries.db` & `brain/*/transcript.jsonl` | `last_modified_time`, **UTC** (dual-source scan) |

Timezone (this is what drops Monday-morning work if you skip it):

- Convert each Claude Code UTC timestamp to local (`date -d "<TS>" +%F`) **before** comparing it to "this week" or "since START."
- Example: `2026-08-12T02:00:00.000Z` is `2026-08-12 10:00` in UTC+8. If you compare the raw `Z` date, 00:00–07:59 local land on the previous calendar day and disappear from the filter.
- Codex index timestamps are UTC (`astimezone()` before comparing); Codex file names are already local.
- ZCode and MiniMax Code are absolute milliseconds: `$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))`. "All history" uses `0`. For MiniMax Code, filter by the last in-file timestamp, not the folder date — cross-day sessions would be dropped otherwise.

Open the ZCode database **read-only** (`mode=ro`). The CLI keeps it open; a write handle will fight WAL. The same query lives in each `SKILL.md` and in `*/scripts/zcode_sessions.py` (used by the unit tests).

User messages in those logs sometimes contain tokens or passwords. Candidates and written files must redact or drop them.

---

## Limits

- These are agent instructions, not a hosted app. Quality depends on the model actually stopping at each gate.
- Date math in the skills uses GNU `date -d`. On macOS, use `gdate` or an equivalent.
- worklog's report agents are specified as haiku-class on Claude Code. Other CLIs should use their cheapest capable sub-agent.
- Word export needs a separate `docx` skill. If it is missing, the agent should say so and stop. change-report keeps the markdown source either way.
- change-report is read-only on git. It will not commit, push, or reset, and it will not paste code or secrets into the memo.
- changelog never writes `CHANGELOG.md` and never commits, pushes, merges, resets, or deploys. Its PNG export needs a browser screenshot capability; without one it says so.
- `本周工作总结` is ambiguous: git memo → `/change-report`; weekly session narrative → `/worklog`; mentor handoff rows → `/changelog`.
- alllog may mention `job-tailored-resume` as a possible next skill. That skill is **not** in this repository.
- Do not commit real weekly reports, résumé files, change memos, or live `jsonl` / SQLite dumps. Fixtures under `*/test/fixtures/` are fake.
- Author machine paths (Windows drive-letter home or workspace folders) do not belong in a published copy. alllog's root is an env var, not a hardcoded drive; the unit tests scan every published file for leaked machine paths.

---

## Repository layout

```
lzl-worklog/                 # copy this folder into ~/.claude/skills/ and ~/.codex/skills/
  SKILL.md
  references/agent-team-contract.md
  scripts/zcode_sessions.py
  test/test-worklog.md
  test/fixtures/
lzl-alllog/
  SKILL.md
  scripts/paths.py           # LZL_ALLLOG_DATA_ROOT resolver + journal/digest paths
  scripts/zcode_sessions.py
  test/test-alllog.md
  test/fixtures/
change-report/
  SKILL.md
  scripts/project_name.py    # _projects.json → folder name
changelog/
  SKILL.md
  references/evidence-routing.md
  references/output-format.md
  agents/openai.yaml
eli5/                        # one self-contained explainer page per skill (Chinese + English)
  worklog.html
  worklog.en.html
  alllog.html
  alllog.en.html
  change-report.html
  change-report.en.html
  changelog.html
  changelog.en.html
tests/                       # unittest checks for this repo
```

---

## Tests

From the repo root (Python 3.10+, standard library only):

```bash
python -m unittest discover -s tests -v
```

The suite calls the shipped `paths.py`, `zcode_sessions.py`, and `project_name.py` entry points, and checks that each `SKILL.md` still names its modes, gates, sources, and output templates — including changelog's scope/granularity gates and delivery-status vocabulary — and that no published file contains author-machine paths.

Manual agent walkthroughs (fixtures only, no live sessions) are in `lzl-worklog/test/test-worklog.md` and `lzl-alllog/test/test-alllog.md`.

---

## License

MIT. See [LICENSE](./LICENSE).

---

# worklog + alllog + change-report + changelog（中文）

🌐 **[↑ English（回到英文版顶部）](#worklog--alllog--change-report--changelog)** ｜ **中文**

四个互补的 Claude Code / Codex / ZCode 系 agent 技能：从本机会话里整理**给别人看的周报**（worklog）和**给简历用的项目素材**（alllog）；只读 git 的**给上级看的变更备忘**（change-report）；以及把实际改动整理成**带序号 Mentor 交接表**的 changelog。

它们是 `SKILL.md` 指令技能，没有后台服务。把技能目录拷进 agent 的 skills 文件夹后，用对应斜杠命令即可。

| 技能 | 干什么 | 怎么触发 | 时间粒度 |
| --- | --- | --- | --- |
| **worklog** (`lzl-worklog`) | 本周做了什么，写成需求叙事周报 | 日常口令或 `/lzl-worklog` / `/worklog` | 按**本周一**归档 |
| **alllog** (`lzl-alllog`) | 哪些内容值得写进简历，按项目归组 | **只能手动 `/lzl-alllog` / `/alllog`** | 按**记录当天**追加，全量积累 |
| **change-report** | 这段 git 改动改了什么，写成给上级的备忘 | 日常口令或 `/change-report` | 按**范围内最旧 commit 日期**命名 |
| **changelog** (`lzl-changelog`) | 实际发生了什么改动，整理成带序号的交接表 | `/lzl-changelog` / `/changelog` 或日常口令 | **本次对话**或**本功能全周期**（每次必问） |

四者文件互不干扰。worklog 写在 `报告文档/需求/`（或全局 `~/worklog`）；change-report 写在 `报告文档/代码/<项目>/`；alllog 写在你自己配置的数据根（环境变量 `LZL_ALLLOG_DATA_ROOT` / `ALLLOG_DATA_ROOT`，默认 `~/alllog`，首次使用提供交互式引导配置）；changelog 默认只输出在对话里，仅在你要求时导出 PNG。

**看文字嫌累？** 每个技能配了中英双语的大白话讲解页——下面的链接直达 **GitHub Pages** 渲染版（仓库里的 `eli5/*.html` 是同一批源文件；GitHub 的文件页对 HTML 只显示源码不渲染，别从那里点）：

| 讲解页 | 技能 | 讲什么 |
| --- | --- | --- |
| [中文](https://solplum.github.io/log-skill/eli5/worklog.html) · [English](https://solplum.github.io/log-skill/eli5/worklog.en.html) | worklog | 四源挖掘 → 候选清单 → 闸口确认 → 需求叙事周报 |
| [中文](https://solplum.github.io/log-skill/eli5/alllog.html) · [English](https://solplum.github.io/log-skill/eli5/alllog.en.html) | alllog | 全量挖简历素材、覆盖度回执、日志/整理双层布局 |
| [中文](https://solplum.github.io/log-skill/eli5/change-report.html) · [English](https://solplum.github.io/log-skill/eli5/change-report.en.html) | change-report | 圈范围 → 正式备忘、只读 git、诚实状态标记 |
| [中文](https://solplum.github.io/log-skill/eli5/changelog.html) · [English](https://solplum.github.io/log-skill/eli5/changelog.en.html) | changelog | 本次 vs 本功能、终态 vs 迭代、可读性闸门、交付状态三值 |

---

## 目录

- [各自是什么](#各自是什么)
- [四者差别](#四者差别)
- [安装](#安装)
- [斜杠命令与触发词](#斜杠命令与触发词)
- [模式说明](#模式说明)
- [确认闸口](#确认闸口)
- [存储布局](#存储布局)
- [会话数据源与时区](#会话数据源与时区)
- [限制](#限制)
- [仓库结构](#仓库结构)
- [测试](#测试)
- [许可](#许可)

---

## 各自是什么

**worklog**（本仓库对应 `lzl-worklog`）回答「这周交差写什么」。特性：首次使用自动引导选择存储目录（推荐全局 `~/worklog` 或工作区 `报告文档/需求/` 并持久化记忆）；支持一键「全量扫描（建初始底账）」（直接从全量历史起扫，不再重复询问时间段）；日常用法支持口述一句就记（随手记）、扫描 CC / Codex / ZCode / MiniMax Code 四源会话（主动梳理，支持断点续扫）以及把本周日志收成「需求背景 / 方案 / 落地 / 结果」周报，需要的话再导出 Word，汇报时可并行派最多 4 个轻量 agent 分源提炼（契约见 `lzl-worklog/references/agent-team-contract.md`）。日志只追加；重跑周报只动 `周报/`，不动 `日志/`。

**alllog**（本仓库对应 `lzl-alllog`）回答「哪些能写进简历」。特性：首次使用自动引导选择存储目录（推荐全局 `~/alllog` 或工作区 `./素材/` 并持久化记忆）；支持一键「全量扫描（建初始底账）」（直接从全量历史起扫，跳过时间段询问）；五源扫描（CC / Codex / ZCode / MiniMax Code / Antigravity 双端）；外部读者与招聘视角去黑话（杜绝 Mimosa 等私有内部代号与 AI 调试痕迹，采用 STAR 规范提炼）；候选清单必附**五源覆盖度回执**，杜绝静默漏挖；把 `素材/日志/` 全量汇总成按项目归组的 `素材/整理/<当天>.md` 快照。对话里出现「素材库」「记简历」**不得**自动启动本技能，必须显式使用 `/lzl-alllog` 或 `/alllog`。

**change-report** 回答「这段 git 改动，给上级怎么写」。只读 `git status` / `log` / `diff`，绝不 commit / push / reset。先圈范围（未提交 / 未推送 / 已推送未合并，或 `--record` / `--range` / `--commit`），起草正式备忘，你确认「为什么」之后才落 `变更记录.md` + md 报告，再委托 `docx` skill 出 Word。推断不出原因就标「原因待确认」，没跑测试就标「未验证」，绝不编造。它还是**可组合、可恢复**的（V3 执行模型，优先于技能内任何冲突规则）：commit 前 / push 前 / push 后 / 补记都能调用，没有规定顺序；重复调用同一范围默认展示或更新 md 草稿再重渲染，md 源保留在 `md形式/`；可选的本地状态索引可记 `reported` 与输出路径，但索引和报告内容都绝不自动 commit / push。

**changelog** 回答「实际改了什么，导师没看对话能不能看懂每一行」。每次必问范围（**本次**会话的实际改动 vs **本功能**全周期）、有被替代的迭代时再问粒度（只记终态 vs 逐版各一行），按 `changelog/references/evidence-routing.md` 路由到最小证据集（对话定范围和理由；文件、git、PR、测试、CI、云端记录只在请求涉及时才看——聊天里说改了不算改，必须有记录）。产出编号主表（改动事项 / 原背景 / 本次实际改动 / 交付状态 / 验证结果）+ 每条对应的「具体改动文件」小节；交付前逐行过**可读性闸门**（没读过对话的人一句白话能复述）；交付状态只有 `未上传 → 已上传 → 已部署` 三值，验证结果必须写明来自哪个环境（本地 / CI / 云端 / 线上）；部署依赖第三方拉取重建时保持 `已上传` 并附一行「部署说明」（谁拉哪个分支重建后才在线上生效）。交付后固定追问：删改哪几条、要不要把表格导出成图片。查无实据时只输出一句「本次未发现已经落实的改动，不生成变更表格」，绝不生成空表。

---

## 四者差别

| | worklog | alllog | change-report | changelog |
| --- | --- | --- | --- | --- |
| 读者 | 老板 / 站会 / 周报 | 以后写简历的自己 | 老板 / 「这次 diff 改了啥」 | 接手工作的导师 |
| 输入 | 助手会话 + 你口述 | 助手会话 + 你口述 | **只有 git** | 对话 + 最小相关证据（git / PR / 测试 / CI / 云端） |
| 谁能启动 | 口令或 `/worklog` | 只有 `/alllog` 或点名 | 口令或 `/change-report` | `/changelog` 或口令 |
| 时间 | 本周，文件名是周一 | 全量，文件名是今天 | 一段 git 范围，文件名是最旧 commit 日期 | 本次对话或本功能全周期（必问，不猜） |
| 去重 | 本周日志里相同 `[需求名]` 跳过 | 全部日志里「同项目且同要点」才跳过 | 该项目 `变更记录.md` 里同主题跳过 | 证据说了算：无记录 = 无条目 |
| 成稿 | 每个需求四段：背景 / 方案 / 落地 / 结果 | 每个项目五段：背景 / 技术栈 / 亮点 / 结果 / 素材记录 | 一句话目标 / 背景 / 本次改动 / 改动文件 / 验证结果 | 编号主表 + 具体改动文件小节 |
| 落盘 | `报告文档/需求/` | `$ALLLOG_DATA_ROOT`（默认 `~/alllog`） | `报告文档/代码/<项目>/` | 默认不落盘，仅按要求导出 PNG |

四个一起用：worklog 管「这周欠老板什么」，change-report 管「这段 git 干了什么」，changelog 管「实际改动怎么交接」，alllog 管「什么值得写上简历」。

---

## 安装

先 clone，再把 **技能目录本身** 拷进各 CLI 的 skills 目录（目录顶层要有 `SKILL.md`）。

### Claude Code

```bash
git clone https://github.com/solplum/log-skill.git
mkdir -p ~/.claude/skills
cp -R log-skill/lzl-worklog    ~/.claude/skills/lzl-worklog
cp -R log-skill/lzl-alllog     ~/.claude/skills/lzl-alllog
cp -R log-skill/change-report  ~/.claude/skills/change-report
cp -R log-skill/changelog      ~/.claude/skills/changelog
# 可选软链接别名：
ln -s ~/.claude/skills/lzl-worklog ~/.claude/skills/worklog
ln -s ~/.claude/skills/lzl-alllog  ~/.claude/skills/alllog
```

### Codex

```bash
git clone https://github.com/solplum/log-skill.git
mkdir -p ~/.codex/skills
cp -R log-skill/lzl-worklog    ~/.codex/skills/lzl-worklog
cp -R log-skill/lzl-alllog     ~/.codex/skills/lzl-alllog
cp -R log-skill/change-report  ~/.codex/skills/change-report
cp -R log-skill/changelog      ~/.codex/skills/changelog
# 可选软链接别名：
ln -s ~/.codex/skills/lzl-worklog ~/.codex/skills/worklog
ln -s ~/.codex/skills/lzl-alllog  ~/.codex/skills/alllog
```

Windows PowerShell 与英文节同构，把四个目录 `Copy-Item -Recurse` 过去即可。拷完重启 CLI 重新加载技能。

可选：首次运行前设 alllog 数据根（任意你拥有的绝对路径）：

```bash
export ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
```

```powershell
$env:ALLLOG_DATA_ROOT = "$env:USERPROFILE\Documents\resume-materials"
```

不设就用 `~/alllog`（Windows 为 `%USERPROFILE%\alllog`）。

---

## 斜杠命令与触发词

### worklog (lzl-worklog)

| 你输入 | 模式 |
| --- | --- |
| 首次运行 | 闸口⓪——选择存储目录（推荐全局 `~/worklog` 或工作区 `./报告文档/需求/`） |
| `/lzl-worklog` 或 `/worklog`（不带别的字） | 闸口①——问：全量扫描 / 梳理最近做了什么 / 随手记 / 出周报？ |
| `全量扫描` / `全量梳理` / `建初始底账` | 模式 A——全量挖掘历史全部会话（直接开始，免除闸口②） |
| `记录一下：…` / `记一下：…` | 模式 B——随手记录 |
| `梳理一下最近做了什么` / `梳理一下` | 模式 A——挖会话 |
| `周报` / `汇报` / `产出` / `站会` / `晨会` | 出周报（站会加 Scrum 三问） |

### alllog

| 你输入 | 模式 |
| --- | --- |
| `/alllog`（不带别的字） | 闸口①——问：记一条 / 挖素材 / 出素材库？ |
| `全量记一下：…` / `记简历：…` | 模式 B——随手记录 |
| `全量梳理` / `挖简历素材` | 模式 A——挖会话 |
| `接着上次挖` / `从上次停的地方继续` | 模式 A，预选「从上次停点续挖」 |
| `素材库` / `汇总简历素材` / `出简历素材库` | 汇总（仅在 `/alllog` 已运行时） |

上表短语都是 **`/alllog` 的参数**，不是全局自动触发词。

### change-report

| 你输入 | 模式 |
| --- | --- |
| `/change-report`（不带别的字） | 闸口①——选 git 范围（未提交 / 未推送 / 已推送未合并，或 SHA / 区间 / 记录号） |
| `提交报告` / `改动报告` / `给上级的报告` / `这次改了什么` / `change report` | 同一技能；未点名范围时仍停在范围闸口 |
| `本周工作总结` | 指 **git** 备忘时归它；指会话叙事周报请用 `/worklog` |

也可传 `--record <ID>` / `--range <base>..<head>` / `--commit <SHA>` 跳过范围选择。

### changelog

| 你输入 | 行为 |
| --- | --- |
| `/changelog` | 先过范围闸口：本次还是本功能？有被替代的迭代再问粒度 |
| `记录本次改动` / `比较本地与云端` / `有哪些还没提交` / `有哪些还没推送` | 同一技能；话里已钉死范围的（如云端对比）不再重复问 |
| `这个 PR 改了什么` / `今天改了什么` | 按语义路由到对应证据集；范围仍歧义时先问 |
| `发现页改造这个事做得怎么样` | 本功能全周期：从事物起点锚定到现在的完整演进 |

本技能（changelog）是**报告**，不是 `CHANGELOG.md` 写手：绝不创建/编辑那个文件，绝不 commit / push / merge / reset / 部署。

---

## 模式说明

### worklog 模式 B——随手记录

1. 算本周一（`date +%u`，周一=1）。
2. 打开或创建 `报告文档/需求/日志/<周一>.md`。
3. 在当天 `## MM-DD` 节下追加 `- [需求] 一句话`。只追加，绝不覆盖旧条目。

### worklog 模式 A——主动梳理

1. **闸口②**：本周一-现在 / 近 7 天 / **从上次搜索-现在**（读 `.last-scan` 断点；无断点则说明并重新给其余选项）/ 自定义。问完即停。
2. 扫四源（缺哪个源跳过并提示）。扫完把今天写进 `报告文档/需求/.last-scan`。
3. 列**编号**候选，不落盘。用户消息里的密钥/密码一律脱敏。
4. **闸口③**：「记哪几条？」问完即停。
5. 只写你点名的条目，回执写明写了什么、漏了什么。

### worklog 周报

1. 读本周日志。
2. **闸口②**选范围（同上四项；起点即周报文件名）。四源挖完后同样更新 `.last-scan` 断点。
3. 按需并行派最多 4 个轻量 agent（Agent-CC / Agent-Codex / Agent-Zcode / Agent-Minimax，契约见 `worklog/references/agent-team-contract.md`）。某源跳过就不派、不出空草稿。
4. 合成需求叙事草案。**闸口③**列编号清单问「全写还是删哪几条」。
5. 写 `周报/md形式/<起点>.md`，删除全部中间草稿（`-cc-` / `-codex-` / `-zcode-` / `-minimax-`）。
6. 有 docx skill 就问要不要导出 `周报/word形式/<起点>.docx`。

模板（人话三段式，组会直接念）：

```markdown
# 产出汇报（<起点> ~ <终点>）

## 1. <动宾平实成果标题>
- **痛点问题**：…   # 之前有什么痛点、阻碍或低效
- **关键改动**：…   # 本周采取了什么关键解决动作，去配置流水账
- **实际效果**：…   # 现在达到了什么状态，带来什么实际改变；缺失标「待补充」

## 下周重点与协作项
- **下周规划**：…
- **需要协调**：…
```

### alllog 模式 B——随手记录

1. `$TODAY=$(date +%F)`。
2. 打开或创建 `$ALLLOG_DATA_ROOT/素材/日志/$TODAY.md`。
3. `## MM-DD` 节下追加 `- [项目名] …`。

### alllog 模式 A——挖简历素材

1. **闸口②**：全部 / **从上次停点续挖**（最新日志文件名 +1 天；日志为空等同全部）/ 近 30 天 / 自定义。（若在闸口①选择了「全量扫描」，直接跳过闸口②并从历史起点直接开始扫描）。
2. 五源分别用 `lzl-alllog/SKILL.md` 内嵌的**给死脚本**扫描（CC 会话扫 / Codex 索引优先 / ZCode 只读 SQLite / MiniMax messages.jsonl / Antigravity 桌面端+CLI 双端探测），留存排除计数供回执。
3. **按事情提炼候选**：严禁按物理路径分类，直接根据五源会话主题与真实工作，按具体事情归并提炼为 STAR 结构化候选清单（去黑话、去自嗨），同屏必附五源覆盖度回执。
4. **闸口③**：编号清单「记哪几条？」（如“全部”、“记 1, 3”）。问完即停。
5. 只写你点名的条目到 `素材/日志/`。

### alllog 汇总

读 `素材/日志/*.md` 全量（日志是唯一事实底账），按 `[项目名]` 归组，写 `$ALLLOG_DATA_ROOT/素材/整理/<今天>.md`（同日重生成覆盖，绝不动日志）。日志为空则提示先记先挖。生成后回执项目数、素材条数、文件路径，并注明「制作简历只需读这份最新整理快照」。

模板（五段：背景 / 技术栈 / 亮点/难点 / 结果/量化 / 素材记录）见上方英文节。

### change-report——git 范围备忘

1. 确认在 git 工作树内，否则退出。
2. 确认有可报告的改动（`git status --short` 或主干有 commit），否则退出。
3. **闸口①**列候选范围问完即停。主干取 `origin/main` → `main` → `master` 第一个存在的；都没有才退回最近 5 条 commit **并说明**。
4. 可读 `docs/change-log.md` 补背景。
5. 从 `git diff --stat`、选中文件 diff、`git log <主干>..HEAD` 起草。缺「为什么」标 `原因待确认`，没测试标 `未验证`。
6. **闸口②**给你确认/补原因，问完即停。
7. 追加 `变更记录.md`（只追加）→ 写 `md形式/<范围起点>.md` → 委托 docx skill 出 Word，md 源保留；渲染失败要说明并保留 md 供手动重试。最后回执 .docx 路径 + 简要摘要（一句话目标 + 大点列表）。

`<范围起点>` = 范围内最旧 commit 的 `%cs` 日期；纯未提交改动用今天；目标文件已存在先确认覆盖。

硬规矩：正式书面语；只写 文件/位置 + 改动 + 效果，**报告里不出现代码、行号、命令**；不带任何凭据与内网地址；主题最多 1–3 个，超了问你怎么砍；正文一页以内、每行 ≤ 25 字；小点按依赖链排序（设计/数据库 → 后端 → 前端）；改动文件清单取自 `git diff --name-only <主干>..HEAD`，按模块分组、每行一个路径。

### changelog——Mentor 交接表

1. **范围闸口（每次必问）**：本次（本会话可归属的实际改动）还是本功能（全生命周期；尽量用计划文档 / ROADMAP / 变更日志锚定起点）。问完即停。
2. **粒度闸口（同轮）**：仅当存在被替代的迭代——只记终态 vs 逐版一行。
3. 按 `changelog/references/evidence-routing.md` 路由最小证据集（对话定范围与理由；文件 / git / PR / 测试 / CI / 云端 / 运行日志只在请求涉及时看）。聊天说改了 ≠ 改了。
4. 产出 汇总范围 + 判断依据 → 编号主表（改动事项 / 原背景 / 本次实际改动 / 交付状态 / 验证结果）→ 每条一个「具体改动文件」小节。全周期口径下每行的「以前」= 事情开始前的状态。
5. 交付前逐行过**可读性闸门**：「以前…；现在…」句式、术语带白话解释、没读过对话的人一句能复述；不过就重写，闸门不可跳过。
6. 你说「删除 2、4」「合并 2 和 3」「把 5 放最前」→ 照办、连续重排号、同步文件小节、返回完整干净版。
7. 收尾固定一问：①按号删改；②表格导出 PNG（只含标题行、元信息行、主表；用样式化 HTML → 本地临时服务 → 浏览器截图渲染）。都不要就结束。

云端对比（`相比云端有哪些改动`）分 `本地未提交改动` / `本地独有改动` / `云端独有改动` 三组，带 `比较概览` 计数行和 `云端状态` 头（如实写明是否真拿到了云端最新版本信息）。

---

## 确认闸口

四个技能的最高优先级规则。展示过选项/候选后必须 **ask then stop（问完即停）**：你下一轮回复之前，禁止任何扫描、深读、落盘、派 agent。

| | worklog | alllog | change-report | changelog |
| --- | --- | --- | --- | --- |
| ① | 裸 `/worklog` 问模式 | 裸 `/alllog` 问模式 | 选 git 范围 | 本次还是本功能（+ 迭代粒度） |
| ② | 日期范围 | 日期范围 | 确认草稿（尤其「为什么」） | —（证据按意图路由，不让你选通道） |
| ③ | 记哪些条？ | 挖哪些项目？ | — | — |
| ④ | — | 记哪些条目？ | — | — |
| 收尾 | — | — | — | 删改条目 / 导出图片 |

写在技能里防违规的细则：

- **禁止自问自答**：问完「近 30 天还是全部？」下一句自己接「那就近 30 天」= 违规（no self-answer）。
- 含糊回答（`都行` / `好` / `随便`）≠ 选择，必须再问。
- **无确认 = 0 条写入**，没有默认全选。

---

## 存储布局

### worklog（相对工作区）

```
报告文档/需求/
├── .last-scan               # 扫描断点，一行 YYYY-MM-DD
├── 日志/<周一>.md
└── 周报/
    ├── md形式/<起点>.md
    └── word形式/<起点>.docx
```

```bash
DOW=$(date +%u)   # 1=周一
MONDAY=$(date -d "$(date +%F) -$((DOW-1)) days" +%F)
```

周内任意调用都定位到同一份日志。

### alllog（用户可配置）

```
$ALLLOG_DATA_ROOT/          # 默认 ~/alllog
└── 素材/
    ├── 日志/<YYYY-MM-DD>.md    # 只追加日志——唯一事实底账
    └── 整理/<YYYY-MM-DD>.md    # 按项目归组的汇总快照，每日重生成
```

```bash
export LZL_ALLLOG_DATA_ROOT="$HOME/Documents/resume-materials"
python lzl-alllog/scripts/paths.py                    # 打印数据根
python lzl-alllog/scripts/paths.py --journal 2026-08-17   # 该日日志文件
python lzl-alllog/scripts/paths.py --digest  2026-08-17   # 该日整理快照
python lzl-alllog/scripts/paths.py --latest               # 最新日志日（续挖停点）
```

数据放技能目录**外面**，防止以后 `git pull` / 重新拷贝时被清掉。

### change-report（相对工作区，按 git 仓分目录）

```
报告文档/代码/
├── _projects.json           # 可选 { "<git根路径>": "<目录名>" }
└── <项目>/
    ├── 变更记录.md
    ├── md形式/<范围起点>.md
    └── word形式/<范围起点>.docx
```

`<项目>` = `_projects.json` 里的映射名，未映射用 git 根目录名。同款规则的脚本：

```bash
python change-report/scripts/project_name.py /path/to/repo 报告文档/代码/_projects.json
```

### changelog（默认不落盘）

表格只在对话里。唯一可能产生的文件是你在收尾问题里明确要的 PNG，存到你指定的位置。

---

## 会话数据源与时区

worklog 和 alllog 读同一批本地存储，缺哪个源跳过并提示。change-report **不读**这些存储，只读 git。changelog 只在路由到的证据需要时才读。

| 源 | 路径 | 时间基准 |
| --- | --- | --- |
| Claude Code（CC） | `~/.claude/projects/**/*.jsonl` | JSONL 内 `"timestamp"`，**UTC**；alllog 以**末条** timestamp 定会话日期（跨天会话不漏），worklog 按单条记录过滤 |
| Codex——alllog | `~/.codex/session_index.jsonl` 首选（thread 名 + `updated_at`），目录扫描兜底 | 索引 `updated_at` 是 **UTC** |
| Codex——worklog | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` + `archived_sessions/`（顶层平铺）；**不读索引**——实测索引 thread_name 多为「你好」 | 目录/文件名内嵌**本地**时间 |
| ZCode | `~/.zcode/cli/db/db.sqlite`（`session` / `message` / `part` 三表） | `session.time_updated`，epoch **毫秒** |
| MiniMax Code | `~/.minimax/v2/sessions/YYYY/MM/DD/HH-MM-SS-mmm-session_*/messages.jsonl` | 文件内末条 `message.timestamp`，epoch **毫秒**——禁用目录名日期过滤 |
| Antigravity（lzl-worklog） | 桌面端 `~/.gemini/antigravity/` + CLI `~/.gemini/antigravity-cli/` 双端同构（`conversation_summaries.db` + `transcript.jsonl`） | `last_modified_time`，**UTC** |

时区（漏掉这步，周一早上的活就丢了）：

- CC 的 UTC 时间戳先转本地（`date -d "<TS>" +%F`）再和「本周 / 起点」比较。`2026-08-12T02:00:00.000Z` 在 UTC+8 是 08-12 10:00——直接比 `Z` 日期，本地 00:00–07:59 的记录会掉进前一天消失。
- Codex 索引时间戳是 UTC（比较前 `astimezone()` 转本地）；目录/文件名已是本地时间。
- ZCode 与 MiniMax Code 是绝对毫秒：`$START_MS=$(( $(date -d "$START 00:00:00" +%s) * 1000 ))`，挖全部传 `0`。MiniMax 必须用文件内末条时间戳过滤，跨天会话按目录名会漏。

ZCode 库**只读打开**（`mode=ro`）——CLI 运行时正占用它，写句柄会和 WAL 打架。同一查询内嵌在两个 `SKILL.md` 里，`*/scripts/zcode_sessions.py` 是可执行副本（单测直接驱动）。

会话日志的用户消息里可能贴过密钥/token/密码：候选与落盘一律脱敏或省略。

---

## 限制

- 这些是 agent 指令，不是托管服务：效果取决于模型是否真在闸口停下。
- 技能里的日期运算用 GNU `date -d`；macOS 请换 `gdate`。
- worklog 汇报的 agent 在 Claude Code 内指定 haiku 级；其他 CLI 用自己最便宜的可用子代理。
- Word 导出需要单独的 `docx` skill，缺了要说并停；change-report 无论如何保留 md 源。
- change-report 对 git 只读：不 commit / push / reset，报告里不贴代码和密钥。
- changelog 绝不写 `CHANGELOG.md`，绝不 commit / push / merge / reset / 部署；PNG 导出需要浏览器截图能力，缺了要说明。
- `本周工作总结` 有歧义：git 备忘 → `/change-report`；会话叙事周报 → `/worklog`；交接表条目 → `/changelog`。
- alllog 可能提到 `job-tailored-resume` 作为下游技能；那个技能**不在本仓库**。
- 别把真实周报、简历素材、变更报告或活的 `jsonl` / SQLite 导出提交进仓库；`*/test/fixtures/` 里都是假数据。
- 作者机器路径（Windows 盘符家目录、工作区绝对路径）不得出现在发布副本里：alllog 数据根是环境变量不是写死的盘符，单测会扫每一个发布文件防泄漏。

---

## 仓库结构

```
lzl-worklog/                 # 整个目录拷进 ~/.claude/skills/ 与 ~/.codex/skills/
  SKILL.md
  references/agent-team-contract.md
  scripts/zcode_sessions.py
  test/test-worklog.md
  test/fixtures/
lzl-alllog/
  SKILL.md
  scripts/paths.py           # LZL_ALLLOG_DATA_ROOT 解析 + 日志/整理路径
  scripts/zcode_sessions.py
  test/test-alllog.md
  test/fixtures/
change-report/
  SKILL.md
  scripts/project_name.py    # _projects.json → 目录名
changelog/
  SKILL.md
  references/evidence-routing.md
  references/output-format.md
  agents/openai.yaml
eli5/                        # 每个技能一篇自包含讲解页（中英双语各一）
  worklog.html
  worklog.en.html
  alllog.html
  alllog.en.html
  change-report.html
  change-report.en.html
  changelog.html
  changelog.en.html
tests/                       # 本仓库的 unittest 检查
```

---

## 测试

仓库根目录（Python 3.10+，仅标准库）：

```bash
python -m unittest discover -s tests -v
```

测试直接驱动随附的 `paths.py`、`zcode_sessions.py`、`project_name.py`，并检查每个 `SKILL.md` 仍写明自己的模式、闸口、数据源与输出模板——包括 changelog 的范围/粒度闸口与交付状态三值——以及任何发布文件里都没有作者机器路径。

手动 agent 走查（只用 fixtures，不碰真实会话）见 `lzl-worklog/test/test-worklog.md` 与 `lzl-alllog/test/test-alllog.md`。

---

## 许可

MIT。见 [LICENSE](./LICENSE)。
