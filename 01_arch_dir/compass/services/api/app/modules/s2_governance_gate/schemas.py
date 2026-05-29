"""S2 横向治理最小接口 Schema。

只表达治理校验结果，不承接人工确认、L2 入链或正式事实字段。
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel


GovernanceStatus = Literal[
    "auto_pass",
    "needs_completion",
    "needs_confirmation",
    "blocked",
]
RiskLevelValue = Literal["none", "low", "medium", "high", "blocking"]
NextAction = Literal["ask_more", "need_confirm", "blocked", "ready_to_chain"]

GOVERNANCE_STATUS_AUTO_PASS: GovernanceStatus = "auto_pass"
GOVERNANCE_STATUS_NEEDS_COMPLETION: GovernanceStatus = "needs_completion"
GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION: GovernanceStatus = "needs_confirmation"
GOVERNANCE_STATUS_BLOCKED: GovernanceStatus = "blocked"

NEXT_ACTION_ASK_MORE: NextAction = "ask_more"
NEXT_ACTION_NEED_CONFIRM: NextAction = "need_confirm"
NEXT_ACTION_BLOCKED: NextAction = "blocked"
NEXT_ACTION_READY_TO_CHAIN: NextAction = "ready_to_chain"


class S2GovernanceCheckRequest(BaseModel):
    candidate_id: str
    input_session_id: Optional[str] = None
    candidate_payload: Dict[str, Any]
    candidate_status: str


class S2GovernanceCheckResponse(BaseModel):
    governance_id: str
    candidate_id: str
    input_session_id: Optional[str] = None
    governance_status: GovernanceStatus
    missing_fields: List[str]
    risk_level: RiskLevelValue
    question_prompts: List[str]
    validation_hints: List[str]
    risk_hints: List[str]
    required_permission: Optional[str] = None
    next_action: NextAction
    message: str
