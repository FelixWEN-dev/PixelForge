# 2D 游戏素材生成 API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

---

## 接口列表

### 1. 生成素材

生成 2D 游戏素材图片，支持文生图和图生图两种模式。

#### 请求

```http
POST /api/v1/generate
```

#### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `asset_type` | string | ✅ | - | 素材类型：`character`(角色)/`prop`(道具)/`background`(背景)/`ui`(UI元素)/`tileset`(瓦片)/`effect`(特效) |
| `description` | string | ✅ | - | 素材描述，例如"一个穿着盔甲的骑士，手持长剑" |
| `style` | string | ❌ | `像素风` | 艺术风格：`像素风`/`卡通`/`手绘`/`扁平化`/`日系`/`写实` |
| `size` | string | ❌ | `1024*1024` | 图片尺寸，支持：`1024*1024`/`1280*1280`/`1280*720`/`1920*1080`/`720*1280` |
| `reference_images` | array | ❌ | `[]` | 参考图片URL列表，最多3张。提供参考图时使用图生图模型 |
| `n` | int | ❌ | `1` | 生成数量，范围 1-4 |
| `negative_prompt` | string | ❌ | `""` | 负面提示词，排除不需要的元素 |
| `watermark` | bool | ❌ | `false` | 是否添加水印 |

#### 请求示例

**示例1：文生图（无参考图）**
```json
{
  "asset_type": "character",
  "description": "一个穿着盔甲的骑士，手持长剑",
  "style": "像素风",
  "size": "1024*1024",
  "n": 1
}
```

**示例2：图生图（有参考图）**
```json
{
  "asset_type": "character",
  "description": "按照这个风格生成一个穿着红色斗篷的法师",
  "style": "日系",
  "size": "1024*1024",
  "reference_images": [
    "https://example.com/reference1.png"
  ],
  "n": 1
}
```

**示例3：生成背景**
```json
{
  "asset_type": "background",
  "description": "奇幻森林场景，有发光的蘑菇和藤蔓",
  "style": "手绘",
  "size": "1920*1080",
  "n": 2
}
```

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `success` | bool | 请求是否成功 |
| `data` | object | 成功时返回的数据 |
| `data.images` | array | 生成的图片列表 |
| `data.images[].url` | string | 图片在线URL |
| `data.images[].local_path` | string | 本地保存路径 |
| `data.images[].filename` | string | 文件名 |
| `data.task_id` | string | 任务ID |
| `data.prompt` | string | 实际使用的完整提示词 |
| `data.model` | string | 使用的AI模型 |
| `error` | string | 失败时的错误信息 |

#### 成功响应示例

```json
{
  "success": true,
  "data": {
    "images": [
      {
        "url": "https://dashscope.oss-cn-shanghai.aliyuncs.com/xxx/xxx.png",
        "local_path": "D:\新项目\2D游戏素材生成\image\character_20240524_001122_a1b2c3d4.png",
        "filename": "character_20240524_001122_a1b2c3d4.png"
      }
    ],
    "task_id": "gen_20240524001122000000",
    "prompt": "一个穿着盔甲的骑士，手持长剑, 2D game character sprite, transparent background, pixel art, pixelated, retro game style, 8-bit, high quality, game art",
    "model": "wan2.5-t2i-preview"
  }
}
```

#### 失败响应示例

```json
{
  "success": false,
  "error": "API调用失败: Model not exist."
}
```

#### 错误码

| 错误信息 | 说明 |
|----------|------|
| `未设置 DASHSCOPE_API_KEY 环境变量` | API Key 未配置 |
| `Model not exist.` | 模型名称错误 |
| `url error, please check url！` | 参考图片URL无效 |
| `生成失败` | AI 生成过程中出错 |
| `生成超时` | 生成时间超过限制 |

---

### 2. 查询任务状态

查询素材生成任务的执行状态。

#### 请求

```http
GET /api/v1/tasks/{task_id}
```

#### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `task_id` | string | ✅ | 任务ID |

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `task_id` | string | 任务ID |
| `status` | string | 状态：`pending`/`processing`/`completed`/`failed` |
| `progress` | int | 进度百分比 0-100 |
| `result` | object | 完成时的结果数据 |
| `error` | string | 失败时的错误信息 |
| `created_at` | string | 创建时间 |
| `completed_at` | string | 完成时间 |

---

### 3. 获取素材列表

获取已生成的素材列表。

#### 请求

