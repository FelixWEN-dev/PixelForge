"""
Pydantic 数据模型定义
"""

from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    """生成素材请求模型"""
    asset_type: str = Field(
        ...,
        description="素材类型: character(角色)/prop(道具)/background(背景)/ui(UI元素)/tileset(瓦片)/effect(特效)"
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="素材描述"
    )
    style: str = Field(
        default="像素风",
        description="艺术风格: 像素风/卡通/手绘/扁平化/日系/写实"
    )
    size: str = Field(
        default="1024*1024",
        description="图片尺寸: 1024*1024/1280*1280/1280*720/1920*1080/720*1280"
    )
    reference_images: list[str] = Field(
        default=[],
        description="参考图片URL列表，最多3张"
    )
    n: int = Field(
        default=1,
        ge=1,
        le=4,
        description="生成数量，范围 1-4"
    )
    negative_prompt: str = Field(
        default="",
        description="负面提示词"
    )
    watermark: bool = Field(
        default=False,
        description="是否添加水印"
    )
    
    @field_validator('reference_images')
    @classmethod
    def validate_reference_images(cls, v: list[str]) -> list[str]:
        if len(v) > 3:
            raise ValueError('参考图片最多3张')
        return v


class ImageResult(BaseModel):
    """生成的图片结果"""
    url: str = Field(..., description="图片在线URL")
    local_path: str = Field(..., description="本地保存路径")
    filename: str = Field(..., description="文件名")


class GenerateData(BaseModel):
    """生成成功返回的数据"""
    images: list[ImageResult] = Field(..., description="生成的图片列表")
    task_id: str = Field(..., description="任务ID")
    prompt: str = Field(..., description="实际使用的完整提示词")
    model: str = Field(..., description="使用的AI模型")


class GenerateResponse(BaseModel):
    """生成素材响应模型"""
    success: bool = Field(..., description="请求是否成功")
    data: GenerateData | None = Field(None, description="成功时返回的数据")
    error: str | None = Field(None, description="失败时的错误信息")


class TaskStatus(BaseModel):
    """任务状态查询响应"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="状态: pending/processing/completed/failed")
    progress: int = Field(..., ge=0, le=100, description="进度百分比 0-100")
    result: GenerateData | None = Field(None, description="完成时的结果数据")
    error: str | None = Field(None, description="失败时的错误信息")
    created_at: str = Field(..., description="创建时间")
    completed_at: str | None = Field(None, description="完成时间")


class DeleteResponse(BaseModel):
    """删除响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="提示信息")


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = Field(default=False)
    error: str = Field(..., description="错误信息")


class HistoryItem(BaseModel):
    """历史记录单项"""
    id: int = Field(..., description="记录ID")
    task_id: str = Field(..., description="任务ID")
    asset_type: str = Field(..., description="素材类型")
    description: str = Field(..., description="描述")
    style: str = Field(..., description="风格")
    size: str = Field(..., description="尺寸")
    n: int = Field(..., description="生成数量")
    watermark: int = Field(..., description="是否加水印: 0=无, 1=有")
    model: str | None = Field(None, description="使用的AI模型")
    prompt: str | None = Field(None, description="完整提示词")
    local_paths: list[str] = Field(default=[], description="图片本地路径列表")
    status: str = Field(..., description="状态")
    created_at: str = Field(..., description="创建时间")


class HistoryListResponse(BaseModel):
    """历史记录列表响应"""
    success: bool = Field(..., description="请求是否成功")
    total: int = Field(..., description="总数")
    data: list[HistoryItem] = Field(..., description="历史记录列表")
    error: str | None = Field(None, description="错误信息")
