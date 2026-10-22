/**
 * 七类身份的颜色与图标（登录、选择身份、工作台等处共用的数据）。
 * 首页楼层的四类身份标识沿用 roles.js / AudienceBadge.vue，色值与此一致。
 */
export const ROLE_COLOR = {
  student: '#b8580c', teacher: '#0a8576', author: '#6a4fe6', school: '#2563eb',
  editor: '#9a6a00', dealer: '#a23d63', admin: '#475569'
}
/** 身份光感视觉用的高亮色（在深色底上发光的版本，见 components/auth/RoleArt.vue） */
export const ROLE_GLOW = {
  student: '#ffa45c', teacher: '#34e0c2', author: '#a796ff', school: '#5b9bff',
  editor: '#f5c94f', dealer: '#ff7aa8', admin: '#9fc2e8'
}
export const ROLE_ICON = {
  author: 'M4 4h10v5M4 4v16h16V10M9 15l2-5 7-7 3 3-7 7-5 2Z',
  school: 'm3 8 9-5 9 5M5 9v11h14V9M3 21h18M9 12v5M15 12v5M10 20v-2h4v2',
  teacher: 'M3 4h18v12H3zM12 16v5M8 21h8M7 8h10M7 12h6',
  student: 'M12 6C8 3 5 3 2 4v15c4-1 7 0 10 2 3-2 6-3 10-2V4c-3-1-6-1-10 2Zm0 0v15M5 8l4 1M15 9l4-1',
  editor: 'M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4M14 20h6',
  dealer: 'M3 7h18v13H3zM8 7V4h8v3M3 12h18M10 12v3h4v-3',
  admin: 'M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6zM9 12l2 2 4-4'
}
const channels = hex => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16)).join(',')
/**
 * 身份色的 CSS 变量：--rc / --rg 为颜色，--rc-rgb / --rg-rgb 为 RGB 分量，
 * 样式里用 rgba(var(--rg-rgb), .5) 写半透明（兼容不支持 color-mix 的旧内核）。
 */
export const roleVars = role => ({
  '--rc': ROLE_COLOR[role], '--rg': ROLE_GLOW[role],
  '--rc-rgb': channels(ROLE_COLOR[role] || '#2563eb'), '--rg-rgb': channels(ROLE_GLOW[role] || '#5fdbff')
})
/** 头像文字：取姓名最后一个汉字或首字母 */
export const avatarText = name => {
  const n = String(name || '').replace(/^演示\s*·\s*/, '').trim()
  return n ? n.slice(-1).toUpperCase() : '我'
}
