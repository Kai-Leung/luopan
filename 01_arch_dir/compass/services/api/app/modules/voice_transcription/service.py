"""语音转写网关服务。

只接收音频并调用后端配置的转写 provider；不写数据库，不生成正式事实。
"""

from fastapi import HTTPException

from app.core.config import settings
from app.modules.voice_transcription.providers import (
    ProviderConfig,
    VoiceTranscriptionProviderError,
    create_voice_transcription_provider,
)

SUPPORTED_AUDIO_TYPES = {
    "audio/webm",
    "audio/mp4",
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
}


def transcribe_audio(*, audio_bytes: bytes, content_type: str) -> str:
    _validate_audio_payload(audio_bytes=audio_bytes, content_type=content_type)
    try:
        provider = create_voice_transcription_provider(
            ProviderConfig(
                name=settings.VOICE_TRANSCRIPTION_PROVIDER,
                api_key=settings.VOICE_TRANSCRIPTION_API_KEY,
                xfyun_app_id=settings.XFYUN_APP_ID,
                xfyun_api_key=settings.XFYUN_API_KEY,
                xfyun_api_secret=settings.XFYUN_API_SECRET,
                xfyun_asr_endpoint=settings.XFYUN_ASR_ENDPOINT,
                xfyun_asr_audio_format=settings.XFYUN_ASR_AUDIO_FORMAT,
            )
        )
        text = provider.transcribe(audio_bytes=audio_bytes, content_type=content_type)
    except VoiceTranscriptionProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    if not text.strip():
        raise HTTPException(status_code=502, detail="voice transcription provider returned empty text")
    return text.strip()


def _validate_audio_payload(*, audio_bytes: bytes, content_type: str) -> None:
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="audio payload is required")
    if len(audio_bytes) > settings.VOICE_TRANSCRIPTION_MAX_BYTES:
        raise HTTPException(status_code=413, detail="audio payload is too large")

    normalized_content_type = content_type.split(";")[0].strip().lower()
    if normalized_content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="unsupported audio content type")
