const STORAGE_KEY_PREFIX = 'compass_';

type StageWindow = Window & {
  __COMPASS_RENDER_STAGE__?: string;
  __COMPASS_BOOT_STAGE__?: string;
};

function isBrowser(): boolean {
  return typeof window !== 'undefined';
}

function hasDocument(): boolean {
  return typeof document !== 'undefined';
}

/** 安全获取 DOM 元素，失败返回 null */
export function safeGetElementById(id: string): HTMLElement | null {
  if (!hasDocument()) return null;
  try {
    return document.getElementById(id);
  } catch {
    return null;
  }
}

/** 安全写入 body fallback，失败则静默 */
export function safeSetBodyHTML(html: string): void {
  if (!hasDocument()) return;
  try {
    document.body.innerHTML = html;
  } catch {
    // 静默忽略
  }
}

/** 安全创建对象 URL，失败返回空字符串 */
export function safeCreateObjectURL(value: Blob | MediaSource): string {
  if (!isBrowser() || typeof URL === 'undefined' || typeof URL.createObjectURL !== 'function') {
    return '';
  }
  try {
    return URL.createObjectURL(value);
  } catch {
    return '';
  }
}

/** 安全释放对象 URL */
export function safeRevokeObjectURL(url: string): void {
  if (!url || !isBrowser() || typeof URL === 'undefined' || typeof URL.revokeObjectURL !== 'function') {
    return;
  }
  try {
    URL.revokeObjectURL(url);
  } catch {
    // 静默忽略
  }
}

/** 安全读取 localStorage，失败返回 null */
export function safeGetItem(key: string): string | null {
  if (!isBrowser()) return null;
  try {
    return window.localStorage.getItem(STORAGE_KEY_PREFIX + key);
  } catch {
    return null;
  }
}

/** 安全写入 localStorage，静默失败 */
export function safeSetItem(key: string, value: string): void {
  safeTrySetItem(key, value);
}

/** 安全写入 localStorage，返回是否成功 */
export function safeTrySetItem(key: string, value: string): boolean {
  if (!isBrowser()) return false;
  try {
    window.localStorage.setItem(STORAGE_KEY_PREFIX + key, value);
    return true;
  } catch {
    return false;
  }
}

/** 安全读取 JSON 值，失败返回 null */
export function safeGetJSON<T>(key: string): T | null {
  try {
    const raw = safeGetItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

/** 安全写入 JSON 值 */
export function safeSetJSON(key: string, value: unknown): void {
  try {
    safeSetItem(key, JSON.stringify(value));
  } catch {
    // 静默忽略
  }
}

/** 安全读取 location hash，失败返回空字符串 */
export function safeGetHash(): string {
  if (!isBrowser()) return '';
  try {
    return window.location.hash || '';
  } catch {
    return '';
  }
}

/** 安全添加 hashchange 监听器，返回清理函数 */
export function safeOnHashChange(handler: () => void): () => void {
  if (!isBrowser()) return () => {};
  try {
    window.addEventListener('hashchange', handler);
    return () => {
      try {
        window.removeEventListener('hashchange', handler);
      } catch {
        // 静默忽略
      }
    };
  } catch {
    return () => {};
  }
}

/** 安全添加事件监听器，返回清理函数 */
export function safeAddEventListener<K extends keyof WindowEventMap>(
  type: K,
  handler: (this: Window, ev: WindowEventMap[K]) => void,
  options?: AddEventListenerOptions | boolean,
): () => void {
  if (!isBrowser()) return () => {};
  try {
    window.addEventListener(type, handler, options);
    return () => {
      try {
        window.removeEventListener(type, handler, options);
      } catch {
        // 静默忽略
      }
    };
  } catch {
    return () => {};
  }
}

/** 安全操作 history，失败则静默 */
export function safePushState(state: unknown, title: string, url?: string): void {
  if (!isBrowser()) return;
  try {
    window.history.pushState(state, title, url);
  } catch {
    // 静默忽略
  }
}

/** 安全读取 history state */
export function safeGetHistoryState(): unknown {
  if (!isBrowser()) return null;
  try {
    return window.history.state || {};
  } catch {
    return {};
  }
}

/** 安全刷新页面 */
export function safeReload(): void {
  if (!isBrowser()) return;
  try {
    window.location.reload();
  } catch {
    // 静默忽略
  }
}

/** 安全记录当前 React 渲染阶段 */
export function safeSetRenderStage(stage: string): void {
  if (!isBrowser()) return;
  try {
    (window as StageWindow).__COMPASS_RENDER_STAGE__ = stage;
  } catch {
    // 静默忽略
  }
}

/** 安全读取当前 React 渲染阶段 */
export function safeGetRenderStage(): string {
  if (!isBrowser()) return '未知阶段';
  try {
    return (window as StageWindow).__COMPASS_RENDER_STAGE__ || '未知阶段';
  } catch {
    return '未知阶段';
  }
}

/** 安全记录最近一次启动阶段 */
export function safeSetBootStage(stage: string): void {
  if (!isBrowser()) return;
  try {
    (window as StageWindow).__COMPASS_BOOT_STAGE__ = stage;
  } catch {
    // 静默忽略
  }
}

/** 安全读取最近一次启动阶段 */
export function safeGetBootStage(): string {
  if (!isBrowser()) return '未知阶段';
  try {
    return (window as StageWindow).__COMPASS_BOOT_STAGE__ || '未知阶段';
  } catch {
    return '未知阶段';
  }
}

export type SafeTimerId = ReturnType<typeof setTimeout> | null;

/** 安全设置定时器，失败返回 null */
export function safeSetTimeout(handler: () => void, ms: number): SafeTimerId {
  if (!isBrowser()) return null;
  try {
    return window.setTimeout(handler, ms) as SafeTimerId;
  } catch {
    return null;
  }
}

/** 安全清除定时器 */
export function safeClearTimeout(id: SafeTimerId): void {
  if (id == null) return;
  try {
    window.clearTimeout(id);
  } catch {
    // 静默忽略
  }
}
