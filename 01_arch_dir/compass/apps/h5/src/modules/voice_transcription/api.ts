import { buildRequestUrl } from '../input_flow/api/client';
import type { VoiceTranscriptionResponse } from './types';

const VOICE_TRANSCRIPTION_PATH = '/api/v1/voice-transcription/transcribe';

export async function transcribeVoiceAudio(audioBlob: Blob): Promise<VoiceTranscriptionResponse> {
  const response = await fetch(buildRequestUrl(VOICE_TRANSCRIPTION_PATH), {
    method: 'POST',
    headers: {
      'Content-Type': audioBlob.type || 'audio/webm',
    },
    body: audioBlob,
  });

  if (!response.ok) {
    throw new Error(await readSafeErrorMessage(response));
  }

  return response.json();
}

async function readSafeErrorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json() as { detail?: unknown };
    if (typeof body.detail === 'string' && body.detail.trim()) {
      if (body.detail === 'voice transcription provider is not configured') {
        return '语音转写服务未配置。';
      }
      return body.detail.trim();
    }
  } catch {
    // ignore non-JSON response bodies
  }
  return `语音转写失败（HTTP ${response.status}）`;
}
