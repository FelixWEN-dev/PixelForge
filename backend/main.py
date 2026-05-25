"""
PixelForge - 2D 游戏素材生成 API (FastAPI)

基于 FastAPI 框架，封装阿里云 DashScope API (wan2.5-t2i-preview / qwen-image-edit-plus)
支持文生图和图生图两种模式
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

from config import settings, IMAGE_DIR
from routers.assets import router as assets_router
from routers.auth import router as auth_router


class CORSStaticFiles(StaticFiles):
    """带 CORS 头的静态文件处理器"""
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        # 为所有响应添加 CORS 头（包括 404）
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    
    async def __call__(self, scope, receive, send):
        # 处理 OPTIONS 预检请求
        if scope["type"] == "http" and scope["method"] == "OPTIONS":
            response = Response(
                content="",
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                }
            )
            await response(scope, receive, send)
            return
        await super().__call__(scope, receive, send)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时检查配置
    if not settings.DASHSCOPE_API_KEY:
        print("⚠️  警告：未设置 DASHSCOPE_API_KEY 环境变量")
        print("   请在 .env 文件中添加：DASHSCOPE_API_KEY=your-api-key")
    else:
        print(f"✅ API Key 已配置: {settings.DASHSCOPE_API_KEY[:10]}...")
    
    print(f"📁 图片保存目录: {IMAGE_DIR}")
    print(f"🚀 服务启动: http://{settings.HOST}:{settings.PORT}")
    
    yield
    
    # 关闭时清理
    print("👋 服务关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    2D 游戏素材生成 API
    
    ## 功能
    - 文生图：根据文本描述生成游戏素材
    - 图生图：基于参考图片生成素材
    - 支持多种素材类型：角色、道具、背景、UI、瓦片、特效
    - 支持多种风格：像素风、卡通、手绘、扁平化、日系、写实
    
    ## 认证
    需要在 .env 文件中设置 DASHSCOPE_API_KEY 环境变量
    """,
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（图片）- 使用自定义 CORSStaticFiles
app.mount("/image", CORSStaticFiles(directory=IMAGE_DIR), name="images")

# 注册路由
app.include_router(assets_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    """根路径 - API 信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api_prefix": "/api/v1"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "api_key_configured": bool(settings.DASHSCOPE_API_KEY)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
