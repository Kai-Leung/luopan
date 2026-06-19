from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.voice_transcription.router import router
from app.modules.voice_transcription.providers import (
    ProviderConfig,
    VoiceTranscriptionProviderError,
    create_voice_transcription_provider,
)

app = FastAPI()
app.include_router(router, prefix="/api/v1")
client = TestClient(app)


def test_voice_transcription_without_provider_is_blocked():
    response = client.post(
        "/api/v1/voice-transcription/transcribe",
        content=b"voice-bytes",
        headers={"content-type": "audio/webm"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "voice transcription provider is not configured"
    assert "voice-bytes" not in response.text
    assert "api_key" not in response.text.lower()
    assert "token" not in response.text.lower()


def test_provider_factory_rejects_unknown_provider_without_leaking_key():
    try:
        create_voice_transcription_provider(
            ProviderConfig(name="unknown_provider", api_key="secret-key-value")
        )
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("unknown provider must be rejected")

    assert message == "voice transcription provider is not supported"
    assert "secret-key-value" not in message


def test_provider_factory_rejects_missing_key():
    try:
        create_voice_transcription_provider(
            ProviderConfig(name="adapter_placeholder", api_key="")
        )
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("missing provider key must be rejected")

    assert message == "voice transcription provider key is not configured"


def test_placeholder_provider_does_not_return_fake_transcription():
    provider = create_voice_transcription_provider(
        ProviderConfig(name="adapter_placeholder", api_key="secret-key-value")
    )

    try:
        provider.transcribe(audio_bytes=b"voice-bytes", content_type="audio/webm")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("placeholder provider must not return fake text")

    assert message == "voice transcription provider is not implemented"
    assert "voice-bytes" not in message
    assert "secret-key-value" not in message


def test_xfyun_provider_rejects_missing_app_id():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_api_key="api-key",
                xfyun_api_secret="api-secret",
                xfyun_asr_endpoint="https://example.invalid/asr",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/wav")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("missing xfyun app id must be rejected")

    assert message == "xfyun app id is not configured"
    assert "api-key" not in message
    assert "api-secret" not in message


def test_xfyun_provider_rejects_missing_api_key():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_app_id="app-id",
                xfyun_api_secret="api-secret",
                xfyun_asr_endpoint="https://example.invalid/asr",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/wav")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("missing xfyun api key must be rejected")

    assert message == "xfyun api key is not configured"
    assert "app-id" not in message
    assert "api-secret" not in message


def test_xfyun_provider_rejects_missing_api_secret():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_app_id="app-id",
                xfyun_api_key="api-key",
                xfyun_asr_endpoint="https://example.invalid/asr",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/wav")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("missing xfyun api secret must be rejected")

    assert message == "xfyun api secret is not configured"
    assert "app-id" not in message
    assert "api-key" not in message


def test_xfyun_provider_rejects_missing_endpoint():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_app_id="app-id",
                xfyun_api_key="api-key",
                xfyun_api_secret="api-secret",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/wav")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("missing xfyun endpoint must be rejected")

    assert message == "xfyun endpoint is not configured"
    assert "api-key" not in message
    assert "api-secret" not in message


def test_xfyun_provider_rejects_unsupported_audio_format():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_app_id="app-id",
                xfyun_api_key="api-key",
                xfyun_api_secret="api-secret",
                xfyun_asr_endpoint="https://example.invalid/asr",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/webm")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("unsupported xfyun audio format must be rejected")

    assert message == "xfyun audio format is not supported"
    assert "voice-bytes" not in message
    assert "api-key" not in message
    assert "api-secret" not in message


def test_xfyun_provider_blocks_when_protocol_is_not_configured():
    try:
        create_voice_transcription_provider(
            ProviderConfig(
                name="xfyun",
                xfyun_app_id="app-id",
                xfyun_api_key="api-key",
                xfyun_api_secret="api-secret",
                xfyun_asr_endpoint="https://example.invalid/asr",
                xfyun_asr_audio_format="audio/wav",
            )
        ).transcribe(audio_bytes=b"voice-bytes", content_type="audio/wav")
    except VoiceTranscriptionProviderError as exc:
        message = str(exc)
    else:
        raise AssertionError("xfyun protocol must not return fake text")

    assert message == "xfyun provider protocol is not configured"
    assert "voice-bytes" not in message
    assert "api-key" not in message
    assert "api-secret" not in message


def test_voice_transcription_rejects_non_audio_payload():
    response = client.post(
        "/api/v1/voice-transcription/transcribe",
        content=b"not-audio",
        headers={"content-type": "text/plain"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "unsupported audio content type"
