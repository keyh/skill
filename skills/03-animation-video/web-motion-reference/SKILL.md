---
name: web-motion-reference
description: 网页动效与 3D 视觉参考库。设计或改版网页、首屏 Hero、登录页、背景、AI 助手形象、知识图谱、讲解动画、转场、加载动画、标题文字动效、宣传短片，或编写 three.js / WebGL / 着色器 / Canvas / SVG / GSAP / CSS 动效之前，先用它检索 1813 个已打中文标签的参考案例：Opus 5.5 动效合集 853 个、three.js 官方示例 608 个、50 个开源效果库的 352 个示例。用它挑参考、核对许可，再动手。内含灵枢医学数字教材的视觉调性、工程约束和已上线的 three.js 场景配方。用户提到动效、特效、粒子、背景动画、3D、three.js、“炫一点”、“有科技感”、找灵感，或要做任何页面视觉时都要用，即使没有提到参考库。
---

# 网页动效与 3D 视觉参考库

设计前先查参考，再动手。这个库的价值在于把“想要什么感觉”快速对到“有人做过、看得到、知道怎么实现”的具体案例上，避免每次凭空想象，也避免选到许可有问题的代码。

## 库里有什么

| 池子 | 条数 | 内容 | 许可 |
|---|---|---|---|
| `opus` | 853 | yihui-dev/awesome-opus5-5-videos：别人用 Opus 5.5 生成的动效短片。有中文描述、标签、封面链接、提示词链接；**没有源码** | C：只借思路，重新实现 |
| `three` | 608 | three.js 官方示例（截至 2026-10-12 的 dev 分支）。有中文描述、标签、在线演示、源码链接、截图链接 | A：MIT，可取代码 |
| `lib` | 352 | 50 个开源效果库的精选示例：TresJS、pmndrs、TSL Textures、Paper Shaders、3d-force-graph、AntV G6、程序化水墨、GSAP、Inspira UI、motion-v、Vue Bits、Codrops 等 | A / B / C 分级，见 `references/licenses.md` |

每条都有：`title` 中文名、`desc` 画面描述、`visual` 视觉元素、`use` 适用位置、`tone` 调性、`palette` 色调、`tech` 实现技法、`fit` 灵枢适配度 1–5、`web` 网页可用度 1–5；适配度高的还有 `idea`（怎么改造给灵枢用）。

## 工作流程

### 1. 说清需求
动手检索前，先用一句话写下：用在哪（首屏、登录、区块背景、AI 形象、图谱、讲解……）、要什么感觉（沉静、典雅、科技……）、技术边界（纯 CSS、Canvas、three.js、能否用后期）、是不是灵枢的页面。是灵枢的页面，先读 `references/lingshu.md`，那里有调性和硬性工程约束。

### 2. 检索
在 skill 目录里运行（Claude Code 中用 `${CLAUDE_SKILL_DIR}/scripts/search.py`）：

```bash
python3 scripts/search.py 粒子 经络 --use 登录背景,首页Hero --min-fit 4
python3 scripts/search.py 水墨 --pool lib,three --tier A          # 只要能直接取代码的
python3 scripts/search.py --use 知识图谱 --tone 学术 --limit 8
python3 scripts/search.py --show vasturiano-3d-force-graph/text-nodes   # 一条的全部字段与链接
python3 scripts/search.py --stats                                  # 看有哪些标签
```

- 关键词是子串匹配，同义词会自动扩展（如“经络”会匹配“流线”）。多个关键词默认须同时命中，结果少时用一个关键词加过滤条件，或加 `--any` 改为命中任一。
- 按技术栈筛：`--stack Canvas,CSS,SVG`（子串，任一）；不想用 WebGL 时加 `--no-webgl`。
- 有些条目是静态生成器（如部分水墨、纸纹），动画要自己加；拿不准时看源码或 demo。
- 至少换两三种说法检索：一次按画面（粒子、水墨），一次按用途（`--use`），一次按技法（ShaderMaterial、ScrollTrigger）。
- 想先看各用途的高分案例，读 `references/top-picks.md`。
- 标签词表：
  - 视觉：粒子 流线 水墨 笔触手绘 几何图形 线框 文字排版 星空宇宙 地球地图 网络图谱 光效辉光 流体烟雾 地形噪声 3D物体 隧道穿梭 图表数据 界面演示 像素风 卡通角色 写实场景 有机生长 玻璃材质 渐变色场 自然景观 人体医学 书本纸张 水面波纹 建筑空间 机械装置 音频可视化
  - 用途：首页Hero 登录背景 区块背景 AI形象 知识图谱 讲解动画 转场过渡 加载等待 数据可视化 宣传短片 互动小游戏 产品演示 标题文字动效 技术演示 仅供欣赏
  - 调性：沉静 典雅 东方 科技 学术 温暖 活泼 炫技 赛博 复古 极简 商务 神秘 写实
  - 色调：深色底 浅色底 单色 高饱和 低饱和

