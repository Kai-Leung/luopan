from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.db.models import FactRecord
from app.db.repositories import create_fact_record
from app.db.session import SessionLocal
from app.main import app
from app.modules.l0_input.service import RAW_INPUT_MEMORY_STORE
from app.modules.l1_candidate.service import CANDIDATE_MEMORY_STORE
from app.modules.l2_fact.service import FACT_RECORD_MEMORY_STORE
from app.modules.s2_governance_gate.confirmation.service import (
    MANUAL_CONFIRMATION_STORE,
    PENDING_CONFIRMATION_QUEUE,
)
from app.modules.s2_governance_gate.service import GOVERNANCE_MEMORY_STORE
from app.modules.upload import service as upload_service


pytestmark = pytest.mark.usefixtures("reset_workflow_state")
client = TestClient(app)


def _create_governed_candidate(text: str) -> tuple[dict, dict, dict]:
    raw_response = client.post(
        "/api/v1/l0/raw-input",
        json={"text": text, "source_type": "manual_input"},
    )
    assert raw_response.status_code == 200
    raw = raw_response.json()

    candidate_response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw["raw_input_id"],
            "input_session_id": raw["input_session_id"],
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )
    assert candidate_response.status_code == 200
    candidate_group = candidate_response.json()
    candidate = candidate_group["candidates"][0]

    governance_response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": candidate["candidate_id"],
            "input_session_id": candidate["input_session_id"],
            "candidate_status": candidate["candidate_status"],
            "candidate_payload": candidate["candidate_payload"],
        },
    )
    assert governance_response.status_code == 200
    return raw, candidate, governance_response.json()


def test_l0_l3_closure_survives_memory_reset_and_is_idempotent():
    text = "今天张师傅在宝山项目做了卫生间防水"
    raw, candidate, governance = _create_governed_candidate(text)
    assert governance["next_action"] == "need_confirm"

    pending_response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": raw["raw_input_id"],
            "input_session_id": raw["input_session_id"],
            "candidate_id": candidate["candidate_id"],
            "governance_id": governance["governance_id"],
            "governance_status": governance["governance_status"],
            "fact_type": candidate["candidate_payload"]["fact_record_type"],
            "fact_payload": candidate["candidate_payload"],
            "display_text": candidate["candidate_payload"]["candidate_summary"],
        },
    )
    assert pending_response.status_code == 200
    pending = pending_response.json()

    RAW_INPUT_MEMORY_STORE.clear()
    CANDIDATE_MEMORY_STORE.clear()
    GOVERNANCE_MEMORY_STORE.clear()
    MANUAL_CONFIRMATION_STORE.clear()
    PENDING_CONFIRMATION_QUEUE.clear()

    listed = client.get("/api/v1/manual-confirmation/pending")
    assert listed.status_code == 200
    assert [item["pending_id"] for item in listed.json()["items"]] == [pending["pending_id"]]

    review_response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "pending_id": pending["pending_id"],
            "governance_id": governance["governance_id"],
            "governance_status": governance["governance_status"],
            "review_action": "confirm",
        },
    )
    assert review_response.status_code == 200
    review = review_response.json()
    assert client.get("/api/v1/manual-confirmation/pending").json()["items"] == []

    fact_payload = {
        "raw_input_id": raw["raw_input_id"],
        "candidate_id": candidate["candidate_id"],
        "governance_id": governance["governance_id"],
        "review_id": review["review_id"],
        "review_status": review["review_status"],
        "fact_type": candidate["candidate_payload"]["fact_record_type"],
        "fact_payload": candidate["candidate_payload"],
    }
    first_fact = client.post("/api/v1/l2/source-of-truth/facts", json=fact_payload)
    second_fact = client.post("/api/v1/l2/source-of-truth/facts", json=fact_payload)
    assert first_fact.status_code == 200
    assert second_fact.status_code == 200
    assert second_fact.json()["fact_id"] == first_fact.json()["fact_id"]

    FACT_RECORD_MEMORY_STORE.clear()
    facts = client.get("/api/v1/l3/facts", params={"keyword": "防水"})
    assert facts.status_code == 200
    assert facts.json()["items"][0]["fact_id"] == first_fact.json()["fact_id"]

    db = SessionLocal()
    try:
        assert db.query(FactRecord).count() == 1
    finally:
        db.close()


@pytest.mark.parametrize(
    ("text", "expected_status"),
    [
        ("今天张师傅做了卫生间防水", "needs_completion"),
        ("今天张师傅在宝山项目禁止入链", "blocked"),
    ],
)
def test_incomplete_and_blocked_candidates_cannot_enter_pending(text: str, expected_status: str):
    raw, candidate, governance = _create_governed_candidate(text)
    assert governance["governance_status"] == expected_status

    pending = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": raw["raw_input_id"],
            "candidate_id": candidate["candidate_id"],
            "governance_id": governance["governance_id"],
            "governance_status": governance["governance_status"],
            "fact_type": candidate["candidate_payload"]["fact_record_type"],
            "fact_payload": candidate["candidate_payload"],
            "display_text": candidate["candidate_payload"]["candidate_summary"],
        },
    )
    assert pending.status_code == 400
    assert client.get("/api/v1/manual-confirmation/pending").json()["items"] == []


