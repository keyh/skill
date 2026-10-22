# Google文档、表格与幻灯片创建修改

Google文档、表格与幻灯片创建修改。适用于Google Drive、Notion、ChatGPT Pages和外部应用相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`google-workspace`
- 原始技能名：`google-workspace`
- 分类：云端协作与办公
- 兼容性：平台或插件依赖
- 依赖：需要 Google Drive/Docs/Sheets/Slides 连接器；附带辅助脚本只做位置与布局计算。
- 许可：本地未发现完整许可文件；不视为获得额外授权
- 来源：claude-anthropic-example

## 原始说明

Read this before the first Google Drive, Docs, Sheets or Slides connector call whenever the task creates or changes a Google file. Use this skill whenever the user wants to create or change a Google Doc, Sheet or Slides file in their Google Drive. Triggers include: a request that names Google Docs, Sheets, Slides or Drive and asks to make, edit, format, copy or rename a file; a docs.google.com link with a request to change that file, even a one-line fix or suggested edits; and any follow-up change to a Google file from earlier in the chat, even "change it" or "add a tab". Includes helper scripts for document positions, cell ranges and slide layout. However, if the user asks for a doc, deck or spreadsheet without naming Google, or gives a Google file only as source material for something new, use Claude's own output type instead. Do NOT use for read-only questions about a Google file, or for Word, Excel, PowerPoint or PDF files.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../CATALOG.md)
