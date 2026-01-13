import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';

import { getDeepAnalyzeItem } from './storage';

/**
 * 前端 <-> 后端 API 封装。
 *
 * 约定：
 * - 所有请求都会携带当前 DeepAnalyze 上下文（workspaceDir/outputPath/scratchPath）。
 * - 流式接口使用 SSE（`text/event-stream`），每个事件以空行 `\n\n` 分隔，payload 在 `data: {json}` 中。
 */
export interface IChatResponse {
  reply: string;
  data?: unknown;
}

export type IChatStreamEvent =
  | { type: 'start' }
  | { type: 'delta'; delta: string }
  | { type: 'final'; response: IChatResponse };

export interface IModelApiKeyStatus {
  model_id: string;
  status: 'ok' | 'missing' | 'invalid' | string;
  has_key: boolean;
  last_error?: string;
  last_validated_at_s?: number;
}

export interface IModelSpecPublic {
  id: string;
  label: string;
  backend: string;
  prompt_name: string;
  requires_api_key: boolean;
  base_url?: string;
  model?: string;
  temperature?: number;
  is_custom?: boolean;
  api_key_status?: IModelApiKeyStatus;
}

export interface IModelsResponse {
  default_model_id: string;
  models: IModelSpecPublic[];
}

export async function fetchModels(): Promise<IModelsResponse> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'models');
  const response = await ServerConnection.makeRequest(requestUrl, { method: 'GET' }, settings);
  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }
  return (await response.json()) as IModelsResponse;
}

export async function setModelApiKey(model_id: string, api_key: string): Promise<IModelApiKeyStatus> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'models', 'key');
  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ model_id, api_key }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );
  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }
  const data = (await response.json()) as { api_key_status?: IModelApiKeyStatus };
  return (data?.api_key_status ?? { model_id, status: 'invalid', has_key: Boolean(api_key) }) as IModelApiKeyStatus;
}

export async function upsertModelConfig(payload: {
  model_id?: string;
  label?: string;
  base_url?: string;
  model?: string;
  temperature?: number;
  api_key?: string;
}): Promise<IModelSpecPublic> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'models', 'upsert');
  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );
  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }
  const data = (await response.json()) as { model?: IModelSpecPublic };
  if (!data?.model) {
    throw new Error('upsertModelConfig: invalid response');
  }
  return data.model;
}

export async function sendChatMessage(
  message: string,
  model_id?: string,
  prompt_lang?: string
): Promise<IChatResponse> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'chat');

  const sessionId = getDeepAnalyzeItem('sessionId').trim();
  const session_id = sessionId ? sessionId : undefined;
  const context = {
    workspaceDir: getDeepAnalyzeItem('activeWorkspaceDir') || undefined,
    outputPath: getDeepAnalyzeItem('activeOutputPath') || undefined,
    scratchPath: getDeepAnalyzeItem('activeScratchPath') || undefined
  };

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ message, context, session_id, model_id, prompt_lang }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  return (await response.json()) as IChatResponse;
}

export async function* streamChatMessage(
  message: string,
  model_id?: string,
  prompt_lang?: string
): AsyncGenerator<IChatStreamEvent> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'chat', 'stream');

  const sessionId = getDeepAnalyzeItem('sessionId').trim();
  const session_id = sessionId ? sessionId : undefined;
  const context = {
    workspaceDir: getDeepAnalyzeItem('activeWorkspaceDir') || undefined,
    outputPath: getDeepAnalyzeItem('activeOutputPath') || undefined,
    scratchPath: getDeepAnalyzeItem('activeScratchPath') || undefined
  };

  // 注意：这里用 `ServerConnection.makeRequest`，以便自动带上 Jupyter 的 baseUrl 与鉴权（token/cookie）。
  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ message, context, session_id, model_id, prompt_lang }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  if (!response.body) {
    throw new Error('stream response.body is empty');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';

  // SSE 基本格式：一段事件由若干行组成，以空行结束；这里仅消费 `data:` 行并拼成 JSON。
  const parseEvent = (chunk: string): IChatStreamEvent | null => {
    const lines = chunk
      .split('\n')
      .map(line => line.trimEnd())
      .filter(line => line.length > 0);
    const dataLines = lines
      .filter(line => line.startsWith('data:'))
      .map(line => line.slice('data:'.length).trim());
    if (dataLines.length === 0) {
      return null;
    }
    const payloadText = dataLines.join('\n').trim();
    if (!payloadText) {
      return null;
    }
    try {
      return JSON.parse(payloadText) as IChatStreamEvent;
    } catch {
      return null;
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    while (true) {
      const idx = buffer.indexOf('\n\n');
      if (idx < 0) {
        break;
      }
      const raw = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const event = parseEvent(raw);
      if (event) {
        yield event;
        if (event.type === 'final') {
          return;
        }
      }
    }
  }
}

export async function sendAgentFeedback(payload: {
  session_id: string;
  execute_text?: string;
  tool_results?: unknown[];
  model_id?: string;
  prompt_lang?: string;
}): Promise<IChatResponse> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'agent', 'feedback');

  const context = {
    workspaceDir: getDeepAnalyzeItem('activeWorkspaceDir') || undefined,
    outputPath: getDeepAnalyzeItem('activeOutputPath') || undefined,
    scratchPath: getDeepAnalyzeItem('activeScratchPath') || undefined
  };

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ ...payload, context }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  return (await response.json()) as IChatResponse;
}

