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


def _seed_fact(fact_id: str = "fact_l6_001") -> str:
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_l6_001",
            candidate_id="cand_l6_001",
            governance_id="gov_l6_001",
            review_id="review_l6_001",
            fact_type="construction_record",
            fact_payload={"text": "施工响应记录来源事实"},
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


def _create_recommendation_id() -> tuple[str, str]:
    fact_id = _seed_fact()
    response = client.post(
        "/api/v1/l5/recommendations/draft",
        json={"source_fact_id": fact_id},
    )
    assert response.status_code == 200
    return response.json()["recommendation_id"], fact_id


def test_l6_response_from_recommendation_id():
    recommendation_id, fact_id = _create_recommendation_id()
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": recommendation_id,
            "execution_note": "已通知现场复核",
            "execution_status": "responded",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["execution_response_id"].startswith("execution_response_")
    assert body["recommendation_id"] == recommendation_id
    assert body["source_fact_id"] == fact_id
    assert body["execution_status"] == "responded"
    assert body["execution_note"] == "已通知现场复核"
    assert body["creates_fact"] is False


def test_l6_response_from_source_fact_id():
    fact_id = _seed_fact()

    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": fact_id,
            "execution_note": "已登记执行响应",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source_fact_id"] == fact_id
    assert body["creates_fact"] is False


def test_l6_missing_recommendation_returns_clear_error():
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": "missing_recommendation",
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "recommendation draft not found"}


def test_l6_missing_source_fact_returns_clear_error():
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": "fact_missing",
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "source fact not found"}


def test_l6_creates_fact_false():
    recommendation_id, _ = _create_recommendation_id()
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": recommendation_id,
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    assert response.json()["creates_fact"] is False


def test_l6_does_not_create_l2_fact():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": fact_id,
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    assert _fact_count() == before_count


def test_l6_does_not_modify_l2_fact():
    fact_id = _seed_fact()
    before_payload = _load_fact_payload(fact_id)

    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": fact_id,
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    assert _load_fact_payload(fact_id) == before_payload


def test_l6_does_not_auto_trigger_l7():
    recommendation_id, _ = _create_recommendation_id()
    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": recommendation_id,
            "execution_note": "响应记录",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["creates_fact"] is False
    assert "feedback_id" not in body
