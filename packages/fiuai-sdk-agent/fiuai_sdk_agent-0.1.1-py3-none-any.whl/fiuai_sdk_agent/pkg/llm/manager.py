# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional, List, Dict, Any
import json

from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage


from ..user_context import get_user_context
from .vendor import get_llm_vendor
from .types import LLMRequestConfig, LLMResponse, LLMModel
from .callbacks.agent_callback import AgentLLMCallback


class LLMManager:
    """
    LLM 管理器
    
    负责管理 LLM 实例的创建、缓存和配置
    """
    
    def __init__(
        self,
        agent_name: str,
        agent_type: str,
        agent_semantic: str,
        task_id: str,
        task_name: str,
        thread_id: str,
        default_llm_model: Optional[LLMModel] = None,
        default_llm_config: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化 LLM 管理器
        
        Args:
            agent_name: Agent 名称
            agent_type: Agent 类型
            agent_semantic: Agent 语义描述
            task_id: 任务 ID（用于日志统计）
            task_name: 任务名称（用于日志统计）
            thread_id: 线程 ID（用于日志统计）
            default_llm_model: 默认 LLM 模型
            default_llm_config: 默认 LLM 配置
            enable_logging: 是否启用日志记录
        """
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.agent_semantic = agent_semantic
        self.task_id = task_id
        self.task_name = task_name
        self.thread_id = thread_id
        # 默认配置
        self._default_llm_model = default_llm_model
        self._default_llm_config = default_llm_config or {
            "temperature": 0.3,
            "max_tokens": 4096,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "streaming": False,
            "max_retries": 3,
            "timeout": 600,
        }
        
        # LLM 实例缓存
        self._llm_cache: Dict[str, ChatOpenAI] = {}
        
        # 默认 callbacks（包含 agent 统计 callback）
        self._default_callbacks: List[BaseCallbackHandler] = [
            AgentLLMCallback(
                agent_name=self.agent_name,
                agent_type=self.agent_type,
                agent_semantic=self.agent_semantic,
                user_id=get_user_context().user_simple_auth_info.user_id,
                auth_tenant_id=get_user_context().user_simple_auth_info.auth_tenant_id,
                auth_company_id=get_user_context().user_simple_auth_info.current_company,
                task_id=self.task_id,
                task_name=self.task_name,
                thread_id=self.thread_id,
            )
        ]
    
    def set_default_callbacks(self, callbacks: List[BaseCallbackHandler]) -> None:
        """
        设置默认 callbacks
        
        Args:
            callbacks: Callback 列表，会替换现有的默认 callbacks
        """
        self._default_callbacks = callbacks
    
    def add_default_callback(self, callback: BaseCallbackHandler) -> None:
        """
        添加默认 callback
        
        Args:
            callback: 要添加的 callback
        """
        if callback not in self._default_callbacks:
            self._default_callbacks.append(callback)
    
    def get_default_llm(
        self,
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        caller: str = "common",
        **override_config
    ) -> ChatOpenAI:
        """
        获取默认 LLM 实例（使用默认配置）
        
        Args:
            callbacks: 可选的 callback 列表，如果提供则覆盖默认 callbacks
            caller: 调用者标识，表示 agent 做什么操作，默认值 "common"
            **override_config: 可选的配置覆盖参数
            
        Returns:
            ChatOpenAI 实例
            
        Raises:
            ValueError: 如果未定义默认模型
        """
        if self._default_llm_model is None:
            raise ValueError(
                f"LLMManager 未定义默认 LLM 模型。"
                "请在初始化时设置 default_llm_model 或使用 get_llm() 方法。"
            )
        
        # 合并默认配置和覆盖配置
        config = {**self._default_llm_config, **override_config}
        
        return self.get_llm(
            model=self._default_llm_model,
            callbacks=callbacks,
            caller=caller,
            **config
        )
    
    def get_llm(
        self,
        model: LLMModel,
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
    ) -> ChatOpenAI:
        """
        创建或获取 LLM 实例
        
        Args:
            model: LLM 模型
            callbacks: 可选的 callback 列表，如果提供则覆盖默认 callbacks
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
            
        Returns:
            ChatOpenAI 实例
        """
        # 使用默认配置填充未提供的参数
        config = {
            "temperature": temperature if temperature is not None else self._default_llm_config.get("temperature", 0.3),
            "max_tokens": max_tokens if max_tokens is not None else self._default_llm_config.get("max_tokens", 4096),
            "top_p": top_p if top_p is not None else self._default_llm_config.get("top_p", 1.0),
            "frequency_penalty": frequency_penalty if frequency_penalty is not None else self._default_llm_config.get("frequency_penalty", 0.0),
            "presence_penalty": presence_penalty if presence_penalty is not None else self._default_llm_config.get("presence_penalty", 0.0),
            "streaming": streaming if streaming is not None else self._default_llm_config.get("streaming", False),
            "max_retries": max_retries if max_retries is not None else self._default_llm_config.get("max_retries", 3),
            "timeout": timeout if timeout is not None else self._default_llm_config.get("timeout", 600),
        }
        
        # 生成缓存 key
        cache_key = f"{model.value if hasattr(model, 'value') else str(model)}:{json.dumps(config, sort_keys=True)}"
        
        # 如果使用缓存且存在，直接返回
        if use_cache and cache_key in self._llm_cache:
            return self._llm_cache[cache_key]
        
        # 获取 vendor 配置
        vendor_config = get_llm_vendor(model.get_vendor_name())
        
        # 确定使用的 callbacks
        final_callbacks = callbacks if callbacks is not None else self._default_callbacks
        
        # 更新 agent callback 中的模型信息和 caller
        for cb in final_callbacks:
            if isinstance(cb, AgentLLMCallback):
                cb.model = model.value if hasattr(model, 'value') else str(model)
                cb.caller = caller
        
        # 创建 LLM 实例
        llm = ChatOpenAI(
            model=model.value if hasattr(model, 'value') else str(model),
            base_url=vendor_config.base_url,
            api_key=vendor_config.api_key,
            temperature=config["temperature"],
            top_p=config["top_p"],
            frequency_penalty=config["frequency_penalty"],
            presence_penalty=config["presence_penalty"],
            max_tokens=config["max_tokens"],
            streaming=config["streaming"],
            max_retries=config["max_retries"],
            request_timeout=config["timeout"],
            callbacks=final_callbacks if final_callbacks else None,
        )
        
        # 缓存实例
        if use_cache:
            self._llm_cache[cache_key] = llm
        
        return llm
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取 LLM 使用统计信息
        
        Returns:
            Dict[str, Any]: 统计信息字典
        """
        stats = []
        for callback in self._default_callbacks:
            if isinstance(callback, AgentLLMCallback):
                stats.append(callback.get_statistics())
        
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "agent_semantic": self.agent_semantic,
            "task_id": self.task_id,
            "callbacks": stats,
        }
    
    def clear_cache(self) -> None:
        """清空 LLM 实例缓存"""
        self._llm_cache.clear()
    
    async def invoke_llms_parallel(
        self,
        messages: List[BaseMessage],
        llm_configs: List[LLMRequestConfig],
        return_exceptions: bool = False,
    ) -> List[LLMResponse]:
        """
        并发调用多个 LLM 模型，返回所有结果
        
        这是一个框架方法，暂时未实现具体逻辑。
        未来实现时，将支持：
        - 并发调用多个模型
        - 统一的消息输入
        - 独立的配置和 callback
        - 错误处理和超时控制
        - Token 使用统计
        
        Args:
            messages: 输入消息列表（所有模型共享）
            llm_configs: LLM 配置列表，每个配置对应一个模型调用
            return_exceptions: 是否在结果中包含异常（而不是抛出）
            
        Returns:
            List[LLMResponse]: 所有模型的响应结果列表，顺序与 llm_configs 一致
            
        Raises:
            NotImplementedError: 方法尚未实现
        """
        # TODO: 实现多模型并发调用逻辑
        # 1. 为每个配置创建 LLM 实例
        # 2. 使用 asyncio.gather 或类似机制并发调用
        # 3. 收集所有结果，包括成功和失败的
        # 4. 统计每个模型的 token 使用情况
        # 5. 返回统一格式的结果列表
        
        raise NotImplementedError(
            "invoke_llms_parallel 方法尚未实现。"
            "这是一个预留框架，用于支持多模型并发调用功能。"
        )
    
    async def invoke_llms_batch(
        self,
        message_batches: List[List[BaseMessage]],
        llm_configs: List[LLMRequestConfig],
        return_exceptions: bool = False,
    ) -> List[List[LLMResponse]]:
        """
        批量并发调用多个 LLM 模型
        
        与 invoke_llms_parallel 的区别：
        - invoke_llms_parallel: 所有模型使用相同的消息
        - invoke_llms_batch: 每个模型使用不同的消息批次
        
        这是一个框架方法，暂时未实现具体逻辑。
        
        Args:
            message_batches: 消息批次列表，每个批次对应一个模型
            llm_configs: LLM 配置列表，每个配置对应一个模型调用
            return_exceptions: 是否在结果中包含异常（而不是抛出）
            
        Returns:
            List[List[LLMResponse]]: 每个模型的响应结果列表
            
        Raises:
            NotImplementedError: 方法尚未实现
            ValueError: 如果 message_batches 和 llm_configs 长度不匹配
        """
        if len(message_batches) != len(llm_configs):
            raise ValueError(
                f"message_batches 和 llm_configs 长度不匹配: "
                f"{len(message_batches)} != {len(llm_configs)}"
            )
        
        # TODO: 实现批量多模型并发调用逻辑
        # 1. 为每个配置创建 LLM 实例
        # 2. 使用 asyncio.gather 并发调用，每个模型使用对应的消息批次
        # 3. 收集所有结果
        # 4. 返回统一格式的结果列表
        
        raise NotImplementedError(
            "invoke_llms_batch 方法尚未实现。"
            "这是一个预留框架，用于支持批量多模型并发调用功能。"
        )

