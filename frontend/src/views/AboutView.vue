<template>
  <div class="about-view">
    <transition name="fade">
      <div v-if="isLoading" class="loading-overlay">
        <AppLoading type="spinner" size="lg" text="正在加载..." />
      </div>
    </transition>

    <div class="about-container">
      <div class="about-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
        </div>
        <h1 class="title">PixelForge</h1>
        <p class="subtitle">AI 驱动的像素风游戏素材生成工具</p>
      </div>

      <div class="about-grid">
        <div class="info-card intro-card">
          <h2>项目简介</h2>
          <p>
            PixelForge 是一款专为游戏开发者打造的 AI 素材生成工具。
            通过简单的文字描述，即可快速生成游戏素材。
          </p>
        </div>

        <div class="info-card feature-card">
          <h2>核心功能</h2>
          <div class="feature-list">
            <div class="feature-item">
              <span class="icon">🎨</span>
              <span>多种风格支持</span>
            </div>
            <div class="feature-item">
              <span class="icon">🎮</span>
              <span>游戏素材类型</span>
            </div>
            <div class="feature-item">
              <span class="icon">📐</span>
              <span>灵活尺寸配置</span>
            </div>
            <div class="feature-item">
              <span class="icon">⚡</span>
              <span>批量生成</span>
            </div>
          </div>
        </div>

        <div class="info-card tech-card">
          <h2>技术栈</h2>
          <div class="tech-grid">
            <div class="tech-item">Vue 3</div>
            <div class="tech-item">Vite</div>
            <div class="tech-item">Less</div>
            <div class="tech-item">FastAPI</div>
            <div class="tech-item">MySQL</div>
            <div class="tech-item">LangChain</div>
            <div class="tech-item">TailwindCSS</div>
          </div>
        </div>

        <div class="info-card version-card">
          <div class="version-info">
            <span>版本号</span>
            <strong>v1.0.0</strong>
          </div>
          <div class="update-time">
            <span>更新时间</span>
            <strong>2026-05-24</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLoading from "@/components/common/AppLoading.vue";

const isLoading = ref(true);

onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 300);
});
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.about-view {
  position: relative;
  height: 100%;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(246, 241, 238, 0.7);
  backdrop-filter: blur(4px);
}

.about-container {
  width: 100%;
  max-width: 800px;
}

.about-header {
  text-align: center;
  margin-bottom: 20px;

  .logo {
    width: 56px;
    height: 56px;
    margin: 0 auto 12px;
    color: #000;

    svg {
      width: 100%;
      height: 100%;
    }
  }

  .title {
    font-size: 28px;
    font-weight: 600;
    color: @text-main;
    margin-bottom: 6px;
  }

  .subtitle {
    font-size: 13px;
    color: @text-muted;
  }
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.info-card {
  background: @bg-panel;
  border-radius: 12px;
  padding: 16px;
  box-shadow: @shadow-sm;

  h2 {
    font-size: 15px;
    font-weight: 600;
    color: @text-main;
    margin-bottom: 12px;
  }

  p {
    font-size: 13px;
    line-height: 1.6;
    color: @text-sub;
  }
}

.intro-card {
  grid-column: span 2;

  @media (max-width: 640px) {
    grid-column: span 1;
  }
}

.feature-card {
  grid-column: span 2;

  @media (max-width: 640px) {
    grid-column: span 1;
  }
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: @text-sub;

  .icon {
    font-size: 18px;
  }
}

.tech-card {
  grid-column: span 2;

  @media (max-width: 640px) {
    grid-column: span 1;
  }
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;

  @media (max-width: 640px) {
    grid-template-columns: repeat(3, 1fr);
  }
}

.tech-item {
  padding: 8px 4px;
  background: @primary-soft;
  color: @primary-color;
  font-size: 12px;
  border-radius: 6px;
  font-weight: 500;
  text-align: center;
}

.version-card {
  grid-column: span 2;
  display: flex;
  justify-content: center;
  gap: 48px;
  text-align: center;
  padding: 12px;

  @media (max-width: 640px) {
    grid-column: span 1;
    gap: 32px;
  }

  > div {
    display: flex;
    flex-direction: column;
    gap: 4px;

    span {
      font-size: 11px;
      color: @text-muted;
    }

    strong {
      font-size: 14px;
      color: @text-main;
      font-weight: 600;
    }
  }
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
