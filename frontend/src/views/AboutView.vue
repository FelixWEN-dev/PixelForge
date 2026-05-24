<template>
  <div class="about-view">
    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <AppLoading type="spinner" size="lg" text="正在加载..." />
      </div>
    </transition>
    <h1>关于</h1>
    <p>这是关于页面</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLoading from "@/components/common/AppLoading.vue";

const isLoading = ref(true);

onMounted(() => {
  // 模拟加载（实际项目中可替换为真实数据请求）
  setTimeout(() => {
    isLoading.value = false;
  }, 300);
});
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.about-view {
  position: relative;
  padding: 24px;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(246, 241, 238, 0.7);
  backdrop-filter: blur(4px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
