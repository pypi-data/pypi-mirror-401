# Agent 基类使用指南

## 概述

`Agent` 基类提供了统一的 Agent 框架，支持 LLM 管理、计划管理、状态管理和事件发布等功能。

## 核心特性

- **LLM 管理**: 统一的 LLM 配置和实例管理，支持多模型并发调用
- **计划管理**: 支持 Plan 和 Step 的生命周期管理，支持动态添加步骤
- **状态管理**: 统一的 LangGraph state 管理，支持类型校验
- **事件发布**: 可选的事件发布功能，支持计划信息同步
- **上下文管理**: 可选的上下文管理，支持消息历史和总结

## 快速开始

### 1. 创建 Agent 子类

```python
from fiuai_sdk_agent.agents import Agent, AgentType
from fiuai_sdk_agent.pkg.llm.types import LLMModel

class MyAgent(Agent):
    """自定义 Agent"""
    
    # 定义默认 LLM 模型
    _default_llm_model = LLMModel.QWEN_PLUS
    
    def __init__(self, task_id: str, thread_id: str):
        super().__init__(
            name="MyAgent",
            semantic="我的 Agent 描述",
            type=AgentType.DOMAIN_AGENT,
            task_id=task_id,
            thread_id=thread_id,
            enable_context=True,  # 启用上下文管理
            enable_event_publish=True,  # 启用事件发布
        )
    
    def set_static_knowledge(self) -> None:
        """设置静态知识库"""
        # 实现知识库设置逻辑
        pass
```

### 2. 在 LangGraph 节点中使用

```python
from agents.state.common_state import FiuaiAgentTaskState
from langchain_core.runnables import RunnableConfig

async def my_node(self, state: FiuaiAgentTaskState, config: RunnableConfig):
    """
    LangGraph 节点方法
    """
    # 1. 设置 state（确保 self.state 和传入的 state 保持一致）
    self.set_state(state)
    
    # 2. 从 state 加载 plan（使用无参数版本，自动使用 self.state）
    self.load_plan_from_state()
    
    # 3. 执行业务逻辑
    result = await self.process_data()
    
    # 4. 记录调试信息（不关闭步骤）
    self.debug_step(message="开始处理数据")
    
    # 5. 完成步骤
    self.close_step(message="数据处理完成", status=PlanStepStatus.COMPLETED)
    
    # 6. 使用统一方法返回状态更新（自动包含 plan、chat_history 等）
    return self.get_state_updates(
        result=result,  # 节点特定的字段
        # ... 其他字段
    )
```

## 核心功能详解

### 1. State 管理

#### 设置和获取 State

```python
# 设置 state（会自动进行类型校验）
self.set_state(state)  # state 必须是 BasicStateInfo 或其子类

# 获取 state
current_state = self.get_state()

# 检查是否有 state
if self.has_state():
    # 使用 state
    pass
```

#### 从 State 加载 Plan

```python
# 方式1: 使用 self.state（推荐）
self.set_state(state)
self.load_plan_from_state()  # 无参数版本

# 方式2: 直接传入 state 参数（向后兼容）
self.load_plan_from_state(state)
```

#### 同步 Plan 到 State

```python
# 方式1: 使用 self.state（推荐）
plan_updates = self.sync_plan_to_state()  # 无参数版本

# 方式2: 直接传入 state 参数（向后兼容）
plan_updates = self.sync_plan_to_state(state)
```

### 2. Plan 和 Step 管理

#### 创建计划

```python
from fiuai_sdk_agent.agents.types.plan_type import BasePlan

# 创建计划
plan = BasePlan(
    title="我的计划",
    plan_id=gen_id(),
    # ... 其他字段
)

# 创建并启动计划
self.create_plan(plan)
```

#### 步骤管理

```python
# 完成步骤
plan_status = self.finish_step(message="步骤完成")

# 标记步骤失败
plan_status = self.fail_step(message="步骤失败")

# 关闭步骤（自定义状态）
plan_status = self.close_step(
    message="步骤完成",
    status=PlanStepStatus.COMPLETED  # 或 FAILED、SKIPPED
)
# 注意：close_step() 会自动：
# 1. 更新 plan/step 状态
# 2. 同步 EventPublisher 的 plan_info（使用刚关闭的步骤信息）
# 3. 发布步骤关闭消息到事件服务器

# 记录调试信息（不关闭步骤）
self.debug_step(message="调试信息")

# 动态添加步骤
self.add_step(
    name="新步骤",
    description="步骤描述",
    step_id=gen_id(),
    domain_agent_type=DomainAgentType.DATA_AGENT,
)
```

