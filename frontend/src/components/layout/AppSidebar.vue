<template>
  <div class="sidebar-container h-full flex flex-col p-4 border-r">
    <!-- 新对话 -->
    <div class="mb-6 mt-6">
      <button
        class="new-chat-btn w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base"
        @click="handleNewChatClick"
      >
        <svg
          class="icon-primary w-4 h-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4v16m8-8H4"
          />
        </svg>
        <span>新对话</span>
      </button>
    </div>

    <!-- 功能区 -->
    <div class="mb-3">
      <ul class="list-none flex flex-col gap-1">
        <li
          class="menu-item flex items-center justify-between px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base"
          @click="toggleHistory"
        >
          <span>历史记录</span>

          <svg
            class="w-4 h-4 transition-transform duration-300"
            :class="{ 'rotate-180': isHistoryOpen }"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </li>
      </ul>
    </div>

    <!-- 历史列表 -->
    <transition name="slide-fade">
      <div
        v-show="isHistoryOpen"
        class="flex-1 overflow-y-auto flex flex-col gap-1"
      >
        <div v-if="isLoading" class="loading-wrap">
          <AppLoading type="spinner" size="sm" text="加载中..." />
        </div>

        <div
          v-for="item in historyList"
          :key="item.id"
          class="history-item flex items-center gap-2.5 px-3.5 py-2.5 rounded cursor-pointer transition-all duration-200 text-base"
          :class="{ selected: selectedId === item.id }"
          @click="handleHistoryItemClick(item)"
        >
          <svg
            class="icon-muted w-4 h-4 flex-shrink-0"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>

          <span class="flex-1 truncate">
            {{ item.title }}
          </span>
        </div>
      </div>
    </transition>

    <!-- 关于 -->
    <div class="footer-section mt-auto pt-4">
      <div
        class="menu-item about-item flex items-center gap-2 px-3.5 py-2.5 rounded-lg cursor-pointer transition-all duration-200 text-base"
        @click="handleAboutClick"
      >
        <svg
          class="icon-about w-4 h-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>关于</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import AppLoading from "@/components/common/AppLoading.vue";
import { getHistory, extractImageUrl } from "@/api/request";

const router = useRouter();
const route = useRoute();

const isHistoryOpen = ref(true);
const historyList = ref([]);
const isLoading = ref(false);
const selectedId = ref(null);

// 监听路由变化，更新选中状态
watch(
  () => route.params.id,
  (id) => {
    selectedId.value = id ? Number(id) : null;
  },
  { immediate: true },
);

// 加载历史记录
const loadHistory = async () => {
  isLoading.value = true;
  try {
    const res = await getHistory();

    if (res.success) {
      historyList.value = res.data.map((item) => ({
        id: item.id,
        title: item.description,
        prompt: item.prompt,
        images: item.local_paths?.map(extractImageUrl) || [],
      }));
    }
  } catch (err) {
    console.error("历史加载失败", err);
  } finally {
    isLoading.value = false;
  }
};

// 挂载时加载
onMounted(() => {
  loadHistory();
});

// 新对话点击
function handleNewChatClick() {
  router.push("/chat");
}

// 历史记录点击 - 只传 id，ResultView 会重新请求数据
function handleHistoryItemClick(item) {
  router.push(`/result/${item.id}`);
}

// 关于
function handleAboutClick() {
  router.push("/about");
}

// 历史记录展开/收起
function toggleHistory() {
  isHistoryOpen.value = !isHistoryOpen.value;
}
</script>
<style scoped lang="less">
@import "@/assets/styles/variables.less";

.sidebar-container {
  border-color: @border-color;
}

/* 新对话 */
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

/* menu */
.menu-item {
  color: @text-sub;
  font-family: @font-main;

  &:hover {
    background-color: @bg-hover;
    color: @text-main;
  }
}

/* history */
.history-item {
  color: @text-sub;

  &:hover {
    background-color: @bg-hover;
    color: @text-main;
  }

  &.selected {
    background-color: @primary-soft;
    color: @primary-color;

    .icon-muted {
      color: @primary-color;
    }
  }
}

/* footer */
.footer-section {
  border-top: 1px solid @border-divider;
}

.icon-muted,
.icon-about {
  color: @text-muted;
}

.loading-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}

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
