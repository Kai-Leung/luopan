import React, { lazy, Suspense, useEffect, useMemo, useState } from 'react';
import { AppErrorBoundary } from './AppErrorBoundary';
import { safeGetHash, safeOnHashChange, safeSetBootStage, safeSetRenderStage } from './utils/browserSafe';

type PageHash = 'h5' | 'mock';

const H5MainPage = lazy(() => import('./pages/H5MainPage'));
const MockPage = lazy(() => import('./pages/MockPage'));

function getPageFromHash(): PageHash {
  return safeGetHash() === '#mock' ? 'mock' : 'h5';
}

function App() {
  safeSetBootStage('App 组件已进入渲染');
  safeSetRenderStage('App 开始渲染');
  const [page, setPage] = useState<PageHash>(() => getPageFromHash());
  const ActivePage = useMemo(() => (page === 'mock' ? MockPage : H5MainPage), [page]);
  safeSetRenderStage('App 路由判断完成');
  safeSetBootStage('App 路由判断完成');

  useEffect(() => {
    return safeOnHashChange(() => setPage(getPageFromHash()));
  }, []);

  return (
    <AppErrorBoundary>
      <Suspense fallback={<StartupFallback text="加载中：页面组件加载中" />}>
        <ActivePage />
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
