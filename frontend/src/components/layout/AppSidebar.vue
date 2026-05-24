<template>
  <div class="h-full flex flex-col p-4">

    <!-- 新对话 -->
    <div class="mb-4">
      <button
        class="w-full flex items-center gap-2 px-3 py-2
               border border-border rounded-md
               bg-card text-main text-sm
               transition
               hover:bg-hover hover:border-primary"
      >
        <svg class="w-4 h-4 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 4v16m8-8H4"/>
        </svg>
        <span>新对话</span>
      </button>
    </div>

    <!-- 历史列表 -->
    <div class="flex-1 overflow-y-auto space-y-1">

      <div
        v-for="item in historyList"
        :key="item.id"
        class="flex items-center gap-2 px-3 py-2 rounded-sm
               text-sub text-sm cursor-pointer
               transition hover:bg-hover hover:text-main"
      >
        <svg class="w-3.5 h-3.5 text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>

        <span class="flex-1 truncate">
          {{ item.title }}
        </span>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const historyList = ref([
  { id: 1, title: "像素角色设计讨论" },
  { id: 2, title: "游戏场景生成" },
  { id: 3, title: "角色行走动画" },
]);
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 122, 89, 0.2);
  border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 122, 89, 0.35);
}
</style>