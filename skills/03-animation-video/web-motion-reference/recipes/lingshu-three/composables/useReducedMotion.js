import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * 是否开启了系统“减少动态效果”。
 * 预渲染与首次激活时一律按 false 渲染（保证与静态 HTML 一致），挂载后立即读取真实设置。
 */
export function useReducedMotion () {
  const reduced = ref(false)
  let mq = null
  const update = () => { reduced.value = !!mq?.matches }
  onMounted(() => {
    if (typeof matchMedia !== 'function') return
    mq = matchMedia('(prefers-reduced-motion: reduce)')
    update()
    mq.addEventListener ? mq.addEventListener('change', update) : mq.addListener?.(update)
  })
  onBeforeUnmount(() => { mq?.removeEventListener ? mq.removeEventListener('change', update) : mq?.removeListener?.(update) })
  return reduced
}
export const prefersReducedMotion = () =>
  typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches
