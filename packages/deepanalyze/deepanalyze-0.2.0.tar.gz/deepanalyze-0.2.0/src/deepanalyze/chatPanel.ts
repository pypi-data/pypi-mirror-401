import { Widget } from '@lumino/widgets';
import { Dialog, showDialog } from '@jupyterlab/apputils';

import {
  fetchModels,
  IChatResponse,
  IModelSpecPublic,
  upsertModelConfig,
  setModelApiKey,
  sendChatMessage,
  sendFrontendLog,
  streamChatMessage
} from './api';
import {
  deepAnalyzeScopeId,
  deepAnalyzeStorageKey,
  getDeepAnalyzeItem,
  setDeepAnalyzeItem
} from './storage';

/**
 * DeepAnalyze Chat 面板（纯前端 UI 层）。
 *
 * 设计要点：
 * - Chat 面板本身不直接操作 notebook；实际写入/执行在 `open.ts` 中完成。
 * - 通过回调把“流式事件（onModelStream）”与“后端返回的 data（onToolResult）”交给外部处理，
 *   从而把 UI 与编排逻辑解耦。
 */
type ChatRole = 'user' | 'assistant' | 'system';

interface IChatRecord {
  role: ChatRole;
  text: string;
  turnId?: string;
  hidden?: boolean;
  trace?: {
    items: Array<{ id: string; tag: string; label: string; path: string; index: number }>;
    activeId?: string;
  };
}

type StreamTag = 'Analyze' | 'Understand' | 'Code' | 'Answer';

interface IStreamBlockUI {
  tag: StreamTag;
  label: string;
  details: HTMLDetailsElement;
  spinner: HTMLSpanElement;
  caret: HTMLSpanElement;
  content: HTMLElement;
  text: string;
  closed: boolean;
}

interface IStreamTurnUI {
  turnId: string;
  container: HTMLDivElement;
  rootDetails: HTMLDetailsElement;
  rootSpinner: HTMLSpanElement;
  rootCaret: HTMLSpanElement;
  rootLabel: HTMLSpanElement;
  answerDetails: HTMLDetailsElement;
  answerSpinner: HTMLSpanElement;
  answerCaret: HTMLSpanElement;
  answerLabel: HTMLSpanElement;
  answerContent: HTMLDivElement;
  innerNode: HTMLDivElement;
  blocks: IStreamBlockUI[];
  activeBlock: IStreamBlockUI | null;
  inAnswer: boolean;
  answerText: string;
  buffer: string;
  countsByTag: Map<StreamTag, number>;
  hasAnswer: boolean;
}

export interface IToolResultUpdate {
  system_text?: string;
  assistant_raw_updates?: string[];
  trace_update?: { tag: string; path: string; index: number };
}

export type IToolResultChunk = void | string | IToolResultUpdate;

export interface IDeepAnalyzeChatPanelOptions {
  onExit?: () => void;
  onReset?: (options: { clearNotebooks: boolean }) => void | Promise<void>;
  onNavigateToCell?: (path: string, index: number) => void | Promise<void>;
  onModelStream?: (
    event:
      | { type: 'start'; turnId: string }
      | { type: 'delta'; turnId: string; delta: string }
      | {
          type: 'final';
          turnId: string;
          awaitFeedback: boolean;
          hasAnswer: boolean;
          raw: string;
        }
      | { type: 'end'; turnId: string }
      | { type: 'error'; turnId: string; error: string }
  ) => void | Promise<void>;
  onToolResult?: (
    data: unknown
  ) =>
    | IToolResultChunk
    | Promise<IToolResultChunk>
    | AsyncIterable<IToolResultChunk>
    | Promise<AsyncIterable<IToolResultChunk>>;
}

export class DeepAnalyzeChatPanel extends Widget {
  private readonly messagesNode: HTMLDivElement;
  private readonly inputNode: HTMLTextAreaElement;
  private readonly sendButtonNode: HTMLButtonElement;
  private readonly continueButtonNode: HTMLButtonElement;
  private readonly abortButtonNode: HTMLButtonElement;
  private readonly autoToggleNode: HTMLInputElement;
  private readonly modelSelectorNode: HTMLDivElement;
  private readonly modelButtonNode: HTMLButtonElement;
  private readonly modelButtonDotNode: HTMLSpanElement;
  private readonly modelButtonLabelNode: HTMLSpanElement;
  private readonly promptLangSelectNode: HTMLSelectElement;
  private readonly modelMenuNode: HTMLDivElement;
  private documentClickHandler: ((event: MouseEvent) => void) | null = null;
  private wheelChainingHandler: ((event: WheelEvent) => void) | null = null;
  private models: IModelSpecPublic[] = [];
  private activeModelId = '';
  private promptLang: 'zh' | 'en' = 'zh';
  private hiddenTabBarNode: HTMLElement | null = null;
  private readonly onReset?: (options: { clearNotebooks: boolean }) => void | Promise<void>;
  private readonly onNavigateToCell?: (path: string, index: number) => void | Promise<void>;
  private readonly onModelStream?: (
    event:
      | { type: 'start'; turnId: string }
      | { type: 'delta'; turnId: string; delta: string }
      | {
          type: 'final';
          turnId: string;
          awaitFeedback: boolean;
          hasAnswer: boolean;
          raw: string;
        }
      | { type: 'end'; turnId: string }
      | { type: 'error'; turnId: string; error: string }
  ) => void | Promise<void>;
  private readonly onToolResult?: (
    data: unknown
  ) =>
    | IToolResultChunk
    | Promise<IToolResultChunk>
    | AsyncIterable<IToolResultChunk>
    | Promise<AsyncIterable<IToolResultChunk>>;

  // UI 状态机：
  // - isBusy: 防止并发发送
  // - isModelGenerating: 控制“生成中...”提示与按钮状态
  // - isAwaitingFeedback: 表示需要执行回环（通常：模型给了 Code 但还没给 Answer）
  private isBusy = false;
  private isModelGenerating = false;
  private isAwaitingFeedback = false;
  private readonly historyKey: string;
  private readonly history: IChatRecord[] = [];
  private markedModule: any | null = null;
  private markedModulePromise: Promise<any> | null = null;
  private markdownRenderer: any | null = null;
  private workingMessageNode: HTMLDivElement | null = null;
  private workingMessageLabelNode: HTMLSpanElement | null = null;
  private activeTraceTurnId: string | null = null;
  private currentTurnId: string | null = null;
  private readonly traceStateByTurnId = new Map<
    string,
    {
      items: Array<{ id: string; tag: string; label: string; path: string; index: number }>;
      activeId?: string;
      counts: Map<string, number>;
    }
  >();
  private readonly traceBubblesByTurnId = new Map<string, Set<HTMLDivElement>>();
  private readonly assistantBubbleByTurnId = new Map<string, HTMLDivElement>();
  private readonly streamUiByTurnId = new Map<string, IStreamTurnUI>();

  private awaitingDecisionPromise: Promise<'continue' | 'abort'> | null = null;
  private awaitingDecisionResolve: ((value: 'continue' | 'abort') => void) | null = null;
  private readonly autoContinueKey = deepAnalyzeStorageKey('autoContinue');

