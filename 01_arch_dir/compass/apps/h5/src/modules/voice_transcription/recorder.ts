import type { VoiceAction } from './types';

export type VoiceRecordingSession = {
  action: VoiceAction;
  recorder: MediaRecorder;
  stream: MediaStream;
  chunks: Blob[];
  mimeType: string;
};

export async function startVoiceRecording(action: VoiceAction): Promise<VoiceRecordingSession> {
  if (!isSecureVoiceContext()) {
    throw new Error('当前环境不支持语音录制；启用需要 HTTPS 和真实语音识别/转写服务。');
  }
  if (!navigator.mediaDevices || typeof navigator.mediaDevices.getUserMedia !== 'function') {
    throw new Error('当前浏览器不支持麦克风录音。');
  }
  if (typeof MediaRecorder === 'undefined') {
    throw new Error('当前浏览器不支持 MediaRecorder 录音。');
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mimeType = getSupportedAudioMimeType();
  let recorder: MediaRecorder;
  try {
    recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
  } catch (error) {
    stopStream(stream);
    throw error;
  }
  const chunks: Blob[] = [];
  recorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      chunks.push(event.data);
    }
  };
  recorder.start();
  return { action, recorder, stream, chunks, mimeType: mimeType || 'audio/webm' };
}

export function stopVoiceRecording(session: VoiceRecordingSession): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const { recorder, stream, chunks, mimeType } = session;
    recorder.onerror = () => {
      stopStream(stream);
      reject(new Error('语音录制失败。'));
    };
    recorder.onstop = () => {
      stopStream(stream);
      resolve(new Blob(chunks, { type: mimeType }));
    };
    if (recorder.state === 'inactive') {
      stopStream(stream);
      resolve(new Blob(chunks, { type: mimeType }));
      return;
    }
    recorder.stop();
  });
}

function isSecureVoiceContext(): boolean {
  return typeof window !== 'undefined' && window.isSecureContext === true;
}

function getSupportedAudioMimeType(): string {
  const candidates = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4'];
  return candidates.find((item) => MediaRecorder.isTypeSupported(item)) || '';
}

function stopStream(stream: MediaStream): void {
  stream.getTracks().forEach((track) => track.stop());
}
