from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.router import router
from app.db.base import Base
from app.db.models import FactRecord
from app.db.repositories import create_fact_record, ensure_minimal_storage_tables, load_json_field
from app.db.session import SessionLocal, engine

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def _seed_fact(fact_id: str = "fact_l7_001") -> str:
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_l7_001",
            candidate_id="cand_l7_001",
            governance_id="gov_l7_001",
            review_id="review_l7_001",
            fact_type="construction_record",
            fact_payload={"text": "反馈候选来源事实"},
            fact_status="active_fact",
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()
    return fact_id


def _fact_count() -> int:
    db = SessionLocal()
    try:
        return db.query(FactRecord).count()
    finally:
        db.close()


def _load_fact_payload(fact_id: str) -> dict:
    db = SessionLocal()
    try:
        row = db.query(FactRecord).filter(FactRecord.fact_id == fact_id).first()
        assert row is not None
        return load_json_field(row.fact_payload)
    finally:
        db.close()


def _create_execution_response_id() -> tuple[str, str]:
    fact_id = _seed_fact()
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": fact_id,
            "execution_note": "测试执行响应",
            "execution_status": "recorded",
        },
    )
    assert response.status_code == 200
    return response.json()["execution_response_id"], fact_id


def test_l7_feedback_from_execution_response_id():
    execution_response_id, fact_id = _create_execution_response_id()
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution_response_id,
            "feedback_note": "执行响应后需要补充现场照片",
            "feedback_type": "supplement",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["feedback_id"].startswith("feedback_")
    assert body["feedback_status"] == "candidate"
    assert body["execution_response_id"] == execution_response_id
    assert body["source_fact_id"] == fact_id
    assert body["feedback_note"] == "执行响应后需要补充现场照片"
    assert body["feedback_type"] == "supplement"
    assert body["returns_to_candidate_flow"] is True
    assert body["governance_required"] is True
    assert body["return_raw_input_id"].startswith("raw_")
    assert body["return_candidate_id"].startswith("cand_")


def test_l7_feedback_from_source_fact_id():
    fact_id = _seed_fact()

    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "source_fact_id": fact_id,
            "feedback_note": "事实后续反馈候选",
            "feedback_type": "follow_up",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source_fact_id"] == fact_id
    assert body["feedback_status"] == "candidate"
    assert body["returns_to_candidate_flow"] is True


def test_l7_missing_execution_response_returns_clear_error():
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": "missing_execution",
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "execution response not found"}


def test_l7_missing_source_fact_returns_clear_error():
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "source_fact_id": "fact_missing",
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "source fact not found"}


def test_l7_feedback_status_is_candidate():
    execution_response_id, _ = _create_execution_response_id()
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution_response_id,
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback_status"] == "candidate"


def test_l7_returns_to_candidate_flow_true():
    execution_response_id, _ = _create_execution_response_id()
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution_response_id,
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 200
    assert response.json()["returns_to_candidate_flow"] is True


def test_l7_does_not_create_l2_fact():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "source_fact_id": fact_id,
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 200
    assert _fact_count() == before_count


def test_l7_does_not_modify_l2_fact():
    fact_id = _seed_fact()
    before_payload = _load_fact_payload(fact_id)

    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "source_fact_id": fact_id,
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 200
    assert _load_fact_payload(fact_id) == before_payload


def test_l7_does_not_publish_rules_or_enter_fact_chain():
    execution_response_id, _ = _create_execution_response_id()
    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution_response_id,
            "feedback_note": "反馈候选",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["returns_to_candidate_flow"] is True
    assert "fact_id" not in body
    assert "rule_id" not in body
