import type { StandardErrorResult } from '../standard_governance/processing';

export interface L7FeedbackRequest {
  execution_response_id?: string;
  source_fact_id?: string;
  feedback_note: string;
  feedback_type?: string;
}

export interface L7FeedbackResponse {
  feedback_id: string;
  feedback_status: 'candidate';
  execution_response_id?: string;
  source_fact_id?: string;
  trace_ref?: string;
  processing_direction: 'candidate';
  feedback_note: string;
  feedback_type?: string;
  returns_to_candidate_flow: true;
  created_at: string;
  standard_error?: StandardErrorResult;
}
