import { ref, onMounted, onBeforeUnmount, watch, unref } from 'vue'

/**
 * three.js 场景的公共外壳（首页 AI 核心、切换身份页的光门等共用）。
 * - three.js 只在浏览器里按需加载（动态 import），不进首屏关键路径，也不参与预渲染；
 * - 不支持 WebGL 时不创建，页面保留原有的 CSS 视觉；
 * - 离屏、页面隐藏、暂停或“减少动态效果”时停止逐帧绘制（减少动态效果时只画一帧静态画面）；
 * - 像素比封顶，手机上自动减少粒子数量（由各场景按 compact 决定）。
 * 场景工厂：factory(THREE, { renderer, compact }) → { scene, camera, resize(w, h), update(dt, t), pointer?(x, y), dispose?() }
 */
let threePromise = null
/* 页面加载完、浏览器空闲时再取 three.js，不和首屏图片、字体抢带宽 */
const whenIdle = () => new Promise(resolve => {
  const go = () => (window.requestIdleCallback ? window.requestIdleCallback(() => resolve(), { timeout: 1500 }) : setTimeout(resolve, 200))
  if (document.readyState === 'complete') go(); else addEventListener('load', go, { once: true })
})
export const loadThree = () => (threePromise ||= whenIdle().then(() => import('./lib.js')))

/** three.js r163 起只支持 WebGL 2；开启“省流量”时也不加载 3D */
export function webglAvailable () {
  if (typeof document === 'undefined') return false
  if (navigator.connection && navigator.connection.saveData) return false
  try {
    return !!(window.WebGL2RenderingContext && document.createElement('canvas').getContext('webgl2'))
  } catch (e) { return false }
}
/** 低配设备（内存或核心数很少）：与手机一样减少粒子数量 */
export const lowPower = () => typeof navigator !== 'undefined' && ((navigator.deviceMemory && navigator.deviceMemory <= 2) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2))
export const prefersReduced = () => typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches

export function useThreeStage (canvasRef, hostRef, factory, opts = {}) {
  const ready = ref(false)
  let THREE = null; let renderer = null; let stage = null
  let frame = 0; let last = 0; let elapsed = 0; let inView = false; let io = null; let ro = null; let disposed = false
  const compact = (typeof matchMedia === 'function' && matchMedia('(max-width: 760px)').matches) || lowPower()
  const fps = compact ? (opts.fpsCompact || 30) : (opts.fps || 60)

  const canRun = () => ready.value && inView && !document.hidden && !unref(opts.paused) && !prefersReduced()
  function render () { renderer.render(stage.scene, stage.camera) }
  function loop (now) {
    frame = 0
    if (!canRun()) { last = 0; return }
    if (!last || now - last >= 1000 / fps - 1.5) {
      const dt = last ? Math.min((now - last) / 1000, 0.1) : 0
      last = now; elapsed += dt
      stage.update(dt, elapsed)
      render()
    }
    frame = requestAnimationFrame(loop)
  }
  function schedule () {
    if (!ready.value) return
    if (canRun()) { if (!frame) { last = 0; frame = requestAnimationFrame(loop) } } else if (frame) { cancelAnimationFrame(frame); frame = 0; last = 0 }
  }
  function resize () {
    const host = unref(hostRef)
    if (!renderer || !host) return
    const w = Math.max(1, host.clientWidth); const h = Math.max(1, host.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, compact ? 1.5 : 1.75))
    renderer.setSize(w, h, false)
    stage.resize(w, h)
    if (!canRun()) { stage.update(0, elapsed); render() }
  }
  function onMove (e) {
    if (!stage?.pointer) return
    const r = unref(hostRef).getBoundingClientRect()
    stage.pointer((e.clientX - r.left) / r.width - 0.5, (e.clientY - r.top) / r.height - 0.5)
  }
  const onLeave = () => stage?.pointer?.(0, 0)
  const onVis = () => schedule()

  onMounted(async () => {
    if (!webglAvailable()) return
    try {
      THREE = await loadThree()
      if (disposed) return
      renderer = new THREE.WebGLRenderer({ canvas: unref(canvasRef), antialias: false, alpha: true, powerPreference: 'high-performance' })
      renderer.setClearColor(0x000000, 0)
      stage = factory(THREE, { renderer, compact })
    } catch (e) {
      renderer?.dispose(); renderer = null; return
    }
    ready.value = true
    const host = unref(hostRef)
    resize()
    stage.update(0, 0); render()
    if ('IntersectionObserver' in window) { io = new IntersectionObserver(en => { inView = en[0].isIntersecting; schedule() }, { threshold: 0.02 }); io.observe(host) } else inView = true
    if ('ResizeObserver' in window) { ro = new ResizeObserver(() => resize()); ro.observe(host) }
    document.addEventListener('visibilitychange', onVis)
    if (matchMedia('(pointer: fine)').matches) { host.addEventListener('pointermove', onMove, { passive: true }); host.addEventListener('pointerleave', onLeave, { passive: true }) }
    schedule()
  })
  onBeforeUnmount(() => {
    disposed = true
    if (frame) cancelAnimationFrame(frame)
    io?.disconnect(); ro?.disconnect()
    document.removeEventListener('visibilitychange', onVis)
    const host = unref(hostRef)
    host?.removeEventListener('pointermove', onMove); host?.removeEventListener('pointerleave', onLeave)
    stage?.dispose?.()
    stage?.scene?.traverse(o => { o.geometry?.dispose?.(); o.material?.dispose?.() })
    renderer?.dispose(); renderer?.forceContextLoss?.()
  })
  if (opts.paused !== undefined) watch(() => unref(opts.paused), schedule)

  /** 在场景上调用方法（如 warp、setRole）；减少动态效果或暂停时立即重画一帧，保证颜色等状态同步 */
  function call (name, ...args) {
    if (!stage?.[name]) return
    stage[name](...args)
    if (!canRun() && renderer) { stage.update(0, elapsed); render() }
    schedule()
  }
  return { ready, call }
}

/** 粒子通用片元着色器：柔和圆点，加色混合时形成光晕 */
export const SOFT_POINT_FRAG = /* glsl */`
  varying vec3 vColor;
  varying float vAlpha;
  void main () {
    vec2 c = gl_PointCoord - 0.5;
    float d = length(c);
    float a = smoothstep(0.5, 0.0, d);
    a = a * a;
    gl_FragColor = vec4(vColor, a * vAlpha);
  }
`
