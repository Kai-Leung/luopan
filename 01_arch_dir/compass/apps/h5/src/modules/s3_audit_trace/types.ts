export interface S3TraceEvent {
  trace_ref: string;
  source_fact_id?: string;
  raw_input_id?: string;
  candidate_id?: string;
  governance_id?: string;
  review_id?: string;
  analysis_id?: string;
  recommendation_id?: string;
  execution_response_id?: string;
  feedback_id?: string;
  created_at: string;
  source_stage: string;
  target_stage: string;
  action_type: string;
  actor_id: string;
  organization_id: string;
  readonly: true;
  no_write_l2: true;
}

export interface S3TraceSummaryRequest {
  source_fact_id?: string;
  trace_ref?: string;
}

export interface S3TraceSummaryResponse {
  trace_ref: string;
  source_fact_id?: string;
  chain_summary: string;
  events: S3TraceEvent[];
  no_write_l2: true;
}
