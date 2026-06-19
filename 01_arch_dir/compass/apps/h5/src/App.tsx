import React, { lazy, Suspense } from 'react';
import { AppErrorBoundary } from './AppErrorBoundary';
import { safeSetBootStage, safeSetRenderStage } from './utils/browserSafe';

const H5MainPage = lazy(() => import('./pages/H5MainPage'));

function App() {
  safeSetBootStage('App 组件已进入渲染');
  safeSetRenderStage('App 开始渲染');
  safeSetRenderStage('App 主页面加载');
  safeSetBootStage('App 主页面加载');

  return (
    <AppErrorBoundary>
      <Suspense fallback={<StartupFallback text="加载中：页面组件加载中" />}>
        <H5MainPage />
      </Suspense>
    </AppErrorBoundary>
  );
}

function StartupFallback({ text }: { text: string }) {
  safeSetRenderStage(text);
  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif', textAlign: 'center', color: '#666' }}>
      {text}
    </div>
  );
}

export default App;
