from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.models import FactRecord
from app.db.repositories import create_fact_record, ensure_minimal_storage_tables, load_json_field
from app.db.session import DATABASE_URL, SessionLocal, engine
from app.modules.l3_query_view.router import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def _seed_fact(fact_id: str = "fact_read_001") -> str:
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_l3_001",
            candidate_id="cand_l3_001",
            governance_id="gov_l3_001",
            review_id="review_l3_001",
            fact_type="construction_record",
            fact_payload={"text": "正式事实只读视图内容"},
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


def _seed_invalid_json_fact(fact_id: str = "fact_invalid_json") -> str:
    db = SessionLocal()
    try:
        row = FactRecord(
            fact_id=fact_id,
            raw_input_id="raw_l3_invalid",
            candidate_id="cand_l3_invalid",
            governance_id="gov_l3_invalid",
            review_id="review_l3_invalid",
            fact_type="construction_record",
            fact_payload="{invalid-json",
            fact_status="active_fact",
            created_at=datetime.now(timezone.utc),
        )
        db.add(row)
        db.commit()
    finally:
        db.close()
    return fact_id


def test_read_existing_fact_record():
    fact_id = _seed_fact()

    response = client.get(f"/api/v1/l3/facts/{fact_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["fact_id"] == fact_id
    assert body["fact_type"] == "construction_record"
    assert body["fact_payload"]["text"] == "正式事实只读视图内容"
    assert body["fact_status"] == "active_fact"
    assert "created_at" in body


def test_missing_fact_id_returns_404():
    response = client.get("/api/v1/l3/facts/fact_missing")

    assert response.status_code == 404


def test_invalid_fact_payload_returns_sanitized_error():
    fact_id = _seed_invalid_json_fact()

    response = client.get(f"/api/v1/l3/facts/{fact_id}")

    assert response.status_code == 500
    assert response.json() == {"detail": "fact payload is invalid"}


def test_l3_does_not_write_fact_records():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.get(f"/api/v1/l3/facts/{fact_id}")

    assert response.status_code == 200
    assert _fact_count() == before_count


def test_l3_does_not_write_when_fact_missing():
    before_count = _fact_count()

    response = client.get("/api/v1/l3/facts/fact_missing")

    assert response.status_code == 404
    assert _fact_count() == before_count


def test_l3_does_not_reverse_write_l2_fact_record():
    fact_id = _seed_fact()

    response = client.get(f"/api/v1/l3/facts/{fact_id}")

    assert response.status_code == 200
    db = SessionLocal()
    try:
        row = db.query(FactRecord).filter(FactRecord.fact_id == fact_id).first()
        assert row is not None
        assert row.fact_status == "active_fact"
        assert load_json_field(row.fact_payload)["text"] == "正式事实只读视图内容"
    finally:
        db.close()


def test_l3_tests_do_not_use_real_database_file():
    assert DATABASE_URL == "sqlite:///:memory:" or not DATABASE_URL.endswith(
        (".db", ".sqlite", ".sqlite3")
    )
