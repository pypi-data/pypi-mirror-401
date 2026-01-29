# -- coding: utf-8 --
# Project: fiuai-sdk-agent
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

CHUNK_DONE_STR = "[DONE]"
TASK_EVENT_STREAM_KEY_PREFIX = "task:events"


class EventType(Enum):
    """事件类型枚举"""
    # 普通markdown格式文本, 流式输出
    STR = "str"
    CHUNK = "chunk"
    # form数据,json格式, 用于填充表单
    DATA = "data"
    # 停止, 用于停止事件, 用于停止任务, 加入用户交互
    STOP = "stop"
    # 任务状态, 用于显示任务状态
    TASK = "task"
    # 警告, 用于显示警告信息
    WARNING = "warning"
    # 中断, 用于中断任务, 加入用户交互
    INTERRUPT = "interrupt"
    # 重定向, 用于发送浏览器重定向指令
    REDIRECT = "redirect"
    # 思考, 用于显示思考信息
    THINK = "think"
    # 未知, 用于未知事件
    UNKNOWN = "unknown"
    # 连接, 用于debug
    CONNECTED = "connected"
    # 心跳, 用于心跳事件, 和客户端保持keepalive
    HEARTBEAT = "heartbeat"

    #### v1.0
    # 计划列表, 用于显示计划列表json数据
    PLAN = "plan"
    # 步骤, 用于显示步骤消息
    STEP = "step"

    # 动作事件, 用于提示前端正在执行动作，action可能是自动执行,也可能是需要确认
    ACTION = "action"


class EventData(BaseModel):
    """事件元数据,发送到客户端时的格式"""
    event_id: str = Field(description="事件ID,用作增量消费时, 标识事件的唯一性")
    timestamp: datetime = Field(description="事件时间", default_factory=datetime.now)
    event_type: EventType = Field(description="事件类型")
    role: str = Field(description="执行角色")
    plan_id: Optional[str] = Field(description="计划ID, 为none表示不是在计划性任务中", default=None)
    step_id: Optional[str] = Field(description="步骤ID, 为none表示不是在计划性任务中", default=None)
    step_index: Optional[int] = Field(description="步骤索引, 为none表示不是在计划性任务中", default=None)
    step_status: Optional[str] = Field(description="步骤状态, 为none表示不是在计划性任务中", default=None)
    tags: Dict[str, Any] = Field(description="事件标签", default={})
    ttl: Optional[int] = Field(description="消息过期时间（秒）", default=None)
    data: str = Field(description="事件数据,若是结构体,需要进行json化", default="")
