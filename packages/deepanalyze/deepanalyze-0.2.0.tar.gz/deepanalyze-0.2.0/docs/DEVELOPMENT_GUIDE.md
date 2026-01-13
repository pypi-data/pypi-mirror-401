# Jupyter-DeepAnalyze 开发文档（代码导读 + 架构说明）

本文面向“要快速上手改代码”的开发者：按目录/模块解释本项目做什么、怎么跑通一条链路、以及常见改动应该改哪里。

> 备注：本仓库在 Windows 上开发时，文件夹名 `DeepAnalyze/` 与 `deepanalyze/` 在磁盘上可能显示为不同大小写，但在 Git 与 Python 包层面以 `deepanalyze/` 为准（Windows 默认大小写不敏感）。

## 1. 项目要解决的问题（1 分钟理解）

DeepAnalyze 是一个 **JupyterLab 前端扩展 + Jupyter Server 后端扩展** 的组合，用于把“大模型推理/代码/答案”以 Notebook 的方式落地：

- 用户在 JupyterLab 里打开 DeepAnalyze 工作区
- 通过右侧 Chat 面板提问
- 后端调用 vLLM（OpenAI-Compatible 接口）生成带标签的结果（`<Analyze>/<Understand>/<Code>/<Answer>`）
- 后端把结果解析为一组 `frontend_ops`（“前端应该如何插入/更新/运行 notebook cell”）
- 前端执行 `frontend_ops`，把内容写入：
  - `scratch.ipynb`：过程（分析/理解/代码）与可执行代码
  - `model-output.ipynb`：最终答案展示
- 如果模型只给了 `<Code>` 没给 `<Answer>`，前端会执行代码并把输出回传，后端再继续生成，直到有 `<Answer>`

核心思想：**Notebook 的写入/执行由前端直接操作 NotebookPanel 完成**，后端只做“编排 + 协议 + LLM 调用”，这样 UI 实时性最好、状态也最一致。

## 2. 运行时组件与数据流

### 2.1 组件

- **JupyterLab（前端）**
  - 插件入口：`src/index.ts`
  - 主要逻辑：`src/deepanalyze/open.ts`（打开工作区、执行 ops、回环）
  - UI：`src/deepanalyze/chatPanel.ts`
- **Jupyter Server Extension（后端）**
  - 路由注册：`deepanalyze/__init__.py`
  - HTTP Handlers：`deepanalyze/handlers.py`
  - 编排器：`deepanalyze/agent_orchestrator.py`
  - vLLM 客户端：`deepanalyze/agent_vllm_client.py`
- **vLLM（或任何 OpenAI-Compatible 推理服务）**
  - 主要接口：`POST /v1/chat/completions`（支持 stream 与非 stream）

### 2.2 一条“提问 -> 写入 Notebook -> 回环 -> 出答案”的链路

1. 用户打开 DeepAnalyze（Launcher 里点 `DeepAnalyze`）
2. 前端创建/打开当前工作区的 `model-output.ipynb` 与 `scratch.ipynb`
3. 用户在 Chat 面板输入问题
4. 前端调用后端：
   - 非流式：`POST /deepanalyze/chat`
   - 流式：`POST /deepanalyze/chat/stream`（SSE）
5. 后端返回：
   - `raw`：模型原始文本（含 `<Analyze>...</Analyze>` 等）
   - `frontend_ops`：一组“如何写 notebook”的指令
   - `await_feedback`：是否需要执行回环（通常：有 `<Code>` 但没有 `<Answer>`）
6. 前端执行 `frontend_ops`：
   - 写 cell / 更新 cell
   - 需要时执行 code cell 并收集 stdout/stderr/traceback
7. 若 `await_feedback=true`：
   - 前端把执行输出与必要的上下文回传到后端
   - 后端将其作为 `role=execute` 写入会话上下文后再次调用 vLLM
   - 返回下一轮 `frontend_ops`，直到产出 `<Answer>`

## 3. 仓库目录结构（按“改动入口”理解）

### 3.1 前端（TypeScript / JupyterLab 插件）

`src/` 是核心源码：

- `src/index.ts`
  - JupyterLab 插件入口：注册命令 `deepanalyze:open` 与 Launcher 按钮
