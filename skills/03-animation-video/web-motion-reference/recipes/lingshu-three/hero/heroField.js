/**
 * 首屏背景动效（装饰用途，不代表任何推理或数据）：
 * 半透明知识缎带、立体书页、能量流与智能光环。
 * createHeroField(canvas, host) 返回控制对象；由 HeroBackdrop.vue 负责挂载与暂停。
 */
const PALETTES = { teacher: [100, 220, 255], student: [108, 208, 255], author: [175, 158, 255], school: [113, 234, 212], editor: [166, 170, 255], dealer: [140, 215, 245], admin: [159, 181, 255] }

export function createHeroField (canvas, host) {
  const ctx = canvas.getContext('2d', { alpha: true })
  const compact = matchMedia('(max-width: 760px)')
  let width = 0; let height = 0; let elapsed = 12; let impulse = 0; let role = 'teacher'
  const mouse = { x: 0, y: 0 }; const smooth = { x: 0, y: 0 }
  let rgb = [100, 220, 255]; let stars = []; let formFocus = false

  const rgba = (c, a) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x))
  function seeded (seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296 } }
  function makeStars () { const r = seeded(2819); stars = Array.from({ length: compact.matches ? 26 : 66 }, () => ({ x: r(), y: r(), r: 0.45 + r() * 1.05, p: r() * 6.28, a: 0.18 + r() * 0.4 })) }
  function poly (pts, color, lw = 1, close = false) { if (!pts.length) return; ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y))); if (close) ctx.closePath(); ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.stroke() }
  function glow (x, y, r, color, o) { const g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, rgba(color, o)); g.addColorStop(0.4, rgba(color, o * 0.35)); g.addColorStop(1, rgba(color, 0)); ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2) }
  function bezier (a, b, c, d, t) { const m = 1 - t; return { x: m * m * m * a.x + 3 * m * m * t * b.x + 3 * m * t * t * c.x + t * t * t * d.x, y: m * m * m * a.y + 3 * m * m * t * b.y + 3 * m * t * t * c.y + t * t * t * d.y } }

  function sky () {
    ctx.save(); ctx.globalCompositeOperation = 'screen'
    const edge = (width - Math.min(width - 32, 1200)) / 2
    glow(edge * 0.48, height * 0.46, compact.matches ? 230 : 370, [30, 91, 213], 0.35)
    glow(width - edge * 0.38, height * 0.30, 380, [80, 83, 214], 0.29)
    glow(width * 0.58, height * 1.1, width * 0.5, [34, 132, 216], 0.26)
    stars.forEach(p => { const a = p.a * (0.8 + 0.2 * Math.sin(elapsed * 0.55 + p.p)); ctx.beginPath(); ctx.arc(p.x * width + smooth.x * 5, p.y * height + smooth.y * 4, p.r, 0, Math.PI * 2); ctx.fillStyle = rgba([163, 205, 251], a); ctx.fill() })
    ctx.restore()
  }
  function ribbonPoint (u, v, ax, ay, scale, phase, mirror) {
    const twist = u * 4.8 + phase; const half = (0.62 + 0.28 * Math.sin(u * Math.PI)) * scale
    return { x: ax + mirror * (Math.sin(twist) * scale * 0.47 + (v - 0.5) * half * Math.cos(twist * 0.65)) + smooth.x * 11, y: ay + u * height * 0.97 + (v - 0.5) * scale * 0.38 * Math.sin(twist) + smooth.y * 7 }
  }
  function ribbon (ax, ay, scale, phase, mirror, alpha) {
    const rows = compact.matches ? 23 : 42; const samples = compact.matches ? 33 : 48
    ctx.save(); ctx.globalCompositeOperation = 'screen'
    for (let i = 0; i <= rows; i++) {
      const v = i / rows; const pts = []
      for (let j = 0; j <= samples; j++) pts.push(ribbonPoint(j / samples, v, ax, ay, scale, phase, mirror))
      const c = i < rows * 0.58 ? rgb : [145, 135, 254]
      poly(pts, rgba(c, (0.14 + Math.pow(Math.abs(v - 0.5) * 2, 1.4) * 0.38) * alpha), i % 10 === 0 ? 1.2 : 0.75)
    }
    for (let j = 0; j <= 24; j++) { const pts = []; for (let i = 0; i <= 16; i++) pts.push(ribbonPoint(j / 24, i / 16, ax, ay, scale, phase, mirror)); poly(pts, rgba([129, 184, 244], 0.13 * alpha), 0.6) }
    for (let n = 0; n < 2; n++) {
      const p = ribbonPoint((elapsed * 0.034 + n * 0.41) % 1, n ? 1 : 0, ax, ay, scale, phase, mirror)
      glow(p.x, p.y, 25, rgb, 0.12 * alpha); ctx.beginPath(); ctx.arc(p.x, p.y, 1.8, 0, 6.283); ctx.fillStyle = rgba([202, 245, 255], 0.7 * alpha); ctx.fill()
    }
    ctx.restore()
  }
  function currents () {
    const off = Math.sin(elapsed * 0.12) * 9
    const a = { x: -80, y: height * 0.56 }; const b = { x: width * 0.28, y: height * 1.05 + off }; const c = { x: width * 0.79, y: height * 0.8 - off }; const d = { x: width + 60, y: height * 0.48 }
    ctx.save(); ctx.globalCompositeOperation = 'screen'
    for (let k = 0; k < 8; k++) {
      const pts = []; for (let j = 0; j <= 95; j++) pts.push(bezier({ x: a.x, y: a.y + k * 5 }, { x: b.x, y: b.y + k * 3 }, { x: c.x, y: c.y + k * 4 }, { x: d.x, y: d.y + k * 4 }, j / 95))
      poly(pts, rgba(k < 7 ? rgb : [134, 126, 250], k % 6 === 0 ? 0.35 : 0.12), k % 6 === 0 ? 1.3 : 0.65)
    }
    for (let i = 0; i < 3; i++) { const t = (elapsed * 0.021 + i * 0.32) % 1; const pts = []; for (let j = 0; j < 20; j++) pts.push(bezier(a, b, c, d, clamp(t - j * 0.001, 0, 1))); poly(pts, rgba(rgb, 0.5), 1.8) }
    if (impulse > 0.02) { const p = bezier(a, b, c, d, 1 - impulse * 0.82); glow(p.x, p.y, 65, rgb, 0.18 * impulse) }
    ctx.restore()
  }
  function intelligenceField (cx, cy, scale) {
    ctx.save(); ctx.globalCompositeOperation = 'screen'
    const base = 145 * scale * (1 + 0.045 * Math.sin(elapsed * 0.65))
    glow(cx, cy, base * 1.6, [62, 181, 229], 0.18); glow(cx + base * 0.3, cy - base * 0.24, base * 0.95, [135, 135, 250], 0.16)
    const turn = elapsed * 0.075; const samples = 94; const loops = 24
    for (let j = 0; j < loops; j++) {
      const v = j / (loops - 1); const pts = []
      for (let k = 0; k <= samples; k++) {
        const a = k / samples * Math.PI * 2
        const r = base * (0.78 + 0.20 * Math.sin(a * 2 + turn) + 0.13 * Math.cos(a * 3 - turn * 0.7))
        const th = (v - 0.5) * base * 0.58; const tw = a * 1.5 + turn * 0.72
        const x = (r + th * Math.cos(tw)) * Math.cos(a); const z = (r + th * Math.cos(tw)) * Math.sin(a); const yy = th * Math.sin(tw)
        const depth = 1 + (z / base) * 0.07
        pts.push({ x: cx + (x * 0.81 + z * 0.24) * depth + smooth.x * 12, y: cy + (yy * 0.96 + z * 0.57 - x * 0.36) * depth + Math.sin(elapsed * 0.48) * 7 + smooth.y * 8 })
      }
      const edgeW = Math.pow(Math.abs(v - 0.5) * 2, 3)
      poly(pts, rgba(v > 0.6 ? [145, 166, 255] : [101, 236, 224], 0.16 + edgeW * 0.37), edgeW > 0.75 ? 1.25 : 0.7)
      if (j === 0 || j === loops - 1) {
        const p = pts[Math.floor(((elapsed * 0.025 + (j ? 0.47 : 0)) % 1) * samples)]
        glow(p.x, p.y, 27 * scale, [132, 255, 238], 0.3); ctx.beginPath(); ctx.arc(p.x, p.y, 2 * scale, 0, 6.283); ctx.fillStyle = 'rgba(212,255,251,.85)'; ctx.fill()
      }
    }
    glow(cx + base * 0.07, cy, base * 0.39, [87, 241, 222], 0.22)
    for (let i = 0; i < 24; i++) {
      const a = elapsed * 0.14 + i * 2.399; const r = base * (0.4 + ((i * 7) % 20) / 50)
      ctx.beginPath(); ctx.arc(cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.61, 0.6 + (i % 3) * 0.35, 0, 6.283); ctx.fillStyle = rgba([173, 249, 255], 0.13 + (i % 5) * 0.07); ctx.fill()
    }
    ctx.restore()
  }
  function paint () {
    if (!ctx || !width || !height) return
    ctx.clearRect(0, 0, width, height)
    const target = PALETTES[role] || PALETTES.teacher
    rgb = rgb.map((c, i) => c + (target[i] - c) * 0.065)
    smooth.x += (mouse.x - smooth.x) * 0.06; smooth.y += (mouse.y - smooth.y) * 0.06
    sky()
    const edge = (width - Math.min(width - 32, 1200)) / 2
    if (compact.matches) { ribbon(width + 24, -70, 190, elapsed * 0.045 + 1, -1, 0.65); intelligenceField(width + 15, 130, 0.73) } else {
      ribbon(Math.max(15, edge * 0.48), -height * 0.05, Math.min(300, edge * 0.9 + 130), elapsed * 0.052 - 0.75, 1, 0.88)
      if (width > 1250) intelligenceField(width - Math.max(40, edge * 0.47), height * 0.40, width >= 1660 ? 1.1 : 0.9)
      else ribbon(width + 30, -50, 200, elapsed * 0.03 + 2, -1, 0.55)
      currents()
    }
  }
  function resize () {
    if (!ctx) return
    const r = host.getBoundingClientRect(); width = Math.round(r.width); height = Math.round(r.height)
    const dpr = Math.min(window.devicePixelRatio || 1, compact.matches ? 1.25 : 1.5)
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr)
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); makeStars(); paint()
  }
  return {
    ok: !!ctx,
    resize,
    paint,
    /** 推进 dt 秒并重绘 */
    step (dt) { elapsed += dt * (formFocus ? 0.22 : 1); impulse = Math.max(0, impulse - dt * 0.44); paint() },
    pointer (x, y) { mouse.x = clamp(x, -0.5, 0.5); mouse.y = clamp(y, -0.5, 0.5) },
    setFocus (v) { formFocus = v },
    setRole (r, immediate) { if (PALETTES[r]) { role = r; if (immediate) { rgb = [...PALETTES[r]]; paint() } } },
    pulse () { impulse = 1 },
    fps () { return compact.matches ? 20 : 30 },
    onCompactChange (fn) { compact.addEventListener?.('change', fn) }
  }
}
