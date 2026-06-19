from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.db.repositories import get_project_asset
from app.db.session import SessionLocal
from app.modules.s2_governance_gate.confirmation.router import router
from app.modules.s2_governance_gate.confirmation.service import (
    MANUAL_CONFIRMATION_STORE,
    PENDING_CONFIRMATION_QUEUE,
)

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def setup_function():
    MANUAL_CONFIRMATION_STORE.clear()
    PENDING_CONFIRMATION_QUEUE.clear()


def test_confirm_candidate():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_001",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 200
    assert response.json()["review_status"] == "confirmed_candidate"


def test_return_for_completion():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_002",
            "governance_status": "needs_confirmation",
            "review_action": "return_for_completion",
        },
    )

    assert response.status_code == 200
    assert response.json()["review_status"] == "returned_for_completion"


def test_reject_candidate():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_003",
            "governance_status": "needs_confirmation",
            "review_action": "reject",
        },
    )

    assert response.status_code == 200
    assert response.json()["review_status"] == "rejected_candidate"


def test_blocked_governance_cannot_review():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_004",
            "governance_status": "blocked",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 400


def test_needs_completion_governance_cannot_review():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_needs_completion",
            "governance_status": "needs_completion",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 400
    assert MANUAL_CONFIRMATION_STORE == []


def test_policy_decision_is_manual_review_required():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_005",
            "governance_status": "auto_pass",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 200
    assert response.json()["policy_decision"] == "manual_review_required"


def test_response_does_not_generate_formal_fact():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_006",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "fact_id" not in body
    assert "truth_record" not in body
    assert "l2_snapshot_id" not in body


def test_memory_store_does_not_call_l2():
    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_007",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
        },
    )

    assert response.status_code == 200
    assert len(MANUAL_CONFIRMATION_STORE) == 1
    record = MANUAL_CONFIRMATION_STORE[0]
    assert record.review_status == "confirmed_candidate"
    assert not hasattr(record, "l2_snapshot_id")


def test_auto_pass_can_enter_pending_confirmation_queue():
    response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_001",
            "candidate_id": "cand_001",
            "governance_id": "gov_pending_auto",
            "governance_status": "auto_pass",
            "fact_type": "construction_record",
            "fact_payload": {"text": "今天张工在宝山项目记录普通事项"},
            "display_text": "今天张工在宝山项目记录普通事项",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["pending_id"].startswith("pending_")
    assert body["input_session_id"].startswith("session_")
    assert body["governance_status"] == "auto_pass"
    assert len(PENDING_CONFIRMATION_QUEUE) == 1


def test_needs_confirmation_can_enter_pending_confirmation_queue():
    response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_002",
            "candidate_id": "cand_002",
            "governance_id": "gov_pending_manual",
            "governance_status": "needs_confirmation",
            "fact_type": "construction_record",
            "fact_payload": {"text": "今天张工在宝山项目涉及金额确认"},
            "display_text": "今天张工在宝山项目涉及金额确认",
        },
    )

    assert response.status_code == 200
    assert response.json()["governance_status"] == "needs_confirmation"
    assert len(PENDING_CONFIRMATION_QUEUE) == 1


def test_project_asset_candidate_can_enter_pending_confirmation_without_creating_project():
    response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_project_001",
            "candidate_id": "cand_project_001",
            "governance_id": "gov_project_pending",
            "governance_status": "needs_confirmation",
            "fact_type": "project_asset_candidate",
            "fact_payload": {
                "candidate_type": "project_asset_candidate",
                "raw_text": "新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼",
                "project_name": "宝山刘老师家",
                "customer_name": "刘老师",
                "project_address": "宝山一号楼",
            },
            "display_text": "项目创建候选：宝山刘老师家；刘老师；宝山一号楼",
            "required_permission": "project_asset:create",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["fact_type"] == "project_asset_candidate"
    assert body["fact_payload"]["project_name"] == "宝山刘老师家"
    assert body["fact_payload"]["customer_name"] == "刘老师"
    assert body["fact_payload"]["project_address"] == "宝山一号楼"
    assert body["required_permission"] == "project_asset:create"
    assert "项目已创建" not in body["display_text"]
    assert "project_id" not in body
    assert "fact_id" not in body
    assert len(PENDING_CONFIRMATION_QUEUE) == 1


def test_project_asset_candidate_confirm_with_permission_creates_project_asset():
    pending = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_project_create_001",
            "candidate_id": "cand_project_create_001",
            "governance_id": "gov_project_create_001",
            "governance_status": "needs_confirmation",
            "fact_type": "project_asset_candidate",
            "fact_payload": {
                "candidate_type": "project_asset_candidate",
                "project_name": "宝山刘老师家",
                "customer_name": "刘老师",
                "project_address": "宝山一号楼",
            },
            "display_text": "项目创建候选：宝山刘老师家；刘老师；宝山一号楼",
            "required_permission": "project_asset:create",
        },
    ).json()

    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_project_create_001",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
            "pending_id": pending["pending_id"],
            "required_permission": "project_asset:create",
            "confirmed_by": "manual_reviewer",
        },
    )

    assert response.status_code == 200
    body = response.json()
    project_asset = body["project_asset"]
    assert body["review_status"] == "confirmed_candidate"
    assert project_asset["project_asset_id"].startswith("project_asset_")
    assert project_asset["project_name"] == "宝山刘老师家"
    assert project_asset["customer_name"] == "刘老师"
    assert project_asset["project_address"] == "宝山一号楼"
    assert project_asset["source_candidate_id"] == "cand_project_create_001"
    assert project_asset["source_raw_input_id"] == "raw_project_create_001"
    assert project_asset["confirmed_by"] == "manual_reviewer"
    assert project_asset["confirmation_id"] == body["review_id"]
    assert "fact_id" not in project_asset
    db = SessionLocal()
    try:
        row = get_project_asset(db, project_asset["project_asset_id"])
        assert row is not None
        assert row.project_name == "宝山刘老师家"
    finally:
        db.close()


