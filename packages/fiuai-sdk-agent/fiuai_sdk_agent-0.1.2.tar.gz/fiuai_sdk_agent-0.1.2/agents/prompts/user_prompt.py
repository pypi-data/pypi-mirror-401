# -- coding: utf-8 --
# Project: prompts
# Created Date: 2025 12 Th
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Optional

from fiuai_sdk_python.profile import UserProfileInfo
from fiuai_sdk_python.auth.type import AuthData

from fiuai_sdk_python.utils.logger import get_logger
from ...utils.errors import FiuaiAgentError

logger = get_logger(__name__)


def format_user_profile_info(profile_info: UserProfileInfo) -> str:
    """
    格式化用户profile信息，描述用户、用户公司、用户权限等信息
    
    Args:
        profile_info: 用户profile信息对象
    
    Returns:
        str: 格式化后的用户profile信息描述
    """
    if not profile_info:
        return ""
    
    lines = []
    lines.append("=== 用户信息 ===")
    
    # 用户基本信息
    if hasattr(profile_info, 'user_id') and profile_info.user_id:
        lines.append(f"用户ID: {profile_info.user_id}")
    if hasattr(profile_info, 'user_name') and profile_info.user_name:
        lines.append(f"用户名: {profile_info.user_name}")
    if hasattr(profile_info, 'email') and profile_info.email:
        lines.append(f"邮箱: {profile_info.email}")
    
    # 公司信息
    has_company = (
        (hasattr(profile_info, 'current_company') and profile_info.current_company) or
        (hasattr(profile_info, 'company_name') and profile_info.company_name)
    )
    if has_company:
        lines.append("\n=== 公司信息 ===")
        if hasattr(profile_info, 'current_company') and profile_info.current_company:
            lines.append(f"公司ID: {profile_info.current_company}")
        if hasattr(profile_info, 'company_name') and profile_info.company_name:
            lines.append(f"公司名称: {profile_info.company_name}")
        if hasattr(profile_info, 'company_unique_no') and profile_info.company_unique_no:
            lines.append(f"公司统一社会信用代码: {profile_info.company_unique_no}")
    
    # 权限信息
    has_permission = (
        (hasattr(profile_info, 'roles') and profile_info.roles) or
        (hasattr(profile_info, 'permissions') and profile_info.permissions)
    )
    if has_permission:
        lines.append("\n=== 权限信息 ===")
        if hasattr(profile_info, 'roles') and profile_info.roles:
            roles = profile_info.roles
            if isinstance(roles, list):
                lines.append(f"角色: {', '.join(str(r) for r in roles)}")
            else:
                lines.append(f"角色: {roles}")
        if hasattr(profile_info, 'permissions') and profile_info.permissions:
            permissions = profile_info.permissions
            if isinstance(permissions, list):
                lines.append(f"权限: {', '.join(str(p) for p in permissions)}")
            else:
                lines.append(f"权限: {permissions}")
    
    # 租户信息
    has_tenant = (
        (hasattr(profile_info, 'auth_tenant_id') and profile_info.auth_tenant_id) or
        (hasattr(profile_info, 'tenant_name') and profile_info.tenant_name)
    )
    if has_tenant:
        lines.append("\n=== 租户信息 ===")
        if hasattr(profile_info, 'auth_tenant_id') and profile_info.auth_tenant_id:
            lines.append(f"租户ID: {profile_info.auth_tenant_id}")
        if hasattr(profile_info, 'tenant_name') and profile_info.tenant_name:
            lines.append(f"租户名称: {profile_info.tenant_name}")
    
    return "\n".join(lines) if lines else ""


def format_user_simple_auth_info(auth_info: AuthData) -> str:
    """
    格式化用户简单认证信息，提供简洁的描述
    
    Args:
        auth_info: 用户认证信息对象
    
    Returns:
        str: 格式化后的用户简单认证信息描述
    """
    if not auth_info:
        return ""
    
    lines = []
    
    # 用户ID
    if hasattr(auth_info, 'user_id') and auth_info.user_id:
        lines.append(f"用户: {auth_info.user_id}")
    
    # 租户ID
    if hasattr(auth_info, 'auth_tenant_id') and auth_info.auth_tenant_id:
        lines.append(f"租户: {auth_info.auth_tenant_id}")
    
    # 公司信息
    if hasattr(auth_info, 'current_company') and auth_info.current_company:
        lines.append(f"当前公司: {auth_info.current_company}")
    if hasattr(auth_info, 'company_unique_no') and auth_info.company_unique_no:
        lines.append(f"公司统一社会信用代码: {auth_info.company_unique_no}")
    
    return " | ".join(lines) if lines else ""

