import React, { useState, useEffect, useCallback } from 'react';
import type { L3FactListResponse, L3FactViewResponse } from '../../../modules/facts_view/types';
import { getL4AnalysisPreview } from '../../../modules/l4_analysis/api';
import type { L4AnalysisPreviewResponse } from '../../../modules/l4_analysis/types';
import { createL5RecommendationDraft } from '../../../modules/l5_recommendation/api';
import type { L5RecommendationDraftResponse } from '../../../modules/l5_recommendation/types';
import { createL6ExecutionResponse } from '../../../modules/l6_execution/api';
import type { L6ExecutionResponseResponse } from '../../../modules/l6_execution/types';
import { createL7FeedbackCandidate } from '../../../modules/l7_feedback/api';
import type { L7FeedbackResponse } from '../../../modules/l7_feedback/types';

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
  const [analysisPreview, setAnalysisPreview] = useState<L4AnalysisPreviewResponse | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState('');
  const [recommendationDraft, setRecommendationDraft] = useState<L5RecommendationDraftResponse | null>(null);
  const [recommendationLoading, setRecommendationLoading] = useState(false);
  const [recommendationError, setRecommendationError] = useState('');
  const [executionResponse, setExecutionResponse] = useState<L6ExecutionResponseResponse | null>(null);
  const [executionLoading, setExecutionLoading] = useState(false);
  const [executionError, setExecutionError] = useState('');
  const [feedbackCandidate, setFeedbackCandidate] = useState<L7FeedbackResponse | null>(null);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [feedbackError, setFeedbackError] = useState('');

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
    setAnalysisPreview(null);
    setAnalysisError('');
    setRecommendationDraft(null);
    setRecommendationError('');
    setExecutionResponse(null);
    setExecutionError('');
    setFeedbackCandidate(null);
    setFeedbackError('');
    try {
      const detail = await getL3FactDetail(factId);
      setSelectedFact(detail);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载失败');
    } finally {
      setDetailLoading(false);
    }
  };

  const handleLoadAnalysisPreview = async () => {
    if (!selectedFact) return;
    setAnalysisLoading(true);
    setAnalysisError('');
    setAnalysisPreview(null);
    setRecommendationDraft(null);
    setRecommendationError('');
    setExecutionResponse(null);
    setExecutionError('');
    setFeedbackCandidate(null);
    setFeedbackError('');
    try {
      const preview = await getL4AnalysisPreview(selectedFact.fact_id);
      setAnalysisPreview(preview);
    } catch (e: unknown) {
      setAnalysisError(e instanceof Error ? e.message : '分析预览加载失败');
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleCreateRecommendationDraft = async () => {
    if (!analysisPreview) return;
    setRecommendationLoading(true);
    setRecommendationError('');
    setRecommendationDraft(null);
    setExecutionResponse(null);
    setExecutionError('');
    setFeedbackCandidate(null);
    setFeedbackError('');
    try {
      const draft = await createL5RecommendationDraft({
        analysis_id: analysisPreview.analysis_id,
        source_fact_id: analysisPreview.source_fact_id,
        context_payload: { source: 'h5_fact_detail' },
      });
      setRecommendationDraft(draft);
    } catch (e: unknown) {
      setRecommendationError(e instanceof Error ? e.message : '建议草稿生成失败');
    } finally {
      setRecommendationLoading(false);
    }
  };

  const handleCreateExecutionResponse = async () => {
    if (!recommendationDraft) return;
    setExecutionLoading(true);
    setExecutionError('');
    setExecutionResponse(null);
    setFeedbackCandidate(null);
    setFeedbackError('');
    try {
      const response = await createL6ExecutionResponse({
        recommendation_id: recommendationDraft.recommendation_id,
        source_fact_id: recommendationDraft.source_fact_id,
        execution_note: 'H5 已记录对建议草稿的执行响应，待人工后续处理。',
        execution_status: 'recorded',
      });
      setExecutionResponse(response);
    } catch (e: unknown) {
      setExecutionError(e instanceof Error ? e.message : '执行响应记录失败');
    } finally {
      setExecutionLoading(false);
    }
  };

  const handleCreateFeedbackCandidate = async () => {
    if (!executionResponse) return;
    setFeedbackLoading(true);
    setFeedbackError('');
    setFeedbackCandidate(null);
    try {
      const feedback = await createL7FeedbackCandidate({
        execution_response_id: executionResponse.execution_response_id,
        source_fact_id: executionResponse.source_fact_id,
        feedback_note: 'H5 提交的执行响应后续反馈候选，需重新进入候选治理链路。',
        feedback_type: 'follow_up',
      });
      setFeedbackCandidate(feedback);
    } catch (e: unknown) {
      setFeedbackError(e instanceof Error ? e.message : '反馈候选提交失败');
    } finally {
      setFeedbackLoading(false);
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
              <button onClick={() => { setSelectedFact(null); setAnalysisPreview(null); setAnalysisError(''); setRecommendationDraft(null); setRecommendationError(''); setExecutionResponse(null); setExecutionError(''); setFeedbackCandidate(null); setFeedbackError(''); }}>关闭</button>
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
              <div className="l4-analysis-panel">
                <div className="l4-analysis-boundary">分析预览不产生正式事实，不作为最终决策，不写入 L2。</div>
                <button className="l4-analysis-btn" onClick={handleLoadAnalysisPreview} disabled={analysisLoading}>
                  {analysisLoading ? '加载中…' : '查看分析预览'}
                </button>
                {!analysisLoading && !analysisPreview && !analysisError ? (
                  <div className="l4-analysis-empty">暂无分析预览，请点击查看。</div>
                ) : null}
                {analysisError ? <div className="fact-error">{analysisError}</div> : null}
                {analysisPreview ? (
                  <div className="l4-analysis-result">
                    <div className="fact-detail-row">
                      <label>摘要</label>
                      <span>{analysisPreview.analysis_summary}</span>
                    </div>
                    <div className="fact-detail-row">
                      <label>来源</label>
                      <span>{analysisPreview.source_fact_id}</span>
                    </div>
                    <div className="fact-detail-row">
                      <label>只读</label>
                      <span>{String(analysisPreview.readonly)}</span>
                    </div>
                    <div className="fact-detail-row">
                      <label>方向</label>
                      <span>{analysisPreview.processing_direction}</span>
                    </div>
                    <div className="fact-detail-row">
                      <label>追溯</label>
                      <span>{analysisPreview.trace_ref || '未提供'}</span>
                    </div>
                    {analysisPreview.standard_error ? (
                      <div className="fact-detail-row">
                        <label>错误</label>
                        <span>{analysisPreview.standard_error.message}</span>
                      </div>
                    ) : null}
                    <div className="fact-detail-row">
                      <label>时间</label>
                      <span>{new Date(analysisPreview.created_at).toLocaleString('zh-CN')}</span>
                    </div>
                    <div className="l5-recommendation-panel">
                      <div className="l5-recommendation-boundary">建议草稿不代表正式决策，不会自动执行，不写入 L2。</div>
                      <button className="l5-recommendation-btn" onClick={handleCreateRecommendationDraft} disabled={recommendationLoading}>
                        {recommendationLoading ? '生成中…' : '生成建议草稿'}
                      </button>
                      {!recommendationLoading && !recommendationDraft && !recommendationError ? (
                        <div className="l5-recommendation-empty">暂无建议草稿，请点击生成。</div>
                      ) : null}
                      {recommendationError ? <div className="fact-error">{recommendationError}</div> : null}
                      {recommendationDraft ? (
                        <div className="l5-recommendation-result">
                          <div className="fact-detail-row">
                            <label>建议</label>
                            <span>{recommendationDraft.recommendation_summary}</span>
                          </div>
                          <div className="fact-detail-row">
                            <label>状态</label>
                            <span>{recommendationDraft.recommendation_status}</span>
                          </div>
                          <div className="fact-detail-row">
                            <label>执行</label>
                            <span>{String(recommendationDraft.auto_executable)}</span>
                          </div>
                          <div className="fact-detail-row">
                            <label>方向</label>
                            <span>{recommendationDraft.processing_direction}</span>
                          </div>
                          <div className="fact-detail-row">
                            <label>追溯</label>
                            <span>{recommendationDraft.trace_ref || '未提供'}</span>
                          </div>
                          {recommendationDraft.standard_error ? (
                            <div className="fact-detail-row">
                              <label>错误</label>
                              <span>{recommendationDraft.standard_error.message}</span>
                            </div>
                          ) : null}
                          <div className="fact-detail-row">
                            <label>来源</label>
                            <span>{recommendationDraft.source_fact_id || recommendationDraft.analysis_id || '未提供'}</span>
                          </div>
                          <div className="fact-detail-row">
                            <label>时间</label>
                            <span>{new Date(recommendationDraft.created_at).toLocaleString('zh-CN')}</span>
                          </div>
                          <div className="l6-execution-panel">
                            <div className="l6-execution-boundary">执行响应只是记录，不代表事实成立，不会自动入链。</div>
                            <button className="l6-execution-btn" onClick={handleCreateExecutionResponse} disabled={executionLoading}>
                              {executionLoading ? '记录中…' : '记录执行响应'}
                            </button>
                            {!executionLoading && !executionResponse && !executionError ? (
                              <div className="l6-execution-empty">暂无执行响应，请点击记录。</div>
                            ) : null}
                            {executionError ? <div className="fact-error">{executionError}</div> : null}
                            {executionResponse ? (
                              <div className="l6-execution-result">
                                <div className="fact-detail-row">
                                  <label>状态</label>
                                  <span>{executionResponse.execution_status}</span>
                                </div>
                                <div className="fact-detail-row">
                                  <label>说明</label>
                                  <span>{executionResponse.execution_note}</span>
                                </div>
                                <div className="fact-detail-row">
                                  <label>入链</label>
                                  <span>{String(executionResponse.creates_fact)}</span>
                                </div>
                                <div className="fact-detail-row">
                                  <label>方向</label>
                                  <span>{executionResponse.processing_direction}</span>
                                </div>
                                <div className="fact-detail-row">
                                  <label>追溯</label>
                                  <span>{executionResponse.trace_ref || '未提供'}</span>
                                </div>
                                {executionResponse.standard_error ? (
                                  <div className="fact-detail-row">
                                    <label>错误</label>
                                    <span>{executionResponse.standard_error.message}</span>
                                  </div>
                                ) : null}
                                <div className="fact-detail-row">
                                  <label>来源</label>
                                  <span>{executionResponse.recommendation_id || executionResponse.source_fact_id || '未提供'}</span>
                                </div>
                                <div className="fact-detail-row">
                                  <label>时间</label>
                                  <span>{new Date(executionResponse.created_at).toLocaleString('zh-CN')}</span>
                                </div>
                                <div className="l7-feedback-panel">
                                  <div className="l7-feedback-boundary">反馈只是候选回流，不会直接修改正式事实，不会自动写入 L2。</div>
                                  <button className="l7-feedback-btn" onClick={handleCreateFeedbackCandidate} disabled={feedbackLoading}>
                                    {feedbackLoading ? '提交中…' : '提交反馈候选'}
                                  </button>
                                  {!feedbackLoading && !feedbackCandidate && !feedbackError ? (
                                    <div className="l7-feedback-empty">暂无反馈候选，请点击提交。</div>
                                  ) : null}
                                  {feedbackError ? <div className="fact-error">{feedbackError}</div> : null}
                                  {feedbackCandidate ? (
                                    <div className="l7-feedback-result">
                                      <div className="fact-detail-row">
                                        <label>状态</label>
                                        <span>{feedbackCandidate.feedback_status}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>反馈</label>
                                        <span>{feedbackCandidate.feedback_note}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>类型</label>
                                        <span>{feedbackCandidate.feedback_type || '未提供'}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>回流</label>
                                        <span>{String(feedbackCandidate.returns_to_candidate_flow)}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>方向</label>
                                        <span>{feedbackCandidate.processing_direction}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>追溯</label>
                                        <span>{feedbackCandidate.trace_ref || '未提供'}</span>
                                      </div>
                                      {feedbackCandidate.standard_error ? (
                                        <div className="fact-detail-row">
                                          <label>错误</label>
                                          <span>{feedbackCandidate.standard_error.message}</span>
                                        </div>
                                      ) : null}
                                      <div className="fact-detail-row">
                                        <label>来源</label>
                                        <span>{feedbackCandidate.execution_response_id || feedbackCandidate.source_fact_id || '未提供'}</span>
                                      </div>
                                      <div className="fact-detail-row">
                                        <label>时间</label>
                                        <span>{new Date(feedbackCandidate.created_at).toLocaleString('zh-CN')}</span>
                                      </div>
                                    </div>
                                  ) : null}
                                </div>
                              </div>
                            ) : null}
                          </div>
                        </div>
                      ) : null}
                    </div>
                  </div>
                ) : null}
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
