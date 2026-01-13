# 通用大模型接入与模型选择器（开发说明）

本文档描述本项目在 **Chat 对话** 场景下接入通用大模型 API 的实现方式：前端“模型下拉栏 + API Key 管理”、后端“模型注册表 + Key 校验/存储 + 动态路由”，以及如何扩展新增模型。

## 目标与范围

- 在 Chat 对话框左下角新增“模型下拉栏”，默认 `DeepAnalyze 8B`，用户修改后会记住选择。
- 支持选择不同模型（如 `DeepSeek`、`OpenAI`）。
- API Key 由用户在前端设置：
  - 已设置且校验通过：模型名旁显示绿点，点击可直接选中。
  - 未设置或校验失败：显示红点，点击可设置/更新 API Key。
- 后端根据 `model_id`：
  - 选择不同 base_url/模型名，向对应后端发请求；
  - 选择不同 system prompt 模板（见 `deepanalyze/prompts/`）。

本次改动 **只覆盖 Chat/Feedback 链路**（`/deepanalyze/chat*`、`/deepanalyze/agent/feedback*`）。单元格“改写”接口仍默认走原本的 vLLM。

## 前端改动（JupyterLab Extension）

### UI：Chat 面板左下角模型下拉栏

文件：

- `src/deepanalyze/chatPanel.ts`
- `style/base.css`

要点：

- 在 `.deepanalyze-chat-actions` 左侧加入 `.deepanalyze-chat-model-selector`，用 `margin-right:auto` 把它推到左侧。
- 下拉菜单为自定义 DOM（不是原生 `<select>`），因此可以在每一项旁显示状态点并绑定点击行为：
  - 绿点：直接选中模型
  - 红点：弹出对话框让用户输入 API Key
- 用户选择写入 `localStorage`：`deepanalyze.modelId@<baseUrlScope>`

### 请求参数：携带 `model_id`

文件：

- `src/deepanalyze/api.ts`
- `src/deepanalyze/open.ts`

改动：

- `sendChatMessage/streamChatMessage`：请求体新增 `model_id`
- `sendAgentFeedback/streamAgentFeedback`：请求体新增 `model_id`（保证回环续写走同一模型）

### 模型列表与 Key 管理 API

文件：

- `src/deepanalyze/api.ts`

新增：

- `GET /deepanalyze/models` → `fetchModels()`
- `POST /deepanalyze/models/key` → `setModelApiKey(model_id, api_key)`

## 后端改动（Jupyter Server Extension）

### 模型注册表（base_url / prompt 对应关系）

文件：

- `deepanalyze/models/index.json`
- `deepanalyze/model_registry.py`

`deepanalyze/models/index.json` 用于描述模型条目：

- `id`：前端/后端交互的 `model_id`
- `label`：前端展示名
- `backend`：`vllm` 或 `openai_compat`
- `base_url`：OpenAI-Compatible 的 base url（建议以 `/v1` 结尾）
- `model`：具体模型名（如 `deepseek-chat`、`gpt-4o-mini`）
- `prompt_name`：system prompt 名称（对应 `deepanalyze/prompts/index.json`）
- `requires_api_key`：是否需要 key

说明：

- 对 `backend=vllm` 的条目，如果未填写 `base_url/model`，会默认读取环境变量配置（保持原本 vLLM 部署方式不变）。

### 通用 OpenAI-Compatible 客户端

文件：

- `deepanalyze/agent_openai_compat_client.py`

实现：

- `POST {base_url}/chat/completions`（流式/非流式）
- `GET {base_url}/models`（用于 API Key 快速校验）

### API Key 存储与校验

文件：

- `deepanalyze/agent_secret_store.py`

行为：

- Key 存储位置：`~/.deepanalyze/api_keys.json`
- 写入时尝试设置文件权限 `0600`
- 用户保存 key 后，后端会用 `GET /models` 做一次校验，记录 `ok/invalid/missing` 状态与错误信息

### Chat/Feedback 动态路由（按 `model_id` 选择后端与 prompt）

文件：

- `deepanalyze/handlers.py`
- `deepanalyze/agent_llm_gateway.py`

关键点：

1. 前端请求体带 `model_id`。
2. 后端通过注册表把 `model_id` 映射为：`backend/base_url/model/prompt_name`。
3. 后端用 `session_key = "{session_id}::model={model_id}"` 隔离不同模型的会话：
   - 因为 system prompt 只在会话初始化时注入一次，隔离能避免用户中途切换模型导致上下文混用。
4. `agent_llm_gateway.py` 根据 `settings.llm_backend` 调用：
   - `vllm` → 原 vLLM 客户端
   - `openai_compat` → 新的 OpenAI-Compatible 客户端（并从 secret store 取 key）

### 新增后端接口

文件：

- `deepanalyze/__init__.py`
- `deepanalyze/handlers.py`

新增路由：

- `GET /deepanalyze/models` → `ModelsHandler`
- `POST /deepanalyze/models/key` → `ModelApiKeyHandler`

## Prompt 模板（通用大模型）

文件：

- `deepanalyze/prompts/universal_llm.md`
- `deepanalyze/prompts/index.json`

该 prompt 约束模型输出 `<Analyze>/<Understand>/<Code>/<Answer>` 结构，并解释：

- `# Instruction`：用户任务指令
- `# Data`：工作区上下文/文件摘要
- 系统的回环流程：先输出 `<Code>`，执行结果回传后再补 `<Answer>`

## 如何新增一个新模型（示例）

1. 在 `deepanalyze/models/index.json` 增加一条：
   - `backend=openai_compat`
   - 填 `base_url/model`
   - `prompt_name` 选择 `universal_llm` 或新增 prompt
2. 若新增 prompt：
   - 在 `deepanalyze/prompts/` 新增 `*.md`
   - 并在 `deepanalyze/prompts/index.json` 注册
3. 重启 Jupyter Server（让 server extension 重新加载），打开 Chat 面板即可在下拉栏看到新模型。

## 验证方式（手动）

1. 启动/进入 JupyterLab，打开 DeepAnalyze Chat 面板。
2. 左下角下拉栏检查：
   - `DeepAnalyze 8B` 默认选中；
   - `DeepSeek/OpenAI` 若未配置 key 显示红点。
3. 点击红点，输入 API Key 并保存：
   - 若校验通过，点变绿；
   - 校验失败仍为红点，并弹出错误提示。
4. 选中对应模型后发送一句简单消息（如“请概述当前工作区有哪些文件”）：
   - 后端应按模型选择路由请求；
   - 若未设置 key，会提示缺少 API Key。