export async function* streamAgentFeedback(payload: {
  session_id: string;
  execute_text?: string;
  tool_results?: unknown[];
  model_id?: string;
  prompt_lang?: string;
}): AsyncGenerator<IChatStreamEvent> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(
    settings.baseUrl,
    'deepanalyze',
    'agent',
    'feedback',
    'stream'
  );

  const context = {
    workspaceDir: getDeepAnalyzeItem('activeWorkspaceDir') || undefined,
    outputPath: getDeepAnalyzeItem('activeOutputPath') || undefined,
    scratchPath: getDeepAnalyzeItem('activeScratchPath') || undefined
  };

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ ...payload, context }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  if (!response.body) {
    throw new Error('stream response.body is empty');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';

  // 事件解析逻辑与 `streamChatMessage` 一致（start/delta/final）。
  const parseEvent = (chunk: string): IChatStreamEvent | null => {
    const lines = chunk
      .split('\n')
      .map(line => line.trimEnd())
      .filter(line => line.length > 0);
    const dataLines = lines
      .filter(line => line.startsWith('data:'))
      .map(line => line.slice('data:'.length).trim());
    if (dataLines.length === 0) {
      return null;
    }
    const payloadText = dataLines.join('\n').trim();
    if (!payloadText) {
      return null;
    }
    try {
      return JSON.parse(payloadText) as IChatStreamEvent;
    } catch {
      return null;
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    while (true) {
      const idx = buffer.indexOf('\n\n');
      if (idx < 0) {
        break;
      }
      const raw = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const event = parseEvent(raw);
      if (event) {
        yield event;
        if (event.type === 'final') {
          return;
        }
      }
    }
  }
}

export async function sendFrontendLog(payload: {
  session_id?: string;
  depth?: number;
  await_feedback?: boolean;
  message?: string;
  logs?: string;
  tool_results?: unknown[];
}): Promise<IChatResponse> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'frontend', 'log');

  const context = {
    workspaceDir: getDeepAnalyzeItem('activeWorkspaceDir') || undefined,
    outputPath: getDeepAnalyzeItem('activeOutputPath') || undefined,
    scratchPath: getDeepAnalyzeItem('activeScratchPath') || undefined
  };

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify({ ...payload, context }),
      headers: { 'Content-Type': 'application/json' }
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  return (await response.json()) as IChatResponse;
}

export interface ICellRewriteResponse {
  answer: string;
  raw: string;
}

export async function rewriteCellSource(payload: {
  source: string;
  instruction: string;
  cell_type?: string;
  execution_result?: string;
  model_id?: string;
  signal?: AbortSignal;
}): Promise<ICellRewriteResponse> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'cell', 'rewrite');
  const { signal, ...body } = payload;

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json' },
      signal
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  return (await response.json()) as ICellRewriteResponse;
}

export type ICellRewriteStreamEvent =
  | { type: 'start' }
  | { type: 'delta'; delta: string }
  | { type: 'final'; response: ICellRewriteResponse & { error?: string } };

export async function* streamRewriteCellSource(payload: {
  source: string;
  instruction: string;
  cell_type?: string;
  execution_result?: string;
  model_id?: string;
  signal?: AbortSignal;
}): AsyncGenerator<ICellRewriteStreamEvent> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(settings.baseUrl, 'deepanalyze', 'cell', 'rewrite', 'stream');
  const { signal, ...body } = payload;

  const response = await ServerConnection.makeRequest(
    requestUrl,
    {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json' },
      signal
    },
    settings
  );

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response);
  }

  if (!response.body) {
    throw new Error('stream response.body is empty');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';

  // 单元格改写的流式协议与 chat 类似（start/delta/final），单独定义事件类型便于最终携带 error。
  const parseEvent = (chunk: string): ICellRewriteStreamEvent | null => {
    const lines = chunk
      .split('\n')
      .map(line => line.trimEnd())
      .filter(line => line.length > 0);
    const dataLines = lines
      .filter(line => line.startsWith('data:'))
      .map(line => line.slice('data:'.length).trim());
    if (dataLines.length === 0) {
      return null;
    }
    const payloadText = dataLines.join('\n').trim();
    if (!payloadText) {
      return null;
    }
    try {
      return JSON.parse(payloadText) as ICellRewriteStreamEvent;
    } catch {
      return null;
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    while (true) {
      const idx = buffer.indexOf('\n\n');
      if (idx < 0) {
        break;
      }
      const raw = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const event = parseEvent(raw);
      if (event) {
        yield event;
        if (event.type === 'final') {
          return;
        }
      }
    }
  }
}
