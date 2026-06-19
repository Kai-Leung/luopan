import { transcribeVoiceAudio } from './api';
import { startNativeSpeechSession } from './nativeSpeech';
import { startVoiceRecording, stopVoiceRecording, type VoiceRecordingSession } from './recorder';
import type { VoiceAction, VoiceTranscriptionResult } from './types';

export type VoiceCaptureSession = {
  action: VoiceAction;
  nativeSession: ReturnType<typeof startNativeSpeechSession>;
  backendSession: VoiceRecordingSession | null;
};

export async function startVoiceCapture(action: VoiceAction): Promise<VoiceCaptureSession> {
  const backendSession = await startBackendFallbackRecording(action);
  const nativeSession = startNativeSpeechSession();
  if (!nativeSession && !backendSession) {
    throw new Error('当前环境不支持语音转写；需要 HTTPS、浏览器语音识别或后端 ASR 网关。');
  }
  return { action, nativeSession, backendSession };
}

export async function finishVoiceCapture(session: VoiceCaptureSession): Promise<VoiceTranscriptionResult> {
  const nativeText = await tryReadNativeSpeech(session.nativeSession);
  if (nativeText) {
    await discardBackendRecording(session.backendSession);
    return { source: 'native_speech', text: nativeText };
  }
  if (!session.backendSession) {
    throw new Error('内置语音不可用，且后端 ASR 录音兜底不可用。');
  }

  const audioBlob = await stopVoiceRecording(session.backendSession);
  const response = await transcribeVoiceAudio(audioBlob);
  const text = response.text.trim();
  if (!text) {
    throw new Error('后端 ASR 未返回转写内容。');
  }
  return { source: 'backend_asr', text };
}

async function startBackendFallbackRecording(action: VoiceAction): Promise<VoiceRecordingSession | null> {
  try {
    return await startVoiceRecording(action);
  } catch {
    return null;
  }
}

async function tryReadNativeSpeech(nativeSession: ReturnType<typeof startNativeSpeechSession>): Promise<string> {
  if (!nativeSession) return '';
  try {
    return await nativeSession.stop();
  } catch {
    return '';
  }
}

async function discardBackendRecording(backendSession: VoiceRecordingSession | null): Promise<void> {
  if (!backendSession) return;
  try {
    await stopVoiceRecording(backendSession);
  } catch {
    // Native speech succeeded; backend fallback recording is discarded.
  }
}
