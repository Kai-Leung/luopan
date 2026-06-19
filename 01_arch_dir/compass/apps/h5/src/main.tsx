import React from 'react';
import { configureNativeRuntime } from './native/runtime';
import { safeSetBootStage } from './utils/browserSafe';

const STARTUP_STYLE = 'padding:20px;font-family:sans-serif;text-align:center;color:#666;';
const STARTUP_ERROR_STYLE = 'padding:20px;font-family:sans-serif;text-align:left;color:#4d1f1f;line-height:1.7;';

function setStartupText(text: string): void {
  safeSetBootStage(text);
  try {
    const root = document.getElementById('root');
    if (root) root.innerHTML = `<div style="${STARTUP_STYLE}">${text}</div>`;
  } catch {
    // 启动诊断兜底，不输出技术细节。
  }
}

function setStartupError(message: string): void {
  safeSetBootStage('页面加载失败提示已显示');
  try {
    const target = document.getElementById('root') || document.body;
    if (target) {
      target.innerHTML = [
        `<div style="${STARTUP_ERROR_STYLE}">`,
        '<h2 style="color:#c00;margin:0 0 12px;">页面加载失败</h2>',
        `<div><strong>错误类型：</strong>StartupError</div>`,
        `<div><strong>错误信息：</strong>${message}</div>`,
        '<div><strong>当前阶段：</strong>React 启动入口</div>',
        '<div><strong>最近阶段：</strong>页面加载失败提示已显示</div>',
        '</div>',
      ].join('');
    }
  } catch {
    // 启动诊断兜底，不输出技术细节。
  }
}

async function bootstrapReactApp(): Promise<void> {
  setStartupText('加载中：JS bundle 已执行');
  void configureNativeRuntime();
  const rootElement = document.getElementById('root');
  if (!rootElement) {
    setStartupError('缺少页面挂载节点');
    return;
  }

  setStartupText('加载中：准备挂载 React');
  const [{ createRoot }, appModule] = await Promise.all([
    import('react-dom/client'),
    import('./App'),
  ]);
  const App = appModule.default;
  setStartupText('加载中：React 已调用 render');
  createRoot(rootElement).render(<App />);
}

try {
  void bootstrapReactApp().catch((error: unknown) => {
    setStartupError(getStartupErrorMessage(error));
  });
} catch (error: unknown) {
  setStartupError(getStartupErrorMessage(error));
}

function getStartupErrorMessage(error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return sanitizeStartupText(error.message);
  }
  return 'React 启动失败，但未提供错误信息';
}

function sanitizeStartupText(value: string): string {
  return value
    .replace(/\/Users\/[^ "'\n]+/g, '[path]')
    .replace(/[A-Za-z]:\\[^ "'\n]+/g, '[path]')
    .replace(/(api[_-]?key|token|secret|password)=([^&\s]+)/gi, '$1=[redacted]')
    .slice(0, 180);
}
