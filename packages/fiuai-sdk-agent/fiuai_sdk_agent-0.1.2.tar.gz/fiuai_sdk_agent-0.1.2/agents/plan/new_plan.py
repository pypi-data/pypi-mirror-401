# -- coding: utf-8 --
# Project: plan
# Created Date: 2025 12 Fr
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


from fiuai_sdk_python.utils.ids import gen_id


from ..types.plan_type import (
    PlanType, 
    PlanStep, 
    PlanStepStatus,
    BasePlan,
)
from ..types.agent_type import DomainAgentType

def new_plan() -> BasePlan:
    """
    创建新的计划

    Args:
    
    Returns:
        plan: 计划
    """
    

    # TODO: 真实plan

    return BasePlan(
        title="问数",
        plan_id=gen_id(),
        plan_type=PlanType.SEQUENTIAL,
        steps=[
            PlanStep(
                name="分析数据范围",
                description="分析用户需求,确定需要获取的数据范围",
                status=PlanStepStatus.TODO,
                step_id=gen_id(),
                step_index=0,
                domain_agent_type=DomainAgentType.INTENT_AGENT,
            ),
            PlanStep(
                name="获取数据",
                description="读取相关数据,并进行分析",
                status=PlanStepStatus.TODO,
                step_id=gen_id(),
                step_index=1,
                domain_agent_type=DomainAgentType.DATA_AGENT,
            ),
        ],
    )

