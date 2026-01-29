# -- coding: utf-8 --
# Project: knowlege
# Created Date: 2025 12 Th
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional

from fiuai_sdk_python.utils.logger import get_logger
from ..types.knowledge_type import StaticKnowledge
from ...utils.errors import FiuaiAgentError

logger = get_logger(__name__)

# 全局实例
_static_knowledge: Optional[StaticKnowledge] = None


def init_static_knowledge(
    data: StaticKnowledge
):
    """
    初始化全局 StaticKnowledge 实例
    
    Args:
        data: StaticKnowledge 实例
    """
    global _static_knowledge
    
    _static_knowledge = data

def get_static_knowledge() -> StaticKnowledge:
    """
    获取全局 StaticKnowledge 实例
    
    Returns:
        StaticKnowledge: 全局实例
    
    Raises:
        FiuaiAgentError: 如果实例未初始化
    """
    global _static_knowledge
    
    if _static_knowledge is None:
        raise FiuaiAgentError(
            "StaticKnowledge not initialized. Please call init_static_knowledge() first",
        )
    
    return _static_knowledge


def reset_static_knowledge() -> None:
    """
    重置全局 StaticKnowledge 实例（主要用于测试）
    """
    global _static_knowledge
    _static_knowledge = None
    logger.info("StaticKnowledge instance reset")

