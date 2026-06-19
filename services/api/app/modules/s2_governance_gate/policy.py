"""S2 治理决策策略。

只承接候选治理的纯决策，不写数据库、不生成正式事实。
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.modules.s2_governance_gate.schemas import (
    GOVERNANCE_STATUS_AUTO_PASS,
    GOVERNANCE_STATUS_BLOCKED,
    GOVERNANCE_STATUS_NEEDS_COMPLETION,
    GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION,
    NEXT_ACTION_ASK_MORE,
    NEXT_ACTION_BLOCKED,
    NEXT_ACTION_NEED_CONFIRM,
    NEXT_ACTION_READY_TO_CHAIN,
    GovernanceStatus,
    NextAction,
    RiskLevelValue,
)
from app.modules.standard_governance.rules.field_rules import (
    build_field_question_prompts,
    build_field_validation_hints,
    find_missing_by_field_rules,
    find_missing_text_required_fields,
    infer_fact_record_type,
    infer_source_type,
    normalize_payload_for_field_rules,
)
from app.modules.standard_governance.rules.risk_rules import RiskLevel, match_risk_keywords
from app.modules.standard_governance.rules.project_asset_rules import (
    PROJECT_ASSET_PERMISSION,
    find_missing_project_asset_fields,
    is_project_asset_candidate,
)
from app.modules.standard_governance.validators import is_valid_status


@dataclass(frozen=True)
class GovernancePolicyResult:
    governance_status: GovernanceStatus
    missing_fields: List[str]
    risk_level: RiskLevelValue
    question_prompts: List[str]
    validation_hints: List[str]
    risk_hints: List[str]
    required_permission: Optional[str]
    next_action: NextAction
    message: str


def evaluate_governance_policy(
    *,
    candidate_status: str,
    candidate_payload: Dict[str, Any],
) -> GovernancePolicyResult:
    if not is_valid_status("candidate_status", candidate_status):
        return _build_invalid_status_result()

    text = extract_text(candidate_payload)
    if not text:
        return _build_missing_text_result(candidate_payload)
    if is_project_asset_candidate(candidate_payload):
        return _evaluate_project_asset_candidate_policy(candidate_payload)

    return _evaluate_text_policy(candidate_payload, text)


def _build_invalid_status_result() -> GovernancePolicyResult:
    return _build_policy_result(
        governance_status=GOVERNANCE_STATUS_BLOCKED,
        missing_fields=[],
        risk_level=RiskLevel.BLOCKING.value,
        risk_hints=["invalid_candidate_status"],
        validation_hints=["candidate_status 不属于标准状态口径"],
    )


def _build_missing_text_result(candidate_payload: Dict[str, Any]) -> GovernancePolicyResult:
    return _build_policy_result(
        governance_status=GOVERNANCE_STATUS_NEEDS_COMPLETION,
        missing_fields=find_missing_text_required_fields(candidate_payload),
        risk_level=RiskLevel.NONE.value,
        risk_hints=[],
    )


def _evaluate_text_policy(
    candidate_payload: Dict[str, Any],
    text: str,
) -> GovernancePolicyResult:
    risk_match = match_risk_keywords(text)
    missing_fields = detect_missing_fields(
        candidate_payload,
        text,
        risk_level=risk_match.risk_level,
    )
    governance_status = _resolve_governance_status(
        blocking_risks=risk_match.blocking_risks,
        high_risks=risk_match.high_risks,
        missing_fields=missing_fields,
    )
    return _build_policy_result(
        governance_status=governance_status,
        missing_fields=missing_fields,
        risk_level=risk_match.risk_level,
        risk_hints=risk_match.risk_hints,
    )


def _evaluate_project_asset_candidate_policy(
    candidate_payload: Dict[str, Any],
) -> GovernancePolicyResult:
    missing_fields = find_missing_project_asset_fields(candidate_payload)
    governance_status: GovernanceStatus = (
        GOVERNANCE_STATUS_NEEDS_COMPLETION
        if missing_fields
        else GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION
    )
    return _build_policy_result(
        governance_status=governance_status,
        missing_fields=missing_fields,
        risk_level=RiskLevel.NONE.value,
        risk_hints=[],
        required_permission=PROJECT_ASSET_PERMISSION,
    )


def _resolve_governance_status(
    *,
    blocking_risks: List[str],
    high_risks: List[str],
    missing_fields: List[str],
) -> GovernanceStatus:
    if blocking_risks:
        return GOVERNANCE_STATUS_BLOCKED
    if missing_fields:
        return GOVERNANCE_STATUS_NEEDS_COMPLETION
    if high_risks:
        return GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION
    return GOVERNANCE_STATUS_AUTO_PASS


def _build_policy_result(
    *,
    governance_status: GovernanceStatus,
    missing_fields: List[str],
    risk_level: RiskLevelValue,
    risk_hints: List[str],
    validation_hints: Optional[List[str]] = None,
    required_permission: Optional[str] = None,
) -> GovernancePolicyResult:
    resolved_validation_hints = list(validation_hints or [])
    question_prompts: List[str] = []
    if missing_fields:
        question_prompts = build_field_question_prompts(missing_fields)
        resolved_validation_hints.extend(build_field_validation_hints(missing_fields))

    return GovernancePolicyResult(
        governance_status=governance_status,
        missing_fields=missing_fields,
        risk_level=risk_level,
        question_prompts=question_prompts,
        validation_hints=resolved_validation_hints,
        risk_hints=risk_hints,
        required_permission=required_permission,
        next_action=build_next_action(governance_status),
        message=build_message(governance_status),
    )


def extract_text(candidate_payload: Dict[str, Any]) -> str:
    for key in ("text", "raw_text", "content", "fact_summary"):
        value = candidate_payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    raw_payload = candidate_payload.get("raw_payload")
    if isinstance(raw_payload, dict):
        for key in ("text", "raw_text", "content", "fact_summary"):
            value = raw_payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return ""


def extract_input_session_id(candidate_payload: Dict[str, Any]) -> Optional[str]:
    value = candidate_payload.get("input_session_id")
    return value if isinstance(value, str) and value else None


def detect_missing_fields(
    candidate_payload: Dict[str, Any],
    text: str,
    *,
    risk_level: str,
) -> List[str]:
    normalized_payload = normalize_payload_for_field_rules(candidate_payload, text)
    return find_missing_by_field_rules(
        normalized_payload,
        text=text,
        fact_record_type=infer_fact_record_type(candidate_payload, text),
        risk_level=risk_level,
        source_type=infer_source_type(candidate_payload),
    )


def build_next_action(governance_status: str) -> NextAction:
    if governance_status == GOVERNANCE_STATUS_NEEDS_COMPLETION:
        return NEXT_ACTION_ASK_MORE
    if governance_status == GOVERNANCE_STATUS_BLOCKED:
        return NEXT_ACTION_BLOCKED
    if governance_status in (
        GOVERNANCE_STATUS_AUTO_PASS,
        GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION,
    ):
        return NEXT_ACTION_NEED_CONFIRM
    return NEXT_ACTION_READY_TO_CHAIN


def build_message(governance_status: str) -> str:
    if governance_status == GOVERNANCE_STATUS_AUTO_PASS:
        return "governance check auto pass"
    if governance_status == GOVERNANCE_STATUS_NEEDS_COMPLETION:
        return "governance check needs completion"
    if governance_status == GOVERNANCE_STATUS_NEEDS_MANUAL_CONFIRMATION:
        return "governance check needs manual confirmation"
    return "governance check blocked"
