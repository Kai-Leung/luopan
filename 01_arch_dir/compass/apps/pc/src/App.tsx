import { FormEvent, useCallback, useEffect, useMemo, useState } from 'react';

import {
  fetchFacts,
  fetchPendingConfirmations,
  fetchRuntimeContext,
  reviewPending,
  type FactListItem,
  type PendingConfirmation,
  type RuntimeContext,
} from './api';

type View = 'pending' | 'facts' | 'permissions';
type ReviewAction = 'confirm' | 'return_for_completion' | 'reject';

const VIEW_LABELS: Record<View, string> = {
  pending: '待处理中心',
  facts: '正式事实',
  permissions: '权限范围',
};

export default function App() {
  const [view, setView] = useState<View>('pending');
  const [context, setContext] = useState<RuntimeContext | null>(null);
  const [pending, setPending] = useState<PendingConfirmation[]>([]);
  const [facts, setFacts] = useState<FactListItem[]>([]);
  const [factTotal, setFactTotal] = useState(0);
  const [keyword, setKeyword] = useState('');
  const [busyId, setBusyId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadAll = useCallback(async (searchKeyword = '') => {
    setLoading(true);
    setError('');
    try {
      const [nextContext, nextPending, nextFacts] = await Promise.all([
        fetchRuntimeContext(),
        fetchPendingConfirmations(),
        fetchFacts(searchKeyword),
      ]);
      setContext(nextContext);
      setPending(nextPending);
      setFacts(nextFacts.items);
      setFactTotal(nextFacts.total);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : '工作台加载失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadAll();
  }, [loadAll]);

  const reviewedCount = useMemo(
    () => pending.filter((item) => item.governance_status === 'needs_confirmation').length,
    [pending],
  );

  async function handleReview(item: PendingConfirmation, action: ReviewAction) {
    if (!context || busyId) {
      return;
    }
    setBusyId(item.pending_id);
    setError('');
    setMessage('');
    try {
      await reviewPending(item, action, context.user_id);
      setMessage(
        action === 'confirm'
          ? '确认完成，正式事实以 L2 返回结果为准。'
          : '处理结果已记录，未创建正式事实。',
      );
      await loadAll(keyword);
    } catch (reviewError) {
      setError(reviewError instanceof Error ? reviewError.message : '处理失败');
    } finally {
      setBusyId(null);
    }
  }

  function handleSearch(event: FormEvent) {
    event.preventDefault();
    void loadAll(keyword);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="product-kicker">COMPASS</p>
          <h1>罗盘治理工作台</h1>
        </div>
        <div className="identity">
          <strong>{context?.organization_name ?? '运行上下文加载中'}</strong>
          <span>{context ? `${context.user_display_name} · ${context.role_names.join(' / ')}` : ''}</span>
        </div>
      </header>

      <div className="workspace">
        <aside className="sidebar" aria-label="主导航">
          <nav>
            {(Object.keys(VIEW_LABELS) as View[]).map((item) => (
              <button
                className={view === item ? 'nav-button active' : 'nav-button'}
                key={item}
                onClick={() => setView(item)}
                type="button"
              >
                <span>{VIEW_LABELS[item]}</span>
                {item === 'pending' && <b>{pending.length}</b>}
              </button>
            ))}
          </nav>
          <div className="scope-summary">
            <span>运行范围</span>
            <strong>{context?.context_source === 'controlled_claim' ? '受控声明' : '开发基线'}</strong>
            <small>{context?.context_id ?? '-'}</small>
          </div>
        </aside>

        <main className="content">
          <div className="content-heading">
            <div>
              <p>{view === 'pending' ? `${reviewedCount} 项需要人工确认` : '后端正式状态'}</p>
              <h2>{VIEW_LABELS[view]}</h2>
            </div>
            <button className="secondary-button" onClick={() => void loadAll(keyword)} type="button">
              刷新
            </button>
          </div>

          {error && <div className="notice error" role="alert">{error}</div>}
          {message && <div className="notice success" role="status">{message}</div>}
          {loading && <div className="loading">正在读取后端状态...</div>}

          {!loading && view === 'pending' && (
            <section className="table-section" aria-label="待处理事项">
              {pending.length === 0 ? (
                <div className="empty-state">当前没有待人工确认事项。</div>
              ) : (
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>事项</th>
                        <th>事实类型</th>
                        <th>治理状态</th>
                        <th>进入时间</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pending.map((item) => (
                        <tr key={item.pending_id}>
                          <td>
                            <strong>{item.display_text}</strong>
                            <small>{item.candidate_id}</small>
                          </td>
                          <td>{item.fact_type}</td>
                          <td><span className="status warning">{item.governance_status}</span></td>
                          <td>{formatDate(item.created_at)}</td>
                          <td>
                            <div className="actions">
                              <button
                                className="primary-button"
                                disabled={busyId !== null}
                                onClick={() => void handleReview(item, 'confirm')}
                                type="button"
                              >
                                确认
                              </button>
                              <button
                                className="secondary-button"
                                disabled={busyId !== null}
                                onClick={() => void handleReview(item, 'return_for_completion')}
                                type="button"
                              >
                                待补
                              </button>
                              <button
                                className="danger-button"
                                disabled={busyId !== null}
                                onClick={() => void handleReview(item, 'reject')}
                                type="button"
                              >
                                驳回
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          )}

          {!loading && view === 'facts' && (
            <section className="table-section" aria-label="正式事实">
              <form className="search-row" onSubmit={handleSearch}>
                <input
                  aria-label="搜索正式事实"
                  onChange={(event) => setKeyword(event.target.value)}
                  placeholder="按正式事实内容搜索"
                  value={keyword}
                />
                <button className="primary-button" type="submit">查询</button>
                <span>共 {factTotal} 条</span>
              </form>
              {facts.length === 0 ? (
                <div className="empty-state">没有符合条件的正式事实。</div>
              ) : (
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>事实编号</th>
                        <th>事实类型</th>
                        <th>摘要</th>
                        <th>来源</th>
                        <th>状态</th>
                        <th>创建时间</th>
                      </tr>
                    </thead>
                    <tbody>
                      {facts.map((fact) => (
                        <tr key={fact.fact_id}>
                          <td><code>{fact.fact_id}</code></td>
                          <td>{fact.fact_type}</td>
                          <td className="summary-cell">{fact.fact_payload_summary}</td>
                          <td>{fact.source_type}</td>
                          <td><span className="status active">{fact.fact_status}</span></td>
                          <td>{formatDate(fact.created_at)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          )}

          {!loading && view === 'permissions' && (
            <section className="permission-section" aria-label="权限范围">
              <dl>
                <div><dt>用户</dt><dd>{context?.user_display_name}</dd></div>
                <div><dt>组织</dt><dd>{context?.organization_name}</dd></div>
                <div><dt>角色</dt><dd>{context?.role_names.join(' / ')}</dd></div>
                <div><dt>上下文来源</dt><dd>{context?.context_source}</dd></div>
              </dl>
              <div className="permission-list">
                {context?.allowed_actions.map((action) => (
                  <span key={action}>{action}</span>
                ))}
              </div>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}

function formatDate(value: string): string {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
}
