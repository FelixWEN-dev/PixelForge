<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">创建账号</h1>
        <p class="auth-subtitle">加入 PixelForge，开始创作之旅</p>
      </div>

      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名（3-20位）"
            required
            minlength="3"
            maxlength="20"
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="请输入密码（6-20位）"
            required
            minlength="6"
            maxlength="20"
          />
        </div>

        <div class="form-group">
          <label class="form-label">确认密码</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            class="form-input"
            placeholder="请再次输入密码"
            required
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button
          type="submit"
          class="submit-btn"
          :disabled="loading"
        >
          <span v-if="loading">注册中...</span>
          <span v-else>注册</span>
        </button>
      </form>

      <div class="auth-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { register } from '@/api/user';

const router = useRouter();

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

const loading = ref(false);
const error = ref('');

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    error.value = '两次输入的密码不一致';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const res = await register({
      username: form.username,
      password: form.password
    });
    if (res.success) {
      localStorage.setItem('token', res.data.token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      router.push('/chat');
    } else {
      error.value = res.message || '注册失败';
    }
  } catch (err) {
    error.value = err.message || '注册失败，请重试';
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="less" scoped>
@import '@/assets/styles/variables.less';

.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: @bg-base;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: @bg-panel;
  border-radius: @radius-lg;
  padding: 40px;
  box-shadow: @shadow-md;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-title {
  font-family: @font-title;
  font-size: @font-2xl;
  color: @text-main;
  margin-bottom: 8px;
}

.auth-subtitle {
  font-size: @font-md;
  color: @text-sub;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: @font-sm;
  color: @text-sub;
  font-weight: 500;
}

.form-input {
  height: 44px;
  padding: 0 16px;
  border: 1px solid @border-color;
  border-radius: @radius-md;
  font-size: @font-md;
  color: @text-main;
  background: @bg-card;
  transition: @transition-fast;

  &::placeholder {
    color: @text-placeholder;
  }

  &:focus {
    outline: none;
    border-color: @primary-color;
    box-shadow: 0 0 0 3px @primary-soft;
  }
}

.error-message {
  padding: 12px 16px;
  background: rgba(255, 77, 79, 0.1);
  border: 1px solid rgba(255, 77, 79, 0.2);
  border-radius: @radius-md;
  color: #ff4d4f;
  font-size: @font-sm;
}

.submit-btn {
  height: 48px;
  background: @primary-color;
  border: none;
  border-radius: @radius-md;
  color: white;
  font-size: @font-md;
  font-weight: 600;
  cursor: pointer;
  transition: @transition-fast;

  &:hover:not(:disabled) {
    background: @primary-hover;
    transform: translateY(-1px);
    box-shadow: @shadow-glow;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: @font-sm;
  color: @text-sub;

  .link {
    color: @primary-color;
    text-decoration: none;
    margin-left: 4px;
    font-weight: 500;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
