import { PathExt } from '@jupyterlab/coreutils';
import { Contents } from '@jupyterlab/services';

export const DEFAULT_DEEPANALYZE_ROOT = 'DeepAnalyze';
export const DEFAULT_DEEPANALYZE_WORKSPACES_ROOT = `${DEFAULT_DEEPANALYZE_ROOT}/workspaces`;

function formatTimestampForPath(date: Date): string {
  const pad2 = (value: number) => String(value).padStart(2, '0');
  const year = date.getFullYear();
  const month = pad2(date.getMonth() + 1);
  const day = pad2(date.getDate());
  const hour = pad2(date.getHours());
  const minute = pad2(date.getMinutes());
  const second = pad2(date.getSeconds());
  return `${year}${month}${day}-${hour}${minute}${second}`;
}

async function pathExists(
  contents: Contents.IManager,
  path: string
): Promise<boolean> {
  try {
    await contents.get(path, { content: false });
    return true;
  } catch {
    return false;
  }
}

async function waitForDirectory(
  contents: Contents.IManager,
  path: string,
  options?: { retries?: number; delayMs?: number }
): Promise<void> {
  const retries = Math.max(0, Number(options?.retries ?? 10));
  const delayMs = Math.max(0, Number(options?.delayMs ?? 150));
  let lastError: unknown = null;

  for (let i = 0; i <= retries; i++) {
    try {
      const model = await contents.get(path, { content: false });
      if (model.type !== 'directory') {
        throw new Error(`目标路径不是目录：${path}`);
      }
      return;
    } catch (error: any) {
      lastError = error;
      const status = Number(error?.response?.status);
      // 仅对“偶发 not found”做重试，其他错误直接抛出。
      if (status !== 404 || i >= retries) {
        throw lastError;
      }
      await new Promise<void>(resolve => setTimeout(resolve, delayMs));
    }
  }

  throw lastError ?? new Error(`等待目录可见超时：${path}`);
}

async function ensureDirectory(
  contents: Contents.IManager,
  fullPath: string
): Promise<void> {
  if (!fullPath || fullPath === '.') {
    return;
  }

  if (await pathExists(contents, fullPath)) {
    return;
  }

  const parentRaw = PathExt.dirname(fullPath);
  const parent = parentRaw === '.' ? '' : parentRaw;
  const name = PathExt.basename(fullPath);

  await ensureDirectory(contents, parent);

  const temp = await contents.newUntitled({ path: parent, type: 'directory' });
  const target = parent ? PathExt.join(parent, name) : name;
  try {
    await contents.rename(temp.path, target);
  } catch {
    // 可能是目录已存在但短暂不可见（或并发创建），兜底等待目标目录可见。
    await waitForDirectory(contents, target, { retries: 12, delayMs: 150 });
    return;
  }

  // 目录创建/重命名后偶发短暂不可见，进入工作区前先等待可见。
  await waitForDirectory(contents, target, { retries: 12, delayMs: 150 });
}

function safeWorkspaceRoot(): string {
  return DEFAULT_DEEPANALYZE_WORKSPACES_ROOT;
}

export async function createDeepAnalyzeWorkspace(
  contents: Contents.IManager
): Promise<string> {
  const root = safeWorkspaceRoot();
  await ensureDirectory(contents, root);

  const timestamp = formatTimestampForPath(new Date());
  const random = Math.random().toString(16).slice(2, 8);
  const workspaceName = `ws-${timestamp}-${random}`;

  const temp = await contents.newUntitled({ path: root, type: 'directory' });
  const workspacePath = PathExt.join(root, workspaceName);
  try {
    await contents.rename(temp.path, workspacePath);
  } catch {
    await waitForDirectory(contents, workspacePath, { retries: 12, delayMs: 150 });
    return workspacePath;
  }
  await waitForDirectory(contents, workspacePath, { retries: 12, delayMs: 150 });

  return workspacePath;
}

export async function ensureDirectoryPath(
  contents: Contents.IManager,
  fullPath: string
): Promise<void> {
  await ensureDirectory(contents, fullPath);
}

export function sanitizeWorkspaceName(raw: string): string {
  const trimmed = String(raw ?? '').trim();
  if (!trimmed) {
    return '';
  }

  const withoutSeparators = trimmed.replace(/[\\/]/g, '-').replace(/\s+/g, ' ');
  const withoutLeadingDots = withoutSeparators.replace(/^\.+/, '');
  const cleaned = withoutLeadingDots.trim();
  if (!cleaned || cleaned === '.' || cleaned === '..') {
    return '';
  }
  return cleaned;
}

export async function ensureNamedDeepAnalyzeWorkspace(
  contents: Contents.IManager,
  name: string
): Promise<string> {
  return ensureNamedWorkspace(contents, safeWorkspaceRoot(), name);
}

export async function ensureNamedWorkspace(
  contents: Contents.IManager,
  workspacesRoot: string,
  name: string
): Promise<string> {
  const safeName = sanitizeWorkspaceName(name);
  if (!safeName) {
    throw new Error('Invalid workspace name');
  }

  await ensureDirectory(contents, workspacesRoot);

  const target = PathExt.join(workspacesRoot, safeName);
  if (await pathExists(contents, target)) {
    const model = await contents.get(target, { content: false });
    if (model.type !== 'directory') {
      throw new Error(`Workspace path exists and is not a directory: ${target}`);
    }
    return target;
  }

  await ensureDirectory(contents, target);
  return target;
}

export async function listDeepAnalyzeWorkspaces(
  contents: Contents.IManager
): Promise<string[]> {
  return listWorkspaces(contents, safeWorkspaceRoot());
}

export async function listWorkspaces(
  contents: Contents.IManager,
  workspacesRoot: string
): Promise<string[]> {
  await ensureDirectory(contents, workspacesRoot);

  try {
    const model = await contents.get(workspacesRoot, { content: true });
    const items = (model.content ?? []) as Contents.IModel[];
    return items
      .filter(item => item.type === 'directory')
      .map(item => PathExt.basename(item.path))
      .sort((a, b) => a.localeCompare(b, 'zh-Hans-CN'));
  } catch {
    return [];
  }
}
