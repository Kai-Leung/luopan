import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.l2_fact.schemas import L2FactCreateRequest
from app.modules.l2_fact.service import create_l2_fact
from app.modules.s2_governance_gate.confirmation.schemas import ManualConfirmationReviewRequest
from app.modules.s2_governance_gate.confirmation.service import review_confirmation
from app.modules.s2_governance_gate.policy import evaluate_governance_policy
from app.modules.s2_governance_gate import policy
from app.modules.s2_governance_gate.router import router
from app.modules.s2_governance_gate.schemas import S2GovernanceCheckRequest
from app.modules.s2_governance_gate.service import GOVERNANCE_MEMORY_STORE, check_candidate_governance

pytestmark = pytest.mark.usefixtures("reset_workflow_state")

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def test_low_risk_candidate_auto_pass():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_001",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "auto_pass"
    assert body["risk_level"] == "none"
    assert body["question_prompts"] == []
    assert body["validation_hints"] == []
    assert body["risk_hints"] == []
    assert body["required_permission"] is None
    assert body["next_action"] == "need_confirm"


def test_s2_response_contains_stable_governance_fields():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_stable_output",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    assert set(response.json()) == {
        "governance_id",
        "candidate_id",
        "input_session_id",
        "governance_status",
        "missing_fields",
        "risk_level",
        "question_prompts",
        "validation_hints",
        "risk_hints",
        "required_permission",
        "next_action",
        "message",
    }


def test_s2_policy_consumes_standard_governance_risk_keywords():
    assert not hasattr(policy, "HIGH_RISK_KEYWORDS")
    assert not hasattr(policy, "BLOCKING_RISK_KEYWORDS")


def test_policy_preserves_low_risk_decision_mapping():
    result = evaluate_governance_policy(
        candidate_status="new_candidate",
        candidate_payload={"text": "今天张工在宝山项目完成普通记录"},
    )

    assert result.governance_status == "auto_pass"
    assert result.risk_level == "none"
    assert result.missing_fields == []
    assert result.question_prompts == []
    assert result.validation_hints == []
    assert result.risk_hints == []
    assert result.required_permission is None
    assert result.next_action == "need_confirm"


def test_complete_low_risk_input_can_reach_confirmation_and_l2():
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

    assert governance.governance_status == "auto_pass"
    assert governance.next_action == "need_confirm"
    assert governance.missing_fields == []

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

    assert review.review_status == "confirmed_candidate"
    assert fact.fact_status == "active_fact"
    assert fact.fact_payload["text"] == text


def test_missing_text_needs_completion():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_002",
            "candidate_status": "new_candidate",
            "candidate_payload": {"raw_payload": {"file_ref": "local-file"}},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["fact_summary"]
    assert body["risk_level"] == "none"
    assert body["question_prompts"] == ["请补充事项内容"]
    assert body["validation_hints"] == ["字段缺口：事项内容"]
    assert body["next_action"] == "ask_more"


def test_high_risk_keyword_needs_confirmation():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_003",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天张工在宝山项目涉及签证和金额确认",
                "evidence_refs": ["chat_001"],
                "confirmation_scope": "签证金额口径",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_confirmation"
    assert body["risk_level"] == "high"
    assert "签证" in body["risk_hints"]
    assert "金额" in body["risk_hints"]
    assert body["next_action"] == "need_confirm"


