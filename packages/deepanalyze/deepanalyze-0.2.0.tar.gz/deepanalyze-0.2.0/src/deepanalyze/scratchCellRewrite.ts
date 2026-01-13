import { JupyterFrontEnd } from '@jupyterlab/application';
import { Dialog, showDialog, showErrorMessage } from '@jupyterlab/apputils';
import { DisposableDelegate } from '@lumino/disposable';
import { Widget } from '@lumino/widgets';

import { rewriteCellSource, streamRewriteCellSource } from './api';
import { getDeepAnalyzeItem } from './storage';

/**
 * scratch 单元格“使用大模型编辑”入口（右键菜单）。
 *
 * 说明：
 * - 该功能面向“手动微调模型生成的 cell”：用户输入指令，后端返回改写后的完整内容，并覆盖当前 cell。
 * - 优先使用流式写回（让用户看到增量变化），失败则回退非流式。
 */
type AnyNotebookPanel = any;
type AnyNotebook = any;
type AnyCell = any;

type CellRewriteBarsState = {
  root: HTMLElement;
  topBar: HTMLElement;
  topStatusText: HTMLElement;
  topDot: HTMLElement;
  stopButton: HTMLButtonElement;
  bottomBar: HTMLElement;
  bottomStatusText: HTMLElement;
  acceptButton: HTMLButtonElement;
  rollbackButton: HTMLButtonElement;
  originalSource: string | null;
  abortController: AbortController | null;
  phase: 'hidden' | 'waiting' | 'running' | 'done';
};

const cellBars = new WeakMap<AnyCell, CellRewriteBarsState>();

function getCellSource(cell: AnyCell): string {
  try {
    const shared = cell?.model?.sharedModel;
    if (shared?.getSource) {
      return String(shared.getSource() ?? '');
    }
  } catch {
    // ignore
  }
  try {
    return String(cell?.model?.value?.text ?? '');
  } catch {
    return '';
  }
}

function getCellType(cell: AnyCell): string {
  try {
    const modelType = String(cell?.model?.type ?? '').trim();
    if (modelType) {
      return modelType;
    }
  } catch {
    // ignore
  }
  try {
    const sharedType = String(cell?.model?.sharedModel?.cell_type ?? '').trim();
    if (sharedType) {
      return sharedType;
    }
  } catch {
    // ignore
  }
  return '';
}

function _asText(value: any): string {
  if (value == null) return '';
  if (Array.isArray(value)) {
    return value.map(v => String(v ?? '')).join('');
  }
  return String(value);
}

function getCodeCellExecutionResult(cell: AnyCell): string {
  const cellType = getCellType(cell);
  if (cellType !== 'code') {
    return '';
  }

  let outputs: any[] = [];
  try {
    const modelOutputs = cell?.model?.outputs;
    if (modelOutputs?.toJSON) {
      const json = modelOutputs.toJSON();
      if (Array.isArray(json)) {
        outputs = json as any[];
      }
    } else if (Array.isArray(modelOutputs)) {
      outputs = modelOutputs as any[];
    }
  } catch {
    // ignore
  }

  if (!outputs.length) {
    return '';
  }

  const parts: string[] = [];
  for (const output of outputs) {
    const outputType = String(output?.output_type ?? '').trim();

    if (outputType === 'stream') {
      const name = String(output?.name ?? 'stdout');
      const text = _asText(output?.text);
      const content = text.trimEnd();
      if (content) {
        parts.push(`[${name}]\n${content}`);
      }
      continue;
    }

    if (outputType === 'error') {
      const ename = String(output?.ename ?? '').trim();
      const evalue = String(output?.evalue ?? '').trim();
      const header = [ename, evalue].filter(Boolean).join(': ');
      const traceback = output?.traceback;
      const tbText = Array.isArray(traceback)
        ? traceback.map(v => String(v ?? '')).join('\n')
        : String(traceback ?? '');
      const content = tbText.trimEnd();
      if (content || header) {
        parts.push(`[error]${header ? ` ${header}` : ''}\n${content || '(无 traceback)'}`);
      }
      continue;
    }

    if (outputType === 'execute_result' || outputType === 'display_data') {
      const data = output?.data ?? {};
      const plain = _asText(data?.['text/plain']);
      const markdown = _asText(data?.['text/markdown']);
      const content = (plain || markdown).trimEnd();
      if (content) {
        parts.push(`[result]\n${content}`);
      }
      continue;
    }
  }

  const merged = parts.join('\n\n').trim();
  if (!merged) {
    return '';
  }

  const maxChars = 8000;
  if (merged.length <= maxChars) {
    return merged;
  }
  const tail = merged.slice(-maxChars);
  return `（输出过长，已截断，仅保留最后 ${maxChars} 个字符）\n${tail}`;
}

