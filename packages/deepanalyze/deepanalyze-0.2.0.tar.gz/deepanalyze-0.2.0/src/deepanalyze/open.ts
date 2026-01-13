import { JupyterFrontEnd } from '@jupyterlab/application';
import { ILabShell } from '@jupyterlab/application';
import { Dialog, showDialog, showErrorMessage } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { PathExt } from '@jupyterlab/coreutils';
import { Contents } from '@jupyterlab/services';
import { NotebookActions } from '@jupyterlab/notebook';
import { DisposableDelegate } from '@lumino/disposable';
import { Widget } from '@lumino/widgets';

import { DeepAnalyzeChatPanel } from './chatPanel';
import { sendAgentFeedback, sendFrontendLog, streamAgentFeedback } from './api';
import { getDeepAnalyzeSettings } from './settings';
import { getDeepAnalyzeItem, removeDeepAnalyzeItem, setDeepAnalyzeItem } from './storage';
import {
  ensureDirectoryPath,
  ensureNamedWorkspace,
  listWorkspaces,
  sanitizeWorkspaceName
} from './workspace';

/**
 * DeepAnalyze 前端编排器（核心文件）。
 *
 * 主要职责：
 * 1) 打开/创建工作区与两个 notebook（scratch + model-output）
 * 2) 执行后端下发的 `frontend_ops`（直接操作 NotebookPanel / sharedModel）
 * 3) 处理回环（执行 code cell -> 汇总输出 -> 调用 feedback 接口 -> 继续执行下一轮 ops）
 * 4) 流式体验：在 scratch 末尾插入 raw cell 作为“生成中占位”，随 SSE delta 增量更新
 */
interface IDeepAnalyzeSession {
  readonly previousBrowserPath: string;
  readonly disposables: DisposableDelegate[];
}

let activeSession: IDeepAnalyzeSession | null = null;

// 工作区根目录的约定：
// - Contents API 使用“server root 相对路径”，不是 OS 绝对路径
// - 历史版本可能落在 legacy 前缀下，这里做兼容映射
const PREFERRED_WORKSPACES_ROOT = 'DeepAnalyze/workspaces';
const LEGACY_WORKSPACES_ROOT = 'jupyter/deepanalyze/DeepAnalyze/workspaces';

const CONFIGURED_WORKSPACES_ROOT_DEFAULT = PREFERRED_WORKSPACES_ROOT;

function configuredWorkspacesRootRaw(): string {
  const settings = getDeepAnalyzeSettings();
  const raw = String(settings.workspacesRoot ?? CONFIGURED_WORKSPACES_ROOT_DEFAULT).trim();

  // 这里主要做“尽量把用户输入的路径规范化为 Contents 可用的 server-root 相对路径”。
  // The JupyterLab Contents API uses paths relative to the server root, not OS absolute paths.
  // If user provides an absolute filesystem-looking path, try to recover a relative suffix.
  const normalized = raw.replace(/\\/g, '/').replace(/^\/+/, '').replace(/\/+$/, '');
  const firstSlash = normalized.indexOf('/');
  const prefix = firstSlash >= 0 ? normalized.slice(0, firstSlash) : normalized;
  if (prefix.includes(':')) {
    return normalized;
  }

  if (!normalized) {
    return '';
  }

  if (normalized === LEGACY_WORKSPACES_ROOT) {
    return PREFERRED_WORKSPACES_ROOT;
  }

  // If it is already a server-root relative path, keep it as-is (except legacy mapping above).
  if (normalized.startsWith('jupyter/deepanalyze/') || normalized.startsWith('DeepAnalyze/')) {
    return normalized;
  }

  // For OS absolute paths, fall back to the preferred contents-relative suffix.
  if (
    normalized.endsWith(`/${PREFERRED_WORKSPACES_ROOT}`) ||
    normalized.endsWith(PREFERRED_WORKSPACES_ROOT)
  ) {
    return PREFERRED_WORKSPACES_ROOT;
  }

  if (
    normalized.endsWith(`/${LEGACY_WORKSPACES_ROOT}`) ||
    normalized.endsWith(LEGACY_WORKSPACES_ROOT)
  ) {
    return PREFERRED_WORKSPACES_ROOT;
  }

  return normalized;
}

function resolveWorkspacesRoot(
  _contents: Contents.IManager,
  _browser: IDefaultFileBrowser,
  configured: string
): string {
  const trimmed = String(configured ?? '').trim();
  if (!trimmed) {
    return CONFIGURED_WORKSPACES_ROOT_DEFAULT;
  }

  const normalized = trimmed.replace(/\\/g, '/').replace(/^\/+/, '');

  // If it looks like a contents "absolute" path with a drive prefix (e.g. "home:..."),
  // do not re-resolve it.
  const firstSlash = normalized.indexOf('/');
  const prefix = firstSlash >= 0 ? normalized.slice(0, firstSlash) : normalized;
  if (prefix.includes(':')) {
    return normalized;
  }

  // Prefer server-root relative paths for workspaces (do not force the file browser drive).
  // If caller provides a drive-prefixed path, keep it as-is.
  return normalized;
}

function toBrowserCdPath(contents: Contents.IManager, path: string): string {
  const local = contents.localPath(path);
  const normalized = String(local ?? '').replace(/^\/+/, '');
  return normalized ? `/${normalized}` : '/';
}

function toContentsPath(contents: Contents.IManager, browserPath: string): string {
  const local = contents.localPath(browserPath);
  return String(local ?? '').replace(/^\/+/, '');
}

