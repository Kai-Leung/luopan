import type { InteractionAction } from '../input_flow/h5Interaction';

export type VoiceAction = Extract<InteractionAction, '查' | '录入' | '问'>;

export type VoiceTranscriptionResponse = {
  status: 'transcribed';
  text: string;
};

export type VoiceTranscriptionSource = 'native_speech' | 'backend_asr' | 'unavailable';

export type VoiceTranscriptionResult = {
  source: VoiceTranscriptionSource;
  text: string;
};
