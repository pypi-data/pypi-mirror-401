# -- coding: utf-8 --
# Project: fiuai-sdk-agent
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

import os
import json
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

from fiuai_sdk_python.utils.logger import get_logger
from ..settings import get_llm_settings

logger = get_logger(__name__)

# 文件写入锁，确保线程安全
_log_file_lock = threading.Lock()


def _get_log_path() -> Optional[str]:
    """
    获取日志文件路径
    
    Returns:
        日志文件完整路径，如果配置不存在则返回 None
    """
    try:
        settings = get_llm_settings()
        log_path = settings.LOG_PATH
        
        if not log_path:
            return None
        
        # 确保日志目录存在
        if not os.path.exists(log_path):
            os.makedirs(log_path, exist_ok=True)
        
        return os.path.join(log_path, "llm.log")
    except Exception:
        # 如果无法获取配置，返回 None
        return None


def _write_log(data: Dict[str, Any]) -> None:
    """
    写入日志到文件
    
    Args:
        data: 要写入的日志数据
    """
    log_file = _get_log_path()
    if not log_file:
        return
    
    try:
        with _log_file_lock:
            # 添加时间戳
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                **data
            }
            
            # 追加写入文件
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        # 忽略写入错误，避免影响主流程
        pass


def write_llm_usage_to_local_log(
    task_id: Optional[str] = None,
    task_name: Optional[str] = None,
    model: Optional[str] = None,
    input_token: int = 0,
    output_token: int = 0,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    user_id: Optional[str] = None,
    auth_tenant_id: Optional[str] = None,
    auth_company_id: Optional[str] = None,
    cost: Optional[float] = None,
) -> None:
    """
    写入 LLM 使用日志到本地文件
    
    Args:
        task_id: 任务 ID
        task_name: 任务名称
        model: 模型名称
        input_token: 输入 token 数
        output_token: 输出 token 数
        start_time: 开始时间
        end_time: 结束时间
        user_id: 用户 ID
        auth_tenant_id: 租户 ID
        auth_company_id: 公司 ID
        cost: 费用
    """
    log_data = {
        "event": "llm_usage",
        "task_id": task_id,
        "task_name": task_name,
        "model": model,
        "input_token": input_token,
        "output_token": output_token,
        "total_token": input_token + output_token,
        "user_id": user_id,
        "auth_tenant_id": auth_tenant_id,
        "auth_company_id": auth_company_id,
        "cost": cost,
    }
    
    if start_time:
        log_data["start_time"] = start_time.isoformat()
    if end_time:
        log_data["end_time"] = end_time.isoformat()
        if start_time:
            duration = (end_time - start_time).total_seconds()
            log_data["duration"] = duration
    
    _write_log(log_data)


class LLMLocalLogCallback(BaseCallbackHandler):
    """
    本地日志回调函数
    
    将 LLM 使用情况写入本地日志文件
    """
    
    def __init__(
        self,
        task_id: Optional[str] = None,
        task_name: Optional[str] = None,
        user_id: Optional[str] = None,
        auth_tenant_id: Optional[str] = None,
        auth_company_id: Optional[str] = None,
    ):
        """
        初始化回调函数
        
        Args:
            task_id: 任务 ID
            task_name: 任务名称
            user_id: 用户 ID
            auth_tenant_id: 租户 ID
            auth_company_id: 公司 ID
        """
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.user_id = user_id
        self.auth_tenant_id = auth_tenant_id
        self.auth_company_id = auth_company_id
        self.model = "unknown"
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        """LLM 请求开始"""
        self.start_time = datetime.now()
        
        # 从 kwargs 中获取模型信息
        if "invocation_params" in kwargs:
            invocation_params = kwargs.get("invocation_params", {})
            self.model = invocation_params.get("model", "unknown")
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """LLM 请求结束"""
        self.end_time = datetime.now()
        
        try:
            # 提取 token 使用信息
            serialized_response = response.model_dump(mode="json")
            llm_output = serialized_response.get("llm_output", {})
            token_usage = llm_output.get("token_usage", {}) if isinstance(llm_output, dict) else {}
            
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            
            # 计算费用（如果有价格配置）
            cost = None
            try:
                from ..price_config import get_model_price_config
                price_config = get_model_price_config()
                cost = price_config.calculate_cost(
                    model_name=self.model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
            except Exception:
                pass
            
            # 写入本地日志
            write_llm_usage_to_local_log(
                task_id=self.task_id,
                task_name=self.task_name,
                model=self.model,
                input_token=prompt_tokens,
                output_token=completion_tokens,
                start_time=self.start_time,
                end_time=self.end_time,
                user_id=self.user_id,
                auth_tenant_id=self.auth_tenant_id,
                auth_company_id=self.auth_company_id,
                cost=cost,
            )
        except Exception as e:
            logger.warning(f"Failed to write local log: {e}")
