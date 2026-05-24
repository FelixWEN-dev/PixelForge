<template>
  <div class="h-full w-full flex items-center justify-between px-6">

    <!-- 左侧 Logo -->
    <div class="flex items-center">
      <div
        class="w-9 h-9 rounded-full overflow-hidden
               bg-gradient-to-br from-primary to-accent-gold
               flex items-center justify-center
               shadow-[0_0_12px_rgba(255,122,89,0.18)]
               border border-white/20"
      >
        <img
          :src="logo"
          alt="logo"
          class="w-6 h-6 object-cover"
        />
      </div>
    </div>

    <!-- 中间标题 -->
    <div class="font-title text-lg font-medium tracking-wide text-primary/90 select-none">
      PixelForge
    </div>

    <!-- 右侧按钮 -->
    <div class="flex items-center">

      <button
        class="w-10 h-10 flex items-center justify-center
               rounded-lg bg-card text-sub
               transition-all duration-200
               hover:bg-hover hover:text-primary hover:scale-105"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>

    </div>

  </div>
</template>

<script setup>
import logo from "@/assets/img/logo.png"
</script>