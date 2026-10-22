/**
 * 只导出页面用到的 three.js 类，便于打包时摇树、缩小按需加载的体积。
 * 新场景需要其他类时在这里补充。
 */
export {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Color, Vector3,
  BufferGeometry, BufferAttribute, ShaderMaterial, LineBasicMaterial,
  Points, Line, LineSegments, Mesh, PlaneGeometry, CatmullRomCurve3,
  AdditiveBlending, DynamicDrawUsage
} from 'three'