function setCellSource(cell: AnyCell, source: string): void {
  try {
    const shared = cell?.model?.sharedModel;
    if (shared?.setSource) {
      shared.setSource(source);
      return;
    }
  } catch {
    // ignore
  }
  try {
    if (cell?.model?.value) {
      cell.model.value.text = source;
    }
  } catch {
    // ignore
  }
}

function getCellRoot(cell: AnyCell): HTMLElement | null {
  return (cell?.node ?? null) as HTMLElement | null;
}

function disposeRewriteBars(cell: AnyCell): void {
  const bars = cellBars.get(cell);
  const root = bars?.root ?? getCellRoot(cell);
  if (root) {
    try {
      root
        .querySelectorAll('.deepanalyze-cell-rewrite-topbar, .deepanalyze-cell-rewrite-bottombar')
        .forEach(node => node.remove());
    } catch {
      // ignore
    }
  }
  if (bars) {
    try {
      bars.topBar.remove();
    } catch {
      // ignore
    }
    try {
      bars.bottomBar.remove();
    } catch {
      // ignore
    }
    cellBars.delete(cell);
  }
}

function ensureRewriteBars(cell: AnyCell): CellRewriteBarsState | null {
  const existing = cellBars.get(cell);
  if (existing) {
    if (existing.topBar.isConnected && existing.bottomBar.isConnected) {
      return existing;
    }
    cellBars.delete(cell);
  }

  const root = getCellRoot(cell);
  if (!root) {
    return null;
  }

  // 防止 notebook 重新渲染/复用 DOM 时重复插入导致出现多个通知条。
  try {
    const leftovers = root.querySelectorAll(
      '.deepanalyze-cell-rewrite-topbar, .deepanalyze-cell-rewrite-bottombar'
    );
    leftovers.forEach(node => node.remove());
  } catch {
    // ignore
  }

  const buildStatus = () => {
    const status = document.createElement('div');
    status.className = 'deepanalyze-cell-rewrite-status';

    const dot = document.createElement('span');
    dot.className = 'deepanalyze-cell-rewrite-dot';

    const text = document.createElement('span');
    text.className = 'deepanalyze-cell-rewrite-text';

    status.appendChild(dot);
    status.appendChild(text);

    return { status, dot, text };
  };

  const topBar = document.createElement('div');
  topBar.className = 'deepanalyze-cell-rewrite-bar deepanalyze-cell-rewrite-topbar';
  topBar.hidden = true;
  const topStatus = buildStatus();

  const topActions = document.createElement('div');
  topActions.className = 'deepanalyze-cell-rewrite-actions';
  const stopButton = document.createElement('button');
  stopButton.type = 'button';
  stopButton.className = 'deepanalyze-cell-rewrite-stop';
  stopButton.textContent = '停止';
  topActions.appendChild(stopButton);
  topBar.appendChild(topStatus.status);
  topBar.appendChild(topActions);

  const bottomBar = document.createElement('div');
  bottomBar.className =
    'deepanalyze-cell-rewrite-bar deepanalyze-cell-rewrite-bottombar';
  bottomBar.hidden = true;
  const bottomStatus = buildStatus();

  const bottomActions = document.createElement('div');
  bottomActions.className = 'deepanalyze-cell-rewrite-actions';

  const acceptButton = document.createElement('button');
  acceptButton.type = 'button';
  acceptButton.className = 'deepanalyze-cell-rewrite-accept';
  acceptButton.textContent = '接受';

  const rollbackButton = document.createElement('button');
  rollbackButton.type = 'button';
  rollbackButton.className = 'deepanalyze-cell-rewrite-rollback';
  rollbackButton.textContent = '回退';

  bottomActions.appendChild(acceptButton);
  bottomActions.appendChild(rollbackButton);
  bottomBar.appendChild(bottomStatus.status);
  bottomBar.appendChild(bottomActions);

  const header = (root.querySelector('.jp-CellHeader') ??
    root.querySelector('.jp-Cell-header')) as HTMLElement | null;
  if (header) {
    header.insertAdjacentElement('afterend', topBar);
  } else {
    root.insertAdjacentElement('afterbegin', topBar);
  }

  // 底部通知条放在“输出区之前”（输入区之后），保证位于输出结果顶部。
  const outputWrapper = root.querySelector('.jp-Cell-outputWrapper') as HTMLElement | null;
  if (outputWrapper) {
    outputWrapper.insertAdjacentElement('beforebegin', bottomBar);
  } else {
    root.insertAdjacentElement('beforeend', bottomBar);
  }

  const state: CellRewriteBarsState = {
    root,
    topBar,
    topStatusText: topStatus.text,
    topDot: topStatus.dot,
    stopButton,
    bottomBar,
    bottomStatusText: bottomStatus.text,
    acceptButton,
    rollbackButton,
    originalSource: null,
    abortController: null,
    phase: 'hidden'
  };
  cellBars.set(cell, state);
  return state;
}

