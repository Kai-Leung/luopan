"""L3 正式事实列表视图测试。

覆盖：无结果、基础分页、fact_type 筛选、keyword 筛选。
"""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.repositories import create_fact_record, ensure_minimal_storage_tables
from app.db.session import DATABASE_URL, SessionLocal, engine
from app.modules.l3_query_view.router import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def _reset_tables():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def setup_function():
    _reset_tables()
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def _seed_facts():
    """Seed 3 facts for list testing."""
    facts = [
        ("fact_list_001", "construction_record", {"text": "宝山刘老师家防水施工", "source_type": "manual_input"}),
        ("fact_list_002", "construction_record", {"text": "李师傅家水电改造", "source_type": "manual_input"}),
        ("fact_list_003", "material_record", {"text": "市三院采购瓷砖", "source_type": "manual_confirmation"}),
    ]
    db = SessionLocal()
    try:
        for fid, ftype, fpayload in facts:
            create_fact_record(
                db,
                fact_id=fid,
                raw_input_id=f"raw_{fid}",
                candidate_id=f"cand_{fid}",
                governance_id=f"gov_{fid}",
                review_id=f"review_{fid}",
                fact_type=ftype,
                fact_payload=fpayload,
                fact_status="active_fact",
                created_at=datetime.now(timezone.utc),
            )
    finally:
        db.close()


class TestL3FactList:
    def setup_method(self):
        _reset_tables()

    def test_list_returns_all_items(self):
        _seed_facts()
        resp = client.get("/api/v1/l3/facts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    def test_list_filters_by_fact_type(self):
        _seed_facts()
        resp = client.get("/api/v1/l3/facts?fact_type=material_record")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["fact_type"] == "material_record"

    def test_list_pagination_limit(self):
        _seed_facts()
        resp = client.get("/api/v1/l3/facts?limit=2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3

    def test_list_pagination_offset(self):
        _seed_facts()
        resp = client.get("/api/v1/l3/facts?limit=1&offset=2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 1

    def test_list_keyword_search(self):
        _seed_facts()
        resp = client.get("/api/v1/l3/facts?keyword=防水")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 1
        assert "防水" in data["items"][0]["fact_payload_summary"]

    def test_list_no_results(self):
        resp = client.get("/api/v1/l3/facts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 0
        assert data["total"] == 0


def _reset_tables():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)
