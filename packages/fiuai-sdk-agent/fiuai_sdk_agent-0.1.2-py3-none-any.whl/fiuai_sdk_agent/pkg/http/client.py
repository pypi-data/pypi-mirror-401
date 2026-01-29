# -- coding: utf-8 --
# Project: fiuai-ai
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import httpx
from typing import Optional, Dict, Any, Union
import logging
import asyncio
import time

from fiuai_sdk_python.context import get_current_headers, is_current_context_valid

logger = logging.getLogger(__name__)

# 需要传递的认证头列表
AUTH_HEADER_KEYS = [
    'x-fiuai-user',
    'x-fiuai-auth-tenant-id',
    'x-fiuai-current-company',
    'x-fiuai-impersonation',
    'x-fiuai-unique-no',
    'x-fiuai-trace-id',
    'x-fiuai-lang',
    'accept-language',
]


def extract_auth_headers() -> Dict[str, str]:
    """
    从当前上下文中提取认证头信息
    
    Returns:
        Dict[str, str]: 认证头字典，如果提取失败则返回空字典
    """
    try:
        # 验证上下文是否有效
        if not is_current_context_valid():
            logger.debug("current context is invalid, cannot extract auth headers")
            return {}
        
        # 获取当前上下文中的请求头
        headers = get_current_headers()
        if not headers:
            logger.debug("cannot get request headers from current context")
            return {}
        
        # 提取需要的认证头
        auth_headers = {}
        for key in AUTH_HEADER_KEYS:
            value = headers.get(key)
            if value:
                auth_headers[key] = value
        
        return auth_headers
        
    except Exception as e:
        logger.warning(f"failed to extract auth headers from context: {e}")
        return {}


async def auth_header_interceptor(request: httpx.Request):
    """
    异步认证头拦截器 - 自动为请求添加认证头和默认 Content-Type
    
    Args:
        request: httpx 请求对象
    """
    # 从上下文中提取认证头
    auth_headers = extract_auth_headers()
    
    if auth_headers:
        # 将认证头添加到请求中
        # httpx 的 headers 是只读的，需要通过 update 方法或创建新的 Headers
        # 使用 request.headers.update() 方法
        for key, value in auth_headers.items():
            # 如果请求中已经存在相同的 header，会被覆盖
            request.headers[key] = value
        logger.debug(f"added auth headers to request: {list(auth_headers.keys())}")
    else:
        logger.debug("no auth headers found in context, skipping header injection")
    
    # 添加默认 Content-Type: application/json
    # 只在请求有 body 且未设置 Content-Type 时添加
    if request.content and "content-type" not in request.headers:
        request.headers["content-type"] = "application/json"
        logger.debug("added default Content-Type: application/json")


def sync_auth_header_interceptor(request: httpx.Request):
    """
    同步认证头拦截器 - 自动为请求添加认证头和默认 Content-Type
    
    Args:
        request: httpx 请求对象
    """
    # 从上下文中提取认证头
    auth_headers = extract_auth_headers()
    
    if auth_headers:
        # 将认证头添加到请求中
        for key, value in auth_headers.items():
            # 如果请求中已经存在相同的 header，会被覆盖
            request.headers[key] = value
        logger.debug(f"added auth headers to request: {list(auth_headers.keys())}")
    else:
        logger.debug("no auth headers found in context, skipping header injection")
    
    # 添加默认 Content-Type: application/json
    # 只在请求有 body 且未设置 Content-Type 时添加
    if request.content and "content-type" not in request.headers:
        request.headers["content-type"] = "application/json"
        logger.debug("added default Content-Type: application/json")


