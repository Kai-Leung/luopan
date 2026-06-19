from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.router import router
from app.db.base import Base
from app.db.models import FactRecord
from app.db.repositories import create_fact_record, ensure_minimal_storage_tables, load_json_field
from app.db.session import SessionLocal, engine
from app.modules.l0_input.router import router as l0_router
from app.modules.l1_candidate.router import router as l1_router
from app.modules.l2_fact.router import router as l2_router
from app.modules.s2_governance_gate.router import router as s2_router
from app.modules.standard_governance.processing import StandardBoundaryNotice

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)

source_app = FastAPI()
source_app.include_router(l0_router, prefix="/api/v1")
source_app.include_router(l1_router, prefix="/api/v1")
source_app.include_router(s2_router, prefix="/api/v1")
source_app.include_router(l2_router, prefix="/api/v1")
source_client = TestClient(source_app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    ensure_minimal_storage_tables(include_fact_records=True)


def _seed_fact(fact_id: str = "fact_horizontal_001") -> str:
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_horizontal_001",
            candidate_id="cand_horizontal_001",
            governance_id="gov_horizontal_001",
            review_id="review_horizontal_001",
            fact_type="construction_record",
            fact_payload={"text": "横向治理来源事实"},
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


def _fact_payload(fact_id: str) -> dict:
    db = SessionLocal()
    try:
        row = db.query(FactRecord).filter(FactRecord.fact_id == fact_id).first()
        assert row is not None
        return load_json_field(row.fact_payload)
    finally:
        db.close()


def test_standard_boundary_notice_defaults_to_no_write_l2():
    notice = StandardBoundaryNotice(
        processing_direction="readonly",
        message="只读处理，不写 L2",
    )

    assert notice.readonly is True
    assert notice.no_write_l2 is True


def test_l4_standard_processing_fields_and_no_l2_write():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.get("/api/v1/l4/analysis/preview", params={"fact_id": fact_id})

    assert response.status_code == 200
    body = response.json()
    assert body["processing_direction"] == "readonly"
    assert body["source_fact_id"] == fact_id
    assert body["trace_ref"].startswith("trace_")
    assert body["readonly"] is True
    assert _fact_count() == before_count


def test_l5_standard_processing_fields_and_no_l2_write():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.post(
        "/api/v1/l5/recommendations/draft",
        json={"source_fact_id": fact_id},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["processing_direction"] == "draft"
    assert body["source_fact_id"] == fact_id
    assert body["trace_ref"].startswith("trace_")
    assert body["auto_executable"] is False
    assert _fact_count() == before_count


def test_l6_standard_processing_fields_and_no_l2_write():
    fact_id = _seed_fact()
    before_payload = _fact_payload(fact_id)
    before_count = _fact_count()

    response = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "source_fact_id": fact_id,
            "execution_note": "仅记录响应",
            "execution_status": "recorded",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["processing_direction"] == "response"
    assert body["source_fact_id"] == fact_id
    assert body["trace_ref"].startswith("trace_")
    assert body["creates_fact"] is False
    assert _fact_count() == before_count
    assert _fact_payload(fact_id) == before_payload


def test_l7_standard_processing_fields_and_no_l2_write():
    fact_id = _seed_fact()
    before_payload = _fact_payload(fact_id)
    before_count = _fact_count()

    response = client.post(
        "/api/v1/l7/feedback",
        json={
            "source_fact_id": fact_id,
            "feedback_note": "仅反馈候选",
            "feedback_type": "follow_up",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["processing_direction"] == "candidate"
    assert body["source_fact_id"] == fact_id
    assert body["trace_ref"].startswith("trace_")
    assert body["returns_to_candidate_flow"] is True
    assert _fact_count() == before_count
    assert _fact_payload(fact_id) == before_payload


def test_s3_trace_summary_returns_no_write_l2_event():
    fact_id = _seed_fact()
    before_count = _fact_count()

    response = client.get("/api/v1/s3/trace/summary", params={"source_fact_id": fact_id})

    assert response.status_code == 200
    body = response.json()
    assert body["source_fact_id"] == fact_id
    assert body["trace_ref"].startswith("trace_")
    assert body["no_write_l2"] is True
    assert body["events"][0]["no_write_l2"] is True
    assert body["events"][0]["readonly"] is True
    assert _fact_count() == before_count


def test_s2_missing_required_fields_does_not_pass_normally():
    response = source_client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_horizontal_missing",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "现场完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["next_action"] == "ask_more"


def test_invalid_source_type_is_rejected_before_l2():
    response = source_client.post(
        "/api/v1/l0/raw-input",
        json={"text": "非法来源输入", "source_type": "illegal_source"},
    )

    assert response.status_code == 422


def test_forged_confirmed_review_without_record_is_rejected_by_l2():
    response = source_client.post(
        "/api/v1/l2/source-of-truth/facts",
        json={
            "raw_input_id": "raw_missing",
            "candidate_id": "cand_missing",
            "governance_id": "gov_missing",
            "review_id": "review_missing",
            "review_status": "confirmed_candidate",
            "fact_type": "construction_record",
            "fact_payload": {"text": "伪造确认不得入链"},
        },
    )

    assert response.status_code == 400
    assert _fact_count() == 0


def test_l4_l7_outputs_do_not_contain_l2_fact_creation_keys():
    fact_id = _seed_fact()
    responses = [
        client.get("/api/v1/l4/analysis/preview", params={"fact_id": fact_id}),
        client.post("/api/v1/l5/recommendations/draft", json={"source_fact_id": fact_id}),
        client.post(
            "/api/v1/l6/execution-responses",
            json={
                "source_fact_id": fact_id,
                "execution_note": "仅记录响应",
                "execution_status": "recorded",
            },
        ),
        client.post(
            "/api/v1/l7/feedback",
            json={"source_fact_id": fact_id, "feedback_note": "仅候选回流"},
        ),
    ]

    for response in responses:
        assert response.status_code == 200
        body = response.json()
        assert "fact_id" not in body
        assert "review_status" not in body
        assert "rule_id" not in body
