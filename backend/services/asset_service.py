"""
素材生成服务 - 基于 LangChain BaseTool
"""

import uuid
import json
from typing import Any
from datetime import datetime
from pathlib import Path

import requests
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import dashscope
from dashscope import ImageSynthesis, MultiModalConversation
from http import HTTPStatus

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings, IMAGE_DIR
from models.database_models import SessionLocal, GenerationHistory


class AssetGenerationInput(BaseModel):
    """素材生成输入参数"""
    asset_type: str = Field(
        description="素材类型: character(角色)/prop(道具)/background(背景)/ui(UI元素)/tileset(瓦片)/effect(特效)"
    )
    description: str = Field(description="素材描述，例如'一个拿着剑的战士'")
    style: str = Field(
        default="像素风",
        description="艺术风格: 像素风/卡通/手绘/扁平化/日系/写实"
    )
    size: str = Field(
        default="1024*1024",
        description="图片尺寸"
    )
    reference_images: list[str] = Field(
        default=[],
        description="参考图片URL列表（可选）"
    )
    n: int = Field(
        default=1,
        ge=1,
        le=4,
        description="生成数量"
    )
    negative_prompt: str = Field(
        default="",
        description="负面提示词"
    )
    watermark: bool = Field(
        default=False,
        description="是否添加水印"
    )


