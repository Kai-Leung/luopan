from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from .json_utils import dump_json


def create_fact_record(
    db: Session,
    *,
    fact_id: str,
    raw_input_id: str,
    candidate_id: str,
    governance_id: str,
    review_id: str,
    fact_type: str,
    fact_payload: Dict[str, Any],
    fact_status: str,
    created_at,
) -> "FactRecord":
    from app.db.models import FactRecord

    row = FactRecord(
        fact_id=fact_id,
        raw_input_id=raw_input_id,
        candidate_id=candidate_id,
        governance_id=governance_id,
        review_id=review_id,
        fact_type=fact_type,
        fact_payload=dump_json(fact_payload),
        fact_status=fact_status,
        created_at=created_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_fact_record(db: Session, fact_id: str) -> Optional["FactRecord"]:
    from app.db.models import FactRecord

    return db.query(FactRecord).filter(FactRecord.fact_id == fact_id).first()
