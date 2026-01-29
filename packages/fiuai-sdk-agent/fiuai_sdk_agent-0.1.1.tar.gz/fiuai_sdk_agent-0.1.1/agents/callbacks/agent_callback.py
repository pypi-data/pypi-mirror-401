# # -- coding: utf-8 --
# # Project: callbacks
# # Created Date: 2025-01-29
# # Author: liming
# # Email: lmlala@aliyun.com
# # Copyright (c) 2025 FiuAI

# from typing import Dict, Any, List, Optional
# from datetime import datetime
# import asyncio

# from langchain_core.callbacks import BaseCallbackHandler
# from langchain_core.messages import BaseMessage
# from langchain_core.outputs import LLMResult

# from utils import get_logger
# from config import get_settings
# from pkg.llm.price_config import get_model_price_config

# logger = get_logger(__name__)


# class AgentLLMCallback(BaseCallbackHandler):
#     """
#     Agent LLM 回调函数
#     用于统计 token 使用情况，并记录 agent 相关信息
#     """
    
#     def __init__(
#         self,
#         agent_name: Optional[str] = None,
#         agent_type: Optional[str] = None,
#         agent_semantic: Optional[str] = None,
#         task_id: Optional[str] = None,
#         model: Optional[str] = None,
#     ):
#         """
#         初始化回调函数
        
#         Args:
#             agent_name: Agent 名称
#             agent_type: Agent 类型
#             agent_semantic: Agent 语义描述
#             task_id: 任务 ID
#             model: 模型名称
#         """
#         super().__init__()
#         self.agent_name = agent_name
#         self.agent_type = agent_type
#         self.agent_semantic = agent_semantic
#         self.task_id = task_id
#         self.model = model
        
#         # 统计信息
#         self.prompt_tokens = 0
#         self.completion_tokens = 0
#         self.total_tokens = 0
#         self.request_count = 0
#         self.total_cost = 0.0  # 总费用（元）
#         self.start_time: Optional[datetime] = None
#         self.end_time: Optional[datetime] = None
        
#         # 价格配置
#         self._price_config = get_model_price_config()

#     def on_chat_model_start(
#         self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
#     ) -> None:
#         """LLM 请求开始"""
#         self.request_count += 1
#         self.start_time = datetime.now()
        
#         # 从 kwargs 中获取模型信息（如果未在初始化时提供）
#         if not self.model and "invocation_params" in kwargs:
#             invocation_params = kwargs.get("invocation_params", {})
#             self.model = invocation_params.get("model", "unknown")
        
#         if get_settings().LLM_TRACING:
#             try:
#                 # 序列化消息用于日志
#                 serialized_messages = [
#                     [msg.model_dump(mode="json") for msg in msg_list]
#                     for msg_list in messages
#                 ]
                
#                 logger.debug(
#                     f"[LLM Request] agent={self.agent_name}, "
#                     f"type={self.agent_type}, model={self.model}, "
#                     f"task_id={self.task_id}, messages={len(messages)}"
#                 )
#             except Exception as e:
#                 logger.warning(f"Failed to serialize messages: {e}")

#     def on_llm_end(self, response: LLMResult, **kwargs) -> None:
#         """LLM 请求结束"""
#         self.end_time = datetime.now()
        
#         try:
#             # 提取 token 使用信息
#             serialized_response = response.model_dump(mode="json")
#             llm_output = serialized_response.get("llm_output", {})
#             token_usage = llm_output.get("token_usage", {}) if isinstance(llm_output, dict) else {}
            
#             # 累计 token 使用
#             prompt_tokens = token_usage.get("prompt_tokens", 0)
#             completion_tokens = token_usage.get("completion_tokens", 0)
#             total_tokens = token_usage.get("total_tokens", 0)
            
#             self.prompt_tokens += prompt_tokens
#             self.completion_tokens += completion_tokens
#             self.total_tokens += total_tokens
            
#             # 计算费用
#             cost = None
#             if self.model:
#                 cost = self._price_config.calculate_cost(
#                     model_name=self.model,
#                     prompt_tokens=prompt_tokens,
#                     completion_tokens=completion_tokens
#                 )
#                 if cost is not None:
#                     self.total_cost += cost
            
#             # 计算耗时
#             duration = None
#             if self.start_time and self.end_time:
#                 duration = (self.end_time - self.start_time).total_seconds()
            
