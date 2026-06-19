"""S2 横向治理最小校验服务。

仅生成治理校验结果并写入 governance_results，不调用人工确认，不写 L2，不生成正式事实。
"""

from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.db.repositories import create_governance_result, ensure_minimal_storage_tables
from app.db.session import SessionLocal
from app.modules.s2_governance_gate.models import GovernanceRecord
from app.modules.s2_governance_gate.policy import (
    GovernancePolicyResult,
    evaluate_governance_policy,
    extract_input_session_id,
)
from app.modules.s2_governance_gate.schemas import (
    S2GovernanceCheckRequest,
    S2GovernanceCheckResponse,
)

GOVERNANCE_MEMORY_STORE: List[GovernanceRecord] = []


def check_candidate_governance(
    payload: S2GovernanceCheckRequest,
) -> S2GovernanceCheckResponse:
    policy_result = evaluate_governance_policy(
        candidate_status=payload.candidate_status,
        candidate_payload=payload.candidate_payload,
    )
    record = _build_governance_record(payload, policy_result)
    GOVERNANCE_MEMORY_STORE.append(record)
    _persist_governance_record(record)
    return _build_governance_response(payload, record, policy_result)


def _build_governance_record(
    payload: S2GovernanceCheckRequest,
    policy_result: GovernancePolicyResult,
) -> GovernanceRecord:
    return GovernanceRecord(
        governance_id=f"gov_{uuid4().hex}",
        candidate_id=payload.candidate_id,
        created_at=datetime.now(timezone.utc),
        governance_status=policy_result.governance_status,
        missing_fields=policy_result.missing_fields,
        risk_level=policy_result.risk_level,
        question_prompts=policy_result.question_prompts,
        validation_hints=policy_result.validation_hints,
        risk_hints=policy_result.risk_hints,
        required_permission=policy_result.required_permission,
        checked_payload=payload.candidate_payload,
    )


def _persist_governance_record(record: GovernanceRecord) -> None:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_governance_result(
            db,
            governance_id=record.governance_id,
            candidate_id=record.candidate_id,
            governance_status=record.governance_status,
            missing_fields=record.missing_fields,
            risk_hints=record.risk_hints,
            created_at=record.created_at,
        )
    finally:
        db.close()


def _build_governance_response(
    payload: S2GovernanceCheckRequest,
    record: GovernanceRecord,
    policy_result: GovernancePolicyResult,
) -> S2GovernanceCheckResponse:
    return S2GovernanceCheckResponse(
        governance_id=record.governance_id,
        candidate_id=record.candidate_id,
        input_session_id=payload.input_session_id or extract_input_session_id(payload.candidate_payload),
        governance_status=record.governance_status,
        missing_fields=record.missing_fields,
        risk_level=record.risk_level,
        question_prompts=record.question_prompts,
        validation_hints=record.validation_hints,
        risk_hints=record.risk_hints,
        required_permission=record.required_permission,
        next_action=policy_result.next_action,
        message=policy_result.message,
    )
