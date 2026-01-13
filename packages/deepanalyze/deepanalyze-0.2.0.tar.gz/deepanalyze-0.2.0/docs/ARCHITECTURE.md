# Jupyter-DeepAnalyze 系统架构与代码导读

本文用于说明当前 `Jupyter-DeepAnalyze` 项目的前后端架构、关键链路、协议约定与主要代码位置，方便后续开发与排障。

补充：更偏“开发者上手”的代码导读请看 `docs/DEVELOPMENT_GUIDE.md`。

## 1. 总体架构（运行时组件）

运行时主要由 5 个组件构成：

1. **JupyterHub（可选）**
   - 负责多用户认证与单用户服务（Single-User Jupyter Server）的拉起。
   - 本仓库的示例配置在 `develop/jupyterhub_config.py`。
2. **Single-User Jupyter Server**
   - 承载 Notebook、Contents API、Kernel 管理、以及本项目的后端 server extension（HTTP API）。
3. **JupyterLab 前端扩展（TypeScript）**
   - 提供 DeepAnalyze 工作区布局、对话 UI、以及对 NotebookPanel 的直接操控能力。
4. **DeepAnalyze 后端扩展（Python / Jupyter Server Extension）**
   - 提供 `/deepanalyze/*` API：对话、反馈回环、前端日志上报等。
   - 负责会话管理、调用 vLLM、解析模型标签并规划前端操作指令。
5. **vLLM（OpenAI-Compatible Server）**
   - 以 OpenAI 兼容接口提供推理服务，主要使用 `POST /v1/chat/completions`。

## 2. 代码目录结构（重点）

- `src/`：JupyterLab 前端扩展源码（TypeScript）
  - `src/index.ts`：插件入口（注册 launcher/命令）
  - `src/deepanalyze/open.ts`：打开工作区、Notebook 操作执行器、回环与流式占位
  - `src/deepanalyze/chatPanel.ts`：聊天 UI 组件
  - `src/deepanalyze/api.ts`：调用后端 API（含 SSE 流式消费）
  - `src/deepanalyze/storage.ts`：localStorage key 管理
- `deepanalyze/`：Python 后端扩展（Jupyter Server Extension）
  - `deepanalyze/__init__.py`：注册 handler 路由
  - `deepanalyze/handlers.py`：HTTP API（chat/feedback/stream/log）
  - `deepanalyze/agent_orchestrator.py`：编排主流程（消息构造、调用 LLM、解析、产出前端 ops、回环）
  - `deepanalyze/agent_vllm_client.py`：vLLM OpenAI-Compatible 客户端（含流式 SSE 解析与兜底重试）
  - `deepanalyze/agent_tag_parser.py`：解析 `<Analyze>/<Understand>/<Code>/<Answer>` 标签段
  - `deepanalyze/agent_frontend_ops.py`：把标签段转换成 `frontend_ops`（Notebook 操作指令）
  - `deepanalyze/notebook_tools.py`：工具模式（JSON op）与工作区发现辅助
  - `deepanalyze/agent_session_store.py`：会话存储（session_id -> message history + meta）
  - `deepanalyze/agent_settings.py`：环境变量配置读取
  - `deepanalyze/agent_logging.py`：日志落盘（RotatingFileHandler）
- `DeepAnalyze/workspaces/`：工作区数据（运行时生成）
  - 每个 workspace 下通常包含：`scratch.ipynb`、`model-output.ipynb`、`history/*.md`、以及产物文件。
- `develop/`：开发环境/Hub 配置脚本
  - `develop/jupyterhub_config.py`：示例 Hub 配置（可注入 DeepAnalyze 相关 env）

## 3. 关键概念与约定

### 3.1 标签协议（模型输出格式）

后端假设模型输出使用以下 XML 风格标签组织内容（顺序可变，可能多段）：

- `<Analyze>...</Analyze>`：推理分析（一般写入 scratch）
- `<Understand>...</Understand>`：对问题/数据的理解（一般写入 scratch）
- `<Code>...</Code>`：可执行代码（写入 scratch 的 code cell，并可触发执行）
- `<Answer>...</Answer>`：最终回答（写入 model-output，并可写入 scratch）

解析位置：`deepanalyze/agent_tag_parser.py`

### 3.2 前端操作指令（frontend_ops）

后端不直接改 ipynb 文件，而是下发 `frontend_ops` 让前端直接操作 `NotebookPanel`，以获得更好的实时性。

典型 op（以 `op` 字段区分）：

- `create_notebook`：创建并可选打开 notebook
- `insert_cell`：插入 markdown/code/raw cell
- `update_cell`：更新指定 cell 的 source
- `delete_cell`：删除 cell
- `run_cell` / `run_last_cell`：执行 cell 并采集 outputs

执行位置：`src/deepanalyze/open.ts`（内部的 `execOpsStream`）

### 3.3 会话与回环（feedback loop）

- 前端发起对话后，后端返回：
  - `raw`：模型原始输出（带标签）
  - `frontend_ops`：写入 scratch/model-output 的 Notebook 操作
  - `await_feedback`：是否需要执行回环（通常存在 `<Code>` 但缺少 `<Answer>` 时为 true）
