from contextvars import ContextVar
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.db.repositories import create_fact_record
from app.db.session import SessionLocal
from app.main import app
from app.modules.s1_runtime_context import service as runtime_service
from app.modules.s1_runtime_context.service import (
    DEFAULT_ORGANIZATION_ID,
    DEFAULT_ROLE_ID,
    DEFAULT_USER_ID,
    get_current_runtime_context,
    require_runtime_context,
)


client = TestClient(app)
VALID_HEADERS = {
    "X-Compass-User-Id": DEFAULT_USER_ID,
    "X-Compass-Organization-Id": DEFAULT_ORGANIZATION_ID,
    "X-Compass-Role": DEFAULT_ROLE_ID,
}


def test_current_context_returns_backend_owned_permissions():
    response = client.get("/api/v1/s1/runtime-context/current", headers=VALID_HEADERS)

    assert response.status_code == 200
    body = response.json()
    assert body["organization_id"] == DEFAULT_ORGANIZATION_ID
    assert body["role_ids"] == [DEFAULT_ROLE_ID]
    assert "l2:create" in body["allowed_actions"]
    assert body["context_source"] == "controlled_claim"


def test_partial_context_headers_are_rejected():
    response = client.get(
        "/api/v1/s1/runtime-context/current",
        headers={"X-Compass-User-Id": DEFAULT_USER_ID},
    )

    assert response.status_code == 400


def test_unknown_organization_is_rejected():
    response = client.get(
        "/api/v1/s1/runtime-context/current",
        headers={**VALID_HEADERS, "X-Compass-Organization-Id": "org_other"},
    )

    assert response.status_code == 403


def test_business_api_rejects_unknown_context():
    response = client.post(
        "/api/v1/l0/raw-input",
        headers={**VALID_HEADERS, "X-Compass-Organization-Id": "org_other"},
        json={"text": "测试输入", "source_type": "manual_input"},
    )

    assert response.status_code == 403


class TrackingContextVar:
    def __init__(self):
        self.context = ContextVar("test_runtime_context", default=None)
        self.set_count = 0
        self.reset_count = 0

    def set(self, value):
        self.set_count += 1
        return self.context.set(value)

    def get(self):
        return self.context.get()

    def reset(self, token):
        self.context.reset(token)
        self.reset_count += 1


def _build_context_probe_app() -> FastAPI:
    probe_app = FastAPI()

    @probe_app.get("/sync", dependencies=[Depends(require_runtime_context)])
    def sync_endpoint():
        return {
            "selected_project_id": get_current_runtime_context().selected_project_id,
        }

    @probe_app.get("/async-error", dependencies=[Depends(require_runtime_context)])
    async def async_error_endpoint():
        assert get_current_runtime_context().selected_project_id == "project_error"
        raise RuntimeError("probe endpoint failure")

    return probe_app


def test_sync_endpoint_cleans_runtime_context_after_normal_completion(monkeypatch):
    tracker = TrackingContextVar()
    monkeypatch.setattr(runtime_service, "_CURRENT_RUNTIME_CONTEXT", tracker)
    probe_client = TestClient(_build_context_probe_app())

    response = probe_client.get(
        "/sync",
        headers={**VALID_HEADERS, "X-Compass-Project-Id": "project_sync"},
    )

    assert response.status_code == 200
    assert response.json()["selected_project_id"] == "project_sync"
    assert tracker.set_count == 1
    assert tracker.reset_count == 1
    assert tracker.get() is None


def test_async_endpoint_exception_still_cleans_runtime_context(monkeypatch):
    tracker = TrackingContextVar()
    monkeypatch.setattr(runtime_service, "_CURRENT_RUNTIME_CONTEXT", tracker)
    probe_client = TestClient(
        _build_context_probe_app(),
        raise_server_exceptions=False,
    )

    response = probe_client.get(
        "/async-error",
        headers={**VALID_HEADERS, "X-Compass-Project-Id": "project_error"},
    )

    assert response.status_code == 500
    assert tracker.set_count == 1
    assert tracker.reset_count == 1
    assert tracker.get() is None


def test_dependency_validation_failure_does_not_leave_runtime_context(monkeypatch):
    tracker = TrackingContextVar()
    monkeypatch.setattr(runtime_service, "_CURRENT_RUNTIME_CONTEXT", tracker)
    probe_client = TestClient(_build_context_probe_app())

    response = probe_client.get(
        "/sync",
        headers={"X-Compass-User-Id": DEFAULT_USER_ID},
    )

    assert response.status_code == 400
    assert tracker.set_count == 0
    assert tracker.reset_count == 0
    assert tracker.get() is None


def test_consecutive_requests_do_not_inherit_selected_project():
    probe_client = TestClient(_build_context_probe_app())

    first = probe_client.get(
        "/sync",
        headers={**VALID_HEADERS, "X-Compass-Project-Id": "project_a"},
    )
    second = probe_client.get("/sync", headers=VALID_HEADERS)

    assert first.json()["selected_project_id"] == "project_a"
    assert second.json()["selected_project_id"] is None


def test_cross_project_fact_read_is_blocked_but_organization_scope_is_allowed(
    reset_workflow_state,
):
    db = SessionLocal()
    try:
        create_fact_record(
            db,
            fact_id="fact_project_a",
            raw_input_id="raw_project_a",
            candidate_id="cand_project_a",
            governance_id="gov_project_a",
            review_id="review_project_a",
            fact_type="construction_record",
            fact_payload={
                "text": "项目 A 事实",
                "_runtime_context": {
                    "organization_id": DEFAULT_ORGANIZATION_ID,
                    "selected_project_id": "project_a",
                },
            },
            fact_status="active_fact",
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()

    blocked = client.get(
        "/api/v1/l3/facts/fact_project_a",
        headers={**VALID_HEADERS, "X-Compass-Project-Id": "project_b"},
    )
    organization_scope = client.get(
        "/api/v1/l3/facts/fact_project_a",
        headers=VALID_HEADERS,
    )

    assert blocked.status_code == 403
    assert blocked.json()["detail"] == "cross-project access is blocked"
    assert organization_scope.status_code == 200