  constructor(options: IDeepAnalyzeChatPanelOptions = {}) {
    super();
    this.addClass('deepanalyze-chat-panel');

    this.title.label = 'DeepAnalyze 对话';
    this.title.closable = false;
    this.onReset = options.onReset;
    this.onNavigateToCell = options.onNavigateToCell;
    this.onModelStream = options.onModelStream;
    this.onToolResult = options.onToolResult;

    const card = document.createElement('div');
    card.className = 'deepanalyze-chat-card';

    const header = document.createElement('div');
    header.className = 'deepanalyze-chat-panel-header';
    const headerTitle = document.createElement('div');
    headerTitle.className = 'deepanalyze-chat-panel-title';
    headerTitle.textContent = 'DeepAnalyze';
    header.appendChild(headerTitle);

    const headerActions = document.createElement('div');
    headerActions.className = 'deepanalyze-chat-panel-actions';

    const resetButton = document.createElement('button');
    resetButton.className = 'deepanalyze-chat-exit-button';
    resetButton.type = 'button';
    resetButton.textContent = '重置';
    resetButton.addEventListener('click', () => void this.handleReset());
    headerActions.appendChild(resetButton);

    const exitButton = document.createElement('button');
    exitButton.className = 'deepanalyze-chat-exit-button';
    exitButton.type = 'button';
    exitButton.textContent = '返回';
    exitButton.addEventListener('click', () => options.onExit?.());
    headerActions.appendChild(exitButton);
    header.appendChild(headerActions);

    const messages = document.createElement('div');
    messages.className = 'deepanalyze-chat-messages';
    this.messagesNode = messages;
    this.installWheelScrollChaining();

    const inputWrapper = document.createElement('div');
    inputWrapper.className = 'deepanalyze-chat-input-wrapper';

    const composer = document.createElement('div');
    composer.className = 'deepanalyze-chat-composer';

    const input = document.createElement('textarea');
    input.className = 'deepanalyze-chat-input';
    input.placeholder = '输入消息，Enter 发送，Shift+Enter 换行…';
    input.rows = 2;
    composer.appendChild(input);
    this.inputNode = input;

    const actions = document.createElement('div');
    actions.className = 'deepanalyze-chat-actions';

    const modelSelector = document.createElement('div');
    modelSelector.className = 'deepanalyze-chat-model-selector';

    const modelButton = document.createElement('button');
    modelButton.className = 'deepanalyze-chat-model-button';
    modelButton.type = 'button';

    const modelDot = document.createElement('span');
    modelDot.className = 'deepanalyze-model-dot deepanalyze-model-dot-ok';
    modelButton.appendChild(modelDot);

    const modelLabel = document.createElement('span');
    modelLabel.className = 'deepanalyze-chat-model-label';
    modelLabel.textContent = 'DeepAnalyze 8B';
    modelButton.appendChild(modelLabel);

    const modelCaret = document.createElement('span');
    modelCaret.className = 'deepanalyze-chat-model-caret';
    modelCaret.textContent = '▾';
    modelButton.appendChild(modelCaret);

    const modelMenu = document.createElement('div');
    modelMenu.className = 'deepanalyze-chat-model-menu';
    modelMenu.style.display = 'none';

    const langSelect = document.createElement('select');
    langSelect.className = 'deepanalyze-chat-lang-select';
    langSelect.title = '语言偏好（决定使用中文或英文 system prompt）';
    const optZh = document.createElement('option');
    optZh.value = 'zh';
    optZh.textContent = '中文';
    const optEn = document.createElement('option');
    optEn.value = 'en';
    optEn.textContent = 'English';
    langSelect.appendChild(optZh);
    langSelect.appendChild(optEn);

    modelSelector.appendChild(modelButton);
    modelSelector.appendChild(langSelect);
    modelSelector.appendChild(modelMenu);
    actions.appendChild(modelSelector);

    this.modelSelectorNode = modelSelector;
    this.modelButtonNode = modelButton;
    this.modelButtonDotNode = modelDot;
    this.modelButtonLabelNode = modelLabel;
    this.promptLangSelectNode = langSelect;
    this.modelMenuNode = modelMenu;

    const continueButton = document.createElement('button');
    continueButton.className = 'deepanalyze-chat-control-button deepanalyze-chat-continue-button';
    continueButton.type = 'button';
    continueButton.textContent = '继续';
    actions.appendChild(continueButton);
    this.continueButtonNode = continueButton;

    const abortButton = document.createElement('button');
    abortButton.className = 'deepanalyze-chat-control-button deepanalyze-chat-abort-button';
    abortButton.type = 'button';
    abortButton.textContent = '中止';
    actions.appendChild(abortButton);
    this.abortButtonNode = abortButton;

    const autoLabel = document.createElement('label');
    autoLabel.className = 'deepanalyze-chat-auto-toggle';
    const autoToggle = document.createElement('input');
    autoToggle.type = 'checkbox';
    autoToggle.checked = this.getAutoContinueEnabled();
    autoLabel.appendChild(autoToggle);
    const autoText = document.createElement('span');
    autoText.textContent = '自动';
    autoLabel.appendChild(autoText);
    actions.appendChild(autoLabel);
    this.autoToggleNode = autoToggle;

    const sendButton = document.createElement('button');
    sendButton.className = 'deepanalyze-chat-send-button';
    sendButton.type = 'button';
    sendButton.textContent = '发送';
    actions.appendChild(sendButton);
    this.sendButtonNode = sendButton;

    composer.appendChild(actions);
    inputWrapper.appendChild(composer);

    card.appendChild(header);
    card.appendChild(messages);
    card.appendChild(inputWrapper);

    this.node.appendChild(card);

    this.inputNode.addEventListener('keydown', event => {
      if (event.key !== 'Enter') {
        return;
      }
      if (event.shiftKey) {
        return;
      }

      event.preventDefault();
      void this.handleSend();
    });

    this.sendButtonNode.addEventListener('click', () => void this.handleSend());
    this.continueButtonNode.addEventListener('click', () => this.resolveAwaitDecision('continue'));
    this.abortButtonNode.addEventListener('click', () => this.resolveAwaitDecision('abort'));
    this.autoToggleNode.addEventListener('change', () =>
      this.setAutoContinueEnabled(this.autoToggleNode.checked)
    );

    this.activeModelId = (getDeepAnalyzeItem('modelId') || '').trim();
    if (!this.normalizeModelId(this.activeModelId)) {
      this.setActiveModelId('deepanalyze_8b');
    }
    const storedPromptLang = (getDeepAnalyzeItem('promptLang') || '').trim();
    this.promptLang = this.normalizePromptLang(storedPromptLang || 'zh');
    this.promptLangSelectNode.value = this.promptLang;
    if (!storedPromptLang) {
      setDeepAnalyzeItem('promptLang', this.promptLang);
    }
    this.modelButtonNode.addEventListener('click', event => {
      event.preventDefault();
      event.stopPropagation();
      this.toggleModelMenu();
    });
    this.promptLangSelectNode.addEventListener('change', () => {
      const next = this.normalizePromptLang(this.promptLangSelectNode.value);
      this.promptLang = next;
      setDeepAnalyzeItem('promptLang', next);
    });
    this.documentClickHandler = event => {
      const target = event.target as Node | null;
      if (!target) {
        return;
      }
      if (!this.modelSelectorNode.contains(target)) {
        this.hideModelMenu();
      }
    };
    document.addEventListener('click', this.documentClickHandler, true);
    void this.refreshModels();

    this.historyKey = this.buildHistoryKey();
    void this.ensureMarkdownReady();
    const restored = this.restoreHistory();
    if (!restored) {
      this.addMessage('assistant', '这里是 DeepAnalyze 对话框。');
    }

    this.syncControlState();
  }

  protected onAfterAttach(): void {
    this.inputNode.focus();

    const tabSelector = `.lm-DockPanel-tabBar .lm-TabBar-tab[data-id="${this.id}"], .jp-DockPanel-tabBar .lm-TabBar-tab[data-id="${this.id}"]`;
    const tab = document.querySelector(tabSelector) as HTMLElement | null;
    const tabBar = tab?.closest('.lm-DockPanel-tabBar, .jp-DockPanel-tabBar') as
      | HTMLElement
      | null;
    tabBar?.classList.add('deepanalyze-hidden-tabbar');
    this.hiddenTabBarNode = tabBar;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    if (this.documentClickHandler) {
      document.removeEventListener('click', this.documentClickHandler, true);
      this.documentClickHandler = null;
    }
    if (this.wheelChainingHandler) {
      this.messagesNode.removeEventListener('wheel', this.wheelChainingHandler, true);
      this.wheelChainingHandler = null;
    }
    this.hiddenTabBarNode?.classList.remove('deepanalyze-hidden-tabbar');
    this.hiddenTabBarNode = null;
    super.dispose();
  }

  private installWheelScrollChaining(): void {
    if (this.wheelChainingHandler) {
      return;
    }

    const handler = (event: WheelEvent) => {
      const target = event.target as HTMLElement | null;
      if (!target) {
        return;
      }

      const inner = target.closest(
        '.deepanalyze-chat-stream-block-content-code, .deepanalyze-chat-stream-block-content-markdown'
      ) as HTMLElement | null;
      if (!inner) {
        return;
      }

      const outer = this.messagesNode;
      let deltaY = event.deltaY;
      if (event.deltaMode === 1) {
        deltaY *= 16;
      } else if (event.deltaMode === 2) {
        deltaY *= outer.clientHeight;
      }
      if (!deltaY) {
        return;
      }

      const eps = 1;
      const atTop = inner.scrollTop <= eps;
      const atBottom = inner.scrollTop + inner.clientHeight >= inner.scrollHeight - eps;
      const wantsUp = deltaY < 0;
      const wantsDown = deltaY > 0;
      if ((wantsUp && atTop) || (wantsDown && atBottom)) {
        outer.scrollTop += deltaY;
        event.preventDefault();
        event.stopPropagation();
      }
    };

    this.wheelChainingHandler = handler;
    this.messagesNode.addEventListener('wheel', handler, { passive: false, capture: true });
  }

  private buildHistoryKey(): string {
    const sessionId = getDeepAnalyzeItem('sessionId');
    const workspaceDir = getDeepAnalyzeItem('activeWorkspaceDir');
    const suffix = (sessionId || workspaceDir || 'default').trim();
    const modelId = (getDeepAnalyzeItem('modelId') || 'default').trim();
    const scope = deepAnalyzeScopeId();
    return `deepanalyze.chatHistory@${scope}:${suffix}:${modelId}`;
  }

  private persistHistory(): void {
    const maxItems = 200;
    const trimmed = this.history.slice(Math.max(0, this.history.length - maxItems));
    try {
      window.localStorage.setItem(this.historyKey, JSON.stringify(trimmed));
    } catch {
      // ignore quota errors
    }
  }

  private restoreHistory(): boolean {
    try {
      const raw = window.localStorage.getItem(this.historyKey);
      if (!raw) {
        return false;
      }
      const parsed = JSON.parse(raw) as unknown;
      if (!Array.isArray(parsed) || parsed.length === 0) {
        return false;
      }

      const items: IChatRecord[] = [];
      for (const item of parsed) {
        const role = (item as any)?.role as ChatRole;
        const text = String((item as any)?.text ?? '');
        if (!role || !text) {
          continue;
        }
        if (role !== 'user' && role !== 'assistant' && role !== 'system') {
          continue;
        }
        const turnIdRaw = (item as any)?.turnId;
        const turnId = typeof turnIdRaw === 'string' && turnIdRaw.trim() ? turnIdRaw.trim() : undefined;
        const hidden = Boolean((item as any)?.hidden);
        const traceRaw = (item as any)?.trace;
        let trace: IChatRecord['trace'] | undefined = undefined;
        if (traceRaw && typeof traceRaw === 'object') {
          const list = Array.isArray((traceRaw as any)?.items) ? (traceRaw as any).items : [];
          const restoredItems: NonNullable<IChatRecord['trace']>['items'] = [];
          for (const t of list) {
            const id = String((t as any)?.id ?? '').trim();
            const tag = String((t as any)?.tag ?? '').trim();
            const label = String((t as any)?.label ?? '').trim();
            const path = String((t as any)?.path ?? '').trim();
            const index = Number.isFinite((t as any)?.index) ? Number((t as any).index) : NaN;
            if (!id || !tag || !label || !path || !Number.isFinite(index) || index < 0) {
              continue;
            }
            restoredItems.push({ id, tag, label, path, index });
          }
          const activeId = String((traceRaw as any)?.activeId ?? '').trim() || undefined;
          if (restoredItems.length > 0) {
            trace = { items: restoredItems, activeId };
          }
        }
        items.push({ role, text, turnId, hidden, trace });
      }

      if (items.length === 0) {
        return false;
      }

      const hiddenAssistantByTurnId = new Map<string, string[]>();
      for (const record of items) {
        if (record.role !== 'assistant' || !record.hidden) {
          continue;
        }
        const id = record.turnId;
        if (!id) {
          continue;
        }
        const list = hiddenAssistantByTurnId.get(id) ?? [];
        list.push(record.text);
        hiddenAssistantByTurnId.set(id, list);
      }

      // 兼容旧版本：历史里可能存在“仅用于恢复的 assistant_raw_updates”，它们在运行时并未渲染到 UI。
      // 旧格式缺少 `hidden` 标记，因此这里按“同一轮 user 之后出现多条带标签的 assistant”做一次折叠。
      let seenTaggedAssistant = false;
      for (const record of items) {
        if (record.role === 'user') {
          seenTaggedAssistant = false;
          continue;
        }
        if (record.role !== 'assistant' || record.hidden) {
          continue;
        }
        if (record.turnId) {
          continue;
        }
        const tagged = /<(Analyze|Understand|Code|Answer)>/i.test(record.text);
        if (!tagged) {
          continue;
        }
        if (seenTaggedAssistant) {
          record.hidden = true;
          continue;
        }
        seenTaggedAssistant = true;
      }

      for (const item of items) {
        if (item.hidden) {
          continue;
        }
        if (item.role === 'assistant' && item.turnId && item.trace?.items?.length) {
          this.restoreTraceState(item.turnId, item.trace);
        }
        let displayText = item.text;
        if (item.role === 'assistant' && item.turnId) {
          const hiddenList = hiddenAssistantByTurnId.get(item.turnId) ?? [];
          if (hiddenList.length > 0) {
            const countTags = (s: string) =>
              (String(s ?? '').match(/<(Analyze|Understand|Code|Answer)>/gi) ?? []).length;
            const combined = hiddenList.join('\n\n').trim();
            if (countTags(combined) > countTags(displayText)) {
              displayText = combined;
            }
          }
        }
        this.addMessage(item.role, displayText, { persist: false, turnId: item.turnId });
      }
      this.history.push(...items);
      return true;
    } catch {
      return false;
    }
  }

