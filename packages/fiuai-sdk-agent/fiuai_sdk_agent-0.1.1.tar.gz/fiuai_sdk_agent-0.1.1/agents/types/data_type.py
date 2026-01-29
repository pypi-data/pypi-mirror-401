# -- coding: utf-8 --
# Project: types
# Created Date: 2025 12 Mo
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from fiuai_sdk_python.datatype import Dtype
from pydantic import BaseModel, Field
from enum import StrEnum
from typing import List, Optional, Dict, Any



class DataSource(StrEnum):
    """
    数据源
    """
    DATABASE = "database"
    PLATFORM = "platform"
    ONTOLOGY = "ontology"
    RAG = "rag"

class DatasetType(StrEnum):
    """
    数据集类型
    """
    ROW = "row" # 行级数据
    AGGREGATE = "aggregate" # 聚合


class RuleConstraints(BaseModel):
    """
    用作规则判断的约束条件, 不能被违反的边界, 但是不能是'已经决定的方案'
    """
    main_object: str = Field(..., description="核心对象名称, 取数过程以此为起点")
    related_objects: List[str] = Field(default=[], description="和核心对象有关联的对象名称,可以为空")



class SemanticConstraints(BaseModel):
    """
    语义性约束
    intent,measure,dimension是关键信息,需要准确理解并避免ai在解析的时候产生重叠
    """
    raw_question: str = Field(..., description="用户原始问题")
    intent: str = Field(..., description="用户想解决的业务问题【不包含时间、口径、维度】")
    measure: str = Field(..., description="用于衡量业务的指标口径说明【不描述分组方式】")
    dimension: Optional[str] = Field(default=None, description="数据拆分或对比的维度【不描述指标算法】")
    time_range: Optional[str] = Field(default=None, description="明确的时间范围【只描述时间，不解释业务】")



class DataAgentInput(BaseModel):
    """
    Data Agent 输入结构
    """
    rule_constraints: RuleConstraints = Field(..., description="规则约束,需要严格遵守,不能被违反的边界")
    semantic_constraints: SemanticConstraints = Field(..., description="语义约束,intent,measure,dimension是关键语义信息")
    description: Optional[str] = Field(default=None, description="意图识别的原因,对数据的分析侧重点,可简要说明")


    def get_related_objects_names(self) -> set[str]:
        """
        获取自身和相关对象的名称
        """
        
        strset = set[str]()

        strset.add(self.rule_constraints.main_object)
        for obj in self.rule_constraints.related_objects:
            strset.add(obj)

        return strset


### raw data
class ColumnSpec(BaseModel):
    """
    数据集列规范
    """
    name: str = Field(..., description="数据集列名称")
    prompt: Optional[str] = Field(default=None, description="数据集列提示词")
    dtype: Dtype = Field(..., description="pandas数据集列类型, fiuai_sdk_python中的DocFieldType类型直接使用to_pandas_dtype转化")


class DataSetLine(BaseModel):
    """
    数据集行
    """
    data: Dict[str, Any] = Field(..., description="数据集行")

class RawDataSet(BaseModel):
    """
    原始数据集
    """
    data_source: Optional[DataSource] = Field(..., description="数据源")
    description: Optional[str] = Field(..., description="数据集描述")
    columns: List[ColumnSpec] = Field(..., description="数据集列")
    data: List[List[Any]] = Field(default=[], description="数据集")

