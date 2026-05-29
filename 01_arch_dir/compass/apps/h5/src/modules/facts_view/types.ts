export interface L3FactViewResponse {
  fact_id: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  fact_status: "active_fact";
  created_at: string;
}

export interface SourceOfTruthFactRequest {
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  review_id: string;
  review_status: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
}

export interface SourceOfTruthFactResponse {
  fact_id: string;
  fact_status: "active_fact";
  fact_payload: Record<string, unknown>;
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  review_id: string;
  message: string;
}
