<template>
  <div class="h-full w-full flex items-center justify-between px-6">
    <!-- 左侧 Logo -->
    <div class="flex items-center">
      <div
        class="w-9 h-9 rounded-full overflow-hidden bg-gradient-to-br from-primary to-accent-gold flex items-center justify-center shadow-[0_0_12px_rgba(255,122,89,0.18)] border border-white/20"
      >
        <img :src="logo" alt="logo" class="w-6 h-6 object-cover" />
      </div>
    </div>

    <!-- 中间标题 -->
    <div
      class="font-title text-lg font-medium tracking-wide text-primary/90 select-none"
    >
      PixelForge
    </div>

    <div class="w-9"></div>
  </div>
</template>

<script setup>
import logo from "@/assets/img/logo.png";
</script>
