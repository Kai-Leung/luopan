from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import GovernanceResult
from .json_utils import dump_json


def create_governance_result(
    db: Session,
    *,
    governance_id: str,
    candidate_id: str,
    governance_status: str,
    missing_fields: List[str],
    risk_hints: List[str],
    created_at,
) -> GovernanceResult:
    row = GovernanceResult(
        governance_id=governance_id,
        candidate_id=candidate_id,
        governance_status=governance_status,
        missing_fields=dump_json(missing_fields),
        risk_hints=dump_json(risk_hints),
        created_at=created_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_governance_result(db: Session, governance_id: str) -> Optional[GovernanceResult]:
    return db.query(GovernanceResult).filter(GovernanceResult.governance_id == governance_id).first()
