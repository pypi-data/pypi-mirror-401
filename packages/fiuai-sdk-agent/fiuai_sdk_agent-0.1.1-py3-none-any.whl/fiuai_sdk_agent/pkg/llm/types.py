# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import StrEnum
from pydantic import BaseModel, Field
from langchain_core.callbacks import BaseCallbackHandler


class LLMModel(StrEnum):
    """
    LLM Vendor类型
    
    模型名称直接使用 API 实际需要的格式
    """
    QWEN_TURBO = "qwen-turbo"
    QWEN_PLUS = "qwen-plus"
    QWEN_MAX = "qwen-max"
    QWEN_INTENT = "qwen-intent"
    OCR = "qwen-vl-plus"
    # DS_V3 = "deepseek-chat"
    # DS_R1 = "deepseek-reasoner"
    DS_V32 = "deepseek-v3.2-exp"
    # DS_R1 = "deepseek-reasoner"
    EMBEDDING = "embedding"
    MAXBAI_EMBEDDING = "maxbai_embedding"

    def get_vendor_name(self) -> str:
        """
        Get the vendor name
        """
        match self:
            case LLMModel.MAXBAI_EMBEDDING:
                return "local"
            # case LLMModel.DS_V3 | LLMModel.DS_R1:
            #     return "deepseek"
            case _:
                return "ali"



@dataclass
class LLMRequestConfig:
    """
    单个 LLM 请求配置
    
    用于多模型并发调用场景
    """
    model: LLMModel
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    streaming: bool = False
    max_retries: Optional[int] = None
    timeout: Optional[int] = None
    callbacks: Optional[List[BaseCallbackHandler]] = None
    # 可选：为每个请求指定唯一标识
    request_id: Optional[str] = None


@dataclass
class LLMResponse:
    """
    LLM 响应结果
    
    用于多模型并发调用的返回结果
    """
    request_id: Optional[str]
    model: LLMModel
    content: Any  # 响应内容，类型取决于调用方式
    success: bool
    error: Optional[str] = None
    token_usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None


class LLMVendor(BaseModel):
    """
    LLM Vendor配置
    """
    name: str = Field(..., description="LLM提供者名称")
    base_url: str = Field(..., description="Base URL")
    api_key: str = Field(..., description="API Key")
    timeout: Optional[int] = Field(default=600, description="超时时间(秒)")
    temperature: Optional[float] = Field(default=0.7, description="温度参数")
    max_tokens: Optional[int] = Field(default=None, description="最大token数")