**close_step() 的状态同步机制**：

`close_step()` 方法实现了完整的状态同步机制，确保事件发布时使用正确的步骤信息：

1. **保存刚关闭的步骤信息**：在关闭步骤之前，保存当前步骤的 `step_id`、`step_index` 和状态
2. **关闭步骤并可能启动下一步**：调用 `PlanManager.close_step()` 关闭当前步骤，如果成功则启动下一步（此时 `plan.current_step_index` 和 `plan.current_step_id` 会更新为新步骤的值）
3. **使用刚关闭的步骤信息更新 EventPublisher**：使用保存的刚关闭步骤信息（而不是新步骤的信息）更新 `EventPublisher` 的 `plan_info`
4. **发布事件**：发布步骤关闭消息，事件中携带的是刚关闭的步骤信息

这样设计的原因：
- 事件应该反映"刚关闭的步骤"的状态，而不是"新启动的步骤"的状态
- 确保事件中的 `step_status` 是刚关闭步骤的状态（COMPLETED/FAILED/SKIPPED），而不是计划状态（RUNNING/COMPLETED/FAILED）

#### 获取步骤信息

```python
# 通过 PlanManager 获取
plan_manager = self._get_plan_manager()
if plan_manager:
    step_id = plan_manager.get_current_step_id()
    step_index = plan_manager.get_current_step_index()
    step_status = plan_manager.get_current_step_status()
```

### 3. 统一的状态更新方法

#### 使用 get_state_updates()

```python
# 在节点方法中返回更新
async def my_node(self, state: FiuaiAgentTaskState, config: RunnableConfig):
    self.set_state(state)
    self.load_plan_from_state()
    
    # ... 执行业务逻辑 ...
    
    # 使用统一方法返回更新
    # 自动包含: plan, plan_id, chat_history（如果子类实现了）
    return self.get_state_updates(
        intent=intent,  # 节点特定的字段
        data_agent_input=data_agent_input,
        raw_data_set=raw_data_set,
        # ... 其他字段
    )
```

#### 自定义 chat_history 更新

如果子类需要返回 chat_history 增量，需要实现 `_get_chat_history_updates()` 方法：

```python
class MyAgent(Agent):
    def _get_chat_history_updates(self) -> Dict[str, Any]:
        """获取聊天历史增量更新"""
        if not self._chat_log_service:
            return {}
        
        # 获取新增的消息
        current_messages = self._chat_log_service.history_to_messages()
        if len(current_messages) > self._last_chat_history_count:
            # 返回完整的消息列表（LangGraph 需要完整列表）
            self._last_chat_history_count = len(current_messages)
            return {"chat_history": current_messages}
        
        return {}
```

### 4. 事件发布

#### 发布事件

```python
# 发布普通事件
self.publish(data="消息内容", event_type=EventTypeEnum.STR)

# 发布到主容器（不关联 plan）
self.publish(
    data="消息内容",
    event_type=EventTypeEnum.STR,
    publish_to_plan=False,
)
```

#### 更新事件计划信息

```python
# 手动更新计划信息
self.update_event_plan_info(
    plan_id=plan_id,
    step_id=step_id,
    step_index=step_index,
    step_status=step_status,
)
```

#### close_step 的事件发布机制

`close_step()` 方法实现了完整的状态同步和事件发布机制，确保事件中的 step_id、step_index、step_status 与实际的 plan 状态一致。

**机制说明**：

1. **状态同步流程**：
   ```
   Agent.close_step() 被调用
   ↓
   PlanManager.close_step() 执行：
   - 保存当前步骤信息（关闭前）
   - 关闭当前步骤
   - 可能启动下一步（更新 plan.current_step_index/step_id）
   - 返回 (plan_status, closed_step_info)
   ↓
   Agent 使用 closed_step_info 更新 EventPublisher：
   - plan_id: 从 plan 获取
   - step_id: 使用 closed_step_info["step_id"]（刚关闭的步骤）
   - step_index: 使用 closed_step_info["step_index"]（刚关闭的步骤）
   - step_status: 使用 closed_step_info["step_status"]（刚关闭的步骤状态）
   ↓
   EventPublisher.publish() 发布事件：
   - 使用 EventPublisher 中存储的 plan_info
   - 每个事件都携带正确的 step_id、step_index、step_status
   ```

