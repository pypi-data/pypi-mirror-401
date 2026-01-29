# -- coding: utf-8 --
# Project: user_context
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from contextvars import ContextVar, copy_context
from typing import Optional
from contextlib import contextmanager
import uuid

from fiuai_sdk_python.auth.type import AuthData
from fiuai_sdk_python.profile import UserProfileInfo

from fiuai_sdk_python.utils.logger import get_logger
from .user import UserContext

logger = get_logger(__name__)

# 使用 contextvars 创建线程/异步安全的上下文变量
_user_context_var: ContextVar[Optional[UserContext]] = ContextVar(
    "user_context", default=None
)


class UserContextManager:
    """
    用户上下文管理器
    
    用于在 HTTP 请求和后台任务中统一管理用户信息
    支持线程/异步安全的上下文传递
    """
    
    @staticmethod
    def init_from_request_context(
        auth_data: AuthData,
        trace_id: str,
        user_profile_info: Optional[UserProfileInfo] = None
    ) -> Optional[UserContext]:
        """
        从请求上下文中初始化用户上下文
        
        由调用方负责从 RequestContext 或其他来源提取 auth_data 并传入
        
        Args:
            auth_data: 认证数据，由调用方从请求中提取
            user_profile_info: 可选的用户配置信息
            
        Returns:
            UserContext: 创建的用户上下文，如果 auth_data 无效则返回 None
        """
        try:
            # 验证基本字段
            if not auth_data or not auth_data.user_id or not auth_data.auth_tenant_id:
                logger.warning("auth data missing required fields: user_id or auth_tenant_id")
                return None
            
            
            
            # 创建 UserContext
            user_context = UserContext(
                trace_id=trace_id,
                user_simple_auth_info=auth_data,
                user_profile_info=user_profile_info
            )
            
            # 设置到上下文变量中
            _user_context_var.set(user_context)
            
            logger.debug(
                f"user context initialized from request context: "
                f"user={auth_data.user_id}, tenant={auth_data.auth_tenant_id}"
            )
            
            return user_context
            
        except Exception as e:
            logger.error(f"failed to init user context from request context: {e}")
            import traceback
            logger.error(f"exception stack: {traceback.format_exc()}")
            return None
    
    @staticmethod
    def init(
        auth_data: AuthData,
        trace_id: str,
        user_profile_info: Optional[UserProfileInfo] = None
    ) -> UserContext:
        """
        手动初始化用户上下文
        
        用于后台任务或其他场景，直接传入认证信息
        
        Args:
            auth_data: 认证数据
            user_profile_info: 可选的用户配置信息
            
        Returns:
            UserContext: 创建的用户上下文
            
        Raises:
            ValueError: 如果 auth_data 缺少必需字段
        """
        # 验证基本字段
        if not auth_data or not auth_data.user_id or not auth_data.auth_tenant_id:
            raise ValueError("auth_data must have user_id and auth_tenant_id")
        
        
        # 创建 UserContext
        user_context = UserContext(
            trace_id=trace_id,
            user_simple_auth_info=auth_data,
            user_profile_info=user_profile_info
        )
        
        # 设置到上下文变量中
        _user_context_var.set(user_context)
        
        logger.debug(
            f"user context initialized manually: "
            f"user={auth_data.user_id}, tenant={auth_data.auth_tenant_id}"
        )
        
        return user_context
    
    @staticmethod
    def get() -> Optional[UserContext]:
        """
        获取当前用户上下文
        
        Returns:
            Optional[UserContext]: 当前用户上下文，如果未设置则返回 None
        """
        return _user_context_var.get()
    
    @staticmethod
    def get_or_raise() -> UserContext:
        """
        获取当前用户上下文，如果不存在则抛出异常
        
        Returns:
            UserContext: 当前用户上下文
            
        Raises:
            RuntimeError: 如果用户上下文未设置
        """
        user_context = _user_context_var.get()
        if user_context is None:
            raise RuntimeError("user context is not initialized")
        return user_context
    
    @staticmethod
    def get_auth_data() -> Optional[AuthData]:
        """
        快速获取当前认证数据
        
        Returns:
            Optional[AuthData]: 当前认证数据，如果未设置则返回 None
        """
        user_context = _user_context_var.get()
        if user_context is None:
            return None
        return user_context.user_simple_auth_info
    
    @staticmethod
    def get_user_profile_info() -> Optional[UserProfileInfo]:
        """
        快速获取当前用户配置信息
        
        Returns:
            Optional[UserProfileInfo]: 当前用户配置信息，如果未设置则返回 None
        """
        user_context = _user_context_var.get()
        if user_context is None:
            return None
        return user_context.user_profile_info
    
    @staticmethod
    def get_user_id() -> Optional[str]:
        """
        快速获取当前用户 ID
        
        Returns:
            Optional[str]: 当前用户 ID，如果未设置则返回 None
        """
        auth_data = UserContextManager.get_auth_data()
        if auth_data is None:
            return None
        return auth_data.user_id
    
    @staticmethod
    def get_tenant_id() -> Optional[str]:
        """
        快速获取当前租户 ID
        
        Returns:
            Optional[str]: 当前租户 ID，如果未设置则返回 None
        """
        auth_data = UserContextManager.get_auth_data()
        if auth_data is None:
            return None
        return auth_data.auth_tenant_id
    
    @staticmethod
    def get_company() -> Optional[str]:
        """
        快速获取当前公司 ID
        
        Returns:
            Optional[str]: 当前公司 ID，如果未设置则返回 None
        """
        auth_data = UserContextManager.get_auth_data()
        if auth_data is None:
            return None
        return auth_data.current_company
    
    @staticmethod
    def get_company_unique_no() -> Optional[str]:
        """
        快速获取当前公司唯一编号
        
        Returns:
            Optional[str]: 当前公司唯一编号，如果未设置则返回 None
        """
        auth_data = UserContextManager.get_auth_data()
        if auth_data is None:
            return None
        return auth_data.company_unique_no
    
    @staticmethod
    def get_trace_id() -> Optional[str]:
        """
        快速获取当前追踪 ID
        
        Returns:
            Optional[str]: 当前追踪 ID，如果未设置则返回 None
        """
        user_context = _user_context_var.get()
        if user_context is None:
            return None
        return user_context.trace_id
    
    @staticmethod
    def get_lang() -> Optional[str]:
        """
        快速获取当前语言设置
        
        Returns:
            Optional[str]: 当前语言设置，如果未设置则返回 None
        """
        auth_data = UserContextManager.get_auth_data()
        if auth_data is None:
            return None
        return auth_data.lang
    
    @staticmethod
    def set(user_context: UserContext) -> None:
        """
        设置用户上下文
        
        Args:
            user_context: 用户上下文对象
        """
        _user_context_var.set(user_context)
        logger.debug(
            f"user context set: "
            f"user={user_context.user_simple_auth_info.user_id}, "
            f"tenant={user_context.user_simple_auth_info.auth_tenant_id}"
        )
    
    @staticmethod
    def clear() -> None:
        """
        清除当前用户上下文
        """
        _user_context_var.set(None)
        logger.debug("user context cleared")
    
    @staticmethod
    def copy_context() -> Optional[UserContext]:
        """
        复制当前用户上下文（用于传递给子任务）
        
        Returns:
            Optional[UserContext]: 当前用户上下文的副本，如果未设置则返回 None
        """
        user_context = _user_context_var.get()
        if user_context is None:
            return None
        
        # 创建新的 UserContext 对象（深拷贝）
        return UserContext(
            trace_id=user_context.trace_id,
            user_simple_auth_info=user_context.user_simple_auth_info,
            user_profile_info=user_context.user_profile_info
        )
    
    @staticmethod
    @contextmanager
    def with_context(
        auth_data: AuthData,
        user_profile_info: Optional[UserProfileInfo] = None
    ):
        """
        上下文管理器，用于临时设置用户上下文
        
        在 with 语句中使用，退出时会自动恢复之前的上下文
        
        Args:
            auth_data: 认证数据
            user_profile_info: 可选的用户配置信息
            
        Yields:
            UserContext: 创建的用户上下文
            
        Example:
            ```python
            with UserContextManager.with_context(auth_data):
                user_id = get_user_id()  # 可以直接使用 helper 方法
                # ... 执行需要用户上下文的代码
            # 退出 with 后，上下文自动恢复
            ```
        """
        # 保存当前上下文
        old_context = _user_context_var.get()
        
        try:
            # 初始化新的上下文
            user_context = UserContextManager.init(auth_data, user_profile_info)
            yield user_context
        finally:
            # 恢复之前的上下文
            _user_context_var.set(old_context)
            if old_context is None:
                logger.debug("user context restored to None")
            else:
                logger.debug(
                    f"user context restored: "
                    f"user={old_context.user_simple_auth_info.user_id}"
                )

