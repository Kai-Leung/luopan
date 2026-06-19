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

// ── S1: Runtime Context ───────────────────────────────────────────────────

export type RuntimeProjectScopeMode = "organization" | "selected_projects";
export type RuntimeContextSource = "controlled_claim" | "development_baseline";

export interface RuntimeProjectScopeItem {
  project_id: string;
  display_name: string;
  aliases: string[];
}

export interface RuntimePermissionResult {
  action: string;
  allowed: boolean;
  denied_reason?: string;
}

export interface RuntimeContextResponse {
  context_id: string;
  user_id: string;
  user_display_name: string;
  organization_id: string;
  organization_name: string;
  role_ids: string[];
  role_names: string[];
  project_scope_mode: RuntimeProjectScopeMode;
  project_scope: RuntimeProjectScopeItem[];
  selected_project_id?: string;
  allowed_actions: string[];
  permission_results: RuntimePermissionResult[];
  denied_reason?: string;
  context_source: RuntimeContextSource;
  is_authenticated: true;
}

// ── L0: Raw Input ──────────────────────────────────────────────────────────

export interface L0RawInputRequest {
  text?: string;
  image_ref?: string;
  file_ref?: string;
  input_session_id?: string;
  idempotency_key?: string;
  source_type: SourceType;
}

export interface L0RawInputResponse {
  raw_input_id: string;
  input_session_id: string;
  status: "received_only";
  message: "raw input received";
}

// ── Upload: Original File Storage ─────────────────────────────────────────

export interface UploadFileStoredResponse {
  upload_id: string;
  filename: string;
  content_type: string;
  file_size: number;
  storage_path: string;
  saved: true;
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

// ── Standard Processing ───────────────────────────────────────────────────

export type StandardProcessingDirection =
  | "readonly"
  | "draft"
  | "response"
  | "candidate"
  | "blocked"
  | "need_supplement"
  | "need_confirmation"
  | "failed";

export interface StandardErrorResult {
  error_code: string;
  message: string;
  processing_direction: StandardProcessingDirection;
}

export interface StandardSourceRef {
  source_stage: string;
  source_id: string;
}

export interface StandardTraceRef {
  trace_ref: string;
  source_fact_id?: string;
  created_at: string;
}

export interface StandardBoundaryNotice {
  processing_direction: StandardProcessingDirection;
  readonly: boolean;
  no_write_l2: boolean;
  message: string;
}

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

// ── L4: Analysis Preview ──────────────────────────────────────────────────

export interface L4AnalysisPreviewRequest {
  fact_id: string;
}

export interface L4AnalysisPreviewResponse {
  analysis_id: string;
  source_fact_id: string;
  trace_ref?: string;
  processing_direction: "readonly";
  analysis_status: "preview";
  analysis_summary: string;
  readonly: true;
  created_at: string;
  standard_error?: StandardErrorResult;
}

// ── L5: Recommendation Draft ──────────────────────────────────────────────

export interface L5RecommendationDraftRequest {
  analysis_id?: string;
  source_fact_id?: string;
  context_payload?: Record<string, unknown>;
}

export interface L5RecommendationDraftResponse {
  recommendation_id: string;
  recommendation_status: "draft";
  source_fact_id?: string;
  analysis_id?: string;
  trace_ref?: string;
  processing_direction: "draft";
  recommendation_summary: string;
  auto_executable: false;
  created_at: string;
  standard_error?: StandardErrorResult;
}

// ── L6: Execution Response ────────────────────────────────────────────────

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
  processing_direction: "response";
  execution_note: string;
  creates_fact: false;
  created_at: string;
  standard_error?: StandardErrorResult;
}

// ── L7: Feedback Candidate ────────────────────────────────────────────────

export interface L7FeedbackRequest {
  execution_response_id?: string;
  source_fact_id?: string;
  feedback_note: string;
  feedback_type?: string;
}

export interface L7FeedbackResponse {
  feedback_id: string;
  feedback_status: "candidate";
  execution_response_id?: string;
  source_fact_id?: string;
  trace_ref?: string;
  processing_direction: "candidate";
  feedback_note: string;
  feedback_type?: string;
  return_raw_input_id: string;
  return_candidate_id: string;
  governance_required: true;
  returns_to_candidate_flow: true;
  created_at: string;
  standard_error?: StandardErrorResult;
}
