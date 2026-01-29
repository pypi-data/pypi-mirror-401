# -- coding: utf-8 --
# Project: user_context
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from .user import UserContext
from .context_manager import UserContextManager

# 便捷函数，可以直接导入使用
def get_user_context():
    """快速获取当前用户上下文"""
    return UserContextManager.get()

def get_auth_data():
    """快速获取当前认证数据"""
    return UserContextManager.get_auth_data()

def get_user_id():
    """快速获取当前用户 ID"""
    return UserContextManager.get_user_id()

def get_tenant_id():
    """快速获取当前租户 ID"""
    return UserContextManager.get_tenant_id()

def get_company():
    """快速获取当前公司 ID"""
    return UserContextManager.get_company()

def get_company_unique_no():
    """快速获取当前公司唯一编号"""
    return UserContextManager.get_company_unique_no()

def get_trace_id():
    """快速获取当前追踪 ID"""
    return UserContextManager.get_trace_id()

def get_user_profile_info():
    """快速获取当前用户配置信息"""
    return UserContextManager.get_user_profile_info()

__all__ = [
    "UserContext",
    "UserContextManager",
    "get_user_context",
    "get_auth_data",
    "get_user_id",
    "get_tenant_id",
    "get_company",
    "get_company_unique_no",
    "get_trace_id",
    "get_user_profile_info",
]

