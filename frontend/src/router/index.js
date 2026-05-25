import { createRouter, createWebHashHistory } from "vue-router";

import ChatView from "@/views/ChatView.vue";
import ResultView from "@/views/ResultView.vue";
import AboutView from "@/views/AboutView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";

const routes = [
  {
    path: "/",
    redirect: "/chat",
  },

  {
    path: "/login",
    name: "Login",
    component: LoginView,
    meta: { title: "登录", public: true },
  },

  {
    path: "/register",
    name: "Register",
    component: RegisterView,
    meta: { title: "注册", public: true },
  },

  {
    path: "/chat",
    name: "Chat",
    component: ChatView,
    meta: { title: "新建生成" },
  },

  {
    path: "/result/:id?",
    name: "Result",
    component: ResultView,
    meta: { title: "生成结果" },
  },

  {
    path: "/about",
    name: "About",
    component: AboutView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 路由守卫：检查登录状态
router.beforeEach((to) => {
  const token = localStorage.getItem('token');
  const isLoggedIn = !!token;
  const isPublicPage = to.meta?.public;

  console.log('[路由守卫]', to.path, 'isLoggedIn:', isLoggedIn, 'token:', token);

  if (!isLoggedIn && !isPublicPage) {
    console.log('[路由守卫] 未登录，跳转到登录页');
    return '/login';
  } else if (isLoggedIn && (to.path === '/login' || to.path === '/register')) {
    console.log('[路由守卫] 已登录，跳转到首页');
    return '/chat';
  }
});

export default router;
