from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import ManualReview


def create_manual_review(
    db: Session,
    *,
    review_id: str,
    governance_id: str,
    review_action: str,
    review_status: str,
    policy_decision: str,
    reviewed_at,
) -> ManualReview:
    row = ManualReview(
        review_id=review_id,
        governance_id=governance_id,
        review_action=review_action,
        review_status=review_status,
        policy_decision=policy_decision,
        reviewed_at=reviewed_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_manual_review(db: Session, review_id: str) -> Optional[ManualReview]:
    return db.query(ManualReview).filter(ManualReview.review_id == review_id).first()
