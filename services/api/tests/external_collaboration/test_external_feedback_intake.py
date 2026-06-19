from fastapi.testclient import TestClient

from app.db.models import FactRecord
from app.db.session import SessionLocal
from app.main import app


client = TestClient(app)


def _fact_count() -> int:
    db = SessionLocal()
    try:
        return db.query(FactRecord).count()
    finally:
        db.close()


def test_external_feedback_returns_to_l0_l1_without_creating_fact(
    reset_workflow_state,
):
    before_count = _fact_count()
    response = client.post(
        "/api/v1/external-collaboration/feedback/intake",
        json={
            "external_source": "partner_portal",
            "source_reference": "receipt_001",
            "feedback_type": "partner_receipt",
            "content": "合作方回执成功，但仍需治理确认",
            "attachment_refs": ["upload_external_001"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["raw_input_id"].startswith("raw_")
    assert body["candidate_ids"][0].startswith("cand_")
    assert body["governance_required"] is True
    assert body["creates_fact"] is False
    assert body["next_stage"] == "s2_governance"
    assert _fact_count() == before_count


def test_external_feedback_requires_source_reference(reset_workflow_state):
    response = client.post(
        "/api/v1/external-collaboration/feedback/intake",
        json={
            "external_source": "partner_portal",
            "source_reference": "",
            "feedback_type": "external_status",
            "content": "外部状态",
        },
    )

    assert response.status_code == 422