2. **关键设计点**：
   - **使用刚关闭的步骤信息**：事件发布时使用刚关闭的步骤信息，而不是新步骤的信息
   - **EventPublisher 内部维护状态**：`EventPublisher` 内部维护 `plan_id`、`step_id`、`step_index`、`step_status` 属性
   - **自动同步**：每次 `publish()` 时，从这些属性读取并写入 `EventData`，确保事件携带正确的信息

3. **每个 publish 如何知道自己的状态和 ID**：
   - `EventPublisher` 在初始化时或通过 `update_plan_info()` 更新这些属性
   - 每次 `publish()` 时，从 `self.plan_id`、`self.step_id`、`self.step_index`、`self.step_status` 读取
   - 这些值会被写入到 `EventData` 中，随事件一起发布
   - 通过 `update_plan_info()` 更新这些属性，确保后续事件使用最新信息

**使用示例**：

```python
# 完成步骤（会自动同步状态并发布事件）
plan_status = self.close_step(
    message="步骤完成",
    status=PlanStepStatus.COMPLETED
)

# 此时 EventPublisher 中的 plan_info 已经更新为刚关闭的步骤信息
# 后续的 publish() 调用会使用这些信息
self.publish(data="后续消息", event_type=EventTypeEnum.STR)
# 这个事件会携带刚关闭的步骤的 step_id、step_index、step_status
```

**注意事项**：
- ✅ **推荐**：使用 `self.close_step()` 而不是直接调用 `PlanManager.close_step()`
- ✅ **推荐**：在 `close_step()` 之后，EventPublisher 会自动更新，后续的 `publish()` 会使用正确的信息
- ❌ **不推荐**：在 `close_step()` 之后手动更新 EventPublisher，因为 `close_step()` 已经自动同步了

### 5. LLM 管理

#### 获取 LLM 实例

```python
# 获取默认 LLM
llm = self.get_default_llm(caller="my_operation")

# 获取指定模型的 LLM
llm = self.get_llm(
    model=LLMModel.QWEN_MAX,
    temperature=0.7,
    caller="my_operation",
)

# 替换默认 LLM
llm = self.get_llm(
    model=LLMModel.QWEN_MAX,
    replace_default=True,
)
```

#### 更新 LLM Caller

```python
# 更新默认 LLM 的 caller
self.update_llm_caller(caller="new_operation")
```

## 完整示例

### 示例1: 基础节点

```python
from fiuai_sdk_agent.agents import Agent, AgentType
from fiuai_sdk_agent.agents.types.plan_type import PlanStepStatus
from agents.state.common_state import FiuaiAgentTaskState
from langchain_core.runnables import RunnableConfig

class DataAgent(Agent):
    async def query_data_node(
        self, 
        state: FiuaiAgentTaskState, 
        config: RunnableConfig
    ) -> Dict[str, Any]:
        """数据查询节点"""
        # 1. 设置 state
        self.set_state(state)
        
        # 2. 加载 plan
        self.load_plan_from_state()
        
        # 3. 记录调试信息
        self.debug_step(message="开始查询数据")
        
        # 4. 执行业务逻辑
        result = await self.query_database()
        
        # 5. 发布进度消息
        self.publish(data=f"查询完成，共 {len(result)} 条记录")
        
        # 6. 完成步骤
        self.close_step(message="数据查询完成", status=PlanStepStatus.COMPLETED)
        
        # 7. 返回更新（自动包含 plan 和节点特定的字段）
        return self.get_state_updates(
            raw_data_set=result,
        )
```

### 示例2: 动态添加步骤

