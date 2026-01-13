# PROGRESS（进展记录）

本文用于记录 `Jupyter-DeepAnalyze` 当前阶段的关键进展、已完成内容与待办事项，便于协作与排期。

## 变更记录

- 2026-01-11 16:09：自定义模型配置与 API Key 存储位置调整：默认从 `~/.deepanalyze/` 迁移为 Jupyter Server `root_dir/.deepanalyze/`（可用环境变量 `DEEPANALYZE_STORE_DIR` 覆盖）；读取时兼容旧路径回退（`deepanalyze/store_dir.py`、`deepanalyze/__init__.py`、`deepanalyze/agent_model_store.py`、`deepanalyze/agent_secret_store.py`）。
- 2026-01-11 15:45：修复打开内层可滚动块后外层聊天区无法继续向下滚动：在内层滚动到边界时将滚轮事件链式转发到外层 messages 滚动容器，避免滚动被“卡住”（`src/deepanalyze/chatPanel.ts`）。
- 2026-01-11 11:17：修复 chat 重进后历史块显示不全：在 finalize 时把流式 UI 的所有块内容汇总为可解析的标签文本并持久化；恢复时优先使用隐藏的 assistant_raw_updates 合并重建，确保显示 `Finished work` 与完整子下拉栏（`src/deepanalyze/chatPanel.ts`）。
- 2026-01-11 11:05：修复 chat 退出重进后历史记录下拉栏错乱：为“仅用于恢复的 assistant_raw_updates”增加隐藏标记并在恢复时折叠旧数据；同时持久化并恢复 trace 链式块定位（turnId+trace items）；优化滚动跟随逻辑，仅在滚轮位于底部时自动滚动；Answer 取消滚轴（`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-11 10:44：修复 chat 流式块边界串字符问题（移除“无活跃块时把前缀内容归入新块”的逻辑，避免上一个块尾部串到下一个块）；下拉标志从三角形改为“勾形 chevron”，并进一步压缩块间距（`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-11 10:22：调整 chat 生成过程展示：Answer 改为独立外层下拉栏（与 Processing/Finished work 同级，默认展开且位于最下方）；为内层块输出增加最大高度与滚动条，避免超长内容挤占聊天区域（`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-11 10:02：进一步完善 chat “生成过程”UI：修复块结束后旋转箭头仍显示（补齐 `hidden` 样式）；外层标题改为 `Processing`/`Finished work`；Answer 改为外层区域渲染且默认展开；内层块增加缩进、间距更紧凑；Code 块增加简易语法高亮，其它块使用 markdown 渲染（`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-11 09:37：优化 chat “生成过程”折叠展示：旋转弧形箭头仅在当前生成中显示，块结束后改为常规下拉标志；同时改进流式解析，确保检测到 `<Analyze>` 等开闭标签时即时创建/闭合对应下拉块（`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-11 09:11：右侧 chat 面板新增“生成过程”折叠区：在 trace 链条下方以紧凑的下拉栏展示 `<Analyze>/<Understand>/<Code>/<Answer>` 的流式增量内容；块结束自动折叠，并在生成中显示旋转弧形箭头；同时将 feedback 阶段的流式 delta 同步到 chat UI（`src/deepanalyze/chatPanel.ts`、`src/deepanalyze/open.ts`、`style/base.css`）。
- 2026-01-10 11:02：同步项目当前状态说明到 `docs/STATUS.md`（功能概览、存储位置、prompt 双语与验证清单）。
- 2026-01-10 10:47：继续修复 chat 流式 500：补齐 `ChatStreamHandler` 对 `prompt_lang` 的解析，并清理 `ChatHandler` 中重复的 `prompt_lang` 赋值，避免再次触发 `NameError`（`deepanalyze/handlers.py`）。
- 2026-01-10 10:37：修复 chat 首轮流式 500：`ChatStreamHandler` 未定义 `prompt_lang` 却传入 `_apply_model_to_settings(...)`，触发 `NameError` 导致 SSE 提前中断；现已补齐解析（`deepanalyze/handlers.py`）。
- 2026-01-10 09:57：模型选择器 UI 调整与 prompt 双语化：移除模型下拉旁“+”按钮（仅保留下拉内“添加自定义模型”入口）；新增“语言偏好（中文/English）”选择并持久化，后端按语言自动选择对应的 system prompt（`*_ZH`）；为内置 prompts 补齐中英文两份并更新索引（`src/deepanalyze/chatPanel.ts`、`src/deepanalyze/api.ts`、`src/deepanalyze/open.ts`、`deepanalyze/handlers.py`、`deepanalyze/prompts/*`、`style/base.css`）。
- 2026-01-09 19:44：增强“使用大模型编辑（cell rewrite）”上下文：当目标单元格为 code cell 时，前端会提取该单元格的输出/错误信息并随请求一并发送；后端将其注入改写 prompt，帮助模型基于运行结果修正代码（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/api.ts`、`deepanalyze/handlers.py`）。
- 2026-01-09 19:19：修复 server extension 加载失败：`CellRewriteStreamHandler` 中 `try` 块缩进错误导致 `IndentationError`，现已修正（`deepanalyze/handlers.py`）。
- 2026-01-09 18:51：修复部分 Jupyter 环境下 `/deepanalyze/*` 接口 404：在后端入口补充 `load_jupyter_server_extension` 与 `_jupyter_server_extension_paths` 兼容别名，确保 server extension 能被正确加载注册路由（`deepanalyze/__init__.py`）。
- 2026-01-09 16:50：让“使用大模型编辑（cell rewrite）”跟随当前模型选择：前端对 `/deepanalyze/cell/rewrite(/stream)` 请求携带 `model_id`；后端按 `model_id` 动态路由选择 LLM 与温度（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/api.ts`、`deepanalyze/handlers.py`）。
- 2026-01-09 16:14：去除日志中对模型输出/大段内容的直接打印：chat/feedback 流式 delta 日志改为只记录长度；后端不再打印前端上报的 logs/tool_results 具体内容，仅保留统计信息（`deepanalyze/handlers.py`）。
- 2026-01-09 15:50：修复外部 API 模型在 feedback 阶段直接失败导致前端“done/回退”的问题：对 OpenAI-compatible 后端把内部 `role=execute` 映射为 `role=user`（带 `# Execution Result` 前缀），避免服务端因非法 role 返回 400（`deepanalyze/agent_llm_gateway.py`）。
- 2026-01-09 11:26：模型选择器增强：下拉项新增“⚙配置”可设置 base_url/model/temperature/api_key；选择器旁新增“+”可添加自定义模型并持久化到用户侧 `~/.deepanalyze/models.json`；后端新增 `/deepanalyze/models/upsert` 并让温度参数贯穿到推理调用（`deepanalyze/agent_model_store.py`、`deepanalyze/model_registry.py`、`deepanalyze/handlers.py`、`src/deepanalyze/chatPanel.ts`、`style/base.css`）。
- 2026-01-09 11:01：修复 Chat 流式接口 `/deepanalyze/chat/stream` 500 导致前端回退非流式的问题：后端 `ChatStreamHandler` 补齐 `model_id` 解析，避免引用未定义变量引发异常（`deepanalyze/handlers.py`）。
- 2026-01-09 10:36：Chat 对话新增“模型选择器 + API Key 管理”（左下角下拉栏，绿/红点提示与设置）；后端新增模型注册表与 OpenAI-Compatible 通用调用（按 `model_id` 动态切换 base_url/prompt，并新增 `/deepanalyze/models`、`/deepanalyze/models/key` 接口）；新增通用大模型 prompt（`universal_llm`）与开发说明文档（`docs/LLM_MODEL_SELECTOR.md`）。
- 2026-01-07 09:34：新增开发者导读文档 `docs/DEVELOPMENT_GUIDE.md`，并在前端（`src/index.ts`、`src/deepanalyze/*`）与后端（`deepanalyze/__init__.py`、`deepanalyze/handlers.py`、`deepanalyze/agent_orchestrator.py`）关键位置补充中文注释，便于快速理解整体链路与模块职责。
- 2026-01-06 11:47：新增 scratch.ipynb 单元格“自然语言改写”（每个单元格按钮 + 内嵌输入框，调用 `POST /deepanalyze/cell/rewrite` 直连 vLLM，并用返回内容覆盖原单元格）；流式输出结束后自动删除 scratch 的流式占位 raw cell（前端 `src/deepanalyze/open.ts`）。
- 2026-01-06 16:04：调整 scratch 单元格“改写”入口为右上角工具栏按钮；输入框改为点击按钮后按需显示，确定/取消后自动收起（`src/deepanalyze/scratchCellRewrite.ts`、`style/base.css`）。
- 2026-01-06 16:11：修复 `scratchCellRewrite` 中对 `cell.node` 的空值处理，避免 `jlpm build` 报 TS18047（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-06 16:32：重做 scratch 单元格改写 UI：按钮使用 CellToolbar 注入；输入框内嵌到 cell 顶部且点击才显示；提交后展示闪烁 working 灰点并提供确认/回退（`src/deepanalyze/scratchCellRewrite.ts`、`style/base.css`）。
- 2026-01-06 17:22：修复部分环境下 cell 工具栏延迟渲染导致“改写”按钮不出现：改为 DOM 注入到 `.jp-CellToolbar/.jp-Cell-toolbar`，并用 MutationObserver 等待工具栏节点出现（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-06 18:52：继续加固“改写”按钮注入：支持 `.jp-CellHeader` 等不同 DOM 结构，并在 notebook 初次渲染阶段重试安装与在 active cell 变化时补装（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-06 19:29：取消单元格顶部按钮/输入框方案，改为在 scratch 单元格右键菜单新增“使用大模型编辑”，点击后弹出对话框输入指令并覆盖单元格内容（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/open.ts`）。
- 2026-01-06 20:06：取消“仅在继续/中止等待阶段才能编辑”的限制：右键“使用大模型编辑”随时可用（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-06 20:37：单元格“使用大模型编辑”支持流式写回：后端新增 `POST /deepanalyze/cell/rewrite/stream`（SSE start/delta/final），前端将 delta 逐步写入 cell；同时清理模型输出的 `[python]`/```python 围栏（`deepanalyze/handlers.py`、`deepanalyze/__init__.py`、`src/deepanalyze/api.ts`、`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-06 21:31：修复“继续生成直接 done/空输出”与快照错位：后端将前端传入的 `execute_text` 写入 `role=execute`（避免 display_data 场景输出摘要为空导致无新增上下文）；前端为模型生成的 cell 写入 `metadata.deepanalyze` 并在回传快照时按该 metadata 重新定位 cell（避免用户增删 cell 后 index 乱套）（`deepanalyze/agent_orchestrator.py`、`src/deepanalyze/open.ts`）。
- 2026-01-07 16:46：右键“使用大模型编辑”点击确定后先把 cell 内容置为 `waiting`，收到流式 `start` 再开始写入增量输出（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-07 16:53：为“使用大模型编辑”新增单元格底部通知条：生成中可“停止”并回退原内容；生成后可“接受/回退”；流式请求支持 AbortSignal（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/api.ts`、`style/base.css`）。
- 2026-01-07 17:33：拆分通知条位置与行为：生成中“停止”通知条放到 cell 顶部；生成后“接受/回退”通知条放到 cell 底部；点击停止/接受/回退后通知条消失；接受会保留用户对最终内容的二次编辑，回退恢复改写前内容（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/api.ts`、`style/base.css`）。
- 2026-01-07 17:53：修复通知条重复与不消失：创建时清理残留通知条；点击停止/接受/回退后直接移除上下两条通知条并清理状态（`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/api.ts`）。
- 2026-01-08 09:31：调整通知条展示：生成结束后强制移除顶部“停止”通知条；底部“接受/回退”通知条移动到输出区之前（输入区之后），保证位于输出结果顶部（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-08 09:37：修复取消/空指令时通知条残留：右键弹窗取消或空输入确定时清理并移除上下通知条；生成开始阶段不再出现“接受/回退”通知条（`src/deepanalyze/scratchCellRewrite.ts`）。
- 2026-01-08 10:22：修复通知条 `hidden` 被 CSS 覆盖导致生成中仍显示“接受/回退”；并将右键“使用大模型编辑”改为全局注册，所有 notebook 单元格均可使用（`style/base.css`、`src/index.ts`、`src/deepanalyze/scratchCellRewrite.ts`、`src/deepanalyze/open.ts`）。
- 2026-01-08 14:38：对话框 tag 跳转改为滚动到目标 cell 的开头位置（不再居中）（`src/deepanalyze/open.ts`）。
- 2026-01-08 14:50：放大大模型编辑通知条与按钮尺寸，并将“接受/回退”按钮分别改为绿色/红色强调（`style/base.css`）。
- 2026-01-08 15:04：修复新建工作区偶发 “directory not found”：目录创建/重命名后增加可重试的可见性确认，避免 Contents API 短暂不一致导致进入失败（`src/deepanalyze/workspace.ts`）。

## 当前状态（截至 2026-01-06）

### 已完成

- vLLM（OpenAI-Compatible）对话链路打通
  - 后端：`deepanalyze/agent_vllm_client.py`、`deepanalyze/agent_orchestrator.py`
  - 标签解析：`<Analyze>/<Understand>/<Code>/<Answer>`（`deepanalyze/agent_tag_parser.py`）
  - 前端写入：把标签段映射为 notebook 操作（`frontend_ops`）并执行（`src/deepanalyze/open.ts`）

- 流式推理与 SSE 通道
  - 后端新增 SSE 接口：
    - `POST /deepanalyze/chat/stream`
    - `POST /deepanalyze/agent/feedback/stream`
  - 前端新增 SSE 消费：
    - `src/deepanalyze/api.ts#streamChatMessage`
    - `src/deepanalyze/api.ts#streamAgentFeedback`

- scratch notebook 的“流式占位显示”
  - 在 `scratch.ipynb` 末尾插入 raw cell，随 token 增量更新，非一次性刷新
  - 生成中锁定 cell（不可编辑/删除），结束后自动解锁
  - 若需要回环（`await_feedback=true` 且未产出 `<Answer>`），显示“等待执行/回环…”而非过早 done

- 流式异常与兜底增强
  - 增加后端 debug 日志（SSE 写入失败、delta 统计、vLLM stream done 等）
  - 修复 vLLM 流式偶发空输出（`deltas=0/content_len=0`）导致前端误判结束：
    - 当流式结果为空时，后端自动回退执行一次非流式请求以获取完整内容

- 执行回传（execute）上下文增强
  - 将 code cell 执行产生的 `stdout/stderr/异常 traceback` 汇总为 execute 文本
  - 后端把 execute 文本作为 `role=execute` 追加到会话 messages，进入下一轮 vLLM 上下文

- 默认开启流式与 Hub 注入
  - `DEEPANALYZE_ENABLE_STREAM` 当前默认开启
  - `develop/jupyterhub_config.py` 可通过 `c.Spawner.environment` 注入该变量

### 已知问题 / 风险

- vLLM/OpenAI-compatible 的流式协议在不同实现之间存在差异（delta 字段、message 字段、finish_reason 等），目前已做部分兼容与兜底，但仍需持续观察日志并按实际服务端行为调整解析策略。

## 待办（建议优先级）

- P0：补齐前端在“回环多轮”场景下的 UI 状态提示（例如在 chat 面板中更显式展示“执行中/等待继续/继续生成中”）。
- P0：完善对“用户中途切换/关闭 scratch 面板”的容错（例如流式占位 cell 的清理与状态同步）。
- P1：抽象并文档化 `frontend_ops` 的 JSON schema（字段、默认行为、兼容策略）。
- P1：补充更系统的异常码与用户可读提示（vLLM 不可达、解析失败、SSE 中断等）。