- `src/deepanalyze/open.ts`
  - “前端编排器”：打开工作区、创建/打开 notebook、执行 `frontend_ops`、回环、以及 scratch 的流式占位写入
- `src/deepanalyze/chatPanel.ts`
  - Chat UI：消息历史、发送/继续/中止、流式增量展示、trace（可定位到 cell）
- `src/deepanalyze/api.ts`
  - 与后端通信：`/deepanalyze/chat*`、`/deepanalyze/agent/feedback*`、`/deepanalyze/cell/rewrite*`、`/deepanalyze/frontend/log`
  - SSE（`text/event-stream`）解析：按 `\n\n` 分帧，解析 `data: {...}` JSON
- `src/deepanalyze/settings.ts`
  - localStorage 设置：`workspacesRoot`、`maxAutoFeedbackTurns` 等
- `src/deepanalyze/storage.ts`
  - localStorage key 统一管理；key 会带 baseUrl scope（避免多站点串数据）
- `src/deepanalyze/workspace.ts`
  - 基于 Contents API 的目录/工作区创建与枚举（更偏“纯文件系统”操作）
- `src/deepanalyze/scratchCellRewrite.ts`
  - scratch 单元格右键菜单“使用大模型编辑”：对单元格进行指令式改写（支持流式写回）

`style/` 是 CSS（UI 样式）。

### 3.2 后端（Python / Jupyter Server Extension）

`deepanalyze/` 是后端包（Jupyter Server Extension）：

- `deepanalyze/__init__.py`
  - Server extension 入口：注册所有 HTTP 路由
- `deepanalyze/handlers.py`
  - HTTP API 的 Tornado handlers：
    - `POST /deepanalyze/chat`
    - `POST /deepanalyze/chat/stream`（SSE）
    - `POST /deepanalyze/agent/feedback`
    - `POST /deepanalyze/agent/feedback/stream`（SSE）
    - `POST /deepanalyze/cell/rewrite`
    - `POST /deepanalyze/cell/rewrite/stream`（SSE）
    - `POST /deepanalyze/frontend/log`
- `deepanalyze/agent_orchestrator.py`
  - **后端编排主流程**：构造 prompt/messages -> 调用 LLM -> 解析标签 -> 生成 `frontend_ops` -> 会话管理/回环
- `deepanalyze/agent_vllm_client.py`
  - vLLM OpenAI-compatible 客户端（stream/非 stream）
  - 兼容与兜底：流式空内容、上下文长度报错自动降 token 等
- `deepanalyze/agent_llm_gateway.py`
  - LLM 网关（中间层）：目前仅透传 vLLM，预留多后端接入点
- `deepanalyze/agent_tag_parser.py`
  - `<Analyze>/<Understand>/<Code>/<Answer>` 解析与提取（含 `<Code>` 围栏提取）
- `deepanalyze/agent_frontend_ops.py`
  - 将标签段落映射为 `frontend_ops`（插入 markdown/code cell 等）
- `deepanalyze/notebook_tools.py`
  - “工具模式”：聊天框发送 JSON op（例如列工作区、下发 create_notebook 等）
  - 方案 A 下这些 op 也会转成 `frontend_ops` 交给前端执行
- `deepanalyze/agent_session_store.py`
  - in-memory 会话存储（session_id -> messages/meta），带 TTL 与 max_sessions
- `deepanalyze/agent_settings.py`
  - 环境变量配置（vLLM baseUrl、模型名、stream 开关、日志目录等）
- `deepanalyze/agent_logging.py`
  - RotatingFileHandler 日志初始化（默认写 `DeepAnalyze/logs/deepanalyze.log`）
- `deepanalyze/prompts/*`
  - system prompt 模板与索引（`index.json`）

### 3.3 文档与进展

- `docs/ARCHITECTURE.md`：现有架构说明（偏“系统视角”）
- `docs/PROGRESS.md`：进展记录（偏“时间线”）
- `docs/DEVELOPMENT_GUIDE.md`：本文（偏“开发者入口 + 代码导读”）

## 4. 核心协议：标签、ops、SSE、会话

### 4.1 模型输出标签（tag 协议）

后端假设模型输出包含以下标签段（顺序可能变化，可能缺失）：

