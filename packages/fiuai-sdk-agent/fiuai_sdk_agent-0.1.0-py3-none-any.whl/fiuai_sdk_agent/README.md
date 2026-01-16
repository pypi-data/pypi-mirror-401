# FiuAI SDK Agent

FiuAI SDK Agent 是一个用于构建 AI Agent 的框架，支持 LLM、上下文管理和事件处理。

## 功能特性

- **Agent 基类**: 提供统一的 Agent 基类，支持 LLM 配置和实例管理
- **LLM 管理**: 支持多模型、并发调用、token 统计等功能
- **上下文管理**: 支持消息历史管理、上下文总结等
- **Callbacks/Hooks**: 支持自定义回调函数，包括统计、日志、调试等
- **配置管理**: 支持灵活的配置系统，包括 LLM 配置、日志配置等

## 安装

### 作为 PyPI 包安装

```bash
pip install fiuai-sdk-agent
```

### 作为本地模块使用

如果在本仓库中使用，可以直接导入：

```python
from fiuai_sdk_agent import Agent, AgentType, LLMManager
```

## 快速开始

### 基本使用

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel

class MyAgent(Agent):
    # 定义默认 LLM 模型
    _default_llm_model = LLMModel.OPENAI_GPT4O
    
    # 可选：覆盖默认 LLM 配置
    _default_llm_config = {
        "temperature": 0.7,
        "max_tokens": 2000,
    }
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="my_agent",
            semantic="My custom agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
            enable_context=True,  # 启用上下文管理
            max_context_tokens=16000,  # 上下文最大 token 数
        )
    
    def set_static_knowledge(self) -> None:
        """设置静态知识库（可选）"""
        pass

# 使用
agent = MyAgent(task_id="task_123", thread_id="thread_456")
response = agent.llm.invoke("Hello, world!")
```

## Agent 配置

### 初始化参数

```python
Agent.__init__(
    name: str,                    # Agent 名称
    semantic: str,                 # Agent 语义描述
    type: AgentType,               # Agent 类型（DOMAIN/SERVICE/SUPER_AGENT）
    task_id: str,                 # 任务 ID（用于日志统计）
    thread_id: str,               # 线程 ID（用于日志统计）
    task_name: str = "default",   # 任务名称（用于日志统计）
    enable_context: bool = True,  # 是否启用上下文管理
    max_context_tokens: int = 32000,  # 上下文最大 token 数
    extra_callbacks: Optional[List[BaseCallbackHandler]] = None,  # 额外的 callbacks
)
```

### 类属性配置

```python
class MyAgent(Agent):
    # 默认 LLM 模型（必需）
    _default_llm_model: Optional[LLMModel] = LLMModel.QWEN_PLUS
    
    # 默认 LLM 配置（可选）
    _default_llm_config: Dict[str, Any] = {
        "temperature": 0.3,           # 温度参数
        "max_tokens": 4096,           # 最大 token 数
        "top_p": 1.0,                 # Top-p 采样
        "frequency_penalty": 0.0,     # 频率惩罚
        "presence_penalty": 0.0,      # 存在惩罚
        "streaming": False,           # 是否流式输出
        "max_retries": 3,             # 最大重试次数
        "timeout": 600,               # 超时时间（秒）
    }
```

### Agent 类型

```python
from fiuai_sdk_agent.agents.types import AgentType

# 可用的 Agent 类型
AgentType.SUPER_AGENT    # 超级 Agent
AgentType.DOMAIN_AGENT   # 领域 Agent
AgentType.SERVICE_AGENT  # 服务 Agent
```

## Callbacks/Hooks

Agent 框架提供了多种 Callback 来监控和记录 LLM 调用。

### 默认 Callbacks

Agent 默认会注册以下 callbacks：

1. **AgentLLMCallback**: 统计 token 使用情况、计算费用、记录请求信息
2. **LLMLocalLogCallback**: 将 LLM 使用情况写入本地日志文件
3. **LLMDebugCallback**: 调试日志（根据 LLM_TRACING 和 LLM_LOGGING 配置）

### 自定义 Callbacks

#### 方式 1: 通过 extra_callbacks 参数

```python
from langchain_core.callbacks import BaseCallbackHandler
from fiuai_sdk_agent.pkg.llm.callbacks.local_log_callback import LLMLocalLogCallback

