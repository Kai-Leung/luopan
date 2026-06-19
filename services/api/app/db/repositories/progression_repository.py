from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import (
    AnalysisRecord,
    AuditEvent,
    ExecutionResponseRecord,
    FeedbackRecord,
    RecommendationRecord,
)


def create_audit_event(db: Session, **values) -> AuditEvent:
    row = AuditEvent(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_audit_events(
    db: Session,
    *,
    organization_id: str,
    source_fact_id: Optional[str] = None,
    trace_ref: Optional[str] = None,
) -> list[AuditEvent]:
    query = db.query(AuditEvent).filter(AuditEvent.organization_id == organization_id)
    if source_fact_id:
        query = query.filter(AuditEvent.source_fact_id == source_fact_id)
    if trace_ref:
        query = query.filter(AuditEvent.trace_ref == trace_ref)
    return query.order_by(AuditEvent.created_at.asc(), AuditEvent.id.asc()).all()


def create_analysis_record(db: Session, **values) -> AnalysisRecord:
    row = AnalysisRecord(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_analysis_record(db: Session, analysis_id: str) -> Optional[AnalysisRecord]:
    return db.query(AnalysisRecord).filter(AnalysisRecord.analysis_id == analysis_id).first()


def create_recommendation_record(db: Session, **values) -> RecommendationRecord:
    row = RecommendationRecord(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_recommendation_record(
    db: Session,
    recommendation_id: str,
) -> Optional[RecommendationRecord]:
    return (
        db.query(RecommendationRecord)
        .filter(RecommendationRecord.recommendation_id == recommendation_id)
        .first()
    )


def create_execution_response_record(db: Session, **values) -> ExecutionResponseRecord:
    row = ExecutionResponseRecord(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_execution_response_record(
    db: Session,
    execution_response_id: str,
) -> Optional[ExecutionResponseRecord]:
    return (
        db.query(ExecutionResponseRecord)
        .filter(ExecutionResponseRecord.execution_response_id == execution_response_id)
        .first()
    )


def create_feedback_record(db: Session, **values) -> FeedbackRecord:
    row = FeedbackRecord(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_feedback_record(db: Session, feedback_id: str) -> Optional[FeedbackRecord]:
    return db.query(FeedbackRecord).filter(FeedbackRecord.feedback_id == feedback_id).first()