class AssetGeneratorTool(BaseTool):
    """
    2D 游戏素材生成工具 - 基于 LangChain BaseTool
    调用阿里云 DashScope API (wan2.5-t2i-preview / qwen-image-edit-plus)
    """
    name: str = "generate_2d_asset"
    description: str = "根据描述生成2D游戏素材图片，支持多模态输入（文本+参考图）"
    args_schema: type[BaseModel] = AssetGenerationInput

    # API 配置
    api_key: str = Field(default_factory=lambda: settings.DASHSCOPE_API_KEY)
    t2i_model: str = Field(default=settings.T2I_MODEL)
    i2i_model: str = Field(default=settings.I2I_MODEL)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dashscope.api_key = self.api_key
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    def _build_prompt(self, asset_type: str, description: str, style: str) -> str:
        """构建生成提示词"""
        style_kw = settings.STYLE_KEYWORDS.get(style, style)
        type_kw = settings.TYPE_KEYWORDS.get(asset_type, "2D game asset")
        return f"{description}, {type_kw}, {style_kw}, high quality, game art"

    def _build_messages(self, prompt: str, reference_images: list[str]) -> list[dict[str, Any]]:
        """构建多模态消息格式"""
        content = []
        for img_url in reference_images[:settings.MAX_REFERENCE_IMAGES]:
            content.append({"image": img_url})
        content.append({"text": prompt})
        return [{"role": "user", "content": content}]

    def _download_image(self, image_url: str, asset_type: str) -> Path | None:
        """下载图片到本地"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_id = uuid.uuid4().hex[:8]
            filename = f"{asset_type}_{timestamp}_{short_id}.png"
            filepath = IMAGE_DIR / filename
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath
        except Exception as e:
            print(f"下载图片失败: {e}")
            return None

    def _generate_task_id(self) -> str:
        """生成任务ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        short_id = uuid.uuid4().hex[:6]
        return f"gen_{timestamp}_{short_id}"

    def _run_text2image(
        self,
        prompt: str,
        asset_type: str,
        size: str = "1024*1024",
        watermark: bool = False
    ) -> dict[str, Any]:
        """文生图：使用 ImageSynthesis API"""
        try:
            response = ImageSynthesis.call(
                api_key=self.api_key,
                model=self.t2i_model,
                prompt=prompt,
                negative_prompt="",
                n=1,
                size=size,
                prompt_extend=True,
                watermark=watermark
            )

            if response.status_code == HTTPStatus.OK:
                results = response.output.results
                if results:
                    image_url = results[0].url
                    print(f"✅ API 返回图片: {image_url[:60]}...")
                    local_path = self._download_image(image_url, asset_type)
                    result = {
                        "success": True,
                        "image_url": image_url,
                    }
                    if local_path:
                        result["local_path"] = str(local_path)
                        result["filename"] = local_path.name
                        print(f"✅ 图片下载成功: {local_path.name}")
                    return result
                return {"success": False, "error": "响应中未找到图片"}
            else:
                return {"success": False, "error": f"API调用失败: {response.message}"}
        except Exception as e:
            return {"success": False, "error": f"文生图异常: {str(e)}"}

    def _run_image_edit(
        self,
        prompt: str,
        asset_type: str,
        reference_images: list[str],
        watermark: bool = False
    ) -> dict[str, Any]:
        """图生图/编辑：使用 qwen-image-edit-plus"""
        messages = self._build_messages(prompt, reference_images)
        parameters = {
            "watermark": watermark,
            "n": 1,
            "negative_prompt": ""
        }

        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.i2i_model,
            messages=messages,
            result_format='message',
            stream=False,
            **parameters
        )

        if response.get('status_code') == 200:
            output = response.get('output', {})
            choices = output.get('choices', [])
            if choices:
                message = choices[0].get('message', {})
                contents = message.get('content', [])
                for content in contents:
                    if 'image' in content:
                        image_url = content['image']
                        print(f"✅ API 返回图片: {image_url[:60]}...")
                        local_path = self._download_image(image_url, asset_type)
                        result = {
                            "success": True,
                            "image_url": image_url,
                        }
                        if local_path:
                            result["local_path"] = str(local_path)
                            result["filename"] = local_path.name
                            print(f"✅ 图片下载成功: {local_path.name}")
                        return result
            return {"success": False, "error": "响应中未找到图片"}
        else:
            return {"success": False, "error": response.get('message', 'API调用失败')}

    def _run(
        self,
        asset_type: str,
        description: str,
        style: str = "像素风",
        size: str = "1024*1024",
        reference_images: list[str] | None = None,
        n: int = 1,
        negative_prompt: str = "",
        watermark: bool = False
    ) -> str:
        """LangChain BaseTool 的抽象方法 - 执行素材生成（带数据库记录）"""
        if not self.api_key:
            return json.dumps({
                "success": False,
                "error": "未设置 DASHSCOPE_API_KEY 环境变量"
            }, ensure_ascii=False)

        reference_images = reference_images or []
        task_id = self._generate_task_id()
        prompt = self._build_prompt(asset_type, description, style)
        model = self.i2i_model if reference_images else self.t2i_model

        # 创建数据库会话
        db = SessionLocal()

        try:
            # 1. 插入记录，状态设为"生成中"
            history = GenerationHistory(
                task_id=task_id,
                asset_type=asset_type,
                description=description,
                style=style,
                size=size,
                n=n,
                watermark=1 if watermark else 0,
                model=model,
                prompt=prompt,
                local_paths=[],
                status="processing"
            )
            db.add(history)
            db.commit()
            print(f"📝 数据库记录已创建: {task_id}, 状态: processing")

            # 2. 生成图片
            images = []
            local_paths = []

            for i in range(n):
                if reference_images:
                    result = self._run_image_edit(prompt, asset_type, reference_images, watermark)
                else:
                    result = self._run_text2image(prompt, asset_type, size, watermark)

                if result.get("success"):
                    images.append({
                        "url": result["image_url"],
                        "local_path": result.get("local_path", ""),
                        "filename": result.get("filename", "")
                    })
                    if result.get("local_path"):
                        local_paths.append(result["local_path"])
                else:
                    # 生成失败，更新状态为 failed
                    history.status = "failed"  # type: ignore
                    db.commit()
                    print(f"❌ 生成失败: {task_id}, 状态: failed")
                    db.close()
                    return json.dumps({
                        "success": False,
                        "error": result.get("error", "生成失败"),
                        "task_id": task_id
                    }, ensure_ascii=False)

            # 3. 生成成功，更新状态为 completed
            history.status = "completed"  # type: ignore
            history.local_paths = local_paths  # type: ignore
            db.commit()
            print(f"✅ 生成完成: {task_id}, 状态: completed")
            db.close()

            return json.dumps({
                "success": True,
                "data": {
                    "images": images,
                    "task_id": task_id,
                    "prompt": prompt,
                    "model": model
                }
            }, ensure_ascii=False)

        except Exception as e:
            # 异常时更新状态为 failed
            try:
                history = db.query(GenerationHistory).filter_by(task_id=task_id).first()
                if history:
                    history.status = "failed"  # type: ignore
                    db.commit()
                    print(f"❌ 异常失败: {task_id}, 状态: failed, 错误: {e}")
            except:
                pass
            finally:
                db.close()

            return json.dumps({
                "success": False,
                "error": str(e),
                "task_id": task_id
            }, ensure_ascii=False)


class AssetService:
    """
    FastAPI 服务封装 - 使用 LangChain AssetGeneratorTool
    """
    def __init__(self):
        self.generator = AssetGeneratorTool()

    def generate_asset(
        self,
        asset_type: str,
        description: str,
        style: str = "像素风",
        size: str = "1024*1024",
        reference_images: list[str] | None = None,
        n: int = 1,
        negative_prompt: str = "",
        watermark: bool = False
    ) -> dict[str, Any]:
        """生成素材"""
        result = self.generator._run(
            asset_type=asset_type,
            description=description,
            style=style,
            size=size,
            reference_images=reference_images,
            n=n,
            negative_prompt=negative_prompt,
            watermark=watermark
        )
        return json.loads(result)


# 单例实例
asset_service = AssetService()
