# 开源效果库目录（50 个来源）

调研日期 2026-10-12。许可证均读过原文；示例链接均请求过。`index/libraries.jsonl` 收录了这些来源里的 352 个具体示例（可用 `scripts/search.py --pool lib` 检索）。

许可分级的含义见 `licenses.md`。同一个来源在两组里都出现时（如 Codrops），分别列出。

## 目录

- **A 可取代码**：animata、animate-css、animejs-v4、gsap、inspira-ui、lenis、magic-ui、motion-vue、number-flow、scroll-driven-animations-style、transition-css、view-transitions-demos、vueuse-motion、ai-lemo-opuscar、antv-g6、curtainsjs、globe-gl、ink-wash-procedural、makio-meshline、ogl、paper-shaders、pmndrs-examples、pmndrs-postprocessing、shadergradient、tresjs、tsl-textures、vanta-js、vasturiano-3d-force-graph、webgl-fluid-simulation
- **B 可用但只放链接**：aceternity-ui、codrops、lottiefiles、react-bits、rive、uiverse、vue-bits、bruno-simon-folio、codrops
- **C 只看思路**：ai-animation-skills、awesome-opus5-5-videos、awwwards、land-book、motionsites-prompts、ai-model-video-collections、ai-motionpromptgallery、ai-opus-100-projects、book-of-shaders、lygia、pavel-mazhuga-lab、shadertoy

## A 可取代码

### Animata（`animata`，页面动效 / UI 组件）

