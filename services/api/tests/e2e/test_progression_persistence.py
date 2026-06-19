from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.models import (
    AnalysisRecord,
    AuditEvent,
    ExecutionResponseRecord,
    FeedbackRecord,
    RecommendationRecord,
)
from app.db.repositories import create_fact_record, ensure_minimal_storage_tables
from app.db.session import SessionLocal, engine
from app.main import app


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def test_l3_l7_records_persist_and_feedback_returns_to_l1():
    fact_id = "fact_progression_001"
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_progression_001",
            candidate_id="cand_progression_001",
            governance_id="gov_progression_001",
            review_id="review_progression_001",
            fact_type="construction_record",
            fact_payload={"text": "现场问题等待闭环"},
            fact_status="active_fact",
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()

    analysis = client.get("/api/v1/l4/analysis/preview", params={"fact_id": fact_id})
    assert analysis.status_code == 200

    recommendation = client.post(
        "/api/v1/l5/recommendations/draft",
        json={
            "analysis_id": analysis.json()["analysis_id"],
            "source_fact_id": fact_id,
        },
    )
    assert recommendation.status_code == 200

    execution = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": recommendation.json()["recommendation_id"],
            "source_fact_id": fact_id,
            "execution_note": "已记录处理响应",
            "execution_status": "recorded",
        },
    )
    assert execution.status_code == 200

    feedback = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution.json()["execution_response_id"],
            "source_fact_id": fact_id,
            "feedback_note": "需要补充现场复核结果",
            "feedback_type": "follow_up",
        },
    )
    assert feedback.status_code == 200
    assert feedback.json()["governance_required"] is True

    trace = client.get("/api/v1/s3/trace/summary", params={"source_fact_id": fact_id})
    assert trace.status_code == 200
    action_types = {event["action_type"] for event in trace.json()["events"]}
    assert "analysis_preview_created" in action_types
    assert "recommendation_draft_created" in action_types
    assert "execution_response_recorded" in action_types
    assert "feedback_returned_to_candidate_flow" in action_types

    db = SessionLocal()
    try:
        assert db.query(AnalysisRecord).count() == 1
        assert db.query(RecommendationRecord).count() == 1
        assert db.query(ExecutionResponseRecord).count() == 1
        assert db.query(FeedbackRecord).count() == 1
        assert db.query(AuditEvent).count() >= 4
    finally:
        db.close()
