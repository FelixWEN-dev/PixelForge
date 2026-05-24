<template>
  <div class="loading-wrapper" :class="[type, size]">
    <div v-if="type === 'spinner'" class="spinner">
      <div class="spinner-ring"></div>
    </div>

    <div v-else-if="type === 'dots'" class="dots">
      <span></span>
      <span></span>
      <span></span>
    </div>

    <div v-else-if="type === 'pulse'" class="pulse">
      <div class="pulse-ring"></div>
      <div class="pulse-ring"></div>
      <div class="pulse-ring"></div>
    </div>

    <div
      v-else-if="type === 'skeleton'"
      class="skeleton"
      :style="skeletonStyle"
    >
      <slot></slot>
    </div>

    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { defineProps } from "vue";
const props = defineProps({
  type: {
    type: String,
    default: "spinner",
  },
  size: {
    type: String,
    default: "md",
  },
  text: {
    type: String,
    default: "",
  },
  width: {
    type: [String, Number],
    default: "100%",
  },
  height: {
    type: [String, Number],
    default: "20px",
  },
});

const skeletonStyle = computed(() => ({
  width: typeof props.width === "number" ? `${props.width}px` : props.width,
  height: typeof props.height === "number" ? `${props.height}px` : props.height,
}));
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.loading-text {
  font-size: @font-sm;
  color: @text-muted;
  margin: 0;
}

.spinner {
  position: relative;

  .spinner-ring {
    border-radius: 50%;
    border-style: solid;
    border-color: @border-color;
    border-top-color: @primary-color;
    animation: spin 0.8s linear infinite;
  }
}

.spinner.sm .spinner-ring {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

.spinner.md .spinner-ring {
  width: 32px;
  height: 32px;
  border-width: 3px;
}

.spinner.lg .spinner-ring {
  width: 48px;
  height: 48px;
  border-width: 4px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.dots {
  display: flex;
  gap: 6px;

  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: @primary-color;
    animation: bounce 0.6s ease-in-out infinite;

    &:nth-child(2) {
      animation-delay: 0.1s;
    }

    &:nth-child(3) {
      animation-delay: 0.2s;
    }
  }
}

.dots.sm span {
  width: 6px;
  height: 6px;
}

.dots.lg span {
  width: 12px;
  height: 12px;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.pulse {
  position: relative;
  width: 40px;
  height: 40px;

  .pulse-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid @primary-color;
    animation: pulse 1.5s ease-out infinite;

    &:nth-child(2) {
      animation-delay: 0.5s;
    }

    &:nth-child(3) {
      animation-delay: 1s;
    }
  }
}

.pulse.sm {
  width: 28px;
  height: 28px;
}

.pulse.lg {
  width: 60px;
  height: 60px;
}

@keyframes pulse {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    @bg-card 25%,
    lighten(@bg-card, 5%) 50%,
    @bg-card 75%
  );
  background-size: 200% 100%;
  border-radius: 6px;
  animation: shimmer 1.5s infinite;

  > * {
    opacity: 0;
  }
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
