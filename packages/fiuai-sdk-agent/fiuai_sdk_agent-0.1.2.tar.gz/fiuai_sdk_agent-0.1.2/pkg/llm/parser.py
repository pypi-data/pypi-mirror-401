# -- coding: utf-8 --
# Project: llm
# Created Date: 2025-12-09
# Author: liming
# Email: lmlala@aliyun.com
# Copyright (c) 2025 FiuAI


import re
from typing import Any, Optional


def clean_markdown_code_blocks(content: str) -> str:
    """
    清理字符串中的 markdown 代码块标记
    
    用于清理 LLM 响应中可能包含的 markdown 代码块标记（```），
    避免这些标记导致后续处理（如数据库存储）时的语法错误。
    
    Args:
        content: 需要清理的内容
        
    Returns:
        清理后的内容
        
    Example:
        >>> clean_markdown_code_blocks('```\\n<summary>\\n内容\\n```')
        '<summary>\\n内容'
        >>> clean_markdown_code_blocks('```markdown\\n内容\\n```')
        '内容'
    """
    if not isinstance(content, str):
        return content
    
    # 移除开头的 ``` 和可能的语言标识符（如 ```markdown, ```text 等）
    content = re.sub(r'^```[\w]*\s*\n?', '', content, flags=re.MULTILINE)
    # 移除结尾的 ```（可能在不同行）
    content = re.sub(r'\n?```\s*$', '', content, flags=re.MULTILINE)
    # 清理多余的空白和换行
    content = content.strip()
    
    return content


def extract_xml_tag_content(content: str, tag_name: str) -> Optional[str]:
    """
    从内容中提取 XML/HTML 标签内的文本
    
    Args:
        content: 需要解析的内容
        tag_name: 标签名称（不包含尖括号）
        
    Returns:
        提取的标签内容，如果未找到则返回 None
        
    Example:
        >>> extract_xml_tag_content('<summary>内容</summary>', 'summary')
        '内容'
    """
    if not isinstance(content, str):
        return None
    
    pattern = rf"<{tag_name}>(.*?)</{tag_name}>"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return None


def parse_llm_response(
    response: Any,
    extract_tag: Optional[str] = None,
    clean_markdown: bool = True,
) -> str:
    """
    解析 LLM 响应内容
    
    通用的 LLM 响应解析函数，用于处理非 langchain parse 的响应。
    支持：
    1. 提取响应内容（支持 langchain 的 response.content）
    2. 提取 XML/HTML 标签内容（可选）
    3. 清理 markdown 代码块标记（可选）
    
    Args:
        response: LLM 响应对象（可以是 langchain 的响应或其他格式）
        extract_tag: 可选，要提取的 XML/HTML 标签名称（如 'summary'）
        clean_markdown: 是否清理 markdown 代码块标记，默认为 True
        
    Returns:
        解析后的纯文本内容
        
    Example:
        >>> # 基本用法
        >>> parse_llm_response(response)
        '纯文本内容'
        
        >>> # 提取标签内容
        >>> parse_llm_response(response, extract_tag='summary')
        'summary 标签内的内容'
        
        >>> # 不清理 markdown
        >>> parse_llm_response(response, clean_markdown=False)
        '保留 markdown 标记的内容'
    """
    # 提取响应内容
    if hasattr(response, "content"):
        content = response.content
    elif isinstance(response, str):
        content = response
    else:
        content = str(response)
    
    # 确保是字符串类型
    if not isinstance(content, str):
        content = str(content)
    
    # 提取标签内容（如果指定）
    if extract_tag:
        extracted = extract_xml_tag_content(content, extract_tag)
        if extracted is not None:
            content = extracted
    
    # 清理 markdown 代码块标记（如果需要）
    if clean_markdown:
        content = clean_markdown_code_blocks(content)
    else:
        # 即使不清理 markdown，也清理首尾空白
        content = content.strip()
    
    return content



