# Evidence Routing

Use this reference when deciding what the user means by “changes” and which evidence to inspect. The user does not select channels; the skill routes to the smallest relevant set.

## Scope precedence

**Gate: the scope question is asked on every invocation, before any evidence gathering.** Ask the user: 本次（本次会话的改动）还是 本功能（本功能全周期）？Never default silently — the same conversation can legitimately produce either report.

Resolve scope in this order after the gate:

1. Explicit project, module, file, commit, PR, branch, comparison, or time range.
2. An explicit comparison such as “相比云端有哪些改动”.
3. A time expression such as “今天” or “本周”.
4. The scope answer from the gate: ① 本次 → current conversation and its attributable work; ② 本功能全周期 → the whole lifecycle of the named effort/topic.
5. The smallest scope supported by the current project and conversation.

Examples:

| User wording | Scope | Primary evidence |
|---|---|---|
| `记录本次改动` | Ask: 本次 or 本功能 | Depends on the answer |
| `相比云端有哪些改动` | Local state versus the current remote tracking branch | Local Git plus remote Git |
| `有哪些还没提交` | Working tree and index | Local Git diff |
| `有哪些还没推送` | Local-only commits, with uncommitted changes reported separately | Local commits plus remote tracking branch |
| `这个 PR 改了什么` | The named PR's change set | PR, commits, review records |
| `今天改了什么` | Changes in the requested time window | Commits, conversation, project records |
| `记录登录模块的改动` | Actual changes in the named module | Conversation plus scoped file/Git evidence |
| `发现页改造这个事做得怎么样` | 本功能全周期：the effort from its origin to now | Full git history of the effort's paths, project records (change-log / troubleshooting / plan docs / ROADMAP), conversation for recent decisions |

Ask one concise question only when multiple projects, PRs, branches, or comparison bases remain plausible. State the current best guess and recommendation in the question.

## Effort (本功能全周期) scope

When the gate answer is 本功能全周期, the effort's evidence spans everything since its origin:

- **Anchor the start**: prefer project records — plan docs (`docs/**/plans/`), ROADMAP, the earliest change-log entry naming the topic. If no record anchors it, ask one question with the best-guess boundary as recommendation.
- **Evidence set**: full git history of the effort's paths (`git log -- <paths>`, plus `--grep` on topic keywords across branches), project records above, and the conversation for recent decisions and rationale.
- **Superseded iterations**: how they appear in the table is decided by the granularity question — final-state-only (one row per deliverable, "before" = the state before the effort started) or per-iteration rows in chronological order. Do not decide silently.

## Channel selection

| Channel | What it establishes | Use when | Limits |
|---|---|---|---|
| Current conversation | Scope, background, reason, decisions, and actions mentioned | Every invocation | Cannot prove a file changed |
| Local files and Git diff | Added, modified, deleted, or renamed files and exact working-tree changes | The scope includes local work | May contain unrelated work |
| Local commits | Saved change batches and commit status | A commit is mentioned or relevant | Commit messages may be vague |
| Remote Git, PR, and review | Pushed, reviewed, remote-only, or review-driven changes | The user mentions cloud, push, PR, review, or a remote branch | Requires access and may omit unpushed work |
| Project records | Historical context, requirements, task descriptions, or prior change notes | A directly related record exists | May be stale or incomplete |
| Tests, builds, and terminal output | Validation results | Checks ran within the requested scope | Cannot prove the implementation itself |
| CI/CD and release records | Merge, release, deployment, and automated checks | The request involves release or deployment | Often lacks implementation rationale |
| Runtime logs | Observed behavior after a change | The request involves an incident, deployment, or runtime result | Cannot identify a code change by itself |

Do not scan broad logs, file timestamps, or unrelated documents just to appear comprehensive. Use the conversation plus the minimum evidence needed to support each reported fact.

## Local Git evidence

For a local change scope, inspect the repository status, unstaged and staged name/status/stat views, and the relevant diff or file contents. Include untracked files only after checking their contents and attributing them to the requested scope. Use commit history when the request includes saved history or a time range.

A dirty working tree can contain other work. Attribute files using the conversation, explicit paths, the selected scope, and diff content. Do not use modification time as default attribution. If attribution remains unreliable, ask rather than mix unrelated changes into the report.

## Cloud comparison

When the user asks for a cloud comparison or remote state, determine the current branch's tracking branch first. If it is unambiguous, obtain the latest remote version information before comparing. Fetching remote metadata must not alter working files or perform pull, merge, checkout, reset, commit, push, or deployment.

Report the result with these exact labels:

```text
云端状态：已获取云端最新版本信息
获取时间：<YYYY-MM-DD HH:mm（本地时区）>
```

If remote metadata cannot be obtained:

```text
云端状态：未能获取云端最新版本信息
以下结果基于本地保存的远端信息，可能不是云端最新状态
```

Separate uncommitted local changes, local-only commits, and remote-only commits when the comparison supports that distinction. Report their counts before the tables:

```text
比较概览：本地未提交 <N> 项；本地独有 <N> 个提交；云端独有 <N> 个提交
```

In the report, use up to three headings in this order: `本地未提交改动`, `本地独有改动`, and `云端独有改动`. Omit empty groups, keep item numbers continuous across all groups, and keep the file sections keyed to those global numbers. If there is no tracking branch or several plausible bases, ask with a recommendation instead of silently choosing one.

## Conflicts and provenance

- Actual file changes follow diff, commit, and PR evidence.
- Background and rationale follow explicit user statements, requirements, and PR descriptions.
- Validation follows real test, CI, build, and runtime records.
- If the conversation says something was changed but no change evidence exists, omit it.
- If evidence cannot be reconciled, write `来源存在冲突` and explain the conflicting facts briefly; do not select the convenient version.
- The report header must name the scope and the evidence actually used.
