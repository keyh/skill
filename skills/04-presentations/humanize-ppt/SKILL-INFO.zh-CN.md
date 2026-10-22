# PPT视觉优化与去模板化

PPT视觉优化与去模板化。适用于汇报材料、可编辑幻灯片、图片转PPT和网页演示相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`humanize-ppt`
- 原始技能名：`humanize-ppt`
- 分类：PPT与演示
- 兼容性：脚本或工具依赖
- 依赖：按 SKILL.md 安装和配置所需运行环境；本仓库安装器只复制文件，不执行技能脚本或启用后台功能。
- 许可：MIT
- 来源：https://github.com/LearnPrompt/humanize-ppt

## 原始说明

A presentation system for agent-made PPTs — born for the talk, not just the template. It turns raw material into an AST (audience-state-transfer) outline with per-page visual-enhancement decisions (image / SVG diagram / video), hands a production brief to a downstream renderer (HTML-PPT skills or native PPTX), then runs a capped 3-round presentation checkup (演讲体检) on the rendered deck. It never renders slides itself. Use before generating PPT/HTML slides from raw material, and after rendering when the user says things like "给这份 deck 做演讲体检" or "PPT 渲染质检". If all you want is one beautiful template page with no outline and no checkup, a rendering skill alone is enough.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../CATALOG.md)
