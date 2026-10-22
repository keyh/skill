# Unity：按切图创建规则瓦片

Unity：按切图创建规则瓦片。适用于游戏、编辑器、场景、音频、渲染和三维文件转换相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`unity--tilemap-ruletile-createfromsegment`
- 原始技能名：`tilemap-ruletile-createfromsegment`
- 分类：Unity与CAD
- 兼容性：平台或插件依赖
- 依赖：保留 Unity 整包目录；阅读 SKILL.md 确认所需工具。复制技能文件不会安装插件、MCP、CLI或账号授权。
- 许可：Unity Companion License
- 来源：Unity 插件 0.1.0-beta

## 原始说明

Use when the user wants tiles that auto-tile (autotile) as they paint, wants a RuleTile built from existing terrain or edge sprites, or asks to make sprites \"tile correctly\" or \"connect properly\". Also converts sprite-segment-3x3grid output patterns into Unity RuleTile TilingRules: 3x3 grid text patterns (X, ., *) become TilingRule neighbor configurations, mapping '.' to 'This' rules and 'X' to 'DontCare', sorted by specificity (more 'This' rules first). Use when creating RuleTiles from sprite analysis or defining tile neighbor rules programmatically. Sprites must be provided as input.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../../../CATALOG.md)
