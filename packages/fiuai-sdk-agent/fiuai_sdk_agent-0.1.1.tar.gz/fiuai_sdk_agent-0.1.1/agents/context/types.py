# -- coding: utf-8 --
# Project: agents
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class AgentSummary(BaseModel):
    """
    Agent 执行总结
    
    每个 DomainAgent 在执行完自身的 subgraph 时输出
    用作上下文传递给其他 Agent
    """
    agent_name: str = Field(..., description="Agent 名称")
    agent_type: str = Field(..., description="Agent 类型")
    task_id: Optional[str] = Field(default=None, description="任务 ID")
    
    # 执行结果
    status: str = Field(..., description="执行状态：success, failed, interrupted")
    summary: str = Field(..., description="执行总结文本")
    key_findings: List[str] = Field(default_factory=list, description="关键发现")
    actions_taken: List[str] = Field(default_factory=list, description="执行的动作")
    outputs: Dict[str, Any] = Field(default_factory=dict, description="输出数据")
    
    # 元数据
    started_at: Optional[datetime] = Field(default=None, description="开始时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    duration: Optional[float] = Field(default=None, description="耗时（秒）")
    
    # 上下文关联
    parent_agent: Optional[str] = Field(default=None, description="父 Agent（如 SuperAgent）")
    related_agents: List[str] = Field(default_factory=list, description="相关 Agent 列表")


class ContextSummary(BaseModel):
    """
    上下文总结
    
    当消息历史超过 token 限制时，对历史消息进行总结
    """
    agent_name: str = Field(..., description="Agent 名称")
    task_id: Optional[str] = Field(default=None, description="任务 ID")
    
    # 总结内容
    summary: str = Field(..., description="上下文总结文本")
    key_points: List[str] = Field(default_factory=list, description="关键要点")
    
    # 统计信息
    original_message_count: int = Field(..., description="原始消息数量")
    original_token_count: int = Field(..., description="原始 token 数量")
    summarized_token_count: int = Field(..., description="总结后的 token 数量")
    
    # 时间信息
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    time_range: Dict[str, Optional[datetime]] = Field(
        default_factory=lambda: {"start": None, "end": None},
        description="原始消息的时间范围"
    )

