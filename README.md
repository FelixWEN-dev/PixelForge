# PixelForge - AI 2D游戏素材生成工具
基于通大模型开发的 AI 2D 游戏素材自动生成系统，支持通过文本描述快速生成多风格、多类型游戏素材。

## 技术栈

- **前端**：Vue 3 + Vue Router + Tailwind CSS + Less
- **后端**：Python + LangChain + DashScope (qwen-image-edit-plus)
- **AI 模型**：通义万相 (wan2.5-t2i-preview)

## 功能特性

- 文本描述生成 2D 游戏素材
- 支持风格选择：像素风、卡通、手绘、扁平化、日系、写实
- 支持素材类型：角色、场景、道具
- 支持尺寸选择：1:1、16:9、高清、竖屏
- 支持透明背景选项
- 批量生成（1-4 张）
- 快捷提示词一键生成
- 图片下载功能

### 🎬 项目演示
演示视频：2D游戏素材生成.mp4
百度网盘链接：https://pan.baidu.com/s/1P6qkYcaZAr5mvuU-OINBPw
提取码：`pd4i`

## 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活环境（Windows）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 修改 .env 文件，将YOU_API_KEY修改为真正的阿里百炼平台api

# 启动服务
python main.py
```

后端服务默认运行在 `http://localhost:8000`

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run serve
```

前端服务默认运行在 `http://localhost:8080`

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/generate` | POST | 生成素材 |
| `/api/v1/history` | GET | 获取历史记录 |
| `/health` | GET | 健康检查 |

### 生成素材请求参数

```json
{
  "asset_type": "character",
  "description": "一个身穿银色盔甲的骑士",
  "style": "像素风",
  "size": "1024*1024",
  "n": 1,
  "watermark": false,
  "reference_images": []
}
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API 密钥 |
