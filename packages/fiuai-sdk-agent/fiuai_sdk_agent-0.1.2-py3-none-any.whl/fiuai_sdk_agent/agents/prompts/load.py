# -- coding: utf-8 --
# Project: prompts
# Created Date: 2025-01-30
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI

from datetime import datetime
from typing import Any, Dict, Optional, Literal, List

from jinja2 import Environment, TemplateError, UndefinedError, Undefined

from ...pkg.user_context import get_user_context
from fiuai_sdk_python.utils.logger import get_logger
from ...utils.errors import FiuaiAgentError
from .user_prompt import format_user_profile_info, format_user_simple_auth_info
from .doctype_prompt import show_doctype_overview, show_all_doctype_metas
from .constraints import get_prompt_constraints
from fiuai_sdk_python.doctype import DoctypeOverview
from fiuai_sdk_python.type import DocTypeMeta

logger = get_logger(__name__)


class SilentUndefined(Undefined):
    """自定义 Undefined 类，未定义变量返回空字符串"""
    def __str__(self):
        return ""
    
    def __repr__(self):
        return ""


class PromptService:
    """
    PromptService类,负责prompt模板的加载和参数注入
    """
    
    def __init__(self):
        """初始化PromptService"""
        pass
    
    def load_from_file(
        self,
        file_path: str,
        dict_args: Optional[Dict[str, Any]] = None,
        doctype_overview: Optional[DoctypeOverview] = None,
        doctype_metas: Optional[Dict[str, DocTypeMeta]] = None,
        query_type: Optional[Literal["db", "graph", "pandas"]] = "db",
        only_has_prompt: bool = True,
        json_output_required: bool = False,
        format_instructions: Optional[str] = None,
        important_tips: Optional[List[str]] = None,
    ) -> str:
        """
        从文件加载prompt模板
        
        Args:
            file_path: 模板文件路径
            dict_args: 可选的模板参数字典
            doctype_overview: 可选的 doctype 概览信息，用于替换 <DOCTYPE_OVERVIEW> 标签
            doctype_metas: 可选的 doctype 元数据字典，用于替换 <DOCTYPE_FIELDS> 标签
            query_type: 查询类型，用于格式化 doctype 字段信息，可选值: "db", "graph", "pandas"
            only_has_prompt: 是否只显示有 prompt 的字段
            json_output_required: 是否需要附加 JSON 输出格式要求
            format_instructions: JSON 格式说明字符串，当 json_output_required=True 时必须提供
            important_tips: 可选的重要提示列表，用于替换 <IMPORTANT_TIP> 标签
            
        Returns:
            str: 加载并处理后的prompt字符串
            
        Raises:
            FileNotFoundError: 如果文件不存在
            IOError: 如果文件读取失败
            KeyError: 如果模板中缺少必需的参数
            FiuaiAgentError: 如果 json_output_required=True 但 format_instructions 为空
        """
        if dict_args is None:
            dict_args = {}
        
        if json_output_required and not format_instructions:
            raise FiuaiAgentError("format_instructions is required when json_output_required=True")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                template = f.read()
            
            return self._load_prompt(
                template, 
                dict_args,
                doctype_overview=doctype_overview,
                doctype_metas=doctype_metas,
                query_type=query_type,
                only_has_prompt=only_has_prompt,
                json_output_required=json_output_required,
                format_instructions=format_instructions,
                important_tips=important_tips,
            )
            
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {file_path}")
            raise
        except IOError as e:
            logger.error(f"Failed to read prompt file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load prompt from file {file_path}: {e}")
            raise
    
    def load_from_template(
        self,
        template: str,
        doctype_overview: Optional[DoctypeOverview] = None,
        doctype_metas: Optional[Dict[str, DocTypeMeta]] = None,
        query_type: Optional[Literal["db", "graph", "pandas"]] = "db",
        only_has_prompt: bool = True,
        dict_args: Optional[Dict[str, Any]] = None,
        json_output_required: bool = False,
        format_instructions: Optional[str] = None,
        important_tips: Optional[List[str]] = None,
    ) -> str:
        """
        从模板字符串加载prompt
        
        Args:
            template: 模板字符串
            dict_args: 可选的模板参数字典
            doctype_overview: 可选的 doctype 概览信息，用于替换 <DOCTYPE_OVERVIEW> 标签
            doctype_metas: 可选的 doctype 元数据字典，用于替换 <DOCTYPE_FIELDS> 标签
            query_type: 查询类型，用于格式化 doctype 字段信息，可选值: "db", "graph", "pandas"
            only_has_prompt: 是否只显示有 prompt 的字段
            json_output_required: 是否需要附加 JSON 输出格式要求
            format_instructions: JSON 格式说明字符串，当 json_output_required=True 时必须提供
            important_tips: 可选的重要提示列表，用于替换 <IMPORTANT_TIP> 标签
            
        Returns:
            str: 处理后的prompt字符串
            
        Raises:
            KeyError: 如果模板中缺少必需的参数
            FiuaiAgentError: 如果 json_output_required=True 但 format_instructions 为空
        """
        if dict_args is None:
            dict_args = {}
        
        if json_output_required and not format_instructions:
            raise FiuaiAgentError("format_instructions is required when json_output_required=True")
        
        try:
            return self._load_prompt(
                template, 
                dict_args,
                doctype_overview=doctype_overview,
                doctype_metas=doctype_metas,
                query_type=query_type,
                only_has_prompt=only_has_prompt,
                json_output_required=json_output_required,
                format_instructions=format_instructions,
                important_tips=important_tips,
            )
        except KeyError as e:
            logger.error(f"Missing required template parameter: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load prompt from template: {e}")
            raise
    
    def _load_prompt(
        self,
        template: str,
        dict_args: Dict[str, Any],
        doctype_overview: Optional[DoctypeOverview] = None,
        doctype_metas: Optional[Dict[str, DocTypeMeta]] = None,
        query_type: Optional[Literal["db", "graph", "pandas"]] = "db",
        only_has_prompt: bool = True,
        json_output_required: bool = False,
        format_instructions: Optional[str] = None,
        important_tips: Optional[List[str]] = None,
    ) -> str:
        """
        注入模板参数到模板字符串中，使用 Jinja2 渲染
        
        支持嵌套属性访问，如 {{ user_context.user_simple_auth_info.user_id }}
        支持特殊标签替换: <USER_PROFILE_INFO>, <USER_SIMPLE_AUTH_INFO>, 
                        <DOCTYPE_OVERVIEW>, <DOCTYPE_FIELDS>, <IMPORTANT_TIPS>
        
        Args:
            template: 模板字符串，使用 Jinja2 语法 {{ variable }} 或 {{ obj.attr.subattr }}
            dict_args: 模板参数字典，支持传入对象或字典
            doctype_overview: 可选的 doctype 概览信息，用于替换 <DOCTYPE_OVERVIEW> 标签
            doctype_metas: 可选的 doctype 元数据字典，用于替换 <DOCTYPE_FIELDS> 标签
            query_type: 查询类型，用于格式化 doctype 字段信息
            only_has_prompt: 是否只显示有 prompt 的字段
            json_output_required: 是否需要附加 JSON 输出格式要求
            format_instructions: JSON 格式说明字符串，当 json_output_required=True 时必须提供
            important_tips: 可选的重要提示列表，用于替换 <IMPORTANT_TIP> 标签
            
        Returns:
            str: 处理后的prompt字符串
            
        Raises:
            FiuaiAgentError: 如果模板渲染失败
        """
        if not template:
            logger.error("Empty template provided")
            raise FiuaiAgentError("Empty template provided")
        
        # 注入用户上下文
        user_context = get_user_context()
        if user_context:
            # 将 Pydantic 模型转换为字典，支持嵌套属性访问
            dict_args.update({
                "user_context": user_context.model_dump()
            })
        else:
            logger.error("User context not found")
            raise FiuaiAgentError("User context not found")
        
        # 替换特殊标签 <USER_PROFILE_INFO> 和 <USER_SIMPLE_AUTH_INFO>
        if "<USER_PROFILE_INFO>" in template:
            if user_context.user_profile_info:
                profile_info = format_user_profile_info(user_context.user_profile_info)
            else:
                profile_info = ""
                logger.warning("User profile info is None, replacing <USER_PROFILE_INFO> with empty string")
            template = template.replace("<USER_PROFILE_INFO>", profile_info)
        
        if "<USER_SIMPLE_AUTH_INFO>" in template:
            simple_auth_info = format_user_simple_auth_info(user_context.user_simple_auth_info)
            template = template.replace("<USER_SIMPLE_AUTH_INFO>", simple_auth_info)
        
        # 替换特殊标签 <DOCTYPE_OVERVIEW>
        if "<DOCTYPE_OVERVIEW>" in template:
            if doctype_overview:
                overview_info = show_doctype_overview(doctype_overview)
            else:
                raise FiuaiAgentError("Doctype overview is None, please provide doctype_overview")
            template = template.replace("<DOCTYPE_OVERVIEW>", overview_info)
        
        # 替换特殊标签 <DOCTYPE_FIELDS>
        if "<DOCTYPE_FIELDS>" in template:
            if doctype_metas:
                fields_info = show_all_doctype_metas(
                    doctype_metas=doctype_metas,
                    query_type=query_type,
                    only_has_prompt=only_has_prompt,
                )
            else:
                raise FiuaiAgentError("Doctype metas is None, please provide doctype_metas")
            template = template.replace("<DOCTYPE_FIELDS>", fields_info)
        
        # 替换特殊标签 <IMPORTANT_TIP>
        if "<IMPORTANT_TIPS>" in template:
            if important_tips:
                tips_text = "\n".join([f"- {tip}" for tip in important_tips])
            else:
                tips_text = ""
                logger.warning("Important tips is None or empty, replacing <IMPORTANT_TIP> with empty string")
            template = template.replace("<IMPORTANT_TIPS>", tips_text)

       
        try:
            # 使用 Jinja2 渲染模板
            # 配置 Jinja2 环境，支持嵌套字典访问
            # 使用 Environment 以便更好地控制行为
            env = Environment(
                undefined=SilentUndefined,  # 未定义变量返回空字符串
                trim_blocks=True,  # 去除块首尾空白
                lstrip_blocks=True,  # 去除行首空白
            )
            jinja_template = env.from_string(template)

            text = jinja_template.render(**dict_args)

            # 自动添加统一的 constraints
            constraints_text = get_prompt_constraints()
            text += f"\n\n{constraints_text}"

            text += f"""
当前系统时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """
            
            # 如果需要 JSON 输出格式，附加格式说明
            if json_output_required and format_instructions:
                text += f"""

=====================
输出格式要求
=====================

{format_instructions}
                """

            return text
            
        except UndefinedError as e:
            logger.error(f"Undefined template variable: {e}")
            raise FiuaiAgentError(f"Undefined template variable: {e}")
        except TemplateError as e:
            logger.error(f"Template syntax error: {e}")
            raise FiuaiAgentError(f"Template syntax error: {e}")
        except Exception as e:
            logger.error(f"Failed to render template: {e}")
            raise FiuaiAgentError(f"Failed to render template: {e}")    

