from datetime import datetime, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.db.repositories import (
    create_governance_result,
    create_manual_review,
    get_fact_record,
    load_json_field,
)
from app.db.session import DATABASE_URL, SessionLocal
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.l2_fact.router import router
from app.modules.l2_fact.service import FACT_RECORD_MEMORY_STORE
from app.modules.s2_governance_gate.confirmation.schemas import ManualConfirmationReviewRequest
from app.modules.s2_governance_gate.confirmation.service import review_confirmation
from app.modules.s2_governance_gate.schemas import S2GovernanceCheckRequest
from app.modules.s2_governance_gate.service import check_candidate_governance

pytestmark = pytest.mark.usefixtures("reset_workflow_state")

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def test_confirmed_candidate_can_enter_l2(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()

    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json=build_fact_payload(raw, candidate, governance, review),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["fact_id"].startswith("fact_")
    assert body["fact_status"] == "active_fact"
    assert body["fact_payload"]["text"] == "今天张工在宝山项目现场质量问题需要确认"


def test_returned_for_completion_cannot_enter_l2(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain("return_for_completion")

    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json=build_fact_payload(raw, candidate, governance, review),
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert "confirmed_candidate" in detail or "blocked governance" in detail
    assert FACT_RECORD_MEMORY_STORE == []


def test_rejected_candidate_cannot_enter_l2(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain("reject")

    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json=build_fact_payload(raw, candidate, governance, review),
    )

    assert response.status_code == 400
    assert FACT_RECORD_MEMORY_STORE == []


def test_blocked_governance_source_cannot_enter_l2():
    raw = receive_raw_input(RawInputCreate(text="普通输入", source_type="manual_input"))
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            raw_payload={"text": "普通输入"},
            source_type="manual_input",
        )
    )
    governance_id = "gov_blocked"
    review_id = "review_blocked"
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        create_governance_result(
            db,
            governance_id=governance_id,
            candidate_id=candidate.candidate_id,
            governance_status="blocked",
            missing_fields=[],
            risk_hints=["invalid_candidate_status"],
            created_at=now,
        )
        create_manual_review(
            db,
            review_id=review_id,
            governance_id=governance_id,
            review_action="confirm",
            review_status="confirmed_candidate",
            policy_decision="manual_review_required",
            reviewed_at=now,
        )
    finally:
        db.close()

    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json={
            "raw_input_id": raw.raw_input_id,
            "candidate_id": candidate.candidate_id,
            "governance_id": governance_id,
            "review_id": review_id,
            "review_status": "confirmed_candidate",
            "fact_type": candidate.candidate_payload["fact_record_type"],
            "fact_payload": {"text": "普通输入"},
        },
    )

    assert response.status_code == 400


def test_auto_pass_cannot_bypass_confirmation():
    text = "今天张工在宝山项目记录普通输入"
    raw = receive_raw_input(RawInputCreate(text=text, source_type="manual_input"))
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            raw_payload={"text": text},
            source_type="manual_input",
        )
    )
    governance = check_candidate_governance(
        S2GovernanceCheckRequest(
            candidate_id=candidate.candidate_id,
            candidate_status=candidate.candidate_status,
            candidate_payload={"text": text},
        )
    )

    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json={
            "raw_input_id": raw.raw_input_id,
            "candidate_id": candidate.candidate_id,
            "governance_id": governance.governance_id,
            "review_id": "review_missing",
            "review_status": "confirmed_candidate",
            "fact_type": candidate.candidate_payload["fact_record_type"],
            "fact_payload": {"text": text},
        },
    )

    assert governance.governance_status == "auto_pass"
    assert response.status_code == 400


def test_needs_completion_cannot_reach_l2_through_confirmation():
    raw = receive_raw_input(RawInputCreate(text="现场完成普通记录", source_type="manual_input"))
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            raw_payload={"text": "现场完成普通记录"},
            source_type="manual_input",
        )
    )
    governance = check_candidate_governance(
        S2GovernanceCheckRequest(
            candidate_id=candidate.candidate_id,
            candidate_status=candidate.candidate_status,
            candidate_payload={"text": "现场完成普通记录"},
        )
    )

    try:
        review_confirmation(
            ManualConfirmationReviewRequest(
                governance_id=governance.governance_id,
                governance_status=governance.governance_status,
                review_action="confirm",
            )
        )
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
    else:
        raise AssertionError("needs_completion governance status must not be reviewed")

    assert governance.governance_status == "needs_completion"
    assert FACT_RECORD_MEMORY_STORE == []


def test_missing_raw_input_id_is_rejected(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["raw_input_id"] = ""

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 400


def test_missing_candidate_id_is_rejected(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["candidate_id"] = ""

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 400


def test_missing_governance_id_is_rejected(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["governance_id"] = ""

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 400


def test_missing_review_id_is_rejected(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["review_id"] = ""

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 400


def test_success_writes_fact_records(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json=build_fact_payload(raw, candidate, governance, review),
    )

    assert response.status_code == 200
    db = SessionLocal()
    try:
        row = get_fact_record(db, response.json()["fact_id"])
        assert row is not None
        assert row.fact_status == "active_fact"
        assert load_json_field(row.fact_payload)["text"] == "今天张工在宝山项目现场质量问题需要确认"
    finally:
        db.close()


def test_fact_type_must_match_candidate_fact_record_type(
    build_confirmed_candidate_chain,
    build_fact_payload,
):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["fact_type"] = "financial_record"

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 400
    assert "fact_type" in response.json()["detail"]
    assert FACT_RECORD_MEMORY_STORE == []


def test_non_standard_fact_type_is_rejected(
    build_confirmed_candidate_chain,
    build_fact_payload,
):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    payload = build_fact_payload(raw, candidate, governance, review)
    payload["fact_type"] = "custom_fact_record"

    response = client.post("/api/v1/l2/source-of-truth/facts", json=payload)

    assert response.status_code == 422
    assert FACT_RECORD_MEMORY_STORE == []


def test_response_does_not_generate_l3_view(build_confirmed_candidate_chain, build_fact_payload):
    raw, candidate, governance, review = build_confirmed_candidate_chain()
    response = client.post(
        "/api/v1/l2/source-of-truth/facts",
        json=build_fact_payload(raw, candidate, governance, review),
    )

    assert response.status_code == 200
    body = response.json()
    assert "view_id" not in body
    assert "l3_view" not in body


def test_l2_tests_do_not_use_real_database_file():
    assert DATABASE_URL == "sqlite:///:memory:" or not DATABASE_URL.endswith(
        (".db", ".sqlite", ".sqlite3")
    )