- 链接：https://github.com/codse/animata · https://animata.design
- 许可：MIT；商用风险 low。MIT。README 称效果“搜集自互联网”后手工重写，个别效果可能有原作者，商用前可看组件页的 credit。
- 技术：React、Tailwind CSS v4、motion；Vue 版本：无，只有 React 版，没有 Vue 移植；多数效果是 Tailwind 加少量 motion，改写成 Vue 不难。
- 规模与更新：约 210 个组件，23 个分类：文字约 50、组件 68、卡片 55、按钮 33、背景 22、预加载 19、图表 12、Hero 10 等；2026-09-14（main 最后一次提交）
- 取代码：没有 CLI 注册表（/r/*.json 返回 404），直接复制源码。原始文件：https://raw.githubusercontent.com/codse/animata/main/animata/<category>/<slug>.tsx；文档：https://animata.design/docs/<category>/<slug>。
- 适用：文字动效、数据可视化、加载、滚动叙事、背景、卡片、首页Hero
- 简介：文字入场效果特别丰富，风格偏“发布会”般从容，还有不少小型图表动画和预加载。虽是 React，但实现简单，适合当作 Vue 改写的参考蓝本。
- 代表示例：`animata/mask-reveal-up` 遮罩内向上揭示；`animata/focus-blur-resolve` 对焦般变清晰；`animata/per-word-crossfade` 逐词淡入上移；`animata/ring-chart` 环形进度图

### Animate.css（`animate-css`，页面动效 / UI 组件）

- 链接：https://github.com/animate-css/animate.css · https://animate.style
- 许可：仓库 main 分支：Hippocratic License 2.1（伦理许可）；npm 包 animate.css@4.1.1 附带的 LICENSE 是 MIT；商用风险 medium。两份许可并存：GitHub 当前 LICENSE 是 Hippocratic 2.1，附加人权合规义务、海牙仲裁条款和赔偿责任，多数企业法务不接受；已发布的 npm 4.1.1 包（2020-09）附带 MIT。请固定使用 npm 或 unpkg 上的 4.1.1 副本，并保留其中的 MIT 声明，风险即降为低。
- 技术：纯 CSS；Vue 版本：有，纯 CSS 类名，配合 Vue <Transition> 的 enter-active-class 即可使用。
- 规模与更新：98 个动画（按入场、离场、强调等 18 个分组）；最后发版 4.1.1 于 2020-09-07；仓库最后一次提交 2024-03-02（基本不再维护）
- 取代码：npm i animate.css@4.1.1。单个动画：https://unpkg.com/animate.css@4.1.1/source/<group>/<name>.css，例如 fading_entrances/fadeInUp.css。
- 适用：卡片、转场、微交互、按钮
- 简介：最常见的 CSS 入场和强调动画合集，零依赖，旧内核也能用。许可有坑，务必取 npm 4.1.1 的 MIT 版本；动画偏通用，适合作为基础素材，不适合做主视觉。
- 代表示例：`animate-css/fadeinup` 淡入上移；`animate-css/fadein` 纯淡入；`animate-css/zoomin` 缩放弹出；`animate-css/flipinx` 沿横轴翻入

### Anime.js v4（`animejs-v4`，页面动效 / UI 组件）

- 链接：https://github.com/juliangarnier/anime · https://animejs.com
- 许可：MIT；商用风险 low。MIT，没有付费插件。
- 技术：原生 JS（ES 模块，可按需引入）；Vue 版本：有，没有 Vue 包，但与框架无关，在 onMounted 里调用即可。v4 内置 splitText、scrambleText、onScroll、draggable、createLayout（自动布局过渡）以及 SVG 描线、变形、路径运动。
- 规模与更新：仓库 examples/ 下 25 个示例目录（text 下另有 5 个子示例），文档按 Timeline、Text、Events/onScroll、SVG、Layout、Draggable 等模块组织；v4.5.0（npm 2026-08-17）；仓库最后一次提交 2026-08-09
- 取代码：npm i animejs。示例源码：https://raw.githubusercontent.com/juliangarnier/anime/master/examples/<name>/index.js（另有 index.html）。animejs.com/examples/* 现在都跳转回首页，不能直接链接，示例请看 GitHub；文档页如 https://animejs.com/documentation/text/splittext 可以访问。
- 适用：文字动效、数据可视化、滚动叙事、加载、微交互
- 简介：体积小、MIT 许可的全能动画库，v4 把文字拆分、滚动联动、布局过渡、SVG 描线都做进了内核。如果不想引入 GSAP 自有条款，这是最好的开源替代，适合知识矩阵、SVG 图表、文字小动效。
- 代表示例：`animejs-v4/svg-line-drawing` SVG 线稿逐笔描绘；`animejs-v4/split-effects` 字词行拆分入场；`animejs-v4/onscroll-sticky` 吸附区段内滚动同步；`animejs-v4/svg-graph` 折线图数据切换

### GSAP（含 ScrollTrigger、SplitText、Flip、DrawSVG 等全部插件）+ GSAP Demo Hub（`gsap`，页面动效 / UI 组件）

- 链接：https://github.com/greensock/GSAP · https://gsap.com （演示：https://demos.gsap.com）
- 许可：GSAP Standard “No Charge” License（Webflow 自有条款，2025-04-30 生效，2025-05-30 修订）；商用风险 low。Webflow 收购后 GSAP 100% 免费，包括原来的会员插件 SplitText、MorphSVG、ScrollSmoother、DrawSVG 等，商用也免费。禁止的用途只有一类：开发帮助用户无代码制作动画、与 Webflow 竞争的可视化工具。条款还说明 AI 生成 GSAP 代码不属于禁止用途。注意这不是 OSI 开源许可：Webflow 可以修改条款，但旧版本仍可按原条款使用；违约时许可可被终止。出版社网站使用没有障碍。Demo Hub 的示例托管在 CodePen，公开 Pen 默认 MIT。
- 技术：原生 JS（与框架无关）；Vue 版本：有，没有官方 Vue 包（npm 上不存在 @gsap/vue）。在 Vue 组件里用 onMounted 加 gsap.context()，onUnmounted 里调用 revert()。官方在 StackBlitz 提供 Vue 3 起步模板集：https://stackblitz.com/@gsap-dev/collections/gsap-vue3-starters。GSAP 支持旧浏览器，与灵枢工程的降级包兼容。
- 规模与更新：Demo Hub 共 78 个演示，全部是原生 JS。另按插件分 4 个官方 CodePen 合集：Scroll bNPYOw、Text ExBwoK、SVG NqewVd、Flip/Observer qOMVGv。；gsap 3.15.0 于 2026-04-13 发布
- 取代码：npm i gsap，所有插件都在包里，例如 gsap/ScrollTrigger、gsap/SplitText。演示页：https://demos.gsap.com/demo/<slug>/，页面数据里带 CodePen 链接。shell 访问 codepen.io 会返回 403，改用 https://cdpn.io/GreenSock/fullpage/<penId>，curl 可返回含 JS 和 CSS 的完整 HTML。
- 适用：滚动叙事、文字动效、转场、数据可视化、卡片、导航、首页Hero
- 简介：滚动叙事和文字逐行动画的行业标准，全部插件现已免费商用，且与框架无关、兼容旧内核，很适合灵枢这种既要 Vue 3 又要兼顾 360、QQ 浏览器的站点。官方 Demo Hub 示例质量高，按 ScrollTrigger、SplitText、Flip、SVG 分类查找即可。
- 代表示例：`gsap/responsive-line-splits-on-scroll` 按行升起的长文；`gsap/text-masking` 遮罩线下升起；`gsap/image-mask-on-scroll` 反向位移互相揭示；`gsap/pinned-panels-with-overscroll` 整屏面板逐个钉住

### Inspira UI（Aceternity UI / Magic UI 的 Vue 移植）（`inspira-ui`，页面动效 / UI 组件）

- 链接：https://github.com/unovue/inspira-ui · https://inspira-ui.com
- 许可：MIT；商用风险 low。MIT。README 说明已获 Aceternity UI 授权改编，约 43 篇文档注明来源 Aceternity、约 41 篇注明 Magic UI，其余来自社区和 ShaderToy 等，个别背景改编自 ShaderToy 着色器。用前看一眼组件文档里的 credits，ShaderToy 的作品默认许可不一定可商用。付费的 Inspira UI Pro（模板单买 29–79 美元，全访问包 249 美元）不在 MIT 范围内。
- 技术：Vue 3、Nuxt、Tailwind CSS v4、motion-v、shadcn-vue 注册表；Vue 版本：有，原生 Vue 3 和 Nuxt。v2 要求 Tailwind v4，Tailwind v3 项目用 v1.inspira-ui.com。Tailwind v4 要求 Chrome 111+ / Safari 16.4+，不支持灵枢工程要兼容的 360、QQ、X5 旧内核，需改写为普通 CSS。
- 规模与更新：仓库约 155 个组件，分 12 类：背景 27、文字 30+、卡片 10、可视化 15 等。文档站目前只上线约 116 页：Globe、NumberTicker、TextGenerateEffect、FileTree 等页面返回 404，但注册表 JSON 和 GitHub 源码都能拿到。；2026-09-18（main 最后一次提交）
- 取代码：CLI：npx shadcn-vue@latest add "https://registry.inspira-ui.com/<component-id>.json"。原始文件：https://raw.githubusercontent.com/unovue/inspira-ui/main/app/components/inspira/ui/<component-id>/<Name>.vue；文档 Markdown 在 content/en/2.components/<category>/<id>.md；示例在 app/components/inspira/examples/<id>/。文档页：https://inspira-ui.com/docs/en/components/<category>/<id>。全量清单：https://inspira-ui.com/llms.txt。
- 适用：首页Hero、背景、文字动效、卡片、滚动叙事、数据可视化、按钮、转场
- 简介：Vue 生态里最完整的 Aceternity UI / Magic UI 风格组件集，MIT 许可，可用 shadcn-vue 一键安装。时间线、追踪光束、连接光束、3D 书本等组件，直接对应教材沿革、长文阅读、平台生态图、教材封面这些场景。
- 代表示例：`inspira-ui/timeline` 吸顶年份时间线；`inspira-ui/book` 悬停微开的 3D 书；`inspira-ui/tracing-beam` 随滚动延伸的光束；`inspira-ui/animated-beam` 节点间流动光点

### Lenis（平滑滚动）（`lenis`，页面动效 / UI 组件）

- 链接：https://github.com/darkroomengineering/lenis · https://lenis.dev
- 许可：MIT；商用风险 low。MIT。
- 技术：原生 JS、Vue、Nuxt、React；Vue 版本：有，包内导出 lenis/vue 和 lenis/nuxt。Vue Bits 的 ScrollStack 就依赖它。可与 GSAP ScrollTrigger 配合使用。
- 规模与更新：1 个核心库，附 snap（分屏吸附）扩展；lenis 1.3.26 于 2026-09-18 发布；仓库最后一次提交 2026-10-01
- 取代码：npm i lenis。Vue 用法：https://raw.githubusercontent.com/darkroomengineering/lenis/main/packages/vue/README.md。
- 适用：平滑滚动、滚动叙事
- 简介：滚动叙事页面常用的平滑滚动底座，让滚动联动动画更顺滑。对阅读类页面要克制使用：教材正文区建议保留原生滚动，只在首页叙事楼层启用，并尊重系统的“减少动态效果”设置。
- 代表示例：`lenis/official-demo` 整站平滑滚动；`lenis/lenis-snap` 滚停吸附分区；`lenis/vue-integration` Vue 中挂载 Lenis

### Magic UI（`magic-ui`，页面动效 / UI 组件）

- 链接：https://github.com/magicuidesign/magicui · https://magicui.design
- 许可：MIT；商用风险 low。开源组件为 MIT。付费的 Magic UI Pro（pro.magicui.design）模板另有条款，不要混用。
- 技术：React、Tailwind CSS、motion（Framer Motion）、shadcn 注册表；Vue 版本：有，官方只有 React 版。约一半组件已由 Inspira UI 移植成 Vue，如 Blur Fade（对应 Blur Reveal）、Animated Beam、Number Ticker、File Tree、Globe、Border Beam、Flickering Grid。
- 规模与更新：79 个注册表组件（apps/www/registry/magicui/*.tsx）；2026-10-11（main 最后一次提交）
- 取代码：CLI：npx shadcn@latest add @magicui/<slug>。注册表 JSON：https://magicui.design/r/<slug>.json，内嵌源码。原始文件：https://raw.githubusercontent.com/magicuidesign/magicui/main/apps/www/registry/magicui/<slug>.tsx。仓库自带一份 Claude skill：skills/magic-ui/SKILL.md。
- 适用：文字动效、数据可视化、背景、按钮、滚动叙事、数字计数
- 简介：偏产品官网风格的 React 动效组件，MIT 许可，组件克制、易读，很多已有 Vue 移植。荧光笔划重点、点阵地图、环绕轨道、文件树这几类，对出版和教育类页面尤其实用。
- 代表示例：`magic-ui/highlighter` 马克笔手绘划重点；`magic-ui/number-ticker` 数字滚动到目标；`magic-ui/orbiting-circles` 图标环绕中心；`magic-ui/dotted-map` 点阵地图标注

### Motion for Vue（motion-v）+ motion.dev 官方示例（`motion-vue`，页面动效 / UI 组件）

- 链接：https://github.com/motiondivision/motion-vue · https://motion.dev/docs/vue
- 许可：MIT（motion-v 和 motion 库）；Motion+ 付费示例和组件另行授权；商用风险 low。库本身是 MIT，Vue Bits 和 Inspira UI 也用它。motion.dev 上 163 个 Vue 示例中，只有 53 个公开源码，其余 110 个属 Motion+，需付费：Solo 一次性买断，Team 按年订阅。另外 split-text、split-text-wavy、number-formatting 这 3 个“免费”示例要导入 motion-plus 包，等同付费功能。AnimateNumber、Ticker、Typewriter、ScrambleText、splitText、Carousel、Cursor 都是 Motion+ 专属。
- 技术：Vue 3、Nuxt、（同源）原生 JS 版 motion、React 版 motion/react；Vue 版本：有，原生 Vue 3 组件和组合式函数：motion.div、AnimatePresence、layout / layoutId、useScroll、useInView、useTransform、AnimateView 等。motion-v 2.6.0 于 2026-10-05 发布。
- 规模与更新：motion.dev 共 163 个 Vue 示例：53 个公开源码，110 个属 Motion+。仓库 playground 另有 44 个 Vue 演示页。；motion-v 2.6.0 于 2026-10-05 发布（仓库同日有提交）；motion 14.1.0 于 2026-10-09 发布
- 取代码：npm i motion-v。示例页：https://motion.dev/examples/vue-<slug>，免费示例的源码直接写在 HTML 里，curl 可抓；WebFetch 会被 robots.txt 拦截。仓库演示：https://raw.githubusercontent.com/motiondivision/motion-vue/master/playground/vite/src/views/<file>.vue。示例总表：https://motion.dev/examples?platform=vue。
- 适用：滚动叙事、转场、卡片、微交互、导航、加载
- 简介：Vue 3 最主流的声明式动画引擎，支持弹簧、布局动画、共享元素过渡、手势和滚动联动，是 Vue Bits 和 Inspira UI 的底层。官方免费示例足够覆盖阅读进度、视差、卡片到详情的共享过渡、骨架屏渐显等常用模式。
- 代表示例：`motion-vue/shared-layout-animation` 共享元素平滑过渡；`motion-vue/path-drawing` SVG 路径依次描绘；`motion-vue/scroll-linked` 滚动联动进度条；`motion-vue/parallax` 滚动视差

### NumberFlow（@number-flow/vue）（`number-flow`，页面动效 / UI 组件）

- 链接：https://github.com/barvian/number-flow · https://number-flow.barvian.me/vue
- 许可：MIT；商用风险 low。MIT。
- 技术：Vue、React、Svelte、Web Components；Vue 版本：有，官方 @number-flow/vue 0.5.2（2026-07-18），提供 NumberFlow 和 NumberFlowGroup 组件。
- 规模与更新：1 个组件，另有分组组件 NumberFlowGroup；仓库最后一次提交 2026-09-20；@number-flow/vue 0.5.2 于 2026-07-18 发布
- 取代码：npm i @number-flow/vue。源码：https://raw.githubusercontent.com/barvian/number-flow/main/packages/vue/src/index.vue。
- 适用：数字计数、数据可视化、微交互
- 简介：数字变化时逐位滚动过渡，基于 Intl.NumberFormat 支持本地化格式，字宽等宽不跳动。适合数据带、价格、题量、掌握度等需要“数字动起来”又要保持可读的地方，可替代 Motion+ 付费的 AnimateNumber。
- 代表示例：`number-flow/basic-usage` 机械计数器式翻滚；`number-flow/format` 本地化数字格式；`number-flow/numberflowgroup` 多数字同步过渡；`number-flow/reduced-motion` 遵循减少动态效果

### scroll-driven-animations.style（CSS 滚动驱动动画演示，Chrome DevRel Bramus）（`scroll-driven-animations-style`，页面动效 / UI 组件）

- 链接：（无站点源码仓库，代码直接 view-source；polyfill：https://github.com/flackr/scroll-timeline） · https://scroll-driven-animations.style
- 许可：Apache-2.0（站点页脚声明）；商用风险 low。Apache-2.0，可商用，保留许可声明即可。
- 技术：纯 CSS（animation-timeline / view-timeline）、WAAPI 版 JS；Vue 版本：有，纯 CSS，与框架无关。浏览器支持（MDN BCD 8.1.5）：animation-timeline 需 Chrome 115+、Safari 26+，Firefox 仅预览版。灵枢要兼容旧内核，只能做渐进增强：用 @supports (animation-timeline: view()) 包裹，不支持时显示静态结果或改走 GSAP。
- 规模与更新：14 个演示，多数同时有纯 CSS 版和 WAAPI 版；站点 2026-10 在线（页面未标日期）
- 取代码：curl https://scroll-driven-animations.style/demos/<name>/css/（JS 版把 css 换成 waapi），代码都在页面里，无构建步骤。
- 适用：滚动叙事、导航、卡片、转场
- 简介：Chrome 团队维护的 CSS 原生滚动动画示例，零 JS，性能最好。适合做阅读进度条、吸顶头部收缩、图片揭示这类小效果，但必须作为渐进增强，并为旧内核准备后备方案。
- 代表示例：`scroll-driven-animations-style/reading-progress-indicator` 纯 CSS 阅读进度条；`scroll-driven-animations-style/cover-card-to-fixed-header` 封面收缩成吸顶头部；`scroll-driven-animations-style/stacking-cards` 卡片层叠覆盖；`scroll-driven-animations-style/horizontal-scroll-section` 横向滚动区段

### transition.css（transition.style，clip-path 转场合集）（`transition-css`，页面动效 / UI 组件）

- 链接：https://github.com/argyleink/transition.css · https://www.transition.style
- 许可：Apache-2.0（LICENSE 文件）；package.json 标为 ISC；商用风险 low。两种都是宽松许可，按 Apache-2.0 保留声明即可。作者是 Google Chrome 团队的 Adam Argyle。
- 技术：纯 CSS（clip-path + @property）；Vue 版本：有，纯 CSS，用 transition-style="in:wipe:up" 这类属性触发，可配合 Vue <Transition> 或 View Transitions。
- 规模与更新：48 个 clip-path 转场：圆形 12、方形 12、擦除 18、多边形 6；2025-06-16（transition-style 0.1.4 发版，仓库同日有提交）
- 取代码：npm i transition-style。单个转场：https://raw.githubusercontent.com/argyleink/transition.css/main/src/<circles|squares|wipes|polygons>/<name>.css。
- 适用：转场、首页Hero、卡片
- 简介：一组用 clip-path 实现的入场和离场转场，轻量、无 JS，适合页面切换、图片揭示、楼层进入。“电影式擦入”“自上而下擦入”有卷轴展开的意味，契合书卷气质。
- 代表示例：`transition-css/wipes-in-top` 竖轴画卷展开；`transition-css/circles-in-center` 中心圆形扩散；`transition-css/circles-in-hesitate` 停顿一拍的圆形揭示；`transition-css/polygons-diamond-in-center` 菱形窗棂展开

### View Transitions 官方演示（view-transitions.chrome.dev）（`view-transitions-demos`，页面动效 / UI 组件）

- 链接：https://github.com/bramus/view-transitions-demos · https://view-transitions.chrome.dev
- 许可：Apache-2.0；商用风险 low。Apache-2.0，可商用。
- 技术：原生 JS、CSS（::view-transition-*、@view-transition）；Vue 版本：有，与框架无关。在 vue-router 切换时调用 document.startViewTransition 即可做 SPA 共享元素过渡。浏览器支持（MDN BCD）：同文档版需 Chrome 111+、Safari 18+、Firefox 144+；跨文档 @view-transition 需 Chrome 126+、Safari 18.2+，Firefox 不支持。灵枢需做特性检测，不支持时直接切换。
- 规模与更新：38 个演示页，涵盖 SPA、MPA、Navigation API、排序列表、视频等；2026-08-17（main 最后一次提交）
- 取代码：原始文件：https://raw.githubusercontent.com/bramus/view-transitions-demos/main/src/<path>/index.html；在线：https://view-transitions.chrome.dev/<path>/。
- 适用：转场、卡片、导航
- 简介：浏览器原生页面转场的权威示例。切换栏目、列表到详情、翻页这类过渡可以不引入动画库，用原生 API 完成，适合教材库进入详情、阅读器翻页等场景，并做好降级。
- 代表示例：`view-transitions-demos/profiles` 封面飞到详情页；`view-transitions-demos/cards` 增删卡片平滑补位；`view-transitions-demos/pagination` 整页左右滑动翻页；`view-transitions-demos/circle` 点击处圆形扩散切换

### VueUse Motion（@vueuse/motion）（`vueuse-motion`，页面动效 / UI 组件）

- 链接：https://github.com/vueuse/motion · https://motion.vueuse.org
- 许可：MIT；商用风险 low。MIT。主要风险是维护停滞：最后一次发版是 2025-03 的 3.0.3，底层依赖 popmotion 也早已停更。新代码建议改用 motion-v。
- 技术：Vue 3、Nuxt；Vue 版本：有，原生 Vue 指令 v-motion 和组合式函数 useMotion，可用 v-motion-slide-visible-once-bottom 这类预设一行写完入场动画。
- 规模与更新：30 个预设：fade、pop、roll、slide 四族，各有普通、Visible、VisibleOnce 版本；2025-03-11（main 最后一次提交）；npm 3.0.3 于 2025-03-10 发布
- 取代码：npm i @vueuse/motion。预设源码：https://raw.githubusercontent.com/vueuse/motion/main/src/presets/<fade|pop|roll|slide>.ts。
- 适用：滚动叙事、卡片、文字动效
- 简介：轻量的 Vue 指令式动画，用预设快速做“进入视口淡入上移”很省事。但已停更一年半，只适合维护旧代码或做极简入场；新功能请用 motion-v。
- 代表示例：`vueuse-motion/slide` 四向滑入参数；`vueuse-motion/presets` 三十种入场预设；`vueuse-motion/directive-usage` 模板声明式动画；`vueuse-motion/motion-properties` 动画属性与过渡参数

### Lemo-Opuscar（43 种影片风格提示词 + Opus 5.5 代码短片，含源码）（`ai-lemo-opuscar`，3D / WebGL / 着色器）

- 链接：https://github.com/lemomo-ai/lemo-opuscar · https://lemomo-ai.github.io/lemo-opuscar/
- 许可：MIT（README 写明；样片中的第三方素材，如字体，沿用各自授权，见各样片 CREDITS）；商用风险 low。代码和风格说明都是 MIT。字体为 SIL OFL（Ma Shan Zheng、Cormorant 等），可以商用；配乐和配音看各样片的 CREDITS。成片里的故事和角色是作者原创，不要直接拿来用。
- 技术：Canvas 2D、WebGL、three.js（部分风格）、Python 合成音乐/配音
- 规模与更新：43 种风格（styles/ 目录，每种有 STYLE.md 风格提示词、DEMO.md、完整 demo 源码和成片）；另有 OPUSCAR 98 列表收录 98 种风格的静帧与提示词；2026-10-10
- 取代码：https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/main/styles/<风格>/STYLE.md ；源码 https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/main/styles/<风格>/demo/<文件>.js ；成片 https://github.com/lemomo-ai/lemo-opuscar/releases/download/films/<风格>.mp4
- 适用：讲解动画、首页Hero背景、转场、加载动画
- 简介：这是给编程 agent 用的『影片风格包』，每种风格都有可复用的长提示词和一支完全用代码画出来的样片。ink-wash（水墨）的 STYLE.md 把墨分五色的透明度、留白、只用一处朱印、宣纸色值都写成了规范，可以直接作为平台水墨视觉的提示词底稿。另有剪纸、皮影、纸灯笼、水彩、版画等风格。
- 代表示例：`ai-lemo-opuscar/ink-wash` 毛笔飞白写『水』；`ai-lemo-opuscar/watercolor` 水彩植物与地图；`ai-lemo-opuscar/shadow-puppet` 暖光透背的皮影；`ai-lemo-opuscar/engraving` 铜版雕刻排线

### AntV G6 v5（蚂蚁集团图可视化）（`antv-g6`，3D / WebGL / 着色器）

- 链接：https://github.com/antvis/G6 · https://g6.antv.antgroup.com/zh/examples
- 许可：MIT；商用风险 low。MIT，国内广泛商用，中文文档完整。
- 技术：Canvas、SVG、WebGL（@antv/g 渲染器）、TypeScript、3D 扩展 @antv/g6-extension-3d
- 规模与更新：官网示例 179 个 demo 文件（布局、元素、插件、场景案例等分类）；2026-10-10（v5 分支；@antv/g6 5.1.1；g6-extension-3d 0.1.23）
- 取代码：https://raw.githubusercontent.com/antvis/G6/v5/packages/site/examples/<分类>/<子类>/demo/<名称>.js （默认分支是 v5）；注意官网是单页应用，任意路径都返回 200，要以仓库里的 demo 文件名为准
- 适用：知识图谱、数据可视化、讲解动画
- 简介：G6 是国内最完整的 2D 图可视化方案，思维导图、径向树、气泡集合、鱼眼放大这些功能都是现成的，中文文档和案例很多。可以和 3d-force-graph 分工：严肃、可读、可打印的知识结构用 G6，氛围化的 3D 图谱用 3d-force-graph。
- 代表示例：`antv-g6/mindmap` 左右展开思维导图；`antv-g6/radial-dendrogram` 径向放射树图；`antv-g6/bubble-sets` 柔和气泡分组；`antv-g6/fisheye` 局部放大鱼眼

### curtains.js / gpu-curtains（DOM 同步的 WebGL/WebGPU 平面）（`curtainsjs`，3D / WebGL / 着色器）

- 链接：https://github.com/martinlaxenaire/curtainsjs · https://www.curtainsjs.com/
- 许可：MIT（curtains.js 与 gpu-curtains 都是）；商用风险 low。MIT。curtains.js 已进入维护期，新项目可以看作者的 WebGPU 版本 gpu-curtains（MIT）。
- 技术：raw WebGL（curtains.js）、WebGPU/WGSL（gpu-curtains）、vanilla JS、GSAP 示例
- 规模与更新：curtains.js 约 21 个示例；gpu-curtains 约 43 个示例；curtains.js 2025-04-03（v8.1.6）；gpu-curtains 2026-03-24（v0.16.3）
- 取代码：https://raw.githubusercontent.com/martinlaxenaire/curtainsjs/master/examples/<名称>/index.html ；https://raw.githubusercontent.com/martinlaxenaire/gpu-curtains/main/examples/<名称>/index.html
- 适用：转场、教材画廊、首页Hero背景
- 简介：它会把页面里的 img/video 变成跟 CSS 布局同步的 WebGL 平面，适合在常规 Vue 页面上给教材封面、图片加滚动弯曲、悬停扭曲、切换转场，不必整页改成 3D。
- 代表示例：`curtainsjs/multiple-planes-scroll-effect` 滚速弯曲的图片；`curtainsjs/ping-pong-flowmap` 逐渐平复的流动痕；`curtainsjs/post-processing-displacement` 整页位移波纹；`curtainsjs/gpu-curtains-slideshow` 图片轮播位移转场

### globe.gl（vasturiano）（`globe-gl`，3D / WebGL / 着色器）

- 链接：https://github.com/vasturiano/globe.gl · https://globe.gl/
- 许可：MIT；商用风险 low。MIT。注意部分示例使用 NASA 等地球贴图，要单独核对来源；国界数据涉及地图审图要求，面向国内公开发布时要用合规底图。
- 技术：three.js、WebGL、three-globe、vanilla JS
- 规模与更新：约 29 个示例（弧线、热力、六边形、城市标签、昼夜、云层等）；轻量替代 shuding/cobe（MIT，约 5KB，v2.0.1，2026-09-22）；2026-08-22（v2.46.2；peer three >=0.179）
- 取代码：https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/<名称>/index.html ；npm i globe.gl
- 适用：首页Hero背景、数据可视化、讲解动画
- 简介：globe.gl 是 3D 地球可视化组件，适合『中医药国际传播』『合作院校分布』这类内容。弧线和镂空地球风格克制。如果只想要一个点阵小地球做装饰，可以改用更轻的 cobe。
- 代表示例：`globe-gl/random-arcs` 地球上的跳动弧线；`globe-gl/hollow-globe` 镂空线框地球；`globe-gl/cobe` 5KB 点阵小地球；`globe-gl/hexed-polygons` 六边形陆地

### 程序化水墨/工笔（{Shan, Shui}*、Nonflowers、inkwash 等）（`ink-wash-procedural`，3D / WebGL / 着色器）

- 链接：https://github.com/LingDong-/shan-shui-inf · https://lingdong-.github.io/shan-shui-inf/
- 许可：MIT（shan-shui-inf、nonflowers、chinatian2000-png/inkwash、mattatz/THREE.Watercolor、madblade/brush-renderer 都已逐个核对为 MIT）；商用风险 low。代码都是 MIT。LingDong 的作品辨识度很高，直接照搬整体画风会显得像抄袭，建议借鉴算法后重新做构图和配色。antonysze/Chinese-Painting-Shader 没有 LICENSE，不要用。
- 技术：SVG、Canvas 2D、vanilla JS、three.js 后期（Watercolor、brush-renderer 为旧版 three）
- 规模与更新：5 个可用项目：shan-shui-inf（2018）、nonflowers（2018）、inkwash（2026，约 300 行）、THREE.Watercolor（2015）、brush-renderer（2021）；inkwash 2026-10-09；shan-shui-inf 2018-12-10、nonflowers 2018-12-14（已不维护但可运行）；THREE.Watercolor 2015-07；brush-renderer 2021-01（three ^0.124）
- 取代码：https://raw.githubusercontent.com/LingDong-/shan-shui-inf/master/index.html ；https://raw.githubusercontent.com/LingDong-/nonflowers/master/main.js ；https://raw.githubusercontent.com/chinatian2000-png/inkwash/main/src/inkwash.js ；https://raw.githubusercontent.com/mattatz/THREE.Watercolor/master/WatercolorPass.js 。注意：lingdong-.github.io 在本环境 shell 被代理拒绝（502），浏览器可访问，README 另有 glitch 备用链接
- 适用：首页Hero背景、登录背景、加载动画、讲解动画、教材封面
- 简介：这是本平台最对味的一类：不用 AI 和图片，纯算法画出山水长卷、工笔花卉和水墨山峦。shan-shui-inf 能无限横向生成宋元山水，nonflowers 能生成工笔风的虚构花卉，用来做本草插画的装饰非常合适。inkwash 是 2026 年的新项目，用 fBm 加等值线画淡墨山峦，作者把试过的 12 种架构和失败原因都写在了 README 里，可以直接当学习材料。
- 代表示例：`ink-wash-procedural/inkwash-seed-7` 层叠淡墨远山；`ink-wash-procedural/shan-shui` 无限山水长卷；`ink-wash-procedural/nonflowers` 程序生成工笔花；`ink-wash-procedural/three-watercolor` 水彩晕染后期

### Makio MeshLine（WebGPU/TSL 宽线条库）（`makio-meshline`，3D / WebGL / 着色器）

- 链接：https://github.com/Makio64/makio-meshline · https://meshline-demo.makio.io/
- 许可：MIT；商用风险 low。MIT。demo 中的雕塑模型（Venus/David）另有来源，不要直接搬用。
- 技术：three.js WebGPURenderer、TSL、ES modules
- 规模与更新：14 个 demo（basic、waves、follow、vertex-colors、gpu-circle、gpu-instance、shadow、sandbox、ricefield、drawlines、baguettes、venus-and-david、bamboooo、laser-heist）；2026-04-28（npm makio-meshline 1.4.0）
- 取代码：https://raw.githubusercontent.com/Makio64/makio-meshline/main/demo/src/demos/<文件>.js （id 与文件名的对应见 demo/src/demoMeta.js）；demo 地址 https://meshline-demo.makio.io/examples/<id>（单页应用，任意 id 都返回 200）
- 适用：首页Hero背景、讲解动画、转场、加载动画
- 简介：这是给 three.js WebGPU 渲染器用的现代宽线条库，支持渐变、虚线、GPU 位置和实例化。它的『竹林』『稻田』两个 demo 本身就有东方田园意境，『画线』『波浪线』适合做书法笔势或经络走向的动态描线。
- 代表示例：`makio-meshline/bamboooo` 实例化线条竹林；`makio-meshline/waves` 平行线正弦波；`makio-meshline/rice-field` 风中稻田涟漪；`makio-meshline/draw-lines` 鼠标绘制宽线

### OGL（极简 WebGL 库）（`ogl`，3D / WebGL / 着色器）

- 链接：https://github.com/oframe/ogl · https://oframe.github.io/ogl/
- 许可：Unlicense（package.json/npm 声明；仓库根目录没有 LICENSE 文件，README 徽章链接 404）；商用风险 low。Unlicense 相当于放弃版权，商用没有障碍；只是仓库缺 LICENSE 文件，属于文档瑕疵。
- 技术：raw WebGL、GLSL、ES modules（零依赖）
- 规模与更新：48 个示例（examples/*.html）；2025-04-13（最后提交；npm 1.0.11 于 2025-01-27）——维护缓慢
- 取代码：https://raw.githubusercontent.com/oframe/ogl/master/examples/<名称>.html ；在线 https://oframe.github.io/ogl/examples/?src=<名称>.html
- 适用：登录背景、首页Hero背景、转场、文字标题
- 简介：OGL 是 API 接近 three.js 的轻量 WebGL 库，体积很小，适合不想加载完整 three 的登录页。它的鼠标 flowmap、流体扭曲后期、MSDF 文字几个示例思路清晰，也方便移植到 three 的 ShaderMaterial。
- 代表示例：`ogl/mouse-flowmap` 鼠标水波拖拽图片；`ogl/post-fluid-distortion` 全屏流体扭曲；`ogl/msdf-text` 距离场汉字标题；`ogl/polylines` 飘动的彩色丝带

### Paper Shaders（paper.design）（`paper-shaders`，3D / WebGL / 着色器）

- 链接：https://github.com/paper-design/shaders · https://shaders.paper.design/
- 许可：Apache License 2.0；商用风险 low。Apache-2.0，README 明确写可用于商业网站且不要求可见署名；只有把代码作为另一个着色器库再分发时，才需要保留 LICENSE/NOTICE。
- 技术：GLSL、WebGL2、vanilla JS（零依赖）、React
- 规模与更新：30 个着色器（mesh-gradient、grain-gradient、paper-texture、neuro-noise、smoke-ring、god-rays、water、warp、metaballs、dithering 等）；2026-09-17（@paper-design/shaders 0.0.81；官方尚无 Vue 包，用 vanilla 包即可）
- 取代码：https://raw.githubusercontent.com/paper-design/shaders/main/packages/shaders/src/shaders/<名称>.ts ；npm i @paper-design/shaders（vanilla，零依赖，可在 Vue onMounted 中挂到 canvas）
- 适用：首页Hero背景、登录背景、AI助手形象、加载动画
- 简介：这是一组可调参数的全屏 canvas 着色器，零依赖、体积小，不需要加载 three.js，适合登录页这类轻量场景。纸张纹理、颗粒渐变、神经丝状噪声、烟环几种能营造安静、高级的学术氛围。
- 代表示例：`paper-shaders/paper-texture` 宣纸般的纸纹；`paper-shaders/grain-gradient` 颗粒渐变流动；`paper-shaders/mesh-gradient` 丝绸般网格渐变；`paper-shaders/neuro-noise` 发光神经细丝

### pmndrs / React Three Fiber 示例库（含 drei 文档）（`pmndrs-examples`，3D / WebGL / 着色器）

- 链接：https://github.com/pmndrs/examples · https://pmndrs.github.io/examples/
- 许可：MIT（示例仓库）；drei 同为 MIT；商用风险 low。代码为 MIT。每个示例的 pmndrs.json 里有 assets 字段，列出第三方模型/贴图的来源和许可，部分为 CC0，部分未注明，商用前要逐个核对。
- 技术：React、React Three Fiber、drei、react-postprocessing、three.js、GLSL
- 规模与更新：199 个示例（examples/ 目录）；目录清单见 https://pmndrs.github.io/examples/llms.txt；2026-10-11（examples）；react-three-fiber 2026-10-10；drei 2026-09-30
- 取代码：https://raw.githubusercontent.com/pmndrs/examples/main/examples/<名称>/src/App.tsx （另有 src/*.tsx、thumbnail.webp、pmndrs.json）；或 npx degit pmndrs/examples/examples/<名称>；drei 源码 https://raw.githubusercontent.com/pmndrs/drei/master/src/core/<组件>.tsx。迁移到 Vue 时用 TresJS/cientos 的对应组件。
- 适用：首页Hero背景、讲解动画、知识图谱、转场、数据可视化
- 简介：这是最大的 R3F 官方示例库，每个示例都能独立运行，带缩略图和元数据，适合按『想要的画面』检索灵感。示例基于 React，本平台需要改写成 TresJS，但着色器和场景结构可以直接借用。适合学术气质的主要有粒子景深、版画/油画后期、节点贝塞尔连线、HTML 标注这几类。
- 代表示例：`pmndrs-examples/gpgpu-curl-noise-dof` 卷曲噪声粒子云；`pmndrs-examples/kuwahara` 油画笔触重绘；`pmndrs-examples/bezier-curves-nodes` 虚线贝塞尔节点图；`pmndrs-examples/clouds` 柔软体积云

### postprocessing（pmndrs，vanilla three.js 后期库）+ react-postprocessing 自定义效果（`pmndrs-postprocessing`，3D / WebGL / 着色器）

- 链接：https://github.com/pmndrs/postprocessing · https://pmndrs.github.io/postprocessing/public/demo/
- 许可：zlib License（postprocessing）；react-postprocessing 为 MIT；商用风险 low。zlib 允许商用，只要求不冒称原作者、修改版要标明修改、保留许可声明。react-postprocessing 的 Kuwahara/Linocut/Water 是 MIT 自定义着色器，可移植。
- 技术：three.js、GLSL、vanilla JS、React（react-postprocessing）
- 规模与更新：vanilla 约 33 个效果（Bloom、GodRays、DepthOfField、TiltShift、Noise、Vignette、LUT、SSAO 等）；react-postprocessing 38 个效果组件；2026-09-09（postprocessing v6.39.5，peer three >=0.168 <0.187，兼容 0.185）；react-postprocessing 2026-10-11
- 取代码：https://raw.githubusercontent.com/pmndrs/postprocessing/main/src/effects/<Name>Effect.js ；React 版自定义效果 https://raw.githubusercontent.com/pmndrs/react-postprocessing/master/src/effects/<Name>.tsx ；npm i postprocessing（Vue+three 可直接用）
- 适用：首页Hero背景、登录背景、讲解动画、转场
- 简介：这是 three.js 生态的标准后期库，不依赖 React，可以直接装进 Vue3 + three 0.185 项目。辉光、体积光、景深、移轴、颗粒噪点、暗角这些『电影感』效果都在这里。react-postprocessing 额外写了 Kuwahara 油画、Linocut 版画、Water 水波等风格化着色器，适合做手绘/版画风格。
- 代表示例：`pmndrs-postprocessing/linocut` 古籍刻本式版画；`pmndrs-postprocessing/bloomeffect` 高亮柔和辉光；`pmndrs-postprocessing/godrayseffect` 放射光丝；`pmndrs-postprocessing/kuwahara` 油画水粉笔触

### ShaderGradient（ruucm，含新发布的 Vue 包）（`shadergradient`，3D / WebGL / 着色器）

- 链接：https://github.com/ruucm/shadergradient · https://www.shadergradient.co/customize
- 许可：MIT（README 与各 package.json 声明；仓库根目录无独立 LICENSE 文件）；商用风险 low。MIT。根目录缺少 LICENSE 文件，只是文档层面的小瑕疵；@shadergradient/vue 才 0.1.0 版，API 还可能变。
- 技术：three.js、R3F（React 包）、TresJS（Vue 包）、GLSL
- 规模与更新：10 个官方预设（Halo、Pensive、Mint、Interstella、Nighty night、Viola、Universe、Sunset、Mandarin、Cotton Candy）+ 可视化编辑器；2026-09-23（@shadergradient/react 2.4.24；@shadergradient/vue 0.1.0 于 2026-09-23 发布到 npm，基于 @tresjs/core ^5、three>=0.180）
- 取代码：https://raw.githubusercontent.com/ruucm/shadergradient/main/packages/shadergradient-vue/src/presets.ts ；Vue 包源码 https://raw.githubusercontent.com/ruucm/shadergradient/main/packages/shadergradient-vue/src/... ；在线编辑器导出 URL 参数即为配置
- 适用：首页Hero背景、登录背景、转场
- 简介：ShaderGradient 在 3D 平面或球体上做流动渐变，可以加颗粒，编辑器可视化调参后导出配置。2026-09 新出的 Vue 包基于 TresJS，可以直接放进本平台。缺点是风格偏『科技公司官网』，要配克制的传统色才不显轻浮。
- 代表示例：`shadergradient/pensive` 低饱和起伏平面；`shadergradient/halo` 中心光晕球面渐变；`shadergradient/vue-tresjs` Vue 版渐变组件；`shadergradient/nighty-night-universe` 夜空式深色渐变

### TresJS（Vue 3 版 three.js：core + cientos + post-processing + Lab）（`tresjs`，3D / WebGL / 着色器）

- 链接：https://github.com/Tresjs/tres · https://lab.tresjs.org/
- 许可：MIT；商用风险 low。MIT，保留版权声明即可。Lab 实验中个别模型/贴图可能另有来源，搬运前看对应实验的 content/experiments/<id>.md。
- 技术：Vue 3、three.js、TresJS、GLSL、TSL/WebGPU、Nuxt
- 规模与更新：Lab 37 个实验；cientos 组件库（Smoke、Sparkles、MeshGlass/Transmission/Wobble 材质、HTML、Bezier 线等）；post-processing 含 Bloom/GodRays/DOF/TiltShift/Kuwahara/Linocut；2026-10-09（monorepo 最后提交；@tresjs/core 5.9.3、cientos 5.9.3、post-processing 3.10.0；monorepo 使用 three ^0.186，peer three>=0.133）
- 取代码：git clone --depth 1 https://github.com/Tresjs/tres ；单文件：https://raw.githubusercontent.com/Tresjs/tres/main/apps/lab/app/components/<实验id>/<文件> ；组件：https://raw.githubusercontent.com/Tresjs/tres/main/packages/cientos/src/core/... ；后期：https://raw.githubusercontent.com/Tresjs/tres/main/packages/postprocessing/src/core/pmndrs/<Effect>Pmndrs.vue 。注意：独立仓库 Tresjs/cientos 已归档并迁入 monorepo，旧仓库 Tresjs/lab 自 2025-09 停更。
- 适用：首页Hero背景、登录背景、AI助手形象、讲解动画、转场、加载动画
- 简介：本平台是 Vue 3 + three.js，TresJS 是能直接拿来用的声明式封装，写法与 R3F 类似，所以 pmndrs 生态的思路基本都能迁移过来。Lab 里的烟雾、粒子变形、近邻连线粒子等实验全部是 Vue SFC 源码，可以直接参考。post-processing 已经把 pmndrs 的 Kuwahara（油画笔触）和 Linocut（版画）移植成 Vue 组件。
- 代表示例：`tresjs/coffee-smoke` 袅袅升起的热气；`tresjs/particles-morphing` 粒子聚散变形；`tresjs/grainy-liquid` 颗粒质感液态团；`tresjs/cientos-smoke-sparkles` 烟雾片与闪烁微粒

### TSL Textures（Pavel Boytchev）（`tsl-textures`，3D / WebGL / 着色器）

- 链接：https://github.com/boytchev/tsl-textures · https://boytchev.github.io/tsl-textures/
- 许可：MIT；商用风险 low。MIT，纯程序化生成，不依赖任何图片素材。
- 技术：three.js、TSL、WebGPU/WebGL2 (three.webgpu)、ES modules
- 规模与更新：约 50 个程序化 TSL 纹理（src/ 下 55 个文件，含工具函数）+ 12 个组合示例；2026-09-09（v3.0.5；在线 demo 使用 three@0.183 three.webgpu）
- 取代码：https://raw.githubusercontent.com/boytchev/tsl-textures/main/src/<纹理名>.js ；文档 https://boytchev.github.io/tsl-textures/docs/<纹理名>.html ；在线调参 https://boytchev.github.io/tsl-textures/online/<纹理名>.html ；预览图 https://raw.githubusercontent.com/boytchev/tsl-textures/main/docs/images/<纹理名>.png
- 适用：首页Hero背景、登录背景、AI助手形象、讲解动画、加载动画
- 简介：这是专门为 three.js TSL（r16x 之后的节点着色语言）写的程序化纹理库，和平台的 three 0.185/WebGPU 方向完全对口，每个纹理都能在线调参。黑白的湍流烟、网状细脉、等高线、大理石裂纹几种，稍加着色就有水墨、经络、宣纸的意味。
- 代表示例：`tsl-textures/turbulent-smoke` 墨滴入水般的湍流烟；`tsl-textures/reticular-veins` 网状细脉纹理；`tsl-textures/isolines` 同心等值线；`tsl-textures/satin` 柔光丝绸纹

### Vanta.js（3D 动态网页背景）（`vanta-js`，3D / WebGL / 着色器）

- 链接：https://github.com/tengbao/vanta · https://www.vantajs.com/
- 许可：MIT；商用风险 low。许可是 MIT，问题在维护：仓库 2023-01 起停更，npm 0.5.24 发布于 2022-09。README 按 three r134 全局 THREE 的用法写，Topology/Trunk 依赖 p5.js。和 three 0.185 的兼容性没有实测过（waves 的 wireframe 分支调用了已移除的 Geometry API，默认不会触发）。建议只借思路、自己重写，或者通过 THREE 选项传入新版 three 后充分测试。
- 技术：three.js（r134 时代 API）、p5.js（topology、trunk）、GLSL、vanilla JS
- 规模与更新：14 个效果：birds、cells、clouds、clouds2、dots、fog、globe、halo、net、rings、ripple、topology、trunk、waves；2023-01-12（最后提交；npm 0.5.24 2022-09-16）——实际已停止维护
- 取代码：https://raw.githubusercontent.com/tengbao/vanta/master/src/vanta.<效果>.js （基类 _base.js / _shaderBase.js / _p5Base.js）；打包版 https://raw.githubusercontent.com/tengbao/vanta/master/dist/vanta.<效果>.min.js ；在线调参 https://www.vantajs.com/?effect=<效果>
- 适用：首页Hero背景、登录背景
- 简介：Vanta 是『一行代码挂 3D 背景』的经典库，fog、net、topology 的气质适合学术网站。但它已停更三年多、绑定旧版 three，适合当视觉参考，用 TSL 或着色器重写一版更稳妥。
- 代表示例：`vanta-js/fog` 三色流雾；`vanta-js/halo` 中心流动光晕；`vanta-js/topology` 噪声拓扑流线；`vanta-js/trunk` 生长的年轮

### 3d-force-graph / force-graph（vasturiano）（`vasturiano-3d-force-graph`，3D / WebGL / 着色器）

- 链接：https://github.com/vasturiano/3d-force-graph · https://vasturiano.github.io/3d-force-graph/
- 许可：MIT；商用风险 low。MIT。示例中的 datasets 是演示数据，换成平台自己的知识数据即可。
- 技术：three.js、WebGL、d3-force-3d、vanilla JS（框架无关）
- 规模与更新：约 32 个示例（example/ 目录）；姊妹库 force-graph（2D Canvas）同样 MIT，2026-09-29 更新；2026-09-29（v1.80.1；peer three >=0.179 <1，兼容 0.185）
- 取代码：https://raw.githubusercontent.com/vasturiano/3d-force-graph/master/example/<名称>/index.html ；npm i 3d-force-graph ；可传入自定义 three 对象做节点（nodeThreeObject）
- 适用：知识图谱、数据可视化、AI助手形象、讲解动画
- 简介：这是最成熟的 3D 力导向图库，节点和连线都能用自定义 three 对象，所以可以做成药材图标、汉字标签或发光球。连线上的流动粒子、点击聚焦、展开子节点、DAG 分层几个示例，几乎可以原样对应『知识图谱 / 能力图谱』页面。
- 代表示例：`vasturiano-3d-force-graph/text-nodes` 文字精灵节点图；`vasturiano-3d-force-graph/directional-links-particles` 连线上流动光点；`vasturiano-3d-force-graph/bloom-effect` 辉光星图网络；`vasturiano-3d-force-graph/expandable-nodes` 点击展开子树

### WebGL Fluid Simulation（PavelDoGreat）及衍生（`webgl-fluid-simulation`，3D / WebGL / 着色器）

- 链接：https://github.com/PavelDoGreat/WebGL-Fluid-Simulation · https://paveldogreat.github.io/WebGL-Fluid-Simulation/
- 许可：MIT；商用风险 low。MIT。注意同类项目 haxiomic/GPU-Fluid-Experiments 是 GPL-3.0，不要混用。衍生包 webgl-fluid-enhanced 为 MIT（npm 0.8.0，2024-10）。dli/fluid、dli/flow 为 MIT。
- 技术：raw WebGL、GLSL、vanilla JS（单文件 script.js）
- 规模与更新：1 个可调参数的核心模拟（染料/速度/压力/卷曲/辉光/阳光射线）；相关：webgl-fluid-enhanced（ES 模块化）、dli/fluid（FLIP 粒子流体）、dli/flow；2024-11-12（最后提交；功能早已稳定）
- 取代码：https://raw.githubusercontent.com/PavelDoGreat/WebGL-Fluid-Simulation/master/script.js ；ES 模块版 https://github.com/michaelbrusegard/WebGL-Fluid-Enhanced（npm i webgl-fluid-enhanced）
- 适用：登录背景、首页Hero背景、转场、加载动画
- 简介：这是最经典的浏览器实时流体，代码只有一个文件、MIT。默认是彩色霓虹风，把染料改成单色墨、背景改成宣纸、调低消散速度，就是『墨入清水』的晕染效果，可做登录页的交互背景或水墨转场。
- 代表示例：`webgl-fluid-simulation/official-demo` 鼠标搅动的流体烟雾；`webgl-fluid-simulation/webgl-fluid-enhanced` 可配置流体模块；`webgl-fluid-simulation/david-li-flow` 流场丝绸流线；`webgl-fluid-simulation/gpu-io-fluid-reaction-diffusion` 反应扩散斑纹生长

## B 可用但只放链接

### Aceternity UI（`aceternity-ui`，页面动效 / UI 组件）

- 链接：（无公开仓库；代码通过网站和 shadcn 注册表分发） · https://ui.aceternity.com
- 许可：Aceternity 自有条款。免费组件：首页 FAQ 写明可用于不限数量的个人和商业项目，只是不得把组件本身作为竞争性模板或组件库转售或再分发。https://ui.aceternity.com/licence 只覆盖 Pro 内容。；商用风险 medium。免费层没有 LICENSE 文件，条款只写在 FAQ 里，依据较弱。用于自有网站是允许的，但禁止再分发，因此不要把源码收进共享 skill。23 类页面区块（Blocks）和模板属 All-Access 付费内容，Pro 许可禁止把源文件当素材再分发。优先用 Inspira UI 的 MIT Vue 移植版，Inspira 已获得 Aceternity 授权。
- 技术：React、Next.js、Tailwind CSS、motion；Vue 版本：有，官方只有 React。Inspira UI 移植了大部分常用组件，包括 Timeline、Tracing Beam、Lamp、Aurora、3D Card、Card Spotlight、Text Generate Effect、Container Scroll、Apple Cards Carousel、Placeholders & Vanish Input 等。
- 规模与更新：免费组件约 112 个（首页写“116+”），另有 23 类 All-Access 付费区块；站点持续更新：组件列表包含新组件；/changelog 页最新条目为 2026-05-29
- 取代码：CLI：npx shadcn@latest add @aceternity/<slug>。注册表 JSON：https://ui.aceternity.com/registry/<slug>.json，内嵌源码，可用 curl 获取。组件页：https://ui.aceternity.com/components/<slug>。
- 适用：首页Hero、背景、滚动叙事、文字动效、卡片、数据可视化
- 简介：“光束、聚光灯、3D 卡片”这一类营销页动效的源头，视觉冲击强，单页面效果好。注意许可是自有条款，组件只有 React 版。建议把它当效果目录查看，落地时用 Inspira UI 的 Vue 版。
- 代表示例：`aceternity-ui/sticky-scroll-reveal` 左文右图吸顶切换；`aceternity-ui/timeline` 吸顶标题滚动时间线；`aceternity-ui/text-generate-effect` 文字逐词生成；`aceternity-ui/container-scroll-animation` 截图容器转正

### Codrops（Tympanus）演示与教程（`codrops`，页面动效 / UI 组件）

- 链接：https://github.com/codrops · https://tympanus.net/codrops/demos/
- 许可：MIT（下载的演示除另有说明外均为 MIT）；每个演示仓库有自己的 LICENSE；商用风险 low。演示代码是 MIT，保留版权声明即可。“设计免费素材”另有条款，禁止再分发素材本身。近年很多教程托管在投稿作者自己的仓库，例如 2026-09 的 ASCII Logo，要看那个仓库的 LICENSE；抽查的几个都是 MIT。
- 技术：原生 JS、CSS、GSAP / Lenis / Splitting.js、部分为 three.js、最新有 Astro；Vue 版本：无，演示多为原生 JS 加 GSAP，没有 Vue 版；思路和动画时间线可直接搬进 Vue 组件。
- 规模与更新：数百个演示（GitHub codrops 组织下每个演示一个仓库）；Demo Hub 2026-10-07 仍有新内容；2026-10-07（最新演示 Interlude，codrops/interlude）
- 取代码：git clone https://github.com/codrops/<RepoName>。原始文件：https://raw.githubusercontent.com/codrops/<RepoName>/<main|master>/index.html；打包类项目在 src/ 或 dist/ 下。tympanus.net 对 curl 返回 403，演示页和文章要用 fetch 工具。
- 适用：滚动叙事、文字动效、转场、首页Hero、卡片
- 简介：编辑出版风格最浓的动效灵感源，滚动排版、文字高亮、粘性分区、页面转场都做得考究，并附完整教程和 MIT 源码。最契合“严肃、优雅、可读”的出版气质，适合做长页叙事的参考。
- 代表示例：`codrops/atmospheric-depth-gallery` 纵深雾气图片长廊；`codrops/breathing-dots` 呼吸的点阵；`codrops/on-scroll-text-highlight` 滚动荧光笔高亮；`codrops/scroll-blur-typography` 滚动模糊显现排版

### LottieFiles 免费动画 + dotLottie Vue 播放器（`lottiefiles`，页面动效 / UI 组件）

- 链接：https://github.com/LottieFiles/dotlottie-web · https://lottiefiles.com/free-animations
- 许可：免费动画：Lottie Simple License（FL 9.13.21）；播放器 @lottiefiles/dotlottie-vue 和 dotlottie-web：MIT；商用风险 medium。Lottie Simple License 允许商用，不强制署名（但建议署名）。修改后的动画仍须以同样条款分发，也不得批量收集 LottieFiles 的文件去做同类素材库。动画由用户上传，来源无法保证；付费素材和 Marketplace 内容另有条款。优先选 free-animation 页面上明确标注 Lottie Simple License 的文件，并在内部清单里记下作者和链接。
- 技术：Vue、React、Svelte、Solid、Web Components、原生 JS；Vue 版本：有，官方 @lottiefiles/dotlottie-vue 0.11.28（2026-10-06）。也可以用 lottie-web 5.13.0（MIT），但它已不常更新。
- 规模与更新：免费动画库规模巨大，未给总数；例如 medical、book、loading 分类各有大量条目；@lottiefiles/dotlottie-vue / dotlottie-web 0.81.0 于 2026-10-06 发布
- 取代码：npm i @lottiefiles/dotlottie-vue。动画页 https://lottiefiles.com/free-animation/<slug>，curl 可访问，可下载 Lottie JSON 或 .lottie。播放器文档：https://raw.githubusercontent.com/LottieFiles/dotlottie-web/main/packages/vue/README.md。
- 适用：加载、图标动画、微交互、空状态插画
- 简介：矢量动画素材的最大来源，适合空状态插画、加载、成功和失败反馈等小动画，体积小、清晰。官方有 Vue 播放器，素材许可允许商用免署名，但要逐个确认来源并记录。
- 代表示例：`lottiefiles/ecg` 心电图线条跳动；`lottiefiles/book-loader` 书本翻页加载；`lottiefiles/book-with-bookmark` 带书签的书本；`lottiefiles/isometric-ekg-loop` 等距心电监护循环

### React Bits（`react-bits`，页面动效 / UI 组件）

- 链接：https://github.com/DavidHDev/react-bits · https://reactbits.dev
- 许可：MIT + Commons Clause License Condition v1.0（自定义，非 OSI 开源许可）；商用风险 medium。条款与 Vue Bits 相同：允许作为网站或产品的一部分商用，禁止把组件本身出售或再分发，明确包括“移植版”。团队可以自己把某个 React 组件改写成 Vue 用在自家网站，但改写后的组件不能作为库或模板对外发布，也不要存进共享 skill。另有付费的 React Bits Pro（pro.reactbits.dev），内容不在开源许可内。
- 技术：React、每个组件 4 个变体：JS-CSS、JS-TW、TS-CSS、TS-TW；Vue 版本：有，大部分已移植到 Vue Bits。少数新组件暂无 Vue 版，如 FluxLines、PatternWaves、MicroSlats、TechText、CircularCarousel、FlexCarousel、DitherVeil、HoloCard、Lanyard、FluidGlass。
- 规模与更新：216 个组件目录：文字 33、动画 41、组件 48、微交互 34、背景 60。另有 Background Studio、Shape Magic、Texture Lab 三个在线工具。；2026-10-12（main 最后一次提交）
- 取代码：CLI：npx shadcn@latest add @react-bits/<Name>-TS-TW。原始文件：https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/ts-tailwind/<Category>/<Name>/<Name>.tsx；纯 CSS 变体在 src/ts-default/<Category>/<Name>/<Name>.tsx 和 <Name>.css。组件说明在 src/constants/Information.js。
- 适用：背景、文字动效、卡片、首页Hero、微交互
- 简介：Vue Bits 的上游，组件更全、更新最快，新效果通常先在这里出现。适合查“Vue 版还没有的效果”，再按许可在自有项目内改写成 Vue。
- 代表示例：`react-bits/patternwaves` 起伏半色调波面；`react-bits/fluxlines` 磁流体发光流线；`react-bits/circularcarousel` 3D 环形封面轮播；`react-bits/microslats` 百叶化作海面

### Rive（交互式状态机动画）社区 / Marketplace（`rive`，页面动效 / UI 组件）

- 链接：https://github.com/rive-app/rive-wasm · https://rive.app/marketplace/
- 许可：运行时 @rive-app/canvas 和 rive-wasm：MIT；Marketplace 社区文件：CC BY 4.0；商用风险 medium。CC BY 4.0 允许商用和修改，但必须署名：写明作者、链接许可、注明是否修改。若用在网站上，需要在页脚或“致谢”页列出。Rive 编辑器的部分功能和导出需付费账号，以官网定价为准。
- 技术：原生 JS（WASM）、React（官方）；Vue 版本：无，官方只有 React 包（@rive-app/react-canvas），没有 Vue 包。在 Vue 组件里直接用 @rive-app/canvas 2.44.2（2026-10-10）创建实例，组件卸载时调用 cleanup。
- 规模与更新：Marketplace 社区文件数量很大，未给总数；@rive-app/canvas 2.44.2 于 2026-10-10 发布；rive-wasm 最后一次提交 2026-10-12
- 取代码：npm i @rive-app/canvas（或 @rive-app/webgl2）。文件页 https://rive.app/marketplace/<id>-<slug>/ 是 JS 渲染的应用，用 fetch 或浏览器查看，在编辑器中 Remix 后导出 .riv。文档索引：https://rive.app/docs/llms.txt。
- 适用：微交互、按钮、加载、图标动画、插画角色
- 简介：适合做有状态的交互小动画，比如开关、勾选、点赞、吉祥物，一个文件内带状态机，前端只需切换输入。社区文件采用 CC BY，必须署名；且没有 Vue 官方包，接入成本略高。
- 代表示例：`rive/book-opening` 点击开合的书；`rive/like-heartbeat-animation` 心跳式点赞；`rive/off-on-toggle` 开关切换动画；`rive/animated-checkbox` 带动画的复选框

### Uiverse.io（社区 CSS/Tailwind 元素库）（`uiverse`，页面动效 / UI 组件）

- 链接：https://github.com/uiverse-io/galaxy · https://uiverse.io
- 许可：MIT。站点页脚写明“All content (UI elements) on this site are published under the MIT License”，每个元素页另有作者署名的 MIT 声明。；商用风险 medium。MIT 允许商用，但内容来自用户投稿，个别元素可能抄自他人作品，来源无法逐一核实。每个文件开头的“From Uiverse.io by <作者>”注释要保留，这就是 MIT 版权声明。用前目测是否像某品牌的标志性设计。
- 技术：HTML + CSS、部分为 Tailwind；Vue 版本：有，单段 HTML 加 CSS，直接粘进 Vue SFC 的 template 和 scoped style 即可；Tailwind 写法的需改写。
- 规模与更新：站点 2026-10 标题为“4488 UI elements”。GitHub 镜像 galaxy 有 3,804 个文件：按钮 1231、卡片 726、加载 718、开关 260、输入框 226、表单 180、复选框 171、图案 103、单选 102、提示 62、通知 23。；站点 2026-10 在线；GitHub 镜像最后同步 2024-09-02（落后于站点）
- 取代码：原始文件：https://raw.githubusercontent.com/uiverse-io/galaxy/main/<Category>/<作者>_<slug>.html，可用 grep 文件头的 Tags 注释检索。站点页面 https://uiverse.io/<作者>/<slug> 对 curl 返回 403，只能用 fetch 工具。
- 适用：加载、按钮、背景、微交互、卡片
- 简介：数千个单文件 CSS 小元素，加载动画、按钮、开关、底纹最多，适合补齐细节。质量参差，需要挑选；可以找到书页翻动加载、叶片加载、心电线这类贴合中医药教育主题的小动效。
- 代表示例：`uiverse/page-flip-loader` 书页翻动加载；`uiverse/book-loader` 书页逐张翻过；`uiverse/leaf-loader` 三叶依次变色；`uiverse/heartbeat-line` 心电线循环

### Vue Bits（React Bits 官方 Vue 移植版）（`vue-bits`，页面动效 / UI 组件）

- 链接：https://github.com/DavidHDev/vue-bits · https://vue-bits.dev
- 许可：MIT + Commons Clause License Condition v1.0（自定义，非 OSI 开源许可）；商用风险 medium。LICENSE 明确允许把组件“作为应用、网站或产品的一部分”用于任何商业目的，所以用在灵枢医学网站上没问题。禁止的是出售、再许可或再分发组件本身，无论单独、打包、做成模板还是做成移植版。因此不要把组件源码整段放进可共享的 skill、模板或组件库，skill 里只记链接和 CLI 命令。社内法务审核时需说明这是非 OSI 许可。
- 技术：Vue 3 SFC（<script setup> + TS）、Tailwind CSS（约 176/208 个 .vue 使用工具类）；Vue 版本：有，原生 Vue 3。依赖按组件不同：gsap、motion-v、ogl、three、lenis，个别用 vgpu（WebGPU）。灵枢工程没有引入 Tailwind，且要兼容 Chromium 64+ 旧内核，接入时需把 Tailwind 类改写为 scoped CSS。
- 规模与更新：约 205 个组件目录：文字动效 32、动画 38、组件 44、微交互 33、背景 58。CLI 注册表 197 项。README 写的“90+”已过时。；2026-09-21（main 最后一次提交）
- 取代码：CLI：npx jsrepo add https://vue-bits.dev/r/<Name>.json，或 npx shadcn@latest add https://vue-bits.dev/r/<Name>.json。注册表 JSON 内嵌完整源码；索引在 https://vue-bits.dev/r/registry.json。原始文件：https://raw.githubusercontent.com/DavidHDev/vue-bits/main/src/content/<Category>/<Name>/<Name>.vue，Category 取 TextAnimations / Animations / Components / Micro / Backgrounds。组件说明与文档 URL 在 src/constants/Information.ts。站点是 SPA，任意路径都返回 200，验证链接要看注册表。
- 适用：首页Hero、背景、文字动效、卡片、滚动叙事、数字计数、微交互、导航、加载
- 简介：目前规模最大、更新最勤的原生 Vue 3 动效组件库，覆盖文字、背景、卡片、微交互五大类，带 jsrepo/shadcn 注册表，可一条命令取单个组件。风格从克制到炫目都有，适合挑出模糊显现、描边成字、等高线背景这类安静的效果，用在学术出版场景。
- 代表示例：`vue-bits/blurtext` 逐词由糊变清；`vue-bits/splittext` 字词依次上浮；`vue-bits/scrollreveal` 滚动逐段去模糊；`vue-bits/stroketext` 描边落笔成字

### Bruno Simon 开源作品集（folio-2025 / folio-2019）（`bruno-simon-folio`，3D / WebGL / 着色器）

- 链接：https://github.com/brunosimon/folio-2025 · https://bruno-simon.com/
- 许可：MIT（folio-2025 与 folio-2019 的 license.md）；商用风险 medium。代码是 MIT，但整站的造型、角色和玩法是作者的个人标识，照搬整体视觉有『抄袭感』和舆论风险。模型、声音等资源是否同属 MIT 未见单独声明，建议只借鉴技术模块（草地、风线、水面、雾）。
- 技术：three.js ^0.183、TSL/WebGPU、Vite、vanilla JS
- 规模与更新：folio-2025 约 1226 个文件，其中 54 个源文件使用 three/tsl；folio-2019 为 three 0.164；folio-2025 2026-04-07；folio-2019 2024-05-06
- 取代码：https://raw.githubusercontent.com/brunosimon/folio-2025/main/sources/Game/World/<模块>.js （Grass.js、WindLines.js、WaterSurface.js）及 sources/Game/<模块>.js（Fog.js、Water.js、Wind.js）
- 适用：首页Hero背景、讲解动画
- 简介：这是 Three.js Journey 作者的 2025 版作品集，是用 TSL/WebGPU 写完整互动世界的少见开源案例。对本平台的价值在于几个可单独抽出的自然要素模块，比如随风摆动的草、风线、水面和雾，可以组合成『药圃』『山野采药』场景。
- 代表示例：`bruno-simon-folio/grass` 随风起伏的草地；`bruno-simon-folio/windlines` 掠过的白色风线；`bruno-simon-folio/fog` 远山淡出的雾；`bruno-simon-folio/watersurface` 风格化水面

### Codrops（tympanus.net）WebGL / Three.js 演示与教程（`codrops`，3D / WebGL / 着色器）

- 链接：https://github.com/codrops · https://tympanus.net/codrops/demos/?tag=three-js
- 许可：Codrops 站点声明：演示默认 MIT（『if not specifically mentioned otherwise』），禁止原样再分发或出售演示本身；每个作者的 GitHub 仓库许可各不相同；商用风险 medium。以每个演示自己的 GitHub 仓库为准：本次核对 houmahani/codrops-depth-gallery、clementgrellier/unwoven、momentchan/false-earth、codrops/interlude、Makio64/makio-meshline 为 MIT；kekkorider/codrops-tutorial-dark-cluster、cullenwebber/three-skull、prinzipiell/tsl、motiontx/html-in-canvas、pavel-mazhuga/portfolio 没有 LICENSE 文件，应视为保留所有权利。CodePen 上的公开作品默认 MIT（CodePen 文档）。
- 技术：three.js、TSL/WebGPU、R3F、GLSL、GSAP、Canvas
- 规模与更新：Three.js 标签 282 篇；Demos 页 WebGL 标签 8 页、Three.js 标签 7 页（每页约 44 个），2026 年仍在密集更新；2026-10-07（最新：Interlude 页面转场）
- 取代码：tympanus.net 对 shell 返回 403，列表和文章需用 fetch 工具读取（如 https://tympanus.net/codrops/demos/?tag=webgl）；源码在各作者 GitHub，可 git clone 或 https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
- 适用：首页Hero背景、转场、讲解动画、教材画廊、知识图谱
- 简介：Codrops 是创意前端演示最集中的来源，2026 年大量新作是 TSL/WebGPU，而且多数附 GitHub 源码和逐步讲解的文章。适合本平台的主要是图片画廊滚动、页面转场、粒子/流体揭示几类。许可要逐个仓库核对，不能只看站点的默认 MIT 说明。
- 代表示例：`codrops/atmospheric-depth-gallery` 纵深雾气图片长廊；`codrops/breathing-dots` 呼吸的点阵；`codrops/on-scroll-text-highlight` 滚动荧光笔高亮；`codrops/scroll-blur-typography` 滚动模糊显现排版

## C 只看思路

### AI Animation Skills（Unclecheng-li/AI_Animation，中文 HTML 动效 Agent Skills 集）（`ai-animation-skills`，页面动效 / UI 组件）

- 链接：https://github.com/Unclecheng-li/AI_Animation · https://github.com/Unclecheng-li/AI_Animation
- 许可：仓库 MIT；但其中 skills/ui2v-motions 镜像了上游无 LICENSE 的 illli-studio/motions；商用风险 high。作者原创的 12 个 skill（SKILL.md 加提示词参考）是 MIT，可参考。但仓库混入了两类高风险内容：一是 ui2v-motions，它是 ui2v.com 动效社区 1,262 个 GSAP 动效包的 641MB 全量镜像，上游没有 LICENSE，该 skill 自己也写明“对外发布或商单前回原站确认授权”；二是 web_animation/ 下有一个目录直接命名为“Pirated websites”。只读作者原创的 skill 目录，不要使用这两部分。
- 技术：Agent Skills（SKILL.md）、单文件 HTML / GSAP / Canvas；Vue 版本：无，产出为单文件 HTML 演示页，不是 Vue 组件。
- 规模与更新：12 个 skill：ppt-animation、flowchart、network-protocol-viz、dynamic-archify、scholar-notes、card-theater、video-shot-demos、phone-ui-demos、stacked-data-cards、win11-ui-demos、swiss-shot-demos、ui2v-motions；2026-10-05（master 最后一次提交）
- 取代码：原始文件：https://raw.githubusercontent.com/Unclecheng-li/AI_Animation/master/skills/<skill>/SKILL.md，各 skill 目录下还有 README.md 和 references/。GitHub 网页的 tree 链接对 curl 返回 403。
- 适用：提示词、数据可视化、讲解动画、滚动叙事
- 简介：中文作者写的“用 AI 生成炫酷 HTML 动画”skill 合集，学霸笔记、流程图、动态架构图、叠放数据卡、瑞士风格图表这几个与教育内容高度相关，可借鉴其提示结构。仓库混有无授权镜像，许可风险高，只能有选择地读。
- 代表示例：`ai-animation-skills/flowchart` 流程图原理演示；`ai-animation-skills/swiss-shot-demos` 瑞士风格图表页；`ai-animation-skills/scholar-notes` 手写笔记本学习笔记；`ai-animation-skills/dynamic-archify` 动态架构图

### Awesome Opus 5.5 Videos（Claude Opus 5.5 动画提示词库）（`awesome-opus5-5-videos`，页面动效 / UI 组件）

- 链接：https://github.com/yihui-dev/awesome-opus5-5-videos · https://skillry.dev/ai-videos/opus-5-5
- 许可：仓库 MIT；README 声明每条视频和提示词的权利归原作者；商用风险 medium。这里只有提示词和原帖链接，没有源码。拿提示词思路让模型重新生成自己的代码，风险较低；不要把他人的提示词原文大段收入对外分发的 skill，可以改写或只记 slug 和链接。部分条目以品牌为主题，比如 Spotify、Pokémon，不要模仿。Skillry 站点另有付费 Pro skill。
- 技术：提示词（产出为单文件 HTML / Canvas / SVG / GSAP / three.js）；Vue 版本：无，提示词与框架无关，生成的多为单文件 HTML；改写成 Vue 组件需在提示词里另行要求。
- 规模与更新：853 条提示词：动态图形 501、3D 123、讲解视频 122、交互 107。其中 523 条在 Skillry 有“原作 vs 复刻”对照，234 条只有部分提示词。技术标签：canvas 357、svg 222、three.js 156、shader 110、gsap 100。；2026-10-12（当日新增 10 条，共 853 条）
- 取代码：全量数据：https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json，字段包括 slug、category、tech_tags、prompt、prompt_partial、has_remake、skillry_url。单条：https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/prompts/<slug>.md。复刻视频：https://skillry.dev/ai-videos/opus-5-5/<slug>，只能看，不提供源码下载。
- 适用：提示词、首页Hero、滚动叙事、数据可视化、讲解动画
- 简介：专门收集“让 Claude Opus 5.5 写代码做动画”的真实提示词，数量最多、日更，带分类和技术标签，可按 three.js、gsap 等标签筛选。适合在给模型下达动效任务前，找结构类似的成功提示词作参考，不含源码。
- 代表示例：`awesome-opus5-5-videos/interactive-3d-heart` 交互 3D 人体心脏；`awesome-opus5-5-videos/papercut-shadow-puppet-theater` 剪纸皮影剧场；`awesome-opus5-5-videos/single-line-throughout` 一线到底串联全片；`awesome-opus5-5-videos/article-to-edu-video` 文章生成教育视频

### Awwwards（仅作灵感参考）（`awwwards`，页面动效 / UI 组件）

- 链接：（无，参考站） · https://www.awwwards.com/websites/culture-education/
- 许可：仅作参考。收录的网站各自保有版权，不提供可复用代码。；商用风险 high。只用来看节奏、版式和动效思路，不复制代码、素材或标志性设计。这里标为高风险，指的是复制的风险。
- 技术：仅参考（reference-only）；Vue 版本：无，不适用。
- 规模与更新：“文化与教育”分类有多页；首页每天评选“今日最佳网站”（2026-10-11 仍在更新）；2026-10-11（最近一次“今日最佳网站”评选）
- 取代码：无代码。curl 会被重置连接，只能用 fetch 工具浏览；分类页 /websites/<category>/，作品页 /sites/<slug>。
- 适用：灵感参考、首页Hero、滚动叙事
- 简介：全球获奖网站评选。“文化与教育”分类里有图书馆、博物馆、教育机构网站，可以学习严肃机构如何在保持可读性的同时用动效营造品质感。只作灵感，不取代码。
- 代表示例：`awwwards/culture-education` 文化教育类获奖站；`awwwards/la-public-library` 公共图书馆网站；`awwwards/tedxportland` 讲座活动品牌站；`awwwards/animation-category` 动效类获奖站

### Land-book（仅作灵感参考）（`land-book`，页面动效 / UI 组件）

- 链接：（无，参考站） · https://land-book.com
- 许可：仅作参考。收录网站各自保有版权；站内另售付费模板（59/79/99 美元等）。；商用风险 high。只看版式和动效思路，不复制。免费 Basic 账户对分类、Motion 栏目等有访问限制，Pro 每月 6 美元起。
- 技术：仅参考（reference-only）；Vue 版本：无，不适用。
- 规模与更新：每日更新的网站设计库，未给总数；行业筛选含 Education、Medical、Health & Fitness；每日更新（2026-10 在线）
- 取代码：无代码。curl 返回 403，只能用 fetch 工具；行业筛选是页面内的 #filter-industry，没有独立 URL。
- 适用：灵感参考、首页Hero、卡片
- 简介：落地页设计画廊，可按行业筛选教育、医疗，看同类机构的首屏和分区结构；新增的 Motion 栏目收录动效片段。只作灵感参考。
- 代表示例：`land-book/industry-education-medical` 教育医疗行业落地页；`land-book/motion-section` 网站动效片段合集

### MotionSites.ai Prompt Library（GitHub 镜像：TheSatyam-Singh/motionsites.ai）（`motionsites-prompts`，页面动效 / UI 组件）

- 链接：https://github.com/TheSatyam-Singh/motionsites.ai · https://motionsites.ai
- 许可：GitHub 镜像声明 MIT（Copyright 2026 Aayushsoam）；motionsites.ai 官网页脚写“© Motionsites AI 2026. All rights reserved”，自称“Official Premium AI Website Prompts”；商用风险 high。来源存疑。镜像 README 说这些提示词是“carefully exported”，看起来是从商业站点导出后再贴上 MIT，原站保留全部权利。即便仓库标了 MIT，也可能无权授权。只可浏览其提示词结构，不要复制进 skill。另一个同类仓库 nomaan5541/motionsites-prompt-collection 已无法通过 git 访问。
- 技术：提示词（目标栈：React + Tailwind + Framer Motion + HLS.js）；Vue 版本：无，提示词默认生成 React/Tailwind 的 SaaS 风格首屏，改成 Vue 需另行改写。
- 规模与更新：prompts/ 下 65 条，Pro prompts/ 下 67 个文件，附 94 个视频或图片预览素材。没有生成后的源码。；2026-04-26（main 最后一次提交）
- 取代码：原始文件：https://raw.githubusercontent.com/TheSatyam-Singh/motionsites.ai/main/prompts/<Name>.md，Pro 版在 Pro%20prompts/<Name>.md。
- 适用：提示词、首页Hero
- 简介：面向 Lovable、Bolt、Cursor、Claude 的落地页和 Hero 提示词，写法很细：字体、色值、布局、动效参数逐项给出，可学习“如何把动效要求写成可执行规格”。但许可来源可疑，风格偏 SaaS，不适合直接用于出版社。
- 代表示例：`motionsites-prompts/bionova-biotech` 生物科技整屏 Hero；`motionsites-prompts/terra-geo-map` 地图 SaaS 首屏；`motionsites-prompts/liquid-glass-agency` 液态玻璃落地页；`motionsites-prompts/mindloop-landing` 完整落地页规格

### AI 模型生成动画合集索引（Opus 5.5 / Fable 5.5 / GPT-6 Astra / Sol / Kimi K3，2026）（`ai-model-video-collections`，3D / WebGL / 着色器）

- 链接：https://github.com/yihui-dev/awesome-opus5-5-videos · https://skillry.dev/ai-videos/opus-5-5
- 许可：各合集仓库只许可自身的整理文字和脚本：yihui-dev 两个合集为 MIT，BeatAPI 为 MIT（只覆盖脚本），coolbat 为 CC0，athemeroy 为 CC BY 4.0（只覆盖自写文字），X-RayLuan 与 OpenVGLab 为 MIT，theolundqvist/frontier-games 与 opusvideo 没有 LICENSE；视频、提示词和作品的版权归原创作者；商用风险 high。这些都是索引，不是素材库。视频和提示词归作者所有（yihui-dev README、BeatAPI RIGHTS.md、motionpromptgallery CONTENT-NOTICE 都写明了这一点）。只能借鉴题材和提示词写法；需要代码时只用带 MIT 许可的作品仓库。
- 技术：three.js、Canvas、SVG、GSAP、GLSL/WebGL（均由模型生成）
- 规模与更新：yihui-dev/awesome-opus5-5-videos：853 条提示词，其中 523 条在 Skillry 有重制版，不含源码 | yihui-dev/awesome-fable5-5-videos：82 个视频，9 条原文提示词，3 个 demo 链接，不含源码 | BeatAPI/awesome-3d-prompts（GPT-6 Astra）：306 条，其中 Web 3D 59 条，不含源码 | theolundqvist/frontier-games（Opus 5.5 + GPT-6 Astra）：127 个游戏（97 个可在浏览器试玩）+ 80 部影片，51 条附代码仓库链接（以 GitHub 为主） | X-RayLuan/awesome-opus-5-5-video-prompts：83 条，中英双语 | coolbat/awesome-opus-5.5-usecase：554 条，128 条链到 GitHub | athemeroy/awesome-opus-5-5-videos：424 条来源帖子（Opus 301、Fable 68、Sonnet 54、Haiku 21） | opusvideo/awesome-claude-video：59 条，3 条附源码 | OpenVGLab/awesome-opus5.5-frontend-showcases：中文，自制作品附完整提示词和源码；2026-10-12（yihui-dev 两个合集当天更新）；其余为 2026-09-24 至 2026-10-11
- 取代码：结构化数据：https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json（字段 slug/category/tech_tags/prompt/skillry_url/has_remake）；提示词 https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/prompts/<slug>.md ；https://raw.githubusercontent.com/yihui-dev/awesome-fable5-5-videos/main/data/videos.json ；https://raw.githubusercontent.com/BeatAPI/awesome-3d-prompts/main/data/prompts.json ；https://raw.githubusercontent.com/theolundqvist/frontier-games/main/data/games.yaml ；https://raw.githubusercontent.com/coolbat/awesome-opus-5.5-usecase/main/data/usecases.json
- 适用：讲解动画、首页Hero背景、转场、AI助手形象
- 简介：这些是 2026 年 9 月 Opus 5.5 发布后涌现的『提示词 + 成片』合集，用来了解前沿模型单文件能做出什么、怎样写提示词。和 yihui-dev 那个 Opus 合集同类的有：同作者的 Fable 5.5 合集、BeatAPI 的 GPT-6 Astra 3D 合集、frontier-games 的 Opus 与 Astra 对比，以及多模型的 motionpromptgallery（单列为一条）。几乎都不含源码。真正带源码的是 opus-100-projects（无许可证）和 lemo-opuscar（MIT），已各自单列。合集中已有好几件中国传统题材作品可以直接作为提示词参考。
- 代表示例：`ai-model-video-collections/interactive-3d-heart` 交互 3D 心脏；`ai-model-video-collections/chinese-civilization-timeline` 宣纸与泥金交替编年；`ai-model-video-collections/glucose-to-ethanol-svg` SVG 分步反应路径；`ai-model-video-collections/temple-of-heaven` 祈年殿由线稿到上色

### MotionPromptGallery（多模型：Opus 5.5 / GPT-6 Astra / Kimi K3 / Fable 5）（`ai-motionpromptgallery`，3D / WebGL / 着色器）

- 链接：https://github.com/mikenevermiss/motionpromptgallery · https://motionpromptgallery.com/
- 许可：MIT（仅网站源码）；内容（提示词、视频、海报）归各创作者；商用风险 high。CONTENT-NOTICE 明确写明 MIT 不覆盖 data/ 与媒体文件，只能参考创意。
- 技术：Canvas、SVG、GSAP、three.js、GLSL/WebGL（由模型生成）
- 规模与更新：178 条：Claude Opus 5.5 80、GPT-6 Astra 44、Kimi K3 39、Claude Fable 5 15；122 条有视频；47 条带 code 字段，但内容是后续追问的提示词，不是可运行源码；2026-10-07
- 取代码：https://raw.githubusercontent.com/mikenevermiss/motionpromptgallery/main/data/items.json（字段：model、stack、prompt、code、tags、video、postUrl）；单条页面 https://motionpromptgallery.com/p/<slug>/
- 适用：讲解动画、AI助手形象、首页Hero背景
- 简介：这是唯一一个把多家模型放在一起、每条都附原文提示词的动效合集，可以对比同一题目在不同模型下的效果。医学/生命科学题材（活细胞剖面、生命起源、T 细胞讲解）对平台的讲解动画很有借鉴意义。
- 代表示例：`ai-motionpromptgallery/living-cell` 活细胞 3D 剖面；`ai-motionpromptgallery/obelisk-physics-explainer` 3D 配文字标注讲解；`ai-motionpromptgallery/word-to-code-art` 词语生成的 GLSL 意象；`ai-motionpromptgallery/abiogenesis` 生命起源演化长镜头

### opus-100-projects（Opus 5.5 一次自主运行产出的 121 个作品，含完整源码）（`ai-opus-100-projects`，3D / WebGL / 着色器）

- 链接：https://github.com/swan4er/opus-100-projects · https://swan4er.github.io/opus-100-projects/
- 许可：未声明（仓库无 LICENSE 文件；README 为俄文）；商用风险 high。没有许可证，默认保留所有权利，只能看思路、对照实现手法，不要拷贝代码。部分 AI 游戏需要用户自己的 OpenRouter key。
- 技术：Canvas 2D、WebGL2/GLSL、three.js、SVG、Web Audio
- 规模与更新：121 个：100 个主项目（10 类各 10 个）+ 10 部动画 + 11 个接入大模型的游戏；每个目录都有 index.html/app.js/meta.json 完整源码；2026-09-24
- 取代码：https://raw.githubusercontent.com/swan4er/opus-100-projects/main/<NNN-名称>/index.html （以及 app.js、meta.json、preview.jpg）；在线 https://swan4er.github.io/opus-100-projects/<NNN-名称>/
- 适用：讲解动画、首页Hero背景、知识图谱、加载动画
- 简介：这是在 AI 生成合集里少见的『带完整源码』的一个，而且有几件作品与中医气质高度吻合：卷轴山水、墨入水中、知识星座。它能说明前沿模型单文件能做到什么程度，适合在给模型写提示词前当参照，但没有许可证，不能复用代码。
- 代表示例：`ai-opus-100-projects/ink-in-water` 宣纸上晕开的墨团；`ai-opus-100-projects/shan-shui-scroll` 可续画的山水手卷；`ai-opus-100-projects/electron-cloud` 发光点云轨道；`ai-opus-100-projects/inside-neural-network` 神经网络训练可视化

### The Book of Shaders（着色器入门书）（`book-of-shaders`，3D / WebGL / 着色器）

- 链接：https://github.com/patriciogonzalezvivo/thebookofshaders · https://thebookofshaders.com/
- 许可：All rights reserved（作者自定义条款：禁止以任何形式托管、展示、分发，禁止用于任何商业或非商业产品、网站或项目；只允许出于教育目的链接和署名截图）；商用风险 high。这不是开源许可。书中的代码和示例不能搬进平台，只能用来学习原理。条款年份 2025-01-01 更新过。
- 技术：GLSL、WebGL
- 规模与更新：章节目录 00–18（部分高级章节未完成），附在线编辑器和示例画廊；有中文版 README-ch；2026-02-27
- 取代码：仅供阅读：https://thebookofshaders.com/<章节号>/?lan=ch ；原文 https://raw.githubusercontent.com/patriciogonzalezvivo/thebookofshaders/master/<章节号>/README-ch.md
- 适用：讲解动画
- 简介：这是团队学习片元着色器最好的中文可读教材，噪声、细胞噪声、fBm 几章是做水墨云雾背景的理论基础。许可非常严格，连非商业网站都不能用，只能读，不能抄。
- 代表示例：`book-of-shaders/ch11-noise` 第 11 章 噪声；`book-of-shaders/ch12-cellular-noise` 第 12 章 细胞噪声；`book-of-shaders/ch13-fbm` 第 13 章 分形噪声；`book-of-shaders/online-editor` 着色器在线编辑器

### LYGIA 着色器函数库（`lygia`，3D / WebGL / 着色器）

- 链接：https://github.com/patriciogonzalezvivo/lygia · https://lygia.xyz/
- 许可：Prosperity Public License 3.0.0（非商用免费，商用只给 30 天试用）+ Patron License（赞助者/贡献者）；商用风险 high。出版社官网属于商业用途，免费许可只允许 30 天商业试用。条款里『教育机构』算非商业，但出版社是企业，不能套用。合规途径是成为 GitHub Sponsor（Patron License，只在赞助期间有效）或购买绑定版本的永久商业许可。许可证自 2022-09-14 起改为非商用。替代方案：three.js TSL 自带的 mx_noise 等噪声节点（随 three.js MIT 发布），或 TSL Textures。
- 技术：GLSL、WGSL、HLSL、Metal、WESL
- 规模与更新：657 个 .glsl 文件（另有 WGSL/HLSL/MSL 版本），分 generative、filter、draw、distort、simulate、sdf、lighting 等模块；2026-09-14
- 取代码：https://raw.githubusercontent.com/patriciogonzalezvivo/lygia/main/<模块>/<函数>.glsl ；lygia.xyz 在本环境被重置连接，只能从 GitHub 读
- 适用：讲解动画、首页Hero背景
- 简介：LYGIA 是内容最全的跨语言着色器函数库，噪声、fBm、curl、Voronoi、Kuwahara、笔触、简易流体、反应扩散都有。但它是非商用许可，出版社商用必须赞助或买授权，否则只能读懂原理后自己实现。
- 代表示例：`lygia/generative-curl-glsl` 卷曲噪声函数；`lygia/generative-fbm-glsl` 分形噪声函数；`lygia/filter-kuwahara-glsl` Kuwahara 绘画滤镜；`lygia/draw-stroke-glsl` SDF 描边函数

### Pavel Mazhuga Lab（TSL/WebGPU 实验集）（`pavel-mazhuga-lab`，3D / WebGL / 着色器）

- 链接：https://github.com/pavel-mazhuga/portfolio · https://pavelmazhuga.com/lab/
- 许可：未声明（仓库无 LICENSE 文件）；商用风险 high。没有许可证即默认保留所有权利，只能学习技术思路，不能复制代码；若要复用需向作者取得授权。
- 技术：three.js 0.185.1、TSL、WebGPU、Next.js、TypeScript
- 规模与更新：约 35 个实验（frontend/src/features/experiments/）；2026-07-26
- 取代码：https://raw.githubusercontent.com/pavel-mazhuga/portfolio/main/frontend/src/features/experiments/<名称>/Demo.ts （另有 README.md）；注意预览图走 Git LFS，raw 拿到的只是指针文件
- 适用：首页Hero背景、登录背景、AI助手形象、转场
- 简介：这是同样基于 three 0.185 + TSL 的高质量实验集，粒子流场、粒子变形、flowmap 扭曲、溶解转场都有，Codrops 多次收录。由于没有许可证，只能当作技术参考，按思路重写实现。
- 代表示例：`pavel-mazhuga-lab/flow-field` 噪声流场墨丝；`pavel-mazhuga-lab/particles-morphing-2` 计算着色器粒子重组；`pavel-mazhuga-lab/flowmap` 水面般拖拽的图片；`pavel-mazhuga-lab/dissolve` 模型溶解消散

### Shadertoy（着色器社区）（`shadertoy`，3D / WebGL / 着色器）

- 链接： · https://www.shadertoy.com/
- 许可：站点默认 CC BY-NC-SA 3.0 Unported（新建着色器模板的代码头即为此许可）；作者可在代码中另行声明（如 MIT）；商用风险 high。没有另行声明的着色器按默认许可应视为『署名-非商业-相同方式共享』，出版社商用网站不能直接使用；只有代码注释里明确写了 MIT/CC0 等许可的才可以用。本环境无法读取 shadertoy.com/terms（403），默认许可是从 three.js 官方手册（manual/pages/shadertoy.html，第 51 行等处）引用的 Shadertoy 默认模板代码头间接核实的，引用前请人工打开条款页确认。
- 技术：GLSL（ES 3.0 片元）、WebGL2
- 规模与更新：数十万公开着色器（未核实具体数字）；API 需要申请 key；持续运营（2026-10）
- 取代码：shell 访问返回 403，只能在浏览器或 fetch 工具中查看；作品页 https://www.shadertoy.com/view/<id>；搜索 https://www.shadertoy.com/results?query=<关键词>。复用前务必读每个着色器头部的许可注释。
- 适用：首页Hero背景、登录背景、讲解动画
- 简介：Shadertoy 是全球最大的着色器灵感库，水墨、水彩、烟雾、流场都能搜到大量作品。但默认许可是非商用，出版社只能看效果、理解算法，然后用 TSL 自己重写，或者只采用作者明确声明为 MIT/CC0 的作品。
- 代表示例：`shadertoy/search-ink` 墨迹着色器检索；`shadertoy/search-chinese-painting` 国画风着色器检索；`shadertoy/search-flow-field` 流场卷曲着色器检索；`shadertoy/search-watercolor` 水彩着色器检索
