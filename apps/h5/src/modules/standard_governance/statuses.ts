/** Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/04_状态口径总表.md */

export enum ObjectLifecycleStatus {
  CANDIDATE = "candidate",
  ACTIVE = "active",
  PENDING_COMPLETION = "pending_completion",
  SUSPENDED = "suspended",
  MERGED = "merged",
  DISABLED = "disabled",
  VOIDED = "voided",
  ARCHIVED = "archived",
}

export enum ObjectConditionStatus {
  NORMAL = "normal",
  INCOMPLETE = "incomplete",
  DAMAGED = "damaged",
  PENDING_INSPECTION = "pending_inspection",
  UNDER_REPAIR = "under_repair",
  UNAVAILABLE = "unavailable",
  SCRAPPED = "scrapped",
}

export enum ObjectUsageStatus {
  AVAILABLE = "available",
  RESERVED = "reserved",
  IN_STOCK = "in_stock",
  PROJECT_OCCUPIED = "project_occupied",
  BORROWED = "borrowed",
  IN_TRANSFER = "in_transfer",
  LOST = "lost",
  RELEASED = "released",
}

export enum FactRecordStatus {
  DRAFT = "draft",
  CANDIDATE = "candidate",
  PENDING_COMPLETION = "pending_completion",
  UNDER_VALIDATION = "under_validation",
  PENDING_CONFIRMATION = "pending_confirmation",
  CONFIRMED = "confirmed",
  OFFICIAL = "official",
  SUSPENDED = "suspended",
  REJECTED = "rejected",
  VOIDED = "voided",
  REVISED = "revised",
  ARCHIVED = "archived",
}

export enum CandidateStatus {
  NEW_CANDIDATE = "new_candidate",
  PENDING_COMPLETION = "pending_completion",
  UNDER_REVIEW = "under_review",
  READY_FOR_CONFIRMATION = "ready_for_confirmation",
  ACCEPTED = "accepted",
  REJECTED = "rejected",
  CONVERTED = "converted",
  EXPIRED = "expired",
}

export enum ValidationStatus {
  NOT_CHECKED = "not_checked",
  CHECKING = "checking",
  PASSED = "passed",
  PENDING_COMPLETION = "pending_completion",
  MANUAL_REVIEW_REQUIRED = "manual_review_required",
  REJECTED = "rejected",
  BLOCKED = "blocked",
  FUSED = "fused",
}

export enum ConfirmationStatus {
  NOT_REQUIRED = "not_required",
  REQUIRED = "required",
  PENDING = "pending",
  CONFIRMED = "confirmed",
  PARTIALLY_CONFIRMED = "partially_confirmed",
  REJECTED = "rejected",
  EXPIRED = "expired",
  REVOKED = "revoked",
}

export enum ViewOutputStatus {
  DRAFT = "draft",
  GENERATED = "generated",
  CANDIDATE_OUTPUT = "candidate_output",
  OFFICIAL_OUTPUT = "official_output",
  PENDING_REVIEW = "pending_review",
  BLOCKED = "blocked",
  EXPORTED = "exported",
  SHARED = "shared",
  ARCHIVED = "archived",
}

export enum AiOutputStatus {
  NOT_USED = "not_used",
  GENERATED_CANDIDATE = "generated_candidate",
  PENDING_REVIEW = "pending_review",
  ACCEPTED_AS_CANDIDATE = "accepted_as_candidate",
  REJECTED = "rejected",
  FAILED = "failed",
  LOGGED_FOR_IMPROVEMENT = "logged_for_improvement",
}

export enum FeedbackStatus {
  NEW_FEEDBACK = "new_feedback",
  CLASSIFIED = "classified",
  PENDING_COMPLETION = "pending_completion",
  ROUTED = "routed",
  ACCEPTED = "accepted",
  REJECTED = "rejected",
  CLOSED = "closed",
  ARCHIVED = "archived",
}

export enum CandidateGovernanceStatus {
  CANDIDATE = "candidate",
  PENDING_SOURCE = "pending_source",
  UNDER_REVIEW = "under_review",
  APPROVED = "approved",
  REVIEWED_CANDIDATE = "reviewed_candidate",
  DEPRECATED = "deprecated",
  REPLACED = "replaced",
  ARCHIVED = "archived",
}

