from datetime import datetime, timezone
from typing import Any, Callable, Optional

import pytest

from app.db.base import Base
from app.db.session import engine
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import RAW_INPUT_MEMORY_STORE, receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import CANDIDATE_MEMORY_STORE, create_candidate
from app.modules.l2_fact.service import FACT_RECORD_MEMORY_STORE
from app.modules.s2_governance_gate.confirmation.schemas import PendingConfirmationCreateRequest, ManualConfirmationReviewRequest
from app.modules.s2_governance_gate.confirmation.service import (
    MANUAL_CONFIRMATION_STORE,
    create_pending_confirmation,
    review_confirmation,
)
from app.modules.s2_governance_gate.schemas import S2GovernanceCheckRequest
from app.modules.s2_governance_gate.service import GOVERNANCE_MEMORY_STORE, check_candidate_governance


@pytest.fixture
def reset_workflow_state() -> None:
    RAW_INPUT_MEMORY_STORE.clear()
    CANDIDATE_MEMORY_STORE.clear()
    GOVERNANCE_MEMORY_STORE.clear()
    MANUAL_CONFIRMATION_STORE.clear()
    FACT_RECORD_MEMORY_STORE.clear()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def build_full_candidate_payload() -> Callable[[], dict[str, Any]]:
    def _build_full_candidate_payload() -> dict[str, Any]:
        return {
            "text": "今天张工在宝山项目现场质量问题需要确认",
            "primary_project_id": "project_宝山",
            "primary_subject_id": "subject_张工",
            "event_type": "quality_check",
            "object_asset_name": "防水层",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "source_type": "manual_input",
            "evidence_refs": ["现场照片001"],
        }

    return _build_full_candidate_payload


@pytest.fixture
def build_confirmed_candidate_chain(
    build_full_candidate_payload: Callable[[], dict[str, Any]],
) -> Callable[[str], tuple[Any, Any, Any, Any]]:
    def _build_confirmed_candidate_chain(review_action: str = "confirm") -> tuple[Any, Any, Any, Any]:
        candidate_payload = build_full_candidate_payload()
        text = candidate_payload["text"]
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
                candidate_payload=candidate_payload,
            )
        )
        if governance.governance_status in ("blocked", "needs_completion"):
            raise RuntimeError(
                f"S2 returned {governance.governance_status}, cannot proceed to MC."
            )
        pending = create_pending_confirmation(
            PendingConfirmationCreateRequest(
                raw_input_id=raw.raw_input_id,
                input_session_id=raw.input_session_id,
                candidate_id=candidate.candidate_id,
                governance_id=governance.governance_id,
                governance_status=governance.governance_status,
                fact_type="construction_record",
                fact_payload=candidate.candidate_payload,
                display_text="test pending",
            )
        )
        review = review_confirmation(
            ManualConfirmationReviewRequest(
                pending_id=pending.pending_id,
                governance_id=governance.governance_id,
                governance_status=governance.governance_status,
                review_action=review_action,
            )
        )
        return raw, candidate, governance, review

    return _build_confirmed_candidate_chain


@pytest.fixture
def build_fact_payload() -> Callable[[Any, Any, Any, Any, Optional[str]], dict[str, Any]]:
    def _build_fact_payload(
        raw_input_response: Any,
        candidate_response: Any,
        governance_response: Any,
        review_response: Any,
        review_status: Optional[str] = None,
    ) -> dict[str, Any]:
        candidate_fact_type = candidate_response.candidate_payload.get("fact_record_type")
        return {
            "raw_input_id": raw_input_response.raw_input_id,
            "candidate_id": candidate_response.candidate_id,
            "governance_id": governance_response.governance_id,
            "review_id": review_response.review_id,
            "review_status": review_status or review_response.review_status,
            "fact_type": candidate_fact_type,
            "fact_payload": {
                "text": "今天张工在宝山项目现场质量问题需要确认",
                "primary_project_id": "project_宝山",
                "primary_subject_id": "subject_张工",
            },
        }

    return _build_fact_payload
