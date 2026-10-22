<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { createHeroField } from './heroField'
import { useDialog } from '@/composables/useDialog'
import { useReducedMotion } from '@/composables/useReducedMotion'
import { loadThree, webglAvailable } from '@/three/stage'
import { createHeroScene } from '@/three/heroScene'

/**
 * 首屏背景：静态缎带兜底 + 动态画布。离屏、页面隐藏、弹窗打开或用户暂停时停止绘制。
 * 先用 2D 画布立即出图，three.js 加载完成后换成 3D「知识星河」（不支持 WebGL 时保留 2D）。
 */
const props = defineProps({ paused: Boolean, role: { type: String, default: 'teacher' }, host: { type: Object, default: null } })
const canvas = ref(null)
const canvas3d = ref(null)
const gl = ref(false)
let unmounted = false
const { current } = useDialog()
const reduced = useReducedMotion()
let field = null; let frame = 0; let last = 0; let lastPaint = 0; let inView = false; let io = null; let ro = null; let rz = 0

const canRun = computed(() => !props.paused && !reduced.value && !current.value)
function loop (now) {
  frame = 0
  if (!canRun.value || !inView || document.hidden) { last = 0; return }
  if (now - lastPaint >= 1000 / field.fps() - 1) {
    const dt = last ? Math.min((now - last) / 1000, 0.1) : 0
    last = now; lastPaint = now; field.step(dt)
  }
  frame = requestAnimationFrame(loop)
}
function schedule () {
  if (!field) return
  if (canRun.value && inView && !document.hidden) { if (!frame) { last = 0; lastPaint = 0; frame = requestAnimationFrame(loop) } } else if (frame) { cancelAnimationFrame(frame); frame = 0; last = 0 }
}
const resizeSoon = () => { if (!rz) rz = requestAnimationFrame(() => { rz = 0; field?.resize(); schedule() }) }

const fine = typeof matchMedia === 'function' ? matchMedia('(pointer: fine)') : { matches: false }
function onMove (e) {
  if (!field || !fine.matches || !canRun.value) return
  const r = props.host.getBoundingClientRect()
  field.pointer((e.clientX - r.left) / r.width - 0.5, (e.clientY - r.top) / r.height - 0.5)
}
const onLeave = () => field?.pointer(0, 0)
function onFocusIn (e) { const v = !!e.target.closest('input,textarea,select'); field?.setFocus(v); props.host.dataset.focusQuiet = String(v) }
function onFocusOut () {
  queueMicrotask(() => {
    const a = document.activeElement
    const v = props.host.contains(a) && !!a.closest('input,textarea,select')
    field?.setFocus(v); props.host.dataset.focusQuiet = String(v)
  })
}
const onVis = () => schedule()

onMounted(() => {
  const host = props.host
  field = createHeroField(canvas.value, host)
  if (!field.ok) return
  field.setRole(props.role, true)
  field.resize()
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver(e => { inView = e[0].isIntersecting; schedule() }, { threshold: 0.03 }); io.observe(host)
  } else inView = true
  if ('ResizeObserver' in window) { ro = new ResizeObserver(resizeSoon); ro.observe(host) }
  addEventListener('resize', resizeSoon, { passive: true })
  field.onCompactChange(resizeSoon)
  document.addEventListener('visibilitychange', onVis)
  host.addEventListener('pointermove', onMove, { passive: true })
  host.addEventListener('pointerleave', onLeave, { passive: true })
  host.addEventListener('focusin', onFocusIn)
  host.addEventListener('focusout', onFocusOut)
  schedule()
  upgrade()
})
async function upgrade () {
  if (!webglAvailable()) return
  let THREE
  try { THREE = await loadThree() } catch (e) { return }
  if (unmounted || !canvas3d.value) return
  const f3 = createHeroScene(THREE, canvas3d.value, props.host)
  if (!f3.ok) return
  if (frame) { cancelAnimationFrame(frame); frame = 0; last = 0 }
  f3.setRole(props.role, true)
  f3.resize()
  field = f3
  gl.value = true
  f3.onCompactChange(resizeSoon)
  schedule()
}
onBeforeUnmount(() => {
  unmounted = true
  if (frame) cancelAnimationFrame(frame)
  field?.dispose?.()
  io?.disconnect(); ro?.disconnect()
  removeEventListener('resize', resizeSoon)
  document.removeEventListener('visibilitychange', onVis)
  const host = props.host
  host?.removeEventListener('pointermove', onMove); host?.removeEventListener('pointerleave', onLeave)
  host?.removeEventListener('focusin', onFocusIn); host?.removeEventListener('focusout', onFocusOut)
})
watch(canRun, schedule)
watch(() => props.role, r => field?.setRole(r, !canRun.value))
defineExpose({ pulse: () => field?.pulse(), canAnimate: computed(() => !reduced.value && !!field?.ok) })
</script>

<template>
  <div aria-hidden="true" class="future-background" :data-gl="String(gl)">
    <svg focusable="false" preserveAspectRatio="none" viewBox="0 0 1920 660">
      <defs><linearGradient id="ribbonFallback" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#71d6ff" stop-opacity=".18" /><stop offset=".5" stop-color="#4e86ff" stop-opacity=".05" /><stop offset="1" stop-color="#a993ff" stop-opacity=".25" /></linearGradient></defs>
      <path d="M-80 190C240 450 1080 760 2010 340L2010 410C1090 730 330 500-80 310Z" fill="url(#ribbonFallback)" />
      <path class="quiet-wire" d="M-80 204C240 462 1080 770 2010 354M-80 226C240 484 1080 748 2010 376M-80 248C240 506 1080 726 2010 398" />
    </svg>
    <div class="future-atmosphere"></div>
    <canvas id="futureCanvas" ref="canvas"></canvas>
    <canvas id="futureCanvas3d" ref="canvas3d"></canvas>
    <div class="future-reading-shield"></div>
  </div>
</template>

<style>
#home .future-background{position:absolute;top:0;right:0;bottom:0;left:0;z-index:0;overflow:hidden;pointer-events:none;contain:paint}
#home .future-reading-shield{position:absolute;top:0;right:0;bottom:0;left:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse 490px 155px at max(260px,calc(50% - 275px)) 140px,rgba(8,23,54,.78),rgba(8,23,54,.48) 65%,transparent 100%)}
#home .future-atmosphere{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.4;background:radial-gradient(ellipse at 72% 70%,rgba(var(--fx-cyan),.18),transparent 42%);transition:opacity .6s ease}
#home .future-background svg{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;height:100%;opacity:.65}
#home .future-background svg .quiet-wire{fill:none;stroke:#387cb7;stroke-width:.8;opacity:.22}
#home[data-focus-quiet=true] .future-atmosphere{opacity:.2}
#home #futureCanvas3d{position:absolute;top:0;left:0;width:100%;height:100%;opacity:0;transition:opacity 1.1s ease}
#home .future-background[data-gl=true] #futureCanvas3d{opacity:1}
#home .future-background[data-gl=true] #futureCanvas{opacity:0;transition:opacity .8s ease}
#home .future-background[data-gl=true] svg{opacity:0;transition:opacity .8s ease}
@media(max-width:960px){
  #home .future-reading-shield{background:linear-gradient(90deg,rgba(7,24,52,.62),rgba(7,24,52,.14))}
}
</style>