class MyCustomCallback(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        print(f"LLM 调用完成: {response}")

agent = MyAgent(
    task_id="task_123",
    thread_id="thread_456",
    extra_callbacks=[MyCustomCallback()]  # 添加自定义 callback
)
```

#### 方式 2: 动态添加 Callback

```python
# 添加单个 callback
agent.add_default_callback(MyCustomCallback())

# 替换所有默认 callbacks
agent.set_default_callbacks([MyCustomCallback()])
```

### Callback 类型说明

#### AgentLLMCallback

用于统计 token 使用情况和费用计算。

```python
from fiuai_sdk_agent.pkg.llm.callbacks.agent_callback import AgentLLMCallback

callback = AgentLLMCallback(
    agent_name="my_agent",
    agent_type="domain_agent",
    agent_semantic="My agent",
    task_id="task_123",
    task_name="my_task",
    thread_id="thread_456",
    caller="common",  # 调用者标识
    user_id="user_123",
    auth_tenant_id="tenant_123",
    auth_company_id="company_123",
)

# 获取统计信息
stats = callback.get_statistics()
# {
#     "agent_name": "my_agent",
#     "prompt_tokens": 100,
#     "completion_tokens": 50,
#     "total_tokens": 150,
#     "total_cost": 0.001,
#     "request_count": 1,
#     ...
# }
```

#### LLMLocalLogCallback

将 LLM 使用情况写入本地日志文件（JSON 格式）。

```python
from fiuai_sdk_agent.pkg.llm.callbacks.local_log_callback import LLMLocalLogCallback

callback = LLMLocalLogCallback(
    task_id="task_123",
    task_name="my_task",
    user_id="user_123",
    auth_tenant_id="tenant_123",
    auth_company_id="company_123",
)

# 日志会写入到配置的 log_path/llm.log 文件
```

#### LLMDebugCallback

调试日志 callback，根据配置决定是否输出。

```python
from fiuai_sdk_agent.pkg.llm.callbacks.debug_callback import LLMDebugCallback

callback = LLMDebugCallback()

# 当 LLM_TRACING=True 时，会打印到控制台
# 当 LLM_LOGGING=True 时，会写入日志文件
```

### 直接使用日志写入函数

```python
from fiuai_sdk_agent.pkg.llm.callbacks.local_log_callback import write_llm_usage_to_local_log
from datetime import datetime

write_llm_usage_to_local_log(
    task_id="task_123",
    task_name="my_task",
    model="qwen-plus",
    input_token=100,
    output_token=50,
    start_time=datetime.now(),
    end_time=datetime.now(),
    user_id="user_123",
    cost=0.001,
)
```

## LLM 配置

### LLM 模型类型

```python
from fiuai_sdk_agent.pkg.llm.types import LLMModel

# 可用的模型
LLMModel.QWEN_TURBO      # 通义千问 Turbo
LLMModel.QWEN_PLUS       # 通义千问 Plus
LLMModel.QWEN_MAX        # 通义千问 Max
LLMModel.QWEN_INTENT     # 通义千问 Intent
LLMModel.OCR             # OCR 模型
LLMModel.DS_V32          # DeepSeek V3.2
LLMModel.EMBEDDING       # 嵌入模型
LLMModel.MAXBAI_EMBEDDING # MaxBAI 嵌入模型
```

### LLM 设置配置

```python
from fiuai_sdk_agent.pkg.llm.settings import init_llm_settings

# 初始化 LLM 设置
init_llm_settings(
    llm_tracing=False,        # 是否开启 LLM 追踪（打印到控制台）
    llm_timeout_seconds=600,  # LLM 超时时间（秒）
    app_debug=False,          # 是否开启调试模式
    llm_logging=True,         # 是否开启日志记录（写入文件）
    log_path="logs/",         # 日志文件路径
)

# 动态修改设置
from fiuai_sdk_agent.pkg.llm.settings import get_llm_settings

settings = get_llm_settings()
settings.set_llm_tracing(True)
settings.set_llm_timeout(300)
settings.set_app_debug(True)
```

### LLM Vendor 配置

```python
from fiuai_sdk_agent.pkg.llm.llm_config import init_llm_config
from fiuai_sdk_agent.pkg.llm.types import LLMVendor

# 初始化 LLM Vendor 配置
vendors = [
    LLMVendor(
        name="ali",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key="your-api-key",
        timeout=600,
        temperature=0.7,
        max_tokens=4096,
    ),
    LLMVendor(
        name="deepseek",
        base_url="https://api.deepseek.com/v1",
        api_key="your-api-key",
        timeout=600,
    ),
]

init_llm_config(
    configs=vendors,
    debug=False,
    tracing=True,
    default_timeout=600,
)
```

### 使用不同的 LLM 模型

```python
# 使用默认模型
response = agent.llm.invoke("Hello")

# 使用指定模型
llm = agent.get_llm(
    model=LLMModel.QWEN_MAX,
    temperature=0.5,
    max_tokens=2000,
)
response = llm.invoke("Hello")

# 并发调用多个模型
from fiuai_sdk_agent.pkg.llm.types import LLMRequestConfig

configs = [
    LLMRequestConfig(model=LLMModel.QWEN_PLUS, temperature=0.3),
    LLMRequestConfig(model=LLMModel.QWEN_MAX, temperature=0.7),
]

responses = await agent.invoke_llms_parallel(
    messages=[[HumanMessage(content="Hello")]],
    llm_configs=configs,
)
```

## Knowledge（知识库）

Knowledge 模块提供了静态知识库管理功能，用于在 Agent 中存储和访问全局知识信息。

### 概述

`StaticKnowledge` 是一个全局静态知识库，包含：
- **doctype_overview**: 文档类型概览信息
- **doctype_metas**: 文档类型元数据字典
- **important_tips**: 重要提示列表

### 初始化知识库

```python
from fiuai_sdk_agent.agents.knowlege.instance import init_static_knowledge, get_static_knowledge
from fiuai_sdk_agent.agents.types.knowledge_type import StaticKnowledge
from fiuai_sdk_python.doctype import DoctypeOverview
from fiuai_sdk_python.type import DocTypeMeta

# 创建知识库实例
doctype_overview = DoctypeOverview(...)  # 从 fiuai_sdk_python 获取
doctype_metas = {...}  # 文档类型元数据字典
important_tips = ["提示1", "提示2"]

static_knowledge = StaticKnowledge(
    docytypes=doctype_overview,
    doctype_metas=doctype_metas,
    important_tips=important_tips,
)

# 初始化全局知识库
init_static_knowledge(static_knowledge)
```

### 在 Agent 中使用知识库

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.agents.knowlege.instance import get_static_knowledge

class MyAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def set_static_knowledge(self) -> None:
        """设置静态知识库"""
        try:
            self.static_knowledge = get_static_knowledge()
        except FiuaiAgentError:
            # 如果知识库未初始化，可以设置默认值或跳过
            pass
    
    def use_knowledge(self):
        """使用知识库"""
        if self.static_knowledge:
            # 获取文档类型概览
            doctype_overview = self.static_knowledge.docytypes
            
            # 获取文档类型元数据
            doctype_metas = self.static_knowledge.doctype_metas
            
            # 获取重要提示
            important_tips = self.static_knowledge.important_tips
            
            # 获取相关文档类型元数据
            related_metas = self.static_knowledge.get_related_doctype_metas(
                doctype_names={"Customer", "Order"}
            )
```

### 知识库 API

```python
from fiuai_sdk_agent.agents.knowlege.instance import (
    init_static_knowledge,
    get_static_knowledge,
    reset_static_knowledge,
)

# 初始化
init_static_knowledge(static_knowledge)

# 获取（如果未初始化会抛出异常）
knowledge = get_static_knowledge()

# 重置（主要用于测试）
reset_static_knowledge()
```

## Plan（计划管理）

Plan 模块提供了任务计划管理功能，支持多步骤任务的执行、状态管理和动态步骤添加。

### 概述

`PlanManager` 负责管理 Plan 和 Step 的生命周期，包括：
- 计划状态管理（NOT_STARTED → PENDING → RUNNING → COMPLETED/FAILED）
- 步骤状态管理（TODO → RUNNING → COMPLETED/FAILED/SKIPPED）
- 动态添加步骤
- 步骤消息管理

### 基本使用

```python
from fiuai_sdk_agent.agents.plan.manager import PlanManager
from fiuai_sdk_agent.agents.plan.new_plan import new_plan
from fiuai_sdk_agent.agents.types.plan_type import PlanStepStatus, PlanStatus

# 创建计划
plan = new_plan()

# 创建计划管理器
plan_manager = PlanManager(plan=plan)

# 检查是否有计划
if plan_manager.has_plan():
    plan_id = plan_manager.get_plan_id()
    step_id = plan_manager.get_current_step_id()
    step_index = plan_manager.get_current_step_index()
    step_status = plan_manager.get_current_step_status()
```

### 步骤管理

#### 完成步骤

```python
# 完成当前步骤
plan_status, closed_step_info = plan_manager.finish_step(
    message="步骤完成"
)

# closed_step_info 包含:
# {
#     "step_id": "...",
#     "step_index": 0,
#     "step_status": "completed"
# }

# 检查计划状态
if plan_status == PlanStatus.COMPLETED:
    print("计划已完成")
elif plan_status == PlanStatus.RUNNING:
    print("计划继续执行下一步")
```

#### 失败步骤

```python
# 标记步骤失败
plan_status, closed_step_info = plan_manager.fail_step(
    message="步骤执行失败"
)

# 如果计划配置了 failed_on_step_fail=True，计划也会被标记为失败
if plan_status == PlanStatus.FAILED:
    print("计划已失败")
```

#### 动态添加步骤

```python
from fiuai_sdk_python.utils.ids import gen_id
from fiuai_sdk_agent.agents.types.agent_type import DomainAgentType

# 在执行过程中动态添加步骤
plan_manager.add_step(
    name="数据分析",
    description="对结果进行深入分析",
    step_id=gen_id(),
    domain_agent_type=DomainAgentType.DATA_AGENT,
)

# 完成当前步骤后，新添加的步骤会自动成为下一步
plan_status, closed_step_info = plan_manager.finish_step(
    message="当前步骤完成"
)
```

#### 添加步骤消息

```python
from fiuai_sdk_agent.agents.types.event_type import EventType

# 添加步骤消息（用于上下文和前端展示）
plan_manager.add_step_message(
    data="开始处理数据",
    event_type=EventType.CHUNK
)

# 注意：PLAN 和 TASK 类型的事件会被自动过滤
```

#### 调试步骤

```python
# 记录调试信息（不关闭步骤）
plan_manager.debug_step(message="调试信息")
```

### 计划信息更新

```python
# 获取计划信息（用于事件发布）
plan_info = plan_manager.update_event_plan_info()

# 或者指定部分信息
plan_info = plan_manager.update_event_plan_info(
    step_status=PlanStepStatus.COMPLETED.value
)

# plan_info 包含:
# {
#     "plan_id": "...",
#     "step_id": "...",
#     "step_index": 0,
#     "step_status": "completed",
#     "plan_status": "running"
# }
```

### 状态转换规则

#### Plan 状态转换

```
NOT_STARTED → PENDING → RUNNING → COMPLETED/FAILED
     ↓           ↓
  RUNNING    FAILED
```

#### Step 状态转换

```
TODO → RUNNING → COMPLETED/FAILED/SKIPPED
  ↓
SKIPPED
```

所有状态转换都通过 `PlanStateMachine` 进行校验，非法转换会抛出异常。

### 完整示例

```python
from fiuai_sdk_agent.agents.plan.manager import PlanManager
from fiuai_sdk_agent.agents.plan.new_plan import new_plan
from fiuai_sdk_agent.agents.types.plan_type import PlanStepStatus, PlanStatus

# 创建计划和管理器
plan = new_plan()
plan_manager = PlanManager(plan=plan)

# 添加步骤消息
plan_manager.add_step_message(
    data="开始执行步骤",
    event_type=EventType.CHUNK
)

# 执行业务逻辑
try:
    result = await execute_business_logic()
    
    # 完成步骤
    plan_status, closed_step_info = plan_manager.finish_step(
        message="步骤执行成功"
    )
    
    # 根据计划状态决定后续操作
    if plan_status == PlanStatus.COMPLETED:
        print("所有步骤已完成")
    elif plan_status == PlanStatus.RUNNING:
        # 继续执行下一步
        next_step_id = plan_manager.get_current_step_id()
        print(f"继续执行步骤: {next_step_id}")
        
except Exception as e:
    # 标记步骤失败
    plan_status, closed_step_info = plan_manager.fail_step(
        message=f"步骤执行失败: {str(e)}"
    )
    
    if plan_status == PlanStatus.FAILED:
        print("计划已失败，停止执行")
```

## Context（上下文管理）

Context 模块提供了 Agent 对话上下文管理功能，支持消息历史、上下文总结和多 Agent 上下文传递。

### 概述

`AgentContextManager` 负责管理 Agent 的对话上下文，包括：
- 消息历史管理
- 上下文总结生成（当超过 token 限制时）
- Agent 总结（用于传递给其他 Agent）
- 上下文导入/导出

### 启用上下文管理

```python
agent = MyAgent(
    task_id="task_123",
    thread_id="thread_456",
    enable_context=True,        # 启用上下文管理
    max_context_tokens=32000,   # 上下文最大 token 数
)
```

### 基本操作

#### 添加消息

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 添加单个消息
agent.add_message(HumanMessage(content="用户消息"))
agent.add_message(AIMessage(content="AI 回复"))
agent.add_message(SystemMessage(content="系统提示"))

# 批量添加消息
agent.add_messages([
    HumanMessage(content="消息1"),
    HumanMessage(content="消息2"),
])
```

#### 获取消息历史

```python
# 获取所有消息（包含上下文总结）
messages = agent.get_messages(include_summaries=True)

# 获取消息历史（不包含总结）
messages = agent.get_messages(include_summaries=False)

# 在 LLM 调用中使用
response = agent.llm.invoke(messages)
```

#### 清空消息历史

```python
# 清空所有消息
agent.clear_messages()
```

### 上下文总结

当消息历史超过 `max_context_tokens` 限制时，会自动触发上下文总结。

#### 生成上下文总结

```python
# 手动生成上下文总结（预留方法，未来实现）
summary = await agent.context_manager.generate_context_summary(
    llm=agent.llm,
    messages_to_summarize=None  # None 表示总结所有消息
)

# 添加上下文总结
if summary:
    agent.context_manager.add_context_summary(summary)
```

#### 上下文总结历史

```python
# 获取上下文总结历史
summaries = agent.context_manager._context_summaries

# 获取消息时会自动包含总结
messages = agent.get_messages(include_summaries=True)
# 返回的消息列表会包含 SystemMessage 格式的总结
```

### Agent 总结

Agent 总结用于在多 Agent 体系中传递执行结果。

#### 设置 Agent 总结

```python
from fiuai_sdk_agent.agents.context.types import AgentSummary
from datetime import datetime

# 创建 Agent 总结
agent_summary = AgentSummary(
    agent_name="my_agent",
    agent_type="domain_agent",
    task_id="task_123",
    status="success",
    summary="执行成功，完成了数据查询和分析",
    key_findings=["发现1", "发现2"],
    actions_taken=["动作1", "动作2"],
    outputs={"result": "..."},
    started_at=datetime.now(),
    completed_at=datetime.now(),
    duration=1.5,
)

# 设置 Agent 总结
agent.context_manager.set_agent_summary(agent_summary)
```

#### 获取 Agent 总结

```python
# 获取 Agent 总结
summary = agent.context_manager.get_agent_summary()

if summary:
    print(f"Agent: {summary.agent_name}")
    print(f"状态: {summary.status}")
    print(f"总结: {summary.summary}")
```

### 上下文传递

#### 导出上下文

```python
# 导出上下文（用于传递给其他 Agent）
context_data = agent.export_context()

# context_data 包含:
# {
#     "agent_name": "...",
#     "agent_type": "...",
#     "task_id": "...",
#     "thread_id": "...",
#     "agent_summary": {...},
#     "recent_messages": [...],
#     "context_summaries": [...]
# }
```

#### 导入上下文

```python
# 从其他 Agent 导入上下文
agent.import_context(context_data)

# 导入后，Agent 总结和上下文总结会被添加到当前上下文
```

### 统计信息

```python
# 获取上下文统计信息
stats = agent.context_manager.get_statistics()

# {
#     "agent_name": "...",
#     "agent_type": "...",
#     "task_id": "...",
#     "thread_id": "...",
#     "message_count": 10,
#     "total_tokens": 5000,
#     "context_summaries_count": 1,
#     "has_agent_summary": True
# }
```

### 完整示例

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel
from langchain_core.messages import HumanMessage, AIMessage

class ContextAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="context_agent",
            semantic="上下文 Agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
            enable_context=True,
            max_context_tokens=16000,
        )
    
    async def chat(self, user_message: str):
        """对话方法"""
        # 添加用户消息
        self.add_message(HumanMessage(content=user_message))
        
        # 获取历史消息（包含上下文总结）
        messages = self.get_messages(include_summaries=True)
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        
        # 添加 AI 回复
        self.add_message(AIMessage(content=response.content))
        
        return response.content
    
    def export_for_other_agent(self):
        """导出上下文给其他 Agent"""
        return self.export_context()
    
    def import_from_other_agent(self, context_data):
        """从其他 Agent 导入上下文"""
        self.import_context(context_data)

# 使用
agent = ContextAgent(task_id="task_123", thread_id="thread_456")

# 多轮对话
response1 = await agent.chat("你好")
response2 = await agent.chat("介绍一下你自己")

# 导出上下文
context_data = agent.export_for_other_agent()

# 在其他 Agent 中使用
other_agent = ContextAgent(task_id="task_123", thread_id="thread_456")
other_agent.import_from_other_agent(context_data)
```

## 日志配置

SDK 使用 `fiuai_sdk_python` 的 logger，请参考 `fiuai_sdk_python` 的文档进行配置。

```python
from fiuai_sdk_python.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Info message")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
```

## 完整示例

### 示例 1: 基础 Agent

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel
from langchain_core.messages import HumanMessage

class SimpleAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="simple_agent",
            semantic="简单 Agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
        )

