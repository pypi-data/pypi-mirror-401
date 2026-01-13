import { PageConfig } from '@jupyterlab/coreutils';

function normalizeScope(raw: string): string {
  const trimmed = String(raw ?? '').trim();
  if (!trimmed) {
    return '/';
  }
  const withLeadingSlash = trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
  const withoutTrailingSlash = withLeadingSlash.replace(/\/+$/, '');
  return withoutTrailingSlash || '/';
}

export function deepAnalyzeScopeId(): string {
  try {
    return normalizeScope(PageConfig.getBaseUrl());
  } catch {
    return '/';
  }
}

export function deepAnalyzeStorageKey(name: string): string {
  const scope = deepAnalyzeScopeId();
  return `deepanalyze.${name}@${scope}`;
}

export function getDeepAnalyzeItem(name: string): string {
  try {
    return window.localStorage.getItem(deepAnalyzeStorageKey(name)) ?? '';
  } catch {
    return '';
  }
}

export function setDeepAnalyzeItem(name: string, value: string): void {
  try {
    window.localStorage.setItem(deepAnalyzeStorageKey(name), String(value ?? ''));
  } catch {
    // ignore quota / unavailable
  }
}

export function removeDeepAnalyzeItem(name: string): void {
  try {
    window.localStorage.removeItem(deepAnalyzeStorageKey(name));
  } catch {
    // ignore
  }
}

