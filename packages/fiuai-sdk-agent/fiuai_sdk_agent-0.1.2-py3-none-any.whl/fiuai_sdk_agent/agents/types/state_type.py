# -- coding: utf-8 --
# Project: types
# Created Date: 2025 12 Tu
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from langchain_core.messages import BaseMessage
from ...pkg.user_context import UserContext
from .intent_type import UserIntent
from .plan_type import BasePlan

class BasicStateInfo(BaseModel):
    """基础状态信息,所有任务状态都需要实现"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # 允许序列化复杂类型
        ser_json_timedelta='iso8601',
    )
    
    thread_id: str = Field(description="会话线程ID")
    user_context: UserContext = Field(description="用户上下文")
    user_input: str = Field(description="用户本轮输入")
    chat_log_id: str = Field(description="聊天日志ID,对应AIChatLog.name")
    chat_history: List[BaseMessage] = Field(description="用户交互消息列表,仅包含用户提问和agent回答,不包含系统消息")

    intent: Optional[UserIntent] = Field(default=None, description="用户意图")
    plan: Optional[BasePlan] = Field(default=None, description="任务计划, 简单任务可以没有计划对象")

