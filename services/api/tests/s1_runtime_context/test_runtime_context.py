from fastapi.testclient import TestClient

from app.main import app
from app.modules.s1_runtime_context.service import (
    DEFAULT_ORGANIZATION_ID,
    DEFAULT_ROLE_ID,
    DEFAULT_USER_ID,
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
