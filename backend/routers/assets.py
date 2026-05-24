"""
素材生成 API 路由
"""

from fastapi import APIRouter

from models.schemas import GenerateRequest, GenerateResponse
from services.asset_service import asset_service


router = APIRouter(prefix="/api/v1", tags=["素材生成"])


@router.post("/generate", response_model=GenerateResponse)
async def generate_asset(request: GenerateRequest):
    """
    生成2D游戏素材

    支持文生图和图生图两种模式：
    - 无参考图：使用文生图模型 (wan2.5-t2i-preview)
    - 有参考图：使用图生图模型 (qwen-image-edit-plus)
    """
    result = asset_service.generate_asset(
        asset_type=request.asset_type,
        description=request.description,
        style=request.style,
        size=request.size,
        reference_images=request.reference_images,
        n=request.n,
        negative_prompt=request.negative_prompt,
        watermark=request.watermark
    )

    if result.get("success"):
        return GenerateResponse(
            success=True,
            data=result["data"]
        )
    else:
        return GenerateResponse(
            success=False,
            error=result.get("error", "生成失败")
        )
