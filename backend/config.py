"""
FastAPI 应用配置
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent.resolve()

# 图片保存目录
IMAGE_DIR = BASE_DIR / "image"
IMAGE_DIR.mkdir(exist_ok=True)

# API 配置
class Settings:
    """应用配置"""
    # 应用信息
    APP_NAME: str = "PixelForge - 2D 游戏素材生成 API"
    APP_VERSION: str = "1.0.0"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # API Key
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # 模型配置
    T2I_MODEL: str = "wan2.5-t2i-preview"  # 文生图模型
    I2I_MODEL: str = "qwen-image-edit-plus"  # 图生图模型
    
    # 图片配置
    DEFAULT_SIZE: str = "1024*1024"
    DEFAULT_STYLE: str = "像素风"
    MAX_REFERENCE_IMAGES: int = 3
    MAX_GENERATION_COUNT: int = 4
    
    # 风格关键词映射
    STYLE_KEYWORDS: dict[str, str] = {
        "像素风": "pixel art, pixelated, retro game style, 8-bit",
        "卡通": "cartoon style, cute, vibrant colors, clean lines",
        "手绘": "hand-drawn, sketch style, artistic",
        "扁平化": "flat design, minimal, simple shapes",
        "日系": "anime style, manga, Japanese game art",
        "写实": "realistic, detailed, lifelike"
    }
    
    # 素材类型关键词
    TYPE_KEYWORDS: dict[str, str] = {
        "character": "2D game character sprite, transparent background",
        "prop": "2D game item/prop, icon, transparent background",
        "background": "2D game background scene, game environment",
        "ui": "2D game UI element, button or panel",
        "tileset": "2D game tileset, map tile, seamless",
        "effect": "2D game VFX, magic effect, particle"
    }
    
    # 支持的尺寸
    SUPPORTED_SIZES: list[str] = [
        "1024*1024",
        "1280*1280",
        "1280*720",
        "1920*1080",
        "720*1280"
    ]


settings = Settings()
