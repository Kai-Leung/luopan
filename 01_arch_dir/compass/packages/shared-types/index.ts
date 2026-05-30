// Compass shared types — derived from real backend FastAPI/Pydantic schemas
// Source: packages/contracts/openapi/openapi.json (auto-generated, do not edit manually — update contracts instead)

// ── Enums ──────────────────────────────────────────────────────────────────

export type SourceType =
  | "manual_input"
  | "uploaded_document"
  | "image_input"
  | "audio_input"
  | "chat_record"
  | "external_feedback"
  | "system_generated"
  | "ai_assisted"
  | "interface_callback"
  | "template_output"
  | "view_output"
  | "manual_confirmation"
  | "system_validation"
  | "feedback_return"
  | "external_collaboration";

export type CandidateStatus =
  | "new_candidate"
  | "pending_completion"
  | "under_review"
  | "ready_for_confirmation"
  | "accepted"
  | "rejected"
  | "converted"
  | "expired";

export type GovernanceStatus =
  | "auto_pass"
  | "needs_completion"
  | "needs_confirmation"
  | "blocked";

export type ReviewAction =
  | "confirm"
  | "return_for_completion"
  | "reject";

export type ReviewStatus =
  | "confirmed_candidate"
  | "returned_for_completion"
  | "rejected_candidate";

export type FactStatus = "active_fact";

export type RiskLevel =
  | "none"
  | "low"
  | "medium"
  | "high"
  | "blocking";

export type NextAction =
  | "ask_more"
  | "need_confirm"
  | "blocked"
  | "ready_to_chain";

// ── L0: Raw Input ──────────────────────────────────────────────────────────

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

// ── L1: Candidate ──────────────────────────────────────────────────────────

export interface L1CandidateCreateRequest {
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
  candidate_status: CandidateStatus;
  candidate_payload: Record<string, unknown>;
}

export interface L1CandidateResponse {
  candidate_id: string;
  input_session_id: string;
  raw_input_id: string;
  candidate_status: CandidateStatus;
  candidate_payload: Record<string, unknown>;
  candidates: L1CandidateItem[];
  message: string;
}

// ── S2: Governance ─────────────────────────────────────────────────────────

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
  governance_status: GovernanceStatus;
  missing_fields: string[];
  risk_level: RiskLevel;
  question_prompts: string[];
  validation_hints: string[];
  risk_hints: string[];
  required_permission?: string;
  next_action: NextAction;
  message: string;
}

// ── Manual Confirmation ────────────────────────────────────────────────────

export interface PendingConfirmationCreateRequest {
  raw_input_id: string;
  input_session_id?: string;
  candidate_id: string;
  governance_id: string;
  governance_status: GovernanceStatus;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  display_text: string;
  required_permission?: string;
}

export interface PendingConfirmationItem {
  pending_id: string;
  input_session_id: string;
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  governance_status: GovernanceStatus;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  display_text: string;
  created_at: string;
}

export interface PendingConfirmationListResponse {
  items: PendingConfirmationItem[];
}

export interface ManualConfirmationReviewRequest {
  governance_id: string;
  governance_status: GovernanceStatus;
  review_action: ReviewAction;
  pending_id?: string;
  required_permission?: string;
  confirmed_by?: string;
}

export interface ManualConfirmationReviewResponse {
  review_id: string;
  governance_id: string;
  review_status: ReviewStatus;
  policy_decision: "manual_review_required";
  message: string;
  project_asset?: Record<string, unknown>;
}

// ── L2: Source of Truth ────────────────────────────────────────────────────

export interface L2FactCreateRequest {
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  review_id: string;
  review_status: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
}

export interface L2FactResponse {
  fact_id: string;
  fact_status: FactStatus;
  fact_payload: Record<string, unknown>;
  raw_input_id: string;
  candidate_id: string;
  governance_id: string;
  review_id: string;
  message: string;
}

// ── L3: Query View ─────────────────────────────────────────────────────────

export interface L3FactViewResponse {
  fact_id: string;
  fact_type: string;
  fact_payload: Record<string, unknown>;
  fact_status: FactStatus;
  created_at: string;
}

// ── L3: List Query ─────────────────────────────────────────────────────────

export interface L3FactListItem {
  fact_id: string;
  fact_type: string;
  fact_payload_summary: string;
  source_type: string;
  fact_status: FactStatus;
  created_at: string;
}

export interface L3FactListResponse {
  items: L3FactListItem[];
  total: number;
}