def test_s1_rejects_partial_and_out_of_scope_context_headers():
    partial = client.get(
        "/api/v1/s1/runtime-context/current",
        headers={"X-Compass-User-Id": "user_compass_owner"},
    )
    out_of_scope = client.post(
        "/api/v1/l0/raw-input",
        headers={
            "X-Compass-User-Id": "user_compass_owner",
            "X-Compass-Organization-Id": "org_other",
            "X-Compass-Role": "owner",
        },
        json={"text": "越权输入", "source_type": "manual_input"},
    )

    assert partial.status_code == 400
    assert out_of_scope.status_code == 403


@pytest.mark.parametrize(
    ("review_action", "expected_review_status"),
    [
        ("return_for_completion", "returned_for_completion"),
        ("reject", "rejected_candidate"),
    ],
)
def test_non_confirm_review_resolves_pending_without_allowing_l2(
    review_action: str,
    expected_review_status: str,
):
    raw, candidate, governance = _create_governed_candidate(
        "今天张师傅在宝山项目做了卫生间防水"
    )
    pending = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": raw["raw_input_id"],
            "input_session_id": raw["input_session_id"],
            "candidate_id": candidate["candidate_id"],
            "governance_id": governance["governance_id"],
            "governance_status": governance["governance_status"],
            "fact_type": candidate["candidate_payload"]["fact_record_type"],
            "fact_payload": candidate["candidate_payload"],
            "display_text": candidate["candidate_payload"]["candidate_summary"],
        },
    ).json()
    review = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "pending_id": pending["pending_id"],
            "governance_id": pending["governance_id"],
            "governance_status": pending["governance_status"],
            "review_action": review_action,
        },
    )

    assert review.status_code == 200
    assert review.json()["review_status"] == expected_review_status
    assert client.get("/api/v1/manual-confirmation/pending").json()["items"] == []

    l2 = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json={
            "raw_input_id": raw["raw_input_id"],
            "candidate_id": candidate["candidate_id"],
            "governance_id": governance["governance_id"],
            "review_id": review.json()["review_id"],
            "review_status": review.json()["review_status"],
            "fact_type": candidate["candidate_payload"]["fact_record_type"],
            "fact_payload": candidate["candidate_payload"],
        },
    )
    assert l2.status_code == 400
    assert l2.json()["detail"] == "only confirmed_candidate can enter L2"


def test_l4_l7_are_traceable_and_never_create_an_l2_fact():
    fact_id = "fact_integration_progression"
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id=fact_id,
            raw_input_id="raw_progression",
            candidate_id="cand_progression",
            governance_id="gov_progression",
            review_id="review_progression",
            fact_type="construction_record",
            fact_payload={"text": "防水施工已完成"},
            fact_status="active_fact",
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()

    analysis = client.get("/api/v1/l4/analysis/preview", params={"fact_id": fact_id})
    assert analysis.status_code == 200
    assert analysis.json()["readonly"] is True

    recommendation = client.post(
        "/api/v1/l5/recommendations/draft",
        json={
            "analysis_id": analysis.json()["analysis_id"],
            "source_fact_id": fact_id,
        },
    )
    assert recommendation.status_code == 200
    assert recommendation.json()["auto_executable"] is False

    execution = client.post(
        "/api/v1/l6/execution-responses",
        json={
            "recommendation_id": recommendation.json()["recommendation_id"],
            "source_fact_id": fact_id,
            "execution_note": "仅记录响应",
            "execution_status": "recorded",
        },
    )
    assert execution.status_code == 200
    assert execution.json()["creates_fact"] is False

    feedback = client.post(
        "/api/v1/l7/feedback",
        json={
            "execution_response_id": execution.json()["execution_response_id"],
            "source_fact_id": fact_id,
            "feedback_note": "回到候选治理",
            "feedback_type": "follow_up",
        },
    )
    assert feedback.status_code == 200
    assert feedback.json()["returns_to_candidate_flow"] is True
    assert feedback.json()["governance_required"] is True

    trace = client.get("/api/v1/s3/trace/summary", params={"source_fact_id": fact_id})
    assert trace.status_code == 200
    assert {
        "analysis_preview_created",
        "recommendation_draft_created",
        "execution_response_recorded",
        "feedback_returned_to_candidate_flow",
    }.issubset({event["action_type"] for event in trace.json()["events"]})

    db = SessionLocal()
    try:
        assert db.query(FactRecord).count() == 1
    finally:
        db.close()


def test_upload_acceptance_validates_type_size_and_original_path(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    accepted = client.post(
        "/api/v1/upload/files",
        files={"file": ("site.jpg", b"jpg-bytes", "image/jpeg")},
    )
    unsupported = client.post(
        "/api/v1/upload/files",
        files={"file": ("notes.txt", b"text", "text/plain")},
    )
    oversized = client.post(
        "/api/v1/upload/files",
        files={"file": ("large.jpg", b"x" * (10 * 1024 * 1024 + 1), "image/jpeg")},
    )

    assert accepted.status_code == 200
    saved_path = upload_service.UPLOAD_ROOT / accepted.json()["storage_path"].split("/")[-1]
    assert saved_path.read_bytes() == b"jpg-bytes"
    assert unsupported.status_code == 415
    assert oversized.status_code == 413
