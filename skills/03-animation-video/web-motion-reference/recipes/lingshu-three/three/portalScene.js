import { SOFT_POINT_FRAG } from './stage'

/**
 * 切换身份页的 3D 背景「光门隧道」：远处一圈旋转的光环（新世界的入口），四周的光点沿隧道缓缓迎面而来。
 * - warp(strength)：推门时光点拉长成光线、急速穿过，光环放亮，随后回落（进入新世界的感觉）；
 * - setColor(hex)：光环与光线渐变为所选身份的颜色；
 * - pointer：鼠标移动时镜头轻微偏移，形成纵深视差。
 * 用于 useThreeStage(factory)。
 */
export function createPortalScene (THREE, { compact }) {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(62, 2, 0.1, 140)
  camera.position.set(0, 0, 6)
  const color = new THREE.Color('#5fdbff')
  const target = new THREE.Color('#5fdbff')
  const cyan = new THREE.Color('#7fe7ff')
  let warp = 0; let warpGoal = 0; let flash = 0
  const cam = { x: 0, y: 0, tx: 0, ty: 0 }
  const NEAR = 6; const FAR = -90
  let vw = 1; let vh = 1; let focusY = 0.32 // 消失点在画面中的纵向位置（0 顶部，1 底部），对准门的中心

  /* ---------- 隧道光线（每条两点：头与尾） ---------- */
  const n = compact ? 900 : 2200
  const seg = new Float32Array(n * 6); const col = new Float32Array(n * 6)
  const data = new Float32Array(n * 4) // x, y, z, speed
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2
    const r = 2.6 + Math.pow(Math.random(), 0.7) * 11
    data[i * 4] = Math.cos(a) * r
    data[i * 4 + 1] = Math.sin(a) * r * 0.72
    data[i * 4 + 2] = FAR + Math.random() * (NEAR - FAR)
    data[i * 4 + 3] = 0.6 + Math.random() * 0.9
  }
  const lg = new THREE.BufferGeometry()
  lg.setAttribute('position', new THREE.BufferAttribute(seg, 3).setUsage(THREE.DynamicDrawUsage))
  lg.setAttribute('color', new THREE.BufferAttribute(col, 3).setUsage(THREE.DynamicDrawUsage))
  const lm = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false })
  const lines = new THREE.LineSegments(lg, lm)
  scene.add(lines)

  /* ---------- 光环：旋转的粒子环 + 内圈辉光 ---------- */
  const RING_Z = -34
  const rn = compact ? 700 : 1600
  const rp = new Float32Array(rn * 3); const rr = new Float32Array(rn)
  for (let i = 0; i < rn; i++) {
    const a = (i / rn) * Math.PI * 2
    const r = 7.2 + (Math.random() - 0.5) * (Math.random() < 0.85 ? 0.35 : 1.6)
    rp[i * 3] = Math.cos(a) * r; rp[i * 3 + 1] = Math.sin(a) * r; rp[i * 3 + 2] = (Math.random() - 0.5) * 0.6
    rr[i] = Math.random()
  }
  const rg = new THREE.BufferGeometry()
  rg.setAttribute('position', new THREE.BufferAttribute(rp, 3))
  rg.setAttribute('aRand', new THREE.BufferAttribute(rr, 1))
  const rm = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uColor: { value: color }, uCyan: { value: cyan }, uTime: { value: 0 }, uI: { value: 1 }, uDpr: { value: 1 } },
    vertexShader: /* glsl */`
      uniform vec3 uColor, uCyan;
      uniform float uTime, uI, uDpr;
      attribute float aRand;
      varying vec3 vColor;
      varying float vAlpha;
      void main () {
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mv;
        float tw = 0.55 + 0.45 * sin(uTime * (1.0 + aRand * 2.0) + aRand * 30.0);
        gl_PointSize = (2.5 + aRand * 5.0) * uDpr * (30.0 / -mv.z) * (0.8 + uI * 0.4);
        vColor = mix(uCyan, uColor, 0.35 + aRand * 0.6);
        vAlpha = tw * (0.45 + 0.4 * uI);
      }`,
    fragmentShader: SOFT_POINT_FRAG
  })
  const ring = new THREE.Points(rg, rm)
  ring.position.z = RING_Z
  scene.add(ring)

  const gm = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uColor: { value: color }, uI: { value: 1 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: /* glsl */`
      uniform vec3 uColor; uniform float uI; varying vec2 vUv;
      void main () {
        float d = length(vUv - 0.5) * 2.0;
        float ringGlow = exp(-pow((d - 0.5) * 7.0, 2.0)) * 0.55;
        float core = exp(-d * d * 7.0) * 0.32;
        vec3 c = mix(uColor, vec3(1.0), core * 0.8);
        gl_FragColor = vec4(c, (ringGlow + core) * uI);
      }`
  })
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), gm)
  glow.position.z = RING_Z - 0.5
  scene.add(glow)

  function applyFocus () {
    camera.setViewOffset(vw, vh, 0, Math.round(vh * (0.5 - focusY)), vw, vh)
    camera.updateProjectionMatrix()
  }

  function updateLines (dt, t) {
    const len = 0.25 + warp * 9
    const v = 4 + warp * 90
    const head = 0.55 + warp * 0.45
    for (let i = 0; i < n; i++) {
      let z = data[i * 4 + 2] + v * data[i * 4 + 3] * dt
      if (z > NEAR) z -= NEAR - FAR
      data[i * 4 + 2] = z
      const x = data[i * 4]; const y = data[i * 4 + 1]
      const fade = Math.min(1, (z - FAR) / 30) * (z > NEAR - 3 ? (NEAR - z) / 3 : 1)
      const k = i * 6
      seg[k] = x; seg[k + 1] = y; seg[k + 2] = z
      seg[k + 3] = x; seg[k + 4] = y; seg[k + 5] = z - len * data[i * 4 + 3]
      const mix = (i % 5) / 5
      const cr = cyan.r + (color.r - cyan.r) * mix; const cg = cyan.g + (color.g - cyan.g) * mix; const cb = cyan.b + (color.b - cyan.b) * mix
      const b = head * fade
      col[k] = cr * b; col[k + 1] = cg * b; col[k + 2] = cb * b
      col[k + 3] = 0; col[k + 4] = 0; col[k + 5] = 0
    }
    lg.attributes.position.needsUpdate = true
    lg.attributes.color.needsUpdate = true
    void t
  }

  return {
    scene,
    camera,
    resize (w, h) {
      camera.aspect = w / h
      camera.fov = w / h < 1 ? 78 : 62
      vw = w; vh = h
      applyFocus()
      rm.uniforms.uDpr.value = Math.min(window.devicePixelRatio || 1, compact ? 1.5 : 1.75)
    },
    update (dt, t) {
      warp += (warpGoal - warp) * Math.min(1, dt * (warpGoal > warp ? 7 : 2.2))
      warpGoal = Math.max(0, warpGoal - dt * 1.1)
      flash = Math.max(0, flash - dt * 0.9)
      color.lerp(target, Math.min(1, dt * 2.5))
      cam.x += (cam.tx - cam.x) * Math.min(1, dt * 2)
      cam.y += (cam.ty - cam.y) * Math.min(1, dt * 2)
      camera.position.x = cam.x; camera.position.y = cam.y
      camera.lookAt(0, 0, RING_Z)
      ring.rotation.z = t * 0.06 + warp * 0.6
      const I = 0.85 + flash * 1.4 + warp * 0.5
      rm.uniforms.uTime.value = t; rm.uniforms.uI.value = I
      gm.uniforms.uI.value = 0.8 + flash * 1.6 + warp * 0.6
      updateLines(dt, t)
    },
    pointer (x, y) { cam.tx = x * 1.6; cam.ty = -y * 1.0 },
    setColor (hex) { target.set(hex) },
    setFocusY (f) { focusY = Math.min(0.8, Math.max(0.2, f)); applyFocus() },
    warp (strength = 1) { warpGoal = Math.max(warpGoal, strength); flash = Math.max(flash, strength) },
    dispose () { lg.dispose(); lm.dispose(); rg.dispose(); rm.dispose(); glow.geometry.dispose(); gm.dispose() }
  }
}
