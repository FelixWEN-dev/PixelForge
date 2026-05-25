<template>
  <div class="image-card" @click="$emit('click')">
    <img :src="src" class="image" />

    <div class="overlay">
      <button class="btn">查看</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
defineProps({
  src: String,
});

defineEmits(["click"]);
</script>

<style scoped lang="less">
@import "@/assets/styles/variables.less";

.image-card {
  position: relative;

  border-radius: 12px;
  overflow: hidden;

  background: @bg-card;

  cursor: pointer;

  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: @shadow-md;

    .overlay {
      opacity: 1;
    }
  }
}

.image {
  width: 100%;
  height: auto;
  object-fit: contain;
  object-position: center;
  display: block;
  background: @bg-card;
}

/* hover遮罩 */
.overlay {
  position: absolute;
  inset: 0;

  background: rgba(0, 0, 0, 0.35);

  display: flex;
  align-items: center;
  justify-content: center;

  opacity: 0;

  transition: all 0.2s ease;
}

.btn {
  padding: 6px 12px;

  border: none;
  border-radius: 999px;

  background: white;
  color: #333;

  font-size: 12px;

  cursor: pointer;

  &:hover {
    background: @primary-color;
    color: white;
  }
}
</style>
