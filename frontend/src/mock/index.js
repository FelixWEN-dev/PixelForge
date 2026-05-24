/**
 * Mock 数据 - 模拟后端 API 响应
 * 使用方式：import mockAPI from '@/mock'
 */

// 模拟网络延迟
function delay(ms = 800) {
  return new Promise((resolve) =>
    setTimeout(resolve, ms + Math.random() * 400),
  );
}

// 生成随机 ID
function generateId(prefix = "gen") {
  const now = new Date();
  const dateStr = now.toISOString().replace(/[-:T]/g, "").slice(0, 14);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${dateStr}_${random}`;
}

// 生成随机文件名
function generateFilename(assetType) {
  const now = new Date();
  const dateStr = now.toISOString().replace(/[-:T]/g, "").slice(0, 14);
  const random = Math.random().toString(36).substring(2, 10);
  return `${assetType}_${dateStr}_${random}.png`;
}

// ========== 历史记录存储（内存） ==========
const historyRecords = [];

// ========== 预设初始历史数据 ==========
function initPresetHistory() {
  if (historyRecords.length > 0) return;

  historyRecords.push(
    {
      id: 1,
      task_id: "gen_20240524001122_a1b2c3",
      asset_type: "character",
      description: "一个身穿银色盔甲的骑士，手持长剑",
      style: "像素风",
      size: "1024*1024",
      n: 1,
      watermark: 0,
      model: "wan2.5-t2i-preview",
      prompt:
        "pixel art style, game asset, character, a knight in silver armor holding a long sword, high quality, 2D game sprite",
      local_paths: [
        "D:/Projects/PixelForge/backend/image/character_20240524_001122_a1b2c3d4.png",
      ],
      status: "completed",
      created_at: "2024-05-24 00:11:22",
    },
    {
      id: 2,
      task_id: "gen_20240524002233_b2c3d4",
      asset_type: "background",
      description: "像素风格的森林场景，有阳光透过树叶",
      style: "像素风",
      size: "1920*1080",
      n: 1,
      watermark: 0,
      model: "wan2.5-t2i-preview",
      prompt:
        "pixel art style, game asset, background, forest scene with sunlight through leaves, high quality, 2D game background",
      local_paths: [
        "D:/Projects/PixelForge/backend/image/background_20240524_002233_b2c3d4e5.png",
      ],
      status: "completed",
      created_at: "2024-05-24 00:22:33",
    },
    {
      id: 3,
      task_id: "gen_20240524003344_c3d4e5",
      asset_type: "prop",
      description: "一把魔法法杖，杖顶镶嵌蓝色宝石",
      style: "卡通",
      size: "1024*1024",
      n: 2,
      watermark: 0,
      model: "wan2.5-t2i-preview",
      prompt:
        "cartoon style, game asset, prop, a magic staff with blue gem, high quality, 2D game sprite",
      local_paths: [
        "D:/Projects/PixelForge/backend/image/prop_20240524_003344_c3d4e5f6.png",
        "D:/Projects/PixelForge/backend/image/prop_20240524_003344_c3d4e5f7.png",
      ],
      status: "completed",
      created_at: "2024-05-24 00:33:44",
    },
    {
      id: 4,
      task_id: "gen_20240524004455_d4e5f6",
      asset_type: "ui",
      description: "游戏主菜单界面，复古像素风格按钮",
      style: "像素风",
      size: "1280*720",
      n: 1,
      watermark: 0,
      model: "wan2.5-t2i-preview",
      prompt:
        "pixel art style, game asset, ui, retro game main menu with buttons, high quality, 2D game UI",
      local_paths: [
        "D:/Projects/PixelForge/backend/image/ui_20240524_004455_d4e5f6g7.png",
      ],
      status: "completed",
      created_at: "2024-05-24 00:44:55",
    },
    {
      id: 5,
      task_id: "gen_20240524005566_e5f6g7",
      asset_type: "character",
      description: "一个可爱的像素风史莱姆怪物",
      style: "像素风",
      size: "1024*1024",
      n: 1,
      watermark: 1,
      model: "wan2.5-t2i-preview",
      prompt:
        "pixel art style, game asset, character, a cute slime monster, high quality, 2D game sprite",
      local_paths: [
        "D:/Projects/PixelForge/backend/image/character_20240524_005566_e5f6g7h8.png",
      ],
      status: "completed",
      created_at: "2024-05-24 00:55:66",
    },
  );
}

// 模块加载时初始化
initPresetHistory();

// ========== Mock API 实现 ==========

/**
 * Mock - 生成素材
 */
async function mockGenerateAsset(payload) {
  await delay(2000);

  const {
    asset_type = "character",
    description,
    style = "像素风",
    size = "1024*1024",
    n = 1,
    watermark = false,
  } = payload;

  const images = [];
  for (let i = 0; i < n; i++) {
    const filename = generateFilename(asset_type);
    images.push({
      url: `/image/${filename}`,
      local_path: `D:/Projects/PixelForge/backend/image/${filename}`,
      filename,
    });
  }

  const data = {
    images,
    task_id: generateId("gen"),
    prompt: `pixel art style, game asset, ${asset_type}, ${description}, high quality, 2D game sprite`,
    model: "wan2.5-t2i-preview",
  };

  // 存入历史记录
  historyRecords.unshift({
    id: historyRecords.length + 1,
    task_id: data.task_id,
    asset_type,
    description,
    style,
    size,
    n,
    watermark: watermark ? 1 : 0,
    model: data.model,
    prompt: data.prompt,
    local_paths: images.map((img) => img.local_path),
    status: "completed",
    created_at: new Date().toISOString().replace("T", " ").slice(0, 19),
  });

  return {
    success: true,
    data,
    error: null,
  };
}

/**
 * Mock - 获取历史记录
 */
async function mockGetHistory() {
  await delay(500);

  return {
    success: true,
    total: historyRecords.length,
    data: historyRecords,
    error: null,
  };
}

/**
 * Mock - 健康检查
 */
async function mockCheckHealth() {
  await delay(300);

  return {
    status: "healthy",
    api_key_configured: true,
  };
}

// ========== 导出 Mock API ==========

export const mockGenerate = (payload) => mockGenerateAsset(payload);
export const mockHistory = () => mockGetHistory();
export const mockHealth = () => mockCheckHealth();

export default {
  mockGenerate,
  mockHistory,
  mockHealth,
};
