<template>
  <div class="input-bar">
    <div class="input-container">
      <textarea
        v-model="input"
        class="input-textarea"
        placeholder="描述你想要的图片..."
        rows="4"
        @keydown.enter.prevent="submit"
      />

      <div class="input-actions">
        <button class="send-btn" :disabled="!input.trim()" @click="submit">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </div>
    </div>

    <div class="bottom-options">
      <div class="option-group">
        <span class="label">风格</span>

        <button
          class="option"
          :class="{ active: style === '像素风' }"
          @click="style = '像素风'"
        >
          像素风
        </button>

        <button
          class="option"
          :class="{ active: style === '卡通' }"
          @click="style = '卡通'"
        >
          卡通
        </button>

        <button
          class="option"
          :class="{ active: style === '手绘' }"
          @click="style = '手绘'"
        >
          手绘
        </button>

        <button
          class="option"
          :class="{ active: style === '扁平化' }"
          @click="style = '扁平化'"
        >
          扁平化
        </button>

        <button
          class="option"
          :class="{ active: style === '日系' }"
          @click="style = '日系'"
        >
          日系
        </button>

        <button
          class="option"
          :class="{ active: style === '写实' }"
          @click="style = '写实'"
        >
          写实
        </button>
      </div>

      <div class="option-group">
        <span class="label">素材</span>

        <button
          class="option"
          :class="{ active: type === 'character' }"
          @click="type = 'character'"
        >
          角色
        </button>

        <button
          class="option"
          :class="{ active: type === 'scene' }"
          @click="type = 'scene'"
        >
          场景
        </button>

        <button
          class="option"
          :class="{ active: type === 'item' }"
          @click="type = 'item'"
        >
          道具
        </button>
      </div>

      <div class="option-group">
        <span class="label">尺寸</span>

        <button
          class="option"
          :class="{ active: size === '1:1' }"
          @click="size = '1:1'"
        >
          1:1
        </button>

        <button
          class="option"
          :class="{ active: size === '3:4' }"
          @click="size = '3:4'"
        >
          3:4
        </button>

        <button
          class="option"
          :class="{ active: size === '16:9' }"
          @click="size = '16:9'"
        >
          16:9
        </button>
      </div>

      <div class="option-group">
        <span class="label">透明背景</span>

        <button
          class="option"
          :class="{ active: transparent }"
          @click="transparent = !transparent"
        >
          {{ transparent ? "开启" : "关闭" }}
        </button>
      </div>

      <div class="option-group">
        <span class="label">张数</span>

        <button
          class="option"
          :class="{ active: count === 1 }"
          @click="count = 1"
        >
          1
        </button>

        <button
          class="option"
          :class="{ active: count === 2 }"
          @click="count = 2"
        >
          2
        </button>

        <button
          class="option"
          :class="{ active: count === 3 }"
          @click="count = 3"
        >
          3
        </button>

        <button
          class="option"
          :class="{ active: count === 4 }"
          @click="count = 4"
        >
          4
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";

const emit = defineEmits(["send"]);

const input = ref("");

const style = ref("");
const type = ref("");
const size = ref("");
const transparent = ref(false);
const count = ref(1);

const submit = () => {
  if (!input.value.trim()) return;

  const prompt = [
    input.value,
    style.value,
    type.value,
    size.value,
    transparent.value ? "透明背景" : "",
  ]
    .filter(Boolean)
    .join("，");

  emit("send", {
    prompt,
    count: count.value || 1,
  });

  input.value = "";
};
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.input-bar {
  width: 100%;
  padding: 24px 32px 32px;

  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-container {
  width: 100%;
  max-width: 920px;

  position: relative;

  background: @bg-panel;
  border: 1px solid @border-color;
  border-radius: 24px;

  padding: 24px 24px 72px;

  box-shadow: @shadow-md;

  transition: all 0.25s ease;

  &:focus-within {
    border-color: @primary-color;
    box-shadow: @shadow-lg, @shadow-glow;
    transform: translateY(-2px);
  }
}

.input-textarea {
  width: 100%;
  min-height: 140px;

  border: none;
  outline: none;
  resize: none;

  background: transparent;

  font-size: @font-md;
  color: @text-main;
  font-family: @font-main;
  line-height: 1.8;
}

.input-actions {
  position: absolute;
  right: 16px;
  bottom: 14px;
}

.send-btn {
  width: 32px;
  height: 32px;

  border: none;
  border-radius: 10px;

  background: linear-gradient(135deg, #e97b5c, #d96a4a);
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;

  transition: all 0.2s ease;

  svg {
    width: 16px;
    height: 16px;
  }

  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(233, 123, 92, 0.4);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.bottom-options {
  width: 100%;
  max-width: 920px;

  margin-top: 12px;

  display: flex;
  flex-wrap: wrap;
  justify-content: center;

  gap: 12px 20px;
}

.option-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;

  gap: 6px;

  .label {
    font-size: 11px;
    color: @text-muted;
    margin-right: 2px;
    font-weight: 500;
  }
}

.option {
  height: 26px;
  padding: 0 10px;

  border-radius: 6px;
  border: 1px solid @border-color;

  background: transparent;
  color: @text-sub;

  font-size: 12px;

  cursor: pointer;

  transition: all 0.15s ease;

  &:hover {
    border-color: @primary-color;
    color: @primary-color;
    background: rgba(255, 122, 89, 0.08);
  }

  &.active {
    background: @primary-soft;
    color: @primary-color;
    border-color: @primary-color;
    font-weight: 500;
  }
}
</style>
