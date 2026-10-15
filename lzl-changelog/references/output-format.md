# Output Format

Use this reference after the scope and evidence are known.

## Report shape

Start with the scope and evidence actually used:

```text
汇总范围：本次对话涉及的实际改动
判断依据：当前对话、本地 Git diff、测试输出
```

Then output this main table:

```markdown
| 序号 | 改动事项 | 原背景/问题 | 本次实际改动 | 交付状态 | 验证结果 |
|---:|---|---|---|---|---|
| 1 | 登录错误分类 | 以前不管哪种登录失败，页面都提示同一句话，用户分不清是密码错了还是网络断了 | 现在密码错误、网络异常、服务故障分别显示不同的提示，用户一眼能看出该重试还是改密码 | 未上传 | 测试通过 |
```

Field rules:

- `改动事项` is a short noun phrase naming the changed outcome.
- `原背景/问题` describes the real prior state or limitation, not a generic goal.
- `本次实际改动` describes the observable transition from the old state to the new state.

Plain-language rules (mandatory for `原背景/问题`, `本次实际改动`, and the `具体变化` cells below):

- **场景 + 之前 → 现在.** Each description must let the reader see who perceives the change and in what situation, phrased as "以前…；现在…" or an equivalent subject–verb–object sentence. Example: 「以前不管哪种登录失败都提示同一句话，分不清是密码错了还是网络断了；现在密码错误、网络异常、服务故障分别显示不同的提示」.
- **术语必须带白话解释.** The first mention of any technical term inside a description gets a short parenthetical gloss, e.g. 「429 护栏（请求太频繁时暂时拒绝）」. The reader is assumed to know the product, not the implementation jargon.
- **禁止无主语的纯名词短语句式.** 「将凭证错误、网络异常和服务异常拆分为不同响应与提示」is a banned style — no subject, no scenario, verb-noun stacking. Write the sentence out instead.
- `原背景/问题` and `本次实际改动` describe the change itself — the problem it addresses and the behavior/content transition. Delivery actions (commit, push, merge, deploy) never appear in these columns or in the `改动事项` name; never name an item with effect-implying words (e.g. “上云/上线”) when only a push happened.
- `交付状态` tracks one item's delivery progress（未上传 → 已上传 → 已部署，仅此三值）. When a later report covers the same item, keep the item itself unchanged and update only delivery status and validation.
- `验证结果` must state which environment the evidence comes from (本地/CI/云端/线上); never back one environment's delivery with another environment's validation (local E2E passing does not confirm an online deployment works).
- Avoid vague wording such as “优化了”“完善了” or “处理了一下”. Do not put paths, code blocks, or implementation narration in the main table.
- A mentor who did not read the conversation should understand every row.

## Item boundaries and order

Number one independently understandable, independently removable deliverable per item. Split items when they change different behavior, have different delivery states, can be reverted independently, or solve different problems. Keep supporting tests, formatting, lockfiles, generated files, and synchronized docs under the related item unless the test/build/documentation system itself changed independently.

Sort in this order unless the evidence strongly suggests otherwise:

1. Highest impact on the requested outcome.
2. Core logic and user/system behavior.
3. Supporting UI, configuration, and integration changes.
4. Tests, documentation, and cleanup.

Do not sort by chat order, file path, or commit order.

## Delivery and validation

交付状态只有三个值：`未上传`、`已上传`、`已部署`。

- `未上传` = 本地有改动或提交，云端还没有（不区分未提交/已提交未推）
- `已上传` = 已推送到远端分支
- `已部署` = 远端部署已生效

When deployment depends on a third party rebuilding (e.g. a mentor pulls and re-deploys), keep the status `已上传` and add one line after `判断依据`:

```text
部署说明：改动需 <谁> 拉取 <分支> 并重建后才在线上生效，当前线上未包含。
```

`验证结果` must state which environment the evidence comes from (本地/CI/云端/线上); never back one environment's delivery with another environment's validation (local E2E passing does not confirm an online deployment works).

## Iteration granularity (asked at the gate)

When the scope contains superseded iterations (an earlier version later replaced, e.g. v1 random flow → v2 heat ranking), the granularity question decided the mode:

- **终态模式**（one row per deliverable）: the row's `原背景/问题` describes the state before the effort started; replaced intermediate versions do not get their own rows — mention them in one clause inside `本次实际改动` only if the evolution itself matters.
- **迭代模式**（one row per iteration）: each historical version gets its own chronological row, including replaced ones; each row's delivery status reflects that iteration's own state (a replaced iteration is still `已上传` if it was pushed before being replaced).

