import { createRouter, createWebHashHistory } from "vue-router";
import ChatView from "@/views/ChatView.vue";
import HistoryView from "@/views/HistoryView.vue";
import AboutView from "@/views/AboutView.vue";

const routes = [
  {
    path: "/",
    name: "Chat",
    component: ChatView,
    meta: { title: "新对话" },
  },
  {
    path: "/history/:id?",
    name: "History",
    component: HistoryView,
    meta: { title: "历史记录" },
  },
  {
    path: "/about",
    name: "About",
    component: AboutView,
    meta: { title: "关于" },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
