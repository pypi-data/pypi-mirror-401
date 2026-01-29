# -- coding: utf-8 --
# Project: types
# Created Date: 2025 12 Th
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List

from fiuai_sdk_python.doctype import DoctypeOverview
from fiuai_sdk_python.type import DocTypeMeta

class StaticKnowledge(BaseModel):
    """
    全局通用的静态知识库
    """
    docytypes: DoctypeOverview = Field(..., description="文档类型")
    doctype_metas: Dict[str, DocTypeMeta] = Field(..., description="文档类型meta")
    important_tips: List[str] = Field(default=[], description="重要提示,用于提示用户注意某些事项")



    # 允许额外字段
    model_config = ConfigDict(extra="allow")



    def get_related_doctype_metas(self, doctype_names: set[str]) -> Dict[str, DocTypeMeta]:
        """
        获取相关文档类型的meta
        """
        return {doctype: self.doctype_metas[doctype] for doctype in doctype_names}
