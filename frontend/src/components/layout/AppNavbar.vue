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

    <!-- 右侧用户操作 -->
    <div class="flex items-center gap-3">
      <!-- 用户下拉菜单 -->
      <div v-if="isLoggedIn" class="user-menu-wrapper">
        <button
          class="user-avatar-btn"
          @click="toggleUserMenu"
          title="用户菜单"
        >
          <div class="avatar">
            {{ username.charAt(0).toUpperCase() }}
          </div>
        </button>

        <!-- 下拉菜单 -->
        <transition name="dropdown">
          <div v-if="isMenuOpen" class="user-dropdown">
            <div class="dropdown-header">
              <span class="username">{{ username }}</span>
            </div>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item logout-item" @click="handleLogout">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span>退出登录</span>
            </button>
          </div>
        </transition>
      </div>
      <div v-else class="w-9"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { logout, getUser } from '@/api/user';
import logo from "@/assets/img/logo.png";

const router = useRouter();
const isLoggedIn = ref(false);
const username = ref('');
const isMenuOpen = ref(false);

onMounted(() => {
  checkLoginStatus();
  document.addEventListener('click', handleDocumentClick);
  window.addEventListener('user-login', checkLoginStatus);
});

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick);
  window.removeEventListener('user-login', checkLoginStatus);
});

const checkLoginStatus = () => {
  const user = getUser();
  if (user) {
    isLoggedIn.value = true;
    username.value = user.username;
  }
};

const toggleUserMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const handleDocumentClick = (e) => {
  const wrapper = document.querySelector('.user-menu-wrapper');
  if (wrapper && !wrapper.contains(e.target)) {
    isMenuOpen.value = false;
  }
};

const handleLogout = () => {
  logout();
  isLoggedIn.value = false;
  username.value = '';
  isMenuOpen.value = false;
  router.push('/login');
};
</script>

<style lang="less" scoped>
@import '@/assets/styles/variables.less';

/* 用户菜单容器 */
.user-menu-wrapper {
  position: relative;
}

/* 用户头像按钮 */
.user-avatar-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
  border-radius: 50%;
  transition: @transition-fast;

  &:hover {
    transform: scale(1.05);
  }

  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, @primary-color, @accent-gold);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(255, 122, 89, 0.3);
  }
}

/* 下拉菜单 */
.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 160px;
  background: @bg-panel;
  border: 1px solid @border-color;
  border-radius: @radius-lg;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-header {
  padding: 12px 16px;
  background: @bg-hover;

  .username {
    font-size: 14px;
    font-weight: 500;
    color: @text-main;
  }
}

.dropdown-divider {
  height: 1px;
  background: @border-divider;
}

.dropdown-item {
  width: 100%;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: @text-sub;
  transition: @transition-fast;

  svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
  }

  &:hover {
    background: @bg-hover;
    color: @text-main;
  }

  &.logout-item {
    color: #ef4444;

    &:hover {
      background: rgba(239, 68, 68, 0.1);
    }
  }
}

/* 下拉动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
