# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import threading
from typing import Optional


class LLMSettings:
    """
    LLM 设置单例类
    负责管理所有 LLM 相关的配置设置
    """
    _instance: Optional['LLMSettings'] = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._llm_tracing: bool = False
                    cls._instance._llm_timeout_seconds: int = 600
                    cls._instance._app_debug: bool = False
                    cls._instance._llm_logging: bool = False
                    cls._instance._log_path: Optional[str] = None
        return cls._instance

    def __init__(self):
        # 单例模式，初始化逻辑在__new__中完成
        pass

    def initialize(
        self,
        llm_tracing: bool = False,
        llm_timeout_seconds: int = 600,
        app_debug: bool = False,
        llm_logging: bool = False,
        log_path: Optional[str] = None,
    ):
        """
        初始化 LLM 设置
        
        Args:
            llm_tracing: 是否开启 LLM 追踪
            llm_timeout_seconds: LLM 超时时间（秒）
            app_debug: 是否开启调试模式
            llm_logging: 是否开启日志记录
            log_path: 日志文件路径
        """
        if LLMSettings._initialized and self._llm_tracing is not None:
            from utils import get_logger
            logger = get_logger(__name__)
            logger.warning("LLMSettings已经初始化，跳过重复初始化")
            return
        
        self._llm_tracing = llm_tracing
        self._llm_timeout_seconds = llm_timeout_seconds
        self._app_debug = app_debug
        self._llm_logging = llm_logging
        self._log_path = log_path

        LLMSettings._initialized = True
        
        from utils import get_logger
        logger = get_logger(__name__)
        logger.info(
            f"LLMSettings初始化完成: "
            f"tracing={llm_tracing}, "
            f"timeout={llm_timeout_seconds}s, "
            f"debug={app_debug}, "
            f"logging={llm_logging}, "
            f"log_path={log_path}"
        )

    @property
    def LLM_TRACING(self) -> bool:
        """是否开启 LLM 追踪"""
        return self._llm_tracing

    @property
    def LLM_TIME_OUT_SECONDS(self) -> int:
        """LLM 超时时间（秒）"""
        return self._llm_timeout_seconds

    @property
    def LLM_LOGGING(self) -> bool:
        """是否开启日志记录"""
        return self._llm_logging

    @property
    def APP_DEBUG(self) -> bool:
        """是否开启调试模式"""
        return self._app_debug

    @property
    def LOG_PATH(self) -> Optional[str]:
        """日志文件路径"""
        return self._log_path

    def set_llm_tracing(self, enabled: bool) -> None:
        """
        设置 LLM 追踪
        
        Args:
            enabled: 是否启用
        """
        self._llm_tracing = enabled
        from utils import get_logger
        logger = get_logger(__name__)
        logger.info(f"LLM Tracing: {'启用' if enabled else '禁用'}")

    def set_llm_timeout(self, timeout: int) -> None:
        """
        设置 LLM 超时时间
        
        Args:
            timeout: 超时时间（秒）
        """
        self._llm_timeout_seconds = timeout
        from utils import get_logger
        logger = get_logger(__name__)
        logger.info(f"LLM Timeout: {timeout}s")

    def set_app_debug(self, enabled: bool) -> None:
        """
        设置调试模式
        
        Args:
            enabled: 是否启用
        """
        self._app_debug = enabled
        from utils import get_logger
        logger = get_logger(__name__)
        logger.info(f"App Debug: {'启用' if enabled else '禁用'}")


# 全局单例实例
_llm_settings: Optional[LLMSettings] = None


def get_llm_settings() -> LLMSettings:
    """
    获取 LLMSettings 单例实例
    
    Returns:
        LLMSettings 实例
    """
    global _llm_settings
    if _llm_settings is None:
        _llm_settings = LLMSettings()
    return _llm_settings


def init_llm_settings(
    llm_tracing: bool = False,
    llm_timeout_seconds: int = 600,
    app_debug: bool = False,
    llm_logging: bool = False,
    log_path: Optional[str] = None,
) -> None:
    """
    初始化 LLM 设置
    
    Args:
        llm_tracing: 是否开启 LLM 追踪
        llm_timeout_seconds: LLM 超时时间（秒）
        app_debug: 是否开启调试模式
        llm_logging: 是否开启日志记录
        log_path: 日志文件路径
    """
    settings = get_llm_settings()
    settings.initialize(
        llm_tracing=llm_tracing,
        llm_timeout_seconds=llm_timeout_seconds,
        app_debug=app_debug,
        llm_logging=llm_logging,
        log_path=log_path,
    )

