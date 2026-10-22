import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * 元素是否在视口内；同时给元素加上 v59-inview 类，
 * 用于离屏时暂停 CSS 动画（见各楼层样式中的 .v59-io 规则）。
 */
export function useInView (target, { threshold = 0.14, onChange } = {}) {
  const inView = ref(false)
  let io = null
  onMounted(() => {
    const el = target.value?.$el || target.value
    if (!el) return
    if (!('IntersectionObserver' in window)) {
      inView.value = true; el.classList.add('v59-inview'); onChange?.(true); return
    }
    document.documentElement.classList.add('v59-io')
    io = new IntersectionObserver(entries => {
      const v = entries[0].isIntersecting
      el.classList.toggle('v59-inview', v)
      if (v !== inView.value) { inView.value = v; onChange?.(v) }
    }, { threshold })
    io.observe(el)
  })
  onBeforeUnmount(() => io?.disconnect())
  return inView
}
