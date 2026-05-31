import type { StandardErrorResult } from '../standard_governance/processing';

export interface L6ExecutionResponseRequest {
  recommendation_id?: string;
  source_fact_id?: string;
  execution_note: string;
  execution_status: string;
}

export interface L6ExecutionResponseResponse {
  execution_response_id: string;
  execution_status: string;
  recommendation_id?: string;
  source_fact_id?: string;
  trace_ref?: string;
  processing_direction: 'response';
  execution_note: string;
  creates_fact: false;
  created_at: string;
  standard_error?: StandardErrorResult;
}
