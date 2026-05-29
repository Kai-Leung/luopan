import React from 'react';
import { safeGetBootStage, safeGetRenderStage, safeReload } from './utils/browserSafe';

type AppErrorBoundaryProps = {
  children: React.ReactNode;
};

type AppErrorBoundaryState = {
  hasError: boolean;
  errorName: string;
  errorMessage: string;
  renderStage: string;
  bootStage: string;
};

export class AppErrorBoundary extends React.Component<AppErrorBoundaryProps, AppErrorBoundaryState> {
  state: AppErrorBoundaryState = {
    hasError: false,
    errorName: '',
    errorMessage: '',
    renderStage: '',
    bootStage: '',
  };

  static getDerivedStateFromError(error: unknown): AppErrorBoundaryState {
    return {
      hasError: true,
      errorName: getSafeErrorName(error),
      errorMessage: getSafeErrorMessage(error),
      renderStage: safeGetRenderStage(),
      bootStage: safeGetBootStage(),
    };
  }

  componentDidCatch(error: unknown): void {
    this.setState({
      hasError: true,
      errorName: getSafeErrorName(error),
      errorMessage: getSafeErrorMessage(error),
      renderStage: safeGetRenderStage(),
      bootStage: safeGetBootStage(),
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 20, fontFamily: 'sans-serif', textAlign: 'center' }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>⚠️</div>
          <h2 style={{ color: '#c00', margin: '0 0 12px' }}>页面加载失败</h2>
          <p style={{ color: '#666', lineHeight: 1.6 }}>
            启动组件时出现错误。请{' '}
            <button
              onClick={safeReload}
              style={{
                background: '#1890ff',
                color: '#fff',
                border: 'none',
                borderRadius: 4,
                padding: '6px 16px',
                fontSize: 14,
                cursor: 'pointer',
              }}
            >
              刷新页面
            </button>
          </p>
          <div
            style={{
              background: '#fff7f7',
              border: '1px solid #f1b4b4',
              borderRadius: 8,
              color: '#4d1f1f',
              fontSize: 14,
              lineHeight: 1.7,
              marginTop: 16,
              padding: 12,
              textAlign: 'left',
              wordBreak: 'break-word',
            }}
          >
            <div><strong>错误类型：</strong>{this.state.errorName || 'UnknownError'}</div>
            <div><strong>错误信息：</strong>{this.state.errorMessage || '未捕获渲染异常，但未提供错误信息'}</div>
            <div><strong>当前阶段：</strong>{this.state.renderStage || '未知阶段'}</div>
            <div><strong>最近阶段：</strong>{this.state.bootStage || '未知阶段'}</div>
          </div>
          <p style={{ color: '#999', fontSize: 12 }}>如持续出现，请联系支持</p>
        </div>
      );
    }
    return this.props.children;
  }
}

function getSafeErrorName(error: unknown): string {
  if (error instanceof Error && error.name.trim()) {
    return sanitizeErrorText(error.name, 40);
  }
  return 'UnknownError';
}

function getSafeErrorMessage(error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return sanitizeErrorText(error.message, 180);
  }
  return '未捕获渲染异常，但未提供错误信息';
}

function sanitizeErrorText(value: string, maxLength: number): string {
  return value
    .replace(/\/Users\/[^ "'\n]+/g, '[path]')
    .replace(/[A-Za-z]:\\[^ "'\n]+/g, '[path]')
    .replace(/(api[_-]?key|token|secret|password)=([^&\s]+)/gi, '$1=[redacted]')
    .slice(0, maxLength);
}
