# -- coding: utf-8 --
# Project: context
# Created Date: 2025 12 We
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


from pydantic import BaseModel, Field
from typing import Optional

from fiuai_sdk_python.auth.type import AuthData
from fiuai_sdk_python.profile import UserProfileInfo




class UserContext(BaseModel):
    """
    User context model
    """
    trace_id: str = Field(..., description="trace id")
    user_simple_auth_info: AuthData = Field(..., description="用户信息,包括用户,租户,当前公司,权限")
    user_profile_info: Optional[UserProfileInfo] = Field(default=None, description="用户信息,包括用户,租户,当前公司,权限")

