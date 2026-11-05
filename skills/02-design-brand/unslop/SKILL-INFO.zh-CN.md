# 去 AI 味界面打磨（unslop）

去除界面的 AI 生成感并建立产品专属视觉方向。先按迹象清单审计，写五行方向（产品、性格、世界、亮点、签名），再按间距、颜色、图标、文案、字体、布局、细节、视觉、动效九遍打磨；适用于网页、仪表盘和 App 界面的设计评审与改版。

- 仓库唯一编号：`unslop`
- 原始技能名：`unslop`
- 分类：设计与品牌
- 兼容性：脚本或工具依赖
- 依赖：核心流程只需读写 HTML/CSS；`scripts/snapshot.mjs`（抓取线上页面）和 `scripts/story.mjs`（生成改版过程视频）需要 Node、Playwright 和 ffmpeg。本仓库安装器只复制文件，不执行技能脚本或启用后台功能。
- 许可：CC BY 4.0（须保留作者 Damir Sokolovsky / @heydamir 署名）
- 来源：https://github.com/heydamir/unslop

## 原始说明

Turns vibecoded, AI-looking UI into a designed interface with its own character. Finds a direction from the product itself, then fixes spacing, color, icons, copy, type, layout, details, visuals and motion in that order, and can generate a real hero visual with an image tool when one is available. Use when the user asks to unslop, polish, clean up or redesign a screen so it stops looking AI-generated, or when a UI shows the usual tells like purple gradients, glows, gradient text, emoji labels, "New ✨" badges, glossy blobs, uppercase tracked labels, pulsing elements or uneven spacing. Works on React, Tailwind, HTML and CSS, for dashboards, apps and landing pages.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../CATALOG.md)
