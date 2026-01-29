# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-27
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional

from fiuai_sdk_python.utils.logger import get_logger
from .types import LLMVendor
from .error import FiuaiLLMError

logger = get_logger(__name__)




def get_llm_vendor(vendor_name: str, **kwargs) -> LLMVendor:
    """
    获取LLM Vendor配置
    
    Args:
        vendor_name: Vendor名称
        **kwargs: 额外的LLM参数
        
    Returns:
        LLM Vendor配置
    """
    # 延迟导入避免循环依赖
    from .llm_config import get_llm_config
    config = get_llm_config()

    if not config:
        raise FiuaiLLMError("LLM Vendor not found")

    vendor = config.get_vendor(vendor_name)
    if not vendor:
        raise FiuaiLLMError(f"LLM Vendor '{vendor_name}' not found")

    return vendor