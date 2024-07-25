<template>
  <div :class="`content-inner ${pageLayout} m-0 pt-20`" id="page_layout">
    <slot></slot>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
export default {
  setup() {
    const store = useStore()
    const pageLayout = computed(() => store.getters['setting/page_layout'])
    return {
      pageLayout
    }
  }
}
</script>
