from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models import RawInput
from .json_utils import dump_json


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
