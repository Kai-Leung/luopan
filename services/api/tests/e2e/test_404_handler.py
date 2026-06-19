from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_backend_json_response():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"status": "ok", "service": "Compass"}
    assert b"<html" not in response.content.lower()


def test_api_unknown_route_returns_json_404():
    response = client.get("/api/v1/not-found-route")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_non_api_unknown_route_returns_valid_response():
    response = client.get("/not-found-route")

    assert response.status_code in {200, 404}
    assert response.content