- `<Analyze>...</Analyze>`：过程推理（通常写 scratch）
- `<Understand>...</Understand>`：问题与数据理解（写 scratch）
- `<Code>...</Code>`：可执行代码（写 scratch code cell，可触发执行）
- `<Answer>...</Answer>`：最终回答（写 model-output；也可写 scratch 便于追踪）

解析实现：`deepanalyze/agent_tag_parser.py`

### 4.2 `frontend_ops`（前端操作指令）

后端不会直接写 ipynb 文件，而是返回一组 JSON 指令，让前端在浏览器中直接操作 `NotebookPanel`：

常见字段：

- `id`：op id（用于关联 trace 与 tool_results）
- `op`：操作类型（如 `insert_cell`、`update_cell`、`run_cell`）
- `path`：目标 notebook（Jupyter Contents 路径）
- `index`：目标 cell index（部分 op 需要）
- `cell_type`：`markdown|code|raw`（`insert_cell`）
- `source`：cell 内容（`insert_cell|update_cell`）

为了让“执行输出回传后能精确覆写原段落”，还会带一组 meta：

- `turn_id`：一次 LLM 输出的 turn id（后端生成）
- `segment_tag`：`Analyze|Understand|Code|Answer`
- `segment_ordinal`：该 turn 内第几个 tag 段（从 0 计数）
- `segment_kind`：前端写入的 cell 类型语义（如 `markdown|code|header|output_markdown`）

生成位置：`deepanalyze/agent_frontend_ops.py`

执行位置：`src/deepanalyze/open.ts` 内部的 `execOpsStream(...)`

### 4.3 SSE 流式事件

前后端约定使用 `text/event-stream`，每个事件为一段以空行分隔的帧：

```
data: {"type":"start"}

data: {"type":"delta","delta":"..."}

data: {"type":"final","response":{...}}

```

前端解析实现：`src/deepanalyze/api.ts`（按 `\n\n` 分帧，提取 `data:` 行并 JSON.parse）

### 4.4 session_id 与 context

- `session_id`：前端保存在 localStorage，用于后端会话关联（同一 session 共享 messages/history）
- `context`：前端每次请求都会带上当前工作区与两个 notebook 路径：
  - `workspaceDir`
  - `outputPath`
  - `scratchPath`

前端实现：`src/deepanalyze/storage.ts`、`src/deepanalyze/api.ts`

后端会话存储：`deepanalyze/agent_session_store.py`

## 5. 前端关键实现：你最常改的地方

### 5.1 插件入口：`src/index.ts`

- 注册命令 `deepanalyze:open`
- 点击 Launcher 触发 `openDeepAnalyze(...)`
- `app.restored` 后调用 `restoreDeepAnalyzeIfNeeded(...)`（用于刷新页面后的恢复）

### 5.2 “前端编排器”：`src/deepanalyze/open.ts`

这是前端最核心的文件，职责集中在三件事：

1. **初始化/打开工作区**
   - 选择或创建 workspace 目录
   - 确保 `model-output.ipynb` 与 `scratch.ipynb` 存在并打开
   - 更新 localStorage：activeWorkspaceDir/activeOutputPath/activeScratchPath/sessionId
2. **执行 `frontend_ops`**
   - `insert_cell/update_cell/delete_cell/run_cell/...` 都在这里落地到 NotebookPanel
   - 同时生成 `tool_results`（执行输出、trace、以及修正后的 index 等）
3. **回环（feedback loop）**
   - 当后端返回 `await_feedback=true`，前端执行 code cell，收集输出
   - 调用 `/deepanalyze/agent/feedback*` 把输出回传，拿到下一轮 ops

该文件里还有一个对用户体验非常重要的机制：

- **scratch 的流式占位写入**：在模型生成时，往 scratch 末尾插入一个 raw cell，把 SSE delta 拼进去，让用户在 notebook 里“看见正在生成”。

### 5.3 Chat UI：`src/deepanalyze/chatPanel.ts`

- 维护消息历史（user/assistant/system）
- 优先走流式 `streamChatMessage`，失败后回退非流式 `sendChatMessage`
- `onModelStream`：把流式事件回调给 `open.ts`，用于写 scratch 占位、更新状态（generating/waiting/done）
- `onToolResult`：把后端 `data`（含 ops/await_feedback 等）交给 `open.ts` 执行