  private normalizeModelId(raw: string): string {
    return String(raw ?? '')
      .trim()
      .toLowerCase()
      .replace(/\s+/g, '_');
  }

  private normalizePromptLang(raw: string): 'zh' | 'en' {
    const v = String(raw ?? '')
      .trim()
      .toLowerCase();
    if (v === 'zh' || v === 'zh-cn' || v === 'zh_cn' || v === 'cn') {
      return 'zh';
    }
    if (v === 'en' || v === 'en-us' || v === 'en_us') {
      return 'en';
    }
    return 'zh';
  }

  private getPromptLang(): 'zh' | 'en' {
    return this.normalizePromptLang(this.promptLang || 'zh');
  }

  private getSelectedModel(): IModelSpecPublic | null {
    const current = this.normalizeModelId(this.activeModelId);
    if (!current) {
      return null;
    }
    for (const model of this.models) {
      if (this.normalizeModelId(model.id) === current) {
        return model;
      }
    }
    return null;
  }

  private getModelDotStatus(model: IModelSpecPublic | null): 'ok' | 'bad' {
    if (!model) {
      return 'ok';
    }
    if (!model.requires_api_key) {
      return 'ok';
    }
    const status = String(model.api_key_status?.status ?? '').toLowerCase().trim();
    return status === 'ok' ? 'ok' : 'bad';
  }

  private setActiveModelId(modelId: string): void {
    const normalized = this.normalizeModelId(modelId);
    this.activeModelId = normalized;
    setDeepAnalyzeItem('modelId', normalized);
  }

  private renderModelButton(): void {
    const selected = this.getSelectedModel();
    const label = selected?.label || this.activeModelId || 'DeepAnalyze 8B';
    this.modelButtonLabelNode.textContent = label;
    const status = this.getModelDotStatus(selected);
    this.modelButtonDotNode.className =
      status === 'ok' ? 'deepanalyze-model-dot deepanalyze-model-dot-ok' : 'deepanalyze-model-dot deepanalyze-model-dot-bad';
  }

  private renderModelMenu(): void {
    const menu = this.modelMenuNode;
    menu.innerHTML = '';

    const models =
      this.models.length > 0
        ? this.models
        : ([
            {
              id: 'deepanalyze_8b',
              label: 'DeepAnalyze 8B',
              backend: 'vllm',
              prompt_name: 'deepanalyze_8b',
              requires_api_key: false
            }
          ] as IModelSpecPublic[]);

    const selectedId = this.normalizeModelId(this.activeModelId);
    for (const model of models) {
      const row = document.createElement('div');
      row.className = 'deepanalyze-chat-model-item';
      if (this.normalizeModelId(model.id) === selectedId) {
        row.classList.add('is-active');
      }

      const dot = document.createElement('span');
      const dotStatus = this.getModelDotStatus(model);
      dot.className =
        dotStatus === 'ok' ? 'deepanalyze-model-dot deepanalyze-model-dot-ok' : 'deepanalyze-model-dot deepanalyze-model-dot-bad';
      row.appendChild(dot);

      const text = document.createElement('span');
      text.className = 'deepanalyze-chat-model-item-label';
      text.textContent = model.label || model.id;
      row.appendChild(text);

      const gear = document.createElement('button');
      gear.type = 'button';
      gear.className = 'deepanalyze-chat-model-gear';
      gear.title = '配置该模型';
      gear.textContent = '⚙';
      row.appendChild(gear);

      dot.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        if (dotStatus === 'ok') {
          this.setActiveModelId(model.id);
          this.renderModelButton();
          this.hideModelMenu();
        } else {
          void this.openApiKeyDialog(model);
        }
      });

