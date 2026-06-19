from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.upload import service as upload_service
from app.modules.upload.api import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def test_upload_jpg_saves_original_file(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("site.jpg", b"jpg-bytes", "image/jpeg")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["saved"] is True
    assert body["filename"] == "site.jpg"
    assert body["content_type"] == "image/jpeg"
    assert body["file_size"] == len(b"jpg-bytes")
    assert body["storage_path"].startswith("storage/dev/uploads/")
    saved_path = upload_service.UPLOAD_ROOT / body["storage_path"].split("/")[-1]
    assert saved_path.read_bytes() == b"jpg-bytes"


def test_upload_pdf_saves_original_file(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("contract.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["saved"] is True
    assert body["filename"] == "contract.pdf"
    assert body["storage_path"].endswith(".pdf")
    saved_path = upload_service.UPLOAD_ROOT / body["storage_path"].split("/")[-1]
    assert saved_path.exists()


def test_upload_heic_saves_original_file(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("site.heic", b"heic-bytes", "image/heic")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["saved"] is True
    assert body["filename"] == "site.heic"
    assert body["content_type"] == "image/heic"
    assert body["storage_path"].endswith(".heic")


def test_upload_accepts_mobile_jpeg_content_type_alias(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("site.jpg", b"jpg-bytes", "image/jpg")},
    )

    assert response.status_code == 200
    assert response.json()["saved"] is True


def test_upload_rejects_file_larger_than_10mb(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("large.jpg", b"x" * (10 * 1024 * 1024 + 1), "image/jpeg")},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "文件大小不能超过 10MB。"
    assert not upload_service.UPLOAD_ROOT.exists()


def test_upload_rejects_unsupported_file_type(tmp_path, monkeypatch):
    monkeypatch.setattr(upload_service, "UPLOAD_ROOT", tmp_path / "uploads")

    response = client.post(
        "/api/v1/upload/files",
        files={"file": ("notes.txt", b"text", "text/plain")},
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "仅支持 jpg、jpeg、png、heic、heif、pdf 文件。"
    assert not upload_service.UPLOAD_ROOT.exists()
