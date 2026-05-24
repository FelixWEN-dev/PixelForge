<template>
  <div class="image-gallery" :style="galleryStyle">
    <ImageCard
      v-for="(item, index) in images"
      :key="item.id ?? index"
      :src="item.url"
      @click="handleClick(item)"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import ImageCard from "@/components/result/ImageCard.vue";
import { defineProps } from "vue";
const props = defineProps({
  images: {
    type: Array,
    default: () => [],
  },
});

// 根据图片数量动态调整列数和最大宽度
const galleryStyle = computed(() => {
  const count = props.images?.length || 0;

  if (count === 0) {
    return {
      gridTemplateColumns: "1fr",
    };
  }

  if (count === 1) {
    // 1张：大图居中，限制最大宽度
    return {
      gridTemplateColumns: "minmax(auto, 480px)",
      justifyContent: "center",
    };
  }

  if (count === 2) {
    // 2张：并排，每项最小280px
    return {
      gridTemplateColumns: "repeat(2, minmax(280px, 380px))",
      justifyContent: "center",
    };
  }

  if (count === 3) {
    // 3张：第一行2个，第二行1个居中，或3个等宽
    return {
      gridTemplateColumns: "repeat(3, minmax(220px, 300px))",
      justifyContent: "center",
    };
  }

  // 4张：2x2宫格
  return {
    gridTemplateColumns: "repeat(2, minmax(220px, 320px))",
    justifyContent: "center",
  };
});

// 处理点击图片事件
const handleClick = (item) => {
  if (item?.url) {
    window.open(item.url, "_blank");
  }
};
</script>

<style scoped lang="less">
.image-gallery {
  display: grid;
  gap: 16px;
  padding: 8px;
  width: 100%;
  max-width: 720px;
}
</style>