- 前端执行 `frontend_ops`（包括运行 code cell），采集输出与当前 notebook snapshot，再调用 `/deepanalyze/agent/feedback`（或流式版本）把执行结果回传，后端将其以 `role=execute` 追加到上下文后再次请求 vLLM，形成多轮迭代。

编排位置：`deepanalyze/agent_orchestrator.py`

## 4. 请求链路（从输入到写入 Notebook）

### 4.1 打开工作区与初始化

入口：`src/deepanalyze/open.ts` 的 `openDeepAnalyze(...)`（由 `src/index.ts` 注册命令触发）

典型动作：

- 创建/打开：
  - `model-output.ipynb`：模型最终回答展示
  - `scratch.ipynb`：模型过程内容与可执行代码
- 设置 localStorage 上下文：
  - `activeWorkspaceDir`
  - `activeOutputPath`
  - `activeScratchPath`
  - `sessionId`

### 4.2 Chat（非流式）

- 前端：`src/deepanalyze/api.ts#sendChatMessage`
- 后端：`deepanalyze/handlers.py#ChatHandler`（`POST /deepanalyze/chat`）

### 4.3 Chat（流式 SSE）

- 前端：`src/deepanalyze/api.ts#streamChatMessage`
- 后端：`deepanalyze/handlers.py#ChatStreamHandler`（`POST /deepanalyze/chat/stream`）
  - SSE event：
    - `{"type":"start"}`
    - `{"type":"delta","delta":"..."}`（增量 token）
    - `{"type":"final","response":{...}}`（最终 JSON，与非流式一致）

流式 vLLM 调用：`deepanalyze/agent_vllm_client.py#chat_completions_stream`

### 4.4 流式占位写入 scratch（前端）

为了让用户在 Notebook 中看到生成进度，前端会在 scratch 末尾插入一个 **raw cell** 作为流式占位，并在 SSE delta 到达时增量更新其内容。

- 实现位置：`src/deepanalyze/open.ts`（`startStreamingToScratch` / `appendStreamingToScratch` / `finalizeStreamingScratchCell`）
- 行为约定：
  - 生成中：显示 `[Streaming] 生成中…`
  - 若需要执行回环：显示 `[Streaming] 等待执行/回环…`
  - 生成结束：显示 `[Streaming] 完成`
  - 生成中锁定 cell（不可编辑/删除），结束后解锁

### 4.5 Feedback（执行回传）

当 `await_feedback=true` 时，前端执行 code cell 并将 stdout/stderr/异常 traceback 汇总为 execute 文本，回传给后端作为下一轮上下文。

- 前端：
  - `src/deepanalyze/api.ts#sendAgentFeedback`
  - `src/deepanalyze/api.ts#streamAgentFeedback`
- 后端：
  - `deepanalyze/handlers.py#FeedbackHandler`（`POST /deepanalyze/agent/feedback`）
  - `deepanalyze/handlers.py#FeedbackStreamHandler`（`POST /deepanalyze/agent/feedback/stream`）
- 上下文写入：
  - `deepanalyze/agent_orchestrator.py#_upsert_execute_message`（`role=execute`）

## 5. 配置与环境变量

配置读取：`deepanalyze/agent_settings.py`

常用环境变量（部分）：

- `DEEPANALYZE_VLLM_BASE_URL`：默认 `http://127.0.0.1:8000/v1`
- `DEEPANALYZE_VLLM_MODEL`：默认 `DeepAnalyze-8B`
- `DEEPANALYZE_VLLM_TIMEOUT_S`：默认 `120`
- `DEEPANALYZE_ENABLE_STREAM`：是否启用流式（当前默认：true）
- `DEEPANALYZE_VLLM_MAX_NEW_TOKENS`：默认 `8192`
- `DEEPANALYZE_LOG_DIR`：日志目录（默认 `DeepAnalyze/logs`）

如使用 JupyterHub，可在 `develop/jupyterhub_config.py` 通过 `c.Spawner.environment` 注入（示例中已包含 `DEEPANALYZE_ENABLE_STREAM`）。

## 6. 日志与排障

日志实现：`deepanalyze/agent_logging.py`（RotatingFileHandler）

- 默认日志文件：`${DEEPANALYZE_LOG_DIR}/deepanalyze.log`
- 常用排障关键词：
  - `chat_stream start/end/delta`
  - `feedback_stream start/end/delta`
  - `vllm stream done`
  - `vllm stream empty_content retry_non_stream`
  - `stream_chat_failed` / `stream_feedback_failed`（前端上报到 `/deepanalyze/frontend/log`）

## 7. 开发与验证建议（最小流程）

1. 前端构建：
   - 在仓库根目录执行：`jlpm build`
2. 后端（Python）安装：
   - `pip install -e .`
3. 让 JupyterLab 使用本地扩展：
   - `jupyter labextension develop . --overwrite`
4. 启动/重启 JupyterLab / JupyterHub 单用户服务
5. 在 JupyterLab 中点击 Launcher 的 `DeepAnalyze`，进入工作区后进行对话与回环验证