```http
GET /api/v1/assets?page=1&page_size=20&asset_type=character
```

#### 查询参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `page` | int | ❌ | `1` | 页码 |
| `page_size` | int | ❌ | `20` | 每页数量 |
| `asset_type` | string | ❌ | - | 筛选素材类型 |
| `style` | string | ❌ | - | 筛选风格 |

#### 响应示例

```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "data": [
    {
      "id": "asset_xxx",
      "filename": "character_20240524_001122_a1b2c3d4.png",
      "asset_type": "character",
      "style": "像素风",
      "url": "/image/character_20240524_001122_a1b2c3d4.png",
      "created_at": "2024-05-24T00:11:22"
    }
  ]
}
```

---

### 4. 删除素材

删除已生成的素材。

#### 请求

```http
DELETE /api/v1/assets/{asset_id}
```

#### 响应

```json
{
  "success": true,
  "message": "删除成功"
}
```

---

## 素材类型说明

| 类型 | 英文 | 适用场景 | 推荐尺寸 |
|------|------|----------|----------|
| 角色 | `character` | 游戏角色、NPC、敌人 | `1024*1024` |
| 道具 | `prop` | 武器、装备、消耗品 | `1024*1024` |
| 背景 | `background` | 游戏场景、地图背景 | `1920*1080`/`1280*720` |
| UI元素 | `ui` | 按钮、面板、血条 | `1024*1024` |
| 瓦片 | `tileset` | 地图瓦片、拼接素材 | `1024*1024` |
| 特效 | `effect` | 技能特效、魔法效果 | `1024*1024` |

---

## 风格说明

| 风格 | 英文关键词 | 效果描述 |
|------|------------|----------|
| 像素风 | `pixel art, pixelated, retro game style, 8-bit` | 复古像素游戏风格 |
| 卡通 | `cartoon style, cute, vibrant colors, clean lines` | 可爱卡通风格 |
| 手绘 | `hand-drawn, sketch style, artistic` | 手绘插画风格 |
| 扁平化 | `flat design, minimal, simple shapes` | 简洁扁平设计 |
| 日系 | `anime style, manga, Japanese game art` | 日式动漫风格 |
| 写实 | `realistic, detailed, lifelike` | 写实精细风格 |

---

## 尺寸说明

| 尺寸 | 宽高比 | 适用场景 |
|------|--------|----------|
| `1024*1024` | 1:1 | 角色、道具、图标 |
| `1280*1280` | 1:1 | 大尺寸角色、头像 |
| `1280*720` | 16:9 | 横版背景、场景 |
| `1920*1080` | 16:9 | 高清背景、主视觉 |
| `720*1280` | 9:16 | 竖版背景、手游场景 |

---

## 模型说明

| 模式 | 使用模型 | 说明 |
|------|----------|------|
| 文生图 | `wan2.5-t2i-preview` | 无参考图时使用，直接根据文本生成 |
| 图生图 | `qwen-image-edit-plus` | 有参考图时使用，基于参考图编辑生成 |

---

## 环境配置

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | ✅ | 阿里云 DashScope API Key |

### .env 文件示例

```ini
DASHSCOPE_API_KEY=sk-your-api-key-here
```

---

## 代码示例

### Python 调用

```python
import requests

# 文生图
response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "asset_type": "character",
        "description": "一个穿着盔甲的骑士",
        "style": "像素风",
        "size": "1024*1024"
    }
)
result = response.json()
print(result)

# 图生图
response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "asset_type": "character",
        "description": "按照这个风格生成法师",
        "style": "日系",
        "reference_images": ["https://example.com/ref.png"]
    }
)
result = response.json()
print(result)
```

### cURL 调用

```bash
# 文生图
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "character",
    "description": "一个穿着盔甲的骑士",
    "style": "像素风"
  }'

# 图生图
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "character",
    "description": "按照这个风格生成法师",
    "reference_images": ["https://example.com/ref.png"]
  }'
```

---

## 注意事项

1. **API Key 安全**: 不要将 API Key 硬编码在代码中，建议使用环境变量
2. **参考图片**: 最多支持 3 张参考图片，URL 必须可公开访问
3. **生成时间**: 文生图通常需要 5-15 秒，图生图可能需要更长时间
4. **图片保存**: 生成的图片会自动保存到 `image` 文件夹
5. **并发限制**: 根据阿里云账号的并发限制，避免同时发起过多请求
