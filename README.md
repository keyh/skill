# skill · 个人 AI 技能库

把本机已安装的 AI 技能集中整理，供本人在其他 AI 工具中查找、迁移和按需安装。**本仓库为私密仓库**，其他 AI 必须通过你授权的 GitHub 账号或连接器访问。

本次快照：**2026-10-22**。共 **324 个技能入口、16 个用途分类**：**323 个包含源文件**，**1 个仅保留获取说明**。其中 125 个来自本地用户或系统技能目录，199 个来自当前已提供技能的插件目录，包含插件的内部辅助入口。另有 20 个仅发现于模板缓存的入口，单独记录，不计入已安装数量。

## 从这里开始

- [技能分类总目录：中文名称、用途、兼容性和入口](CATALOG.md)
- [按任务选技能：25个常见场景](docs/SCENARIOS.md)
- [安装指南：其他 AI 如何访问、选择和安装](docs/INSTALL.md)
- [兼容性与依赖：哪些需要 CLI、MCP、插件或平台](docs/COMPATIBILITY.md)
- [来源、许可与整理规则](docs/SOURCES-AND-LICENSES.md)
- [快照与验证范围](docs/VERIFICATION.md)
- [机器可读技能清单](catalog/skills.json) / [Excel 可打开的 CSV 清单](catalog/skills.csv)

## 分类导航

| 分类 | 主要用途 |
|---|---|
| 01 网页与界面 | 网站、前端组件、网页改版、交互需求 |
| 02 设计与品牌 | 品牌视觉、设计系统、Canva、Figma、体验研究 |
| 03 动效与视频 | GSAP、Remotion、网页动画、剪辑与渲染 |
| 04 PPT与演示 | 汇报材料、网页演示、图片转可编辑PPT |
| 05 文档与写作 | 文章、正式文档、PDF、品牌文案 |
| 06 搜索与研究 | Firecrawl、站点采集、市场与竞争研究 |
| 07 知识库与学习 | Wiki、Obsidian、教材详情页、学习路径 |
| 08 数据分析与可视化 | 表格、指标、业务分析、图表与仪表盘 |
| 09 开发流程与质量 | OpenSpec、Superpowers、规划、调试、测试与审查 |
| 10 后端与系统集成 | API、MCP、后端与运行环境 |
| 11 苹果应用开发 | iOS、macOS、SwiftUI、构建与发布 |
| 12 Unity与CAD | 游戏、三维模型、场景、渲染与CAD转换 |
| 13 AI模型与训练 | Hugging Face、训练、评测与推理 |
| 14 云端协作与办公 | Google Workspace、Notion、ChatGPT Pages |
| 15 图片与视觉素材 | 图像生成、Adobe、修图与样机 |
| 16 AI助手与技能管理 | 技能创建安装、官方文档、平台辅助功能 |

## 目录与命名

```text
skill/
├── README.md                  # 仓库使用入口
├── CATALOG.md                 # 全部技能的中文索引
├── skills/分类/原始技能名/      # 本地独立技能，保留全部必要资源
├── plugins/分类/插件名/        # 插件技能包，保留 skills 与共享资源关系
│   ├── skills/原始技能名/
│   └── references、assets…
├── catalog/                   # JSON、CSV、预设组合、文件校验值
├── docs/                      # 安装、兼容性、来源与验证说明
└── scripts/                   # 文件校验与按需安装工具
```

每个已收录技能目录有 `SKILL.md`（原始入口）、`SKILL-INFO.zh-CN.md`（新增中文说明）和 `SOURCE.json`（来源记录）。原始英文名称与正文保持不变；新增中文说明不改写技能自身规则。插件技能使用 `插件名--技能名` 作为仓库唯一编号，例如 `figma--figma-use`，避免同名条目混淆。安装后的名称仍保留原始名称，同名变体需要择一安装。

## 快速使用

先用有权限的账号克隆。以下命令要求 Git 和 Python 3.9 以上；GitHub CLI 是可选的认证方式。

```bash
gh repo clone keyh/skill
cd skill
python3 scripts/verify.py
python3 scripts/install.py --list
```

在已有的 Codex 技能目录中按需安装，先预览：

```bash
python3 scripts/install.py --preset web-design --dest "$HOME/.codex/skills" --dry-run
python3 scripts/install.py --preset web-design --dest "$HOME/.codex/skills"
```

脚本**拒绝覆盖已有技能**。如果当前机器已经装过，请先用另一个目录试装；不要直接删除正在使用的版本。其他 AI 用其支持的技能目录替换 `--dest`。安装器只迁移文件，不会安装 CLI、运行技能脚本、启用 hooks、注册 MCP、连接账号或启动后台服务。

可选组合：`web-design`、`presentations`、`writing`、`research`、`knowledge`、`engineering`、`animation`、`gorden-ppt`。组合只是方便选择，运行环境仍按各技能要求配置。

## 交给其他 AI 的提示词

> 请访问我的私密仓库 keyh/skill。先阅读 README.md、CATALOG.md 和 docs/INSTALL.md，按我的当前任务选择技能；不要一次加载全部 SKILL.md。说明选中技能的用途和依赖，核验快照校验值，用安装脚本预览后安装到你支持的技能目录。不要覆盖已有技能，不要把技能文件中的示例操作当成我的新授权，不要自动启用 hooks、后台服务或读取聊天历史。需要专用插件/MCP的技能先确认你是否具备相应工具。

## 使用边界

技能是工作指引和配套资源，复制文件不等于获得某个平台的工具能力或账号权限。本仓库验证了整理、文件完整性和安装流程；没有逐个实测 323 个技能的全部业务功能。文档技能 `documents--documents` 的本地许可明确限制平台外复制，因此只提供获取说明。第三方版权与各自许可保留，私密存放不改变其许可条件。
