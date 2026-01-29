# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-27
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import threading
from typing import List, Optional, Dict, Any, Callable

from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler

from fiuai_sdk_python.utils.logger import get_logger
from .types import LLMVendor

logger = get_logger(__name__)


class LLMConfig:
    """
    LLM配置单例类
    负责管理所有LLM Vendor配置和实例创建
    """
    _instance: Optional['LLMConfig'] = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._vendors: Dict[str, LLMVendor] = {}
                    cls._instance._callbacks: List[Callable] = []
                    cls._instance._debug_enabled: bool = False
                    cls._instance._tracing_enabled: bool = False
                    cls._instance._default_timeout: int = 600
        return cls._instance

    def __init__(self):
        # 单例模式，初始化逻辑在__new__中完成
        pass

    def initialize(
        self,
        configs: List[LLMVendor],
        debug: bool = False,
        tracing: bool = True,
        default_timeout: int = 600
    ):
        """
        初始化LLM配置
        
        Args:
            configs: LLM Vendor配置列表
            debug: 是否启用debug模式
            tracing: 是否启用追踪
            default_timeout: 默认超时时间(秒)
        """
        if LLMConfig._initialized and self._vendors:
            logger.warning("LLMConfig已经初始化，跳过重复初始化")
            return
        
        if not configs:
            raise ValueError("LLM Vendor配置列表不能为空")
        
        # 存储vendor配置
        for config in configs:
            if not isinstance(config, LLMVendor):
                raise TypeError(f"配置项必须是LLMVendor类型，当前类型: {type(config)}")
            
            if config.name in self._vendors:
                logger.warning(f"Vendor '{config.name}'已存在，将被覆盖")
            
            self._vendors[config.name] = config
            logger.info(f"注册LLM Vendor: {config.name}")
        
        # 设置全局配置
        self._debug_enabled = debug
        self._tracing_enabled = tracing
        self._default_timeout = default_timeout
        
        LLMConfig._initialized = True
        
        logger.info(f"LLMConfig初始化完成，共注册{len(self._vendors)}个Vendor")
        logger.info(f"Debug模式: {debug}, Tracing: {tracing}")

    def get_vendor(self, name: str) -> Optional[LLMVendor]:
        """
        获取指定名称的Vendor配置
        
        Args:
            name: Vendor名称
            
        Returns:
            LLMVendor配置，如果不存在返回None
        """
        return self._vendors.get(name)

    def list_vendors(self) -> List[str]:
        """
        列出所有已注册的Vendor名称
        
        Returns:
            Vendor名称列表
        """
        return list(self._vendors.keys())

    def add_callback(self, callback: Callable):
        """
        添加callback函数
        
        Args:
            callback: callback函数
        """
        if not callable(callback):
            raise TypeError("callback必须是可调用对象")
        
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            logger.info(f"添加LLM callback: {callback.__name__ if hasattr(callback, '__name__') else type(callback).__name__}")

    def remove_callback(self, callback: Callable):
        """
        移除callback函数
        
        Args:
            callback: callback函数
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            logger.info(f"移除LLM callback: {callback.__name__ if hasattr(callback, '__name__') else type(callback).__name__}")

    def get_callbacks(self) -> List[Callable]:
        """
        获取所有callback函数
        
        Returns:
            callback函数列表
        """
        return self._callbacks.copy()

    def set_debug(self, enabled: bool):
        """
        设置debug模式
        
        Args:
            enabled: 是否启用debug
        """
        self._debug_enabled = enabled
        logger.info(f"LLM Debug模式: {'启用' if enabled else '禁用'}")

    def is_debug_enabled(self) -> bool:
        """
        检查是否启用debug模式
        
        Returns:
            是否启用debug
        """
        return self._debug_enabled

    def set_tracing(self, enabled: bool):
        """
        设置tracing模式
        
        Args:
            enabled: 是否启用tracing
        """
        self._tracing_enabled = enabled
        logger.info(f"LLM Tracing模式: {'启用' if enabled else '禁用'}")

    def is_tracing_enabled(self) -> bool:
        """
        检查是否启用tracing模式
        
        Returns:
            是否启用tracing
        """
        return self._tracing_enabled

    def create_llm(self, vendor_name: str, **kwargs) -> Any:
        """
        创建LLM实例
        
        Args:
            vendor_name: Vendor名称
            **kwargs: 额外的LLM参数
            
        Returns:
            LLM实例
            
        Raises:
            ValueError: Vendor不存在时抛出
        """
        vendor = self.get_vendor(vendor_name)
        if not vendor:
            available = ", ".join(self.list_vendors())
            raise ValueError(f"Vendor '{vendor_name}'不存在，可用Vendor: {available}")
        
        # 构建LLM参数
        llm_params = {
            "base_url": vendor.base_url,
            "api_key": vendor.api_key,
            "timeout": kwargs.get("timeout", vendor.timeout or self._default_timeout),
            "temperature": kwargs.get("temperature", vendor.temperature),
        }
        
        if vendor.max_tokens:
            llm_params["max_tokens"] = vendor.max_tokens
        
        # 添加额外参数（包括model，如果提供的话）
        llm_params.update(kwargs)
        
        # 构建callbacks
        callbacks = []
        if self._callbacks:
            # 将自定义callbacks包装为BaseCallbackHandler
            for cb in self._callbacks:
                if isinstance(cb, BaseCallbackHandler):
                    callbacks.append(cb)
                else:
                    # 创建简单的callback handler
                    handler = _create_callback_handler(cb)
                    callbacks.append(handler)
        
        if callbacks:
            llm_params["callbacks"] = callbacks
        
        # 创建LLM实例
        llm = ChatOpenAI(**llm_params)
        
        if self._debug_enabled:
            model_info = f", model={llm_params.get('model', 'N/A')}" if 'model' in llm_params else ""
            logger.debug(f"创建LLM实例: vendor={vendor_name}{model_info}, params={llm_params}")
        
        return llm

    def get_default_timeout(self) -> int:
        """
        获取默认超时时间
        
        Returns:
            默认超时时间(秒)
        """
        return self._default_timeout


def _create_callback_handler(callback: Callable) -> BaseCallbackHandler:
    """
    创建callback handler包装器
    
    Args:
        callback: callback函数
        
    Returns:
        BaseCallbackHandler实例
    """
    class CallbackWrapper(BaseCallbackHandler):
        """Callback包装器"""
        
        def __init__(self, cb: Callable):
            super().__init__()
            self.cb = cb
        
        def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            *,
            run_id: Any = None,
            parent_run_id: Any = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any
        ):
            """LLM开始调用时触发"""
            try:
                if callable(self.cb):
                    # 尝试调用callback，支持不同签名
                    try:
                        self.cb(
                            event="on_llm_start",
                            serialized=serialized,
                            prompts=prompts,
                            run_id=run_id,
                            parent_run_id=parent_run_id,
                            tags=tags,
                            metadata=metadata,
                            **kwargs
                        )
                    except TypeError:
                        # 如果callback不支持这些参数，尝试只传递必要参数
                        try:
                            self.cb(event="on_llm_start", prompts=prompts)
                        except TypeError:
                            self.cb(prompts)
            except Exception as e:
                logger.error(f"Callback执行失败: {str(e)}")
        
        def on_llm_end(
            self,
            response: Any,
            *,
            run_id: Any = None,
            parent_run_id: Any = None,
            **kwargs: Any
        ):
            """LLM调用结束时触发"""
            try:
                if callable(self.cb):
                    try:
                        self.cb(
                            event="on_llm_end",
                            response=response,
                            run_id=run_id,
                            parent_run_id=parent_run_id,
                            **kwargs
                        )
                    except TypeError:
                        try:
                            self.cb(event="on_llm_end", response=response)
                        except TypeError:
                            self.cb(response)
            except Exception as e:
                logger.error(f"Callback执行失败: {str(e)}")
        
        def on_llm_error(
            self,
            error: Exception,
            *,
            run_id: Any = None,
            parent_run_id: Any = None,
            **kwargs: Any
        ):
            """LLM调用出错时触发"""
            try:
                if callable(self.cb):
                    try:
                        self.cb(
                            event="on_llm_error",
                            error=error,
                            run_id=run_id,
                            parent_run_id=parent_run_id,
                            **kwargs
                        )
                    except TypeError:
                        try:
                            self.cb(event="on_llm_error", error=error)
                        except TypeError:
                            self.cb(error)
            except Exception as e:
                logger.error(f"Callback执行失败: {str(e)}")
    
    return CallbackWrapper(callback)


# 全局单例实例
_llm_config: Optional[LLMConfig] = None


def get_llm_config() -> LLMConfig:
    """
    获取LLMConfig单例实例
    
    Returns:
        LLMConfig实例
    """
    global _llm_config
    if _llm_config is None:
        _llm_config = LLMConfig()
    return _llm_config


def init_llm_config(
    configs: List[LLMVendor],
    debug: bool = False,
    tracing: bool = True,
    default_timeout: int = 600
):
    """
    LLM Vendor配置初始化
    
    Args:
        configs: LLM Vendor配置列表
        debug: 是否启用debug模式
        tracing: 是否启用追踪
        default_timeout: 默认超时时间(秒)
    """
    config = get_llm_config()
    config.initialize(configs, debug=debug, tracing=tracing, default_timeout=default_timeout)