# 使用
agent = SimpleAgent(task_id="task_123", thread_id="thread_456")
response = agent.llm.invoke([HumanMessage(content="你好")])
print(response.content)
```

### 示例 2: 带自定义 Callback 的 Agent

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class MyCallback(BaseCallbackHandler):
    def on_llm_end(self, response: LLMResult, **kwargs):
        print(f"Token 使用: {response.llm_output.get('token_usage', {})}")

class CustomAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="custom_agent",
            semantic="自定义 Agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
            extra_callbacks=[MyCallback()],  # 添加自定义 callback
        )

# 使用
agent = CustomAgent(task_id="task_123", thread_id="thread_456")
response = agent.llm.invoke([HumanMessage(content="你好")])
```

### 示例 3: 带上下文管理的 Agent

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel
from langchain_core.messages import HumanMessage, AIMessage

class ContextAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="context_agent",
            semantic="上下文 Agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
            enable_context=True,
            max_context_tokens=16000,
        )
    
    async def chat(self, user_message: str):
        # 添加用户消息
        self.add_message(HumanMessage(content=user_message))
        
        # 获取历史消息（包含上下文总结）
        messages = self.get_messages(include_summaries=True)
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        
        # 添加 AI 回复
        self.add_message(AIMessage(content=response.content))
        
        return response.content

