# -- coding: utf-8 --
# Project: agents
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional, Literal, Any, Dict
from fiuai_sdk_python.utils.logger import get_logger
from ..types.event_type import EventType
from ...utils.errors import FiuaiAgentError
from ..types.plan_type import (
    PlanStepStatus, 
    PlanStatus, 
    PlanStateMachine,
    BasePlan
)

logger = get_logger(__name__)


class PlanManager:
    """
    计划管理器（PlanManager）
    
    职责：
    - 管理 Plan 和 Step 的生命周期
    - 处理 Step 状态转换的业务逻辑
    - 处理 Plan 状态转换的业务逻辑
    - 提供 Plan/Step 信息的查询接口
    
    设计理念：
    1. 单一职责：PlanManager 只负责 Plan/Step 的业务逻辑，不涉及事件发布、上下文管理等
    2. 状态机驱动：所有状态转换都通过 PlanStateMachine 进行校验，确保状态转换的合法性
    3. 纯业务逻辑：PlanManager 的方法都是纯业务逻辑，不涉及外部依赖（如事件发布、数据库等）
    
    与 Agent 的关系：
    - Agent 通过 PlanManager 管理 Plan/Step 的状态
    - Agent 负责协调 PlanManager 和 EventPublisher，确保状态和事件的一致性
    - Agent 的方法（如 close_step）会先调用 PlanManager 的方法修改状态，然后同步到 EventPublisher
    
    使用示例：
        # 创建 PlanManager
        plan_manager = PlanManager(plan=my_plan)
        
        # 关闭当前步骤（返回计划状态和刚关闭的步骤信息）
        plan_status, closed_step_info = plan_manager.close_step(
            message="步骤完成",
            status=PlanStepStatus.COMPLETED
        )
        # closed_step_info 包含: step_id, step_index, step_status
        
        # 获取当前步骤信息（关闭后可能是下一步）
        step_id = plan_manager.get_current_step_id()
        step_index = plan_manager.get_current_step_index()
        
        # 获取计划信息用于事件发布
        plan_info = plan_manager.update_event_plan_info()
    """
    
    def __init__(self, plan: Optional[BasePlan] = None):
        """
        初始化计划管理器
        
        Args:
            plan: 计划对象，如果为None则没有计划
        """
        self.plan: Optional[BasePlan] = plan
    
    def set_plan(self, plan: BasePlan) -> None:
        """
        设置计划
        
        Args:
            plan: 计划对象
        """
        self.plan = plan
    
    def get_plan(self) -> Optional[BasePlan]:
        """
        获取计划
        
        Returns:
            计划对象或None
        """
        return self.plan
    
    def has_plan(self) -> bool:
        """
        检查是否有计划
        
        Returns:
            是否有计划
        """
        return self.plan is not None
    
    def get_plan_id(self) -> Optional[str]:
        """
        获取计划ID
        
        Returns:
            计划ID或None
        """
        return self.plan.plan_id if self.plan else None
    
    def get_current_step_id(self) -> Optional[str]:
        """
        获取当前步骤ID
        
        Returns:
            当前步骤ID或None
        """
        return self.plan.current_step_id if self.plan else None
    
    def get_current_step_index(self) -> Optional[int]:
        """
        获取当前步骤索引
        
        Returns:
            当前步骤索引或None
        """
        return self.plan.current_step_index if self.plan else None
    
    def get_current_step_status(self) -> Optional[str]:
        """
        获取当前步骤状态
        
        Returns:
            当前步骤状态值或None
        """
        if self.plan:
            return self.plan.get_current_step_status().value
        return None
    
    def add_step(
        self,
        name: str,
        description: str,
        step_id: str,
        domain_agent_type: Optional[Any] = None,
    ) -> None:
        """
        动态添加步骤到计划中
        
        该方法支持在计划执行过程中动态添加新的步骤。
        添加的步骤会自动更新 total_step_count，确保计划状态正确。
        
        使用场景：
        - 在执行过程中，根据业务逻辑需要动态添加新的步骤
        - 例如：根据数据查询结果，决定是否需要额外的分析步骤
        
        Args:
            name: 步骤名称
            description: 步骤描述
            step_id: 步骤ID
            domain_agent_type: 执行该步骤的domain agent类型（可选）
        """
        if not self.plan:
            raise FiuaiAgentError("Cannot add step: plan is None")
        
        self.plan.add_step(
            name=name,
            description=description,
            step_id=step_id,
            domain_agent_type=domain_agent_type,
        )
        
        # 记录日志
        logger.info(
            f"plan {self.plan.title} added new step: {name} (step_id: {step_id}, "
            f"total_steps: {self.plan.total_step_count})"
        )
    
    def add_step_message(self, data: Any, event_type: EventType = EventType.CHUNK) -> None:
        """
        添加当前步骤的消息
        
        该方法将消息添加到当前步骤的 messages 列表中，用于：
        - 作为 Agent 的上下文信息
        - 前端通过 chunk 和其他类型接收
        
        注意：
        - 会跳过 PLAN 和 TASK 类型的事件
        - 会跳过空数据
        
        Args:
            data: 消息数据
            event_type: 事件类型（默认为 CHUNK）
        """
        if self.plan:
            # 跳过PLAN和TASK类型的事件，以及空数据
            if event_type != EventType.PLAN and event_type != EventType.TASK and data != "":
                self.plan.add_step_message(data=data, event_type=event_type)
    
    def close_step(
        self,
        message: str,
        status: Literal[PlanStepStatus.COMPLETED, PlanStepStatus.FAILED, PlanStepStatus.SKIPPED] = PlanStepStatus.COMPLETED,
    ) -> tuple[Optional[PlanStatus], Dict[str, Any]]:
        """
        关闭当前步骤（业务逻辑：决定如何切换状态和切换后的操作）
        
        该方法执行以下操作：
        1. 验证 message 不为空
        2. 关闭当前步骤（通过 BasePlan.close_current_step）
        3. 根据步骤状态决定后续操作：
           - 如果步骤失败且 failed_on_step_fail=True，则标记计划失败
           - 如果步骤成功，启动下一个步骤
           - 如果所有步骤完成，标记计划完成
        4. 记录日志
        
        注意：
        - 该方法只负责 Plan/Step 的状态管理，不涉及事件发布
        - 调用者（通常是 Agent）需要在调用此方法后同步更新 EventPublisher
        - 返回的 closed_step_info 包含刚关闭的步骤信息，用于事件发布
        
        Args:
            message: 步骤关闭消息（不能为空）
            status: 步骤状态（COMPLETED/FAILED/SKIPPED）
            
        Returns:
            tuple[plan_status, closed_step_info]:
            - plan_status: 计划状态（PlanStatus）或 None（如果没有计划）
            - closed_step_info: 刚关闭的步骤信息字典，包含：
              - step_id: 刚关闭的步骤ID
              - step_index: 刚关闭的步骤索引
              - step_status: 刚关闭的步骤状态（字符串值）
            
        Raises:
            FiuaiAgentError: 如果 message 为空
        """
        if not self.plan:
            return None, {}
        
        if message == "":
            raise FiuaiAgentError(f"message is empty when close step, {self.plan.current_step_id}")
        
        # 保存刚关闭的步骤信息（在关闭之前保存，因为关闭后可能会切换到下一步）
        closed_step = self.plan._lookup_current_step()
        closed_step_id = self.plan.current_step_id
        closed_step_index = self.plan.current_step_index
        closed_step_status = status.value  # 使用传入的状态值，这是关闭后的状态
        
        # 获取当前步骤状态（用于日志）
        current_step_status = closed_step.status
        
        # 关闭当前步骤（纯数据操作，状态机校验在 BasePlan 内部完成）
        self.plan.close_current_step(status=status)
        
        # 业务逻辑：根据步骤状态决定后续操作
        if status == PlanStepStatus.FAILED:
            # 如果步骤失败，根据配置决定是否标记计划失败
            if self.plan.failed_on_step_fail:
                self.plan.set_plan_to_failed(message=f"step {closed_step_index} failed")
                plan_status = PlanStatus.FAILED
            else:
                plan_status = PlanStatus.RUNNING
                # 即使步骤失败，如果配置允许，继续执行下一步
                if not self.plan.is_all_steps_completed():
                    has_next = self.plan.start_next_step()
                    if not has_next:
                        self.plan.set_plan_to_completed()
                        plan_status = PlanStatus.COMPLETED
        else:
            # 步骤成功完成，启动下一个步骤
            if self.plan.is_all_steps_completed():
                self.plan.set_plan_to_completed()
                plan_status = PlanStatus.COMPLETED
            else:
                has_next = self.plan.start_next_step()
                if not has_next:
                    self.plan.set_plan_to_completed()
                    plan_status = PlanStatus.COMPLETED
                else:
                    plan_status = PlanStatus.RUNNING
        
        # 业务逻辑：记录日志
        logger.info(
            f"plan {self.plan.title} close step {closed_step_index}, "
            f"status transition: {current_step_status.value} -> {status.value}, "
            f"new plan status {plan_status}"
        )
        
        # 返回计划状态和刚关闭的步骤信息
        closed_step_info = {
            "step_id": closed_step_id,
            "step_index": closed_step_index,
            "step_status": closed_step_status,
        }
        
        return plan_status, closed_step_info
    
    def finish_step(self, message: str) -> tuple[Optional[PlanStatus], Dict[str, Any]]:
        """
        完成当前步骤（简化方法）
        
        Args:
            message: 步骤完成消息
            
        Returns:
            tuple[plan_status, closed_step_info]: 计划状态和刚关闭的步骤信息
        """
        return self.close_step(message=message, status=PlanStepStatus.COMPLETED)
    
    def fail_step(self, message: str) -> tuple[Optional[PlanStatus], Dict[str, Any]]:
        """
        标记当前步骤失败（简化方法）
        
        Args:
            message: 步骤失败消息
            
        Returns:
            tuple[plan_status, closed_step_info]: 计划状态和刚关闭的步骤信息
        """
        return self.close_step(message=message, status=PlanStepStatus.FAILED)
    
    def debug_step(self, message: str) -> None:
        """
        记录调试信息到当前步骤（不关闭步骤）
        
        该方法用于在步骤执行过程中记录调试信息，不会改变步骤状态。
        调试信息会被添加到步骤的 messages 中，并记录到日志。
        
        Args:
            message: 调试消息
        """
        if not self.plan:
            return
        
        # 添加调试消息到步骤
        self.add_step_message(data=message, event_type=EventType.CHUNK)
        
        # 记录调试日志
        logger.debug(
            f"plan {self.plan.title} step {self.plan.current_step_index} debug: {message}"
        )
    
    def update_event_plan_info(
        self,
        plan_id: Optional[str] = None,
        step_id: Optional[str] = None,
        step_index: Optional[int] = None,
        step_status: Optional[str] = None,
    ) -> dict:
        """
        获取计划信息用于事件发布
        
        该方法用于从 Plan 中提取当前的状态信息，供 EventPublisher 使用。
        如果提供了参数，则使用参数值；否则从 plan 中获取当前值。
        
        使用场景：
        - Agent 在发布事件前，需要获取当前的 plan/step 信息
        - 确保事件中的 plan_id、step_id 等信息与实际的 plan 状态一致
        
        Args:
            plan_id: 计划ID（如果提供则使用，否则从plan获取）
            step_id: 步骤ID（如果提供则使用，否则从plan获取）
            step_index: 步骤索引（如果提供则使用，否则从plan获取）
            step_status: 步骤状态（如果提供则使用，否则从plan获取）
            
        Returns:
            包含计划信息的字典，包含以下字段：
            - plan_id: 计划ID
            - step_id: 步骤ID
            - step_index: 步骤索引
            - step_status: 步骤状态（字符串值）
        """
        if not self.plan:
            return {
                "plan_id": plan_id,
                "step_id": step_id,
                "step_index": step_index,
                "step_status": step_status,
            }
        
        return {
            "plan_id": plan_id if plan_id is not None else self.plan.plan_id,
            "step_id": step_id if step_id is not None else self.plan.current_step_id,
            "step_index": step_index if step_index is not None else self.plan.current_step_index,
            "step_status": step_status if step_status is not None else self.plan.get_current_step_status().value,
        }

