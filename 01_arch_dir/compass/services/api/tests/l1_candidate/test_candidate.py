from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.db.repositories import get_candidate, load_json_field
from app.db.session import SessionLocal
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.extractor import extract_candidate_fields
from app.modules.l1_candidate.router import router
from app.modules.l1_candidate.segmenter import extract_raw_text, split_candidate_texts
from app.modules.l1_candidate.service import CANDIDATE_MEMORY_STORE

pytestmark = pytest.mark.usefixtures("reset_workflow_state")

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def setup_function():
    CANDIDATE_MEMORY_STORE.clear()


def create_raw_input_id(text: str = "原始输入内容") -> str:
    return receive_raw_input(
        RawInputCreate(text=text, source_type="manual_input")
    ).raw_input_id


def test_segmenter_extracts_raw_text_and_splits_candidates():
    assert extract_raw_text({"text": " 今天张师傅做了防水 "}) == "今天张师傅做了防水"
    assert split_candidate_texts("今天张师傅做了厨房防水，王师傅买了20袋水泥，金额3000元") == [
        "今天张师傅做了厨房防水",
        "王师傅买了20袋水泥，金额3000元",
    ]
    assert split_candidate_texts("新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼") == [
        "新建项目叫宝山刘老师家，客户刘老师，地址宝山一号楼"
    ]
    assert split_candidate_texts("我要新建一个项目叫宝山刘老师家，客户刘老师，地址宝山一号楼") == [
        "我要新建一个项目叫宝山刘老师家，客户刘老师，地址宝山一号楼"
    ]


def test_extractor_keeps_existing_fact_type_classification():
    extracted = extract_candidate_fields("客户说明天付尾款5000")

    assert extracted["primary_subject_id"] == "客户"
    assert extracted["occurred_at"] == "明天"
    assert extracted["amount_text"] == "尾款5000"
    assert extracted["fact_record_type"] == "financial_record"


def test_create_candidate_from_raw_input():
    raw_input_id = create_raw_input_id()
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": "原始输入内容"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["raw_input_id"] == raw_input_id
    assert body["input_session_id"].startswith("session_")
    assert len(body["candidates"]) == 1
    assert body["message"] == "candidate created"
    payload = body["candidate_payload"]
    assert body["candidate_id"].startswith("cand_")
    assert body["candidate_status"] == "new_candidate"
    assert payload["fact_record_type"]
    assert payload["candidate_summary"]


def test_create_candidate_rejects_missing_raw_input_id():
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": "raw_missing",
            "raw_payload": {"text": "脱离 L0 的候选"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "raw_input_id not found"


def test_candidate_id_is_returned():
    raw_input_id = create_raw_input_id()
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": "原始输入内容"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    assert response.json()["candidate_id"].startswith("cand_")


def test_candidate_status_is_candidate_state():
    raw_input_id = create_raw_input_id()
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": "原始输入内容"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    assert response.json()["candidate_status"] == "new_candidate"


def test_response_does_not_generate_formal_fact_fields():
    raw_input_id = create_raw_input_id("只做候选包装")
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": "只做候选包装"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "fact_id" not in body
    assert "is_truth" not in body
    assert "l2_snapshot_id" not in body
    assert "governance_result" not in body


def test_candidate_memory_store_receives_record_without_s2_or_l2_fields():
    raw_input_id = create_raw_input_id("内存候选")
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": "内存候选"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    assert len(CANDIDATE_MEMORY_STORE) == 1
    record = CANDIDATE_MEMORY_STORE[0]
    assert record.candidate_status.value == "new_candidate"
    assert "governance_result" not in record.candidate_payload
    assert "truth_record" not in record.candidate_payload


def test_extracts_project_subject_time_and_issue_from_decoration_text():
    text = "今天张师傅在宝山项目做了卫生间防水"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    payload = response.json()["candidate_payload"]
    assert payload["primary_project_id"] == "今天张师傅在宝山项目"
    assert payload["primary_subject_id"] == "今天张师傅"
    assert payload["occurred_at"] == "今天"
    assert payload["issue_or_action"] == "防水"
    assert payload["fact_record_type"] == "construction_record"
    assert "宝山项目" in payload["candidate_summary"]


def test_extracts_subject_amount_and_material_action():
    text = "王师傅买了20袋水泥，金额3000元"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    payload = response.json()["candidate_payload"]
    assert payload["primary_subject_id"] == "王师傅"
    assert payload["amount_text"] == "金额3000元"
    # L1 抽取 issue_or_action 可能包含额外上下文，验证关键词匹配即可
    assert "水泥" in payload["issue_or_action"]
    assert payload["fact_record_type"] == "purchase_record"
    assert "primary_project_id" not in payload


def test_extracts_customer_time_payment_and_amount():
    text = "客户说明天付尾款5000"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    payload = response.json()["candidate_payload"]
    assert payload["primary_subject_id"] == "客户"
    assert payload["occurred_at"] == "明天"
    assert payload["amount_text"] == "尾款5000"
    assert payload["issue_or_action"] == "付款、尾款"
    assert payload["fact_record_type"] == "financial_record"


def test_single_input_can_split_multiple_candidates_in_same_session():
    text = "今天张师傅做了厨房防水，王师傅买了20袋水泥，客户说明天付尾款5000"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "input_session_id": "session_multi_001",
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["input_session_id"] == "session_multi_001"
    assert len(body["candidates"]) == 3
    assert {item["raw_input_id"] for item in body["candidates"]} == {raw_input_id}
    assert {item["input_session_id"] for item in body["candidates"]} == {"session_multi_001"}
    summaries = [item["candidate_payload"]["candidate_summary"] for item in body["candidates"]]
    assert any("防水" in summary for summary in summaries)
    assert any("水泥" in summary for summary in summaries)
    assert any("尾款" in summary for summary in summaries)
    fact_types = [item["candidate_payload"]["fact_record_type"] for item in body["candidates"]]
    assert fact_types == ["construction_record", "purchase_record", "financial_record"]
    assert len(CANDIDATE_MEMORY_STORE) == 3


def test_l1_classifies_communication_and_issue_risk_separately():
    communication_text = "今天客户沟通售后服务安排"
    issue_text = "今天客户投诉漏水并提示质量风险"
    communication = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": create_raw_input_id(communication_text),
            "raw_payload": {"text": communication_text},
            "source_type": "manual_input",
        },
    ).json()
    issue = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": create_raw_input_id(issue_text),
            "raw_payload": {"text": issue_text},
            "source_type": "manual_input",
        },
    ).json()

    assert communication["candidate_payload"]["fact_record_type"] == "communication_service_record"
    assert issue["candidate_payload"]["fact_record_type"] == "issue_risk_record"


