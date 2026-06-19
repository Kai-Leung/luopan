import { useCallback, useRef, useState } from 'react';
import type { InteractionAction, InteractionMessage } from '../input_flow/h5Interaction';
import { finishVoiceCapture, startVoiceCapture } from './strategy';
import type { VoiceCaptureSession } from './strategy';
import type { VoiceAction, VoiceTranscriptionSource } from './types';

type AppendMessage = (message: Omit<InteractionMessage, 'id' | 'createdAt'>) => void;

type UseVoiceTranscriptionFlowOptions = {
  appendMessage: AppendMessage;
  showToast: (message: string) => void;
  submitText: (text: string, action: InteractionAction) => Promise<void>;
  queryExistingFacts: (keyword: string) => Promise<void>;
  openFactAnalysis: (keyword: string, voiceSourceLabel?: string) => void;
};

export function useVoiceTranscriptionFlow({
  appendMessage,
  showToast,
  submitText,
  queryExistingFacts,
  openFactAnalysis,
}: UseVoiceTranscriptionFlowOptions) {
  const [pressingAction, setPressingAction] = useState<InteractionAction | null>(null);
  const activePressActionRef = useRef<VoiceAction | null>(null);
  const voiceCaptureRef = useRef<VoiceCaptureSession | null>(null);

  const handleVoiceTranscript = useCallback(async (
    action: VoiceAction,
    text: string,
    source: VoiceTranscriptionSource,
  ) => {
    const transcript = text.trim();
    if (!transcript) {
      showToast('语音转写结果为空。');
      return;
    }
    const sourceLabel = formatVoiceSourceLabel(source);
    if (action === '录入') {
      appendMessage({ type: 'status', action: '录入', content: `已识别语音：${sourceLabel}` });
      await submitText(transcript, '录入');
      return;
    }
    if (action === '查') {
      appendMessage({
        type: 'status',
        action: '查',
        content: `已识别语音：${sourceLabel}\n查询内容：${transcript}`,
      });
      await queryExistingFacts(transcript);
      return;
    }
    openFactAnalysis(transcript, sourceLabel);
  }, [appendMessage, openFactAnalysis, queryExistingFacts, showToast, submitText]);

  const beginVoicePress = useCallback(async (action: InteractionAction) => {
    if (!isVoiceAction(action) || voiceCaptureRef.current) return;
    activePressActionRef.current = action;
    setPressingAction(action);
    try {
      voiceCaptureRef.current = await startVoiceCapture(action);
      showToast('正在听你说话。');
    } catch (error) {
      activePressActionRef.current = null;
      setPressingAction(null);
      showToast(getVoiceErrorMessage(error));
    }
  }, [showToast]);

  const finishVoicePress = useCallback(async (action: InteractionAction) => {
    if (activePressActionRef.current !== action) return;
    const session = voiceCaptureRef.current;
    voiceCaptureRef.current = null;
    activePressActionRef.current = null;
    setPressingAction(null);
    if (!session) return;

    try {
      showToast('正在整理语音内容。');
      const result = await finishVoiceCapture(session);
      await handleVoiceTranscript(session.action, result.text, result.source);
    } catch (error) {
      showToast(getVoiceErrorMessage(error));
    }
  }, [handleVoiceTranscript, showToast]);

  return { pressingAction, beginVoicePress, finishVoicePress };
}

function isVoiceAction(action: InteractionAction): action is VoiceAction {
  return action === '查' || action === '录入' || action === '问';
}

function getVoiceErrorMessage(error: unknown): string {
  if (error instanceof Error && error.message.trim()) return error.message.trim();
  return '语音转写失败。';
}

function formatVoiceSourceLabel(source: VoiceTranscriptionSource): string {
  if (source === 'native_speech') return '本机识别';
  if (source === 'backend_asr') return '服务识别';
  return '不可用';
}
