# -- coding: utf-8 --
# Project: agents
# Created Date: 2025 11 Sa
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage


from ..utils.errors import FiuaiAgentError

from ..pkg.llm.types import LLMModel
from ..pkg.llm.manager import LLMManager, LLMRequestConfig, LLMResponse
from ..pkg.llm.callbacks.agent_callback import AgentLLMCallback
from ..pkg.llm.callbacks.debug_callback import LLMDebugCallback
from ..pkg.llm.callbacks.local_log_callback import LLMLocalLogCallback
from ..pkg.user_context import UserContext, get_user_context

from .context.context_manager import AgentContextManager, AgentSummary
from .prompts.load import PromptService

from .types.knowledge_type import StaticKnowledge
from .types import AgentType


class Agent(ABC):
    """
    Agent基类
    
    支持默认 LLM 配置和实例管理(通过 LLMManager):
    - 子类可以定义默认的 LLM 模型和配置
    - 支持统一的 callback 管理(默认 + 覆盖)
    - 支持 LLM 实例缓存
    - 自动统计 token 使用情况(通过 LLMManager)
    
    支持上下文管理:
    - context_manager: 上下文管理器（可选）
    - 支持消息历史管理、上下文总结等
    
    支持静态知识库:
    - static_knowledge: 静态知识库（子类需要实现 set_static_knowledge）
    """
    
    # 子类可以覆盖这些类属性来定义默认配置
    _default_llm_model: Optional[LLMModel] = None
    _default_llm_config: Dict[str, Any] = {
        "temperature": 0.3,
        "max_tokens": 4096,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "streaming": False,
        "max_retries": 3,
        "timeout": 600,
    }

    def __init__(self, 
            name: str,
            semantic: str,
            type: AgentType,
            task_id: str,
            thread_id: str,
            task_name: str = "default",
            enable_context: bool = True,  # 是否启用上下文管理
            max_context_tokens: int = 32000,  # 上下文最大 token 数
            extra_callbacks: Optional[List[BaseCallbackHandler]] = None,  # 额外的 callbacks
        ):
        """
        Initialize the agent
        
        Args:
            name: Agent 名称
            semantic: Agent 语义描述
            type: Agent 类型
            task_id: 任务 ID（用于日志统计）
            task_name: 任务名称（用于日志统计），默认值 "default"
            thread_id: 线程 ID（用于日志统计）
            enable_context: 是否启用上下文管理（DomainAgent 通常需要，ServiceAgent 可能不需要）
            max_context_tokens: 上下文最大 token 数，超过此值会触发 context_summary
        """
        self.name = name
        self.semantic = semantic
        self.type = type
        self.task_id = task_id
        self.task_name = task_name
        self.thread_id = thread_id


        self.static_knowledge: Optional[StaticKnowledge] = None

        # 创建 prompt 服务
        self.prompt_service = PromptService()

        # 创建当前用户上下文
        self.user_context = get_user_context()

        # 创建 LLM 管理器
        agent_type_str = self.type.value if hasattr(self.type, 'value') else str(self.type)
        self.llm_manager = LLMManager(
            agent_name=self.name,
            agent_type=agent_type_str,
            agent_semantic=self.semantic,
            task_id=self.task_id,
            task_name=self.task_name,
            thread_id=self.thread_id,
            default_llm_model=self._default_llm_model,
            default_llm_config=self._default_llm_config,
        )
        
        # 创建上下文管理器（可选）
        self.context_manager: Optional[AgentContextManager] = None
        if enable_context:
            self.context_manager = AgentContextManager(
                agent_name=self.name,
                agent_type=agent_type_str,
                task_id=self.task_id,
                thread_id=self.thread_id,
                max_tokens=max_context_tokens,
            )
        
        # 创建默认 LLM 实例（如果有默认模型）
        self.llm: Optional[ChatOpenAI] = None
        self._default_llm_callbacks: Optional[List[BaseCallbackHandler]] = None
        if self._default_llm_model is not None:
            default_callbacks = self._get_default_callbacks(caller="common", extra_callbacks=extra_callbacks)
            self.llm = self.get_default_llm(callbacks=default_callbacks, caller="common")
            self._default_llm_callbacks = default_callbacks

        
        
        self.set_static_knowledge()


    #########################################################
    # 抽象 Methods
    #########################################################
    
    # 子类可以重写这些方法来实现具体功能

    # @abstractmethod
    def set_static_knowledge(self) -> None:
        """
        设置静态知识库
        """
        pass


    #########################################################
    # LLM 管理 Methods（委托给 LLMManager）
    #########################################################
    
    def set_default_callbacks(self, callbacks: List[BaseCallbackHandler]) -> None:
        """设置默认 callbacks（委托给 LLMManager）"""
        self.llm_manager.set_default_callbacks(callbacks)
    
    def add_default_callback(self, callback: BaseCallbackHandler) -> None:
        """添加默认 callback（委托给 LLMManager）"""
        self.llm_manager.add_default_callback(callback)
    
    def get_default_llm(
        self,
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        caller: str = "common",
        **override_config
    ) -> ChatOpenAI:
        """
        获取默认 LLM 实例（委托给 LLMManager）
        
        Args:
            callbacks: 可选的 callback 列表
            caller: 调用者标识，表示 agent 做什么操作，默认值 "common"
            **override_config: 其他配置参数
        """
        # 如果没有提供 callbacks，使用默认 callbacks 并设置 caller
        if callbacks is None:
            callbacks = self._get_default_callbacks(caller=caller)
        return self.llm_manager.get_default_llm(callbacks=callbacks, **override_config)
    
    def get_llm(
        self,
        model: Optional[LLMModel] = None,
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        caller: str = "common",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        streaming: Optional[bool] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[int] = None,
        use_cache: bool = True,
        replace_default: bool = False,
    ) -> ChatOpenAI:
        """
        创建或获取 LLM 实例（委托给 LLMManager）
        
        Args:
            model: LLM 模型，如果为 None 且 replace_default=True，则使用默认模型
            callbacks: 可选的 callback 列表
            caller: 调用者标识，表示 agent 做什么操作，默认值 "common"
            temperature: 温度参数
            max_tokens: 最大 token 数
            top_p: Top-p 参数
            frequency_penalty: 频率惩罚
            presence_penalty: 存在惩罚
            streaming: 是否流式输出
            max_retries: 最大重试次数
            timeout: 超时时间（秒）
            use_cache: 是否使用缓存
            replace_default: 是否替换默认 LLM 实例（self.llm）
            
        Returns:
            ChatOpenAI 实例
        """
        # 如果没有提供 callbacks，使用默认 callbacks 并设置 caller
        if callbacks is None:
            callbacks = self._get_default_callbacks(caller=caller)
        
        # 如果 replace_default=True，使用默认模型
        if replace_default and model is None:
            if self._default_llm_model is None:
                raise FiuaiAgentError(
                    "无法替换默认 LLM 实例：未定义默认 LLM 模型。"
                    "请在子类中设置 _default_llm_model 或提供 model 参数。"
                )
            model = self._default_llm_model
        
        # 如果未提供 model，使用默认模型
        if model is None:
            if self._default_llm_model is None:
                raise FiuaiAgentError(
                    "未提供 model 参数且未定义默认 LLM 模型。"
                    "请提供 model 参数或在子类中设置 _default_llm_model。"
                )
            model = self._default_llm_model
        
        llm = self.llm_manager.get_llm(
            model=model,
            callbacks=callbacks,
            caller=caller,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            streaming=streaming,
            max_retries=max_retries,
            timeout=timeout,
            use_cache=use_cache,
        )
        
        # 如果 replace_default=True，更新默认实例
        if replace_default:
            self.llm = llm
            # 保存 callbacks 引用以便后续更新 caller
            if callbacks:
                self._default_llm_callbacks = callbacks
        
        return llm
    
    def get_llm_statistics(self) -> Dict[str, Any]:
        """获取 LLM 使用统计信息（委托给 LLMManager）"""
        return self.llm_manager.get_statistics()
    
    def clear_llm_cache(self) -> None:
        """清空 LLM 实例缓存（委托给 LLMManager）"""
        self.llm_manager.clear_cache()
    
    def update_llm_caller(self, caller: str) -> None:
        """
        更新默认 LLM 实例的 caller
        
        只更新 self.llm 中 AgentLLMCallback 的 caller 属性，不创建新实例
        
        Args:
            caller: 新的调用者标识
            
        Raises:
            FiuaiAgentError: 如果默认 LLM 实例不存在
        """
        if self.llm is None:
            raise FiuaiAgentError(
                "默认 LLM 实例不存在。"
                "请先调用 get_llm() 或确保在初始化时创建了默认 LLM 实例。"
            )
        
        # 更新保存的 callbacks 中的 caller
        if self._default_llm_callbacks:
            for callback in self._default_llm_callbacks:
                if isinstance(callback, AgentLLMCallback):
                    callback.caller = caller
        
        # 同时尝试更新 LLM 实例中的 callbacks（如果可访问）
        if hasattr(self.llm, 'callbacks') and self.llm.callbacks:
            for callback in self.llm.callbacks:
                if isinstance(callback, AgentLLMCallback):
                    callback.caller = caller
    
    def _get_default_callbacks(
        self, 
        caller: str = "common",
        extra_callbacks: Optional[List[BaseCallbackHandler]] = None
    ) -> List[BaseCallbackHandler]:
        """
        获取默认 callbacks
        
        Args:
            caller: 调用者标识，表示 agent 做什么操作，默认值 "common"
            extra_callbacks: 额外的 callbacks 列表，会追加到默认 callbacks 后面
            
        Returns:
            默认 callback 列表，包含 AgentLLMCallback、LLMLocalLogCallback、LLMDebugCallback 和额外的 callbacks
        """
        callbacks = [
            AgentLLMCallback(
                agent_name=self.name,
                agent_type=self.type.value,
                agent_semantic=self.semantic,
                task_id=self.task_id,
                task_name=self.task_name,
                thread_id=self.thread_id,
                caller=caller,
            ),
            LLMLocalLogCallback(
                task_id=self.task_id,
                task_name=self.task_name,
                user_id=self.user_context.user_id if self.user_context else None,
                auth_tenant_id=self.user_context.auth_tenant_id if self.user_context else None,
                auth_company_id=self.user_context.auth_company_id if self.user_context else None,
            ),
            LLMDebugCallback(),
        ]
        
        # 添加额外的 callbacks
        if extra_callbacks:
            callbacks.extend(extra_callbacks)
        
        return callbacks
    #########################################################
    # 多模型并发调用 Methods（委托给 LLMManager）
    #########################################################
    
    async def invoke_llms_parallel(
        self,
        messages: List[BaseMessage],
        llm_configs: List[LLMRequestConfig],
        return_exceptions: bool = False,
    ) -> List[LLMResponse]:
        """并发调用多个 LLM 模型（委托给 LLMManager）"""
        return await self.llm_manager.invoke_llms_parallel(
            messages=messages,
            llm_configs=llm_configs,
            return_exceptions=return_exceptions,
        )
    
    async def invoke_llms_batch(
        self,
        message_batches: List[List[BaseMessage]],
        llm_configs: List[LLMRequestConfig],
        return_exceptions: bool = False,
    ) -> List[List[LLMResponse]]:
        """批量并发调用多个 LLM 模型（委托给 LLMManager）"""
        return await self.llm_manager.invoke_llms_batch(
            message_batches=message_batches,
            llm_configs=llm_configs,
            return_exceptions=return_exceptions,
        )
    
    #########################################################
    # 上下文管理 Methods
    #########################################################
    
    def add_message(self, message: BaseMessage) -> None:
        """
        添加消息到上下文历史
        
        Args:
            message: 消息对象
        """
        if self.context_manager:
            self.context_manager.add_message(message)
    
    def add_messages(self, messages: List[BaseMessage]) -> None:
        """
        批量添加消息到上下文历史
        
        Args:
            messages: 消息列表
        """
        if self.context_manager:
            self.context_manager.add_messages(messages)
    
    def get_messages(self, include_summaries: bool = True) -> List[BaseMessage]:
        """
        获取消息历史
        
        Args:
            include_summaries: 是否包含上下文总结
            
        Returns:
            消息列表
        """
        if self.context_manager:
            return self.context_manager.get_messages(include_summaries=include_summaries)
        return []
    
    def set_agent_summary(self, summary: AgentSummary) -> None:
        """
        设置 Agent 总结（用于传递给其他 Agent）
        
        Args:
            summary: Agent 总结对象
        """
        if self.context_manager:
            self.context_manager.set_agent_summary(summary)
    
    def get_agent_summary(self) -> Optional[AgentSummary]:
        """
        获取 Agent 总结
        
        Returns:
            AgentSummary 或 None
        """
        if self.context_manager:
            return self.context_manager.get_agent_summary()
        return None
    
    def export_context(self) -> Dict[str, Any]:
        """
        导出上下文（用于传递给其他 Agent）
        
        Returns:
            上下文数据字典
        """
        if self.context_manager:
            return self.context_manager.export_context()
        return {
            "agent_name": self.name,
            "agent_type": self.type.value if hasattr(self.type, 'value') else str(self.type),
            "task_id": self.task_id,
            "thread_id": self.thread_id,
        }
    
    def import_context(self, context_data: Dict[str, Any]) -> None:
        """
        导入上下文（从其他 Agent 接收）
        
        Args:
            context_data: 上下文数据字典
        """
        if self.context_manager:
            self.context_manager.import_context(context_data)
    