def test_project_asset_candidate_confirm_without_permission_is_blocked():
    pending = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_project_create_002",
            "candidate_id": "cand_project_create_002",
            "governance_id": "gov_project_create_002",
            "governance_status": "needs_confirmation",
            "fact_type": "project_asset_candidate",
            "fact_payload": {
                "candidate_type": "project_asset_candidate",
                "project_name": "宝山刘老师家",
            },
            "display_text": "项目创建候选：宝山刘老师家",
            "required_permission": "project_asset:create",
        },
    ).json()

    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_project_create_002",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
            "pending_id": pending["pending_id"],
        },
    )

    assert response.status_code == 400
    assert "project_asset:create" in response.json()["detail"]


def test_non_project_candidate_confirm_does_not_create_project_asset():
    pending = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_regular_pending",
            "candidate_id": "cand_regular_pending",
            "governance_id": "gov_regular_pending",
            "governance_status": "needs_confirmation",
            "fact_type": "construction_record",
            "fact_payload": {"text": "今天张工在宝山项目涉及金额确认"},
            "display_text": "今天张工在宝山项目涉及金额确认",
        },
    ).json()

    response = client.post(
        "/api/v1/manual-confirmation/review",
        json={
            "governance_id": "gov_regular_pending",
            "governance_status": "needs_confirmation",
            "review_action": "confirm",
            "pending_id": pending["pending_id"],
            "required_permission": "project_asset:create",
        },
    )

    assert response.status_code == 200
    assert response.json()["project_asset"] is None


def test_needs_completion_cannot_enter_pending_confirmation_queue():
    response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_003",
            "candidate_id": "cand_003",
            "governance_id": "gov_pending_completion",
            "governance_status": "needs_completion",
            "fact_type": "construction_record",
            "fact_payload": {"text": "现场完成普通记录"},
            "display_text": "现场完成普通记录",
        },
    )

    assert response.status_code == 400
    assert PENDING_CONFIRMATION_QUEUE == []


def test_blocked_cannot_enter_pending_confirmation_queue():
    response = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_004",
            "candidate_id": "cand_004",
            "governance_id": "gov_pending_blocked",
            "governance_status": "blocked",
            "fact_type": "construction_record",
            "fact_payload": {"text": "普通记录"},
            "display_text": "普通记录",
        },
    )

    assert response.status_code == 400
    assert PENDING_CONFIRMATION_QUEUE == []


def test_pending_confirmation_queue_list():
    created = client.post(
        "/api/v1/manual-confirmation/pending",
        json={
            "raw_input_id": "raw_005",
            "candidate_id": "cand_005",
            "governance_id": "gov_pending_list",
            "governance_status": "auto_pass",
            "fact_type": "construction_record",
            "fact_payload": {"text": "今天张工在宝山项目记录普通事项"},
            "display_text": "今天张工在宝山项目记录普通事项",
        },
    ).json()

    listed = client.get("/api/v1/manual-confirmation/pending")
    assert listed.status_code == 200
    assert listed.json()["items"][0]["pending_id"] == created["pending_id"]


def test_confirm_updates_candidate_status_in_db(
    reset_workflow_state,
    build_confirmed_candidate_chain,
):
    """确认后 candidate.status 应从 new_candidate 变为 confirmed_candidate。"""
    from app.db.repositories import get_candidate
    from app.db.session import SessionLocal

    raw, candidate, governance, review = build_confirmed_candidate_chain("confirm")

    # review 确认后，candidate DB 状态应该是 confirmed_candidate
    db = SessionLocal()
    try:
        row = get_candidate(db, candidate.candidate_id)
        assert row is not None, "候选应存在于 DB"
        assert row.candidate_status == "confirmed_candidate", (
            f"候选状态应为 confirmed_candidate，实际为 {row.candidate_status}"
        )
    finally:
        db.close()

    assert review.review_status == "confirmed_candidate"


def test_same_candidate_cannot_enter_pending_confirmation_twice():
    payload = {
        "raw_input_id": "raw_dup_001",
        "input_session_id": "session_dup_001",
        "candidate_id": "cand_dup_001",
        "governance_id": "gov_pending_dup",
        "governance_status": "auto_pass",
        "fact_type": "construction_record",
        "fact_payload": {"text": "今天张工在宝山项目记录普通事项"},
        "display_text": "今天张工在宝山项目记录普通事项",
    }

    first = client.post("/api/v1/manual-confirmation/pending", json=payload)
    second = client.post("/api/v1/manual-confirmation/pending", json=payload)

    assert first.status_code == 200
    assert second.status_code == 400
    assert len(PENDING_CONFIRMATION_QUEUE) == 1