export enum StandardGovernanceStatus {
  DRAFT = "draft",
  CANDIDATE = "candidate",
  UNDER_REVIEW = "under_review",
  APPROVED = "approved",
  ACTIVE = "active",
  DEPRECATED = "deprecated",
  SUPERSEDED = "superseded",
  BLOCKED = "blocked",
}

export enum VisibilityStatus {
  INTERNAL_ONLY = "internal_only",
  RESTRICTED = "restricted",
  DESENSITIZATION_REQUIRED = "desensitization_required",
  EXTERNAL_REVIEW_REQUIRED = "external_review_required",
  EXTERNAL_ALLOWED = "external_allowed",
  EXPORT_ALLOWED = "export_allowed",
  SHARE_BLOCKED = "share_blocked",
  EXTERNAL_BLOCKED = "external_blocked",
}

export enum DocumentFileStatus {
  DRAFT = "draft",
  REVISION = "revision",
  OFFICIAL = "official",
}

export enum RuntimeTaskStatus {
  QUEUED = "queued",
  PROCESSING = "processing",
  WAITING_CALLBACK = "waiting_callback",
  RETRYABLE = "retryable",
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  CANCELLED = "cancelled",
  FUSED = "fused",
}

export enum ExternalSyncStatus {
  RECEIVED = "received",
  IDENTIFIED = "identified",
  PENDING_IDENTITY = "pending_identity",
  PENDING_SCOPE = "pending_scope",
  PENDING_CONFIRMATION = "pending_confirmation",
  ACCEPTED_AS_CANDIDATE = "accepted_as_candidate",
  REJECTED = "rejected",
  BLOCKED = "blocked",
}

export enum ArchiveStatus {
  NOT_ARCHIVED = "not_archived",
  ARCHIVE_PENDING = "archive_pending",
  ARCHIVED = "archived",
  ARCHIVE_BLOCKED = "archive_blocked",
  RECOVERY_PENDING = "recovery_pending",
}

export const STATUS_GROUP_VALUES: Record<string, readonly string[]> = {
  object_lifecycle_status: ["candidate", "active", "pending_completion", "suspended", "merged", "disabled", "voided", "archived"],
  object_condition_status: ["normal", "incomplete", "damaged", "pending_inspection", "under_repair", "unavailable", "scrapped"],
  object_usage_status: ["available", "reserved", "in_stock", "project_occupied", "borrowed", "in_transfer", "lost", "released"],
  fact_record_status: ["draft", "candidate", "pending_completion", "under_validation", "pending_confirmation", "confirmed", "official", "suspended", "rejected", "voided", "revised", "archived"],
  candidate_status: ["new_candidate", "pending_completion", "under_review", "ready_for_confirmation", "accepted", "rejected", "converted", "expired"],
  validation_status: ["not_checked", "checking", "passed", "pending_completion", "manual_review_required", "rejected", "blocked", "fused"],
  confirmation_status: ["not_required", "required", "pending", "confirmed", "partially_confirmed", "rejected", "expired", "revoked"],
  view_output_status: ["draft", "generated", "candidate_output", "official_output", "pending_review", "blocked", "exported", "shared", "archived"],
  ai_output_status: ["not_used", "generated_candidate", "pending_review", "accepted_as_candidate", "rejected", "failed", "logged_for_improvement"],
  feedback_status: ["new_feedback", "classified", "pending_completion", "routed", "accepted", "rejected", "closed", "archived"],
  candidate_governance_status: ["candidate", "pending_source", "under_review", "approved", "reviewed_candidate", "deprecated", "replaced", "archived"],
  standard_governance_status: ["draft", "candidate", "under_review", "approved", "active", "deprecated", "superseded", "blocked"],
  visibility_status: ["internal_only", "restricted", "desensitization_required", "external_review_required", "external_allowed", "export_allowed", "share_blocked", "external_blocked"],
  document_file_status: ["draft", "revision", "official"],
  runtime_task_status: ["queued", "processing", "waiting_callback", "retryable", "succeeded", "failed", "cancelled", "fused"],
  external_sync_status: ["received", "identified", "pending_identity", "pending_scope", "pending_confirmation", "accepted_as_candidate", "rejected", "blocked"],
  archive_status: ["not_archived", "archive_pending", "archived", "archive_blocked", "recovery_pending"],
};

export const KNOWN_STATUS_GROUPS = new Set(Object.keys(STATUS_GROUP_VALUES));
