# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-01-29
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import Dict, Optional
from dataclasses import dataclass



@dataclass
class ModelPrice:
    """
    模型价格配置
    
    价格单位：元/千 token
    """
    input_price_per_1k: float  # 输入价格（元/千 token）
    output_price_per_1k: float  # 输出价格（元/千 token）
    currency: str = "CNY"  # 货币单位


class ModelPriceConfig:
    """
    模型价格配置管理器
    
    支持从内存配置加载，未来可扩展为从数据库加载
    """
    
    # 默认价格配置（写死，未来可从数据库加载）
    _default_prices: Dict[str, ModelPrice] = {
        # 阿里云 Qwen 模型
        "qwen-turbo": ModelPrice(input_price_per_1k=0.003, output_price_per_1k=0.006),
        "qwen-plus": ModelPrice(input_price_per_1k=0.012, output_price_per_1k=0.012),
        "qwen-max": ModelPrice(input_price_per_1k=0.12, output_price_per_1k=0.12),
        "qwen-intent": ModelPrice(input_price_per_1k=0.003, output_price_per_1k=0.006),
        "qwen-vl-plus": ModelPrice(input_price_per_1k=0.008, output_price_per_1k=0.008),
        
        # DeepSeek 模型
        "deepseek-chat": ModelPrice(input_price_per_1k=0.0014, output_price_per_1k=0.0028),
        "deepseek-reasoner": ModelPrice(input_price_per_1k=0.055, output_price_per_1k=0.11),
        
        # 其他模型
        "embedding": ModelPrice(input_price_per_1k=0.0007, output_price_per_1k=0.0),
        "maxbai_embedding": ModelPrice(input_price_per_1k=0.0, output_price_per_1k=0.0),  # 本地模型免费
    }
    
    _instance: Optional['ModelPriceConfig'] = None
    _prices: Dict[str, ModelPrice] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._prices = cls._default_prices.copy()
        return cls._instance
    
    def get_price(self, model_name: str) -> Optional[ModelPrice]:
        """
        获取模型价格配置
        
        Args:
            model_name: 模型名称
            
        Returns:
            ModelPrice 或 None（如果未找到）
        """
        return self._prices.get(model_name)
    
    def set_price(self, model_name: str, price: ModelPrice) -> None:
        """
        设置模型价格配置
        
        Args:
            model_name: 模型名称
            price: 价格配置
        """
        self._prices[model_name] = price
    
    def update_prices(self, prices: Dict[str, ModelPrice]) -> None:
        """
        批量更新价格配置
        
        Args:
            prices: 价格配置字典
        """
        self._prices.update(prices)
    
    def reload_from_database(self) -> None:
        """
        从数据库重新加载价格配置
        
        这是一个预留方法，未来实现时将从数据库加载价格配置
        """
        # TODO: 从数据库加载价格配置
        # 1. 连接数据库
        # 2. 查询模型价格表
        # 3. 更新 _prices 字典
        # 4. 可选：设置缓存过期时间
        pass
    
    def calculate_cost(
        self,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> Optional[float]:
        """
        计算费用
        
        Args:
            model_name: 模型名称
            prompt_tokens: 输入 token 数
            completion_tokens: 输出 token 数
            
        Returns:
            费用（元），如果模型未配置价格则返回 None
        """
        price = self.get_price(model_name)
        if price is None:
            return None
        
        # 按千 token 计算
        input_cost = (prompt_tokens / 1000.0) * price.input_price_per_1k
        output_cost = (completion_tokens / 1000.0) * price.output_price_per_1k
        
        return input_cost + output_cost


# 全局单例实例
_model_price_config: Optional[ModelPriceConfig] = None


def get_model_price_config() -> ModelPriceConfig:
    """
    获取模型价格配置单例
    
    Returns:
        ModelPriceConfig 实例
    """
    global _model_price_config
    if _model_price_config is None:
        _model_price_config = ModelPriceConfig()
    return _model_price_config

