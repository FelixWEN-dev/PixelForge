# PixelForge API 接口文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 前缀**: `/api/v1`
- **Content-Type**: `application/json`

---

## 1. 生成素材

生成 2D 游戏素材，支持文生图和图生图两种模式。

### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方法 | POST |
| 接口路径 | `/api/v1/generate` |

### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| asset_type | string | 是 | - | 素材类型：`character`(角色)、`prop`(道具)、`background`(背景)、`ui`(UI元素)、`tileset`(瓦片)、`effect`(特效) |
| description | string | 是 | - | 素材描述，长度 1-1000 字符 |
| style | string | 否 | 像素风 | 艺术风格：`像素风`、`卡通`、`手绘`、`扁平化`、`日系`、`写实` |
| size | string | 否 | 1024*1024 | 图片尺寸：`1024*1024`、`1280*1280`、`1280*720`、`1920*1080`、`720*1280` |
| reference_images | array | 否 | [] | 参考图片 URL 列表，最多 3 张 |
| n | integer | 否 | 1 | 生成数量，范围 1-4 |
| watermark | boolean | 否 | false | 是否添加水印 |

### 请求示例

```json
{
  "asset_type": "character",
  "description": "一个身穿银色盔甲的骑士，手持长剑",
  "style": "像素风",
  "size": "1024*1024",
  "reference_images": [],
  "n": 1,
  "watermark": false
}
```

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| data | object | 成功时返回的数据，失败时为 null |
| error | string | 失败时的错误信息，成功时为 null |

#### data 对象

| 参数名 | 类型 | 说明 |
|--------|------|------|
| images | array | 生成的图片列表 |
| task_id | string | 任务 ID |
| prompt | string | 实际使用的完整提示词 |
| model | string | 使用的 AI 模型 |

#### images 数组项

| 参数名 | 类型 | 说明 |
|--------|------|------|
| url | string | 图片在线 URL（相对路径，如 `/image/xxx.png`） |
| local_path | string | 本地保存的完整路径 |
| filename | string | 文件名 |

### 响应示例

**成功响应：**

```json
{
  "success": true,
  "data": {
    "images": [
      {
        "url": "/image/character_20240524_001122_a1b2c3d4.png",
        "local_path": "D:/.../PixelForge-main/backend/image/character_20240524_001122_a1b2c3d4.png",
        "filename": "character_20240524_001122_a1b2c3d4.png"
      }
    ],
    "task_id": "gen_20240524001122_a1b2c3",
    "prompt": "pixel art style, game asset, character, a knight in silver armor holding a long sword, high quality, 2D game sprite",
    "model": "wan2.5-t2i-preview"
  },
  "error": null
}
```

**失败响应：**

```json
{
  "success": false,
  "data": null,
  "error": "生成失败：API 调用超时"
}
```

### 图片访问

生成的图片可通过以下 URL 访问：

```
GET http://localhost:8000/image/{filename}
```

例如：
```
http://localhost:8000/image/character_20240524_001122_a1b2c3d4.png
```

---

## 2. 获取历史记录

获取所有已完成的生成历史记录，按时间倒序排列。

### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方法 | GET |
| 接口路径 | `/api/v1/history` |

### 请求参数

无

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| total | integer | 历史记录总数 |
| data | array | 历史记录列表 |
| error | string | 失败时的错误信息 |

#### data 数组项

| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | integer | 记录 ID |
| task_id | string | 任务 ID |
| asset_type | string | 素材类型 |
| description | string | 素材描述 |
| style | string | 艺术风格 |
| size | string | 图片尺寸 |
| n | integer | 生成数量 |
| watermark | integer | 是否加水印：0=无，1=有 |
| model | string | 使用的 AI 模型 |
| prompt | string | 完整提示词 |
| local_paths | array | 图片本地路径列表 |
| status | string | 状态：`completed` |
| created_at | string | 创建时间，格式：YYYY-MM-DD HH:MM:SS |

### 响应示例

**成功响应：**

```json
{
  "success": true,
  "total": 3,
  "data": [
    {
      "id": 1,
      "task_id": "gen_20240524001122_a1b2c3",
      "asset_type": "character",
      "description": "一个身穿银色盔甲的骑士",
      "style": "像素风",
      "size": "1024*1024",
      "n": 1,
      "watermark": 0,
      "model": "wan2.5-t2i-preview",
      "prompt": "pixel art style, game asset, character...",
      "local_paths": [
        "D:/.../PixelForge-main/backend/image/character_20240524_001122_a1b2c3d4.png"
      ],
      "status": "completed",
      "created_at": "2024-05-24 00:11:22"
    }
  ],
  "error": null
}
```

### 历史记录图片访问

历史记录中的 `local_paths` 存储的是完整本地路径，需要提取文件名后访问：

```javascript
// 从路径中提取文件名
const filename = localPath.split(/[\\/]/).pop();
// 拼接访问 URL
const imageUrl = `http://localhost:8000/image/${filename}`;
```

---

## 3. 健康检查

检查 API 服务运行状态。

### 接口信息

| 项目 | 内容 |
|------|------|
| 请求方法 | GET |
| 接口路径 | `/health` |

### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| status | string | 服务状态：`healthy` |
| api_key_configured | boolean | API Key 是否已配置 |

### 响应示例

```json
{
  "status": "healthy",
  "api_key_configured": true
}
```

---

## 错误码说明

| 错误场景 | 说明 |
|----------|------|
| 参数验证失败 | 请求参数不符合要求，如 description 为空、reference_images 超过 3 张等 |
| API 调用失败 | 调用 AI 模型接口失败 |
| 图片下载失败 | 生成成功但下载图片到本地失败 |
| 数据库错误 | 保存历史记录时出错 |

---

## 前端使用示例

### 生成素材

```javascript
const API_BASE = 'http://localhost:8000';

async function generateAsset() {
  const requestData = {
    asset_type: 'character',
    description: '一个身穿银色盔甲的骑士',
    style: '像素风',
    size: '1024*1024',
    reference_images: [],
    n: 1,
    watermark: false
  };

  const response = await fetch(`${API_BASE}/api/v1/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  });

  const data = await response.json();
  
  if (data.success) {
    // 获取图片完整 URL
    const imageUrl = `${API_BASE}${data.data.images[0].url}`;
    console.log('生成成功:', imageUrl);
  } else {
    console.error('生成失败:', data.error);
  }
}
```

### 获取历史记录

```javascript
async function loadHistory() {
  const response = await fetch(`${API_BASE}/api/v1/history`);
  const data = await response.json();

  if (data.success) {
    data.data.forEach(item => {
      // 提取文件名并拼接 URL
      const filename = item.local_paths[0].split(/[\\/]/).pop();
      const imageUrl = `${API_BASE}/image/${filename}`;
      console.log('历史记录图片:', imageUrl);
    });
  }
}
```
