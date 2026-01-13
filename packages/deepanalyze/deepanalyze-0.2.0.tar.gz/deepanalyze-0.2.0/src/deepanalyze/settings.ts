export interface IDeepAnalyzeSettings {
  workspacesRoot?: string;
  maxAutoFeedbackTurns?: number;
}

// 源码默认值：可在此处直接修改默认配置（localStorage 仍可覆盖）。
export const DEFAULT_DEEPANALYZE_SETTINGS: Required<IDeepAnalyzeSettings> = {
  // 对应 Jupyter Contents API 的 server-root 相对路径（不是 OS 绝对路径）。
  workspacesRoot: 'DeepAnalyze/workspaces',
  // 自动回环最大轮数（反馈-继续）默认 50。
  maxAutoFeedbackTurns: 50
};

const SETTINGS_KEY = 'deepanalyze.settings';

const LEGACY_WORKSPACES_ROOT_KEY = 'deepanalyze.workspacesRoot';

function safeParseJson(raw: string): unknown {
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function readSettingsObject(): Record<string, unknown> {
  try {
    const raw = window.localStorage.getItem(SETTINGS_KEY);
    if (!raw) {
      return {};
    }
    const parsed = safeParseJson(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return {};
    }
    return parsed as Record<string, unknown>;
  } catch {
    return {};
  }
}

function readLegacyString(key: string): string | undefined {
  try {
    const raw = window.localStorage.getItem(key);
    const v = String(raw ?? '').trim();
    return v ? v : undefined;
  } catch {
    return undefined;
  }
}

function readLegacyNumber(key: string): number | undefined {
  try {
    const raw = window.localStorage.getItem(key);
    if (raw == null) {
      return undefined;
    }
    const num = Number(raw);
    return Number.isFinite(num) ? num : undefined;
  } catch {
    return undefined;
  }
}

export function getDeepAnalyzeSettings(): IDeepAnalyzeSettings {
  const obj = readSettingsObject();
  const workspacesRootCandidate =
    (typeof obj.workspacesRoot === 'string' ? obj.workspacesRoot : undefined) ??
    readLegacyString(LEGACY_WORKSPACES_ROOT_KEY) ??
    DEFAULT_DEEPANALYZE_SETTINGS.workspacesRoot;

  const maxAutoFeedbackTurnsCandidate =
    (typeof obj.maxAutoFeedbackTurns === 'number' ? obj.maxAutoFeedbackTurns : undefined) ??
    readLegacyNumber('deepanalyze.maxAutoFeedbackTurns') ??
    DEFAULT_DEEPANALYZE_SETTINGS.maxAutoFeedbackTurns;

  const workspacesRoot = String(workspacesRootCandidate ?? '').trim() || undefined;
  const maxAutoFeedbackTurnsRaw = Number(maxAutoFeedbackTurnsCandidate);
  const maxAutoFeedbackTurns =
    Number.isFinite(maxAutoFeedbackTurnsRaw) && maxAutoFeedbackTurnsRaw > 0
      ? Math.floor(maxAutoFeedbackTurnsRaw)
      : DEFAULT_DEEPANALYZE_SETTINGS.maxAutoFeedbackTurns;

  return {
    workspacesRoot,
    maxAutoFeedbackTurns
  };
}

export function updateDeepAnalyzeSettings(patch: Partial<IDeepAnalyzeSettings>): void {
  const current = getDeepAnalyzeSettings();
  const next: IDeepAnalyzeSettings = { ...current, ...patch };
  try {
    window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(next));
  } catch {
    // ignore quota / unavailable
  }
}
