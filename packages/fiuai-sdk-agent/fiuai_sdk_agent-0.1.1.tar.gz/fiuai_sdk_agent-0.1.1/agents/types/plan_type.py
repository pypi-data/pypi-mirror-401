# -- coding: utf-8 --
# Project: agents
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict, Set, Tuple, Literal
from datetime import datetime
from enum import StrEnum

from ...utils.errors import FiuaiAgentError
from .event_type import EventType
from ...agents.types.agent_type import DomainAgentType


class PlanStepStatus(StrEnum):
    """计划步骤状态"""
    TODO = "todo"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PlanStatus(StrEnum):
    """计划状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    NOT_STARTED = "not_started"


class PlanType(StrEnum):
    """计划类型"""
    SEQUENTIAL = "Sequential"
    PARALLEL = "Parallel"


class StepMessage(BaseModel):
    """步骤消息"""
    event_type: EventType = Field(description="事件类型")
    data: Any = Field(description="事件数据")


class PlanStep(BaseModel):
    """计划步骤"""
    step_index: int = Field(description="步骤序号,从0开始", default=0)
    step_id: str = Field(description="步骤id", default="")
    name: str = Field(description="步骤名称代号")
    description: str = Field(description="步骤描述, 用于前端展示")
    status: PlanStepStatus = Field(description="步骤状态", default=PlanStepStatus.TODO)
    start_time: Optional[datetime] = Field(description="步骤创建时间", default=None)
    end_time: Optional[datetime] = Field(description="步骤结束时间", default=None)
    domain_agent_type: Optional[DomainAgentType] = Field(
        description="执行该步骤的domain agent类型", 
        default=None
    )
    
    # runtime
    messages: List[StepMessage] = Field(
        description="步骤消息,用作agent上下文, 前端通过chunk和其他类型接收,plan初始状态下此列表为空",
        default=[]
    )



# -- coding: utf-8 --
# Project: plan
# Created Date: 2025 12 Fr
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


class PlanStateMachine:
    """计划状态机，负责管理状态转换规则和校验"""
    
    # Plan状态转换规则
    PLAN_TRANSITIONS: Dict[PlanStatus, Set[PlanStatus]] = {
        PlanStatus.NOT_STARTED: {PlanStatus.PENDING, PlanStatus.RUNNING},
        PlanStatus.PENDING: {PlanStatus.RUNNING, PlanStatus.FAILED},
        PlanStatus.RUNNING: {PlanStatus.COMPLETED, PlanStatus.FAILED},
        PlanStatus.COMPLETED: set(),  # 终态
        PlanStatus.FAILED: set(),  # 终态
    }
    
    # Step状态转换规则
    STEP_TRANSITIONS: Dict[PlanStepStatus, Set[PlanStepStatus]] = {
        PlanStepStatus.TODO: {PlanStepStatus.RUNNING, PlanStepStatus.SKIPPED},
        PlanStepStatus.RUNNING: {PlanStepStatus.COMPLETED, PlanStepStatus.FAILED},
        PlanStepStatus.COMPLETED: set(),  # 终态
        PlanStepStatus.FAILED: set(),  # 终态
        PlanStepStatus.SKIPPED: set(),  # 终态
    }
    
    @classmethod
    def can_transition_plan(
        cls, 
        from_status: PlanStatus, 
        to_status: PlanStatus
    ) -> bool:
        """
        检查Plan状态是否可以转换
        
        Args:
            from_status: 当前状态
            to_status: 目标状态
            
        Returns:
            是否可以转换
        """
        valid_transitions = cls.PLAN_TRANSITIONS.get(from_status, set())
        return to_status in valid_transitions
    
    @classmethod
    def can_transition_step(
        cls,
        from_status: PlanStepStatus,
        to_status: PlanStepStatus
    ) -> bool:
        """
        检查Step状态是否可以转换
        
        Args:
            from_status: 当前状态
            to_status: 目标状态
            
        Returns:
            是否可以转换
        """
        valid_transitions = cls.STEP_TRANSITIONS.get(from_status, set())
        return to_status in valid_transitions
    
    @classmethod
    def get_valid_plan_transitions(cls, current_status: PlanStatus) -> Set[PlanStatus]:
        """
        获取Plan的合法状态转换列表
        
        Args:
            current_status: 当前状态
            
        Returns:
            可转换的状态集合
        """
        return cls.PLAN_TRANSITIONS.get(current_status, set())
    
    @classmethod
    def get_valid_step_transitions(cls, current_status: PlanStepStatus) -> Set[PlanStepStatus]:
        """
        获取Step的合法状态转换列表
        
        Args:
            current_status: 当前状态
            
        Returns:
            可转换的状态集合
        """
        return cls.STEP_TRANSITIONS.get(current_status, set())
    
    @classmethod
    def validate_plan_transition(
        cls,
        from_status: PlanStatus,
        to_status: PlanStatus
    ) -> Tuple[bool, Optional[str]]:
        """
        验证Plan状态转换是否合法
        
        Args:
            from_status: 当前状态
            to_status: 目标状态
            
        Returns:
            (是否合法, 错误信息)
        """
        if from_status == to_status:
            return True, None
        
        if cls.can_transition_plan(from_status, to_status):
            return True, None
        
        valid_transitions = cls.get_valid_plan_transitions(from_status)
        error_msg = (
            f"Invalid plan state transition: {from_status.value} -> {to_status.value}. "
            f"Valid transitions from {from_status.value} are: "
            f"{[s.value for s in valid_transitions]}"
        )
        return False, error_msg
    
    @classmethod
    def validate_step_transition(
        cls,
        from_status: PlanStepStatus,
        to_status: PlanStepStatus
    ) -> Tuple[bool, Optional[str]]:
        """
        验证Step状态转换是否合法
        
        Args:
            from_status: 当前状态
            to_status: 目标状态
            
        Returns:
            (是否合法, 错误信息)
        """
        if from_status == to_status:
            return True, None
        
        if cls.can_transition_step(from_status, to_status):
            return True, None
        
        valid_transitions = cls.get_valid_step_transitions(from_status)
        error_msg = (
            f"Invalid step state transition: {from_status.value} -> {to_status.value}. "
            f"Valid transitions from {from_status.value} are: "
            f"{[s.value for s in valid_transitions]}"
        )
        return False, error_msg
    
    @classmethod
    def is_plan_terminal_state(cls, status: PlanStatus) -> bool:
        """
        检查Plan状态是否为终态
        
        Args:
            status: 状态
            
        Returns:
            是否为终态
        """
        return status in {PlanStatus.COMPLETED, PlanStatus.FAILED}
    
    @classmethod
    def is_step_terminal_state(cls, status: PlanStepStatus) -> bool:
        """
        检查Step状态是否为终态
        
        Args:
            status: 状态
            
        Returns:
            是否为终态
        """
        return status in {
            PlanStepStatus.COMPLETED, 
            PlanStepStatus.FAILED, 
            PlanStepStatus.SKIPPED
        }




class BasePlan(BaseModel):
    """计划基类"""
    title: str = Field(description="计划标题")
    plan_id: str = Field(description="计划id")
    plan_type: PlanType = Field(description="计划类型", default=PlanType.SEQUENTIAL)
    failed_on_step_fail: bool = Field(description="是否某个步骤失败就判定任务失败", default=False)
    status: PlanStatus = Field(description="计划状态", default=PlanStatus.NOT_STARTED)
    steps: List[PlanStep] = Field(description="计划步骤列表", default=[])
    start_time: datetime = Field(description="计划开始时间", default_factory=datetime.now)
    end_time: Optional[datetime] = Field(description="计划结束时间", default=None)
    current_step_index: int = Field(description="当前步骤序号,从0开始", default=0)
    current_step_id: str = Field(description="当前步骤id", default="")
    summary: str = Field(description="计划汇总消息, 用于前端展示", default="")
    
    # runtime
    current_step_names: List[str] = Field(description="当前步骤名称列表", default=[])
    total_step_count: int = Field(description="总步骤数", default=0)
    passed_step_count: int = Field(description="已运行步骤数", default=0)
    
    def _validate(self) -> bool:
        """验证计划数据"""
        # 检查是否有name重复的步骤
        step_names = [step.name for step in self.steps]
        if len(step_names) != len(set(step_names)):
            return False
        return True
    
    def _lookup_step_by_name(self, step_name: str) -> Optional[PlanStep]:
        """根据步骤名称获取步骤"""
        for step in self.steps:
            if step.name == step_name:
                return step
        return None
    
    def _lookup_step_by_id(self, step_id: str) -> Optional[PlanStep]:
        """根据步骤ID获取步骤"""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None
    
    def _lookup_current_step(self) -> PlanStep:
        """获取当前步骤"""
        if self.current_step_index >= len(self.steps):
            raise IndexError(f"Current step index {self.current_step_index} out of range")
        return self.steps[self.current_step_index]
    
    
    def get_current_step_status(self) -> PlanStepStatus:
        """获取当前步骤状态"""
        if self.current_step_index >= len(self.steps):
            return PlanStepStatus.TODO
        return self.steps[self.current_step_index].status
    
    def add_step(
        self, 
        name: str, 
        description: str,
        step_id: str,
        domain_agent_type: Optional[DomainAgentType] = None
    ) -> None:
        """
        按顺序添加步骤（支持动态添加）
        
        该方法可以在计划执行过程中动态添加新的步骤。
        添加的步骤会自动更新 total_step_count，确保计划状态正确。
        
        Args:
            name: 步骤名称
            description: 步骤描述
            step_id: 步骤ID
            domain_agent_type: 执行该步骤的domain agent类型（可选）
        """
        last_step_id = len(self.steps)
        step = PlanStep(
            name=name,
            description=description,
            status=PlanStepStatus.TODO,
            step_id=step_id,
            step_index=last_step_id,
            messages=[],
            start_time=None,
            end_time=None,
            domain_agent_type=domain_agent_type,
        )
        self.steps.append(step)
        
        # 更新总步骤数（支持动态添加）
        self.total_step_count = len(self.steps)
    
    def transition_plan_status(self, to_status: PlanStatus) -> None:
        """
        切换计划状态（使用状态机校验）
        
        Args:
            to_status: 目标状态
        """
        is_valid, error_msg = PlanStateMachine.validate_plan_transition(
            from_status=self.status,
            to_status=to_status
        )
        if not is_valid:
            raise FiuaiAgentError(f"Invalid plan state transition: {error_msg}")
        
        self.status = to_status
        if to_status in {PlanStatus.COMPLETED, PlanStatus.FAILED}:
            self.end_time = datetime.now()
    
    def transition_step_status(self, step_index: int, to_status: PlanStepStatus) -> None:
        """
        切换步骤状态（使用状态机校验）
        
        Args:
            step_index: 步骤索引
            to_status: 目标状态
        """
        if step_index >= len(self.steps):
            raise IndexError(f"Step index {step_index} out of range")
        
        step = self.steps[step_index]
        is_valid, error_msg = PlanStateMachine.validate_step_transition(
            from_status=step.status,
            to_status=to_status
        )
        if not is_valid:
            raise FiuaiAgentError(f"Invalid step state transition: {error_msg}")
        
        step.status = to_status
        if to_status == PlanStepStatus.RUNNING and step.start_time is None:
            step.start_time = datetime.now()
        elif to_status in {PlanStepStatus.COMPLETED, PlanStepStatus.FAILED, PlanStepStatus.SKIPPED}:
            step.end_time = datetime.now()
        
        self.steps[step_index] = step
    
    def start(self) -> None:
        """启动计划, 初始化状态, 并启动第一个步骤（使用状态机校验）"""
        if len(self.steps) == 0:
            raise ValueError("plan steps is empty")
        
        # 切换计划状态
        self.transition_plan_status(PlanStatus.RUNNING)
        
        # 初始化计划状态
        self.current_step_index = 0
        self.current_step_names = [self.steps[self.current_step_index].name]
        self.current_step_id = self.steps[self.current_step_index].step_id
        self.start_time = datetime.now()
        self.total_step_count = len(self.steps)
        
        # 启动第一个步骤
        self.transition_step_status(0, PlanStepStatus.RUNNING)
    
    def set_plan_to_failed(self, message: str = "") -> None:
        """设置计划为失败（使用状态机校验）"""
        self.transition_plan_status(PlanStatus.FAILED)
        self.summary = message
    
    def set_plan_to_completed(self, message: str = "") -> None:
        """设置计划为完成（使用状态机校验）"""
        self.transition_plan_status(PlanStatus.COMPLETED)
        self.summary = message
    
    def _step_validate(self) -> Optional[str]:
        """验证step数据, 返回错误信息"""
        if self.status == PlanStatus.NOT_STARTED:
            return "plan is not started"
        return None
    
    def add_step_message(self, data: Any, event_type: EventType = EventType.CHUNK) -> None:
        """添加当前步骤的消息, 作为上下文"""
        err = self._step_validate()
        if err:
            raise FiuaiAgentError(f"step {self.current_step_index} is not valid when add message: {err}")
        
        message = StepMessage(event_type=event_type, data=data)
        if self.current_step_index < len(self.steps):
            self.steps[self.current_step_index].messages.append(message)
    
    def close_current_step(
        self,
        status: Literal[PlanStepStatus.COMPLETED, PlanStepStatus.FAILED, PlanStepStatus.SKIPPED] = PlanStepStatus.COMPLETED,
    ) -> None:
        """
        关闭当前步骤（纯数据操作，使用状态机校验）
        
        Args:
            status: 步骤状态
        """
        err = self._step_validate()
        if err:
            raise FiuaiAgentError(f"step {self.current_step_index} is not valid when close step: {err}")
        
        # 切换步骤状态
        self.transition_step_status(self.current_step_index, status)
        
        # 更新已运行的步骤数
        self.passed_step_count += 1
    
    def start_next_step(self) -> bool:
        """
        启动下一个步骤（纯数据操作，使用状态机校验）
        
        Returns:
            是否成功启动下一步（False表示没有下一步，计划已完成）
        """
        next_step_index = self.current_step_index + 1
        if next_step_index >= len(self.steps):
            return False
        
        # 切换下一步骤状态
        self.transition_step_status(next_step_index, PlanStepStatus.RUNNING)
        
        # 更新全局状态
        next_step = self.steps[next_step_index]
        self.current_step_index = next_step_index
        self.current_step_names = [next_step.name]
        self.current_step_id = next_step.step_id
        
        return True
    
    def is_all_steps_completed(self) -> bool:
        """
        检查是否所有步骤都已完成（支持动态添加的步骤）
        
        该方法会检查所有步骤（包括动态添加的）是否都已完成。
        如果所有步骤都处于终态（COMPLETED/FAILED/SKIPPED），则返回 True。
        
        Returns:
            是否所有步骤都已完成
        """
        # 如果没有任何步骤，返回 True
        if len(self.steps) == 0:
            return True
        
        # 检查所有步骤是否都处于终态
        for step in self.steps:
            if not PlanStateMachine.is_step_terminal_state(step.status):
                return False
        
        return True

