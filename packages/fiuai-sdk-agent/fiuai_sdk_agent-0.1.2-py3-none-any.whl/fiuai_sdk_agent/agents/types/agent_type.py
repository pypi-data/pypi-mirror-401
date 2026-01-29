# -- coding: utf-8 --
# Project: agents
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from enum import StrEnum


class AgentType(StrEnum):
    """
    Agent类型
    """
    SUPER_AGENT = "super_agent"
    DOMAIN_AGENT = "domain_agent"
    SERVICE_AGENT = "service_agent"


class DomainAgentType(StrEnum):
    """
    Domain Agent类型
    """
    DATA_AGENT = "data_agent"
    TAX_AGENT = "tax_agent"
    FINANCE_AGENT = "finance_agent"
    CASH_AGENT = "cash_agent"
    INTENT_AGENT = "intent_agent"

