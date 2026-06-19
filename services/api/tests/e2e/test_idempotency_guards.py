from fastapi.testclient import TestClient

from app.main import app
from app.modules.s2_governance_gate.confirmation.schemas import ManualConfirmationReviewRequest
from app.modules.s2_governance_gate.confirmation.service import review_confirmation


client = TestClient(app)


def test_l0_same_idempotency_key_returns_same_raw_input(reset_workflow_state):
    payload = {
        "text": "同一条现场记录",
        "source_type": "manual_input",
        "idempotency_key": "idempotency-l0-001",
    }

    first = client.post("/api/v1/l0/raw-input", json=payload)
    second = client.post("/api/v1/l0/raw-input", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["raw_input_id"] == second.json()["raw_input_id"]


def test_same_governance_result_cannot_be_reviewed_twice(
    reset_workflow_state,
    build_confirmed_candidate_chain,
):
    _, _, governance, review = build_confirmed_candidate_chain("confirm")

    assert review.review_status == "confirmed_candidate"
    try:
        review_confirmation(
            ManualConfirmationReviewRequest(
                governance_id=governance.governance_id,
                governance_status=governance.governance_status,
                review_action="confirm",
            )
        )
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 409
    else:
        raise AssertionError("governance result must not be reviewed twice")


def test_l2_same_review_returns_existing_fact(
    reset_workflow_state,
    build_confirmed_candidate_chain,
    build_fact_payload,
):
    raw, candidate, governance, review = build_confirmed_candidate_chain("confirm")
    payload = build_fact_payload(raw, candidate, governance, review)

    first = client.post("/api/v1/l2/source-of-truth/facts", json=payload)
    second = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["fact_id"] == second.json()["fact_id"]
    assert second.json()["message"] == "fact record already exists"
