# Figma：生成关系图

Figma：生成关系图。适用于品牌视觉、设计规范、用户体验研究和设计评审相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`figma--figma-generate-diagram`
- 原始技能名：`figma-generate-diagram`
- 分类：设计与品牌
- 兼容性：平台或插件依赖
- 依赖：保留 Figma 整包目录；阅读 SKILL.md 确认所需工具。复制技能文件不会安装插件、MCP、CLI或账号授权。
- 许可：本地未发现完整许可文件；不视为获得额外授权
- 来源：Figma 插件 16.0.0

## 原始说明

MANDATORY prerequisite — load this skill BEFORE every `generate_diagram` tool call. NEVER call `generate_diagram` directly without loading this skill first. Trigger whenever the user asks to create, generate, draw, render, sketch, or build a diagram — flowchart, architecture diagram, sequence diagram, ERD or entity-relationship diagram, state diagram or state machine, gantt chart, or timeline. Also trigger when the user mentions Mermaid syntax or wants a system architecture, decision tree, dependency graph, API call flow, auth handshake, schema, or pipeline visualized in FigJam. Routes to type-specific guidance, sets universal Mermaid constraints, and tells you when to use a different diagram type or skip the tool entirely (mindmaps, pie charts, class diagrams, etc.).

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../../../CATALOG.md)
