import { SOFT_POINT_FRAG } from './stage'

/**
 * 灵枢AI 楼层的 3D 核心：由数千个光点组成、缓缓呼吸起伏的球体（AI 的“思考”），
 * 外围两条倾斜的粒子轨道环绕旋转。对话演示“思考中”时，球面起伏加大、转速加快、亮度提高。
 * 用于 useThreeStage(factory)。
 */
const NOISE = /* glsl */`
  vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}
  vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}
  vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}
  vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}
  float snoise(vec3 v){
    const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);
    vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);
    vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);
    vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;
    i=mod289(i);
    vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));
    float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx;
    vec4 j=p-49.0*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);
    vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);
    vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);
    vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));
    vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
    vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);
    vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
    p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
    vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;
    return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
  }
`

export function createAiCoreScene (THREE, { compact }) {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 50)
  camera.position.set(0, 0, 8.2)
  const group = new THREE.Group()
  scene.add(group)
  let busy = 0; let busyGoal = 0
  const rot = { x: 0.25, y: 0, tx: 0.25, ty: 0 }

  /* 光点球：斐波那契球面均匀分布 */
  const n = compact ? 1800 : 4200
  const pos = new Float32Array(n * 3); const rnd = new Float32Array(n)
  const ga = Math.PI * (3 - Math.sqrt(5))
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2; const r = Math.sqrt(1 - y * y); const t = ga * i
    pos[i * 3] = Math.cos(t) * r; pos[i * 3 + 1] = y; pos[i * 3 + 2] = Math.sin(t) * r
    rnd[i] = Math.random()
  }
  const sg = new THREE.BufferGeometry()
  sg.setAttribute('position', new THREE.BufferAttribute(pos, 3))
  sg.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1))
  const sm = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uTime: { value: 0 }, uBusy: { value: 0 }, uDpr: { value: 1 }, uA: { value: new THREE.Color('#5fdbff') }, uB: { value: new THREE.Color('#2f6ff0') }, uC: { value: new THREE.Color('#a08fff') } },
    vertexShader: NOISE + /* glsl */`
      uniform float uTime, uBusy, uDpr;
      uniform vec3 uA, uB, uC;
      attribute float aRand;
      varying vec3 vColor;
      varying float vAlpha;
      void main () {
        vec3 p = position;
        float n = snoise(p * 1.6 + vec3(uTime * 0.22, uTime * 0.18, 0.0));
        float amp = 0.16 + uBusy * 0.22;
        vec3 q = p * (1.55 + n * amp);
        vec4 mv = modelViewMatrix * vec4(q, 1.0);
        gl_Position = projectionMatrix * mv;
        float facing = smoothstep(-0.6, 1.0, normalize(mv.xyz).z * -1.0 + 0.2);
        gl_PointSize = (2.2 + aRand * 2.6 + max(n, 0.0) * 4.0) * uDpr * (8.0 / -mv.z);
        vec3 c = mix(uB, uA, smoothstep(-0.3, 0.6, n));
        c = mix(c, uC, smoothstep(0.55, 1.0, p.y * 0.5 + 0.5) * 0.45);
        vColor = c;
        vAlpha = (0.35 + max(n, 0.0) * 0.8 + uBusy * 0.25) * (0.35 + facing * 0.65);
      }`,
    fragmentShader: SOFT_POINT_FRAG
  })
  group.add(new THREE.Points(sg, sm))

  /* 内核辉光 */
  const cm = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uBusy: { value: 0 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: /* glsl */`
      uniform float uBusy; varying vec2 vUv;
      void main () {
        float d = length(vUv - 0.5) * 2.0;
        float a = exp(-d * d * 5.0) * (0.42 + uBusy * 0.35);
        gl_FragColor = vec4(mix(vec3(0.18, 0.43, 0.94), vec3(0.6, 0.9, 1.0), exp(-d * d * 14.0)), a);
      }`
  })
  const core = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), cm)
  scene.add(core)

  /* 两条粒子轨道 */
  function orbit (radius, count, tiltX, tiltZ, color) {
    const p = new Float32Array(count * 3); const r = new Float32Array(count)
    for (let i = 0; i < count; i++) {
      const a = (i / count) * Math.PI * 2; const j = (Math.random() - 0.5) * 0.08
      p[i * 3] = Math.cos(a) * (radius + j); p[i * 3 + 1] = (Math.random() - 0.5) * 0.04; p[i * 3 + 2] = Math.sin(a) * (radius + j)
      r[i] = Math.random()
    }
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.BufferAttribute(p, 3))
    g.setAttribute('aRand', new THREE.BufferAttribute(r, 1))
    const m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      uniforms: { uDpr: { value: 1 }, uColor: { value: new THREE.Color(color) }, uTime: { value: 0 } },
      vertexShader: /* glsl */`
        uniform float uDpr, uTime; uniform vec3 uColor; attribute float aRand;
        varying vec3 vColor; varying float vAlpha;
        void main () {
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * mv;
          float head = pow(aRand, 14.0);
          gl_PointSize = (1.6 + aRand * 2.4 + head * 6.0) * uDpr * (8.0 / -mv.z);
          vColor = uColor; vAlpha = 0.28 + aRand * 0.4 + head * 0.5;
        }`,
      fragmentShader: SOFT_POINT_FRAG
    })
    const pts = new THREE.Points(g, m)
    const holder = new THREE.Group()
    holder.rotation.set(tiltX, 0, tiltZ)
    holder.add(pts)
    scene.add(holder)
    return { pts, m }
  }
  const o1 = orbit(2.55, compact ? 260 : 520, 1.15, 0.35, '#7fe7ff')
  const o2 = orbit(2.95, compact ? 220 : 420, 1.35, -0.55, '#a796ff')

  const mats = [sm, o1.m, o2.m]
  return {
    scene,
    camera,
    resize (w, h) {
      camera.aspect = w / h
      camera.position.z = w / h < 0.9 ? 9.6 : 8.2
      camera.updateProjectionMatrix()
      const dpr = Math.min(window.devicePixelRatio || 1, compact ? 1.5 : 1.75)
      mats.forEach(m => { m.uniforms.uDpr.value = dpr })
    },
    update (dt, t) {
      busy += (busyGoal - busy) * Math.min(1, dt * 3)
      rot.x += (rot.tx - rot.x) * Math.min(1, dt * 2)
      rot.y += (rot.ty - rot.y) * Math.min(1, dt * 2)
      group.rotation.y = t * (0.12 + busy * 0.35) + rot.y
      group.rotation.x = rot.x
      o1.pts.rotation.y = t * (0.35 + busy * 0.8)
      o2.pts.rotation.y = -t * (0.25 + busy * 0.6)
      sm.uniforms.uTime.value = t * (1 + busy * 1.6)
      sm.uniforms.uBusy.value = busy
      cm.uniforms.uBusy.value = busy
    },
    pointer (x, y) { rot.ty = x * 0.6; rot.tx = 0.25 + y * 0.4 },
    setBusy (v) { busyGoal = v ? 1 : 0 }
  }
}
