# -- coding: utf-8 --
# Project: callbacks
# Created Date: 2025 12 We
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

from ..settings import get_llm_settings

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


class LLMDebugCallback(BaseCallbackHandler):
    """
    调试回调函数
    
    当 LLM_TRACING 为 true 时，打印调试信息
    当 LLM_LOGGING 为 true 时，将日志写入文件
    """
    
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        """
        LLM 开始调用时触发
        """
        settings = get_llm_settings()
        
        # 获取 task_id
        task_id = kwargs.get("task_id")
        
        try:
            # 序列化消息: messages 是 List[List[BaseMessage]]，需要遍历序列化
            serialized_messages = [
                [msg.model_dump(mode="json") for msg in msg_list]
                for msg_list in messages
            ]
            
            log_data = {
                "event": "llm_start",
                "task_id": task_id,
                "serialized": serialized,
                "messages": serialized_messages,
            }
            
            # 如果开启追踪，打印到控制台
            if settings.LLM_TRACING:
                print(json.dumps(log_data, ensure_ascii=False, indent=2))
            
            # 如果开启日志记录，写入文件
            if settings.LLM_LOGGING:
                _write_log(log_data)
                
        except Exception as e:
            # 记录序列化错误
            if settings.LLM_TRACING:
                print(f"LLM start callback error: {str(e)}")
            if settings.LLM_LOGGING:
                _write_log({
                    "event": "llm_start_error",
                    "error": str(e),
                    "task_id": task_id,
                })

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """
        LLM 调用结束时触发
        """
        settings = get_llm_settings()
        
        # 获取 task_id
        task_id = kwargs.get("task_id")
        
        try:
            # 序列化LLM响应: 使用 model_dump 方法
            serialized_response = response.model_dump(mode="json")
            
            # 提取token使用信息
            # LLMResult 的 token_usage 在 llm_output 中
            llm_output = serialized_response.get("llm_output", {})
            token_usage = llm_output.get("token_usage", {}) if isinstance(llm_output, dict) else {}
            completion_tokens = token_usage.get("completion_tokens", 0)
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)
            
            log_data = {
                "event": "llm_end",
                "task_id": task_id,
                "response": serialized_response,
                "token_usage": {
                    "completion_tokens": completion_tokens,
                    "prompt_tokens": prompt_tokens,
                    "total_tokens": total_tokens,
                },
            }
            
            # 如果开启追踪，打印到控制台
            if settings.LLM_TRACING:
                print(json.dumps(log_data, ensure_ascii=False, indent=2))
            
            # 如果开启日志记录，写入文件
            if settings.LLM_LOGGING:
                _write_log(log_data)
                
        except Exception as e:
            # 记录序列化错误
            if settings.LLM_TRACING:
                print(f"LLM end callback error: {str(e)}")
            if settings.LLM_LOGGING:
                _write_log({
                    "event": "llm_end_error",
                    "error": str(e),
                    "task_id": task_id,
                })


