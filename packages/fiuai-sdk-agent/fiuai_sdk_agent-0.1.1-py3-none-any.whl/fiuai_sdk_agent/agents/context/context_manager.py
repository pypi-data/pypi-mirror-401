# -- coding: utf-8 --
# Project: agents
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional, List, Dict, Any
from datetime import datetime

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from fiuai_sdk_python.utils.logger import get_logger
from .types import AgentSummary, ContextSummary

logger = get_logger(__name__)


class AgentContextManager:
    """
    Agent 上下文管理器
    
    负责管理 Agent 的对话上下文、消息历史、总结生成等
    支持多 Agent 体系中的上下文传递和管理
    """
    
    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        task_id: str,
        thread_id: str,
        max_tokens: int = 32000,  # 默认最大 token 数
        max_messages: Optional[int] = None,  # 最大消息数量（可选）
    ):
        """
        初始化上下文管理器
        
        Args:
            agent_name: Agent 名称
            agent_type: Agent 类型
            task_id: 任务 ID
            thread_id: 线程 ID
            max_tokens: 最大 token 数，超过此值会触发 context_summary
            max_messages: 最大消息数量（可选）
        """
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.task_id = task_id
        self.thread_id = thread_id
        self.max_tokens = max_tokens
        self.max_messages = max_messages
        
        # 消息历史
        self._messages: List[BaseMessage] = []
        
        # 上下文总结历史
        self._context_summaries: List[ContextSummary] = []
        
        # Agent 总结（用于传递给其他 Agent）
        self._agent_summary: Optional[AgentSummary] = None
        
        # 统计信息
        self._total_tokens = 0
        self._message_count = 0
    
    def add_message(self, message: BaseMessage) -> None:
        """
        添加消息到历史
        
        Args:
            message: 消息对象
        """
        self._messages.append(message)
        self._message_count += 1
        
        # 估算 token 数（简单估算：1 token ≈ 4 字符）
        if hasattr(message, 'content') and isinstance(message.content, str):
            estimated_tokens = len(message.content) // 4
            self._total_tokens += estimated_tokens
        
        # 检查是否需要总结
        if self._should_summarize():
            logger.debug(
                f"[ContextManager] {self.agent_name} context exceeds limit, "
                f"tokens={self._total_tokens}, messages={self._message_count}"
            )
            # TODO: 触发 context_summary 生成
    
    def add_messages(self, messages: List[BaseMessage]) -> None:
        """
        批量添加消息
        
        Args:
            messages: 消息列表
        """
        for message in messages:
            self.add_message(message)
    
    def get_messages(self, include_summaries: bool = True) -> List[BaseMessage]:
        """
        获取消息历史
        
        Args:
            include_summaries: 是否包含上下文总结
            
        Returns:
            消息列表
        """
        messages = []
        
        # 添加上下文总结（如果有）
        if include_summaries and self._context_summaries:
            for summary in self._context_summaries:
                summary_msg = SystemMessage(
                    content=f"[Context Summary] {summary.summary}"
                )
                messages.append(summary_msg)
        
        # 添加当前消息
        messages.extend(self._messages)
        
        return messages
    
    def clear_messages(self) -> None:
        """清空消息历史"""
        self._messages.clear()
        self._total_tokens = 0
        self._message_count = 0
    
    def set_agent_summary(self, summary: AgentSummary) -> None:
        """
        设置 Agent 总结
        
        Args:
            summary: Agent 总结对象
        """
        self._agent_summary = summary
        logger.debug(f"[ContextManager] {self.agent_name} agent summary set")
    
    def get_agent_summary(self) -> Optional[AgentSummary]:
        """
        获取 Agent 总结
        
        Returns:
            AgentSummary 或 None
        """
        return self._agent_summary
    
    def add_context_summary(self, summary: ContextSummary) -> None:
        """
        添加上下文总结
        
        Args:
            summary: 上下文总结对象
        """
        self._context_summaries.append(summary)
        
        # 清空已总结的消息（保留最近的几条）
        # TODO: 实现更智能的消息保留策略
        keep_recent = 5
        if len(self._messages) > keep_recent:
            self._messages = self._messages[-keep_recent:]
            # 重新计算 token 数
            self._total_tokens = sum(
                len(msg.content) // 4 
                for msg in self._messages 
                if hasattr(msg, 'content') and isinstance(msg.content, str)
            )
        
        logger.debug(
            f"[ContextManager] {self.agent_name} context summary added, "
            f"summaries={len(self._context_summaries)}"
        )
    
    def _should_summarize(self) -> bool:
        """
        判断是否需要生成上下文总结
        
        Returns:
            bool: 是否需要总结
        """
        # 检查 token 限制
        if self._total_tokens > self.max_tokens:
            return True
        
        # 检查消息数量限制
        if self.max_messages and self._message_count > self.max_messages:
            return True
        
        return False
    
    async def generate_context_summary(
        self,
        llm,
        messages_to_summarize: Optional[List[BaseMessage]] = None
    ) -> Optional[ContextSummary]:
        """
        生成上下文总结
        
        这是一个预留方法，未来实现时将通过 LLM 生成总结
        
        Args:
            llm: LLM 实例
            messages_to_summarize: 要总结的消息列表，如果为 None 则总结所有消息
            
        Returns:
            ContextSummary 或 None
        """
        # TODO: 实现上下文总结生成逻辑
        # 1. 选择要总结的消息（通常是旧消息）
        # 2. 使用 LLM 生成总结
        # 3. 创建 ContextSummary 对象
        # 4. 调用 add_context_summary 添加到历史
        
        logger.debug(
            f"[ContextManager] {self.agent_name} context summary generation "
            f"(not implemented yet)"
        )
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            Dict[str, Any]: 统计信息字典
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "task_id": self.task_id,
            "thread_id": self.thread_id,
            "message_count": self._message_count,
            "total_tokens": self._total_tokens,
            "context_summaries_count": len(self._context_summaries),
            "has_agent_summary": self._agent_summary is not None,
        }
    
    def export_context(self) -> Dict[str, Any]:
        """
        导出上下文（用于传递给其他 Agent）
        
        Returns:
            Dict[str, Any]: 上下文数据
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "task_id": self.task_id,
            "thread_id": self.thread_id,
            "agent_summary": self._agent_summary.model_dump() if self._agent_summary else None,
            "recent_messages": [
                {
                    "type": msg.__class__.__name__,
                    "content": msg.content if hasattr(msg, 'content') else str(msg)
                }
                for msg in self._messages[-10:]  # 只导出最近 10 条消息
            ],
            "context_summaries": [
                summary.model_dump() for summary in self._context_summaries
            ],
        }
    
    def import_context(self, context_data: Dict[str, Any]) -> None:
        """
        导入上下文（从其他 Agent）
        
        Args:
            context_data: 上下文数据
        """
        # 导入 agent_summary
        if context_data.get("agent_summary"):
            self._agent_summary = AgentSummary(**context_data["agent_summary"])
        
        # 导入上下文总结
        if context_data.get("context_summaries"):
            for summary_data in context_data["context_summaries"]:
                summary = ContextSummary(**summary_data)
                self._context_summaries.append(summary)
        
        logger.debug(
            f"[ContextManager] {self.agent_name} context imported from "
            f"{context_data.get('agent_name', 'unknown')}"
        )