def test_l1_uses_other_fact_record_only_for_unclassified_text():
    text = "今天记录一个暂时无法归类的普通事项"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    assert response.json()["candidate_payload"]["fact_record_type"] == "other_fact_record"


def test_l1_creates_project_asset_candidate_for_create_project_intent():
    text = "我要新建一个项目叫宝山刘老师家，客户刘老师，地址宝山一号楼"
    raw_input_id = create_raw_input_id(text)
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": raw_input_id,
            "raw_payload": {"text": text},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    body = response.json()
    payload = body["candidate_payload"]
    assert body["raw_input_id"] == raw_input_id
    assert payload["candidate_type"] == "project_asset_candidate"
    assert payload["raw_text"] == text
    assert payload["project_name"] == "宝山刘老师家"
    assert payload["customer_name"] == "刘老师"
    assert payload["project_address"] == "宝山一号楼"
    assert payload["required_permission"] == "project_asset:create"
    assert "primary_project_id" not in payload
    assert "truth_record" not in payload


def test_l1_extracts_project_name_from_minimal_project_create_text():
    text = "我要新建一个项目叫宝山刘老师家"
    payload = extract_candidate_fields(text)

    assert payload["candidate_type"] == "project_asset_candidate"
    assert payload["project_name"] == "宝山刘老师家"
    assert payload["raw_text"] == text


def test_supplement_merges_into_existing_candidate_session():
    original_raw_input_id = create_raw_input_id("今天张师傅做了防水")
    created = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": original_raw_input_id,
            "input_session_id": "session_supplement_001",
            "raw_payload": {"text": "今天张师傅做了防水"},
            "source_type": "manual_input",
        },
    ).json()

    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": create_raw_input_id("补充项目是宝山项目"),
            "input_session_id": "session_supplement_001",
            "supplement_candidate_id": created["candidate_id"],
            "raw_payload": {"text": "补充项目是宝山项目"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == created["candidate_id"]
    assert body["input_session_id"] == "session_supplement_001"
    assert "补充项目是宝山项目" in body["candidate_payload"]["text"]
    assert len(CANDIDATE_MEMORY_STORE) == 1
    db = SessionLocal()
    try:
        row = get_candidate(db, created["candidate_id"])
        assert row is not None
        persisted_payload = load_json_field(row.candidate_payload)
        assert "补充项目是宝山项目" in persisted_payload["text"]
        assert persisted_payload["supplemental_texts"] == ["补充项目是宝山项目"]
    finally:
        db.close()


def test_missing_supplement_candidate_id_is_rejected():
    response = client.post(
        "/api/v1/l1/candidates",
        json={
            "raw_input_id": create_raw_input_id("补充内容"),
            "input_session_id": "session_supplement_missing",
            "supplement_candidate_id": "cand_missing",
            "raw_payload": {"text": "补充内容"},
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "supplement_candidate_id not found"
