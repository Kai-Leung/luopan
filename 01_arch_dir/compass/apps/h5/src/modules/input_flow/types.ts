import type { SourceType } from "../standard_governance/enums";

// L0
export interface L0RawInputRequest {
  text?: string;
  image_ref?: string;
  file_ref?: string;
  input_session_id?: string;
  source_type: SourceType;
}

export interface L0RawInputResponse {
  raw_input_id: string;
  input_session_id: string;
  status: "received_only";
  message: "raw input received";
}

// L1
export interface L1CandidateRequest {
  raw_input_id: string;
  input_session_id?: string;
  supplement_candidate_id?: string;
  raw_payload: Record<string, unknown>;
  source_type: string;
}

export interface L1CandidateItem {
  candidate_id: string;
  input_session_id: string;
  raw_input_id: string;
  candidate_status: string;
  candidate_payload: Record<string, unknown> & {
    candidate_summary?: string;
    fact_record_type?: string;
    project_name?: string;
    subject_name?: string;
    occurred_at?: string;
    amount_text?: string;
    issue_or_action?: string;
  };
}

export interface L1CandidateResponse extends L1CandidateItem {
  candidates: L1CandidateItem[];
  message: string;
}

// S2
export interface S2GovernanceCheckRequest {
  candidate_id: string;
  input_session_id?: string;
  candidate_status: string;
  candidate_payload: Record<string, unknown>;
}

export interface S2GovernanceCheckResponse {
  governance_id: string;
  candidate_id: string;
  input_session_id?: string;
  governance_status: string;
  missing_fields: string[];
  risk_level: "none" | "low" | "medium" | "high" | "blocking";
  question_prompts: string[];
  validation_hints: string[];
  risk_hints: string[];
  next_action: "ask_more" | "need_confirm" | "blocked" | "ready_to_chain";
  message: string;
}

// MC
export interface ManualConfirmationReviewRequest {
  governance_id: string;
  governance_status: string;
  review_action: "confirm" | "return_for_completion" | "reject";
}

export interface ManualConfirmationReviewResponse {
  review_id: string;
  governance_id: string;
  review_status: string;
  policy_decision: string;
  message: string;
}

export interface PendingConfirmationCreateRequest {
  raw_input_id: string;
  input_session_id?: string;
  candidate_id: string;
  governance_id: string;
  governance_status: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  display_text: string;
}

export interface PendingConfirmationItem {
  pending_id: string;
  input_session_id: string;
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  governance_status: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  display_text: string;
  created_at: string;
}

export interface PendingConfirmationListResponse {
  items: PendingConfirmationItem[];
}