Never mix modes in one report; the mode comes from the user's answer, not from convenience.

## Cloud comparison layout

For a local-versus-cloud comparison, place cloud metadata after `汇总范围` and `判断依据`:

```text
云端状态：已获取云端最新版本信息
获取时间：2026-08-24 14:30（Asia/Shanghai）
比较概览：本地未提交 1 项；本地独有 2 个提交；云端独有 1 个提交
```

Then group the main-table rows under `### 本地未提交改动`, `### 本地独有改动`, and `### 云端独有改动`. Omit empty groups. Use the ordinary main-table columns in every group and keep numbering continuous across groups. Within this comparison, local groups use `未上传`; remote-only rows use `已上传` and spell out "本地尚未包含" inside the row's `本次实际改动` or `交付状态` cell. The later `具体改动文件` section uses the same global numbers.

## File sections

Immediately below the main table, show a section for every remaining item using the same number and title:

```markdown
## 具体改动文件

### 1. 登录错误分类

| 文件 | 操作 | 具体变化 |
|---|---|---|
| `src/auth/login.ts` | 修改 | 登录失败时按错误原因（密码错/网络异常/服务故障）分别生成不同的提示文案。 |
| `tests/auth/login.test.ts` | 修改 | 新增三类登录失败场景的测试，确认三种情况各显示对应提示。 |
```

File operations are limited to `新增`, `修改`, `删除`, and `重命名`. Describe what the file contributes to that item, not a code dump. The same file may appear under multiple items with different descriptions. If the mapping cannot be confirmed, write `未从现有证据确认`; never guess.

## Editing the draft

Treat the first report as a draft. Handle natural-language requests such as:

```text
删除 2、4
合并 2 和 3
把 5 放到最前面
```

Apply the operation, renumber continuously, update all file sections, and return the complete clean report rather than only describing the edit.

## Closing question and image export

Every report ends with the closing question — one question offering both follow-ups, never skipped:

- ① Item removal: user replies with numbers (e.g. “去掉 8”), apply per the editing rules above and return the clean full report.
- ② Image export: whether to render the table as a PNG and where to save it (commonly the desktop).

Image export format:

- The image contains only the title line, the meta lines (scope/cloud status/evidence), and the **main table** — never the file sections.
- Render the current final version, including any removals applied from ①.
- Rendering route is flexible; the verified one is: styled HTML table → browser screenshot. Note `file://` may be blocked by the browser tool — serve the HTML over a temporary local HTTP server instead, and stop the server after export. Ask the user for the save path; if the screenshot tool cannot write outside the workspace, save inside and copy the file over.
- Keep the image readable for chat handoff: fixed-width columns, ~13px body text, full-page capture.

## No change and safety

When no actual change is supported by evidence, output exactly:

```text
本次未发现已经落实的改动，不生成变更表格。
```

Do not count plans, suggestions, or discussion-only decisions. Do not expose secrets, tokens, cookies, private URLs, personal data, or sensitive configuration values; describe protected configuration generically. A report file created only after an explicit user request is not evidence for the current report and must not recursively list itself.

## Complete example

```markdown
汇总范围：本次对话涉及的实际改动
判断依据：当前对话、本地 Git diff、测试输出

| 序号 | 改动事项 | 原背景/问题 | 本次实际改动 | 交付状态 | 验证结果 |
|---:|---|---|---|---|---|
| 1 | 登录错误分类 | 以前不管哪种登录失败，页面都提示同一句话，用户分不清是密码错了还是网络断了 | 现在密码错误、网络异常、服务故障分别显示不同的提示，用户一眼能看出该重试还是改密码 | 未上传 | 测试通过 |
| 2 | 重复提交限制 | 以前点提交后如果网络慢，用户可以连点几次，导致同一笔请求被重复发送 | 现在请求发出后提交按钮立即置灰（不可再点），请求结束后才恢复 | 未上传 | 测试通过 |

## 具体改动文件

### 1. 登录错误分类

| 文件 | 操作 | 具体变化 |
|---|---|---|
| `src/auth/login.ts` | 修改 | 登录失败时按错误原因（密码错/网络异常/服务故障）分别生成不同的提示文案。 |
| `tests/auth/login.test.ts` | 修改 | 新增三类登录失败场景的测试，确认三种情况各显示对应提示。 |

### 2. 重复提交限制

| 文件 | 操作 | 具体变化 |
|---|---|---|
| `src/pages/LoginPage.tsx` | 修改 | 提交请求进行中把按钮设为禁用，结束后恢复。 |
| `tests/pages/LoginPage.test.tsx` | 修改 | 测试连点提交按钮时只发出一次请求。 |
```