### 5.4 单元格改写：`src/deepanalyze/scratchCellRewrite.ts`

- 在 scratch 的 cell 右键菜单添加“使用大模型编辑”
- 调用后端 `/deepanalyze/cell/rewrite/stream`（SSE）增量写回 cell source
- 若流式失败则回退到 `/deepanalyze/cell/rewrite`

## 6. 后端关键实现：你最常改的地方

### 6.1 路由注册：`deepanalyze/__init__.py`

Jupyter Server Extension 的入口，在 `_load_jupyter_server_extension` 里把 APIHandler 挂到指定路径。

### 6.2 HTTP API：`deepanalyze/handlers.py`

主要关注点：

- Chat / Feedback 的请求体格式与响应体格式（是否流式）
- 与 `DeepAnalyzeNotebookTool` 的交互（JSON op）
- 调用编排器：
  - `handle_user_message(...)`
  - `handle_feedback(...)`

### 6.3 编排器：`deepanalyze/agent_orchestrator.py`

这是后端的“大脑”，主要做：

- 会话管理：把 user/assistant/execute messages 放进 session
- prompt 构造：
  - system prompt：`deepanalyze/agent_prompt.py`
  - user prompt：`deepanalyze/agent_prompt_builder.py`（含 `# Data` 文件列表）
- LLM 调用：`deepanalyze/agent_llm_gateway.py`
- 标签解析：`deepanalyze/agent_tag_parser.py`
- ops 生成：`deepanalyze/agent_frontend_ops.py`
- 回环：把 tool_results/execute 输出写回上下文后继续生成

## 7. 常见需求：改哪里最省时间

### 7.1 增加一种新的 `frontend_ops`

1. 定义后端如何产出该 op：
   - 通常在 `deepanalyze/agent_frontend_ops.py` 里从标签段映射
   - 或在 `deepanalyze/notebook_tools.py` 里从 JSON op 透传
2. 在前端实现该 op 的执行：
   - `src/deepanalyze/open.ts` 的 `execOpsStream(...)` 分支里添加处理
3. 若该 op 需要“回传结果给后端”，在前端生成 tool_results，并在后端 `handle_feedback(...)` 里消费

### 7.2 调整标签协议 / 增加新标签

1. `deepanalyze/agent_tag_parser.py`：修改正则/解析逻辑
2. `deepanalyze/agent_frontend_ops.py`：决定写到 scratch/output 的方式
3. `src/deepanalyze/chatPanel.ts`：如需在 Chat UI 中做特殊渲染/提示

### 7.3 调整 system prompt

- 默认模板：`deepanalyze/prompts/deepanalyze_8b.md`
- 索引：`deepanalyze/prompts/index.json`
- 选择方式：
  - `DEEPANALYZE_SYSTEM_PROMPT_PATH` 指定文件
  - 或 `DEEPANALYZE_SYSTEM_PROMPT_NAME` 从 index 里选

实现：`deepanalyze/agent_prompt.py`

### 7.4 排查“流式卡住/空输出”

优先看日志：`DeepAnalyze/logs/deepanalyze.log`

- 前端流式失败会调用：`POST /deepanalyze/frontend/log`（后端会把 payload 记录到日志）
- vLLM 流式偶发空输出时，后端会回退非流式再请求一次（相关关键字在 `agent_vllm_client.py` 中）

## 8. 如何验证你的改动（不在本文中自动执行）

前端（TypeScript）：

1. `jlpm`
2. `jlpm build`（或开发模式 `jlpm watch`）

后端（Python）：

1. `pip install -e .`
2. `jupyter labextension develop . --overwrite`
3. 启动/重启 `jupyter lab`

功能验证建议：

- 打开 JupyterLab Launcher -> 点击 `DeepAnalyze`
- 输入一条问题，观察：
  - scratch 是否出现流式占位 cell（并随 token 增量更新）
  - model-output 是否写入 `<Answer>` 内容
- 若出现 `<Code>` 但未给 `<Answer>`，是否能自动执行并进入回环直到出答案
- 在 scratch 单元格右键，使用“使用大模型编辑”验证单元格改写接口