### 3. 看图
文字描述只是索引，选定前要看画面：

```bash
python3 scripts/search.py --poster <id>     # 下载封面或截图到 /tmp/wmr_posters/，打印路径
```

再用 Read 打开图片。一次看 3–6 个候选就够。`lib` 池没有封面，需要时用网页抓取工具打开 `demo` 链接。下载失败通常是网络限制，那就依据描述判断，并告诉用户没能看图。封面只是一帧，运动方式以描述和源码为准。

### 4. 取实现
- **three 池**：`source_raw` 是 dev 分支源码。灵枢固定 three 0.185，取对应版本时把 URL 里的 `dev` 换成 `r185`；返回 404 说明这个示例是 r185 之后新增的，用到的新 API 需要核对。
- **lib 池**：先看 `index/sources.json` 或 `references/sources.md` 里该来源的 `code_access`（clone 方法或 raw 路径模板），再按许可分级处理：
  - A 级：可以读源码、改写进项目，保留原版权声明。
  - B 级：可以用在自家网站，但要遵守条件；不把源码收进 skill、模板或对外分发的东西。
  - C 级：只看思路，自己重新实现。
- **opus 池**：没有源码。`prompt_raw` 是原提示词（GitHub raw），读它学写法；`page` 是 Skillry 的原作与复刻对照页。交付物里不要照搬他人提示词原文，用自己的话重写。写提示词时参考 `references/prompt-craft.md`。
- 能连 GitHub 时用 `git clone --depth 1` 或 raw 链接取代码；其他站点只能用网页抓取工具读。

### 5. 设计与说明
- 在回复里简短说明参考了哪 2–3 个案例、各借鉴什么（构图、运动方式、技法），附上 id 和链接，方便用户去看原作。
- 借鉴的是手法，不是外观。不要复刻某个作品的整体样貌，不要画受版权保护的角色、品牌标志或吉祥物；遇到以品牌或角色为主题的案例，只借它的运动和技法。
- 灵枢的页面要套用 `references/lingshu.md` 的规则。新的 three.js 场景直接复用 `recipes/lingshu-three/three/stage.js` 的公共外壳，参照那里的三个场景写工厂函数（说明见 `recipes/README.md`）。

### 6. 沉淀
用户确认某个效果好用、要上线后，建议把它加进配方：按 `recipes/README.md` 末尾的模板写一条（效果、参数、代码位置、参考了哪些案例）。已安装的 skill 是只读的，所以要更新时先在工作区修改一份副本，重新打包，交给用户保存。

## 文件地图

| 文件 | 什么时候读 |
|---|---|
| `scripts/search.py` | 每次都用：检索、看全字段、下载封面 |
| `references/top-picks.md` | 想快速看某个用途的高分案例 |
| `references/lingshu.md` | 做灵枢医学数字教材的任何页面 |
| `references/licenses.md` | 要取代码或决定能不能用某个库之前 |
| `references/sources.md` | 要了解某个开源库（许可、技术栈、取代码方式、代表示例） |
| `references/prompt-craft.md` | 要写动效或短片的提示词，或把设计意图写成可交给其他模型的规格 |
| `recipes/README.md` | 灵枢已上线的 three.js 场景说明、接入方法，以及新配方模板 |
| `recipes/lingshu-three/` | 这三个场景的源码：公共外壳、three 类导出、三个场景、首屏 2D 降级与调度、身份色、两个组合式函数 |
| `index/*.jsonl`、`index/sources.json` | 检索脚本的数据；需要批量处理时直接读 |
| `references/credits.md` | 数据来源与致谢 |

## 几条底线
- 动效服务内容：文字、按钮、表单用普通网页实现，3D 和着色器只做背景与氛围。
- 默认尊重“减少动态效果”，离屏或页面隐藏时停绘，移动端减量。
- 许可不清楚时按 C 级处理，并告诉用户需要核实。
- 库里的信息截至 2026-10-12。库的维护状态、许可都可能变化；正式采用前重新确认一次。