function getOrCreateDeepAnalyzeSessionId(): string {
  const existing = getDeepAnalyzeItem('sessionId');
  if (existing && String(existing).trim()) {
    return String(existing).trim();
  }

  let created = '';
  try {
    created = (window.crypto as any)?.randomUUID?.() ?? '';
  } catch {
    created = '';
  }
  if (!created) {
    created = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  setDeepAnalyzeItem('sessionId', created);
  return created;
}

async function safeFileBrowserCd(
  contents: Contents.IManager,
  browser: IDefaultFileBrowser,
  candidates: string[]
): Promise<void> {
  for (const candidate of candidates) {
    const value = String(candidate ?? '').trim();
    if (!value) {
      continue;
    }

    try {
      const contentPath = toContentsPath(contents, value);
      if (contentPath) {
        const model = await contents.get(contentPath, { content: false });
        if (model.type !== 'directory') {
          continue;
        }
      }

      const cdValue = value.startsWith('/') || value.includes(':') ? value : `/${value}`;
      await browser.model.cd(cdValue);
      return;
    } catch {
      // Try next.
    }
  }
}

async function cdFileBrowserToDirectory(
  contents: Contents.IManager,
  browser: IDefaultFileBrowser,
  targetDir: string
): Promise<boolean> {
  const cdPath = toBrowserCdPath(contents, targetDir);
  const resolved = contents.resolvePath(browser.model.path || '/', cdPath);

  try {
    const model = await contents.get(resolved, { content: false });
    if (model.type !== 'directory') {
      return false;
    }
  } catch {
    return false;
  }

  await browser.model.cd(cdPath);
  return true;
}

function installFileBrowserRootRestriction(
  contents: Contents.IManager,
  defaultBrowser: IDefaultFileBrowser,
  rootPath: string
): DisposableDelegate {
  const model = defaultBrowser.model;
  let isRedirecting = false;

  const rootLocal = String(contents.localPath(rootPath) ?? '').replace(/^\/+/, '');

  const isAllowed = (path: string): boolean => {
    const currentLocal = String(contents.localPath(path) ?? '').replace(/^\/+/, '');
    if (!currentLocal) {
      return false;
    }
    return currentLocal === rootLocal || currentLocal.startsWith(`${rootLocal}/`);
  };

  const handler = () => {
    if (isRedirecting) {
      return;
    }

    if (isAllowed(model.path)) {
      return;
    }

    isRedirecting = true;
    void model.cd(toBrowserCdPath(contents, rootPath)).finally(() => {
      isRedirecting = false;
    });
  };

  model.pathChanged.connect(handler);

  return new DisposableDelegate(() => {
    model.pathChanged.disconnect(handler);
  });
}

async function createNewNotebook(
  docManager: IDocumentManager,
  workspaceDir: string,
  refWidgetId?: string
): Promise<Widget | null> {
  try {
    const model = await docManager.newUntitled({ path: workspaceDir, type: 'notebook' });
    const openOptions = refWidgetId
      ? { mode: 'tab-after' as const, ref: refWidgetId }
      : undefined;
    return docManager.openOrReveal(model.path, undefined, undefined, openOptions) ?? null;
  } catch (error) {
    void showErrorMessage('DeepAnalyze', `新建 Notebook 失败：${error}`);
    return null;
  }
}

function installMainAreaAddButtonClickInterceptor(
  app: JupyterFrontEnd,
  docManager: IDocumentManager,
  workspaceDir: string
): DisposableDelegate {
  const labShell = app.shell as unknown as ILabShell;

  const getRefIdFromAddButton = (button: HTMLElement): string | undefined => {
    const dockTabBar =
      button.closest('.lm-DockPanel-tabBar') ?? button.closest('.jp-DockPanel-tabBar');
    if (!dockTabBar) {
      return labShell.currentWidget?.id ?? undefined;
    }

    const currentTab = dockTabBar.querySelector(
      '.lm-TabBar-tab.lm-mod-current'
    ) as HTMLElement | null;
    const refId = currentTab?.dataset?.id;
    return refId || (labShell.currentWidget?.id ?? undefined);
  };

  const shouldHandle = (target: HTMLElement | null): HTMLElement | null => {
    if (!target) {
      return null;
    }
    const button = target.closest('.lm-TabBar-addButton') as HTMLElement | null;
    if (!button) {
      return null;
    }
    if (
      !button.closest('.lm-DockPanel-tabBar') &&
      !button.closest('.jp-DockPanel-tabBar')
    ) {
      return null;
    }
    return button;
  };

  const pointerHandler = (event: PointerEvent) => {
    const button = shouldHandle(event.target as HTMLElement | null);
    if (!button) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (event as any).stopImmediatePropagation?.();

    const refId = getRefIdFromAddButton(button);
    void createNewNotebook(docManager, workspaceDir, refId);
  };

  const keyHandler = (event: KeyboardEvent) => {
    const target = event.target as HTMLElement | null;
    if (!target) {
      return;
    }
    const button = shouldHandle(target);
    if (!button) {
      return;
    }
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }

    event.preventDefault();
    event.stopPropagation();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (event as any).stopImmediatePropagation?.();

    const refId = getRefIdFromAddButton(button);
    void createNewNotebook(docManager, workspaceDir, refId);
  };

  // TabBar emits `addRequested` on document `pointerup` (capture). Intercept it early.
  document.addEventListener('pointerup', pointerHandler, true);
  document.addEventListener('keydown', keyHandler, true);

  return new DisposableDelegate(() => {
    document.removeEventListener('pointerup', pointerHandler, true);
    document.removeEventListener('keydown', keyHandler, true);
  });
}

async function promptWorkspaceDir(
  contents: Contents.IManager,
  workspacesRoot: string
): Promise<string | null> {
  const workspaces = await listWorkspaces(contents, workspacesRoot);

  const body = document.createElement('div');
  body.className = 'deepanalyze-workspace-dialog';

  const intro = document.createElement('div');
  intro.textContent = `请选择一个工作区，或新建工作区（目录会创建在 ${workspacesRoot} 下）。`;
  body.appendChild(intro);

  const modeLabel = document.createElement('label');
  modeLabel.textContent = '模式';
  modeLabel.style.display = 'block';
  modeLabel.style.marginTop = '10px';
  body.appendChild(modeLabel);

  const modeSelect = document.createElement('select');
  modeSelect.style.width = '100%';
  modeSelect.style.marginTop = '6px';
  const modeExistingOption = document.createElement('option');
  modeExistingOption.value = 'existing';
  modeExistingOption.textContent = '使用已有工作区';
  const modeNewOption = document.createElement('option');
  modeNewOption.value = 'new';
  modeNewOption.textContent = '新建工作区';
  modeSelect.appendChild(modeExistingOption);
  modeSelect.appendChild(modeNewOption);
  body.appendChild(modeSelect);

  const existingSelect = document.createElement('select');
  existingSelect.style.width = '100%';
  existingSelect.style.marginTop = '6px';
  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = workspaces.length ? '请选择…' : '暂无可用工作区';
  existingSelect.appendChild(placeholder);
  for (const name of workspaces) {
    const option = document.createElement('option');
    option.value = name;
    option.textContent = name;
    existingSelect.appendChild(option);
  }
  body.appendChild(existingSelect);

  const newInput = document.createElement('input');
  newInput.type = 'text';
  newInput.placeholder = '输入工作区名字（将作为子目录名）';
  newInput.style.width = '100%';
  newInput.style.marginTop = '6px';
  body.appendChild(newInput);

  const update = () => {
    const mode = String(modeSelect.value ?? 'existing');
    existingSelect.disabled = mode !== 'existing';
    newInput.disabled = mode !== 'new';
  };

  if (workspaces.length) {
    modeSelect.value = 'existing';
  } else {
    modeSelect.value = 'new';
  }
  update();

  modeSelect.addEventListener('change', update);

  for (;;) {
    const result = await showDialog({
      title: 'DeepAnalyze 工作区',
      body: new Widget({ node: body }),
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: '进入' })]
    });

    if (!result.button.accept) {
      return null;
    }

    if (String(modeSelect.value ?? 'existing') === 'existing') {
      const selected = String(existingSelect.value ?? '').trim();
      if (!selected) {
        await showErrorMessage('DeepAnalyze', '请选择一个已有工作区。');
        continue;
      }
      const target = PathExt.join(workspacesRoot, selected);
      try {
        const model = await contents.get(target, { content: false });
        if (model.type !== 'directory') {
          await showErrorMessage('DeepAnalyze', '所选工作区不是目录。');
          continue;
        }
      } catch {
        await showErrorMessage('DeepAnalyze', '所选工作区不存在或不可访问。');
        continue;
      }
      return target;
    }

    const rawName = String(newInput.value ?? '');
    const name = sanitizeWorkspaceName(rawName);
    if (!name) {
      await showErrorMessage('DeepAnalyze', '请输入工作区名字。');
      continue;
    }
    await ensureNamedWorkspace(contents, workspacesRoot, name);
    return PathExt.join(workspacesRoot, name);
  }
}

async function createNotebookFile(
  contents: Contents.IManager,
  docManager: IDocumentManager,
  directory: string,
  preferredName: string
): Promise<string> {
  const targetPath = PathExt.join(directory, preferredName);

  try {
    const existing = await contents.get(targetPath, { content: false });
    if (existing.type === 'directory') {
      throw new Error(`目标路径是目录：${targetPath}`);
    }
    return targetPath;
  } catch {
    // Not found; proceed to create.
  }

  const model = await docManager.newUntitled({ path: directory, type: 'notebook' });

  try {
    const renamed = await docManager.rename(model.path, targetPath);
    return renamed.path;
  } catch {
    try {
      await contents.get(targetPath, { content: false });
      await contents.delete(model.path);
      return targetPath;
    } catch {
      // Non-fatal.
    }
    return model.path;
  }
}

