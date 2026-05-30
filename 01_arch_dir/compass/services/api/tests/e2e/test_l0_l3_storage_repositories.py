import os

import pytest

from app.db.base import Base
from app.db.repositories import (
    get_candidate,
    get_governance_result,
    get_manual_review,
    get_raw_input,
    load_json_field,
)
from app.db.repositories.candidate_repository import get_candidate as layered_get_candidate
from app.db.repositories.governance_repository import get_governance_result as layered_get_governance_result
from app.db.repositories.json_utils import load_json_field as layered_load_json_field
from app.db.repositories.raw_input_repository import get_raw_input as layered_get_raw_input
from app.db.repositories.storage_repository import ensure_minimal_storage_tables as layered_ensure_storage
from app.db.session import DATABASE_URL, DEVELOPMENT_DATABASE_URL, TEST_DATABASE_URL, DEVELOPMENT_DATABASE_PATH, SessionLocal, resolve_database_url
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.s2_governance_gate.confirmation.schemas import ManualConfirmationReviewRequest
from app.modules.s2_governance_gate.confirmation.service import review_confirmation
from app.modules.s2_governance_gate.schemas import S2GovernanceCheckRequest
from app.modules.s2_governance_gate.service import check_candidate_governance

pytestmark = pytest.mark.usefixtures("reset_workflow_state")


def test_pytest_default_database_url_uses_isolated_memory_database():
    if "COMPASS_DATABASE_URL" not in os.environ and "DATABASE_URL" not in os.environ:
        assert DATABASE_URL == TEST_DATABASE_URL


def test_development_database_url_uses_project_file_database():
    assert DEVELOPMENT_DATABASE_URL.startswith("sqlite:///")
    assert str(DEVELOPMENT_DATABASE_PATH).endswith("data/dev/compass_dev.sqlite3")


def test_development_database_url_defaults_to_file_database():
    assert resolve_database_url(app_env="development", explicit_database_url="") == DEVELOPMENT_DATABASE_URL


def test_test_database_url_defaults_to_memory():
    assert resolve_database_url(app_env="test", explicit_database_url="") == TEST_DATABASE_URL


def test_production_database_url_requires_explicit_value():
    with pytest.raises(RuntimeError, match="DATABASE_URL must be configured"):
        resolve_database_url(app_env="production", explicit_database_url="")


def test_repository_package_keeps_compatibility_exports():
    assert layered_get_candidate is get_candidate
    assert layered_get_governance_result is get_governance_result
    assert layered_get_raw_input is get_raw_input
    assert layered_load_json_field is load_json_field
    assert callable(layered_ensure_storage)


def test_l0_writes_and_reads_raw_input():
    response = receive_raw_input(
        RawInputCreate(text="原始输入", source_type="manual_input")
    )

    db = SessionLocal()
    try:
        row = get_raw_input(db, response.raw_input_id)
        assert row is not None
        assert row.status == "received_only"
        assert load_json_field(row.raw_payload)["text"] == "原始输入"
    finally:
        db.close()


def test_l1_writes_and_reads_candidate():
    raw = receive_raw_input(
        RawInputCreate(text="候选输入", source_type="manual_input")
    )
    response = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            raw_payload={"text": "候选输入"},
            source_type="manual_input",
        )
    )

    db = SessionLocal()
    try:
        row = get_candidate(db, response.candidate_id)
        assert row is not None
        assert row.candidate_status == "new_candidate"
        assert load_json_field(row.candidate_payload)["raw_payload"]["text"] == "候选输入"
    finally:
        db.close()


def test_s2_writes_and_reads_governance_result():
    response = check_candidate_governance(
        S2GovernanceCheckRequest(
            candidate_id="cand_001",
            candidate_status="new_candidate",
            candidate_payload={"text": "今天张工在宝山项目记录普通候选"},
        )
    )

    db = SessionLocal()
    try:
        row = get_governance_result(db, response.governance_id)
        assert row is not None
        assert row.governance_status == "auto_pass"
        assert load_json_field(row.missing_fields) == []
    finally:
        db.close()


def test_manual_review_writes_and_reads_review():
    response = review_confirmation(
        ManualConfirmationReviewRequest(
            governance_id="gov_001",
            governance_status="needs_confirmation",
            review_action="confirm",
        )
    )

    db = SessionLocal()
    try:
        row = get_manual_review(db, response.review_id)
        assert row is not None
        assert row.review_status == "confirmed_candidate"
        assert row.policy_decision == "manual_review_required"
    finally:
        db.close()


def test_confirmed_candidate_does_not_create_formal_fact_table():
    review_confirmation(
        ManualConfirmationReviewRequest(
            governance_id="gov_002",
            governance_status="needs_confirmation",
            review_action="confirm",
        )
    )

    assert "fact_records" not in Base.metadata.tables


def test_blocked_governance_status_cannot_review():
    try:
        review_confirmation(
            ManualConfirmationReviewRequest(
                governance_id="gov_003",
                governance_status="blocked",
                review_action="confirm",
            )
        )
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
    else:
        raise AssertionError("blocked governance status must not be reviewed")