# 使用
agent = ContextAgent(task_id="task_123", thread_id="thread_456")
response = await agent.chat("你好")
print(response)
```

### 示例 4: 并发调用多个模型

```python
from fiuai_sdk_agent import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel, LLMRequestConfig
from langchain_core.messages import HumanMessage

class MultiModelAgent(Agent):
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="multi_model_agent",
            semantic="多模型 Agent",
            type=AgentType.DOMAIN,
            task_id=task_id,
            thread_id=thread_id,
        )
    
    async def compare_models(self, prompt: str):
        # 配置多个模型
        configs = [
            LLMRequestConfig(
                model=LLMModel.QWEN_PLUS,
                temperature=0.3,
            ),
            LLMRequestConfig(
                model=LLMModel.QWEN_MAX,
                temperature=0.7,
            ),
        ]
        
        # 并发调用
        responses = await self.invoke_llms_parallel(
            messages=[[HumanMessage(content=prompt)]],
            llm_configs=configs,
        )
        
        return [r.content for r in responses if r.success]

# 使用
agent = MultiModelAgent(task_id="task_123", thread_id="thread_456")
results = await agent.compare_models("解释一下 AI")
for i, result in enumerate(results):
    print(f"模型 {i+1}: {result}")
```

## 依赖说明

### 必需依赖

- `fiuai-sdk-python>=0.6.3`: FiuAI SDK Python 客户端
- `langchain>=1.2.0`: LangChain 框架
- `langchain-openai>=1.1.6`: LangChain OpenAI 集成
- `pydantic>=2.0.0`: 数据验证
- `redis>=7.1.0`: Redis 客户端（用于事件处理，可选）
- `httpx>=0.27.0`: HTTP 客户端
- `tenacity>=8.0.0`: 重试库
- `snowflake-id>=1.0.2`: 雪花算法 ID 生成

### 可选依赖

- `pkg.db`: 数据库支持（用于 LLM 使用日志记录，如果未安装则日志功能会被禁用）

## 开发

### 本地开发

1. 克隆仓库
2. 安装依赖：`pip install -e .`
3. 运行测试：`pytest`

### 发布到 PyPI

```bash
cd fiuai_sdk_agent
python -m build
twine upload dist/*
```

或者使用发布脚本：

```bash
./publish_sdk_agent.sh
```

## 架构说明

### SDK 层 vs 业务层

- **SDK 层** (`fiuai_sdk_agent/`): 通用框架，不依赖业务配置
  - Agent 基类
  - LLM 管理
  - 上下文管理
  - 类型定义（EventType、EventData 等）
  - 本地日志 Callback

- **业务层** (`agents/`): 业务特定实现
  - 数据库日志 Callback
  - 事件管理（EventManager、TaskEvent）
  - 业务特定的 Agent 实现

### 设计原则

1. **可扩展性**: 通过 Callbacks 和配置系统支持扩展
2. **可配置性**: 所有功能都可通过配置控制
3. **可观测性**: 内置统计、日志、调试功能
4. **独立性**: SDK 层不依赖业务配置，可独立发布

## 许可证

Copyright (c) 2025 FiuAI