class RetryableAsyncClient(httpx.AsyncClient):
    """支持重试的异步 httpx 客户端"""
    
    def __init__(
        self,
        retry_count: int = 0,
        retry_interval: float = 1.0,
        *args,
        **kwargs
    ):
        """
        初始化支持重试的异步客户端
        
        Args:
            retry_count: 重试次数，0 表示不重试
            retry_interval: 重试间隔（秒）
            *args: httpx.AsyncClient 的位置参数
            **kwargs: httpx.AsyncClient 的关键字参数
        """
        super().__init__(*args, **kwargs)
        self.retry_count = retry_count
        self.retry_interval = retry_interval
    
    async def _request_with_retry(
        self,
        method: str,
        url: Union[httpx.URL, str],
        *args,
        **kwargs
    ) -> httpx.Response:
        """
        带重试的请求方法
        
        Args:
            method: HTTP 方法
            url: 请求 URL
            *args: 其他位置参数
            **kwargs: 其他关键字参数
            
        Returns:
            httpx.Response: HTTP 响应
            
        Raises:
            httpx.HTTPError: 所有重试都失败后抛出异常
        """
        last_exception = None
        
        for attempt in range(self.retry_count + 1):
            try:
                response = await super().request(method, url, *args, **kwargs)
                # 如果状态码表示需要重试（5xx 服务器错误），则重试
                if response.status_code >= 500 and attempt < self.retry_count:
                    logger.warning(
                        f"request failed with status {response.status_code}, "
                        f"retrying ({attempt + 1}/{self.retry_count})"
                    )
                    await response.aclose()
                    await asyncio.sleep(self.retry_interval)
                    continue
                return response
            except httpx.HTTPStatusError as e:
                # 对于 5xx 服务器错误，进行重试
                if e.response.status_code >= 500 and attempt < self.retry_count:
                    logger.warning(
                        f"request failed with status {e.response.status_code}, "
                        f"retrying ({attempt + 1}/{self.retry_count})"
                    )
                    await e.response.aclose()
                    await asyncio.sleep(self.retry_interval)
                    continue
                # 对于 4xx 客户端错误，不重试，直接抛出
                last_exception = e
                logger.error(f"request failed with client error: {e}")
                raise
            except httpx.RequestError as e:
                # 对于网络错误等，进行重试
                last_exception = e
                if attempt < self.retry_count:
                    logger.warning(
                        f"request failed: {e}, retrying ({attempt + 1}/{self.retry_count})"
                    )
                    await asyncio.sleep(self.retry_interval)
                else:
                    logger.error(f"request failed after {self.retry_count + 1} attempts: {e}")
                    raise
        
        # 如果所有重试都失败，抛出最后一个异常
        if last_exception:
            raise last_exception
        raise httpx.HTTPError("request failed")
    
    async def get(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """GET 请求，支持重试"""
        return await self._request_with_retry("GET", url, *args, **kwargs)
    
    async def post(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """POST 请求，支持重试"""
        return await self._request_with_retry("POST", url, *args, **kwargs)
    
    async def put(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """PUT 请求，支持重试"""
        return await self._request_with_retry("PUT", url, *args, **kwargs)
    
    async def delete(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """DELETE 请求，支持重试"""
        return await self._request_with_retry("DELETE", url, *args, **kwargs)
    
    async def patch(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """PATCH 请求，支持重试"""
        return await self._request_with_retry("PATCH", url, *args, **kwargs)
    
    async def head(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """HEAD 请求，支持重试"""
        return await self._request_with_retry("HEAD", url, *args, **kwargs)
    
    async def options(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """OPTIONS 请求，支持重试"""
        return await self._request_with_retry("OPTIONS", url, *args, **kwargs)


class RetryableSyncClient(httpx.Client):
    """支持重试的同步 httpx 客户端"""
    
    def __init__(
        self,
        retry_count: int = 0,
        retry_interval: float = 1.0,
        *args,
        **kwargs
    ):
        """
        初始化支持重试的同步客户端
        
        Args:
            retry_count: 重试次数，0 表示不重试
            retry_interval: 重试间隔（秒）
            *args: httpx.Client 的位置参数
            **kwargs: httpx.Client 的关键字参数
        """
        super().__init__(*args, **kwargs)
        self.retry_count = retry_count
        self.retry_interval = retry_interval
    
    def _request_with_retry(
        self,
        method: str,
        url: Union[httpx.URL, str],
        *args,
        **kwargs
    ) -> httpx.Response:
        """
        带重试的请求方法
        
        Args:
            method: HTTP 方法
            url: 请求 URL
            *args: 其他位置参数
            **kwargs: 其他关键字参数
            
        Returns:
            httpx.Response: HTTP 响应
            
        Raises:
            httpx.HTTPError: 所有重试都失败后抛出异常
        """
        last_exception = None
        
        for attempt in range(self.retry_count + 1):
            try:
                response = super().request(method, url, *args, **kwargs)
                # 如果状态码表示需要重试（5xx 服务器错误），则重试
                if response.status_code >= 500 and attempt < self.retry_count:
                    logger.warning(
                        f"request failed with status {response.status_code}, "
                        f"retrying ({attempt + 1}/{self.retry_count})"
                    )
                    response.close()
                    time.sleep(self.retry_interval)
                    continue
                return response
            except httpx.HTTPStatusError as e:
                # 对于 5xx 服务器错误，进行重试
                if e.response.status_code >= 500 and attempt < self.retry_count:
                    logger.warning(
                        f"request failed with status {e.response.status_code}, "
                        f"retrying ({attempt + 1}/{self.retry_count})"
                    )
                    e.response.close()
                    time.sleep(self.retry_interval)
                    continue
                # 对于 4xx 客户端错误，不重试，直接抛出
                last_exception = e
                logger.error(f"request failed with client error: {e}")
                raise
            except httpx.RequestError as e:
                # 对于网络错误等，进行重试
                last_exception = e
                if attempt < self.retry_count:
                    logger.warning(
                        f"request failed: {e}, retrying ({attempt + 1}/{self.retry_count})"
                    )
                    time.sleep(self.retry_interval)
                else:
                    logger.error(f"request failed after {self.retry_count + 1} attempts: {e}")
                    raise
        
        # 如果所有重试都失败，抛出最后一个异常
        if last_exception:
            raise last_exception
        raise httpx.HTTPError("request failed")
    
    def get(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """GET 请求，支持重试"""
        return self._request_with_retry("GET", url, *args, **kwargs)
    
    def post(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """POST 请求，支持重试"""
        return self._request_with_retry("POST", url, *args, **kwargs)
    
    def put(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """PUT 请求，支持重试"""
        return self._request_with_retry("PUT", url, *args, **kwargs)
    
    def delete(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """DELETE 请求，支持重试"""
        return self._request_with_retry("DELETE", url, *args, **kwargs)
    
    def patch(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """PATCH 请求，支持重试"""
        return self._request_with_retry("PATCH", url, *args, **kwargs)
    
    def head(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """HEAD 请求，支持重试"""
        return self._request_with_retry("HEAD", url, *args, **kwargs)
    
    def options(self, url: Union[httpx.URL, str], *args, **kwargs) -> httpx.Response:
        """OPTIONS 请求，支持重试"""
        return self._request_with_retry("OPTIONS", url, *args, **kwargs)


def create_http_client(
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    retry_count: int = 0,
    retry_interval: float = 1.0,
    **kwargs: Any
) -> httpx.AsyncClient:
    """
    创建带认证头拦截器的 httpx 异步客户端
    
    Args:
        base_url: 基础 URL
        timeout: 请求超时时间（秒）
        follow_redirects: 是否跟随重定向
        verify: 是否验证 SSL 证书
        retry_count: 重试次数，0 表示不重试
        retry_interval: 重试间隔（秒）
        **kwargs: 其他 httpx.AsyncClient 参数
        
    Returns:
        httpx.AsyncClient: 配置好的异步客户端
    """
    # 创建客户端配置
    client_kwargs = {
        "base_url": base_url,
        "timeout": timeout,
        "follow_redirects": follow_redirects,
        "verify": verify,
        **kwargs
    }
    
    # 创建客户端并添加拦截器
    # httpx 使用 event_hooks 来实现拦截器功能
    if retry_count > 0:
        # 使用支持重试的客户端
        client = RetryableAsyncClient(
            retry_count=retry_count,
            retry_interval=retry_interval,
            **client_kwargs,
            event_hooks={
                "request": [auth_header_interceptor]
            }
        )
    else:
        # 使用普通客户端
        client = httpx.AsyncClient(
            **client_kwargs,
            event_hooks={
                "request": [auth_header_interceptor]
            }
        )
    
    return client


def create_sync_http_client(
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    retry_count: int = 0,
    retry_interval: float = 1.0,
    **kwargs: Any
) -> httpx.Client:
    """
    创建带认证头拦截器的 httpx 同步客户端
    
    Args:
        base_url: 基础 URL
        timeout: 请求超时时间（秒）
        follow_redirects: 是否跟随重定向
        verify: 是否验证 SSL 证书
        retry_count: 重试次数，0 表示不重试
        retry_interval: 重试间隔（秒）
        **kwargs: 其他 httpx.Client 参数
        
    Returns:
        httpx.Client: 配置好的同步客户端
    """
    # 创建客户端配置
    client_kwargs = {
        "base_url": base_url,
        "timeout": timeout,
        "follow_redirects": follow_redirects,
        "verify": verify,
        **kwargs
    }
    
    # 创建客户端并添加拦截器
    if retry_count > 0:
        # 使用支持重试的客户端
        client = RetryableSyncClient(
            retry_count=retry_count,
            retry_interval=retry_interval,
            **client_kwargs,
            event_hooks={
                "request": [sync_auth_header_interceptor]
            }
        )
    else:
        # 使用普通客户端
        client = httpx.Client(
            **client_kwargs,
            event_hooks={
                "request": [sync_auth_header_interceptor]
            }
        )
    
    return client


# 全局客户端实例（可选，用于单例模式）
_global_async_client: Optional[httpx.AsyncClient] = None
_global_sync_client: Optional[httpx.Client] = None


def get_async_http_client(
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    retry_count: int = 0,
    retry_interval: float = 1.0,
    **kwargs: Any
) -> httpx.AsyncClient:
    """
    获取全局 httpx 异步客户端（单例模式）
    
    如果全局客户端不存在或配置不同，会创建新的客户端
    
    Args:
        base_url: 基础 URL
        timeout: 请求超时时间（秒）
        follow_redirects: 是否跟随重定向
        verify: 是否验证 SSL 证书
        retry_count: 重试次数，0 表示不重试
        retry_interval: 重试间隔（秒）
        **kwargs: 其他 httpx.AsyncClient 参数
        
    Returns:
        httpx.AsyncClient: 全局异步客户端实例
    """
    global _global_async_client
    
    # 如果全局客户端不存在，创建新的
    if _global_async_client is None:
        _global_async_client = create_http_client(
            base_url=base_url,
            timeout=timeout,
            follow_redirects=follow_redirects,
            verify=verify,
            retry_count=retry_count,
            retry_interval=retry_interval,
            **kwargs
        )
    
    return _global_async_client


def get_sync_http_client(
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    retry_count: int = 0,
    retry_interval: float = 1.0,
    **kwargs: Any
) -> httpx.Client:
    """
    获取全局 httpx 同步客户端（单例模式）
    
    如果全局客户端不存在或配置不同，会创建新的客户端
    
    Args:
        base_url: 基础 URL
        timeout: 请求超时时间（秒）
        follow_redirects: 是否跟随重定向
        verify: 是否验证 SSL 证书
        retry_count: 重试次数，0 表示不重试
        retry_interval: 重试间隔（秒）
        **kwargs: 其他 httpx.Client 参数
        
    Returns:
        httpx.Client: 全局同步客户端实例
    """
    global _global_sync_client
    
    # 如果全局客户端不存在，创建新的
    if _global_sync_client is None:
        _global_sync_client = create_sync_http_client(
            base_url=base_url,
            timeout=timeout,
            follow_redirects=follow_redirects,
            verify=verify,
            retry_count=retry_count,
            retry_interval=retry_interval,
            **kwargs
        )
    
    return _global_sync_client


def close_global_clients():
    """关闭全局客户端"""
    global _global_async_client, _global_sync_client
    
    if _global_async_client:
        _global_async_client.close()
        _global_async_client = None
    
    if _global_sync_client:
        _global_sync_client.close()
        _global_sync_client = None

