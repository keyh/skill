# 许可分级与用法

灵枢由出版社运营，属于商业用途。每条参考都带 `tier`，取代码前先看它。分级依据 2026-10-12 读到的许可原文；许可会变，正式采用前再确认一次。

## 三级

| 级别 | 含义 | 怎么用 |
|---|---|---|
| **A 可取代码** | MIT、Apache-2.0、zlib、Unlicense，或 GSAP 的免费商用条款 | 可以读源码、改写进项目；保留原版权声明（文件头注释或第三方声明清单） |
| **B 有条件可用** | 允许用在自家网站，但禁止再分发组件本身（Commons Clause 等）、需要署名（CC BY）、或需逐个仓库核对 | 可以用在灵枢网站；不要把源码收进 skill、模板、组件库或任何对外分发的东西；按要求署名 |
| **C 只看思路** | 非商用许可、没有许可证、版权归作者、来源存疑 | 只学手法和构图，自己重新实现；不复制代码、提示词原文或素材 |

three.js 官方示例全部是 A（MIT）。Opus 5.5 合集全部是 C：仓库本身是 MIT，但每条视频和提示词的权利归原作者，且没有源码。

## 各来源分级

- **A**：TresJS、pmndrs examples、postprocessing、TSL Textures、Paper Shaders、ShaderGradient、3d-force-graph、AntV G6、globe.gl、makio-meshline、Vanta.js、WebGL-Fluid-Simulation、程序化水墨组、OGL、curtains.js、lemo-opuscar、Inspira UI、Magic UI、motion-v、VueUse Motion、GSAP、Anime.js v4、transition.css、Animata、Scroll-driven Animations 演示、View Transitions 演示、Lenis、NumberFlow、Animate.css（仅 npm 4.1.1 版）
- **B**：Codrops、Bruno Simon folio、Vue Bits、React Bits、Aceternity UI（免费组件）、Uiverse、LottieFiles、Rive 社区文件
- **C**：Pavel Mazhuga lab、LYGIA、The Book of Shaders、Shadertoy、各类 AI 生成动画合集（含 awesome-opus5-5-videos、motionpromptgallery、opus-100-projects）、AI_Animation、motionsites 提示词、Awwwards、Land-book

## 容易踩的坑

- **LYGIA** 自 2022-09 起是非商用许可（商用仅 30 天试用）。噪声函数改用 three.js TSL 自带的噪声节点或 TSL Textures。
- **The Book of Shaders** 保留全部权利，代码不能搬进任何项目，只能学原理。
- **Shadertoy** 默认 CC BY-NC-SA 3.0，不能商用；只有作者在代码里明确声明 MIT / CC0 的才可以用。Inspira UI 里个别背景改编自 Shadertoy，用前看 credits。
- **Vue Bits / React Bits** 是 MIT + Commons Clause：网站可以商用，但禁止再分发组件本身，明确包括移植版。所以只记链接和取用命令（`npx jsrepo add https://vue-bits.dev/r/<Name>.json`）。
- **Animate.css** 的 GitHub 版是 Hippocratic 2.1（企业法务通常不接受），npm 的 4.1.1 版是 MIT。固定用 4.1.1。
- **Motion（motion.dev）**：163 个 Vue 示例中约 110 个是 Motion+ 付费内容；免费示例里也有几个要 `import "motion-plus"`。数字滚动用 NumberFlow，文字拆分用 GSAP SplitText 或 Anime.js。
- **GSAP**：2025 年起含全部插件免费商用（Webflow 自有条款，不是 OSI 开源许可）；唯一禁止的是做与 Webflow 竞争的无代码动画工具。出版社网站不受影响。
- **Codrops**：站点说默认 MIT，但各演示仓库差别很大，有的没有 LICENSE。逐个仓库看，没有 LICENSE 的按 C 处理。
- **Vanta.js**：MIT，但 2023-01 以后不再更新，按 three r134 写的。借视觉思路，用新版 three 重写。
- **Bruno Simon folio**：代码 MIT，但整站造型是作者的个人标识，只借技术模块（草地、风线、水面、雾），不照搬整体视觉。
- **LottieFiles**：免费动画是 Lottie Simple License，可商用；修改后的动画须按同样条款分发；在内部清单记下作者与链接。
- **Rive 社区文件**：CC BY 4.0，必须署名（作者、许可链接、是否修改），放在页脚或致谢页。
- **AI_Animation 仓库**里有一个名为“Pirated websites”的目录和一份无授权的动效包镜像，不要使用；只读作者原创的 skill 目录。
- **没有 LICENSE 的仓库**（opus-100-projects、Pavel Mazhuga lab 等）默认保留所有权利，只看思路。

## 通用做法

- 把采用的第三方代码记进项目的第三方声明清单（名称、版本、许可、链接）。
- 从参考作品里借的是手法，不是外观：不要复刻某个作品的整体样貌，不要使用受版权保护的角色、品牌标志或素材。
- 拿不准时按 C 处理，并告诉用户需要法务或作者确认。
