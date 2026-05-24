<template>
  <div class="result-panel">
    <div class="panel-header">
      <div class="title">生成结果</div>

      <div
        v-if="prompt?.trim()"
        class="prompt"
        :class="{ expanded: isPromptExpanded }"
        @click="isPromptExpanded = !isPromptExpanded"
      >
        {{ prompt }}
      </div>
    </div>

    <div class="panel-content">
      <AppLoading v-if="loading" type="spinner" size="lg" :text="loadingText" />

      <div v-else-if="!images?.length" class="empty">
        <p>暂无生成结果</p>
        <span>输入描述后开始生成图片</span>
      </div>

      <ImageGallery v-else :images="images" />
    </div>
  </div>
</template>

<script setup>
import ImageGallery from "@/components/result/ImageGallery.vue";
import AppLoading from "@/components/common/AppLoading.vue";
import { defineProps, ref, computed } from "vue";

const props = defineProps({
  images: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  prompt: {
    type: String,
    default: "",
  },
  mode: {
    type: String,
    default: "load",
    validator: (val) => ["generate", "load"].includes(val),
  },
});

const isPromptExpanded = ref(false);

// 根据 mode 显示不同的 loading 文字
const loadingText = computed(() => {
  return props.mode === "generate" ? "正在生成中..." : "正在加载中...";
});
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.result-panel {
  flex: 1;
  height: 100%;

  display: flex;
  flex-direction: column;

  background: @bg-panel;
  border-left: 1px solid @border-color;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid @border-divider;

  .title {
    font-size: @font-md;
    font-weight: 600;
    color: @text-main;
    text-align: center;
  }

  .prompt {
    margin-top: 8px;
    font-size: @font-xs;
    color: @text-muted;

    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;

    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;

    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      color: @text-main;
    }

    &.expanded {
      display: block;
      -webkit-line-clamp: unset;
      overflow: visible;
      white-space: pre-wrap;
    }
  }
}

.panel-content {
  flex: 1;

  padding: 16px;

  overflow-y: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  background: transparent;
}

.empty {
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  text-align: center;

  color: @text-muted;

  p {
    font-size: @font-sm;
    margin-bottom: 6px;
  }

  span {
    font-size: @font-xs;
  }
}
</style>