```python
async def process_node(self, state: FiuaiAgentTaskState, config: RunnableConfig):
    """处理节点，根据结果动态添加步骤"""
    self.set_state(state)
    self.load_plan_from_state()
    
    # 执行业务逻辑
    result = await self.process_data()
    
    # 根据结果决定是否需要额外的分析步骤
    if result.needs_analysis:
        # 动态添加新的分析步骤
        self.add_step(
            name="数据分析",
            description="对查询结果进行深入分析",
            step_id=gen_id(),
            domain_agent_type=DomainAgentType.DATA_AGENT,
        )
    
    # 完成当前步骤
    self.close_step(message="数据处理完成")
    
    # 返回更新
    return self.get_state_updates(
        result=result,
    )
```

### 示例3: 错误处理

```python
async def risky_node(self, state: FiuaiAgentTaskState, config: RunnableConfig):
    """可能失败的节点"""
    self.set_state(state)
    self.load_plan_from_state()
    
    try:
        # 执行业务逻辑
        result = await self.risky_operation()
        
        # 成功完成
        self.close_step(message="操作成功", status=PlanStepStatus.COMPLETED)
        
        return self.get_state_updates(result=result)
        
    except Exception as e:
        # 标记步骤失败
        self.fail_step(message=f"操作失败: {str(e)}")
        
        # 返回更新（plan 状态会更新为 FAILED 或继续执行）
        return self.get_state_updates(error=str(e))
```

## 最佳实践

### 1. State 管理

- ✅ **推荐**: 在节点开始时调用 `self.set_state(state)`
- ✅ **推荐**: 使用无参数版本的 `load_plan_from_state()` 和 `sync_plan_to_state()`
- ❌ **不推荐**: 在节点中直接使用传入的 `state` 参数，而不设置 `self.state`

### 2. Plan 和 Step 管理

- ✅ **推荐**: 使用 `self.close_step()` 而不是直接调用 `PlanManager.close_step()`
- ✅ **推荐**: 使用 `self.finish_step()` 和 `self.fail_step()` 简化代码
- ✅ **推荐**: 在步骤执行过程中使用 `self.debug_step()` 记录调试信息
- ❌ **不推荐**: 直接操作 `self.plan`，应该通过 Agent 的方法

### 3. 状态更新

- ✅ **推荐**: 使用 `self.get_state_updates()` 统一返回更新
- ✅ **推荐**: 在 `get_state_updates()` 中附加节点特定的字段
- ❌ **不推荐**: 手动构建返回字典，可能遗漏 plan 或 chat_history

### 4. 错误处理

- ✅ **推荐**: 使用 `self.fail_step()` 标记步骤失败
- ✅ **推荐**: 根据 `failed_on_step_fail` 配置决定是否继续执行
- ❌ **不推荐**: 直接修改 plan 状态，应该通过 Agent 的方法

## 类型要求

### State 类型

- `state` 必须是 `BasicStateInfo` 或其子类
- 自定义 state 类需要继承 `BasicStateInfo`:

```python
from fiuai_sdk_agent.agents.types.state_type import BasicStateInfo

class MyCustomState(BasicStateInfo):
    """自定义状态"""
    custom_field: Optional[str] = None
```

### Plan 类型

- `plan` 必须是 `BasePlan` 类型
- 步骤状态必须使用 `PlanStepStatus` 枚举
- 计划状态必须使用 `PlanStatus` 枚举

## 注意事项

1. **State 类型校验**: `set_state()` 会自动校验类型，不符合要求会抛出异常
2. **PlanManager 初始化**: 会自动初始化，无需手动创建
3. **事件发布顺序**: `close_step()` 会先更新 plan 状态，再更新 EventPublisher（使用刚关闭的步骤信息），最后发送消息
4. **动态添加步骤**: 支持在计划执行过程中动态添加步骤，会自动更新 `total_step_count`
5. **chat_history 增量**: 子类需要实现 `_get_chat_history_updates()` 方法才能返回 chat_history
6. **close_step 的状态同步**: `close_step()` 会自动同步状态，事件发布时使用刚关闭的步骤信息，而不是新步骤的信息
7. **EventPublisher 的状态维护**: `EventPublisher` 内部维护 `plan_id`、`step_id`、`step_index`、`step_status`，每次 `publish()` 时从这些属性读取

## 架构设计

### 职责划分

#### Agent 基类
- **协调者角色**: 协调 PlanManager、EventPublisher、ContextManager 等组件
- **统一接口**: 为子类提供统一的管理接口
- **生命周期管理**: 管理 state、plan、event 的统一生命周期

