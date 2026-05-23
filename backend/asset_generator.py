"""
2D 游戏素材生成器 - LangChain + qwen-image-edit-plus
"""

import os
import json
import uuid
from typing import Any
from datetime import datetime

import requests
from dotenv import load_dotenv
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from dashscope import MultiModalConversation
import dashscope

# 加载 .env 文件中的环境变量
load_dotenv()

# 图片保存目录
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "image")
os.makedirs(IMAGE_DIR, exist_ok=True)


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
    reference_images: list[str] = Field(
        default=[],
        description="参考图片URL列表（可选）"
    )


class AssetGenerator(BaseTool):
    """
    2D 游戏素材生成工具 - 调用 qwen-image-edit-plus API
    """
    name: str = "generate_2d_asset"
    description: str = "根据描述生成2D游戏素材图片，支持多模态输入（文本+参考图），返回图片URL"
    args_schema: type[BaseModel] | None = AssetGenerationInput
    
    # API 配置
    api_key: str = Field(default_factory=lambda: os.getenv("DASHSCOPE_API_KEY", ""))
    # 文生图模型（无参考图时使用）
    t2i_model: str = "wan2.5-t2i-preview"
    # 图生图/编辑模型（有参考图时使用）
    i2i_model: str = "qwen-image-edit-plus"
    
    # 风格关键词映射
    style_keywords: dict[str, str] = {
        "像素风": "pixel art, pixelated, retro game style, 8-bit",
        "卡通": "cartoon style, cute, vibrant colors, clean lines",
        "手绘": "hand-drawn, sketch style, artistic",
        "扁平化": "flat design, minimal, simple shapes",
        "日系": "anime style, manga, Japanese game art",
        "写实": "realistic, detailed, lifelike"
    }
    
    # 素材类型关键词
    type_keywords: dict[str, str] = {
        "character": "2D game character sprite, transparent background",
        "prop": "2D game item/prop, icon, transparent background",
        "background": "2D game background scene, game environment",
        "ui": "2D game UI element, button or panel",
        "tileset": "2D game tileset, map tile, seamless",
        "effect": "2D game VFX, magic effect, particle"
    }
    
    def _build_prompt(self, asset_type: str, description: str, style: str) -> str:
        """构建生成提示词"""
        style_kw = self.style_keywords.get(style, style)
        type_kw = self.type_keywords.get(asset_type, "2D game asset")
        
        return f"{description}, {type_kw}, {style_kw}, high quality, game art"
    
    def _build_messages(self, prompt: str, reference_images: list[str]) -> list[dict[str, Any]]:
        """构建多模态消息格式"""
        content = []
        
        # 添加参考图片（如果有）
        for img_url in reference_images:
            content.append({"image": img_url})
        
        # 添加文本提示
        content.append({"text": prompt})
        
        return [
            {
                "role": "user",
                "content": content
            }
        ]
    
    def _download_image(self, image_url: str, asset_type: str) -> str | None:
        """
        下载图片到本地 image 文件夹
        
        Args:
            image_url: 图片URL
            asset_type: 素材类型，用于文件名
            
        Returns:
            本地文件路径，下载失败返回 None
        """
        try:
            # 发送请求下载图片
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 生成文件名: 类型_时间戳_UUID.png
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            short_id = uuid.uuid4().hex[:8]
            filename = f"{asset_type}_{timestamp}_{short_id}.png"
            
            # 完整文件路径
            filepath = os.path.join(IMAGE_DIR, filename)
            
            # 保存图片
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            return filepath
            
        except Exception as e:
            print(f"下载图片失败: {e}")
            return None
    
    def _run(self, asset_type: str, description: str, style: str = "像素风", reference_images: list[str] | None = None) -> str:
        """执行素材生成"""
        
        reference_images = reference_images or []
        
        # 构建提示词
        prompt = self._build_prompt(asset_type, description, style)
        
        # 设置 API Key
        dashscope.api_key = self.api_key
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        
        try:
            # 根据是否有参考图选择不同的模型和调用方式
            if reference_images:
                # 有参考图：使用图生图/编辑模型
                return self._run_image_edit(prompt, asset_type, reference_images)
            else:
                # 无参考图：使用文生图模型
                return self._run_text2image(prompt, asset_type)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "prompt": prompt
            }, ensure_ascii=False)
    
    def _run_text2image(self, prompt: str, asset_type: str) -> str:
        """文生图：使用 ImageSynthesis API (wan2.5-t2i-preview)"""
        from dashscope import ImageSynthesis
        from http import HTTPStatus
        
        try:
            # 调用文生图 API
            response = ImageSynthesis.call(
                api_key=self.api_key,
                model=self.t2i_model,
                prompt=prompt,
                negative_prompt="",
                n=1,
                size="1024*1024",
                prompt_extend=True,
                watermark=False
            )
            
            # 检查响应状态
            if response.status_code == HTTPStatus.OK:
                results = response.output.results
                if results:
                    image_url = results[0].url
                    
                    # 下载图片到本地
                    local_path = self._download_image(image_url, asset_type)
                    
                    result = {
                        "success": True,
                        "image_url": image_url,
                        "prompt": prompt,
                        "model": self.t2i_model
                    }
                    
                    if local_path:
                        result["local_path"] = local_path
                        result["filename"] = os.path.basename(local_path)
                    
                    return json.dumps(result, ensure_ascii=False)
                
                return json.dumps({
                    "success": False,
                    "error": "响应中未找到图片",
                    "prompt": prompt
                }, ensure_ascii=False)
            else:
                return json.dumps({
                    "success": False,
                    "error": f"API调用失败: {response.message}",
                    "prompt": prompt,
                    "status_code": response.status_code
                }, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"文生图异常: {str(e)}",
                "prompt": prompt
            }, ensure_ascii=False)
    
    def _run_image_edit(self, prompt: str, asset_type: str, reference_images: list[str]) -> str:
        """图生图/编辑：使用 qwen-image-edit-plus"""
        # 构建消息
        messages = self._build_messages(prompt, reference_images)
        
        # 构建参数
        parameters = {
            "watermark": True,
            "n": 1,
            "negative_prompt": ""
        }
        
        # 调用多模态对话 API
        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.i2i_model,
            messages=messages,
            result_format='message',
            stream=False,
            **parameters
        )
        
        # 解析响应
        if response.get('status_code') == 200:
            output = response.get('output', {})
            choices = output.get('choices', [])
            
            if choices:
                message = choices[0].get('message', {})
                contents = message.get('content', [])
                
                for content in contents:
                    if 'image' in content:
                        image_url = content['image']
                        
                        # 下载图片到本地
                        local_path = self._download_image(image_url, asset_type)
                        
                        result = {
                            "success": True,
                            "image_url": image_url,
                            "prompt": prompt,
                            "model": self.i2i_model
                        }
                        
                        if local_path:
                            result["local_path"] = local_path
                            result["filename"] = os.path.basename(local_path)
                        
                        return json.dumps(result, ensure_ascii=False)
            
            return json.dumps({
                "success": False,
                "error": "响应中未找到图片",
                "prompt": prompt,
                "raw_response": response
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "success": False,
                "error": response.get('message', 'API调用失败'),
                "prompt": prompt
            }, ensure_ascii=False)


