# -- coding: utf-8 --
# Project: prompts
# Created Date: 2025 12 Th
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from typing import List, Dict, Literal, Optional

from ...utils.errors import FiuaiPlatformError
from fiuai_sdk_python.utils.logger import get_logger
from fiuai_sdk_python.doctype import DoctypeOverview, get_platform_doctype_overview
from fiuai_sdk_python.type import DocTypeMeta
from fiuai_sdk_python.datatype import DocFieldType
from fiuai_sdk_python import FiuaiSDK
from fiuai_sdk_python.setup import load_doctype_meta



logger = get_logger(__name__)




def show_doctype_overview(doctype_overview: DoctypeOverview):
    """
    返回用户所有有权限的doctype的概览和其关联的子doctype和link doctype
    """

    r = "## 用户有权限访问的所有doctype的概览和其关联的子doctype和link doctype\n"

    for doctype, info in doctype_overview.doctypes.items():
        r += f"### {doctype} ({info.doctype_prompts})\n"

        if info.link_doctypes:
            r += "#### 关联的link doctype:\n"
            for link_doctype in info.link_doctypes:
                r += f"  - {link_doctype.name} \n"

        if info.child_doctypes:
            r += "#### 拥有的子doctype:\n"
            for child_doctype in info.child_doctypes:
                r += f"  - {child_doctype.name}\n"
    
    return r



def show_all_doctype_metas(
    doctype_metas: Dict[str, DocTypeMeta],
    query_type: Optional[Literal["db", "graph", "pandas"]] = "db",
    only_has_prompt: bool = True,
    indent: int = 2,
) -> str:
    """
    返回所有doctype的metas描述
    """
    r = "## 所有doctype的数据结构信息\n"

    for doctype, doctype_meta in doctype_metas.items():
        r += f"### {doctype}\n" + _show_doctype_fields(doctype_meta, query_type, only_has_prompt) + "\n"
    

    if query_type == "db":
        r += """
**数据表名有空格或者大写字母,请使用引号包裹, 字段名不需要包裹**
**平台使用frappe framework作为底层数据, 子doctype中使用parentfield(父级的字段名), parenttype(父级的doctype名称), parent(父级的id,即父表中的name字段)来反向关联父级doctype, join时请注意使用**
"""
    return r

def _show_doctype_fields(
        doctype_meta: DocTypeMeta,
        query_type: Optional[Literal["db", "graph", "pandas"]] = "db",
        only_has_prompt: bool = True,
    ) -> str:
    """
    返回一个doctype的fields描述
    """

    
    
    r = f'---\nDoctype名称: {doctype_meta.name}, 数据表名 "tab{doctype_meta.name}\n"'

    field_lines = []

    for field in doctype_meta.fields:
        if only_has_prompt:
            if not field.field_prompt or field.field_prompt == "":
                continue

        if query_type is None:
            data_type = field.fieldtype
        else:
            match query_type:
                case "db":
                    data_type = field.fieldtype.to_db_column_type()
                case "graph":
                    data_type = field.fieldtype
                case "pandas":
                    data_type = field.fieldtype.to_pandas_dtype().value
                case _:
                    raise FiuaiPlatformError(f"invalid _show_doctype_fields query_type: {query_type}")


        
        match field.fieldtype:
            case DocFieldType.Link:
                extra_info = f"该字段关联到{field.options[0]}的name字段"
            case DocFieldType.Table:
                extra_info = f"该字段是{field.options[0]}子表对应的字段"
            case _:
                extra_info = ""

        field_lines.append(f"  - 字段名: {field.fieldname}, 数据类型: {data_type}, 描述: {field.field_prompt}, {extra_info}")


    if len(field_lines) == 0:
        logger.warning(f"no fields in doctype {doctype_meta.name}")
        # raise FiuaiPlatformError(f"no fields in doctype {doctype_meta.name}")

    r += "\n".join(field_lines)

    return r