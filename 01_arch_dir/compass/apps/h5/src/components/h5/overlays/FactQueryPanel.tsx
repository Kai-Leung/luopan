import React, { useState, useEffect, useCallback } from 'react';
import type { L3FactListResponse, L3FactViewResponse } from '../../../modules/facts_view/types';

const L3_BASE = "/api/v1/l3/facts";

async function listL3Facts(params?: {
  fact_type?: string;
  keyword?: string;
  limit?: number;
  offset?: number;
}): Promise<L3FactListResponse> {
  const query = new URLSearchParams();
  if (params?.fact_type) query.set("fact_type", params.fact_type);
  if (params?.keyword) query.set("keyword", params.keyword);
  if (params?.limit !== undefined) query.set("limit", String(params.limit));
  if (params?.offset !== undefined) query.set("offset", String(params.offset));
  const qs = query.toString();
  const url = qs ? `${L3_BASE}?${qs}` : L3_BASE;
  const res = await fetch(url);
  if (!res.ok) throw new Error("事实列表加载失败");
  return res.json();
}

async function getL3FactDetail(factId: string): Promise<L3FactViewResponse> {
  const res = await fetch(`${L3_BASE}/${encodeURIComponent(factId)}`);
  if (!res.ok) throw new Error("事实加载失败");
  return res.json();
}

interface FactQueryPanelProps {
  onClose: () => void;
}

export default function FactQueryPanel({ onClose }: FactQueryPanelProps) {
  const [items, setItems] = useState<L3FactListResponse['items']>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterKeyword, setFilterKeyword] = useState('');
  const [selectedFact, setSelectedFact] = useState<L3FactViewResponse | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const loadList = useCallback(async (appended = false) => {
    setLoading(true);
    setError('');
    try {
      const offset = appended ? items.length : 0;
      const res = await listL3Facts({
        fact_type: filterType || undefined,
        keyword: filterKeyword || undefined,
        limit: 20,
        offset,
      });
      setItems(appended ? [...items, ...res.items] : res.items);
      setTotal(res.total);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载失败');
    } finally {
      setLoading(false);
    }
  }, [filterType, filterKeyword, items]);

  useEffect(() => {
    loadList();
  }, []);

  const handleSearch = () => {
    loadList();
  };

  const handleViewDetail = async (factId: string) => {
    setDetailLoading(true);
    setSelectedFact(null);
    try {
      const detail = await getL3FactDetail(factId);
      setSelectedFact(detail);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载失败');
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="h5-overlay-panel fact-query-panel">
      <div className="h5-overlay-header">
        <span className="h5-overlay-title">事实查询</span>
        <span className="h5-notice-bar">只读查询，不产生正式事实</span>
        <button className="h5-overlay-close" onClick={onClose}>关闭</button>
      </div>

      {/* 筛选栏 */}
      <div className="fact-query-filters">
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="fact-filter-select"
        >
          <option value="">全部类型</option>
          <option value="construction_record">施工记录</option>
          <option value="material_record">材料记录</option>
          <option value="other_fact_record">其他记录</option>
        </select>
        <input
          type="text"
          placeholder="搜索关键词..."
          value={filterKeyword}
          onChange={(e) => setFilterKeyword(e.target.value)}
          className="fact-filter-input"
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch} className="fact-filter-btn" disabled={loading}>
          {loading ? '查询中…' : '查询'}
        </button>
      </div>

      {/* 只读提示 */}
      <div className="fact-readonly-banner">
        🔍 只读查询结果 — 不创建、不修改、不删除正式事实
      </div>

      {/* 错误提示 */}
      {error && <div className="fact-error">{error}</div>}

      {/* 空状态 */}
      {!loading && !error && items.length === 0 && (
        <div className="fact-empty-state">
          <p>暂无事实记录</p>
          <p className="fact-empty-hint">提交信息并通过人工确认后，正式事实将在此显示</p>
        </div>
      )}

      {/* 列表 */}
      {items.length > 0 && (
        <div className="fact-list">
          <div className="fact-list-count">共 {total} 条记录</div>
          {items.map((item) => (
            <div
              key={item.fact_id}
              className="fact-list-item"
              onClick={() => handleViewDetail(item.fact_id)}
            >
              <div className="fact-item-header">
                <span className={`fact-type-badge fact-type-${item.fact_type}`}>{item.fact_type}</span>
                <span className="fact-source">{item.source_type}</span>
              </div>
              <div className="fact-item-summary">{item.fact_payload_summary}</div>
              <div className="fact-item-time">{new Date(item.created_at).toLocaleString('zh-CN')}</div>
            </div>
          ))}
        </div>
      )}

      {/* 详情弹窗 */}
      {selectedFact && (
        <div className="fact-detail-overlay" onClick={() => setSelectedFact(null)}>
          <div className="fact-detail-card" onClick={(e) => e.stopPropagation()}>
            <div className="fact-detail-header">
              <span>事实详情</span>
              <button onClick={() => setSelectedFact(null)}>关闭</button>
            </div>
            <div className="fact-detail-body">
              <div className="fact-detail-row">
                <label>ID</label>
                <span>{selectedFact.fact_id}</span>
              </div>
              <div className="fact-detail-row">
                <label>类型</label>
                <span>{selectedFact.fact_type}</span>
              </div>
              <div className="fact-detail-row">
                <label>状态</label>
                <span>{selectedFact.fact_status}</span>
              </div>
              <div className="fact-detail-row">
                <label>创建时间</label>
                <span>{new Date(selectedFact.created_at).toLocaleString('zh-CN')}</span>
              </div>
              <div className="fact-detail-row fact-detail-payload">
                <label>内容</label>
                <pre>{JSON.stringify(selectedFact.fact_payload, null, 2)}</pre>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 加载更多 */}
      {!loading && items.length < total && (
        <button onClick={() => loadList(true)} className="fact-load-more">
          加载更多 ({total - items.length} 条)
        </button>
      )}

      {detailLoading && <div className="fact-loading">加载详情中…</div>}
    </div>
  );
}
