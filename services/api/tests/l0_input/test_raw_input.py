from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.l0_input.router import router
from app.modules.l0_input.service import RAW_INPUT_MEMORY_STORE

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def setup_function():
    RAW_INPUT_MEMORY_STORE.clear()


def test_text_raw_input_received():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={"text": "今天现场记录一条原始输入", "source_type": "manual_input"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "received_only"
    assert body["message"] == "raw input received"


def test_valid_source_type_is_accepted():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={"image_ref": "local-image-ref", "source_type": "image_input"},
    )

    assert response.status_code == 200


def test_invalid_source_type_is_rejected():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={"text": "原始输入", "source_type": "invalid_source_type"},
    )

    assert response.status_code == 422


def test_raw_input_id_is_returned():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={"file_ref": "local-file-ref", "source_type": "uploaded_document"},
    )

    assert response.status_code == 200
    assert response.json()["raw_input_id"].startswith("raw_")
    assert response.json()["input_session_id"].startswith("session_")


def test_existing_input_session_id_is_preserved():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={
            "text": "补充输入",
            "input_session_id": "session_existing",
            "source_type": "manual_input",
        },
    )

    assert response.status_code == 200
    assert response.json()["input_session_id"] == "session_existing"


def test_memory_store_receives_record():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={"text": "只接收原始输入", "source_type": "manual_input"},
    )

    assert response.status_code == 200
    assert len(RAW_INPUT_MEMORY_STORE) == 1
    record = RAW_INPUT_MEMORY_STORE[0]
    assert record.status == "received_only"
    assert record.source_type.value == "manual_input"
    assert record.raw_payload["text"] == "只接收原始输入"


def test_asr_provider_details_are_not_saved_in_l0_payload():
    response = client.post(
        "/api/v1/l0/raw-input",
        json={
            "text": "语音录入后的原始文字",
            "source_type": "manual_input",
            "native_speech": "enabled",
            "backend_asr": "fallback",
            "xfyun": "configured",
            "provider": "xfyun",
            "asr_provider": "xfyun",
            "transcription_source": "backend_asr",
            "speech_provider": "xfyun",
            "voice_model": "asr",
            "api_provider": "xfyun",
        },
    )

    assert response.status_code == 200
    record = RAW_INPUT_MEMORY_STORE[0]
    assert record.raw_payload["text"] == "语音录入后的原始文字"
    assert record.raw_payload["image_ref"] is None
    assert record.raw_payload["file_ref"] is None
    assert record.raw_payload["input_session_id"]
    assert "idempotency_key" in record.raw_payload
    assert record.raw_payload["_runtime_context"]
    assert not {
        "native_speech",
        "backend_asr",
        "xfyun",
        "provider",
        "asr_provider",
        "transcription_source",
        "speech_provider",
        "voice_model",
        "api_provider",
    }.intersection(record.raw_payload)
