<template>
  <div class="result-panel">
    <div class="panel-header">
      <div class="title">生成结果</div>

      <div v-if="prompt?.trim()" class="prompt" :class="{ expanded: isPromptExpanded }"
        @click="isPromptExpanded = !isPromptExpanded">
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

    <div v-if="images?.length && !loading" class="panel-footer">
      <button class="download-btn" @click="handleDownload">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
        <span>下载图片</span>
      </button>
    </div>
  </div>
</template>

<script setup>
  import ImageGallery from "@/components/result/ImageGallery.vue";
  import AppLoading from "@/components/common/AppLoading.vue";
  import { downloadImages } from "@/utils/download.js";
  import { getImageUrl } from "@/api/request.js";
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

  const loadingText = computed(() => {
    return props.mode === "generate" ? "正在生成中..." : "正在加载中...";
  });

  const handleDownload = () => {
    if (!props.images?.length) return;

    console.log('handleDownload - 原始图片数据:', props.images);

    const imagesToDownload = props.images.map((img, index) => {
      const url = getImageUrl(img.url);
      console.log(`图片 ${index + 1}: 原始url=`, img.url, ', 转换后=', url);
      return {
        url: url,
        name: `pixelforge_${Date.now()}_${index + 1}.png`,
      };
    });

    console.log('handleDownload - 准备下载:', imagesToDownload);
    downloadImages(imagesToDownload);
  };
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

  .panel-footer {
    padding: 16px;
    border-top: 1px solid @border-divider;
    display: flex;
    justify-content: center;
  }

  .download-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;

    border: none;
    border-radius: 20px;

    background: @primary-color;
    color: white;

    font-size: 14px;
    font-family: @font-main;

    cursor: pointer;

    transition: all 0.2s ease;

    svg {
      width: 16px;
      height: 16px;
    }

    &:hover {
      background: @primary-hover;
      transform: translateY(-2px);
      box-shadow: @shadow-md;
    }
  }
</style>