#             # 记录日志
#             cost_str = f"cost={cost:.6f}CNY" if cost is not None else "cost=N/A"
#             duration_str = f"duration={duration:.2f}s" if duration else "duration=N/A"
#             logger.info(
#                 f"[LLM Usage] agent={self.agent_name}, "
#                 f"type={self.agent_type}, model={self.model}, "
#                 f"task_id={self.task_id}, "
#                 f"prompt_tokens={prompt_tokens}, "
#                 f"completion_tokens={completion_tokens}, "
#                 f"total_tokens={total_tokens}, "
#                 f"{duration_str}, {cost_str}"
#             )
            
#             # 异步写入详细日志（预留扩展）
#             if get_settings().LLM_TRACING:
#                 logger.debug(f"[LLM Response] agent={self.agent_name}, response={serialized_response}")
#                 # 异步记录费用日志（预留扩展）
#                 try:
#                     # 尝试创建异步任务（如果有事件循环）
#                     loop = asyncio.get_event_loop()
#                     if loop.is_running():
#                         asyncio.create_task(self._async_log_cost(
#                             model=self.model,
#                             prompt_tokens=prompt_tokens,
#                             completion_tokens=completion_tokens,
#                             cost=cost,
#                             duration=duration
#                         ))
#                     else:
#                         # 如果没有运行中的事件循环，直接调用（同步）
#                         asyncio.run(self._async_log_cost(
#                             model=self.model,
#                             prompt_tokens=prompt_tokens,
#                             completion_tokens=completion_tokens,
#                             cost=cost,
#                             duration=duration
#                         ))
#                 except RuntimeError:
#                     # 如果没有事件循环，直接记录 debug 日志
#                     logger.debug(
#                         f"[LLM Cost Log] agent={self.agent_name}, "
#                         f"model={self.model}, prompt_tokens={prompt_tokens}, "
#                         f"completion_tokens={completion_tokens}, "
#                         f"cost={cost}, duration={duration}"
#                     )
                
#         except Exception as e:
#             logger.warning(f"Failed to extract token usage: {e}")

#     async def _async_log_cost(
#         self,
#         model: Optional[str],
#         prompt_tokens: int,
#         completion_tokens: int,
#         cost: Optional[float],
#         duration: Optional[float]
#     ) -> None:
#         """
#         异步记录费用日志
        
#         这是一个预留方法，未来可以实现：
#         - 写入数据库
#         - 写入消息队列
#         - 更新缓存统计
        
#         Args:
#             model: 模型名称
#             prompt_tokens: 输入 token 数
#             completion_tokens: 输出 token 数
#             cost: 费用
#             duration: 耗时（秒）
#         """
#         # TODO: 实现异步日志写入
#         # 1. 写入数据库的 LLM 使用记录表
#         # 2. 更新 Redis 缓存中的统计信息
#         # 3. 发送到消息队列进行后续处理
        
#         # 目前先打 debug 日志
#         logger.debug(
#             f"[LLM Cost Log] agent={self.agent_name}, "
#             f"model={model}, prompt_tokens={prompt_tokens}, "
#             f"completion_tokens={completion_tokens}, "
#             f"cost={cost}, duration={duration}"
#         )
    
#     def get_statistics(self) -> Dict[str, Any]:
#         """
#         获取统计信息
        
#         Returns:
#             Dict[str, Any]: 统计信息字典
#         """
#         duration = None
#         if self.start_time and self.end_time:
#             duration = (self.end_time - self.start_time).total_seconds()
        
#         return {
#             "agent_name": self.agent_name,
#             "agent_type": self.agent_type,
#             "agent_semantic": self.agent_semantic,
#             "task_id": self.task_id,
#             "model": self.model,
#             "request_count": self.request_count,
#             "prompt_tokens": self.prompt_tokens,
#             "completion_tokens": self.completion_tokens,
#             "total_tokens": self.total_tokens,
#             "total_cost": self.total_cost,
#             "duration": duration,
#         }

#     def reset(self):
#         """重置统计信息"""
#         self.prompt_tokens = 0
#         self.completion_tokens = 0
#         self.total_tokens = 0
#         self.request_count = 0
#         self.total_cost = 0.0
#         self.start_time = None
#         self.end_time = None

