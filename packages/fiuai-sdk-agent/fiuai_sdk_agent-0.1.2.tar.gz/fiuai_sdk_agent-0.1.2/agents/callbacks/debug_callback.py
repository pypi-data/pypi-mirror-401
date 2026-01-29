# # -- coding: utf-8 --
# # Project: callbacks
# # Created Date: 2025 12 We
# # Author: liming
# # Email: lmlala@aliyun.com
# # Copyright (c) 2025 FiuAI

# from typing import Dict, Any, List

# from langchain_core.callbacks import BaseCallbackHandler
# from langchain_core.messages import BaseMessage
# from langchain_core.outputs import LLMResult

# from config import get_settings

# class LLMDebugCallback(BaseCallbackHandler):
#     """
#     调试回调函数
#     """
#     def on_chat_model_start(
#         self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
#     ) -> None:
        
#         if get_settings().LLM_TRACING:
#             # 获取task_id
#             task_id = kwargs.get("task_id")
            
#             try:
#                 # 序列化消息: messages 是 List[List[BaseMessage]]，需要遍历序列化
#                 serialized_messages = [
#                     [msg.model_dump(mode="json") for msg in msg_list]
#                     for msg_list in messages
#                 ]
                
#                 # 记录LLM请求日志
#                 print(serialized_messages)
#             except Exception as e:
#                 # 记录序列化错误
#                 pass
#         else:
#             pass

#     def on_llm_end(self, response: LLMResult, **kwargs) -> None:
#         if get_settings().LLM_TRACING:
#             # 获取task_id
#             task_id = kwargs.get("task_id")
            
#             try:
#                 # 序列化LLM响应: 使用 model_dump 方法
#                 serialized_response = response.model_dump(mode="json")
                
#                 # 提取token使用信息
#                 # LLMResult 的 token_usage 在 llm_output 中
#                 llm_output = serialized_response.get("llm_output", {})
#                 token_usage = llm_output.get("token_usage", {}) if isinstance(llm_output, dict) else {}
#                 completion_tokens = token_usage.get("completion_tokens", 0)
#                 prompt_tokens = token_usage.get("prompt_tokens", 0)
#                 total_tokens = token_usage.get("total_tokens", 0)
                
#                 # 记录LLM响应日志
#                 print(serialized_response)
#             except Exception as e:
#                 pass
#         else:
#             pass


