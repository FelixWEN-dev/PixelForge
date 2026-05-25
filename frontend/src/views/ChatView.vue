<template>
  <div class="chat-view">
    <div class="welcome-container">
      <div class="welcome-content">
        <div class="welcome-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
        </div>

        <h1 class="welcome-title">PixelForge</h1>

        <div class="quick-actions">
          <button
            v-for="(prompt, index) in quickPrompts"
            :key="index"
            class="quick-btn"
            @click="handleQuickPrompt(prompt)"
          >
            {{ prompt }}
          </button>
        </div>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <AppLoading type="spinner" size="lg" text="正在生成，请稍候..." />
      </div>
    </transition>

    <InputBar @send="handleSend" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import InputBar from "@/components/chat/InputBar.vue";
import AppLoading from "@/components/common/AppLoading.vue";
import { generateAsset, getImageUrl } from "@/api/request";

const router = useRouter();
const isLoading = ref(false);

const quickPrompts = [
  "一个身穿银色盔甲的骑士，手持长剑",
  "一片神秘的魔法森林，有发光的蘑菇",
  "一只喷火的巨龙，张开翅膀",
];

const handleQuickPrompt = async (prompt) => {
  if (!prompt?.trim()) return;
  await doGenerate(prompt, 1, "1024*1024");
};

const handleSend = async (payload) => {
  if (!payload?.prompt?.trim()) return;
  await doGenerate(
    payload.prompt,
    payload.count || 1,
    payload.size || "1024*1024",
  );
};

const doGenerate = async (description, n, size) => {
  isLoading.value = true;
  try {
    const res = await generateAsset({
      asset_type: "character",
      description,
      style: "像素风",
      size: size || "1024*1024",
      reference_images: [],
      n,
      watermark: false,
    });

    if (!res.success) {
      throw new Error(res.error || "生成失败");
    }

    const images = res.data.images.map((img, index) => ({
      id: index + 1,
      url: getImageUrl(img.url),
      status: "done",
    }));

    const prompt = res.data.prompt;

    router.push({
      path: "/result",
      state: {
        images,
        prompt,
      },
    });
  } catch (err) {
    console.error("生成失败：", err);
    alert("生成失败，请检查后端服务");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.chat-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: @bg-base;
}

.welcome-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.welcome-content {
  text-align: center;
}

.welcome-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  color: #000;
}

.welcome-title {
  font-size: 32px;
  margin-bottom: 20px;
}

.quick-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.quick-btn {
  padding: 10px 14px;
  border-radius: 20px;
  border: 1px solid @border-color;
  background: @bg-card;
  cursor: pointer;
}

.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(246, 241, 238, 0.85);
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
