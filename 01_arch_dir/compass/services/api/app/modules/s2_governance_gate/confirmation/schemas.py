"""人工确认层最小接口 Schema。

只表达人工 review 结果，不承接 L2 入链或正式事实字段。
"""

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel

GovernanceStatus = Literal[
    "auto_pass",
    "needs_completion",
    "needs_confirmation",
    "blocked",
]
ReviewAction = Literal["confirm", "return_for_completion", "reject"]
ReviewStatus = Literal[
    "confirmed_candidate",
    "returned_for_completion",
    "rejected_candidate",
]
PolicyDecision = Literal["manual_review_required"]


class ManualConfirmationReviewRequest(BaseModel):
    governance_id: str
    governance_status: GovernanceStatus
    review_action: ReviewAction
    pending_id: Optional[str] = None
    required_permission: Optional[str] = None
    confirmed_by: Optional[str] = None


class ManualConfirmationReviewResponse(BaseModel):
    review_id: str
    governance_id: str
    review_status: ReviewStatus
    policy_decision: PolicyDecision
    message: str
    project_asset: Optional[Dict[str, Any]] = None


class PendingConfirmationCreateRequest(BaseModel):
    raw_input_id: str
    input_session_id: Optional[str] = None
    candidate_id: str
    governance_id: str
    governance_status: GovernanceStatus
    fact_type: str
    fact_payload: Dict[str, Any]
    display_text: str
    required_permission: Optional[str] = None


class PendingConfirmationItem(BaseModel):
    pending_id: str
    input_session_id: str
    raw_input_id: str
    candidate_id: str
    governance_id: str
    governance_status: GovernanceStatus
    fact_type: str
    fact_payload: Dict[str, Any]
    display_text: str
    required_permission: Optional[str] = None
    created_at: str


class PendingConfirmationListResponse(BaseModel):
    items: list[PendingConfirmationItem]
