import { createRouter, createWebHashHistory } from "vue-router";

import ChatView from "@/views/ChatView.vue";
import ResultView from "@/views/ResultView.vue";
import AboutView from "@/views/AboutView.vue";

const routes = [
  {
    path: "/",
    redirect: "/chat",
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

export default router;