#### PlanManager
- **业务逻辑**: 只负责 Plan/Step 的业务逻辑
- **状态机驱动**: 所有状态转换都通过状态机校验
- **纯业务逻辑**: 不涉及事件发布、数据库等外部依赖

#### EventPublisher
- **事件发布**: 负责将事件发布到事件服务器
- **计划信息同步**: 自动同步 plan/step 信息到事件中

### 数据流

```
LangGraph State → Agent.set_state() → self.state
                                    ↓
                            load_plan_from_state()
                                    ↓
                            self.plan (同步到 Agent)
                                    ↓
                            业务逻辑处理
                                    ↓
                            close_step() / add_step()
                                    ↓
                            PlanManager (业务逻辑)
                                    ↓
                            EventPublisher (事件发布)
                                    ↓
                            get_state_updates()
                                    ↓
                            LangGraph State (返回更新)
```

## 常见问题

### Q1: 为什么需要先调用 set_state()？

A: 确保 `self.state` 和传入的 `state` 保持一致，这样后续使用无参数版本的方法时，会自动使用 `self.state`，避免状态不一致的问题。

### Q2: sync_plan_to_state() 和 get_state_updates() 有什么区别？

A: 
- `sync_plan_to_state()`: 只返回 plan 相关的更新（plan、plan_id）
- `get_state_updates()`: 返回完整的更新，包括 plan、chat_history 和节点附加的字段

推荐使用 `get_state_updates()`，它是统一的方法。

### Q3: 可以直接使用 PlanManager 的方法吗？

A: 不推荐。应该通过 Agent 的方法（如 `close_step()`），因为 Agent 会协调 PlanManager 和 EventPublisher，确保状态和事件的一致性。

### Q4: 动态添加的步骤什么时候执行？

A: 动态添加的步骤会追加到步骤列表末尾。如果当前步骤完成后，会自动执行新添加的步骤（如果存在）。

### Q5: chat_history 为什么只返回增量？

A: 为了性能考虑。如果每次都返回完整的 chat_history，数据量会很大。只返回增量可以减少数据传输量。但实际实现中，为了简化，返回的是完整的列表（LangGraph 需要完整列表来更新 state）。

### Q6: close_step() 中事件发布时，step_id 和 step_status 是如何获取的？

A: `close_step()` 实现了完整的状态同步机制：

1. **保存刚关闭的步骤信息**：在关闭步骤之前，保存当前步骤的 `step_id`、`step_index` 和状态
2. **关闭步骤并可能启动下一步**：调用 `PlanManager.close_step()` 关闭当前步骤，如果成功则启动下一步（此时 `plan.current_step_index` 和 `plan.current_step_id` 会更新为新步骤的值）
3. **使用刚关闭的步骤信息更新 EventPublisher**：使用保存的刚关闭步骤信息（而不是新步骤的信息）更新 `EventPublisher` 的 `plan_info`
4. **发布事件**：发布步骤关闭消息，事件中携带的是刚关闭的步骤信息

这样设计的原因：
- 事件应该反映"刚关闭的步骤"的状态，而不是"新启动的步骤"的状态
- 确保事件中的 `step_status` 是刚关闭步骤的状态（COMPLETED/FAILED/SKIPPED），而不是计划状态（RUNNING/COMPLETED/FAILED）

### Q7: 每个 publish() 如何知道自己的 step_id 和 step_status？

A: `EventPublisher` 内部维护了 `plan_id`、`step_id`、`step_index`、`step_status` 属性：

1. **初始化时设置**：在创建 `EventPublisher` 时可以传入初始值
2. **通过 update_plan_info() 更新**：调用 `update_plan_info()` 可以更新这些属性
3. **自动同步**：`close_step()` 等方法会自动调用 `update_plan_info()` 同步最新状态
4. **publish() 时读取**：每次 `publish()` 时，从这些属性读取并写入 `EventData`，随事件一起发布

因此，每个 `publish()` 调用都会使用 `EventPublisher` 中当前存储的 `plan_info`，确保事件携带正确的信息。

## 相关文档

- [PlanManager 使用文档](./plan/manager.py) - PlanManager 的详细说明
- [Plan 类型定义](./types/plan_type.py) - Plan 和 Step 的类型定义
- [State 类型定义](./types/state_type.py) - State 的类型定义

