from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models import RawInput
from .json_utils import dump_json, load_json_field


def create_raw_input(
    db: Session,
    *,
    raw_input_id: str,
    source_type: str,
    raw_payload: Dict[str, Any],
    status: str,
    received_at,
) -> RawInput:
    row = RawInput(
        raw_input_id=raw_input_id,
        source_type=source_type,
        raw_payload=dump_json(raw_payload),
        status=status,
        received_at=received_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_raw_input(db: Session, raw_input_id: str) -> Optional[RawInput]:
    return db.query(RawInput).filter(RawInput.raw_input_id == raw_input_id).first()


def find_raw_input_by_idempotency_key(
    db: Session,
    idempotency_key: str,
) -> Optional[RawInput]:
    for row in db.query(RawInput).order_by(RawInput.id.desc()).all():
        try:
            payload = load_json_field(row.raw_payload)
        except ValueError:
            continue
        if payload.get("idempotency_key") == idempotency_key:
            return row
    return None
