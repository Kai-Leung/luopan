"""人工确认层最小 review 服务。

只消费 S2 governance 状态并写入 manual_reviews；不写 L2，不生成正式事实。
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.db.repositories import (
    create_manual_review,
    create_pending_confirmation_record,
    create_project_asset,
    ensure_minimal_storage_tables,
    get_manual_review_by_governance_id,
    get_pending_confirmation,
    get_pending_confirmation_by_candidate_id,
    list_pending_confirmation_records,
    load_json_field,
    resolve_pending_confirmation,
    update_candidate_status,
)
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
    ensure_minimal_storage_tables()
    db = SessionLocal()
    review_id = f"review_{uuid4().hex}"
    reviewed_at = datetime.now(timezone.utc)
    try:
        if get_manual_review_by_governance_id(db, payload.governance_id) is not None:
            raise HTTPException(
                status_code=409,
                detail="governance result has already been reviewed",
            )

        pending_record = _load_pending_for_review(db, payload)
        _validate_project_asset_review(payload, pending_record)
        if pending_record is not None and not resolve_pending_confirmation(
            db,
            pending_id=pending_record.pending_id,
            review_id=review_id,
            resolved_action=payload.review_action,
            resolved_at=reviewed_at,
        ):
            raise HTTPException(
                status_code=409,
                detail="pending confirmation has already been resolved",
            )

        project_asset = _create_project_asset_if_allowed(
            db,
            payload,
            pending_record,
            review_id,
            reviewed_at,
        )
        record = _build_confirmation_record(
            payload,
            review_id,
            project_asset,
            reviewed_at,
        )
        create_manual_review(
            db,
            review_id=record.review_id,
            governance_id=record.governance_id,
            review_action=record.review_action,
            review_status=record.review_status,
            policy_decision=record.policy_decision,
            reviewed_at=record.created_at,
            commit=False,
        )
        _update_candidate_status_if_confirmed(db, payload, pending_record)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="pending confirmation or governance result has already been reviewed",
        ) from exc
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    MANUAL_CONFIRMATION_STORE.append(record)
    if pending_record is not None:
        PENDING_CONFIRMATION_QUEUE[:] = [
            pending
            for pending in PENDING_CONFIRMATION_QUEUE
            if pending.pending_id != pending_record.pending_id
        ]
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


def _load_pending_for_review(
    db,
    payload: ManualConfirmationReviewRequest,
) -> Optional[PendingConfirmationRecord]:
    if payload.pending_id is None:
        return None
    row = get_pending_confirmation(db, payload.pending_id)
    if row is None:
        raise HTTPException(status_code=400, detail="pending confirmation not found")
    if row.pending_status != "active":
        raise HTTPException(
            status_code=409,
            detail="pending confirmation has already been resolved",
        )
    if row.governance_id != payload.governance_id:
        raise HTTPException(
            status_code=400,
            detail="pending confirmation does not belong to governance result",
        )
    if row.governance_status != payload.governance_status:
        raise HTTPException(
            status_code=400,
            detail="pending confirmation governance status does not match",
        )
    return _pending_row_to_record(row)


def _build_confirmation_record(
    payload: ManualConfirmationReviewRequest,
    review_id: str,
    project_asset: Optional[dict],
    reviewed_at: datetime,
) -> ManualConfirmationRecord:
    review_status = REVIEW_STATUS_BY_ACTION[payload.review_action]
    return ManualConfirmationRecord(
        review_id=review_id,
        governance_id=payload.governance_id,
        created_at=reviewed_at,
        governance_status=payload.governance_status,
        review_action=payload.review_action,
        review_status=review_status,
        policy_decision="manual_review_required",
        project_asset=project_asset,
    )


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
    db,
    payload: ManualConfirmationReviewRequest,
    pending_record: Optional[PendingConfirmationRecord],
    review_id: str,
    created_at: datetime,
) -> Optional[dict]:
    if pending_record is None:
        return None

    if not _is_project_asset_pending(pending_record):
        return None

    if payload.review_action != "confirm":
        return None

    return _create_confirmed_project_asset(
        db,
        pending_record,
        payload,
        review_id,
        created_at,
    )


def _is_project_asset_pending(record: PendingConfirmationRecord) -> bool:
    return (
        record.fact_type == PROJECT_ASSET_CANDIDATE_KIND
        or record.fact_payload.get("candidate_type") == PROJECT_ASSET_CANDIDATE_KIND
    )


def _validate_project_asset_review(
    payload: ManualConfirmationReviewRequest,
    pending_record: Optional[PendingConfirmationRecord],
) -> None:
    if pending_record is None or not _is_project_asset_pending(pending_record):
        return
    if payload.review_action != "confirm":
        return
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
    project_name = pending_record.fact_payload.get("project_name")
    if not isinstance(project_name, str) or not project_name.strip():
        raise HTTPException(status_code=400, detail="project_name is required")


def _create_confirmed_project_asset(
    db,
    pending_record: PendingConfirmationRecord,
    payload: ManualConfirmationReviewRequest,
    review_id: str,
    created_at: datetime,
) -> dict:
    fact_payload = pending_record.fact_payload
    project_name = str(fact_payload["project_name"]).strip()
    project_asset_id = f"project_asset_{uuid4().hex}"
    row = create_project_asset(
        db,
        project_asset_id=project_asset_id,
        project_name=project_name,
        customer_name=_optional_text(fact_payload.get("customer_name")),
        project_address=_optional_text(fact_payload.get("project_address")),
        source_candidate_id=pending_record.candidate_id,
        source_raw_input_id=pending_record.raw_input_id,
        status="active_project_asset",
        created_at=created_at,
        confirmed_by=_optional_text(payload.confirmed_by),
        confirmation_id=review_id,
        commit=False,
    )

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
    db,
    payload: ManualConfirmationReviewRequest,
    pending_record: Optional[PendingConfirmationRecord],
) -> None:
    if payload.review_action != "confirm" or pending_record is None:
        return
    update_candidate_status(
        db,
        candidate_id=pending_record.candidate_id,
        candidate_status="confirmed_candidate",
        commit=False,
    )


def create_pending_confirmation(
    payload: PendingConfirmationCreateRequest,
) -> PendingConfirmationItem:
    _ensure_pending_confirmation_allowed(payload)
    record = _build_pending_confirmation_record(payload)
    try:
        _persist_pending_confirmation(record)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="candidate already has pending confirmation",
        ) from exc
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
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        if get_pending_confirmation_by_candidate_id(db, payload.candidate_id) is not None:
            logger.warning("pending confirmation rejected because candidate already has pending item")
            raise HTTPException(
                status_code=400,
                detail="candidate already has pending confirmation",
            )
    finally:
        db.close()


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


def _persist_pending_confirmation(record: PendingConfirmationRecord) -> None:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_pending_confirmation_record(
            db,
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
            created_at=record.created_at,
        )
    finally:
        db.close()


def list_pending_confirmations() -> PendingConfirmationListResponse:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        records = [_pending_row_to_record(row) for row in list_pending_confirmation_records(db)]
        return PendingConfirmationListResponse(
            items=[_to_pending_item(record) for record in records]
        )
    finally:
        db.close()


def _pending_row_to_record(row) -> PendingConfirmationRecord:
    return PendingConfirmationRecord(
        pending_id=row.pending_id,
        input_session_id=row.input_session_id,
        raw_input_id=row.raw_input_id,
        candidate_id=row.candidate_id,
        governance_id=row.governance_id,
        governance_status=row.governance_status,
        fact_type=row.fact_type,
        fact_payload=load_json_field(row.fact_payload),
        display_text=row.display_text,
        required_permission=row.required_permission,
        created_at=row.created_at,
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