      gear.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        void this.openModelConfigDialog(model);
      });

      row.addEventListener('click', () => {
        if (dotStatus === 'ok') {
          this.setActiveModelId(model.id);
          this.renderModelButton();
          this.hideModelMenu();
        } else {
          void this.openApiKeyDialog(model);
        }
      });

      menu.appendChild(row);
    }

    const addRow = document.createElement('div');
    addRow.className = 'deepanalyze-chat-model-item deepanalyze-chat-model-item-add';
    addRow.textContent = '+ 添加自定义模型';
    addRow.addEventListener('click', () => void this.openAddCustomModelDialog());
    menu.appendChild(addRow);
  }

  private toggleModelMenu(): void {
    if (this.modelMenuNode.style.display === 'none') {
      this.modelMenuNode.style.display = 'block';
      // 展开时尽量刷新一次状态（比如用户刚设置过 key）
      void this.refreshModels();
      return;
    }
    this.hideModelMenu();
  }

  private hideModelMenu(): void {
    this.modelMenuNode.style.display = 'none';
  }

  private async refreshModels(): Promise<void> {
    try {
      const data = await fetchModels();
      const models = Array.isArray(data?.models) ? data.models : [];
      this.models = models;

      const defaultId = this.normalizeModelId(String(data?.default_model_id ?? 'deepanalyze_8b'));
      let nextId = this.normalizeModelId(this.activeModelId) || defaultId || 'deepanalyze_8b';
      if (models.length > 0 && !models.some(m => this.normalizeModelId(m.id) === nextId)) {
        nextId = defaultId || this.normalizeModelId(models[0]?.id ?? '') || 'deepanalyze_8b';
      }
      this.setActiveModelId(nextId);
      this.renderModelButton();
      this.renderModelMenu();
    } catch {
      if (!this.normalizeModelId(this.activeModelId)) {
        this.setActiveModelId('deepanalyze_8b');
      }
      this.renderModelButton();
      this.renderModelMenu();
    }
  }

  private async openApiKeyDialog(model: IModelSpecPublic): Promise<void> {
    const wrapper = document.createElement('div');
    wrapper.className = 'deepanalyze-chat-model-key-dialog';
    const hint = document.createElement('div');
    hint.className = 'deepanalyze-chat-model-key-hint';
    hint.textContent = `为「${model.label || model.id}」设置 API Key（保存后将进行一次校验）。`;
    wrapper.appendChild(hint);

    const input = document.createElement('input');
    input.type = 'password';
    input.placeholder = '请输入 API Key（例如 sk-...）';
    input.className = 'deepanalyze-chat-model-key-input';
    wrapper.appendChild(input);

    const body = new Widget({ node: wrapper });
    const result = await showDialog({
      title: `设置 ${model.label || model.id} API Key`,
      body,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: '保存' })]
    });
    if (!result.button.accept) {
      return;
    }

    const value = String(input.value ?? '').trim();
    try {
      const status = await setModelApiKey(model.id, value);
      await this.refreshModels();
      const ok = String(status?.status ?? '').toLowerCase() === 'ok';
      if (!ok) {
        const msg = String(status?.last_error ?? '').trim() || '该 API Key 未通过校验，请检查后重试。';
        await showDialog({
          title: 'API Key 校验失败',
          body: msg,
          buttons: [Dialog.okButton({ label: '知道了' })]
        });
      } else {
        // 校验通过后直接选中该模型
        this.setActiveModelId(model.id);
        this.renderModelButton();
        this.hideModelMenu();
      }
    } catch (err) {
      await showDialog({
        title: '设置失败',
        body: String(err),
        buttons: [Dialog.okButton({ label: '知道了' })]
      });
    }
  }

  private async openModelConfigDialog(model: IModelSpecPublic): Promise<void> {
    const wrapper = document.createElement('div');
    wrapper.className = 'deepanalyze-chat-model-config-dialog';

    const makeField = (label: string, input: HTMLElement): HTMLDivElement => {
      const row = document.createElement('div');
      row.className = 'deepanalyze-chat-model-config-row';
      const l = document.createElement('div');
      l.className = 'deepanalyze-chat-model-config-label';
      l.textContent = label;
      row.appendChild(l);
      row.appendChild(input);
      return row;
    };

    const baseUrlInput = document.createElement('input');
    baseUrlInput.className = 'deepanalyze-chat-model-key-input';
    baseUrlInput.placeholder = 'https://.../v1';
    baseUrlInput.value = String(model.base_url ?? '');

    const modelNameInput = document.createElement('input');
    modelNameInput.className = 'deepanalyze-chat-model-key-input';
    modelNameInput.placeholder = '模型名称（例如 gpt-4o-mini / deepseek-chat）';
    modelNameInput.value = String(model.model ?? '');

    const tempInput = document.createElement('input');
    tempInput.type = 'number';
    tempInput.step = '0.1';
    tempInput.min = '0';
    tempInput.max = '2';
    tempInput.className = 'deepanalyze-chat-model-key-input';
    tempInput.value =
      model.temperature === undefined || model.temperature === null ? '' : String(model.temperature);

    wrapper.appendChild(makeField('Base URL', baseUrlInput));
    wrapper.appendChild(makeField('Model', modelNameInput));
    wrapper.appendChild(makeField('温度 (temperature)', tempInput));

    let apiKeyInput: HTMLInputElement | null = null;
    if (model.requires_api_key) {
      apiKeyInput = document.createElement('input');
      apiKeyInput.type = 'password';
      apiKeyInput.className = 'deepanalyze-chat-model-key-input';
      apiKeyInput.placeholder = '留空则不修改已保存的 API Key';
      wrapper.appendChild(makeField('API Key', apiKeyInput));
    }

    const body = new Widget({ node: wrapper });
    const result = await showDialog({
      title: `配置 ${model.label || model.id}`,
      body,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: '保存' })]
    });
    if (!result.button.accept) {
      return;
    }

    const payload: any = {
      model_id: model.id,
      base_url: String(baseUrlInput.value ?? '').trim(),
      model: String(modelNameInput.value ?? '').trim()
    };
    const tempRaw = String(tempInput.value ?? '').trim();
    if (tempRaw) {
      const t = Number(tempRaw);
      if (!Number.isNaN(t)) {
        payload.temperature = t;
      }
    }
    const key = apiKeyInput ? String(apiKeyInput.value ?? '').trim() : '';
    if (key) {
      payload.api_key = key;
    }

    try {
      await upsertModelConfig(payload);
      await this.refreshModels();
      // 配置完成后保持当前选中不变
      this.hideModelMenu();
    } catch (err) {
      await showDialog({
        title: '保存失败',
        body: String(err),
        buttons: [Dialog.okButton({ label: '知道了' })]
      });
    }
  }

  private async openAddCustomModelDialog(): Promise<void> {
    const wrapper = document.createElement('div');
    wrapper.className = 'deepanalyze-chat-model-config-dialog';

    const makeField = (label: string, input: HTMLElement): HTMLDivElement => {
      const row = document.createElement('div');
      row.className = 'deepanalyze-chat-model-config-row';
      const l = document.createElement('div');
      l.className = 'deepanalyze-chat-model-config-label';
      l.textContent = label;
      row.appendChild(l);
      row.appendChild(input);
      return row;
    };

    const labelInput = document.createElement('input');
    labelInput.className = 'deepanalyze-chat-model-key-input';
    labelInput.placeholder = '展示名称（例如 My LLM）';

    const baseUrlInput = document.createElement('input');
    baseUrlInput.className = 'deepanalyze-chat-model-key-input';
    baseUrlInput.placeholder = 'https://.../v1';

    const modelNameInput = document.createElement('input');
    modelNameInput.className = 'deepanalyze-chat-model-key-input';
    modelNameInput.placeholder = '模型名称（例如 gpt-4o-mini / deepseek-chat）';

    const tempInput = document.createElement('input');
    tempInput.type = 'number';
    tempInput.step = '0.1';
    tempInput.min = '0';
    tempInput.max = '2';
    tempInput.className = 'deepanalyze-chat-model-key-input';
    tempInput.placeholder = '默认 0.4';

    const apiKeyInput = document.createElement('input');
    apiKeyInput.type = 'password';
    apiKeyInput.className = 'deepanalyze-chat-model-key-input';
    apiKeyInput.placeholder = 'API Key（可选，保存后会校验）';

    wrapper.appendChild(makeField('名称', labelInput));
    wrapper.appendChild(makeField('Base URL', baseUrlInput));
    wrapper.appendChild(makeField('Model', modelNameInput));
    wrapper.appendChild(makeField('温度 (temperature)', tempInput));
    wrapper.appendChild(makeField('API Key', apiKeyInput));

    const body = new Widget({ node: wrapper });
    const result = await showDialog({
      title: '添加自定义模型',
      body,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: '添加' })]
    });
    if (!result.button.accept) {
      return;
    }

    const payload: any = {
      label: String(labelInput.value ?? '').trim(),
      base_url: String(baseUrlInput.value ?? '').trim(),
      model: String(modelNameInput.value ?? '').trim()
    };
    const tempRaw = String(tempInput.value ?? '').trim();
    if (tempRaw) {
      const t = Number(tempRaw);
      if (!Number.isNaN(t)) {
        payload.temperature = t;
      }
    }
    const key = String(apiKeyInput.value ?? '').trim();
    if (key) {
      payload.api_key = key;
    }

    try {
      const created = await upsertModelConfig(payload);
      await this.refreshModels();
      if (created?.id) {
        this.setActiveModelId(created.id);
        this.renderModelButton();
      }
      this.hideModelMenu();
    } catch (err) {
      await showDialog({
        title: '添加失败',
        body: String(err),
        buttons: [Dialog.okButton({ label: '知道了' })]
      });
    }
  }

  private addMessage(
    role: ChatRole,
    text: string,
    options?: { persist?: boolean; before?: Element | null; turnId?: string }
  ): HTMLDivElement {
    const shouldScroll = this.isNearBottom();
    const item = document.createElement('div');
    item.className = `deepanalyze-chat-message deepanalyze-chat-message-${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'deepanalyze-chat-bubble';
    if (role === 'assistant') {
      bubble.dataset.assistantText = String(text ?? '');
      this.renderAssistantContent(bubble, text);
      const turnId = options?.turnId ?? this.currentTurnId ?? '';
      if (turnId) {
        bubble.dataset.deepanalyzeTurnId = turnId;
        const set = this.traceBubblesByTurnId.get(turnId) ?? new Set();
        set.add(bubble);
        this.traceBubblesByTurnId.set(turnId, set);
        if (!options?.turnId) {
          this.activeTraceTurnId = turnId;
        }
        this.renderTraceBarFromTurn(bubble, turnId);
      } else {
        if (!options?.turnId) {
          this.activeTraceTurnId = null;
        }
      }
    } else {
      bubble.textContent = text;
    }

    item.appendChild(bubble);
    const beforeNode = options?.before ?? null;
    if (beforeNode) {
      this.messagesNode.insertBefore(item, beforeNode);
    } else {
      this.messagesNode.appendChild(item);
    }
    this.scrollToBottomIfNeeded(shouldScroll);

    const persist = options?.persist === false ? false : true;
    if (persist) {
      const turnId = role === 'assistant' ? options?.turnId ?? this.currentTurnId ?? undefined : undefined;
      const trace = turnId ? this.buildTraceSnapshot(turnId) : undefined;
      this.history.push({ role, text, turnId, trace });
      this.persistHistory();
    }

    return bubble;
  }

  private ensureTaggedText(raw: string): string {
    const text = String(raw ?? '').trim();
    if (!text) {
      return '';
    }
    const hasKnownTags = /<(Analyze|Understand|Code|Answer)>\s*[\s\S]*?<\/\1>/i.test(text);
    if (hasKnownTags) {
      return text;
    }
    if (text.includes('<') && text.includes('>')) {
      return text;
    }
    return `<Answer>\n${text}\n</Answer>`;
  }

  private showWorkingIndicator(): void {
    if (this.workingMessageNode) {
      return;
    }

    const shouldScroll = this.isNearBottom();
    const item = document.createElement('div');
    item.className =
      'deepanalyze-chat-message deepanalyze-chat-message-assistant deepanalyze-chat-message-working';

    const bubble = document.createElement('div');
    bubble.className = 'deepanalyze-chat-bubble deepanalyze-chat-working-bubble';

    const indicator = document.createElement('div');
    indicator.className = 'deepanalyze-chat-working-indicator';

    const dot = document.createElement('span');
    dot.className = 'deepanalyze-chat-working-dot';
    indicator.appendChild(dot);

    const label = document.createElement('span');
    label.className = 'deepanalyze-chat-working-text';
    label.textContent = this.isAwaitingFeedback ? 'waiting for user choice' : 'working';
    indicator.appendChild(label);
    this.workingMessageLabelNode = label;

    if (this.isAwaitingFeedback) {
      item.classList.add('deepanalyze-chat-message-working-waiting');
    }

    bubble.appendChild(indicator);
    item.appendChild(bubble);
    this.messagesNode.appendChild(item);
    this.workingMessageNode = item;
    this.scrollToBottomIfNeeded(shouldScroll);
  }

  private finalizeWorkingIndicator(): void {
    const node = this.workingMessageNode;
    if (!node) {
      return;
    }
    node.classList.remove('deepanalyze-chat-message-working-waiting');
    node.classList.add('deepanalyze-chat-message-working-done');
    if (this.workingMessageLabelNode) {
      this.workingMessageLabelNode.textContent = 'done';
    }

    this.workingMessageNode = null;
    this.workingMessageLabelNode = null;
  }

  private isAsyncIterable(value: unknown): value is AsyncIterable<unknown> {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return typeof (value as any)?.[Symbol.asyncIterator] === 'function';
  }

  private applyToolResultChunk(chunk: IToolResultChunk): void {
    if (!chunk) {
      return;
    }

    const insertBefore = this.workingMessageNode;

    if (typeof chunk === 'string') {
      const text = chunk.trim();
      if (text) {
        this.addMessage('system', text, { before: insertBefore });
      }
      return;
    }

    if (typeof chunk !== 'object') {
      return;
    }

    const update = chunk as IToolResultUpdate;
    const systemText = String(update.system_text ?? '').trim();
    if (systemText) {
      this.addMessage('system', systemText, { before: insertBefore });
    }

    const trace = update.trace_update as any;
    if (trace && typeof trace === 'object') {
      const tag = String(trace.tag ?? '').trim();
      const path = String(trace.path ?? '').trim();
      const index = Number.isFinite(trace.index) ? Number(trace.index) : NaN;
      if (tag && path && Number.isFinite(index) && index >= 0) {
        this.applyTraceUpdateToTurn({ tag, path, index });
      }
    }

    const raws = Array.isArray(update.assistant_raw_updates)
      ? update.assistant_raw_updates
      : [];
    for (const raw of raws) {
      const normalized = this.fixUnclosedTags(this.ensureTaggedText(String(raw ?? '')));
      if (normalized.trim()) {
        // 不在 UI 中重复追加 assistant 消息（会导致 trace 链重复渲染）。
        // 仅保留首条链式标签显示，assistant 原文仍写入本地历史用于恢复。
        const turnId = this.activeTraceTurnId ?? this.currentTurnId ?? undefined;
        this.appendHistoryOnly('assistant', normalized, { hidden: true, turnId });
      }
    }
  }

  private appendHistoryOnly(
    role: ChatRole,
    text: string,
    options?: { turnId?: string; hidden?: boolean; trace?: IChatRecord['trace'] }
  ): void {
    const turnId = options?.turnId;
    const trace = options?.trace;
    const hidden = Boolean(options?.hidden);
    this.history.push({ role, text, turnId, hidden, trace });
    this.persistHistory();
  }

  private async loadMarked(): Promise<any> {
    if (this.markedModule) {
      return this.markedModule;
    }
    if (!this.markedModulePromise) {
      this.markedModulePromise = import('marked').then(m => {
        this.markedModule = m;
        this.markdownRenderer = this.buildMarkdownRenderer(m);
        return m;
      });
    }
    return this.markedModulePromise;
  }

  private async ensureMarkdownReady(): Promise<void> {
    try {
      await this.loadMarked();
      this.rerenderAssistantMessages();
    } catch {
      // ignore
    }
  }

  private rerenderAssistantMessages(): void {
    const nodes = this.messagesNode.querySelectorAll(
      '.deepanalyze-chat-message-assistant .deepanalyze-chat-bubble'
    );
    for (const node of Array.from(nodes)) {
      const el = node as HTMLDivElement;
      const text = el.dataset.assistantText ?? '';
      this.renderAssistantContent(el, text);
    }
  }

  private fixUnclosedTags(text: string): string {
    const s = String(text ?? '');
    const tags = ['Analyze', 'Understand', 'Code', 'Answer'];
    let fixed = s;
    for (const tag of tags) {
      const open = new RegExp(`<${tag}>`, 'i');
      const close = new RegExp(`</${tag}>`, 'i');
      if (open.test(fixed) && !close.test(fixed)) {
        fixed = `${fixed}\n</${tag}>`;
      }
    }
    return fixed;
  }

  private extractFencedCode(text: string): string {
    const raw = String(text ?? '').trim();
    const match = raw.match(/```(?:python)?\s*([\s\S]*?)```/i);
    if (match) {
      return String(match[1] ?? '').trim();
    }
    return raw;
  }

  private parseModules(text: string): Array<{ tag: string; content: string }> {
    const s = this.fixUnclosedTags(text);
    const pattern = /<(Analyze|Understand|Code|Answer)>([\s\S]*?)<\/\1>/gi;
    const modules: Array<{ tag: string; content: string }> = [];
    let match: RegExpExecArray | null = null;
    while ((match = pattern.exec(s))) {
      const rawTag = String(match[1] ?? '').trim();
      const tag = rawTag
        ? rawTag[0].toUpperCase() + rawTag.slice(1).toLowerCase()
        : rawTag;
      const content = String(match[2] ?? '').trim();
      if (!tag || !content) {
        continue;
      }
      modules.push({ tag, content });
    }
    return modules;
  }

  private escapeHtml(raw: string): string {
    const s = String(raw ?? '');
    return s
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  private buildMarkdownRenderer(markedModule: any): any {
    const renderer = new markedModule.Renderer();
    // 禁用原始 HTML，避免模型输出插入不安全标签。
    renderer.html = (token: any) => this.escapeHtml(String(token?.text ?? ''));
    renderer.image = (token: any) => this.escapeHtml(String(token?.text ?? ''));
    renderer.link = (token: any) => {
      const url = String(token?.href ?? '').trim();
      const label = this.escapeHtml(url || '(link)');
      const safe =
        url.startsWith('http://') ||
        url.startsWith('https://') ||
        url.startsWith('mailto:') ||
        url.startsWith('#');
      if (!safe) {
        return label;
      }
      const escaped = this.escapeHtml(url);
      return `<a href="${escaped}" target="_blank" rel="noreferrer noopener">${label}</a>`;
    };
    return renderer;
  }

  private renderMarkdownInto(host: HTMLElement, markdown: string): void {
    const md = String(markdown ?? '').trim();
    if (!md) {
      host.textContent = '';
      return;
    }

    if (!this.markedModule || !this.markdownRenderer) {
      host.textContent = md;
      return;
    }

    try {
      const html = this.markedModule.marked.parse(md, {
        gfm: true,
        breaks: true,
        renderer: this.markdownRenderer
      }) as unknown as string;
      host.innerHTML = String(html ?? '');
    } catch {
      host.textContent = md;
    }
  }

  private normalizeStreamTag(raw: string): StreamTag | null {
    const v = String(raw ?? '')
      .trim()
      .toLowerCase();
    if (v === 'analyze') {
      return 'Analyze';
    }
    if (v === 'understand') {
      return 'Understand';
    }
    if (v === 'code') {
      return 'Code';
    }
    if (v === 'answer') {
      return 'Answer';
    }
    return null;
  }

  private createStreamUi(turnId: string): IStreamTurnUI {
    const container = document.createElement('div');
    container.className = 'deepanalyze-chat-stream';

    const rootDetails = document.createElement('details');
    rootDetails.className = 'deepanalyze-chat-stream-root';
    rootDetails.open = true;

    const rootSummary = document.createElement('summary');
    rootSummary.className = 'deepanalyze-chat-stream-root-summary';

    const rootSpinner = document.createElement('span');
    rootSpinner.className = 'deepanalyze-chat-stream-spinner';
    rootSpinner.hidden = true;

    const rootCaret = document.createElement('span');
    rootCaret.className = 'deepanalyze-chat-stream-caret';
    rootCaret.hidden = false;

    const rootLabel = document.createElement('span');
    rootLabel.className = 'deepanalyze-chat-stream-root-label';
    rootLabel.textContent = 'Processing';

    rootSummary.appendChild(rootSpinner);
    rootSummary.appendChild(rootCaret);
    rootSummary.appendChild(rootLabel);
    rootDetails.appendChild(rootSummary);

    const innerNode = document.createElement('div');
    innerNode.className = 'deepanalyze-chat-stream-inner';
    rootDetails.appendChild(innerNode);

    const answerDetails = document.createElement('details');
    answerDetails.className = 'deepanalyze-chat-stream-answer-panel';
    answerDetails.open = true;
    answerDetails.hidden = true;

    const answerSummary = document.createElement('summary');
    answerSummary.className = 'deepanalyze-chat-stream-answer-summary';

    const answerSpinner = document.createElement('span');
    answerSpinner.className = 'deepanalyze-chat-stream-spinner';
    answerSpinner.hidden = true;

    const answerCaret = document.createElement('span');
    answerCaret.className = 'deepanalyze-chat-stream-caret';
    answerCaret.hidden = false;

    const answerLabel = document.createElement('span');
    answerLabel.className = 'deepanalyze-chat-stream-answer-label';
    answerLabel.textContent = 'Answer';

    answerSummary.appendChild(answerSpinner);
    answerSummary.appendChild(answerCaret);
    answerSummary.appendChild(answerLabel);
    answerDetails.appendChild(answerSummary);

    const answerContent = document.createElement('div');
    answerContent.className = 'deepanalyze-chat-stream-answer-content jp-RenderedMarkdown';
    answerDetails.appendChild(answerContent);

    container.appendChild(rootDetails);
    container.appendChild(answerDetails);

    return {
      turnId,
      container,
      rootDetails,
      rootSpinner,
      rootCaret,
      rootLabel,
      answerDetails,
      answerSpinner,
      answerCaret,
      answerLabel,
      answerContent,
      innerNode,
      blocks: [],
      activeBlock: null,
      inAnswer: false,
      answerText: '',
      buffer: '',
      countsByTag: new Map(),
      hasAnswer: false
    };
  }

  private ensureStreamUi(turnId: string, bubble: HTMLDivElement): IStreamTurnUI {
    const existing = this.streamUiByTurnId.get(turnId);
    if (existing) {
      if (existing.container.parentElement !== bubble) {
        bubble.appendChild(existing.container);
      }
      return existing;
    }
    const created = this.createStreamUi(turnId);
    this.streamUiByTurnId.set(turnId, created);
    bubble.appendChild(created.container);
    return created;
  }

  private setStreamRootRunning(ui: IStreamTurnUI, running: boolean): void {
    ui.rootSpinner.hidden = !running;
    ui.rootCaret.hidden = running;
    if (running) {
      ui.rootLabel.textContent = 'Processing';
    } else if (ui.hasAnswer) {
      ui.rootLabel.textContent = 'Finished work';
    } else {
      ui.rootLabel.textContent = 'Processing';
    }
  }

  private ensureAnswerPanelVisible(ui: IStreamTurnUI): void {
    if (ui.answerDetails.hidden) {
      ui.answerDetails.hidden = false;
    }
    if (!ui.answerDetails.open) {
      ui.answerDetails.open = true;
    }
  }

  private setAnswerRunning(ui: IStreamTurnUI, running: boolean): void {
    this.ensureAnswerPanelVisible(ui);
    ui.answerSpinner.hidden = !running;
    ui.answerCaret.hidden = running;
  }

  private ensureStreamBlock(ui: IStreamTurnUI, tag: StreamTag): IStreamBlockUI {
    const prev = ui.countsByTag.get(tag) ?? 0;
    const next = prev + 1;
    ui.countsByTag.set(tag, next);
    const label = next <= 1 ? tag : `${tag}(${next})`;

    const details = document.createElement('details');
    details.className = 'deepanalyze-chat-stream-block';
    details.open = true;

    const summary = document.createElement('summary');
    summary.className = 'deepanalyze-chat-stream-block-summary';

    const spinner = document.createElement('span');
    spinner.className = 'deepanalyze-chat-stream-spinner';
    spinner.hidden = false;

    const caret = document.createElement('span');
    caret.className = 'deepanalyze-chat-stream-caret';
    caret.hidden = true;

    const name = document.createElement('span');
    name.className = 'deepanalyze-chat-stream-block-label';
    name.textContent = label;

    summary.appendChild(spinner);
    summary.appendChild(caret);
    summary.appendChild(name);
    details.appendChild(summary);

    let content: HTMLElement;
    if (tag === 'Code') {
      const pre = document.createElement('pre');
      pre.className =
        'deepanalyze-chat-stream-block-content deepanalyze-chat-stream-block-content-code';
      const code = document.createElement('code');
      code.className = 'deepanalyze-chat-stream-code';
      pre.appendChild(code);
      details.appendChild(pre);
      content = code;
    } else {
      const host = document.createElement('div');
      host.className =
        'deepanalyze-chat-stream-block-content deepanalyze-chat-stream-block-content-markdown jp-RenderedMarkdown';
      details.appendChild(host);
      content = host;
    }

    ui.innerNode.appendChild(details);

    const block: IStreamBlockUI = {
      tag,
      label,
      details,
      spinner,
      caret,
      content,
      text: '',
      closed: false
    };
    ui.blocks.push(block);
    return block;
  }

  private closeStreamBlock(block: IStreamBlockUI): void {
    if (block.closed) {
      return;
    }
    block.closed = true;
    block.spinner.hidden = true;
    block.caret.hidden = false;
    block.details.open = false;
    block.details.classList.add('is-done');
  }

  private renderStreamMarkdown(host: HTMLElement, markdown: string): void {
    this.renderMarkdownInto(host, markdown);
  }

  private highlightPythonCodeHtml(code: string): string {
    const lines = String(code ?? '').replace(/\r\n/g, '\n').split('\n');
    const keywords = [
      'False',
      'None',
      'True',
      'and',
      'as',
      'assert',
      'async',
      'await',
      'break',
      'class',
      'continue',
      'def',
      'del',
      'elif',
      'else',
      'except',
      'finally',
      'for',
      'from',
      'global',
      'if',
      'import',
      'in',
      'is',
      'lambda',
      'nonlocal',
      'not',
      'or',
      'pass',
      'raise',
      'return',
      'try',
      'while',
      'with',
      'yield'
    ];
    const kw = new RegExp(`\\\\b(${keywords.join('|')})\\\\b`, 'g');

    const out: string[] = [];
    for (const rawLine of lines) {
      const idx = rawLine.indexOf('#');
      const head = idx >= 0 ? rawLine.slice(0, idx) : rawLine;
      const comment = idx >= 0 ? rawLine.slice(idx) : '';

      const escape = (s: string) => this.escapeHtml(s);
      const stringRe = /(\"([^\"\\\\]|\\\\.)*\"|'([^'\\\\]|\\\\.)*')/g;
      const bodyParts: string[] = [];
      let last = 0;
      for (const m of head.matchAll(stringRe)) {
        const i = typeof m.index === 'number' ? m.index : -1;
        if (i < 0) {
          continue;
        }
        const before = head.slice(last, i);
        if (before) {
          bodyParts.push(
            escape(before).replace(kw, '<span class=\"deepanalyze-code-keyword\">$1</span>')
          );
        }
        bodyParts.push(`<span class=\"deepanalyze-code-string\">${escape(m[0])}</span>`);
        last = i + m[0].length;
      }
      const tail = head.slice(last);
      if (tail) {
        bodyParts.push(escape(tail).replace(kw, '<span class=\"deepanalyze-code-keyword\">$1</span>'));
      }
      const body = bodyParts.join('');

      const commentHtml = comment
        ? `<span class=\"deepanalyze-code-comment\">${escape(comment)}</span>`
        : '';
      out.push(`${body}${commentHtml}`);
    }
    return out.join('\n');
  }

  private renderStreamCode(host: HTMLElement, code: string): void {
    host.innerHTML = this.highlightPythonCodeHtml(code);
  }

  private renderStreamBlockContent(block: IStreamBlockUI): void {
    if (block.tag === 'Code') {
      this.renderStreamCode(block.content, block.text);
      return;
    }
    this.renderStreamMarkdown(block.content, block.text);
  }

  private renderStreamAnswer(ui: IStreamTurnUI): void {
    this.ensureAnswerPanelVisible(ui);
    this.renderStreamMarkdown(ui.answerContent, ui.answerText);
  }

  private buildTranscriptFromStreamUi(ui: IStreamTurnUI): string {
    const parts: string[] = [];
    for (const block of ui.blocks) {
      const content = String(block.text ?? '').trimEnd();
      parts.push(`<${block.tag}>\n${content}\n</${block.tag}>`);
    }
    if (ui.hasAnswer || ui.answerText.trim()) {
      const content = String(ui.answerText ?? '').trimEnd();
      parts.push(`<Answer>\n${content}\n</Answer>`);
    }
    return parts.join('\n\n').trim();
  }

  private persistAssistantTranscriptFromUi(ui: IStreamTurnUI): void {
    const transcript = this.buildTranscriptFromStreamUi(ui);
    if (!transcript.trim()) {
      return;
    }
    for (let i = this.history.length - 1; i >= 0; i--) {
      const record = this.history[i];
      if (record.role !== 'assistant' || record.hidden) {
        continue;
      }
      if (record.turnId !== ui.turnId) {
        continue;
      }
      record.text = transcript;
      record.trace = this.buildTraceSnapshot(ui.turnId);
      this.persistHistory();
      return;
    }
  }

  private applyStreamDeltaToUi(ui: IStreamTurnUI, delta: string): void {
    ui.buffer += String(delta ?? '');

    const openTagRe = /<(Analyze|Understand|Code|Answer)>/i;
    const maxOpenTagLen = '<Understand>'.length;

    const appendToActive = (piece: string) => {
      if (!piece) {
        return;
      }
      if (ui.inAnswer) {
        ui.answerText += piece;
        this.renderStreamAnswer(ui);
        return;
      }
      if (ui.activeBlock) {
        ui.activeBlock.text += piece;
        this.renderStreamBlockContent(ui.activeBlock);
      }
    };

    const tryOpenFromBuffer = (): boolean => {
      const m = ui.buffer.match(openTagRe);
      if (!m || typeof m.index !== 'number') {
        return false;
      }

      const before = ui.buffer.slice(0, m.index);
      ui.buffer = ui.buffer.slice(m.index + String(m[0] ?? '').length);
      const tag = this.normalizeStreamTag(m[1]);
      if (!tag) {
        return false;
      }

      // 先把开标签前的内容归入“当前活跃区域”（如果没有活跃区域则丢弃空白）。
      if ((ui.inAnswer || ui.activeBlock) && before) {
        appendToActive(before);
      }

      // 开始新的块
      if (tag === 'Answer') {
        if (ui.activeBlock) {
          this.closeStreamBlock(ui.activeBlock);
          ui.activeBlock = null;
        }
        ui.inAnswer = true;
        ui.hasAnswer = true;
        this.ensureAnswerPanelVisible(ui);
        // 不创建内层下拉：Answer 直接渲染到外层区域
        return true;
      }

      if (ui.inAnswer) {
        ui.inAnswer = false;
      }
      if (ui.activeBlock) {
        this.closeStreamBlock(ui.activeBlock);
      }
      ui.activeBlock = this.ensureStreamBlock(ui, tag);
      return true;
    };

    while (true) {
      if (!ui.inAnswer && !ui.activeBlock) {
        if (!tryOpenFromBuffer()) {
          const keep = Math.max(0, maxOpenTagLen - 1);
          if (ui.buffer.length > keep) {
            ui.buffer = ui.buffer.slice(ui.buffer.length - keep);
          }
          break;
        }
        continue;
      }

      const closing = ui.inAnswer ? '</Answer>' : `</${ui.activeBlock?.tag}>`;
      const lower = ui.buffer.toLowerCase();
      const idxClose = closing ? lower.indexOf(closing.toLowerCase()) : -1;
      const openMatch = ui.buffer.match(openTagRe);
      const idxOpen = openMatch && typeof openMatch.index === 'number' ? openMatch.index : -1;

      // 容错：若下一个开标签先出现，按“隐式闭合当前区域”处理
      if (idxOpen >= 0 && (idxClose < 0 || idxOpen < idxClose)) {
        const piece = ui.buffer.slice(0, idxOpen);
        appendToActive(piece);
        ui.buffer = ui.buffer.slice(idxOpen);
        if (ui.inAnswer) {
          ui.inAnswer = false;
        } else if (ui.activeBlock) {
          const finished = ui.activeBlock;
          this.closeStreamBlock(finished);
          ui.activeBlock = null;
        }
        continue;
      }

      if (idxClose >= 0) {
        const piece = ui.buffer.slice(0, idxClose);
        appendToActive(piece);
        ui.buffer = ui.buffer.slice(idxClose + closing.length);
        if (ui.inAnswer) {
          ui.inAnswer = false;
        } else if (ui.activeBlock) {
          const finished = ui.activeBlock;
          this.closeStreamBlock(finished);
          ui.activeBlock = null;
        }
        continue;
      }

      // 无任何边界：流式追加，并保留可能构成边界的尾部
      const keep = Math.max(0, Math.max(closing.length - 1, maxOpenTagLen - 1));
      const safeLen = Math.max(0, ui.buffer.length - keep);
      const emit = ui.buffer.slice(0, safeLen);
      appendToActive(emit);
      ui.buffer = ui.buffer.slice(safeLen);
      break;
    }
  }

  private resolveActiveStreamUi(): IStreamTurnUI | null {
    const turnId = this.currentTurnId ?? this.activeTraceTurnId;
    if (!turnId) {
      return null;
    }
    const bubble = this.assistantBubbleByTurnId.get(turnId);
    if (!bubble) {
      return null;
    }
    return this.ensureStreamUi(turnId, bubble);
  }

  public startAssistantStreaming(): void {
    const ui = this.resolveActiveStreamUi();
    if (!ui) {
      return;
    }
    ui.rootDetails.open = true;
    this.setStreamRootRunning(ui, true);
  }

  public appendAssistantStreaming(delta: string): void {
    const ui = this.resolveActiveStreamUi();
    if (!ui) {
      return;
    }
    const shouldScroll = this.isNearBottom();
    this.applyStreamDeltaToUi(ui, delta);
    if (ui.inAnswer) {
      this.setAnswerRunning(ui, true);
      this.setStreamRootRunning(ui, false);
    } else {
      if (!ui.answerDetails.hidden) {
        ui.answerSpinner.hidden = true;
        ui.answerCaret.hidden = false;
        ui.answerDetails.open = true;
      }
      const processingRunning = Boolean(ui.activeBlock && !ui.activeBlock.closed);
      this.setStreamRootRunning(ui, processingRunning);
    }
    this.scrollToBottomIfNeeded(shouldScroll);
  }

  public finalizeAssistantStreaming(options?: { raw?: string; hasAnswer?: boolean }): void {
    const ui = this.resolveActiveStreamUi();
    if (!ui) {
      return;
    }
    const shouldScroll = this.isNearBottom();
    const raw = String(options?.raw ?? '');
    const hasAnswer =
      options?.hasAnswer === true || (/<Answer\b/i.test(raw) && /<\/Answer>/i.test(raw));
    if (ui.activeBlock) {
      this.closeStreamBlock(ui.activeBlock);
      ui.activeBlock = null;
    }
    ui.inAnswer = false;

    if (raw && ui.blocks.length === 0 && !ui.answerText.trim()) {
      ui.buffer = '';
      const modules = this.parseModules(raw);
      if (modules.length > 0) {
        for (const module of modules) {
          const tag = this.normalizeStreamTag(module.tag);
          if (!tag) {
            continue;
          }
          if (tag === 'Answer') {
            ui.hasAnswer = true;
            ui.answerText = String(module.content ?? '');
            this.renderStreamAnswer(ui);
            continue;
          }
          const block = this.ensureStreamBlock(ui, tag);
          block.text = String(module.content ?? '');
          this.renderStreamBlockContent(block);
          this.closeStreamBlock(block);
        }
      } else {
        ui.hasAnswer = true;
        ui.answerText = raw;
        this.renderStreamAnswer(ui);
      }
    }

    ui.hasAnswer = ui.hasAnswer || hasAnswer;
    this.setStreamRootRunning(ui, false);
    if (!ui.answerDetails.hidden) {
      ui.answerSpinner.hidden = true;
      ui.answerCaret.hidden = false;
      ui.answerDetails.open = true;
    }
    this.persistAssistantTranscriptFromUi(ui);
    this.scrollToBottomIfNeeded(shouldScroll);
  }

  private renderStaticAssistantBlocks(bubble: HTMLDivElement, text: string): void {
    const modules = this.parseModules(text);
    if (modules.length === 0) {
      return;
    }
    const ui = this.createStreamUi('static');
    const hasAnswer = modules.some(m => this.normalizeStreamTag(m.tag) === 'Answer');
    ui.hasAnswer = hasAnswer;
    ui.rootLabel.textContent = hasAnswer ? 'Finished work' : 'Processing';

    for (const module of modules) {
      const tag = this.normalizeStreamTag(module.tag);
      if (!tag) {
        continue;
      }
      if (tag === 'Answer') {
        ui.answerText = String(module.content ?? '');
        this.renderStreamAnswer(ui);
        continue;
      }
      const block = this.ensureStreamBlock(ui, tag);
      block.text = String(module.content ?? '');
      this.renderStreamBlockContent(block);
      this.closeStreamBlock(block);
    }

    bubble.appendChild(ui.container);
  }

  private renderAssistantContent(bubble: HTMLDivElement, text: string): void {
    while (bubble.firstChild) {
      bubble.removeChild(bubble.firstChild);
    }

    // 聊天区展示“链式标签 + 本轮生成过程（可折叠）”：
    // - 链式标签由前端执行 op 时的 trace_update 增量更新，以确保“继续”后的多轮也会接在一起。
    // - 生成过程来自模型输出的 <Analyze>/<Understand>/<Code>/<Answer> 块（支持流式增量展示）。
    const turnId = bubble.dataset.deepanalyzeTurnId ?? '';
    if (turnId) {
      this.renderTraceBarFromTurn(bubble, turnId);
      const stream = this.streamUiByTurnId.get(turnId);
      if (stream) {
        bubble.appendChild(stream.container);
        return;
      }
    }

    this.renderStaticAssistantBlocks(bubble, text);
  }

  private ensureTraceState(turnId: string): {
    items: Array<{ id: string; tag: string; label: string; path: string; index: number }>;
    activeId?: string;
    counts: Map<string, number>;
  } {
    const existing = this.traceStateByTurnId.get(turnId);
    if (existing) {
      return existing;
    }
    const created = { items: [], activeId: undefined, counts: new Map<string, number>() };
    this.traceStateByTurnId.set(turnId, created);
    return created;
  }

  private buildTraceSnapshot(turnId: string): IChatRecord['trace'] | undefined {
    const state = this.traceStateByTurnId.get(turnId);
    if (!state || state.items.length === 0) {
      return undefined;
    }
    return {
      items: state.items.map(it => ({
        id: it.id,
        tag: it.tag,
        label: it.label,
        path: it.path,
        index: it.index
      })),
      activeId: state.activeId
    };
  }

  private restoreTraceState(turnId: string, trace: NonNullable<IChatRecord['trace']>): void {
    const counts = new Map<string, number>();
    for (const item of trace.items) {
      counts.set(item.tag, (counts.get(item.tag) ?? 0) + 1);
    }
    this.traceStateByTurnId.set(turnId, {
      items: trace.items.map(it => ({ ...it })),
      activeId: trace.activeId ?? trace.items[trace.items.length - 1]?.id,
      counts
    });
  }

  private persistTraceSnapshotForTurn(turnId: string): void {
    const snapshot = this.buildTraceSnapshot(turnId);
    if (!snapshot) {
      return;
    }
    for (let i = this.history.length - 1; i >= 0; i--) {
      const record = this.history[i];
      if (record.role !== 'assistant' || record.hidden) {
        continue;
      }
      if (record.turnId === turnId) {
        record.trace = snapshot;
        this.persistHistory();
        return;
      }
    }
  }

  private applyTraceUpdateToTurn(update: { tag: string; path: string; index: number }): void {
    const turnId = this.activeTraceTurnId ?? this.currentTurnId;
    if (!turnId) {
      return;
    }

    const state = this.ensureTraceState(turnId);
    const prev = state.counts.get(update.tag) ?? 0;
    const next = prev + 1;
    state.counts.set(update.tag, next);

    const label = next <= 1 ? update.tag : `${update.tag}(${next})`;
    const id = `${update.tag}:${next}`;
    state.items.push({ id, tag: update.tag, label, path: update.path, index: update.index });
    state.activeId = id;
    this.persistTraceSnapshotForTurn(turnId);

    const bubbles = this.traceBubblesByTurnId.get(turnId);
    if (!bubbles || bubbles.size === 0) {
      return;
    }
    for (const bubble of bubbles) {
      this.renderTraceBarFromTurn(bubble, turnId);
    }
  }

  private renderTraceBarFromTurn(bubble: HTMLDivElement, turnId: string): void {
    const state = this.traceStateByTurnId.get(turnId);
    const existing = bubble.querySelector('.deepanalyze-chat-trace');
    existing?.parentElement?.removeChild(existing);

    if (!state || state.items.length === 0) {
      return;
    }

    const bar = document.createElement('div');
    bar.className = 'deepanalyze-chat-trace';

    state.items.forEach((item, i) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'deepanalyze-chat-trace-tag';
      btn.dataset.id = item.id;
      btn.textContent = item.label;
      btn.addEventListener('click', () => void this.handleTraceTagClick(turnId, item.id));
      bar.appendChild(btn);
      if (i < state.items.length - 1) {
        const sep = document.createElement('span');
        sep.className = 'deepanalyze-chat-trace-sep';
        sep.textContent = '→';
        bar.appendChild(sep);
      }
    });

    const stream = bubble.querySelector('.deepanalyze-chat-stream');
    if (stream && stream.parentElement === bubble) {
      bubble.insertBefore(bar, stream);
    } else {
      bubble.appendChild(bar);
    }
    this.applyTraceActiveToBubble(bubble, turnId);
  }

  private applyTraceActiveToBubble(bubble: HTMLDivElement, turnId: string): void {
    const state = this.traceStateByTurnId.get(turnId);
    const activeId = state?.activeId;
    if (!activeId) {
      return;
    }
    const buttons = bubble.querySelectorAll<HTMLButtonElement>('.deepanalyze-chat-trace-tag');
    buttons.forEach(btn => {
      const id = String(btn.dataset.id ?? '');
      btn.classList.toggle('deepanalyze-chat-trace-tag-active', id === activeId);
    });
  }

  private async handleTraceTagClick(turnId: string, id: string): Promise<void> {
    const state = this.traceStateByTurnId.get(turnId);
    const item = state?.items.find(it => it.id === id);
    if (!item) {
      return;
    }
    try {
      await this.onNavigateToCell?.(item.path, item.index);
    } catch {
      // ignore
    }
  }

  private isNearBottom(thresholdPx = 24): boolean {
    const el = this.messagesNode;
    const distance = el.scrollHeight - (el.scrollTop + el.clientHeight);
    return distance <= thresholdPx;
  }

  private scrollToBottomIfNeeded(shouldScroll: boolean): void {
    if (!shouldScroll) {
      return;
    }
    this.messagesNode.scrollTop = this.messagesNode.scrollHeight;
  }

  public setBusy(isBusy: boolean): void {
    this.isBusy = isBusy;
    this.syncControlState();
  }

  public setModelGenerating(isGenerating: boolean): void {
    this.isModelGenerating = isGenerating;
    this.syncControlState();
  }

  public setAwaitingFeedback(isAwaiting: boolean): void {
    this.isAwaitingFeedback = isAwaiting;
    this.updateWorkingStateClasses();
    this.syncControlState();
    this.updateWorkingIndicatorLabel();
  }

  public getAwaitingFeedback(): boolean {
    return this.isAwaitingFeedback;
  }

  public getAutoContinueEnabled(): boolean {
    try {
      const raw = window.localStorage.getItem(this.autoContinueKey);
      if (raw == null) {
        return false;
      }
      return raw === '1' || raw.toLowerCase() === 'true';
    } catch {
      return false;
    }
  }

  public setAutoContinueEnabled(enabled: boolean): void {
    try {
      window.localStorage.setItem(this.autoContinueKey, enabled ? '1' : '0');
    } catch {
      // ignore
    }

    if (this.autoToggleNode.checked !== enabled) {
      this.autoToggleNode.checked = enabled;
    }

    if (enabled && this.isAwaitingFeedback) {
      this.resolveAwaitDecision('continue');
    }
  }

  public waitForContinueOrAbort(): Promise<'continue' | 'abort'> {
    if (this.awaitingDecisionPromise) {
      return this.awaitingDecisionPromise;
    }

    this.setAwaitingFeedback(true);

    this.awaitingDecisionPromise = new Promise<'continue' | 'abort'>(resolve => {
      this.awaitingDecisionResolve = resolve;
    });

    if (this.getAutoContinueEnabled()) {
      queueMicrotask(() => this.resolveAwaitDecision('continue'));
    }

    return this.awaitingDecisionPromise;
  }

  private resolveAwaitDecision(value: 'continue' | 'abort'): void {
    const resolve = this.awaitingDecisionResolve;
    if (!resolve) {
      return;
    }
    this.awaitingDecisionResolve = null;
    const promise = this.awaitingDecisionPromise;
    this.awaitingDecisionPromise = null;

    this.setAwaitingFeedback(false);

    try {
      resolve(value);
    } finally {
      void promise;
    }
  }

  private updateWorkingIndicatorLabel(): void {
    if (!this.workingMessageLabelNode) {
      return;
    }
    this.workingMessageLabelNode.textContent = this.isAwaitingFeedback
      ? 'waiting for user choice'
      : 'working';
  }

  private updateWorkingStateClasses(): void {
    const node = this.workingMessageNode;
    if (!node) {
      return;
    }
    node.classList.toggle('deepanalyze-chat-message-working-waiting', this.isAwaitingFeedback);
  }

  private syncControlState(): void {
    const sendingLocked = this.isBusy;

    this.sendButtonNode.disabled = sendingLocked;
    this.inputNode.disabled = sendingLocked;
    this.sendButtonNode.textContent = this.isModelGenerating ? '发送中…' : '发送';

    const canControl = this.isAwaitingFeedback && !this.isModelGenerating;
    this.continueButtonNode.disabled = !canControl;
    this.abortButtonNode.disabled = !canControl;
  }

  private clearHistory(): void {
    this.history.length = 0;
    this.messagesNode.textContent = '';
    this.traceStateByTurnId.clear();
    this.traceBubblesByTurnId.clear();
    this.assistantBubbleByTurnId.clear();
    this.streamUiByTurnId.clear();
    try {
      window.localStorage.removeItem(this.historyKey);
    } catch {
      // ignore
    }
  }

  private async handleReset(): Promise<void> {
    if (this.isBusy) {
      return;
    }

    const bodyNode = document.createElement('div');
    bodyNode.className = 'deepanalyze-chat-reset-dialog';

    const text = document.createElement('div');
    text.textContent = '确认重置当前会话与对话历史吗？';
    bodyNode.appendChild(text);

    const label = document.createElement('label');
    label.style.display = 'flex';
    label.style.alignItems = 'center';
    label.style.gap = '8px';
    label.style.marginTop = '12px';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    label.appendChild(checkbox);

    const labelText = document.createElement('span');
    labelText.textContent = '同时清除 Notebook 结果（model_output / scratch）';
    label.appendChild(labelText);
    bodyNode.appendChild(label);

    const body = new Widget({ node: bodyNode });
    const result = await showDialog({
      title: '重置确认',
      body,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: '重置' })]
    });

    if (!result.button.accept) {
      return;
    }

      this.setBusy(true);
      try {
        this.setModelGenerating(true);
        const response = await sendChatMessage(
          '/reset',
          this.activeModelId || undefined,
          this.getPromptLang()
        );
      try {
        await this.onReset?.({ clearNotebooks: checkbox.checked });
      } catch {
        // ignore notebook clear failures
      }
      this.clearHistory();
      this.addMessage('assistant', response.reply || '已重置当前会话。');
    } catch (error) {
      this.addMessage('system', '重置失败（后端可能未启用）。');
      this.addMessage('system', String(error));
    } finally {
      this.setModelGenerating(false);
      this.setBusy(false);
      this.inputNode.focus();
    }
  }

  private async handleSend(): Promise<void> {
    if (this.isBusy) {
      return;
    }

    const raw = this.inputNode.value ?? '';
    const message = raw.trim();
    if (!message) {
      return;
    }

    this.inputNode.value = '';
    this.addMessage('user', message);
    this.showWorkingIndicator();

    this.setBusy(true);
    const turnId = String(Date.now());
    this.currentTurnId = turnId;
    try {
      const placeholderBubble = this.addMessage('assistant', '', {
        persist: false,
        before: this.workingMessageNode
      });
      this.assistantBubbleByTurnId.set(turnId, placeholderBubble);
      this.ensureStreamUi(turnId, placeholderBubble);
      this.startAssistantStreaming();

      await this.loadMarked();
      this.setModelGenerating(true);
      let response: IChatResponse | null = null;

      const tryStream = async (): Promise<IChatResponse> => {
        // 优先走流式：一方面更好的用户体验，另一方面可以驱动 `open.ts` 写 scratch 流式占位 cell。
        await this.onModelStream?.({ type: 'start', turnId });
        for await (const event of streamChatMessage(
          message,
          this.activeModelId || undefined,
          this.getPromptLang()
        )) {
          if (event.type === 'delta') {
            this.appendAssistantStreaming(event.delta);
            await this.onModelStream?.({ type: 'delta', turnId, delta: event.delta });
            continue;
          }
          if (event.type === 'final') {
            response = event.response;
            break;
          }
        }
        if (!response) {
          throw new Error('流式响应缺少 final');
        }
        try {
          const data = response.data as any;
          const raw =
            typeof data?.raw === 'string'
              ? String(data.raw)
              : String(response.reply ?? '');
          const awaitFeedback = Boolean(data?.await_feedback);
          const hasAnswer = /<Answer\b/i.test(raw) && /<\/Answer>/i.test(raw);
          this.finalizeAssistantStreaming({ raw, hasAnswer });
          await this.onModelStream?.({
            type: 'final',
            turnId,
            awaitFeedback,
            hasAnswer,
            raw
          });
        } catch {
          // ignore
        }
        await this.onModelStream?.({ type: 'end', turnId });
        return response;
      };

      try {
        response = await tryStream();
      } catch (error) {
        // 流式失败时回退到非流式，并把失败信息上报给后端日志接口，便于定位 SSE/vLLM 兼容问题。
        await this.onModelStream?.({ type: 'error', turnId, error: String(error) });
        try {
          void sendFrontendLog({
            session_id: getDeepAnalyzeItem('sessionId').trim() || undefined,
            message: 'stream_chat_failed',
            logs: JSON.stringify(
              {
                turnId,
                error: String(error),
                errorType: (error as any)?.name,
                status: (error as any)?.response?.status,
                statusText: (error as any)?.response?.statusText
              },
              null,
              2
            )
          });
        } catch {
          // ignore
        }
        response = await sendChatMessage(message, this.activeModelId || undefined, this.getPromptLang());
      }

      this.setModelGenerating(false);

      const data = response.data as any;
      const raw = typeof data?.raw === 'string' ? String(data.raw) : '';
      const assistantText = this.fixUnclosedTags(
        this.ensureTaggedText(raw.trim() ? raw : String(response.reply ?? ''))
      );
      placeholderBubble.dataset.assistantText = assistantText.trim()
        ? assistantText
        : '<Answer>\n\n</Answer>';
      this.appendHistoryOnly('assistant', placeholderBubble.dataset.assistantText, {
        turnId,
        trace: this.buildTraceSnapshot(turnId)
      });
      this.finalizeAssistantStreaming({ raw: placeholderBubble.dataset.assistantText });

      if (response.data) {
        try {
          const result = await this.onToolResult?.(response.data);
          if (this.isAsyncIterable(result)) {
            for await (const chunk of result) {
              this.applyToolResultChunk(chunk as IToolResultChunk);
            }
          } else {
            this.applyToolResultChunk(result as IToolResultChunk);
          }
        } catch {
          // Ignore UI-side sync errors.
        }
      }
    } catch (error) {
      const bubble = this.assistantBubbleByTurnId.get(turnId);
      if (bubble) {
        bubble.dataset.assistantText = this.ensureTaggedText('请求失败（后端可能未启用）。');
        this.appendHistoryOnly('assistant', bubble.dataset.assistantText, { turnId });
        this.finalizeAssistantStreaming({ raw: bubble.dataset.assistantText, hasAnswer: true });
      } else {
        this.addMessage('assistant', this.ensureTaggedText('请求失败（后端可能未启用）。'), {
          before: this.workingMessageNode
        });
      }
      this.addMessage('system', String(error), { before: this.workingMessageNode });
    } finally {
      this.setAwaitingFeedback(false);
      this.finalizeWorkingIndicator();
      this.setModelGenerating(false);
      this.setBusy(false);
      this.assistantBubbleByTurnId.delete(turnId);
      this.currentTurnId = null;
      this.inputNode.focus();
    }
  }
}
