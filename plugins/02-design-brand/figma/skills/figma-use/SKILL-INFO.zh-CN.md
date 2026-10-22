# Figma：Figma操作总入口

Figma：Figma操作总入口。适用于品牌视觉、设计规范、用户体验研究和设计评审相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`figma--figma-use`
- 原始技能名：`figma-use`
- 分类：设计与品牌
- 兼容性：平台或插件依赖
- 依赖：保留 Figma 整包目录；阅读 SKILL.md 确认所需工具。复制技能文件不会安装插件、MCP、CLI或账号授权。
- 许可：本地未发现完整许可文件；不视为获得额外授权
- 来源：Figma 插件 16.0.0

## 原始说明

**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../../../CATALOG.md)
