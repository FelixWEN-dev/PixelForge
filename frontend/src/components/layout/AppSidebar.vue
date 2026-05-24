<template>
  <div class="sidebar-container h-full flex flex-col p-4 border-r">
    <!-- 顶部：新对话 -->
    <div class="mb-6 mt-6" @click="handleNewChatClick">
      <button class="new-chat-btn w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base">
        <svg class="icon-primary w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 4v16m8-8H4"/>
        </svg>
        <span>新对话</span>
      </button>
    </div>

    <!-- 功能区 -->
    <div class="mb-3">
      <ul class="list-none flex flex-col gap-1">
        <li class="menu-item flex items-center justify-between px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base" @click="toggleHistory">
          <span>历史记录</span>
          <svg 
            class="w-4 h-4 transition-transform duration-300" 
            :class="{ 'rotate-180': isHistoryOpen }"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </li>
      </ul>
    </div>

    <!-- 历史列表 -->
    <transition name="slide-fade">
      <div v-show="isHistoryOpen" class="flex-1 overflow-y-auto flex flex-col gap-1">
        <div
          v-for="item in historyList"
          :key="item.id"
          class="history-item flex items-center gap-2.5 px-3.5 py-2.5 rounded cursor-pointer transition-all duration-200 text-base"
          @click="handleHistoryItemClick(item)"
        >
          <svg class="icon-muted w-4 h-4 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <span class="flex-1 truncate">{{ item.title }}</span>
        </div>
      </div>
    </transition>

    <!-- 关于 - 固定在底部 -->
    <div class="footer-section mt-auto pt-4">
      <div class="menu-item about-item flex items-center gap-2 px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base" @click="handleAboutClick">
        <svg class="icon-about w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span>关于</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isHistoryOpen = ref(true);

function handleAboutClick() {
  router.push("/about");
}

function handleHistoryItemClick(item) {
  router.push(`/history/${item.id}`);
}

function toggleHistory() {
  isHistoryOpen.value = !isHistoryOpen.value;
}

function handleNewChatClick() {
  router.push("/");
}

const historyList = ref([
  { id: 1, title: "像素角色设计讨论" },
  { id: 2, title: "游戏场景生成" },
  { id: 3, title: "角色行走动画" },
]);
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.sidebar-container {
  border-color: @border-color;
}

.new-chat-btn {
  border: 1px solid @border-color;
  background-color: @bg-card;
  color: @text-main;
  font-family: @font-main;

  &:hover {
    background-color: @bg-hover;
    border-color: @primary-color;
  }
}

.icon-primary {
  color: @primary-color;
}

.menu-item {
  color: @text-sub;
  font-family: @font-main;

  &:hover {
    background-color: @bg-hover;
    color: @text-main;
  }
}

.history-item {
  color: @text-sub;
  font-family: @font-main;

  &:hover {
    background-color: @bg-hover;
    color: @text-main;
  }
}

.icon-muted {
  color: @text-muted;
}

.footer-section {
  border-top: 1px solid @border-divider;
}

.icon-about {
  color: @text-muted;
}

/* 过渡动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  opacity: 1;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>
