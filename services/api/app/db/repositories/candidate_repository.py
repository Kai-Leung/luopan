from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models import Candidate
from .json_utils import dump_json


def create_candidate(
    db: Session,
    *,
    candidate_id: str,
    raw_input_id: str,
    candidate_status: str,
    candidate_payload: Dict[str, Any],
    created_at,
) -> Candidate:
    row = Candidate(
        candidate_id=candidate_id,
        raw_input_id=raw_input_id,
        candidate_status=candidate_status,
        candidate_payload=dump_json(candidate_payload),
        created_at=created_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_candidate(db: Session, candidate_id: str) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()


def update_candidate_payload(
    db: Session,
    *,
    candidate_id: str,
    candidate_payload: Dict[str, Any],
) -> Optional[Candidate]:
    row = get_candidate(db, candidate_id)
    if row is None:
        return None
    row.candidate_payload = dump_json(candidate_payload)
    db.commit()
    db.refresh(row)
    return row


def update_candidate_status(
    db: Session,
    *,
    candidate_id: str,
    candidate_status: str,
) -> Optional[Candidate]:
    row = get_candidate(db, candidate_id)
    if row is None:
        return None
    row.candidate_status = candidate_status
    db.commit()
    db.refresh(row)
    return row
