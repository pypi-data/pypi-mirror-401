# -- coding: utf-8 --
# Project: fiuai-ai
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import json
from typing import Optional, Dict, Any, Union, Callable
from pydantic import BaseModel

from fiuai_sdk_python.utils.ids import gen_id

from ..types.event_type import EventType, EventData, CHUNK_DONE_STR
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # 类型提示时导入，避免循环依赖
    # EventManager 是业务层的，SDK 中不直接依赖
    EventManager = Any
from fiuai_sdk_python.utils.logger import get_logger

logger = get_logger(__name__)

# 每个chunk的大小
STR_SIZE_PER_CHUNK = 8


class EventPublisher:
    """事件发布器，负责将事件发布到事件服务器"""
    
    def __init__(
        self,
        task_id: str,
        thread_id: str,
        role: str = "assistant",
        event_manager: Optional[EventManager] = None,
        writer: Optional[Callable] = None,
        plan_id: Optional[str] = None,
        step_id: Optional[str] = None,
        step_index: Optional[int] = None,
        step_status: Optional[str] = None,
    ):
        """
        初始化事件发布器
        
        Args:
            task_id: 任务ID
            thread_id: 线程ID
            role: 执行角色
            event_manager: 事件管理器实例，如果为None则不会发布到Redis
            writer: langgraph的流式写入器，如果为None则不会使用writer
            plan_id: 计划ID（可选）
            step_id: 步骤ID（可选）
            step_index: 步骤索引（可选）
            step_status: 步骤状态（可选）
        """
        self.task_id = task_id
        self.thread_id = thread_id
        self.role = role
        self.event_manager = event_manager
        self.writer = writer
        self.plan_id = plan_id
        self.step_id = step_id
        self.step_index = step_index
        self.step_status = step_status
    
    def update_plan_info(
        self,
        plan_id: Optional[str] = None,
        step_id: Optional[str] = None,
        step_index: Optional[int] = None,
        step_status: Optional[str] = None,
    ) -> None:
        """
        更新计划相关信息
        
        Args:
            plan_id: 计划ID，只有当参数不为None时才更新
            step_id: 步骤ID，只有当参数不为None时才更新
            step_index: 步骤索引，只有当参数不为None时才更新
            step_status: 步骤状态，只有当参数不为None时才更新
            
        Note:
            如果需要清除字段，请使用 clear_plan_info() 方法
        """
        if plan_id is not None:
            self.plan_id = plan_id
        if step_id is not None:
            self.step_id = step_id
        if step_index is not None:
            self.step_index = step_index
        if step_status is not None:
            self.step_status = step_status
    
    def clear_plan_info(self) -> None:
        """
        清除所有计划相关信息（设置为None）
        """
        self.plan_id = None
        self.step_id = None
        self.step_index = None
        self.step_status = None
    
    def publish(
        self,
        data: Union[str, BaseModel, Dict[str, Any]],
        event_type: EventType = EventType.STR,
        tags: Optional[Dict[str, Any]] = None,
        ttl: int = 0,
    ) -> None:
        """
        发布事件到事件服务器
        
        Args:
            data: 事件数据，可以是字符串、BaseModel或字典
            event_type: 事件类型，默认为STR
            tags: 事件标签
            ttl: 消息过期时间（秒），0表示使用默认值
        """
        if tags is None:
            tags = {}
        
        # 如果事件类型是STR且数据不为空，拆分为chunk
        if event_type == EventType.STR and data != "":
            data_str = self._format_message(data)
            # 拆分为n个chunk
            for i in range(0, len(data_str), STR_SIZE_PER_CHUNK):
                chunk = data_str[i:i + STR_SIZE_PER_CHUNK]
                self._publish(
                    event_id=gen_id(),
                    event_type=EventType.CHUNK,
                    data=chunk,
                    tags=tags,
                    ttl=ttl,
                )
            
            # 额外发送一个结束符
            self._publish(
                event_id=gen_id(),
                event_type=EventType.CHUNK,
                data=CHUNK_DONE_STR,
                tags=tags,
                ttl=ttl,
            )
        else:
            self._publish(
                event_id=gen_id(),
                event_type=event_type,
                data=self._format_message(data),
                tags=tags,
                ttl=ttl,
            )
    
    def _publish(
        self,
        event_id: str,
        event_type: EventType,
        data: str,
        tags: Optional[Dict[str, Any]] = None,
        ttl: int = 0,
    ) -> None:
        """
        内部发布方法，实际执行发布操作
        
        Args:
            event_id: 事件ID
            event_type: 事件类型
            data: 事件数据（字符串）
            tags: 事件标签
            ttl: 消息过期时间（秒）
        """
        if tags is None:
            tags = {}
        
        # 创建EventData对象
        event_data = EventData(
            event_id=event_id,
            event_type=event_type,
            data=data,
            role=self.role,
            plan_id=self.plan_id,
            step_id=self.step_id,
            step_index=self.step_index,
            step_status=self.step_status,
            tags=tags,
            ttl=ttl if ttl > 0 else None,
        )
        
        # 如果提供了writer，使用writer发布（langgraph流式写入）
        if self.writer:
            try:
                self.writer(event_data.model_dump(mode="json"))
            except Exception as e:
                logger.error(f"Error publishing event via writer: {str(e)}")
        
        # 如果提供了event_manager，使用event_manager发布到Redis
        if self.event_manager:
            try:
                self.event_manager.publish_event(
                    event_type=event_type.value if hasattr(event_type, 'value') else str(event_type),
                    data=data,
                    role=self.role,
                    task_id=self.task_id,
                    plan_id=self.plan_id,
                    step_id=self.step_id,
                    step_index=self.step_index,
                    step_status=self.step_status,
                    tags=tags,
                    ttl=ttl if ttl > 0 else None,
                )
            except Exception as e:
                logger.error(f"Error publishing event via event_manager: {str(e)}")
    
    def _format_message(
        self,
        message: Union[str, BaseModel, Dict[str, Any]]
    ) -> str:
        """
        格式化消息，生成字符串
        
        Args:
            message: 消息对象，可以是字符串、BaseModel或字典
            
        Returns:
            格式化后的字符串
        """
        if isinstance(message, dict):
            return json.dumps(message, ensure_ascii=False)
        elif isinstance(message, BaseModel):
            return message.model_dump_json()
        else:
            return str(message)