function setBarsPhase(state: CellRewriteBarsState, phase: CellRewriteBarsState['phase']): void {
  state.phase = phase;
  if (phase === 'hidden') {
    state.topBar.hidden = true;
    state.bottomBar.hidden = true;
    return;
  }

  if (phase === 'waiting') {
    state.topBar.hidden = false;
    state.bottomBar.hidden = true;
    state.topDot.classList.add('deepanalyze-cell-rewrite-dot-working');
    state.topStatusText.textContent = 'waiting';
    return;
  }

  if (phase === 'running') {
    state.topBar.hidden = false;
    state.bottomBar.hidden = true;
    state.topDot.classList.add('deepanalyze-cell-rewrite-dot-working');
    state.topStatusText.textContent = '生成中…';
    return;
  }

  // done
  // 为避免偶发残留，结束后直接移除顶部停止条（底部接受/回退条会出现）。
  try {
    state.topBar.hidden = true;
    state.topBar.remove();
  } catch {
    // ignore
  }
  try {
    const leftovers = state.root.querySelectorAll('.deepanalyze-cell-rewrite-topbar');
    leftovers.forEach(node => node.remove());
  } catch {
    // ignore
  }
  state.bottomBar.hidden = false;
  state.topDot.classList.remove('deepanalyze-cell-rewrite-dot-working');
  state.bottomStatusText.textContent = '已生成改写结果';
}

function buildInstructionDialogBody(): { widget: Widget; textarea: HTMLTextAreaElement } {
  const body = document.createElement('div');
  body.style.display = 'flex';
  body.style.flexDirection = 'column';
  body.style.gap = '8px';
  body.style.minWidth = '420px';

  const hint = document.createElement('div');
  hint.textContent = '请输入对该单元格的修改指令：';
  body.appendChild(hint);

  const textarea = document.createElement('textarea');
  textarea.rows = 5;
  textarea.placeholder = '例如：把这段代码改成使用 pandas 读取 CSV，并输出前 5 行…';
  textarea.style.width = '100%';
  textarea.style.boxSizing = 'border-box';
  body.appendChild(textarea);

  return { widget: new Widget({ node: body }), textarea };
}

function stripLeadingLanguageWrappers(state: { buf: string; done: boolean }, delta: string): string {
  if (state.done) {
    return delta;
  }

  state.buf += String(delta ?? '');

  // 等待首行完整出现再判断（避免 ```python 被切成多段）
  if (!state.buf.includes('\n') && state.buf.length < 120) {
    return '';
  }

  let s = state.buf.replace(/\r\n/g, '\n');
  for (;;) {
    const trimmed = s.replace(/^\s+/, '');
    const lower = trimmed.toLowerCase();
    if (lower.startsWith('[python]')) {
      s = trimmed.slice('[python]'.length);
      s = s.replace(/^\s*\n?/, '');
      continue;
    }
    if (lower.startsWith('[py]')) {
      s = trimmed.slice('[py]'.length);
      s = s.replace(/^\s*\n?/, '');
      continue;
    }

    if (trimmed.startsWith('```')) {
      const lineEnd = trimmed.indexOf('\n');
      if (lineEnd < 0) {
        // 还没有完整的围栏行，继续等待
        state.buf = trimmed;
        return '';
      }
      const firstLine = trimmed.slice(0, lineEnd).trim().toLowerCase();
      if (firstLine === '```' || firstLine === '```python' || firstLine === '```py') {
        s = trimmed.slice(lineEnd + 1);
        continue;
      }
    }

    break;
  }

  state.done = true;
  state.buf = '';
  return s;
}

