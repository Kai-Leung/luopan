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


def _seed_fact(fact_id: str = "fact_l5_001") -> str:
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_l5_001",
            candidate_id="cand_l5_001",
            governance_id="gov_l5_001",
            review_id="review_l5_001",
            fact_type="construction_record",
            fact_payload={"text": "防水施工复核发现局部渗漏风险"},
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


def _create_analysis_id() -> tuple[str, str]:
    fact_id = _seed_fact()
    response = client.get("/api/v1/l4/analysis/preview", params={"fact_id": fact_id})
    assert response.status_code == 200
    return response.json()["analysis_id"], fact_id


def test_l5_draft_from_source_fact_id():
    fact_id = _seed_fact()

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    body = response.json()
    assert body["recommendation_id"].startswith("recommendation_")
    assert body["recommendation_status"] == "draft"
    assert body["source_fact_id"] == fact_id
    assert body["auto_executable"] is False
    assert "正式决策" in body["recommendation_summary"]


def test_l5_draft_from_analysis_id():
    analysis_id, fact_id = _create_analysis_id()
    response = client.post(
        "/api/v1/l5/recommendations/draft",
        json={"analysis_id": analysis_id},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_id"] == analysis_id
    assert body["source_fact_id"] == fact_id
    assert body["recommendation_status"] == "draft"
    assert body["auto_executable"] is False


def test_l5_draft_missing_source_fact_returns_clear_error():
    response = client.post(
        "/api/v1/l5/recommendations/draft",
        json={"source_fact_id": "fact_missing"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "source fact not found"}


def test_l5_draft_missing_analysis_returns_clear_error():
    response = client.post(
        "/api/v1/l5/recommendations/draft",
        json={"analysis_id": "missing_analysis"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "analysis preview not found"}


def test_l5_draft_auto_executable_false():
    fact_id = _seed_fact()

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    assert response.json()["auto_executable"] is False


def test_l5_draft_status_is_draft():
    fact_id = _seed_fact()

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    assert response.json()["recommendation_status"] == "draft"


def test_l5_draft_does_not_create_l2_fact():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    assert _fact_count() == before_count


def test_l5_draft_does_not_modify_l2_fact():
    fact_id = _seed_fact()
    before_payload = _load_fact_payload(fact_id)

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    assert _load_fact_payload(fact_id) == before_payload


def test_l5_draft_does_not_auto_trigger_l6():
    fact_id = _seed_fact()

    response = client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id})

    assert response.status_code == 200
    body = response.json()
    assert body["auto_executable"] is False
    assert "execution_id" not in body
