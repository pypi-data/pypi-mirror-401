# FiuAI SDK Agent 项目设置说明

## 项目结构

`fiuai_sdk_agent/` 目录已改造为独立的 PyPI 项目，同时保持在本仓库中作为模块使用。

## 使用方式

### 1. 在本仓库中使用（作为本地模块）

```python
from fiuai_sdk_agent import Agent, AgentType, LLMManager
```

### 2. 作为 PyPI 包使用

```bash
pip install fiuai-sdk-agent
```

```python
from fiuai_sdk_agent import Agent, AgentType, LLMManager
```

## 依赖关系

### 已修复的外部依赖

1. ✅ **config.app_config**: 已移除，不再依赖仓库内的配置模块
2. ✅ **utils.ids.gen_id**: 改为使用 `fiuai_sdk_python.utils.ids.gen_id`
3. ✅ **utils.text.safe_str**: 改为使用标准库 `urllib.parse.quote_plus`
4. ✅ **utils.get_logger**: 使用 `fiuai_sdk_agent.utils.logger.get_logger`
5. ✅ **pkg.db**: 作为可选依赖，如果未安装则数据库日志功能会被禁用

### 外部依赖（允许使用）

- ✅ `fiuai-sdk-python`: 继续使用，这是外部 PyPI 包

### 依赖检查

所有对仓库内其他包的依赖（`config`, `pkg.db`, `utils`, `middleware`, `app`, `agents`）都已移除或改为可选依赖。

## 发布到 PyPI

### 构建包

```bash
cd fiuai_sdk_agent
python -m build
```

### 上传到 PyPI

```bash
twine upload dist/*
```

## 未来迁移

当项目成熟稳定后，可以将 `fiuai_sdk_agent/` 目录单独移到一个独立的工程仓库。

迁移步骤：
1. 创建新的 git 仓库
2. 将 `fiuai_sdk_agent/` 目录内容复制到新仓库
3. 更新本仓库中的导入，改为从 PyPI 安装
4. 在新仓库中继续开发和维护
