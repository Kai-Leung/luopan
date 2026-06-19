"""语音转写网关路由。"""

from fastapi import APIRouter, Request

from app.modules.voice_transcription.schemas import VoiceTranscriptionResponse
from app.modules.voice_transcription.service import transcribe_audio

router = APIRouter(prefix="/voice-transcription", tags=["voice-transcription"])


@router.post("/transcribe", response_model=VoiceTranscriptionResponse)
async def transcribe_voice(request: Request) -> VoiceTranscriptionResponse:
    audio_bytes = await request.body()
    text = transcribe_audio(
        audio_bytes=audio_bytes,
        content_type=request.headers.get("content-type", ""),
    )
    return VoiceTranscriptionResponse(status="transcribed", text=text)
