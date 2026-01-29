# PlanManager 使用指南

## 概述

`PlanManager` 是计划管理器，负责管理 Plan 和 Step 的生命周期，处理状态转换的业务逻辑。

## 设计理念

1. **单一职责**: PlanManager 只负责 Plan/Step 的业务逻辑，不涉及事件发布、上下文管理等
2. **状态机驱动**: 所有状态转换都通过 `PlanStateMachine` 进行校验，确保状态转换的合法性
3. **纯业务逻辑**: PlanManager 的方法都是纯业务逻辑，不涉及外部依赖（如事件发布、数据库等）

## 与 Agent 的关系

- Agent 通过 PlanManager 管理 Plan/Step 的状态
- Agent 负责协调 PlanManager 和 EventPublisher，确保状态和事件的一致性
- Agent 的方法（如 `close_step`）会先调用 PlanManager 的方法修改状态，然后同步到 EventPublisher

## 基本使用

### 创建 PlanManager

```python
from fiuai_sdk_agent.agents.plan.manager import PlanManager
from fiuai_sdk_agent.agents.types.plan_type import BasePlan

# 创建 PlanManager
plan_manager = PlanManager(plan=my_plan)

# 或者先创建，后设置 plan
plan_manager = PlanManager()
plan_manager.set_plan(my_plan)
```

### 获取计划信息

```python
# 检查是否有计划
if plan_manager.has_plan():
    plan_id = plan_manager.get_plan_id()
    step_id = plan_manager.get_current_step_id()
    step_index = plan_manager.get_current_step_index()
    step_status = plan_manager.get_current_step_status()
```

### 步骤管理

#### 关闭步骤

```python
from fiuai_sdk_agent.agents.types.plan_type import PlanStepStatus, PlanStatus

# 关闭当前步骤（返回计划状态和刚关闭的步骤信息）
plan_status, closed_step_info = plan_manager.close_step(
    message="步骤完成",
    status=PlanStepStatus.COMPLETED
)
# closed_step_info 包含: step_id, step_index, step_status

# 标记步骤失败
plan_status, closed_step_info = plan_manager.fail_step(message="步骤失败")

# 完成步骤（便捷方法）
plan_status, closed_step_info = plan_manager.finish_step(message="步骤完成")
```

#### 动态添加步骤

```python
# 在计划执行过程中动态添加步骤
plan_manager.add_step(
    name="新步骤",
    description="步骤描述",
    step_id=gen_id(),
    domain_agent_type=DomainAgentType.DATA_AGENT,
)
```

#### 添加步骤消息

```python
from fiuai_sdk_agent.agents.types.event_type import EventType

# 添加步骤消息（用于上下文和前端展示）
plan_manager.add_step_message(
    data="消息内容",
    event_type=EventType.CHUNK
)
```

#### 调试步骤

```python
# 记录调试信息（不关闭步骤）
plan_manager.debug_step(message="调试信息")
```

### 获取计划信息用于事件发布

```python
# 获取计划信息（用于 EventPublisher）
plan_info = plan_manager.update_event_plan_info()

# 或者指定部分信息
plan_info = plan_manager.update_event_plan_info(
    step_status=PlanStepStatus.COMPLETED.value
)
```

## 状态转换规则

### Plan 状态转换

```
NOT_STARTED → PENDING → RUNNING → COMPLETED/FAILED
     ↓           ↓
  RUNNING    FAILED
```

### Step 状态转换

```
TODO → RUNNING → COMPLETED/FAILED/SKIPPED
  ↓
SKIPPED
```

所有状态转换都通过 `PlanStateMachine` 进行校验，非法转换会抛出异常。

## 业务逻辑说明

### close_step() 的业务逻辑

1. 验证 message 不为空
2. 关闭当前步骤（通过 `BasePlan.close_current_step`）
3. 根据步骤状态决定后续操作：
   - 如果步骤失败且 `failed_on_step_fail=True`，则标记计划失败
   - 如果步骤成功，启动下一个步骤
   - 如果所有步骤完成，标记计划完成
4. 记录日志

### 动态添加步骤的支持

- 支持在计划执行过程中动态添加步骤
- 添加的步骤会自动更新 `total_step_count`
- `is_all_steps_completed()` 会检查所有步骤（包括动态添加的）是否都处于终态

## 使用示例

### 示例1: 基本步骤管理

```python
# 创建 PlanManager
plan_manager = PlanManager(plan=my_plan)

# 添加步骤消息
plan_manager.add_step_message(data="开始处理", event_type=EventType.CHUNK)

# 完成步骤
plan_status, closed_step_info = plan_manager.finish_step(message="处理完成")

# 检查计划状态
if plan_status == PlanStatus.COMPLETED:
    print("计划已完成")
```

### 示例2: 动态添加步骤

```python
# 在执行过程中动态添加步骤
if need_extra_analysis:
    plan_manager.add_step(
        name="数据分析",
        description="对结果进行深入分析",
        step_id=gen_id(),
    )

# 完成当前步骤（新添加的步骤会自动成为下一步）
plan_status, closed_step_info = plan_manager.finish_step(message="当前步骤完成")
```

### 示例3: 错误处理

```python
try:
    result = await risky_operation()
    plan_status, closed_step_info = plan_manager.finish_step(message="操作成功")
except Exception as e:
    # 标记步骤失败
    plan_status, closed_step_info = plan_manager.fail_step(message=f"操作失败: {str(e)}")
    
    # 根据配置决定是否继续执行
    if plan_status == PlanStatus.FAILED:
        print("计划已失败，停止执行")
    else:
        print("步骤失败，但计划继续执行")
```

## 注意事项

1. **纯业务逻辑**: PlanManager 不涉及事件发布，如果需要发布事件，应该通过 Agent 的方法
2. **状态机校验**: 所有状态转换都会进行校验，非法转换会抛出异常
3. **动态添加步骤**: 支持动态添加，但需要确保步骤顺序合理
4. **消息过滤**: `add_step_message()` 会跳过 PLAN 和 TASK 类型的事件，以及空数据

## 相关文档

- [Agent 基类使用指南](../README.md) - Agent 基类的详细说明
- [Plan 类型定义](../types/plan_type.py) - Plan 和 Step 的类型定义和状态机规则

