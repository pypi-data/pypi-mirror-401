# -- coding: utf-8 --
# Project: types
# Created Date: 2025 12 Th
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


from enum import StrEnum
from pydantic import BaseModel, Field

class IntentType(StrEnum):
    """
    Intent type
    """
    IDP = "idp"
    DATA = "data"
    CHAT = "chat"
    TASK = "task"


class UserIntent(BaseModel):
    """
    User intent model
    """
    intent_type: IntentType = Field(..., description="意图类型")
    user_input: str = Field(..., description="用户原始输入")
    description: str = Field(..., description="意图描述,和判断原因,类似简单的深度思考")