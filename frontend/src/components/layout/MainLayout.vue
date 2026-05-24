<template>
  <div class="layout">

    <!-- Sidebar -->
    <aside class="sidebar">
      <AppSidebar />
    </aside>

    <!-- Main -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- Navbar -->
      <header class="navbar">
        <AppNavbar />
      </header>

      <!-- Content -->
      <main class="content">
        <router-view />
      </main>

    </div>
  </div>
</template>

<script setup>
import AppSidebar from "./AppSidebar.vue";
import AppNavbar from "./AppNavbar.vue";
</script>

<style scoped lang="less">
@import '@/assets/styles/variables.less';

/* ===== Layout ===== */
.layout {
  height: 100vh;
  display: flex;
  background: @bg-base;
  color: @text-main;
  font-family: @font-main;
  overflow: hidden;
}

/* ===== Sidebar ===== */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: @bg-panel;
  border-right: 1px solid @border-color;
  box-shadow: @shadow-sm;
}

/* ===== Navbar ===== */
.navbar {
  height: 64px;
  flex-shrink: 0;
  background: @bg-panel;
  border-bottom: 1px solid @border-color;
  box-shadow: @shadow-sm;
}

/* ===== Content ==== */
.content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 28px;
  background: @bg-base;
}

/* ===== 滚动条 ===== */
.content::-webkit-scrollbar {
  width: 8px;
}

.content::-webkit-scrollbar-track {
  background: transparent;
}

.content::-webkit-scrollbar-thumb {
  background: rgba(255, 122, 89, 0.2);
  border-radius: 999px;
}

.content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 122, 89, 0.35);
}

/* ===== 响应式 ===== */
@media (max-width: 960px) {
  .sidebar {
    width: 84px;
  }

  .content {
    padding: 20px;
  }
}

@media (max-width: 640px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    display: none;
  }

  .navbar {
    padding: 0 16px;
  }

  .content {
    padding: 16px;
  }
}
</style>