export async function openDeepAnalyze(
  app: JupyterFrontEnd,
  docManager: IDocumentManager,
  defaultBrowser: IDefaultFileBrowser,
  options?: { workspaceDir?: string; skipPrompt?: boolean }
): Promise<Widget | null> {
  const { contents } = app.serviceManager;

  await defaultBrowser.model.restored;

  activeSession?.disposables.forEach(disposable => disposable.dispose());
  activeSession = null;

  const previousBrowserPath = defaultBrowser.model.path ?? '';
  let workspacesRoot = '';
  let rootPath = '';
  let lastError: unknown = null;

  let preselectedWorkspaceDir = String(options?.workspaceDir ?? '').trim();
  if (preselectedWorkspaceDir) {
    workspacesRoot = PathExt.dirname(preselectedWorkspaceDir);
    rootPath = PathExt.dirname(workspacesRoot);
    try {
      const rootModel = await contents.get(rootPath, { content: false });
      if (rootModel.type !== 'directory') {
        throw new Error(`"${rootPath}" 不是目录`);
      }
      const wsRootModel = await contents.get(workspacesRoot, { content: false });
      if (wsRootModel.type !== 'directory') {
        throw new Error(`"${workspacesRoot}" 不是目录`);
      }
      const wsModel = await contents.get(preselectedWorkspaceDir, { content: false });
      if (wsModel.type !== 'directory') {
        throw new Error(`"${preselectedWorkspaceDir}" 不是目录`);
      }
      lastError = null;
    } catch (error) {
      lastError = error;
      workspacesRoot = '';
      rootPath = '';
      preselectedWorkspaceDir = '';
    }
  } else {
    const configuredRaw = configuredWorkspacesRootRaw();
    const primaryRawCandidates = [PREFERRED_WORKSPACES_ROOT, configuredRaw];
    const uniquePrimaryRawCandidates = Array.from(
      new Set(primaryRawCandidates.map(value => String(value ?? '').trim()).filter(Boolean))
    );

    const legacyRawCandidates = [LEGACY_WORKSPACES_ROOT];
    const uniqueRawCandidates = Array.from(
      new Set([...uniquePrimaryRawCandidates, ...legacyRawCandidates])
    );

    const resolvedPrimaryCandidates = uniquePrimaryRawCandidates.map(raw => {
      return resolveWorkspacesRoot(contents, defaultBrowser, raw);
    });

    for (const resolved of resolvedPrimaryCandidates) {
      const parent = PathExt.dirname(resolved);
      try {
        const model = await contents.get(resolved, { content: false });
        if (model.type !== 'directory') {
          throw new Error(`"${resolved}" 不是目录`);
        }
        const parentModel = await contents.get(parent, { content: false });
        if (parentModel.type !== 'directory') {
          throw new Error(`"${parent}" 不是目录`);
        }
        workspacesRoot = resolved;
        rootPath = parent;
        lastError = null;
        break;
      } catch (error) {
        lastError = error;
      }
    }

    if (!workspacesRoot) {
      // None exists yet; create the preferred default root.
      const resolved =
        resolvedPrimaryCandidates[0] ??
        resolveWorkspacesRoot(contents, defaultBrowser, CONFIGURED_WORKSPACES_ROOT_DEFAULT);
      const parent = PathExt.dirname(resolved);
      try {
        await ensureDirectoryPath(contents, resolved);
        const model = await contents.get(resolved, { content: false });
        if (model.type !== 'directory') {
          throw new Error(`"${resolved}" 不是目录`);
        }
        const parentModel = await contents.get(parent, { content: false });
        if (parentModel.type !== 'directory') {
          throw new Error(`"${parent}" 不是目录`);
        }
        workspacesRoot = resolved;
        rootPath = parent;
      } catch (error) {
        lastError = error;
      }
    }

    if (!workspacesRoot) {
      const resolvedLegacyCandidates = legacyRawCandidates.map(raw => {
        return resolveWorkspacesRoot(contents, defaultBrowser, raw);
      });

      for (const resolved of resolvedLegacyCandidates) {
        const parent = PathExt.dirname(resolved);
        try {
          const model = await contents.get(resolved, { content: false });
          if (model.type !== 'directory') {
            throw new Error(`"${resolved}" 不是目录`);
          }
          const parentModel = await contents.get(parent, { content: false });
          if (parentModel.type !== 'directory') {
            throw new Error(`"${parent}" 不是目录`);
          }
          workspacesRoot = resolved;
          rootPath = parent;
          lastError = null;
          break;
        } catch (error) {
          lastError = error;
        }
      }
    }

    if (!workspacesRoot) {
      await showErrorMessage(
        'DeepAnalyze',
        `无法初始化工作区父目录（候选：${uniqueRawCandidates.join(' , ')}）：${lastError ?? '未知错误'}`
      );
      return null;
    }
  }

  const rootRestriction = installFileBrowserRootRestriction(contents, defaultBrowser, rootPath);

  if (!(await cdFileBrowserToDirectory(contents, defaultBrowser, rootPath))) {
    rootRestriction.dispose();
    await showErrorMessage('DeepAnalyze', `无法进入目录: ${rootPath}`);
    return null;
  }

  const workspaceDir =
    preselectedWorkspaceDir || (await promptWorkspaceDir(contents, workspacesRoot));
  if (!workspaceDir) {
    rootRestriction.dispose();
    await safeFileBrowserCd(contents, defaultBrowser, [
      previousBrowserPath,
      toBrowserCdPath(contents, rootPath),
      '/'
    ]);
    return null;
  }

  const instanceId = Math.random().toString(16).slice(2, 10);

  if (!(await cdFileBrowserToDirectory(contents, defaultBrowser, workspaceDir))) {
    rootRestriction.dispose();
    await showErrorMessage('DeepAnalyze', `无法进入工作区目录: ${workspaceDir}`);
    return null;
  }

  const outputNotebookPath = await createNotebookFile(
    contents,
    docManager,
    workspaceDir,
    'model-output.ipynb'
  );
  const scratchNotebookPath = await createNotebookFile(
    contents,
    docManager,
    workspaceDir,
    'scratch.ipynb'
  );

  getOrCreateDeepAnalyzeSessionId();
  setDeepAnalyzeItem('activeWorkspaceDir', workspaceDir);
  setDeepAnalyzeItem('activeOutputPath', outputNotebookPath);
  setDeepAnalyzeItem('activeScratchPath', scratchNotebookPath);

  const outputWidget = docManager.openOrReveal(outputNotebookPath);
  if (!outputWidget) {
    rootRestriction.dispose();
    await showErrorMessage('DeepAnalyze', '无法打开模型输出 Notebook。');
    return null;
  }
  outputWidget.title.closable = false;

  const ensureInMainArea = (widget: Widget) => {
    try {
      app.shell.add(widget, 'main');
    } catch {
      // ignore
    }
  };

  ensureInMainArea(outputWidget);
  app.shell.activateById(outputWidget.id);

  const ensureNotebookPanel = async (path: string) => {
    const existing = docManager.findWidget(path) ?? docManager.openOrReveal(path);
    if (!existing) {
      throw new Error(`无法打开文档：${path}`);
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const context = (existing as any).context;
    if (context?.ready) {
      await context.ready;
    }
    return existing as any;
  };

  let chatWidget: Widget | null = null;
  let chatPanel: DeepAnalyzeChatPanel | null = null;
  let restoreAddButtonInterceptor: DisposableDelegate | null = null;
  try {
    type StreamingScratchState = {
      path: string;
      index: number;
      content: string;
      flushHandle: number | null;
      lastFlush: number;
      status: 'streaming' | 'waiting' | 'error' | 'done';
      panel: any | null;
      notebook: any | null;
      sharedModel: any | null;
      sharedCell: any | null;
      cellType: 'raw';
    };

    // scratch 的“流式占位 cell”状态：用于把 SSE delta 实时展示在 notebook 中。
    let streamingScratch: StreamingScratchState | null = null;
    const STREAM_FLUSH_MS = 80;

    const renderStreamingText = (content: string, status: StreamingScratchState['status']) => {
      const title =
        status === 'error'
          ? '[Streaming] 发生错误'
          : status === 'done'
            ? '[Streaming] 完成'
            : status === 'waiting'
              ? '[Streaming] 等待执行/回环…'
              : '[Streaming] 生成中…';
      const body = String(content ?? '');
      return `${title}\n\n${body}`;
    };

    const setCellSource = (notebook: any, sharedModel: any, index: number, source: string) => {
      const cell = notebook.widgets?.[index];
      if (cell?.model?.sharedModel?.setSource) {
        cell.model.sharedModel.setSource(source);
        return;
      }
      const sharedCell = sharedModel.getCell?.(index);
      sharedCell?.setSource?.(source);
    };

    const setCellLock = (notebook: any, index: number, locked: boolean) => {
      const cell = notebook?.widgets?.[index];
      const meta = cell?.model?.metadata;
      if (!meta?.set) {
        return;
      }
      const editable = locked ? false : true;
      try {
        meta.set('editable', editable);
      } catch {
        // ignore
      }
      try {
        meta.set('deletable', editable);
      } catch {
        // ignore
      }
    };

    const finalizeStreamingScratchCell = async (
      status: StreamingScratchState['status'],
      options: { unlock: boolean }
    ) => {
      const state = streamingScratch;
      if (!state) {
        return;
      }
      if (state.flushHandle != null) {
        window.clearTimeout(state.flushHandle);
      }

      try {
        const panel: any = state.panel ?? (await ensureNotebookPanel(state.path));
        const notebook: any = state.notebook ?? panel?.content;
        const sharedModel: any = state.sharedModel ?? notebook?.model?.sharedModel;
        if (!notebook?.model?.sharedModel || !sharedModel) {
          return;
        }
        const placeholderIndex =
          state.sharedCell && Array.isArray(sharedModel.cells)
            ? sharedModel.cells.indexOf(state.sharedCell)
            : state.index;
        if (placeholderIndex < 0) {
          return;
        }
        state.status = status;
        if (state.status === 'done' || state.status === 'waiting') {
          sharedModel.deleteCell(placeholderIndex);
        } else {
          setCellSource(
            notebook,
            sharedModel,
            placeholderIndex,
            renderStreamingText(state.content, state.status)
          );
          if (options.unlock) {
            setCellLock(notebook, placeholderIndex, false);
          }
        }
      } catch {
        // ignore
      } finally {
        streamingScratch = null;
      }
    };

    const startStreamingToScratch = async () => {
      const scratchPath = getDeepAnalyzeItem('activeScratchPath') ?? '';
      if (!scratchPath.trim()) {
        return;
      }
      // 如果上一次还留有流式 cell，先“完成并解锁”，避免残留锁定状态。
      await finalizeStreamingScratchCell('done', { unlock: true });

      const panel: any = await ensureNotebookPanel(scratchPath);
      const notebook: any = panel?.content;
      if (!notebook?.model?.sharedModel) {
        return;
      }

      const sharedModel = notebook.model.sharedModel as any;
      const insertIndex = notebook.widgets?.length ?? 0;
      const sharedCell = sharedModel.insertCell(insertIndex, {
        cell_type: 'raw',
        source: renderStreamingText('', 'streaming'),
        metadata: { editable: false, deletable: false }
      });
      try {
        notebook.activeCellIndex = Math.min(insertIndex, (notebook.widgets?.length ?? 1) - 1);
        notebook.scrollToItem?.(insertIndex);
        // 锁定状态下保持 command 模式，避免误入编辑。
        notebook.mode = 'command';
      } catch {
        // ignore
      }

      streamingScratch = {
        path: scratchPath,
        index: insertIndex,
        content: '',
        flushHandle: null,
        lastFlush: 0,
        status: 'streaming',
        panel,
        notebook,
        sharedModel,
        sharedCell,
        cellType: 'raw'
      };
    };

    const flushStreamingToScratch = async () => {
      const state = streamingScratch;
      if (!state) {
        return;
      }

      const scratchPath = getDeepAnalyzeItem('activeScratchPath') ?? '';
      if (!scratchPath.trim() || scratchPath !== state.path) {
        return;
      }

      try {
        const panel: any = state.panel ?? (await ensureNotebookPanel(state.path));
        const notebook: any = state.notebook ?? panel?.content;
        const sharedModel: any = state.sharedModel ?? notebook?.model?.sharedModel;
        if (!notebook?.model?.sharedModel || !sharedModel) {
          return;
        }
        const placeholderIndex =
          state.sharedCell && Array.isArray(sharedModel.cells)
            ? sharedModel.cells.indexOf(state.sharedCell)
            : state.index;
        if (placeholderIndex < 0) {
          return;
        }
        setCellSource(
          notebook,
          sharedModel,
          placeholderIndex,
          renderStreamingText(state.content, state.status)
        );
        state.lastFlush = Date.now();
      } catch {
        // ignore
      }
    };

    const scheduleFlushStreamingToScratch = () => {
      const state = streamingScratch;
      if (!state || state.flushHandle != null) {
        return;
      }
      const elapsed = Date.now() - state.lastFlush;
      const delay = Math.max(0, STREAM_FLUSH_MS - elapsed);
      state.flushHandle = window.setTimeout(() => {
        if (!streamingScratch) {
          return;
        }
        streamingScratch.flushHandle = null;
        void flushStreamingToScratch();
      }, delay);
    };

    const appendStreamingToScratch = (delta: string) => {
      const state = streamingScratch;
      if (!state) {
        return;
      }
      const d = String(delta ?? '');
      if (!d) {
        return;
      }
      state.content += d;
      scheduleFlushStreamingToScratch();
    };

    const markStreamingToScratch = (status: StreamingScratchState['status']) => {
      const state = streamingScratch;
      if (!state) {
        return;
      }
      state.status = status;
      scheduleFlushStreamingToScratch();
    };

    const clearNotebook = async (path: string) => {
      const panel: any = await ensureNotebookPanel(path);
      const notebook: any = panel?.content;
      if (!notebook?.model?.sharedModel) {
        return;
      }

      const sharedModel = notebook.model.sharedModel as any;
      const count = notebook.widgets?.length ?? 0;
      for (let i = count - 1; i >= 0; i--) {
        sharedModel.deleteCell(i);
      }
      sharedModel.insertCell(0, { cell_type: 'markdown', source: '' });
      notebook.activeCellIndex = 0;

      try {
        await panel.context?.save?.();
      } catch {
        // ignore
      }
    };

    const cleanupSession = async () => {
      const disposables = activeSession?.disposables ?? [];
      activeSession = null;
      for (const disposable of disposables) {
        disposable.dispose();
      }

      removeDeepAnalyzeItem('activeWorkspaceDir');
      removeDeepAnalyzeItem('activeOutputPath');
      removeDeepAnalyzeItem('activeScratchPath');
      removeDeepAnalyzeItem('sessionId');

      await safeFileBrowserCd(contents, defaultBrowser, [
        previousBrowserPath,
        toBrowserCdPath(contents, rootPath),
        '/'
      ]);
    };

    const exit = async () => {
      await cleanupSession();

      try {
        await app.commands.execute('application:close-all');
      } catch {
        // Non-fatal.
      }

      try {
        await app.commands.execute('launcher:create');
      } catch {
        // Non-fatal.
      }
    };

    // 处理后端返回的 data（包含 frontend_ops / await_feedback 等），并把执行过程以“chunk”形式回流给 Chat UI：
    // - system_text：系统提示（例如执行日志/错误）
    // - assistant_raw_updates：对 assistant raw 的增量覆写（用于回环时同步 notebook 的真实内容）
    // - trace_update：用于在 Chat 中点击定位到对应的 cell
    const handleToolResult = async function* (data: unknown) {
      const maybeObject = data as
        | { frontend_ops?: unknown; changed_paths?: unknown; await_feedback?: unknown; reply?: unknown }
        | null
        | undefined;

      const MAX_AUTO_FEEDBACK_TURNS = getDeepAnalyzeSettings().maxAutoFeedbackTurns ?? 50;

      const ops = Array.isArray(maybeObject?.frontend_ops)
        ? (maybeObject?.frontend_ops as unknown[])
        : [];

      const changedPaths = Array.isArray(maybeObject?.changed_paths)
        ? (maybeObject?.changed_paths as unknown[])
        : [];

      const revertByPath = (path: string) => {
        const widget = docManager.findWidget(path);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const context = (widget as any)?.context;
        if (!context) {
          return;
        }
        if (context.model?.dirty) {
          return;
        }
        void context.revert?.();
      };

      for (const item of changedPaths) {
        const path = String(item ?? '').trim();
        if (path) {
          revertByPath(path);
        }
      }

      const truncateText = (value: unknown, limit = 2000): string => {
        const raw = String(value ?? '');
        if (raw.length <= limit) {
          return raw;
        }
        return `${raw.slice(0, Math.max(0, limit - 1))}…`;
      };

      const normalizeOutputs = (outputs: any[]): any[] => {
        const items = Array.isArray(outputs) ? outputs.slice(0, 20) : [];
        return items.map(out => {
          const cloned = { ...(out ?? {}) } as any;
          if (cloned?.output_type === 'stream') {
            cloned.text = truncateText(cloned.text);
          }
          if (cloned?.output_type === 'error') {
            cloned.ename = truncateText(cloned.ename, 200);
            cloned.evalue = truncateText(cloned.evalue, 2000);
            if (Array.isArray(cloned.traceback)) {
              cloned.traceback = cloned.traceback.map((t: any) => truncateText(t, 2000));
            }
          }
          const data = cloned?.data;
          if (data && typeof data === 'object') {
            const nextData: Record<string, any> = { ...(data as any) };
            if (typeof nextData['text/plain'] === 'string') {
              nextData['text/plain'] = truncateText(nextData['text/plain']);
            }
            cloned.data = nextData;
          }
          return cloned;
        });
      };

      const summarizeOutputs = (outputs: any[]): string => {
        const lines: string[] = [];

        const stdout = outputs
          .filter(out => out?.output_type === 'stream' && out?.name === 'stdout')
          .map(out => String(out?.text ?? ''))
          .join('');
        const stderr = outputs
          .filter(out => out?.output_type === 'stream' && out?.name === 'stderr')
          .map(out => String(out?.text ?? ''))
          .join('');

        if (stdout.trim()) {
          lines.push(`stdout: ${truncateText(stdout.trim(), 8000)}`);
        }
        if (stderr.trim()) {
          lines.push(`stderr: ${truncateText(stderr.trim(), 8000)}`);
        }

        const executeResult = outputs.find(out => out?.output_type === 'execute_result');
        const textPlain = executeResult?.data?.['text/plain'];
        if (typeof textPlain === 'string' && textPlain.trim()) {
          lines.push(`result: ${truncateText(String(textPlain).trim(), 4000)}`);
        }

        const errors = outputs.filter(out => out?.output_type === 'error');
        for (const err of errors) {
          const ename = String(err?.ename ?? '').trim();
          const evalue = String(err?.evalue ?? '').trim();
          const tb = Array.isArray(err?.traceback) ? err.traceback.join('\n') : '';
          const head = [ename, evalue].filter(Boolean).join(': ');
          const body = tb.trim() ? tb.trim() : head;
          if (body.trim()) {
            lines.push(`error: ${truncateText(body.trim(), 12000)}`);
          }
        }

        return lines.join('\n');
      };

        // 执行一批 frontend_ops（由后端下发），并在过程中产出 tool_results：
        // - 对 notebook 的写入/执行全部发生在前端（NotebookPanel/sharedModel）
        // - 执行输出会汇总为文本，用于后端下一轮上下文（role=execute）
        const execOpsStream = async function* (
          opsToRun: unknown[],
          awaitFeedback: boolean,
          depth = 0
        ): AsyncGenerator<{
        system_text?: string;
        assistant_raw_updates?: string[];
        trace_update?: { tag: string; path: string; index: number };
      }> {
        const logs: string[] = [];
        const userVisible: string[] = [];
        const toolResults: any[] = [];
        let pendingScratchCodeCell = false;

        const pickSyncMeta = (rawOp: any): Record<string, any> => {
          const meta: Record<string, any> = {};
          if (rawOp?.turn_id != null) {
            meta.turn_id = String(rawOp.turn_id);
          }
          if (rawOp?.segment_tag != null) {
            meta.segment_tag = String(rawOp.segment_tag);
          }
          if (rawOp?.segment_kind != null) {
            meta.segment_kind = String(rawOp.segment_kind);
          }
          const ordinal = Number(rawOp?.segment_ordinal);
          if (Number.isFinite(ordinal)) {
            meta.segment_ordinal = ordinal;
          }
          return meta;
        };

        for (const raw of opsToRun) {
          const op = raw as any;
          const opName = String(op?.op ?? '').trim();
          const path = String(op?.path ?? '').trim();
          const opId = op?.id ? String(op.id) : undefined;
          if (!opName || !path) {
            continue;
          }

          if (opName === 'create_notebook') {
            const overwrite = Boolean(op?.overwrite);
            const shouldOpen = op?.open === false ? false : true;
            const target = String(op?.target ?? '').trim().toLowerCase();
            const parent = PathExt.dirname(path);
            await ensureDirectoryPath(contents, parent);

            const resolveRefWidgetId = (): string | undefined => {
              const outputPath =
                getDeepAnalyzeItem('activeOutputPath') ?? '';
              const scratchPath =
                getDeepAnalyzeItem('activeScratchPath') ?? '';

              const normalize = (value: string) =>
                String(value ?? '')
                  .trim()
                  .toLowerCase()
                  .replace(/[\s_]+/g, '-');

              const targetNormalized = normalize(target);
              const isOutput =
                targetNormalized === 'output' ||
                targetNormalized === 'model-output' ||
                targetNormalized === 'modeloutput' ||
                targetNormalized === 'model';
              const isScratch = targetNormalized === 'scratch';

              if (isOutput && outputPath) {
                return docManager.findWidget(outputPath)?.id;
              }
              if (isScratch && scratchPath) {
                return docManager.findWidget(scratchPath)?.id;
              }
              return undefined;
            };

            const refWidgetId = resolveRefWidgetId();
            const openOptions = refWidgetId
              ? ({ mode: 'tab-after' as const, ref: refWidgetId } as const)
              : undefined;

            if (!overwrite) {
              try {
                await contents.get(path, { content: false });
                if (shouldOpen) {
                  docManager.openOrReveal(path, undefined, undefined, openOptions);
                  logs.push(`已打开 notebook：${path}`);
                } else {
                  logs.push(`已确认 notebook 存在（未打开）：${path}`);
                }
                continue;
              } catch {
                // create
              }
            }
            const model = await docManager.newUntitled({ path: parent, type: 'notebook' });
            try {
              await docManager.rename(model.path, path);
            } catch {
              // ignore rename failure
            }
            if (shouldOpen) {
              docManager.openOrReveal(path, undefined, undefined, openOptions);
              logs.push(`已创建 notebook：${path}`);
            } else {
              logs.push(`已创建 notebook（未打开）：${path}`);
            }
            continue;
          }

          const panel = await ensureNotebookPanel(path);
          const notebook = panel.content as any;
          if (!notebook?.model?.sharedModel) {
            throw new Error(`不是 NotebookPanel：${path}`);
          }

          const sharedModel = notebook.model.sharedModel as any;
          const index = Number.isFinite(op?.index) ? Number(op.index) : 0;

          if (opName === 'list_cells') {
            const items = (notebook.widgets ?? []).map((cell: any, i: number) => {
              const cellType = cell?.model?.type ?? cell?.model?.sharedModel?.cell_type ?? 'unknown';
              const source = cell?.model?.sharedModel?.getSource?.() ?? cell?.model?.value?.text ?? '';
              const firstLine = String(source).split('\n')[0] ?? '';
              return `${i}. [${cellType}] ${firstLine}`.trim();
            });
            logs.push(items.join('\n') || '(empty)');
            continue;
          }

          if (opName === 'get_cell') {
            const cell = notebook.widgets?.[index];
            const source =
              cell?.model?.sharedModel?.getSource?.() ??
              cell?.model?.value?.text ??
              '';
            logs.push(String(source));
            continue;
          }

          if (opName === 'read_cell') {
            const cell = notebook.widgets?.[index];
            if (!cell) {
              throw new Error(`cell index 越界：${index}`);
            }
            const cellType =
              cell?.model?.type ?? cell?.model?.sharedModel?.cell_type ?? 'unknown';
            const source =
              cell?.model?.sharedModel?.getSource?.() ??
              cell?.model?.value?.text ??
              '';
            const outputs = cell?.model?.outputs?.toJSON?.() ?? [];
            const executionCount =
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              (cell?.model as any)?.executionCount ??
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              (cell?.model as any)?.execution_count ??
              cell?.model?.sharedModel?.execution_count ??
              null;
            const metadata = cell?.model?.metadata?.toJSON?.() ?? {};

            const payload = {
              index,
              cell_type: cellType,
              source: String(source),
              execution_count: executionCount,
              outputs: normalizeOutputs(outputs),
              metadata
            };
            logs.push(JSON.stringify(payload, null, 2));
            continue;
          }

          if (opName === 'insert_cell') {
            const cellType = String(op?.cell_type ?? 'code');
            const source = String(op?.source ?? '');
            const maybeIndex = Number.isFinite(op?.index) ? Number(op.index) : NaN;
            const insertIndex =
              Number.isFinite(maybeIndex) && maybeIndex >= 0
                ? maybeIndex
                : notebook.widgets?.length ?? 0;
            const syncMeta = pickSyncMeta(op);
            if (opId) {
              syncMeta.op_id = opId;
            }
            sharedModel.insertCell(insertIndex, {
              cell_type: cellType,
              source,
              metadata: {
                ...(cellType === 'code' ? { trusted: true } : {}),
                deepanalyze: syncMeta
              }
            });
            notebook.activeCellIndex = Math.min(
              insertIndex,
              (notebook.widgets?.length ?? 1) - 1
            );
            logs.push(`已插入 cell：index=${insertIndex} type=${cellType}`);
            toolResults.push({
              id: opId,
              op: opName,
              path,
              index: insertIndex,
              cell_type: cellType,
              ...syncMeta
            });

            const scratchPath = getDeepAnalyzeItem('activeScratchPath') ?? '';
            if (scratchPath && path === scratchPath) {
              const headerMatch = source.match(/^###\s*(Analyze|Understand|Code|Answer)\b/i);
              if (cellType === 'markdown' && headerMatch) {
                const tag = String(headerMatch[1] ?? '').trim();
                if (tag.toLowerCase() === 'code') {
                  pendingScratchCodeCell = true;
                } else {
                  pendingScratchCodeCell = false;
                  yield { trace_update: { tag, path, index: insertIndex } };
                }
              } else if (cellType === 'code' && pendingScratchCodeCell) {
                pendingScratchCodeCell = false;
                yield { trace_update: { tag: 'Code', path, index: insertIndex } };
              }
            }
            continue;
          }

          if (opName === 'delete_cell') {
            sharedModel.deleteCell(index);
            logs.push(`已删除 cell：index=${index}`);
            toolResults.push({ id: opId, op: opName, path, index, ...pickSyncMeta(op) });
            continue;
          }

          if (opName === 'update_cell') {
            const source = String(op?.source ?? '');
            const cell = notebook.widgets?.[index];
            const syncMeta = pickSyncMeta(op);
            if (opId) {
              syncMeta.op_id = opId;
            }
            if (cell?.model?.sharedModel?.setSource) {
              cell.model.sharedModel.setSource(source);
            } else {
              const sharedCell = sharedModel.getCell?.(index);
              sharedCell?.setSource?.(source);
            }
            try {
              cell?.model?.metadata?.set?.('deepanalyze', syncMeta);
            } catch {
              // ignore
            }
            logs.push(`已更新 cell：index=${index}`);
            toolResults.push({ id: opId, op: opName, path, index, ...syncMeta });
            continue;
          }

          if (opName === 'run_last_cell') {
            const widgets = notebook.widgets ?? [];
            let targetIndex = -1;
            for (let i = widgets.length - 1; i >= 0; i--) {
              const w = widgets[i];
              const cellType = w?.model?.type ?? w?.model?.sharedModel?.cell_type ?? '';
              if (String(cellType).toLowerCase() === 'code') {
                targetIndex = i;
                break;
              }
            }
            if (targetIndex < 0) {
              throw new Error('没有可执行的 code cell');
            }
            const cellWidget = widgets[targetIndex];
            try {
              const syncMeta = pickSyncMeta(op);
              if (opId) {
                syncMeta.op_id = opId;
              }
              cellWidget?.model?.metadata?.set?.('deepanalyze', syncMeta);
            } catch {
              // ignore
            }
            const ok = await NotebookActions.runCells(
              notebook,
              [cellWidget],
              panel.sessionContext
            );
            const outputs = cellWidget?.model?.outputs?.toJSON?.() ?? [];
            const text = summarizeOutputs(outputs);
            logs.push(`执行${ok ? '成功' : '失败'}：index=${targetIndex}\n${text}`);
            toolResults.push({
              id: opId,
              op: opName,
              path,
              index: targetIndex,
              ok,
              outputs: normalizeOutputs(outputs),
              text,
              ...pickSyncMeta(op)
            });
            continue;
          }

          if (opName === 'run_cell') {
            const cellWidget = notebook.widgets?.[index];
            if (!cellWidget) {
              throw new Error(`cell index 越界：${index}`);
            }
            try {
              const syncMeta = pickSyncMeta(op);
              if (opId) {
                syncMeta.op_id = opId;
              }
              cellWidget?.model?.metadata?.set?.('deepanalyze', syncMeta);
            } catch {
              // ignore
            }
            const ok = await NotebookActions.runCells(
              notebook,
              [cellWidget],
              panel.sessionContext
            );
            const outputs = cellWidget?.model?.outputs?.toJSON?.() ?? [];
            const text = summarizeOutputs(outputs);
            logs.push(`执行${ok ? '成功' : '失败'}：index=${index}\n${text}`);
            toolResults.push({
              id: opId,
              op: opName,
              path,
              index,
              ok,
              outputs: normalizeOutputs(outputs),
              text,
              ...pickSyncMeta(op)
            });
            continue;
          }

          const message = `未知 op：${opName}`;
          logs.push(message);
          userVisible.push(message);
          toolResults.push({ id: opId, op: opName, path, ok: false, ...pickSyncMeta(op) });
        }

        const sessionId = getDeepAnalyzeItem('sessionId') ?? '';
        const logText = logs.filter(Boolean).join('\n\n');
        const autoContinueEnabled = chatPanel?.getAutoContinueEnabled() ?? true;
        const deferBackendReturn = awaitFeedback && !autoContinueEnabled;
        if (!deferBackendReturn && (logText.trim() || toolResults.length > 0)) {
          void sendFrontendLog({
            session_id: sessionId || undefined,
            depth,
            await_feedback: awaitFeedback,
            logs: logText,
            tool_results: toolResults
          }).catch(() => undefined);
        }

        if (userVisible.length > 0) {
          yield { system_text: userVisible.join('\n') };
        }

        if (!awaitFeedback) {
          return;
        }

        if (depth >= MAX_AUTO_FEEDBACK_TURNS) {
          yield {
            system_text: `(已达到自动执行轮次上限 ${MAX_AUTO_FEEDBACK_TURNS}，停止继续调用模型)`
          };
          return;
        }

        if (!sessionId) {
          yield { system_text: '(缺少 sessionId，无法回传执行结果)' };
          return;
        }

        const collectNotebookSnapshots = async (): Promise<{
          execute_text: string;
          tool_results: any[];
        }> => {
          const indicesByPath = new Map<string, Set<number>>();
          const addIndex = (path: string, index: number) => {
            if (!Number.isFinite(index) || index < 0) {
              return;
            }
            const set = indicesByPath.get(path) ?? new Set<number>();
            set.add(index);
            indicesByPath.set(path, set);
          };

          const MAX_CELLS = 16;
          const MAX_SOURCE_LEN = 6000;

          const blocks: string[] = [];
          const refreshedToolResults = toolResults.map(it => ({ ...(it ?? {}) }));

          const getDeepAnalyzeMeta = (cell: any): any => {
            try {
              const meta = cell?.model?.metadata;
              if (meta?.get) {
                return meta.get('deepanalyze');
              }
              return meta?.toJSON?.()?.deepanalyze ?? null;
            } catch {
              return null;
            }
          };

          const normalizeWanted = (it: any) => {
            const turnId = String(it?.turn_id ?? '').trim();
            const segTag = String(it?.segment_tag ?? '').trim();
            const segKind = String(it?.segment_kind ?? '').trim();
            const ordinal = Number.isFinite(it?.segment_ordinal) ? Number(it.segment_ordinal) : NaN;
            return { turnId, segTag, segKind, ordinal };
          };

          const resolveIndexByMeta = (notebook: any, it: any): number | null => {
            const wanted = normalizeWanted(it);
            if (!wanted.turnId || !wanted.segTag || !wanted.segKind || !Number.isFinite(wanted.ordinal)) {
              return null;
            }
            const widgets = notebook?.widgets ?? [];
            for (let i = 0; i < widgets.length; i++) {
              const cell = widgets[i];
              const meta = getDeepAnalyzeMeta(cell);
              if (!meta) {
                continue;
              }
              const turnId = String(meta?.turn_id ?? '').trim();
              const segTag = String(meta?.segment_tag ?? '').trim();
              const segKind = String(meta?.segment_kind ?? '').trim();
              const ordinal = Number.isFinite(meta?.segment_ordinal) ? Number(meta.segment_ordinal) : NaN;
              if (
                turnId === wanted.turnId &&
                segTag === wanted.segTag &&
                segKind === wanted.segKind &&
                Number.isFinite(ordinal) &&
                ordinal === wanted.ordinal
              ) {
                return i;
              }
            }
            return null;
          };

          // 先按 meta 把 tool_results 的 index 纠正，避免用户增删 cell 后 index 漂移导致快照/覆写错位。
          const pathGroups = new Map<string, any[]>();
          for (const it of refreshedToolResults) {
            const path = String(it?.path ?? '').trim();
            if (!path) continue;
            const list = pathGroups.get(path) ?? [];
            list.push(it);
            pathGroups.set(path, list);
          }

          for (const [path, items] of pathGroups) {
            const panel: any = await ensureNotebookPanel(path);
            const notebook: any = panel?.content;
            if (!notebook) {
              continue;
            }

            for (const it of items) {
              const resolved = resolveIndexByMeta(notebook, it);
              if (resolved != null && Number.isFinite(resolved) && resolved >= 0) {
                it.index = resolved;
              }
              const index = Number.isFinite(it?.index) ? Number(it.index) : NaN;
              addIndex(path, index);
            }

            const indicesSet = indicesByPath.get(path) ?? new Set<number>();
            const indices = Array.from(indicesSet)
              .filter(n => Number.isFinite(n))
              .sort((a, b) => a - b)
              .slice(0, MAX_CELLS);
            if (indices.length === 0) {
              continue;
            }

            blocks.push(`# Notebook: ${path}`);
            for (const index of indices) {
              const cell = notebook.widgets?.[index];
              if (!cell) {
                continue;
              }

              const cellType =
                cell?.model?.type ?? cell?.model?.sharedModel?.cell_type ?? 'unknown';
              const rawSource =
                cell?.model?.sharedModel?.getSource?.() ??
                cell?.model?.value?.text ??
                '';
              const source = truncateText(String(rawSource ?? ''), MAX_SOURCE_LEN);
              const outputs = cell?.model?.outputs?.toJSON?.() ?? [];
              const outputsText = summarizeOutputs(outputs);

              blocks.push(`\n## cell[${index}] (${cellType})`);
              if (String(cellType).toLowerCase() === 'code') {
                blocks.push(`\n\`\`\`python\n${source}\n\`\`\``);
                if (outputsText.trim()) {
                  blocks.push(`\n### outputs\n${outputsText}`);
                }
              } else {
                blocks.push(`\n${source}`);
              }

              for (const item of refreshedToolResults) {
                if (String(item?.path ?? '') !== path) {
                  continue;
                }
                if (!Number.isFinite(item?.index) || Number(item.index) !== index) {
                  continue;
                }
                if (item?.op === 'run_cell' || item?.op === 'run_last_cell') {
                  item.source = source;
                  item.outputs = normalizeOutputs(outputs);
                  item.text = outputsText;
                }
                if (item?.op === 'insert_cell' || item?.op === 'update_cell') {
                  item.source = source;
                }
              }
            }
          }

          const executeText = blocks.join('\n').trim();
          return { execute_text: executeText, tool_results: refreshedToolResults };
        };

        try {
          if (!autoContinueEnabled) {
            const decision = chatPanel
              ? await chatPanel.waitForContinueOrAbort()
              : 'continue';
            if (decision === 'abort') {
              yield { system_text: '已中止：未回传本轮执行结果，停止继续生成。' };
              return;
            }
          }

          const feedbackPayload = await collectNotebookSnapshots();

          if (deferBackendReturn && (logText.trim() || toolResults.length > 0)) {
            void sendFrontendLog({
              session_id: sessionId || undefined,
              depth,
              await_feedback: awaitFeedback,
              logs: logText,
              tool_results: feedbackPayload.tool_results
            }).catch(() => undefined);
          }

          chatPanel?.setModelGenerating(true);
          let feedbackResponse: any = null;
          try {
            await startStreamingToScratch();
            chatPanel?.startAssistantStreaming();
            for await (const event of streamAgentFeedback({
              session_id: sessionId,
              execute_text: feedbackPayload.execute_text,
              tool_results: feedbackPayload.tool_results,
              model_id: getDeepAnalyzeItem('modelId') || undefined,
              prompt_lang: getDeepAnalyzeItem('promptLang') || 'zh'
            })) {
              if (event.type === 'delta') {
                appendStreamingToScratch(event.delta);
                chatPanel?.appendAssistantStreaming(event.delta);
                continue;
              }
              if (event.type === 'final') {
                feedbackResponse = event.response;
                break;
              }
            }
            const data = feedbackResponse?.data as any;
            const raw =
              typeof data?.raw === 'string' ? String(data.raw) : String(feedbackResponse?.reply ?? '');
            if (!raw.trim()) {
              throw new Error('流式 feedback 返回空内容');
            }
            const awaitFeedbackNext = Boolean(data?.await_feedback);
            const hasAnswer = /<Answer\b/i.test(raw) && /<\/Answer>/i.test(raw);
            chatPanel?.finalizeAssistantStreaming({ raw, hasAnswer });
            const nextStatus = awaitFeedbackNext && !hasAnswer ? 'waiting' : 'done';
            await finalizeStreamingScratchCell(nextStatus, { unlock: true });
          } catch (error) {
            await finalizeStreamingScratchCell('error', { unlock: true });
            chatPanel?.finalizeAssistantStreaming({ hasAnswer: true });
            try {
              void sendFrontendLog({
                session_id: sessionId || undefined,
                depth,
                await_feedback: awaitFeedback,
                message: 'stream_feedback_failed',
                logs: JSON.stringify({ error: String(error) }, null, 2)
              });
            } catch {
              // ignore
            }
            feedbackResponse = await sendAgentFeedback({
              session_id: sessionId,
              execute_text: feedbackPayload.execute_text,
              tool_results: feedbackPayload.tool_results,
              model_id: getDeepAnalyzeItem('modelId') || undefined,
              prompt_lang: getDeepAnalyzeItem('promptLang') || 'zh'
            });
          } finally {
            chatPanel?.setModelGenerating(false);
          }

          const followData: any = feedbackResponse?.data ?? null;
          const followText = String(feedbackResponse?.reply ?? '').trim();
          let followRaw = typeof followData?.raw === 'string' ? String(followData.raw) : '';
          if (!followRaw.trim() && followText) {
            followRaw = followText.includes('<')
              ? followText
              : `<Answer>\n${followText}\n</Answer>`;
          }
          if (followRaw.trim()) {
            yield { assistant_raw_updates: [followRaw.trim()] };
          }
          const followOps = Array.isArray(followData?.frontend_ops)
            ? (followData?.frontend_ops as unknown[])
            : [];
          if (followOps.length > 0) {
            for await (const chunk of execOpsStream(
              followOps,
              Boolean(followData?.await_feedback),
              depth + 1
            )) {
              yield chunk;
            }
          }
        } catch (error) {
          chatPanel?.setModelGenerating(false);
          yield { system_text: `(回传执行结果失败：${String(error)})` };
        }
      };

      for await (const chunk of execOpsStream(ops, Boolean(maybeObject?.await_feedback))) {
        yield chunk;
      }
    };

    const chat = new DeepAnalyzeChatPanel({
      onExit: () => void exit(),
      onReset: async options => {
        if (!options?.clearNotebooks) {
          return;
        }
        const outputPath = getDeepAnalyzeItem('activeOutputPath') ?? '';
        const scratchPath = getDeepAnalyzeItem('activeScratchPath') ?? '';
        if (outputPath.trim()) {
          await clearNotebook(outputPath);
        }
        if (scratchPath.trim()) {
          await clearNotebook(scratchPath);
        }
      },
      onModelStream: async event => {
        if (event.type === 'start') {
          try {
            await startStreamingToScratch();
          } catch {
            // ignore
          }
          return;
        }
        if (event.type === 'delta') {
          appendStreamingToScratch(event.delta);
          return;
        }
        if (event.type === 'final') {
          const nextStatus = event.awaitFeedback && !event.hasAnswer ? 'waiting' : 'done';
          try {
            // 生成结束后解锁（允许复制/修改），但如果需要回环则显示“等待执行”而非 done。
            await finalizeStreamingScratchCell(nextStatus, { unlock: true });
          } catch {
            // ignore
          }
          return;
        }
        if (event.type === 'end') {
          // 兜底：如果没有拿到 final（例如 SSE 被截断），避免一直停留在“生成中…”
          await finalizeStreamingScratchCell('done', { unlock: true });
          return;
        }
        if (event.type === 'error') {
          await finalizeStreamingScratchCell('error', { unlock: true });
          return;
        }
      },
      onNavigateToCell: async (path, index) => {
        const panel: any = await ensureNotebookPanel(path);
        const notebook: any = panel?.content;
        if (!notebook) {
          return;
        }
        try {
          app.shell.activateById(panel.id);
        } catch {
          // ignore
        }
        try {
          notebook.activeCellIndex = index;
        } catch {
          // ignore
        }
        try {
          notebook.scrollToItem?.(index);
        } catch {
          // ignore
        }
        try {
          const node = notebook.widgets?.[index]?.node as HTMLElement | undefined;
          node?.scrollIntoView?.({ block: 'start' });
        } catch {
          // ignore
        }
      },
      onToolResult: handleToolResult
    });
    chat.id = `deepanalyze-chat-${instanceId}`;
    chat.title.closable = false;
    chatPanel = chat;
    chatWidget = chat;

    restoreAddButtonInterceptor = installMainAreaAddButtonClickInterceptor(
      app,
      docManager,
      workspaceDir
    );

    activeSession = {
      previousBrowserPath,
      disposables: [rootRestriction, restoreAddButtonInterceptor]
    };

    const originalDispose = chat.dispose.bind(chat);
    chat.dispose = () => {
      void cleanupSession();
      originalDispose();
    };
  } catch {
    chatWidget = null;
    rootRestriction.dispose();
    restoreAddButtonInterceptor?.dispose();
    restoreAddButtonInterceptor = null;
  }

  if (chatWidget) {
    // scratch 与 model_output 放在中间栏同一组（tab），右侧仅保留 chat。
    const scratchWidget = docManager.openOrReveal(
      scratchNotebookPath,
      undefined,
      undefined,
      {
        mode: 'tab-after',
        ref: outputWidget.id
      }
    );

    if (scratchWidget) {
      scratchWidget.title.closable = false;
      try {
        app.shell.add(scratchWidget, 'main', { mode: 'tab-after', ref: outputWidget.id });
      } catch {
        ensureInMainArea(scratchWidget);
      }
    }

    // “使用大模型编辑”右键菜单已改为全局注册（见 src/index.ts），这里不再对 scratch 单独安装。

    try {
      app.shell.add(chatWidget, 'main', { mode: 'split-right', ref: outputWidget.id });
    } catch {
      ensureInMainArea(chatWidget);
    }
  } else {
    const scratchWidget = docManager.openOrReveal(scratchNotebookPath, undefined, undefined, {
      mode: 'split-right',
      ref: outputWidget.id
    });
    scratchWidget && (scratchWidget.title.closable = false);
    await showErrorMessage(
      'DeepAnalyze',
      '对话面板不可用，已用 Notebook 分屏代替。'
    );
  }

  return outputWidget;
}

export async function restoreDeepAnalyzeIfNeeded(
  app: JupyterFrontEnd,
  docManager: IDocumentManager,
  defaultBrowser: IDefaultFileBrowser
): Promise<void> {
  // 页面刷新后，若 localStorage 仍保存着上一次的 workspace 信息，则尝试自动恢复布局。
  const workspaceDir = getDeepAnalyzeItem('activeWorkspaceDir') ?? '';
  if (!String(workspaceDir).trim()) {
    return;
  }

  try {
    const { contents } = app.serviceManager;
    try {
      const model = await contents.get(workspaceDir, { content: false });
      if (model.type !== 'directory') {
        removeDeepAnalyzeItem('activeWorkspaceDir');
        removeDeepAnalyzeItem('activeOutputPath');
        removeDeepAnalyzeItem('activeScratchPath');
        removeDeepAnalyzeItem('sessionId');
        return;
      }
    } catch (error: any) {
      const status = Number(error?.response?.status);
      if (status === 404) {
        removeDeepAnalyzeItem('activeWorkspaceDir');
        removeDeepAnalyzeItem('activeOutputPath');
        removeDeepAnalyzeItem('activeScratchPath');
        removeDeepAnalyzeItem('sessionId');
        return;
      }
    }

    await openDeepAnalyze(app, docManager, defaultBrowser, {
      workspaceDir,
      skipPrompt: true
    });
  } catch {
    // ignore restore errors
  }
}
