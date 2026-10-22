import { SOFT_POINT_FRAG, lowPower } from './stage'
import { ROLE_GLOW } from '@/components/common/roleMeta'

/**
 * 首屏 3D 背景「知识星河」：远处是一片随时间起伏的光点海（教材内容的数据底座），
 * 几条经络光流从左下方升起、汇向右侧登录卡（内容流向每一种身份），上方散布微光星尘。
 * - 登录卡切换身份时，光流与浪尖渐变为该身份的颜色；
 * - 灵枢AI 检索提交时，从光海中心荡开一圈涟漪，光流短暂加速；
 * - 输入框聚焦时整体放慢、变暗，避免干扰填写；鼠标移动时镜头轻微视差。
 * 接口与 2D 背景（heroField.js）一致，由 HeroBackdrop 统一调度帧率、暂停与离屏。
 */
export function createHeroScene (THREE, canvas, host) {
  const mq = matchMedia('(max-width: 760px)')
  const lite = lowPower()
  const compact = { get matches () { return mq.matches || lite }, addEventListener: (t, f) => mq.addEventListener?.(t, f), removeEventListener: (t, f) => mq.removeEventListener?.(t, f) }
  let renderer
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, powerPreference: 'high-performance' })
  } catch (e) { return { ok: false } }
  renderer.setClearColor(0x000000, 0)

  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(40, 2, 0.1, 80)
  const look = new THREE.Vector3(0, -0.6, -3)
  const cam = { x: 0, y: 2.4, tx: 0, ty: 2.4 }
  const roleColor = new THREE.Color(ROLE_GLOW.teacher)
  const roleTarget = new THREE.Color(ROLE_GLOW.teacher)
  let time = 8; let speed = 1; let focus = false; let pulseT = -10; let pulse = 0; let boost = 0

  /* ---------- 光点海 ---------- */
  function buildSea () {
    const nx = compact.matches ? 110 : 190; const nz = compact.matches ? 46 : 78
    const pos = new Float32Array(nx * nz * 3); const rnd = new Float32Array(nx * nz)
    let k = 0
    for (let j = 0; j < nz; j++) {
      for (let i = 0; i < nx; i++) {
        pos[k * 3] = (i / (nx - 1) - 0.5) * 34 + (j % 2) * 0.09
        pos[k * 3 + 1] = 0
        pos[k * 3 + 2] = -18 + (j / (nz - 1)) * 24
        rnd[k] = Math.random(); k++
      }
    }
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3))
    g.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1))
    const m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      uniforms: {
        uTime: { value: 0 }, uPulseT: { value: -10 }, uPulse: { value: 0 }, uDpr: { value: 1 }, uFade: { value: 1 },
        uBase: { value: new THREE.Color('#1d4fb8') }, uHi: { value: new THREE.Color('#5fdbff') }, uRole: { value: roleColor }
      },
      vertexShader: /* glsl */`
        uniform float uTime, uPulseT, uPulse, uDpr, uFade;
        uniform vec3 uBase, uHi, uRole;
        attribute float aRand;
        varying vec3 vColor;
        varying float vAlpha;
        void main () {
          vec3 p = position;
          float h = sin(p.x * 0.32 + uTime * 0.55) * 0.34
                  + sin(p.z * 0.46 + uTime * 0.42 + p.x * 0.11) * 0.3
                  + sin((p.x * 0.8 + p.z) * 0.85 + uTime * 1.05) * 0.07;
          float d = length(p.xz - vec2(1.5, -4.0));
          float r = (uTime - uPulseT) * 6.5;
          float ring = exp(-pow(d - r, 2.0) * 0.45) * uPulse;
          h += ring * 0.55;
          p.y = h - 1.7;
          vec4 mv = modelViewMatrix * vec4(p, 1.0);
          gl_Position = projectionMatrix * mv;
          float crest = smoothstep(0.18, 0.62, h);
          gl_PointSize = (3.0 + aRand * 2.2 + crest * 3.2 + ring * 5.0) * uDpr * (9.0 / -mv.z);
          vec3 c = mix(uBase, uHi, clamp(h * 1.1 + 0.45, 0.0, 1.0));
          vColor = mix(c, uRole, crest * 0.75 + ring * 0.8);
          vAlpha = smoothstep(-18.0, -9.0, p.z) * (1.0 - smoothstep(3.5, 6.0, p.z)) * smoothstep(17.0, 10.0, abs(p.x))
                 * (0.5 + crest * 0.45 + ring * 0.6) * uFade;
        }`,
      fragmentShader: SOFT_POINT_FRAG
    })
    return new THREE.Points(g, m)
  }

  /* ---------- 经络光流 ---------- */
  /* 从左下光海升起，越过标题右侧的空白，汇入右侧登录卡后方 */
  const STREAMS = [
    [[-17, -1.2, -4], [-9, -0.2, -5], [-3, 1.3, -6.5], [2.5, 2.5, -7], [8, 1.7, -6.4], [17, 0.9, -6]],
    [[-17, -1.6, -2.5], [-10, -0.9, -3.4], [-4, 0.5, -5.4], [2, 1.7, -5.8], [7.5, 1.2, -5], [17, -0.2, -5.5]],
    [[-16, 0.0, -10], [-8, 1.6, -11], [-1, 3.0, -11.5], [5, 3.4, -10.5], [10, 2.6, -9], [18, 2.0, -10]],
    [[-17, -2.0, 0], [-11, -1.6, -1], [-5, -0.4, -3.2], [1, 0.8, -4.4], [6, 0.6, -3.6], [16, -0.8, -4]]
  ]
  const NODE_AT = [0.36, 0.52, 0.66]
  const SAMPLES = 400
  function buildStreams () {
    const per = compact.matches ? 140 : 300
    const curves = STREAMS.map(pts => new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))).getSpacedPoints(SAMPLES))
    const n = per * curves.length
    const pos = new Float32Array(n * 3); const info = new Float32Array(n * 4) // offset, speed, jitter, stream
    const rnd = new Float32Array(n)
    for (let s = 0; s < curves.length; s++) {
      for (let i = 0; i < per; i++) {
        const k = s * per + i
        info[k * 4] = Math.random(); info[k * 4 + 1] = 0.018 + Math.random() * 0.03; info[k * 4 + 2] = (Math.random() - 0.5) * 0.5; info[k * 4 + 3] = s
        rnd[k] = Math.random()
      }
    }
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3).setUsage(THREE.DynamicDrawUsage))
    g.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1))
    const m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      uniforms: { uDpr: { value: 1 }, uRole: { value: roleColor }, uCyan: { value: new THREE.Color('#7fe7ff') }, uFade: { value: 1 } },
      vertexShader: /* glsl */`
        uniform float uDpr, uFade;
        uniform vec3 uRole, uCyan;
        attribute float aRand;
        varying vec3 vColor;
        varying float vAlpha;
        void main () {
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * mv;
          gl_PointSize = (3.2 + aRand * aRand * 9.0) * uDpr * (9.0 / -mv.z);
          vColor = mix(uCyan, uRole, smoothstep(0.25, 0.9, aRand));
          vAlpha = (0.4 + aRand * 0.6) * uFade;
        }`,
      fragmentShader: SOFT_POINT_FRAG
    })
    const points = new THREE.Points(g, m)
    const lineMat = new THREE.LineBasicMaterial({ color: new THREE.Color('#4fb6ff'), transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false })
    const lines = curves.map(c => new THREE.Line(new THREE.BufferGeometry().setFromPoints(c), lineMat))
    /* 知识节点：光流经过处的亮点，节点之间以细线相连，形成一张若隐若现的知识网络 */
    const nodePos = []
    curves.forEach(c => NODE_AT.forEach(u => { const p = c[Math.round(u * SAMPLES)]; nodePos.push(p.x, p.y, p.z) }))
    const ng = new THREE.BufferGeometry()
    ng.setAttribute('position', new THREE.BufferAttribute(new Float32Array(nodePos), 3))
    ng.setAttribute('aRand', new THREE.BufferAttribute(new Float32Array(nodePos.length / 3).map(() => Math.random()), 1))
    const nm = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      uniforms: { uDpr: { value: 1 }, uTime: { value: 0 }, uRole: { value: roleColor }, uFade: { value: 1 } },
      vertexShader: /* glsl */`
        uniform float uDpr, uTime, uFade;
        uniform vec3 uRole;
        attribute float aRand;
        varying vec3 vColor;
        varying float vAlpha;
        void main () {
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * mv;
          float beat = 0.5 + 0.5 * sin(uTime * 1.4 + aRand * 6.28);
          gl_PointSize = (14.0 + beat * 10.0) * uDpr * (9.0 / -mv.z);
          vColor = mix(vec3(0.62, 0.92, 1.0), uRole, 0.45);
          vAlpha = (0.45 + beat * 0.45) * uFade;
        }`,
      fragmentShader: SOFT_POINT_FRAG
    })
    const nodes = new THREE.Points(ng, nm)
    const seg = []
    const N = NODE_AT.length
    for (let s = 0; s < curves.length - 1; s++) {
      for (let i = 0; i < N; i++) {
        const a = s * N + i; const b = (s + 1) * N + Math.min(N - 1, i + (s % 2))
        seg.push(nodePos[a * 3], nodePos[a * 3 + 1], nodePos[a * 3 + 2], nodePos[b * 3], nodePos[b * 3 + 1], nodePos[b * 3 + 2])
      }
    }
    const webMat = new THREE.LineBasicMaterial({ color: new THREE.Color('#7fc8ff'), transparent: true, opacity: 0.12, blending: THREE.AdditiveBlending, depthWrite: false })
    const web = new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg), 3)), webMat)
    return { points, lines, curves, info, pos, per, lineMat, nodes, web }
  }

  /* ---------- 星尘 ---------- */
  function buildDust () {
    const n = compact.matches ? 120 : 260
    const pos = new Float32Array(n * 3); const rnd = new Float32Array(n)
    for (let i = 0; i < n; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 36; pos[i * 3 + 1] = Math.random() * 7 - 0.5; pos[i * 3 + 2] = -18 + Math.random() * 14
      rnd[i] = Math.random()
    }
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3))
    g.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1))
    const m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      uniforms: { uTime: { value: 0 }, uDpr: { value: 1 }, uFade: { value: 1 } },
      vertexShader: /* glsl */`
        uniform float uTime, uDpr, uFade;
        attribute float aRand;
        varying vec3 vColor;
        varying float vAlpha;
        void main () {
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * mv;
          gl_PointSize = (1.2 + aRand * 2.2) * uDpr * (8.0 / -mv.z);
          vColor = mix(vec3(0.62, 0.8, 1.0), vec3(0.75, 0.68, 1.0), aRand);
          vAlpha = (0.25 + 0.5 * (0.5 + 0.5 * sin(uTime * (0.6 + aRand * 1.4) + aRand * 40.0))) * uFade;
        }`,
      fragmentShader: SOFT_POINT_FRAG
    })
    return new THREE.Points(g, m)
  }

  let sea = buildSea(); let streams = buildStreams(); let dust = buildDust()
  scene.add(sea, streams.points, dust, streams.nodes, streams.web, ...streams.lines)

  function rebuild () {
    const old = [sea, streams.points, dust, streams.nodes, streams.web, ...streams.lines]
    scene.remove(...old)
    old.forEach(o => { o.geometry.dispose(); o.material.dispose() })
    sea = buildSea(); streams = buildStreams(); dust = buildDust()
    scene.add(sea, streams.points, dust, streams.nodes, streams.web, ...streams.lines)
    ;[sea, streams.points, dust, streams.nodes].forEach(o => { o.material.uniforms.uDpr.value = renderer.getPixelRatio() })
  }

  function updateStreams (dt) {
    const { curves, info, pos, per } = streams
    const spd = 1 + boost * 3
    for (let k = 0; k < info.length / 4; k++) {
      let u = info[k * 4] + info[k * 4 + 1] * dt * spd * speed
      u -= Math.floor(u)
      info[k * 4] = u
      const c = curves[info[k * 4 + 3]]
      const f = u * SAMPLES; const i = Math.floor(f); const t = f - i
      const a = c[i]; const b = c[Math.min(i + 1, SAMPLES)]
      const j = info[k * 4 + 2]
      const wob = Math.sin(u * 18 + k) * 0.12
      pos[k * 3] = a.x + (b.x - a.x) * t
      pos[k * 3 + 1] = a.y + (b.y - a.y) * t + j * 0.5 + wob
      pos[k * 3 + 2] = a.z + (b.z - a.z) * t + j
    }
    streams.points.geometry.attributes.position.needsUpdate = true
    void per
  }

  function paint () {
    const fade = focus ? 0.62 : 1
    sea.material.uniforms.uTime.value = time
    sea.material.uniforms.uPulseT.value = pulseT
    sea.material.uniforms.uPulse.value = pulse
    sea.material.uniforms.uFade.value = fade
    streams.points.material.uniforms.uFade.value = fade
    dust.material.uniforms.uTime.value = time
    dust.material.uniforms.uFade.value = fade
    streams.nodes.material.uniforms.uTime.value = time
    streams.nodes.material.uniforms.uFade.value = fade
    streams.lineMat.color.copy(roleColor).lerp(new THREE.Color('#4fb6ff'), 0.55)
    camera.position.set(cam.x, cam.y, 9.6)
    camera.lookAt(look)
    renderer.render(scene, camera)
  }

  function resize () {
    const w = Math.max(1, host.clientWidth); const h = Math.max(1, host.clientHeight)
    const dpr = Math.min(window.devicePixelRatio || 1, compact.matches ? 1.4 : 1.75)
    renderer.setPixelRatio(dpr)
    renderer.setSize(w, h, false)
    camera.aspect = w / h
    camera.fov = w / h < 1.2 ? 58 : 40
    camera.updateProjectionMatrix()
    ;[sea, streams.points, dust, streams.nodes].forEach(o => { o.material.uniforms.uDpr.value = dpr })
    updateStreams(0)
    paint()
  }

  let compactFn = null
  return {
    ok: true,
    resize,
    step (dt) {
      const s = focus ? 0.22 : 1
      speed = s
      time += dt * s
      pulse = Math.max(0, pulse - dt * 0.45)
      boost = Math.max(0, boost - dt * 0.8)
      roleColor.lerp(roleTarget, Math.min(1, dt * 3))
      cam.x += (cam.tx - cam.x) * Math.min(1, dt * 2.2)
      cam.y += (cam.ty - cam.y) * Math.min(1, dt * 2.2)
      updateStreams(dt)
      paint()
    },
    pointer (x, y) { cam.tx = x * 1.4; cam.ty = 2.4 - y * 0.5 },
    setFocus (v) { focus = v },
    setRole (r, immediate) {
      if (!ROLE_GLOW[r]) return
      roleTarget.set(ROLE_GLOW[r])
      if (immediate) { roleColor.copy(roleTarget); paint() }
    },
    pulse () { pulseT = time; pulse = 1; boost = 1 },
    fps () { return compact.matches ? 30 : 50 },
    onCompactChange (fn) {
      compactFn = () => { rebuild(); fn() }
      compact.addEventListener?.('change', compactFn)
    },
    dispose () {
      if (compactFn) compact.removeEventListener?.('change', compactFn)
      scene.traverse(o => { o.geometry?.dispose?.(); o.material?.dispose?.() })
      renderer.dispose(); renderer.forceContextLoss?.()
    }
  }
}
