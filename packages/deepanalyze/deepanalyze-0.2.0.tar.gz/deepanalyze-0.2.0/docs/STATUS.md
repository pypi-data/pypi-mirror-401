# 项目当前状态（Status）

更新时间：2026-01-10 11:02

## 关键能力

- **多模型调用（OpenAI-Compatible）**：Chat 可在多模型间切换，后端按 `model_id` 路由到不同 `base_url/model/temperature/prompt`。
- **模型配置管理**：模型列表项支持“⚙配置”，可修改 `base_url/api_key/model name/temperature`；下拉菜单内支持“添加自定义模型”。
- **API Key 状态提示**：模型名旁用绿/红点表示 key 是否可用（可点击跳转设置/选择）。
- **提示词双语**：每个内置 prompt 提供中英文两份（中文为 `*_ZH`）；前端提供“语言偏好（中文/English）”，后端按语言选择对应 system prompt。
- **Notebook 回环与反馈**：支持流式 chat 与流式 feedback（SSE：start/delta/final），并在 scratch notebook 里展示流式占位输出。
- **单元格“使用大模型编辑”**：支持流式改写；对 code cell 会把该单元格输出/报错信息一并送入模型，帮助基于执行结果修正代码。

## 存储与隔离

- **用户模型配置**：`~/.deepanalyze/models.json`（用户添加/修改自定义模型会写入这里）。
- **用户 API Key**：`~/.deepanalyze/api_keys.json`（会尽量以 `600` 权限保存）。
- **浏览器侧偏好**：`localStorage` 保存 `modelId`、`promptLang`、`sessionId`、工作区路径等（同一浏览器 profile 可能跨账号共享；JupyterHub 多用户通常问题不大）。

## prompts 结构

- 索引：`deepanalyze/prompts/index.json`
- 英文：`deepanalyze/prompts/deepanalyze_8b.md`、`deepanalyze/prompts/general.md`、`deepanalyze/prompts/universal_llm.md`
- 中文：`deepanalyze/prompts/deepanalyze_8b_ZH.md`、`deepanalyze/prompts/general_ZH.md`、`deepanalyze/prompts/universal_llm_ZH.md`

## 近期问题与修复

- **chat 首轮流式 500（NameError: prompt_lang 未定义）**：已在 `deepanalyze/handlers.py` 补齐 `ChatStreamHandler` 对 `prompt_lang` 的解析并清理重复赋值。

## 验证清单（建议）

1. **重启 Jupyter Server**（后端改动需要重启才能生效）。
2. 打开 DeepAnalyze → 发送第一条消息，确认 **首轮就能流式输出**，日志无 `NameError: prompt_lang`。
3. 切换“语言偏好”为中文/English，分别发起对话，确认 system prompt 生效（会话按 `lang` 隔离）。
4. 在模型下拉中选择一个外部模型，设置 key 后确认状态点变绿并可正常调用。
5. 对一个会报错的 code cell 使用“使用大模型编辑”，确认模型能看到该 cell 的输出/traceback 并据此改写。

