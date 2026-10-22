# 验证过的配方

这里记录已经做出来、确认可用的效果。和参考案例不同，配方是“我们自己的结果”：知道参数、知道代码在哪、知道在目标环境里跑得动。

## 灵枢 three.js 场景（2026-10-12，原型 v1.6）

**代码已打包在 `lingshu-three/` 里**，取自 GitHub `keyh/Claude-lsdb` 分支 `feat/login-v62-prototype`（PR #4），提交 `6b532ca`（2026-10-12）。这是项目自己的代码。仓库之后有改动时以仓库为准，必要时重新打包这份副本。

| skill 里的文件 | 工程里的位置 | 作用 |
|---|---|---|
| `three/stage.js` | `apps/portal/src/three/stage.js` | 公共外壳 `useThreeStage`，以及 `loadThree`、`webglAvailable`、`lowPower`、`prefersReduced`、`SOFT_POINT_FRAG` |
| `three/lib.js` | `apps/portal/src/three/lib.js` | 只导出用到的 three 类 |
| `three/heroScene.js` | `apps/portal/src/three/heroScene.js` | 首屏「知识星河」 |
| `three/aiCoreScene.js` | `apps/portal/src/three/aiCoreScene.js` | 灵枢AI「AI 核心」 |
| `three/portalScene.js` | `apps/portal/src/three/portalScene.js` | 切换身份「光门隧道」 |
| `hero/HeroBackdrop.vue` | `apps/portal/src/views/home/hero/HeroBackdrop.vue` | 首屏调度：先跑 2D 背景，three 加载好后换成 3D |
| `hero/heroField.js` | `apps/portal/src/views/home/hero/heroField.js` | 首屏 2D Canvas 背景（降级方案，接口与 3D 一致） |
| `common/roleMeta.js` | `apps/portal/src/components/common/roleMeta.js` | 身份色，含 `ROLE_GLOW` |
| `composables/useInView.js`、`useReducedMotion.js` | `apps/portal/src/composables/` | 进入视口检测、系统“减少动态效果” |

**接入到别的工程时**：
- 代码里的 `@/` 指工程的 `src/`。按上表放回对应位置，或改写导入路径。
- 依赖 `vue` 3 和 `three` 0.185.1（固定版本）。
- `HeroBackdrop.vue` 还依赖工程里的 `@/composables/useDialog`（打开弹窗时暂停背景），这个文件没有打包；在别处使用时去掉相关几行即可。
- `aiCoreScene.js` 里的 3D Simplex 噪声 GLSL 是常见的 webgl-noise 实现（Ashima Arts / Stefan Gustavson，MIT 许可）。对外发布时把它记进第三方声明清单。

**用法**（与工程中的调用方式一致）：

```js
// 灵枢AI 楼层：思考中时让光点球加速
const { ready, call } = useThreeStage(canvasRef, hostRef, createAiCoreScene, { fps: 50, fpsCompact: 30 })
watch(() => chat.busy, v => call('setBusy', v))

// 切换身份页：进入“新世界”时暂停背景；选中身份时换色并冲刺
const { ready, call } = useThreeStage(canvasRef, pageRef, createPortalScene, { fps: 60, fpsCompact: 30, paused: computed(() => phase.value === 'world') })
call('setColor', ROLE_GLOW[role]); call('warp', 1)
```

### 公共外壳 `stage.js`

所有场景都通过 `useThreeStage(canvasRef, hostRef, factory, opts)` 运行，它负责：

- 页面 `load` 之后、空闲时动态 `import('./lib.js')`，three.js 不进首屏关键路径，也不参与预渲染；
- WebGL 2 检测、省流量检测；不满足时不创建，页面保留 CSS 视觉；
- 低配或窄屏（≤760px）进入紧凑模式：30fps、像素比封顶 1.5（桌面 60fps、1.75）；
- 离屏（IntersectionObserver）、页面隐藏、`opts.paused`、系统减少动态效果时停止逐帧绘制，只画一帧静态画面；
- ResizeObserver 自适应；仅精细指针设备监听 `pointermove` 做视差；
- 卸载时释放几何体、材质、渲染器，并调用 `forceContextLoss()`；
- 返回 `{ ready, call }`，`call('setRole', color)` 这类调用在停绘状态下也会立即重画一帧，保证状态同步。

场景工厂约定：`factory(THREE, { renderer, compact })` 返回 `{ scene, camera, resize(w, h), update(dt, t), pointer?(x, y), dispose?() }`，外加各自的方法（如 `setRole`、`pulse`、`setBusy`、`warp`）。

外壳还导出一段柔和圆点的片元着色器（`SOFT_POINT_FRAG`）：按 `gl_PointCoord` 到中心的距离做平滑衰减，配合加色混合形成光晕，用来代替后期 Bloom。

`lib.js` 只导出用到的类：WebGLRenderer、Scene、PerspectiveCamera、Group、Color、Vector3、BufferGeometry、BufferAttribute、ShaderMaterial、LineBasicMaterial、Points、Line、LineSegments、Mesh、PlaneGeometry、CatmullRomCurve3、AdditiveBlending、DynamicDrawUsage。新场景需要别的类就在这里补。

### 三个场景

AI 核心和光门隧道走 `useThreeStage`。首屏「知识星河」例外：它的工厂是 `createHeroScene(THREE, canvas, host)`，接口与 2D 背景 `heroField.js` 一致，由 `views/home/hero/HeroBackdrop.vue` 统一调度帧率、暂停与离屏（three.js 没加载好或不支持时，同一位置显示 2D 背景）。

| 文件 | 场景 | 对外方法 | 关键参数 |
|---|---|---|---|
| `heroScene.js` | 首屏「知识星河」：光点海 + 四条经络光流 + 知识节点 + 星尘 | `step(dt)`、`pointer(x, y)`、`setFocus(bool)`、`setRole(身份, immediate)`、`pulse()`、`fps()` | 海面 190×78 点、三层正弦；每条曲线 300 点；身份色取 `ROLE_GLOW`；聚焦时速度 22%；视差 ±1.4；帧率紧凑 30 / 桌面 50 |
| `aiCoreScene.js` | 灵枢AI「AI 核心」：呼吸的光点球 + 两条轨道 | `setBusy(bool)` | 4200 点（紧凑 1800）斐波那契球面；Simplex 噪声改半径；色 `#2f6ff0→#5fdbff`、顶部 `#a08fff`；忙碌时起伏加大、转速 ×3 |
| `portalScene.js` | 切换身份「光门隧道」：光环 + 迎面光线 | `warp()`、`setColor(color)`、`setFocusY(y)` | 光环 1600 点、光线 2200 条；推门时光线拉长 ×9、提速 ×20 |

它们分别对应参考库里这些手法：粒子海与曲线流动（three 池 `webgl_points_waves`、lib 池 `makio-meshline/*`），噪声粒子球（`pmndrs-examples/gpgpu-curl-noise-dof` 一类），隧道光线（opus 池检索“隧道穿梭”）。

## 新配方模板

用户确认某个效果要上线后，在这里追加一节：

```
## <效果名>（日期，版本）
- 用在：页面 / 位置
- 效果：一两句话描述画面和运动
- 参考了：<id>（借鉴了什么）、<id>（借鉴了什么）
- 代码位置：仓库 / 分支 / 路径（代码不大时，同时复制一份到 recipes/ 下）
- 接口与参数：对外方法、关键数值
- 性能与降级：紧凑模式怎么减量、不支持时显示什么
- 注意：踩过的坑
```
