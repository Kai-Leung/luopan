"""标准治理只读约束层：事实与枚举常量。"""

from enum import Enum

from .source_types import SourceType


class ObjectAssetType(str, Enum):
    """object_asset_type"""
    ORGANIZATION_ASSET = "organization_asset"
    PROJECT_ASSET = "project_asset"
    SUBJECT_ASSET = "subject_asset"
    MATERIAL_ASSET = "material_asset"
    DOCUMENT_ASSET = "document_asset"


class FactRecordType(str, Enum):
    """fact_record_type"""
    CONSTRUCTION_RECORD = "construction_record"
    FINANCIAL_RECORD = "financial_record"
    MATERIAL_FLOW_RECORD = "material_flow_record"
    DOCUMENT_RECORD = "document_record"
    COMMUNICATION_SERVICE_RECORD = "communication_service_record"
    ISSUE_RISK_RECORD = "issue_risk_record"
    DECISION_CHANGE_RECORD = "decision_change_record"
    RELATIONSHIP_RECORD = "relationship_record"
    ATTENDANCE_RECORD = "attendance_record"
    RESUME_RECORD = "resume_record"
    BUSINESS_MAINTENANCE_RECORD = "business_maintenance_record"
    ACCEPTANCE_DELIVERY_RECORD = "acceptance_delivery_record"
    PURCHASE_RECORD = "purchase_record"
    OTHER_FACT_RECORD = "other_fact_record"


class DocumentAssetType(str, Enum):
    """document_asset_type"""
    CONTRACT_DOCUMENT = "contract_document"
    QUOTATION_DOCUMENT = "quotation_document"
    BUDGET_DOCUMENT = "budget_document"
    TENDER_DOCUMENT = "tender_document"
    VISA_DOCUMENT = "visa_document"
    CHANGE_ORDER_DOCUMENT = "change_order_document"
    SETTLEMENT_DOCUMENT = "settlement_document"
    INVOICE_DOCUMENT = "invoice_document"
    PAYMENT_VOUCHER_DOCUMENT = "payment_voucher_document"
    DRAWING_DOCUMENT = "drawing_document"
    ACCEPTANCE_DOCUMENT = "acceptance_document"
    HANDOVER_DOCUMENT = "handover_document"
    CONSTRUCTION_LOG_DOCUMENT = "construction_log_document"
    PHOTO_DOCUMENT = "photo_document"
    VIDEO_DOCUMENT = "video_document"
    CHAT_RECORD_DOCUMENT = "chat_record_document"
    MEETING_RECORD_DOCUMENT = "meeting_record_document"
    APPROVAL_DOCUMENT = "approval_document"
    MATERIAL_RECEIPT_DOCUMENT = "material_receipt_document"
    ATTENDANCE_DOCUMENT = "attendance_document"
    ISSUE_RISK_DOCUMENT = "issue_risk_document"
    CUSTOMER_CONFIRMATION_DOCUMENT = "customer_confirmation_document"
    SUPPLIER_DOCUMENT = "supplier_document"
    SUBCONTRACTOR_DOCUMENT = "subcontractor_document"
    EXTERNAL_DISPLAY_DOCUMENT = "external_display_document"
    ARCHIVE_PACKAGE_DOCUMENT = "archive_package_document"
    AUDIT_TRACE_DOCUMENT = "audit_trace_document"


class ViewType(str, Enum):
    """view_type"""
    EXECUTION_VIEW = "execution_view"
    BUSINESS_VIEW = "business_view"
    SETTLEMENT_VIEW = "settlement_view"
    DELIVERY_COLLABORATION_VIEW = "delivery_collaboration_view"


class ExperienceRuleContentType(str, Enum):
    """experience_rule_content_type"""
    EXPERIENCE_RULE_ITEM = "experience_rule_item"
    BUSINESS_TEMPLATE = "business_template"
    CANDIDATE_KNOWLEDGE = "candidate_knowledge"


class EvidenceType(str, Enum):
    """evidence_type"""
    CONTRACT_DOCUMENT = "contract_document"
    DRAWING_DOCUMENT = "drawing_document"
    PHOTO_EVIDENCE = "photo_evidence"
    VIDEO_EVIDENCE = "video_evidence"
    CHAT_SCREENSHOT = "chat_screenshot"
    RECEIPT_DOCUMENT = "receipt_document"
    PAYMENT_VOUCHER = "payment_voucher"
    SITE_RECORD = "site_record"
    APPROVAL_RECORD = "approval_record"
    SYSTEM_LOG = "system_log"
    SNAPSHOT_RECORD = "snapshot_record"
    INVOICE_DOCUMENT = "invoice_document"
    QUOTATION_DOCUMENT = "quotation_document"
    CHANGE_ORDER_DOCUMENT = "change_order_document"
    ATTENDANCE_EVIDENCE = "attendance_evidence"
    MATERIAL_RECEIPT = "material_receipt"
    HANDOVER_RECORD = "handover_record"
    EXTERNAL_CONFIRMATION = "external_confirmation"
    AUDIT_TRACE_RECORD = "audit_trace_record"


