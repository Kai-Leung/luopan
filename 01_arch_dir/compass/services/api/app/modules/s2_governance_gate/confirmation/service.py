"""人工确认层最小 review 服务。

只消费 S2 governance 状态并写入 manual_reviews；不写 L2，不生成正式事实。
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import create_manual_review, create_project_asset, ensure_minimal_storage_tables, update_candidate_status
from app.db.session import SessionLocal
from app.modules.s2_governance_gate.confirmation.models import ManualConfirmationRecord, PendingConfirmationRecord
from app.modules.s2_governance_gate.confirmation.schemas import (
    ManualConfirmationReviewRequest,
    ManualConfirmationReviewResponse,
    PendingConfirmationCreateRequest,
    PendingConfirmationItem,
    PendingConfirmationListResponse,
    ReviewStatus,
)
from app.modules.standard_governance.rules.project_asset_rules import (
    PROJECT_ASSET_CANDIDATE_KIND,
    PROJECT_ASSET_PERMISSION,
)

MANUAL_CONFIRMATION_STORE: List[ManualConfirmationRecord] = []
PENDING_CONFIRMATION_QUEUE: List[PendingConfirmationRecord] = []

REVIEW_STATUS_BY_ACTION: dict[str, ReviewStatus] = {
    "confirm": "confirmed_candidate",
    "return_for_completion": "returned_for_completion",
    "reject": "rejected_candidate",
}

logger = logging.getLogger(__name__)


def review_confirmation(
    payload: ManualConfirmationReviewRequest,
) -> ManualConfirmationReviewResponse:
    _ensure_reviewable_governance_status(payload.governance_status)
    review_id = f"review_{uuid4().hex}"
    project_asset = _create_project_asset_if_allowed(payload, review_id)
    record = _build_confirmation_record(payload, review_id, project_asset)
    MANUAL_CONFIRMATION_STORE.append(record)
    _persist_manual_review(record)
    _update_candidate_status_if_confirmed(payload, record)
    return _build_confirmation_response(record)


def _ensure_reviewable_governance_status(governance_status: str) -> None:
    if governance_status == "needs_completion":
        logger.warning("manual confirmation rejected for needs_completion governance status")
        raise HTTPException(
            status_code=400,
            detail="needs_completion governance result cannot be reviewed",
        )

    if governance_status == "blocked":
        logger.warning("manual confirmation rejected for blocked governance status")
        raise HTTPException(
            status_code=400,
            detail="blocked governance result cannot be reviewed",
        )


def _resolve_candidate_id_from_pending(pending_id: str) -> Optional[str]:
    for pending in PENDING_CONFIRMATION_QUEUE:
        if pending.pending_id == pending_id:
            return pending.candidate_id
    return None


def _build_confirmation_record(
    payload: ManualConfirmationReviewRequest,
    review_id: str,
    project_asset: Optional[dict],
) -> ManualConfirmationRecord:
    review_status = REVIEW_STATUS_BY_ACTION[payload.review_action]
    return ManualConfirmationRecord(
        review_id=review_id,
        governance_id=payload.governance_id,
        created_at=datetime.now(timezone.utc),
        governance_status=payload.governance_status,
        review_action=payload.review_action,
        review_status=review_status,
        policy_decision="manual_review_required",
        project_asset=project_asset,
    )


def _persist_manual_review(record: ManualConfirmationRecord) -> None:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_manual_review(
            db,
            review_id=record.review_id,
            governance_id=record.governance_id,
            review_action=record.review_action,
            review_status=record.review_status,
            policy_decision=record.policy_decision,
            reviewed_at=record.created_at,
        )
    finally:
        db.close()


def _build_confirmation_response(
    record: ManualConfirmationRecord,
) -> ManualConfirmationReviewResponse:
    return ManualConfirmationReviewResponse(
        review_id=record.review_id,
        governance_id=record.governance_id,
        review_status=record.review_status,
        policy_decision=record.policy_decision,
        message="manual confirmation reviewed",
        project_asset=record.project_asset,
    )


def _create_project_asset_if_allowed(
    payload: ManualConfirmationReviewRequest,
    review_id: str,
) -> Optional[dict]:
    if payload.pending_id is None:
        return None

    pending_record = _find_pending_confirmation(payload.pending_id)
    if not _is_project_asset_pending(pending_record):
        return None

    if payload.review_action != "confirm":
        return None

    _ensure_project_asset_confirmation_allowed(payload, pending_record)
    return _create_confirmed_project_asset(pending_record, payload, review_id)


def _find_pending_confirmation(pending_id: str) -> PendingConfirmationRecord:
    for record in PENDING_CONFIRMATION_QUEUE:
        if record.pending_id == pending_id:
            return record
    raise HTTPException(status_code=400, detail="pending confirmation not found")


def _is_project_asset_pending(record: PendingConfirmationRecord) -> bool:
    return (
        record.fact_type == PROJECT_ASSET_CANDIDATE_KIND
        or record.fact_payload.get("candidate_type") == PROJECT_ASSET_CANDIDATE_KIND
    )


def _ensure_project_asset_confirmation_allowed(
    payload: ManualConfirmationReviewRequest,
    pending_record: PendingConfirmationRecord,
) -> None:
    if payload.governance_status != "needs_confirmation":
        raise HTTPException(
            status_code=400,
            detail="project asset candidate requires manual confirmation governance status",
        )
    if payload.required_permission != PROJECT_ASSET_PERMISSION:
        raise HTTPException(
            status_code=400,
            detail="project_asset:create permission is required",
        )
    if pending_record.required_permission != PROJECT_ASSET_PERMISSION:
        raise HTTPException(
            status_code=400,
            detail="pending confirmation lacks project_asset:create permission",
        )


def _create_confirmed_project_asset(
    pending_record: PendingConfirmationRecord,
    payload: ManualConfirmationReviewRequest,
    review_id: str,
) -> dict:
    fact_payload = pending_record.fact_payload
    project_name = fact_payload.get("project_name")
    if not isinstance(project_name, str) or not project_name.strip():
        raise HTTPException(status_code=400, detail="project_name is required")

    created_at = datetime.now(timezone.utc)
    project_asset_id = f"project_asset_{uuid4().hex}"
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        row = create_project_asset(
            db,
            project_asset_id=project_asset_id,
            project_name=project_name.strip(),
            customer_name=_optional_text(fact_payload.get("customer_name")),
            project_address=_optional_text(fact_payload.get("project_address")),
            source_candidate_id=pending_record.candidate_id,
            source_raw_input_id=pending_record.raw_input_id,
            status="active_project_asset",
            created_at=created_at,
            confirmed_by=_optional_text(payload.confirmed_by),
            confirmation_id=review_id,
        )
    finally:
        db.close()

    return {
        "project_asset_id": row.project_asset_id,
        "project_name": row.project_name,
        "customer_name": row.customer_name,
        "project_address": row.project_address,
        "source_candidate_id": row.source_candidate_id,
        "source_raw_input_id": row.source_raw_input_id,
        "status": row.status,
        "created_at": row.created_at.isoformat(),
        "confirmed_by": row.confirmed_by,
        "confirmation_id": row.confirmation_id,
    }


def _optional_text(value: object) -> Optional[str]:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _update_candidate_status_if_confirmed(
    payload: ManualConfirmationReviewRequest,
    record: ManualConfirmationRecord,
) -> None:
    if payload.review_action != "confirm":
        return
    candidate_id = _resolve_candidate_id_from_pending(payload.pending_id)
    if not candidate_id:
        return
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        update_candidate_status(
            db,
            candidate_id=candidate_id,
            candidate_status="confirmed_candidate",
        )
    finally:
        db.close()


def create_pending_confirmation(
    payload: PendingConfirmationCreateRequest,
) -> PendingConfirmationItem:
    _ensure_pending_confirmation_allowed(payload)
    record = _build_pending_confirmation_record(payload)
    PENDING_CONFIRMATION_QUEUE.append(record)
    return _to_pending_item(record)


def _ensure_pending_confirmation_allowed(payload: PendingConfirmationCreateRequest) -> None:
    if payload.governance_status == "needs_completion":
        logger.warning("pending confirmation rejected for needs_completion governance status")
        raise HTTPException(
            status_code=400,
            detail=f"{payload.governance_status} governance result cannot enter pending confirmation",
        )
    if payload.governance_status == "blocked":
        logger.warning("pending confirmation rejected for blocked governance status")
        raise HTTPException(
            status_code=400,
            detail=f"{payload.governance_status} governance result cannot enter pending confirmation",
        )
    if payload.governance_status not in ("auto_pass", "needs_confirmation"):
        logger.warning("pending confirmation rejected for unsupported governance status")
        raise HTTPException(status_code=400, detail="unsupported governance_status")
    if any(record.candidate_id == payload.candidate_id for record in PENDING_CONFIRMATION_QUEUE):
        logger.warning("pending confirmation rejected because candidate already has pending item")
        raise HTTPException(
            status_code=400,
            detail="candidate already has pending confirmation",
        )


def _build_pending_confirmation_record(
    payload: PendingConfirmationCreateRequest,
) -> PendingConfirmationRecord:
    return PendingConfirmationRecord(
        pending_id=f"pending_{uuid4().hex}",
        input_session_id=payload.input_session_id or f"session_{payload.raw_input_id.removeprefix('raw_')}",
        raw_input_id=payload.raw_input_id,
        candidate_id=payload.candidate_id,
        governance_id=payload.governance_id,
        governance_status=payload.governance_status,
        fact_type=payload.fact_type,
        fact_payload=payload.fact_payload,
        display_text=payload.display_text,
        required_permission=payload.required_permission,
        created_at=datetime.now(timezone.utc),
    )


def list_pending_confirmations() -> PendingConfirmationListResponse:
    return PendingConfirmationListResponse(
        items=[_to_pending_item(record) for record in PENDING_CONFIRMATION_QUEUE]
    )


def _to_pending_item(record: PendingConfirmationRecord) -> PendingConfirmationItem:
    return PendingConfirmationItem(
        pending_id=record.pending_id,
        input_session_id=record.input_session_id,
        raw_input_id=record.raw_input_id,
        candidate_id=record.candidate_id,
        governance_id=record.governance_id,
        governance_status=record.governance_status,
        fact_type=record.fact_type,
        fact_payload=record.fact_payload,
        display_text=record.display_text,
        required_permission=record.required_permission,
        created_at=record.created_at.isoformat(),
    )