# 使用示例
if __name__ == "__main__":
    # 创建生成器（API Key 从 .env 文件自动加载）
    generator = AssetGenerator()
    
    # 检查 API Key 是否设置
    if not generator.api_key:
        print("错误：未设置 DASHSCOPE_API_KEY 环境变量")
        print("请确保 .env 文件存在且包含 API Key")
        exit(1)
    
    print(f"图片将保存到: {IMAGE_DIR}")
    print("=" * 50)
    
    # 示例1: 纯文本生成
    print("\n=== 示例1: 纯文本生成 ===")
    result = generator._run(
        asset_type="character",
        description="一个穿着盔甲的骑士，手持长剑",
        style="像素风"
    )
    
    # 解析结果并显示
    result_data = json.loads(result)
    if result_data.get("success"):
        print(f"✅ 生成成功!")
        print(f"   在线URL: {result_data.get('image_url')[:60]}...")
        if "local_path" in result_data:
            print(f"   本地文件: {result_data.get('local_path')}")
            print(f"   文件名: {result_data.get('filename')}")
    else:
        print(f"❌ 生成失败: {result_data.get('error')}")
    
    # 示例2: 带参考图片的多模态生成
    print("\n=== 示例2: 多模态生成（带参考图） ===")
    result2 = generator._run(
        asset_type="character",
        description="按照这个姿势和风格，生成一个穿着红色斗篷的法师",
        style="日系",
        reference_images=[
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"
        ]
    )
    
    # 解析结果并显示
    result_data2 = json.loads(result2)
    if result_data2.get("success"):
        print(f"✅ 生成成功!")
        print(f"   在线URL: {result_data2.get('image_url')[:60]}...")
        if "local_path" in result_data2:
            print(f"   本地文件: {result_data2.get('local_path')}")
            print(f"   文件名: {result_data2.get('filename')}")
    else:
        print(f"❌ 生成失败: {result_data2.get('error')}")
