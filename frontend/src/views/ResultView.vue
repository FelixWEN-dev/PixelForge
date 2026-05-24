<template>
  <div class="result-view">
    <ResultPanel
      :images="images"
      :loading="loading"
      :prompt="prompt"
      :mode="mode"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import ResultPanel from "@/components/result/ResultPanel.vue";
import { getHistory, extractImageUrl } from "@/api/request";

const route = useRoute();

const images = ref([]);
const loading = ref(false);
const prompt = ref("");
const mode = ref("load");

const loadData = async () => {
  const state = history.state;
  const id = route.params.id;
  const fromGenerate = state?.fromGenerate;

  if (id && fromGenerate) {
    mode.value = "generate";
    loading.value = true;
    try {
      const res = await getHistory();
      if (res.success) {
        const item = res.data.find((h) => h.task_id === id);
        if (item) {
          images.value =
            item.local_paths?.map((path, i) => ({
              id: i,
              url: extractImageUrl(path),
              status: "done",
            })) || [];
          prompt.value = item.prompt || item.description || "";
        } else {
          images.value = [];
          prompt.value = "记录不存在";
        }
      }
    } catch (err) {
      console.error("加载失败", err);
      prompt.value = "加载失败";
    } finally {
      loading.value = false;
      mode.value = "load";
    }
  } else if (id) {
    mode.value = "load";
    loading.value = true;
    try {
      const res = await getHistory();
      if (res.success) {
        const item = res.data.find(
          (h) => h.id === Number(id) || h.task_id === id,
        );
        if (item) {
          images.value =
            item.local_paths?.map((path, i) => ({
              id: i,
              url: extractImageUrl(path),
              status: "done",
            })) || [];
          prompt.value = item.prompt || item.description || "";
        } else {
          images.value = [];
          prompt.value = "记录不存在";
        }
      }
    } catch (err) {
      console.error("加载历史记录失败", err);
      prompt.value = "加载失败";
    } finally {
      loading.value = false;
    }
  } else if (state?.images?.length > 0) {
    mode.value = "generate";
    images.value = state.images;
    prompt.value = state.prompt || "";
    loading.value = false;
  } else {
    mode.value = "load";
    images.value = [];
    prompt.value = "";
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});

watch(
  () => route.params.id,
  () => {
    loadData();
  },
);
</script>
<style scoped lang="less">
.result-view {
  height: 100%;
  width: 100%;

  display: flex;

  background: transparent;
}
</style>
