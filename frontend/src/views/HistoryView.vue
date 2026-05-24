<template>
  <div class="history-view">
    <h1>历史记录</h1>
    <p v-if="historyId">当前会话 ID: {{ historyId }}</p>
    <p v-else>请选择左侧的历史记录</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const historyId = computed(() => route.params.id);
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.history-view {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h1 {
  font-size: @font-2xl;
  color: @text-main;
  margin-bottom: 16px;
}

p {
  font-size: @font-md;
  color: @text-sub;
}
</style>
