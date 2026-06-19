"""标准治理只读约束层：状态常量。"""

from enum import Enum


class ObjectLifecycleStatus(str, Enum):
    """object_lifecycle_status"""
    CANDIDATE = "candidate"
    ACTIVE = "active"
    PENDING_COMPLETION = "pending_completion"
    SUSPENDED = "suspended"
    MERGED = "merged"
    DISABLED = "disabled"
    VOIDED = "voided"
    ARCHIVED = "archived"


class ObjectConditionStatus(str, Enum):
    """object_condition_status"""
    NORMAL = "normal"
    INCOMPLETE = "incomplete"
    DAMAGED = "damaged"
    PENDING_INSPECTION = "pending_inspection"
    UNDER_REPAIR = "under_repair"
    UNAVAILABLE = "unavailable"
    SCRAPPED = "scrapped"


class ObjectUsageStatus(str, Enum):
    """object_usage_status"""
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_STOCK = "in_stock"
    PROJECT_OCCUPIED = "project_occupied"
    BORROWED = "borrowed"
    IN_TRANSFER = "in_transfer"
    LOST = "lost"
    RELEASED = "released"


class FactRecordStatus(str, Enum):
    """fact_record_status"""
    DRAFT = "draft"
    CANDIDATE = "candidate"
    PENDING_COMPLETION = "pending_completion"
    UNDER_VALIDATION = "under_validation"
    PENDING_CONFIRMATION = "pending_confirmation"
    CONFIRMED = "confirmed"
    OFFICIAL = "official"
    SUSPENDED = "suspended"
    REJECTED = "rejected"
    VOIDED = "voided"
    REVISED = "revised"
    ARCHIVED = "archived"


class CandidateStatus(str, Enum):
    """candidate_status"""
    NEW_CANDIDATE = "new_candidate"
    PENDING_COMPLETION = "pending_completion"
    UNDER_REVIEW = "under_review"
    READY_FOR_CONFIRMATION = "ready_for_confirmation"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CONVERTED = "converted"
    EXPIRED = "expired"


class ValidationStatus(str, Enum):
    """validation_status"""
    NOT_CHECKED = "not_checked"
    CHECKING = "checking"
    PASSED = "passed"
    PENDING_COMPLETION = "pending_completion"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    FUSED = "fused"


class ConfirmationStatus(str, Enum):
    """confirmation_status"""
    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PARTIALLY_CONFIRMED = "partially_confirmed"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"


class ViewOutputStatus(str, Enum):
    """view_output_status"""
    DRAFT = "draft"
    GENERATED = "generated"
    CANDIDATE_OUTPUT = "candidate_output"
    OFFICIAL_OUTPUT = "official_output"
    PENDING_REVIEW = "pending_review"
    BLOCKED = "blocked"
    EXPORTED = "exported"
    SHARED = "shared"
    ARCHIVED = "archived"


class AiOutputStatus(str, Enum):
    """ai_output_status"""
    NOT_USED = "not_used"
    GENERATED_CANDIDATE = "generated_candidate"
    PENDING_REVIEW = "pending_review"
    ACCEPTED_AS_CANDIDATE = "accepted_as_candidate"
    REJECTED = "rejected"
    FAILED = "failed"
    LOGGED_FOR_IMPROVEMENT = "logged_for_improvement"


class FeedbackStatus(str, Enum):
    """feedback_status"""
    NEW_FEEDBACK = "new_feedback"
    CLASSIFIED = "classified"
    PENDING_COMPLETION = "pending_completion"
    ROUTED = "routed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CLOSED = "closed"
    ARCHIVED = "archived"


class CandidateGovernanceStatus(str, Enum):
    """candidate_governance_status"""
    CANDIDATE = "candidate"
    PENDING_SOURCE = "pending_source"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REVIEWED_CANDIDATE = "reviewed_candidate"
    DEPRECATED = "deprecated"
    REPLACED = "replaced"
    ARCHIVED = "archived"


class StandardGovernanceStatus(str, Enum):
    """standard_governance_status"""
    DRAFT = "draft"
    CANDIDATE = "candidate"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    BLOCKED = "blocked"


class VisibilityStatus(str, Enum):
    """visibility_status"""
    INTERNAL_ONLY = "internal_only"
    RESTRICTED = "restricted"
    DESENSITIZATION_REQUIRED = "desensitization_required"
    EXTERNAL_REVIEW_REQUIRED = "external_review_required"
    EXTERNAL_ALLOWED = "external_allowed"
    EXPORT_ALLOWED = "export_allowed"
    SHARE_BLOCKED = "share_blocked"
    EXTERNAL_BLOCKED = "external_blocked"


class DocumentFileStatus(str, Enum):
    """document_file_status"""
    DRAFT = "draft"
    REVISION = "revision"
    OFFICIAL = "official"


class RuntimeTaskStatus(str, Enum):
    """runtime_task_status"""
    QUEUED = "queued"
    PROCESSING = "processing"
    WAITING_CALLBACK = "waiting_callback"
    RETRYABLE = "retryable"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    FUSED = "fused"


class ExternalSyncStatus(str, Enum):
    """external_sync_status"""
    RECEIVED = "received"
    IDENTIFIED = "identified"
    PENDING_IDENTITY = "pending_identity"
    PENDING_SCOPE = "pending_scope"
    PENDING_CONFIRMATION = "pending_confirmation"
    ACCEPTED_AS_CANDIDATE = "accepted_as_candidate"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class ArchiveStatus(str, Enum):
    """archive_status"""
    NOT_ARCHIVED = "not_archived"
    ARCHIVE_PENDING = "archive_pending"
    ARCHIVED = "archived"
    ARCHIVE_BLOCKED = "archive_blocked"
    RECOVERY_PENDING = "recovery_pending"


STATUS_GROUP_MAP = {
    "object_lifecycle_status": ObjectLifecycleStatus,
    "object_condition_status": ObjectConditionStatus,
    "object_usage_status": ObjectUsageStatus,
    "fact_record_status": FactRecordStatus,
    "candidate_status": CandidateStatus,
    "validation_status": ValidationStatus,
    "confirmation_status": ConfirmationStatus,
    "view_output_status": ViewOutputStatus,
    "ai_output_status": AiOutputStatus,
    "feedback_status": FeedbackStatus,
    "candidate_governance_status": CandidateGovernanceStatus,
    "standard_governance_status": StandardGovernanceStatus,
    "visibility_status": VisibilityStatus,
    "document_file_status": DocumentFileStatus,
    "runtime_task_status": RuntimeTaskStatus,
    "external_sync_status": ExternalSyncStatus,
    "archive_status": ArchiveStatus,
}

KNOWN_STATUS_GROUPS = set(STATUS_GROUP_MAP.keys())
