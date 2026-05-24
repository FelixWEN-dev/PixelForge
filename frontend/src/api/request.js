import { mockGenerate, mockHistory, mockHealth } from "@/mock/index.js";

// 后端 API 地址
const API_BASE = "";
const API_PREFIX = "";

// ========== Mock 开关 ==========
// 开发阶段设为 true 使用 Mock 数据，联调/生产时改为 false
let USE_MOCK = true;

export function setUseMock(useMock) {
  USE_MOCK = useMock;
}

export function isMockEnabled() {
  return USE_MOCK;
}

// ========== 通用请求封装 ==========
async function request(url, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${url}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    const data = await response.json();

    if (!data.success && data.success !== undefined) {
      throw new Error(data.error || "请求失败");
    }

    return data;
  } catch (error) {
    console.error("[API Error]", error);
    throw error;
  }
}

// ========== API 接口 ==========

/**
 * 生成素材
 */
export function generateAsset(payload) {
  if (USE_MOCK) {
    return mockGenerate(payload);
  }
  return request(`${API_PREFIX}/generate`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * 获取历史记录
 */
export function getHistory() {
  if (USE_MOCK) {
    return mockHistory();
  }
  return request(`${API_PREFIX}/history`, {
    method: "GET",
  });
}

/**
 * 健康检查
 */
export function checkHealth() {
  if (USE_MOCK) {
    return mockHealth();
  }
  return request(`/health`, {
    method: "GET",
  });
}

/**
 * 图片 URL 工具
 */
export function getImageUrl(path) {
  if (!path) return "";

  // 如果已经是完整 URL
  if (path.startsWith("http")) return path;

  return `${API_BASE}${path}`;
}

/**
 * 历史记录路径转换工具
 */
export function extractImageUrl(localPath) {
  if (!localPath) return "";

  const filename = localPath.split(/[\\/]/).pop();
  return `${API_BASE}/image/${filename}`;
}