export function installScratchCellRewriteUI(
  app: JupyterFrontEnd
): DisposableDelegate {
  let running = false;
  let lastContextCellNode: HTMLElement | null = null;

  const commandId = 'deepanalyze:cell-llm-edit';
  const has = (app.commands as any).hasCommand?.(commandId) ?? false;
  if (has) {
    return new DisposableDelegate(() => undefined);
  }

  const findNotebook = (): AnyNotebook | null => {
    const widget: any = app.shell.currentWidget as any;
    const notebook = widget?.content ?? null;
    if (!notebook?.widgets || !notebook?.activeCell) {
      return null;
    }
    return notebook as AnyNotebook;
  };

  const findCellByNode = (notebook: AnyNotebook, node: HTMLElement | null): AnyCell | null => {
    if (!node) {
      return notebook?.activeCell ?? null;
    }
    const cells: AnyCell[] = notebook.widgets ?? [];
    for (const cell of cells) {
      const root = getCellRoot(cell);
      if (!root) continue;
      if (root === node || root.contains(node)) {
        return cell;
      }
    }
    return notebook?.activeCell ?? null;
  };

  const onContextMenu = (ev: MouseEvent) => {
    try {
      const target = ev.target as HTMLElement | null;
      if (!target) return;
      const cellNode = target.closest('.jp-Notebook .jp-Cell') as HTMLElement | null;
      if (!cellNode) return;
      lastContextCellNode = cellNode;
    } catch {
      // ignore
    }
  };
  document.addEventListener('contextmenu', onContextMenu, true);

  app.commands.addCommand(commandId, {
    label: '使用大模型编辑',
    caption: '用自然语言指令改写当前单元格内容',
    isVisible: () => Boolean(findNotebook()),
    isEnabled: () => Boolean(findNotebook()) && !running,
    execute: async () => {
      const notebook = findNotebook();
      if (!notebook) {
        return;
      }
      const cell = findCellByNode(notebook, lastContextCellNode);
      if (!cell) {
        void showErrorMessage('DeepAnalyze', '未找到当前选中的单元格。');
        return;
      }

      const existingBars = cellBars.get(cell) ?? null;
      if (existingBars && existingBars.phase === 'done' && existingBars.originalSource != null) {
        void showErrorMessage('DeepAnalyze', '该单元格有未确认的改写结果，请先接受或回退。');
        return;
      }

      const { widget, textarea } = buildInstructionDialogBody();
      const result = await showDialog({
        title: '使用大模型编辑单元格',
        body: widget,
        buttons: [Dialog.cancelButton({ label: '取消' }), Dialog.okButton({ label: '确定' })],
        focusNodeSelector: 'textarea'
      });

      if (!result.button.accept) {
        disposeRewriteBars(cell);
        return;
      }

      const instruction = String(textarea.value ?? '').trim();
      if (!instruction) {
        disposeRewriteBars(cell);
        return;
      }

      const source = getCellSource(cell);
      const cell_type = getCellType(cell) || undefined;
      const execution_result = getCodeCellExecutionResult(cell) || undefined;
      const bars = ensureRewriteBars(cell);
      running = true;
      if (bars) {
        bars.originalSource = source;
        bars.abortController = new AbortController();
        setBarsPhase(bars, 'waiting');
      }
      setCellSource(cell, 'waiting');

      try {
        let rendered = '';
        let pending = '';
        let raf = 0;
        let canceled = false;
        let gotFinal = false;
        const flush = () => {
          raf = 0;
          if (!pending) return;
          rendered += pending;
          pending = '';
          setCellSource(cell, rendered);
        };

        const leading = { buf: '', done: false };
        rendered = '';
        let started = false;

        try {
          if (bars) {
            bars.stopButton.onclick = ev => {
              ev?.preventDefault?.();
              ev?.stopPropagation?.();
              if (canceled) return;
              canceled = true;
              try {
                bars.abortController?.abort();
              } catch {
                // ignore
              }
              if (raf) {
                try {
                  cancelAnimationFrame(raf);
                } catch {
                  // ignore
                }
                raf = 0;
              }
              pending = '';
              rendered = '';
              try {
                if (bars.originalSource != null) {
                  setCellSource(cell, bars.originalSource);
                }
              } catch {
                // ignore
              }
              bars.abortController = null;
              bars.originalSource = null;
              setBarsPhase(bars, 'hidden');
              disposeRewriteBars(cell);
              running = false;
            };

            bars.acceptButton.onclick = ev => {
              ev?.preventDefault?.();
              ev?.stopPropagation?.();
              bars.abortController = null;
              bars.originalSource = null;
              setBarsPhase(bars, 'hidden');
              disposeRewriteBars(cell);
            };

            bars.rollbackButton.onclick = ev => {
              ev?.preventDefault?.();
              ev?.stopPropagation?.();
              try {
                if (bars.originalSource != null) {
                  setCellSource(cell, bars.originalSource);
                }
              } catch {
                // ignore
              }
              bars.abortController = null;
              bars.originalSource = null;
              setBarsPhase(bars, 'hidden');
              disposeRewriteBars(cell);
            };
          }

          for await (const event of streamRewriteCellSource({
            source,
            instruction,
            cell_type,
            execution_result,
            model_id: getDeepAnalyzeItem('modelId') || undefined,
            signal: bars?.abortController?.signal
          })) {
            if (event.type === 'start') {
              started = true;
              rendered = '';
              pending = '';
              setCellSource(cell, '');
              if (bars) {
                setBarsPhase(bars, 'running');
              }
              continue;
            }
            if (event.type === 'delta') {
              if (!started) {
                started = true;
                rendered = '';
                pending = '';
                setCellSource(cell, '');
                if (bars) {
                  setBarsPhase(bars, 'running');
                }
              }
              const nextDelta = stripLeadingLanguageWrappers(leading, event.delta);
              if (!nextDelta) continue;
              pending += nextDelta;
              if (!raf) {
                raf = requestAnimationFrame(flush);
              }
              continue;
            }
            if (event.type === 'final') {
              gotFinal = true;
              if (raf) {
                cancelAnimationFrame(raf);
                raf = 0;
              }
              flush();
              const finalAnswer = String(event.response?.answer ?? '').replace(/\r\n/g, '\n');
              if (finalAnswer) {
                setCellSource(cell, finalAnswer);
              }
              if (bars) {
                bars.abortController = null;
                setBarsPhase(bars, 'done');
              }
              return;
            }
          }

          if (!canceled && !gotFinal) {
            throw new Error('cell rewrite stream ended without final');
          }
        } catch (error) {
          const aborted =
            canceled ||
            Boolean(bars?.abortController?.signal?.aborted) ||
            String((error as any)?.name ?? '') === 'AbortError';
          if (aborted) {
            return;
          }
          if (bars) {
            setBarsPhase(bars, 'running');
          }
          const response = await rewriteCellSource({
            source,
            instruction,
            cell_type,
            execution_result,
            model_id: getDeepAnalyzeItem('modelId') || undefined,
            signal: bars?.abortController?.signal
          });
          const next = String(response?.answer ?? '').replace(/\r\n/g, '\n');
          setCellSource(cell, next);
          if (bars) {
            bars.abortController = null;
            setBarsPhase(bars, 'done');
          }
          return;
        } finally {
          if (raf) {
            cancelAnimationFrame(raf);
          }
        }
      } catch (error) {
        try {
          setCellSource(cell, source);
        } catch {
          // ignore
        }
        if (bars) {
          bars.abortController = null;
          bars.originalSource = null;
          setBarsPhase(bars, 'hidden');
        }
        void showErrorMessage('DeepAnalyze', `单元格改写失败：${String(error)}`);
      } finally {
        running = false;
      }
    }
  });

  const menuDisposable = (app.contextMenu as any).addItem?.({
    command: commandId,
    selector: '.jp-Notebook .jp-Cell',
    rank: 80
  });

  return new DisposableDelegate(() => {
    try {
      document.removeEventListener('contextmenu', onContextMenu, true);
    } catch {
      // ignore
    }
    try {
      menuDisposable?.dispose?.();
    } catch {
      // ignore
    }
    try {
      (app.commands as any).removeCommand?.(commandId);
    } catch {
      // ignore
    }
  });
}