def test_invalid_candidate_status_blocked():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_004",
            "candidate_status": "fake_status",
            "candidate_payload": {"text": "普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "blocked"
    assert body["risk_level"] == "blocking"
    assert body["risk_hints"] == ["invalid_candidate_status"]
    assert body["validation_hints"] == ["candidate_status 不属于标准状态口径"]
    assert body["next_action"] == "blocked"


def test_blocking_content_maps_to_blocked_next_action():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_blocking_content",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目提交阻断事项"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "blocked"
    assert body["risk_level"] == "blocking"
    assert body["risk_hints"] == ["阻断"]
    assert body["next_action"] == "blocked"


def test_response_does_not_generate_formal_fact():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_005",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "fact_id" not in body
    assert "truth_record" not in body
    assert "l2_snapshot_id" not in body
    assert "confirmed_by" not in body


def test_memory_store_does_not_call_l2():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_006",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    assert len(GOVERNANCE_MEMORY_STORE) == 1
    record = GOVERNANCE_MEMORY_STORE[0]
    assert record.governance_status == "auto_pass"
    assert record.risk_level == "none"
    assert record.required_permission is None
    assert "truth_record" not in record.checked_payload


def test_content_missing_project_time_subject_generates_questions():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_007",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "现场完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == [
        "primary_project_id",
        "primary_subject_id",
        "occurred_at",
    ]
    assert body["risk_level"] == "none"
    assert body["question_prompts"] == [
        "请补充项目",
        "请补充人员或主体",
        "请补充时间",
    ]
    assert body["validation_hints"] == [
        "字段缺口：项目",
        "字段缺口：人员/主体",
        "字段缺口：时间",
    ]
    assert body["next_action"] == "ask_more"


def test_project_asset_candidate_missing_fields_needs_completion_without_project_assignment():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_project_asset_missing",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "candidate_type": "project_asset_candidate",
                "raw_text": "我要新建一个项目",
                "text": "我要新建一个项目",
                "required_permission": "project_asset:create",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert "primary_project_id" not in body["missing_fields"]
    assert "project_name" in body["missing_fields"]
    assert "customer_name" in body["missing_fields"]
    assert "project_address" in body["missing_fields"]
    assert "请补充项目" not in body["question_prompts"]
    assert "请补充项目名称" in body["question_prompts"]
    assert body["required_permission"] == "project_asset:create"
    assert body["next_action"] == "ask_more"


def test_complete_project_asset_candidate_needs_confirmation():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_project_asset_complete",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "candidate_type": "project_asset_candidate",
                "raw_text": "新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼",
                "text": "新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼",
                "project_name": "宝山刘老师家",
                "customer_name": "刘老师",
                "project_address": "宝山一号楼",
                "required_permission": "project_asset:create",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_confirmation"
    assert body["missing_fields"] == []
    assert body["question_prompts"] == []
    assert body["required_permission"] == "project_asset:create"
    assert body["next_action"] == "need_confirm"


def test_optional_field_missing_does_not_block():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_optional_missing",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "auto_pass"
    assert body["missing_fields"] == []
    assert body["question_prompts"] == []
    assert body["next_action"] == "need_confirm"


def test_conditional_keyword_missing_field_generates_question():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_conditional_keyword",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天张师傅做了防水",
                "fact_record_type": "construction_record",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["primary_project_id", "object_asset_name"]
    assert body["question_prompts"] == [
        "请补充项目",
        "请补充位置或对象",
    ]
    assert body["next_action"] == "ask_more"


def test_high_risk_conditional_required_fields_are_checked():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_high_risk_conditional",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天客户在宝山项目说明天付尾款5000",
                "evidence_refs": ["chat_001"],
                "confirmation_scope": "尾款支付口径",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_confirmation"
    assert body["risk_level"] == "high"
    assert body["missing_fields"] == []
    assert body["next_action"] == "need_confirm"


def test_high_risk_conditional_missing_fields_ask_more():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_high_risk_missing",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天客户在宝山项目说明天付尾款5000"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["risk_level"] == "high"
    assert body["missing_fields"] == ["evidence_refs", "confirmation_scope"]
    assert body["question_prompts"] == [
        "请补充证据",
        "请补充确认范围",
    ]
    assert body["next_action"] == "ask_more"


def test_fact_record_type_conditional_required_fields_are_checked():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_fact_type_conditional",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天王师傅在宝山项目买了20袋水泥",
                "fact_record_type": "material_flow_record",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["related_subject_ids"]
    assert body["question_prompts"] == [
        "请补充供应商或相关主体",
    ]
    assert body["next_action"] == "ask_more"


def test_s2_uses_candidate_fact_record_type_for_field_rules():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_purchase_type",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天王师傅买了20袋水泥",
                "fact_record_type": "purchase_record",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["primary_project_id", "related_subject_ids"]
    assert body["question_prompts"] == [
        "请补充项目",
        "请补充供应商或相关主体",
    ]
    assert body["next_action"] == "ask_more"


def test_material_text_without_project_asks_project_and_supplier():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_material_without_project",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天王师傅买了20袋水泥",
                "fact_record_type": "purchase_record",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["primary_project_id", "related_subject_ids"]
    assert body["question_prompts"] == [
        "请补充项目",
        "请补充供应商或相关主体",
    ]
    assert body["next_action"] == "ask_more"


def test_source_type_conditional_required_fields_are_checked():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_source_type_conditional",
            "candidate_status": "new_candidate",
            "candidate_payload": {
                "text": "今天张工在宝山项目提交资料",
                "source_type": "uploaded_document",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["governance_status"] == "needs_completion"
    assert body["missing_fields"] == ["source_record_id"]
    assert body["question_prompts"] == ["请补充来源记录"]
    assert body["next_action"] == "ask_more"


def test_s2_returns_input_session_for_each_candidate():
    response = client.post(
        "/api/v1/s2/governance/check",
        json={
            "candidate_id": "cand_session_001",
            "input_session_id": "session_s2_001",
            "candidate_status": "new_candidate",
            "candidate_payload": {"text": "今天张工在宝山项目完成普通记录"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == "cand_session_001"
    assert body["input_session_id"] == "session_s2_001"
    assert body["next_action"] == "need_confirm"


def test_multi_candidate_input_runs_s2_per_candidate():
    text = "今天张师傅做了厨房防水，王师傅买了20袋水泥，客户说明天付尾款5000"
    raw = receive_raw_input(RawInputCreate(text=text, source_type="manual_input"))
    candidate_group = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            input_session_id="session_multi_s2",
            raw_payload={"text": text},
            source_type="manual_input",
        )
    )

    results = [
        check_candidate_governance(
            S2GovernanceCheckRequest(
                candidate_id=item.candidate_id,
                input_session_id=item.input_session_id,
                candidate_status=item.candidate_status,
                candidate_payload=item.candidate_payload,
            )
        )
        for item in candidate_group.candidates
    ]

    assert len(results) == 3
    assert {result.input_session_id for result in results} == {"session_multi_s2"}
    assert all(result.next_action in {"ask_more", "need_confirm", "blocked"} for result in results)
    assert any("请补充项目" in result.question_prompts for result in results)
    assert any("请补充供应商或相关主体" in result.question_prompts for result in results)