class ViewOutputType(str, Enum):
    """view_output_type"""
    SUMMARY_OUTPUT = "summary_output"
    LIST_OUTPUT = "list_output"
    DASHBOARD = "dashboard"
    TOPIC_LEDGER = "topic_ledger"
    DRAFT_REPORT = "draft_report"
    SETTLEMENT_DRAFT = "settlement_draft"
    EXTERNAL_DISPLAY_PACKAGE = "external_display_package"
    TRACE_OUTPUT = "trace_output"
    SNAPSHOT_OUTPUT = "snapshot_output"
    COMPARISON_OUTPUT = "comparison_output"
    STATISTICS_OUTPUT = "statistics_output"
    TREND_OUTPUT = "trend_output"
    EXCEPTION_OUTPUT = "exception_output"
    COLLABORATION_OUTPUT = "collaboration_output"
    EVIDENCE_PACKAGE_OUTPUT = "evidence_package_output"
    REMINDER_OUTPUT = "reminder_output"
    EXPORT_OUTPUT = "export_output"


class TemplateOutputType(str, Enum):
    """template_output_type"""
    DAILY_REPORT_DRAFT = "daily_report_draft"
    WEEKLY_REPORT_DRAFT = "weekly_report_draft"
    MONTHLY_REPORT_DRAFT = "monthly_report_draft"
    STAGE_REPORT_DRAFT = "stage_report_draft"
    SETTLEMENT_DRAFT = "settlement_draft"
    CUSTOMER_CONFIRMATION_DRAFT = "customer_confirmation_draft"
    DOCUMENT_GAP_LIST = "document_gap_list"
    ISSUE_RISK_LIST = "issue_risk_list"
    TOPIC_LEDGER_OUTPUT = "topic_ledger_output"
    EXTERNAL_DISPLAY_PACKAGE = "external_display_package"
    REVIEW_SUMMARY = "review_summary"
    HANDOVER_LIST = "handover_list"
    MATERIAL_RECONCILIATION_LIST = "material_reconciliation_list"
    PAYMENT_COLLECTION_LIST = "payment_collection_list"
    CHANGE_ORDER_PACKAGE = "change_order_package"
    ACCEPTANCE_PACKAGE = "acceptance_package"
    RESPONSIBILITY_CONFIRMATION_LIST = "responsibility_confirmation_list"
    BUSINESS_FOLLOWUP_LIST = "business_followup_list"
    PROFILE_SUMMARY = "profile_summary"
    FEEDBACK_ACTION_LIST = "feedback_action_list"


class AiAssistOutputType(str, Enum):
    """ai_assist_output_type"""
    INPUT_ASSIST = "input_assist"
    TRANSCRIPTION_ASSIST = "transcription_assist"
    SUMMARY_ASSIST = "summary_assist"
    GAP_HINT = "gap_hint"
    RISK_HINT = "risk_hint"
    CANDIDATE_SUGGESTION = "candidate_suggestion"
    RULE_QUESTION_HINT = "rule_question_hint"
    ANALYSIS_ASSIST = "analysis_assist"
    TEMPLATE_DRAFT_ASSIST = "template_draft_assist"
    CANDIDATE_KNOWLEDGE_ASSIST = "candidate_knowledge_assist"
    CLASSIFICATION_ASSIST = "classification_assist"
    EVIDENCE_BINDING_ASSIST = "evidence_binding_assist"
    DESENSITIZATION_ASSIST = "desensitization_assist"
    VERSION_COMPARE_ASSIST = "version_compare_assist"
    CONFLICT_DETECTION_ASSIST = "conflict_detection_assist"
    SEARCH_ASSIST = "search_assist"
    DECISION_REFERENCE_ASSIST = "decision_reference_assist"


class StandardCategory(str, Enum):
    """standard_category"""
    TERM_STANDARD = "term_standard"
    FIELD_STANDARD = "field_standard"
    ENUM_STANDARD = "enum_standard"
    STATE_STANDARD = "state_standard"
    DEPENDENCY_STANDARD = "dependency_standard"
    PERMISSION_VISIBILITY_STANDARD = "permission_visibility_standard"
    RISK_STANDARD = "risk_standard"
    VALIDATION_STANDARD = "validation_standard"
    TRACE_VERSION_STANDARD = "trace_version_standard"
    QUESTION_STANDARD = "question_standard"
    DESENSITIZATION_STANDARD = "desensitization_standard"
    AI_CANDIDATE_OUTPUT_STANDARD = "ai_candidate_output_standard"
    DOCUMENT_ASSET_TYPE_CONTRACT_DOCUMENT = "document_asset_type.contract_document"
    EVIDENCE_TYPE_CONTRACT_DOCUMENT = "evidence_type.contract_document"
    FACT_RECORD_TYPE_DOCUMENT_RECORD = "fact_record_type.document_record"
    SOURCE_TYPE_UPLOADED_DOCUMENT = "source_type.uploaded_document"


ENUM_CATEGORY_MAP = {
    "object_asset_type": ObjectAssetType,
    "fact_record_type": FactRecordType,
    "document_asset_type": DocumentAssetType,
    "view_type": ViewType,
    "experience_rule_content_type": ExperienceRuleContentType,
    "source_type": SourceType,
    "evidence_type": EvidenceType,
    "view_output_type": ViewOutputType,
    "template_output_type": TemplateOutputType,
    "ai_assist_output_type": AiAssistOutputType,
    "standard_category": StandardCategory,
}

KNOWN_ENUM_CATEGORIES = set(ENUM_CATEGORY_MAP.keys())
