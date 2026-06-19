import type { StandardErrorResult } from '../standard_governance/processing';

export interface L5RecommendationDraftRequest {
  analysis_id?: string;
  source_fact_id?: string;
  context_payload?: Record<string, unknown>;
}

export interface L5RecommendationDraftResponse {
  recommendation_id: string;
  recommendation_status: 'draft';
  source_fact_id?: string;
  analysis_id?: string;
  trace_ref?: string;
  processing_direction: 'draft';
  recommendation_summary: string;
  auto_executable: false;
  created_at: string;
  standard_error?: StandardErrorResult;
}
