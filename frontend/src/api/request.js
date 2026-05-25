// 后端 API 地址
const API_BASE = "http://localhost:8000";
const API_PREFIX = "/api/v1";

// ========== 获取当前用户ID ==========
function getCurrentUserId() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  
  try {
    // token 格式: user_{user_id}_{username}
    const parts = token.split("_");
    if (parts.length >= 2) {
      return parts[1];
    }
  } catch (e) {
    console.error("[API] 解析 token 失败", e);
  }
  return null;
}

// ========== 通用请求封装 ==========
export async function request(url, options = {}) {
  try {
    const userId = getCurrentUserId();
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
    
    // 添加用户ID到请求头
    if (userId) {
      headers["X-User-Id"] = userId;
    }
    
    const response = await fetch(`${API_BASE}${url}`, {
      headers,
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
  return request(`${API_PREFIX}/generate`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * 获取历史记录
 */
export function getHistory() {
  return request(`${API_PREFIX}/history`, {
    method: "GET",
  });
}

/**
 * 健康检查
 */
export function checkHealth() {
  return request(`/health`, {
    method: "GET",
  });
}

/**
 * 图片 URL 工具
 */
export function getImageUrl(path) {
  if (!path) return "";

  // 如果已经是完整 URL（支持 http://, https:// 以及格式错误的 https//）
  if (
    path.startsWith("http://") ||
    path.startsWith("https://") ||
    path.startsWith("https//")
  ) {
    // 修复可能的格式错误
    if (path.startsWith("https//")) {
      return path.replace("https//", "https://");
    }
    return path;
  }

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
