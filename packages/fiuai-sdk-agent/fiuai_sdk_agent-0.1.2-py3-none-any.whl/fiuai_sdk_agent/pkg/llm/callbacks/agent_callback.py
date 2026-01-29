# -- coding: utf-8 --
# Project: callbacks
# Created Date: 2025 12 Sa
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI



from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

from fiuai_sdk_python.utils.logger import get_logger
from ..settings import get_llm_settings
from ..price_config import get_model_price_config

logger = get_logger(__name__)


class AgentLLMCallback(BaseCallbackHandler):
    """
    Agent LLM 回调函数
    用于统计 token 使用情况，并记录 agent 相关信息
    """
    
    def __init__(
        self,
        agent_name: Optional[str] = None,
        agent_type: Optional[str] = None,
        agent_semantic: Optional[str] = None,
        task_id: Optional[str] = None,
        task_name: Optional[str] = None,
        thread_id: Optional[str] = None,
        caller: str = "common",
        user_id: Optional[str] = None,
        auth_tenant_id: Optional[str] = None,
        auth_company_id: Optional[str] = None,
    ):
        """
        初始化回调函数
        
        Args:
            agent_name: Agent 名称
            agent_type: Agent 类型
            agent_semantic: Agent 语义描述
            task_id: 任务 ID
            task_name: 任务名称
            thread_id: 线程 ID
            caller: 调用者标识，表示 agent 做什么操作，默认值 "common"
            user_id: 用户 ID（由 agent 类注入）
            auth_tenant_id: 租户 ID（由 agent 类注入）
            auth_company_id: 公司 ID（由 agent 类注入）
        """
        super().__init__()
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.agent_semantic = agent_semantic
        self.task_id = task_id
        self.task_name = task_name
        self.thread_id = thread_id
        self.caller = caller
        self.user_id = user_id
        self.auth_tenant_id = auth_tenant_id
        self.auth_company_id = auth_company_id
        self.model = "unknown"
        # 统计信息
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.request_count = 0
        self.total_cost = 0.0  # 总费用（元）
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        # 价格配置
        self._price_config = get_model_price_config()
        self.settings = get_llm_settings()
    
    def _format_agent_name(self) -> str:
        """格式化 agent_name，如果为 None 则返回 'N/A'"""
        return self.agent_name if self.agent_name else "N/A"
        
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        """LLM 请求开始"""
        self.request_count += 1
        self.start_time = datetime.now()
        
        # 从 kwargs 中获取模型信息（如果未在初始化时提供）
        if not self.model and "invocation_params" in kwargs:
            invocation_params = kwargs.get("invocation_params", {})
            self.model = invocation_params.get("model", "unknown")
        
        try:
        # 序列化消息用于日志
            serialized_messages = [
                [msg.model_dump(mode="json") for msg in msg_list]
                for msg_list in messages
            ]
            
            logger.debug(
                f"[LLM Request] agent={self._format_agent_name()}, "
                f"type={self.agent_type}, model={self.model}, "
                f"task_id={self.task_id}, thread_id={self.thread_id}, caller={self.caller}, "
                f"messages={len(messages)}"
            )
        except Exception as e:
            logger.warning(f"Failed to serialize messages: {e}")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """LLM 请求结束"""
        self.end_time = datetime.now()
        
        try:
            # 提取 token 使用信息
            serialized_response = response.model_dump(mode="json")
            llm_output = serialized_response.get("llm_output", {})
            token_usage = llm_output.get("token_usage", {}) if isinstance(llm_output, dict) else {}
            
            # 累计 token 使用
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)
            
            self.prompt_tokens += prompt_tokens
            self.completion_tokens += completion_tokens
            self.total_tokens += total_tokens
            
            # 计算费用
            cost = None
            if self.model:
                cost = self._price_config.calculate_cost(
                    model_name=self.model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
                if cost is not None:
                    self.total_cost += cost
            
            # 计算耗时
            duration = None
            if self.start_time and self.end_time:
                duration = (self.end_time - self.start_time).total_seconds()
            
            # 记录日志
            cost_str = f"cost={cost:.6f}CNY" if cost is not None else "cost=N/A"
            duration_str = f"duration={duration:.2f}s" if duration else "duration=N/A"
            logger.info(
                f"[LLM Usage] agent={self._format_agent_name()}, "
                f"type={self.agent_type}, model={self.model}, "
                f"task_id={self.task_id}, thread_id={self.thread_id}, caller={self.caller}, "
                f"prompt_tokens={prompt_tokens}, "
                f"completion_tokens={completion_tokens}, "
                f"total_tokens={total_tokens}, "
                f"{duration_str}, {cost_str}"
            )
            
            # 记录详细日志
            if self.settings.LLM_LOGGING:
                logger.debug(f"[LLM Response] agent={self._format_agent_name()}, response={serialized_response}")
                
        except Exception as e:
            logger.warning(f"Failed to extract token usage: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            Dict[str, Any]: 统计信息字典
        """
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "agent_semantic": self.agent_semantic,
            "task_id": self.task_id,
            "thread_id": self.thread_id,
            "caller": self.caller,
            "model": self.model,
            "request_count": self.request_count,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "duration": duration,
        }

    def reset(self):
        """重置统计信息"""
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.request_count = 0
        self.total_cost = 0.0
        self.start_time = None
        self.end_time = None

