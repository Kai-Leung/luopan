from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.db.models import PendingConfirmation
from .json_utils import dump_json


def create_pending_confirmation_record(
    db: Session,
    *,
    pending_id: str,
    input_session_id: str,
    raw_input_id: str,
    candidate_id: str,
    governance_id: str,
    governance_status: str,
    fact_type: str,
    fact_payload: dict[str, Any],
    display_text: str,
    required_permission: Optional[str],
    created_at,
) -> PendingConfirmation:
    row = PendingConfirmation(
        pending_id=pending_id,
        input_session_id=input_session_id,
        raw_input_id=raw_input_id,
        candidate_id=candidate_id,
        governance_id=governance_id,
        governance_status=governance_status,
        fact_type=fact_type,
        fact_payload=dump_json(fact_payload),
        display_text=display_text,
        required_permission=required_permission,
        pending_status="active",
        created_at=created_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_pending_confirmation(
    db: Session,
    pending_id: str,
) -> Optional[PendingConfirmation]:
    return (
        db.query(PendingConfirmation)
        .filter(PendingConfirmation.pending_id == pending_id)
        .first()
    )


def get_pending_confirmation_by_candidate_id(
    db: Session,
    candidate_id: str,
) -> Optional[PendingConfirmation]:
    return (
        db.query(PendingConfirmation)
        .filter(
            PendingConfirmation.candidate_id == candidate_id,
            PendingConfirmation.pending_status == "active",
        )
        .first()
    )


def list_pending_confirmation_records(db: Session) -> list[PendingConfirmation]:
    return (
        db.query(PendingConfirmation)
        .filter(PendingConfirmation.pending_status == "active")
        .order_by(PendingConfirmation.created_at.asc(), PendingConfirmation.id.asc())
        .all()
    )


def resolve_pending_confirmation(
    db: Session,
    *,
    pending_id: str,
    review_id: str,
    resolved_action: str,
    resolved_at: datetime,
) -> bool:
    result = db.execute(
        update(PendingConfirmation)
        .where(
            PendingConfirmation.pending_id == pending_id,
            PendingConfirmation.pending_status == "active",
        )
        .values(
            pending_status="resolved",
            resolved_at=resolved_at,
            review_id=review_id,
            resolved_action=resolved_action,
        )
    )
    return result.rowcount == 1
