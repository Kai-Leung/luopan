import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.l2_fact.schemas import L2FactCreateRequest
from app.modules.l2_fact.service import create_l2_fact
from app.modules.l3_query_view.router import router as l3_router
from app.modules.s2_governance_gate.confirmation.schemas import (
    ManualConfirmationReviewRequest,
    PendingConfirmationCreateRequest,
)
from app.modules.s2_governance_gate.confirmation.service import create_pending_confirmation, review_confirmation
from app.modules.s2_governance_gate.schemas import S2GovernanceCheckRequest
from app.modules.s2_governance_gate.service import check_candidate_governance

pytestmark = pytest.mark.usefixtures("reset_workflow_state")

app = FastAPI()
app.include_router(l3_router, prefix="/api/v1")
client = TestClient(app)


def test_l0_l3_e2e_confirmed_candidate_becomes_readable_fact():
    text = "今天张工在宝山项目完成普通记录"
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
            candidate_payload=candidate.candidate_payload,
        )
    )
    review = review_confirmation(
        ManualConfirmationReviewRequest(
            governance_id=governance.governance_id,
            governance_status=governance.governance_status,
            review_action="confirm",
        )
    )
    fact = create_l2_fact(
        L2FactCreateRequest(
            raw_input_id=raw.raw_input_id,
            candidate_id=candidate.candidate_id,
            governance_id=governance.governance_id,
            review_id=review.review_id,
            review_status=review.review_status,
            fact_type=candidate.candidate_payload["fact_record_type"],
            fact_payload={"text": text},
        )
    )

    response = client.get(f"/api/v1/l3/facts/{fact.fact_id}")

    assert raw.status == "received_only"
    assert candidate.candidate_status == "new_candidate"
    assert governance.governance_status == "auto_pass"
    assert governance.next_action == "need_confirm"
    assert review.review_status == "confirmed_candidate"
    assert fact.fact_status == "active_fact"
    assert response.status_code == 200
    assert response.json()["fact_id"] == fact.fact_id
    assert response.json()["fact_payload"]["text"] == text


def test_material_purchase_record_can_enter_l2_and_be_queried():
    text = "宝山项目张三买了500袋水泥，花了3200元"
    raw = receive_raw_input(RawInputCreate(text=text, source_type="manual_input"))
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            raw_payload={"text": text},
            source_type="manual_input",
        )
    )
    candidate_item = candidate.candidates[0]
    governance = check_candidate_governance(
        S2GovernanceCheckRequest(
            candidate_id=candidate_item.candidate_id,
            candidate_status=candidate_item.candidate_status,
            candidate_payload=candidate_item.candidate_payload,
        )
    )
    pending = create_pending_confirmation(
        PendingConfirmationCreateRequest(
            raw_input_id=raw.raw_input_id,
            input_session_id=raw.input_session_id,
            candidate_id=candidate_item.candidate_id,
            governance_id=governance.governance_id,
            governance_status=governance.governance_status,
            fact_type=candidate_item.candidate_payload["fact_record_type"],
            fact_payload=candidate_item.candidate_payload,
            display_text=candidate_item.candidate_payload["candidate_summary"],
        )
    )
    review = review_confirmation(
        ManualConfirmationReviewRequest(
            governance_id=governance.governance_id,
            governance_status=governance.governance_status,
            review_action="confirm",
            pending_id=pending.pending_id,
        )
    )
    fact = create_l2_fact(
        L2FactCreateRequest(
            raw_input_id=raw.raw_input_id,
            candidate_id=candidate_item.candidate_id,
            governance_id=governance.governance_id,
            review_id=review.review_id,
            review_status=review.review_status,
            fact_type=candidate_item.candidate_payload["fact_record_type"],
            fact_payload=candidate_item.candidate_payload,
        )
    )

    response = client.get("/api/v1/l3/facts", params={"keyword": "水泥"})

    assert len(candidate.candidates) == 1
    assert candidate_item.candidate_payload["primary_subject_id"] == "张三"
    assert candidate_item.candidate_payload["material_asset_id"] == "水泥"
    assert candidate_item.candidate_payload["amount_text"] == "花了3200元"
    assert governance.governance_status == "auto_pass"
    assert governance.next_action == "need_confirm"
    assert review.review_status == "confirmed_candidate"
    assert fact.fact_status == "active_fact"
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["fact_id"] == fact.fact_id


def test_project_asset_candidate_flow_creates_project_asset_without_l2_fact():
    text = "新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼"
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
            candidate_payload=candidate.candidate_payload,
        )
    )
    pending = create_pending_confirmation(
        PendingConfirmationCreateRequest(
            raw_input_id=raw.raw_input_id,
            candidate_id=candidate.candidate_id,
            governance_id=governance.governance_id,
            governance_status=governance.governance_status,
            fact_type=candidate.candidate_payload["candidate_type"],
            fact_payload=candidate.candidate_payload,
            display_text=candidate.candidate_payload["candidate_summary"],
            required_permission=governance.required_permission,
        )
    )
    review = review_confirmation(
        ManualConfirmationReviewRequest(
            governance_id=governance.governance_id,
            governance_status=governance.governance_status,
            review_action="confirm",
            pending_id=pending.pending_id,
            required_permission="project_asset:create",
        )
    )

    assert candidate.candidate_payload["candidate_type"] == "project_asset_candidate"
    assert governance.governance_status == "needs_confirmation"
    assert governance.required_permission == "project_asset:create"
    assert pending.required_permission == "project_asset:create"
    assert pending.fact_payload["project_name"] == "宝山刘老师家"
    assert review.review_status == "confirmed_candidate"
    assert review.project_asset is not None
    assert review.project_asset["project_name"] == "宝山刘老师家"
    assert "fact_id" not in review.project_asset
    assert not hasattr(pending, "fact_id")
    assert not hasattr(pending, "project_id")
