"""
素材生成 API 路由
"""

from fastapi import APIRouter, Header, HTTPException

from models.schemas import (
    GenerateRequest, GenerateResponse,
    HistoryListResponse, HistoryItem
)
from services.asset_service import asset_service
from models.database_models import SessionLocal, GenerationHistory


router = APIRouter(prefix="/api/v1", tags=["素材生成"])


# ========== 辅助函数 ==========

def get_current_user_id(authorization: str = Header(None)) -> int:
    """从 Authorization header 解析用户ID"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    
    token = authorization.replace("Bearer ", "")
    try:
        parts = token.split("_")
        if len(parts) >= 2:
            return int(parts[1])
    except:
        pass
    
    raise HTTPException(status_code=401, detail="登录已过期")


@router.post("/generate", response_model=GenerateResponse)
async def generate_asset(
    request: GenerateRequest,
    user_id: int = Header(..., alias="X-User-Id")
):
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
        watermark=request.watermark,
        user_id=user_id
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


@router.get("/history", response_model=HistoryListResponse)
async def get_history(user_id: int = Header(..., alias="X-User-Id")):
    """
    获取当前用户的生成历史记录（仅返回已完成的记录）
    """
    db = SessionLocal()
    try:
        # 查询当前用户 status 为 completed 的记录
        records = db.query(GenerationHistory).filter(
            GenerationHistory.user_id == user_id,
            GenerationHistory.status == "completed"
        ).order_by(GenerationHistory.created_at.desc()).all()

        # 转换为响应模型
        history_items = []
        for record in records:
            history_items.append(HistoryItem(
                id=record.id,
                task_id=record.task_id,
                asset_type=record.asset_type,
                description=record.description,
                style=record.style,
                size=record.size,
                n=record.n,
                watermark=record.watermark,
                model=record.model,
                prompt=record.prompt,
                local_paths=record.local_paths or [],
                status=record.status,
                created_at=record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ))

        return HistoryListResponse(
            success=True,
            total=len(history_items),
            data=history_items
        )
    except Exception as e:
        return HistoryListResponse(
            success=False,
            total=0,
            data=[],
            error=str(e)
        )
    finally:
        db.close()
