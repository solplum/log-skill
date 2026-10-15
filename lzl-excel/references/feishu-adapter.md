# 飞书表格适配器指南（Feishu / Lark Sheets Adapter）

本指南说明如何将 `lzl-excel` 的标准数据写入飞书云文档在线表格（Sheets）。

---

## 1. 接入方式

飞书表格支持两种主要操作路径：
1. **官方 CLI（`@larksuite/cli` / `lark-cli`）**：适合终端与 Agent 本地调用，支持命令行建表与单元格样式配置。
2. **飞书开放平台 REST API**：通过飞书应用凭据（App ID / App Secret）直接向开放平台接口发送 JSON 请求。

---

## 2. 权限与授权要求

操作飞书表格需要以下权限范围（Scope）：
- `sheets:spreadsheet`：查看与编辑工作表
- `sheets:spreadsheet:create`：创建新表格
- `sheets:spreadsheet:write_only`：写入表格数据

> [!TIP]
> 首次调用 `lark-cli` 会引导用户在浏览器中完成 OAuth 授权；一旦授权完毕，Token 会保存在本地配置中供后续直接调用。

---

## 3. 工作簿与工作表结构设计

```
[变更记录表 工作簿]
  ├── Sheet 1: cluster-cli (8 列表格)
  ├── Sheet 2: cluster-dashboard-server (8 列表格)
  ├── Sheet 3: cluster-dashboard-web (8 列表格)
  └── Sheet 4: 变更日志 (文档式排版)
```

1. **一仓一表**：以业务仓库名称命名 Sheet（例如 `cluster-cli`、`cluster-dashboard-server`、`cluster-dashboard-web`）；
2. **示例 Sheet 清理**：新建工作簿时飞书默认创建的空白 `Sheet1` 在填充完毕后应予以删除；
3. **冻结与自动换行**：
   - 表头行（Row 1）设置 `frozen_row_count: 1`；
   - 全表单元格默认设置 `wrap_strategy: "WRAP"`（自动换行），确保包含多条编号的单元格正常展示。

---

## 4. 单元格样式与色值规范

| 元素 | 规范设置 | 示例效果 |
|:---|:---|:---|
| **表头底色** | 科技蓝 `#245BDB` 或 深黛灰 `#1F2329` | 高对比度专业感 |
| **表头文字** | 纯白 `#FFFFFF`，`bold: true`，字号 10pt/11pt | 清晰易辨 |
| **表头高度** | 36px ~ 40px | 保证呼吸感 |
| **正文对齐** | 序号居中对齐；其余列左对齐、垂直居中 | 规整阅读体验 |
| **正文换行** | `\n` 换行符驱动，必须开启自动换行 | `1、... \n2、...` |
| **表外注样式**| 字体颜色 `#646A73`（灰色），斜体 `italic: true` | 与正文改动明确区分 |

---

## 5. “变更日志”页（文档式排版）实现细节

当生成全局“变更日志”页时，采用无网格单列文档布局：

1. **隐藏网格线**：设置属性 `show_grid: false`；
2. **列宽设置**：A 列宽度设为 `900`（避免内容过窄挤压）；
3. **日期大标题**：
   - 文本格式：`YYYY-MM-DD`（如 `2026-10-15`）；
   - 样式属性：字号 `14`，`bold: true`，**`horizontal_alignment: center`（居中对齐）**；
   - 边框：底部单实线横线分隔；
4. **小节与圆点内容**：
   - 仓库标题：`horizontal_alignment: left`，字号 `11`，颜色 `#245BDB` 加粗；
   - 变更条目：左对齐，字号 `10`，每条前置 `• `。
