import type { StandardErrorResult } from '../standard_governance/processing';

export interface L4AnalysisPreviewRequest {
  fact_id: string;
}

export interface L4AnalysisPreviewResponse {
  analysis_id: string;
  source_fact_id: string;
  trace_ref?: string;
  processing_direction: 'readonly';
  analysis_status: 'preview';
  analysis_summary: string;
  readonly: true;
  created_at: string;
  standard_error?: StandardErrorResult;
}
