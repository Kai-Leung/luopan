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


def test_ai_assist_output_returns_to_l0_l1_without_creating_fact(
    reset_workflow_state,
):
    before_count = _fact_count()
    response = client.post(
        "/api/v1/ai-assist/candidates/intake",
        json={
            "model_call_ref": "model_call_test_001",
            "assist_type": "candidate_organization",
            "candidate_text": "AI 整理候选，仍需治理和人工确认",
            "uncertainty_hints": ["项目主体待核实"],
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


def test_ai_assist_requires_model_call_reference(reset_workflow_state):
    response = client.post(
        "/api/v1/ai-assist/candidates/intake",
        json={
            "model_call_ref": "",
            "assist_type": "gap_hint",
            "candidate_text": "缺口提示",
        },
    )

    assert response.status_code == 422
