type NativeSpeechRecognitionConstructor = new () => NativeSpeechRecognition;

type NativeSpeechRecognition = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  onresult: ((event: NativeSpeechRecognitionEvent) => void) | null;
  onerror: ((event: NativeSpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
};

type NativeSpeechRecognitionEvent = {
  results: ArrayLike<ArrayLike<{ transcript: string }>>;
};

type NativeSpeechRecognitionErrorEvent = {
  error?: string;
};

type NativeSpeechWindow = Window & {
  SpeechRecognition?: NativeSpeechRecognitionConstructor;
  webkitSpeechRecognition?: NativeSpeechRecognitionConstructor;
};

export type NativeSpeechSession = {
  stop: () => Promise<string>;
};

const NATIVE_SPEECH_TIMEOUT_MS = 15000;

export function startNativeSpeechSession(): NativeSpeechSession | null {
  const Recognition = getNativeSpeechRecognition();
  if (!Recognition) return null;

  const recognition = new Recognition();
  let transcript = '';
  let failure: Error | null = null;
  let ended = false;

  recognition.lang = 'zh-CN';
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.onresult = (event) => {
    transcript = readTranscript(event);
  };
  recognition.onerror = (event) => {
    failure = new Error(formatNativeSpeechError(event.error));
  };
  recognition.onend = () => {
    ended = true;
  };

  try {
    recognition.start();
  } catch {
    return null;
  }

  return {
    stop: () => stopNativeRecognition(recognition, () => transcript, () => failure, () => ended),
  };
}

function getNativeSpeechRecognition(): NativeSpeechRecognitionConstructor | null {
  if (typeof window === 'undefined' || window.isSecureContext !== true) return null;
  const speechWindow = window as NativeSpeechWindow;
  return speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition || null;
}

function stopNativeRecognition(
  recognition: NativeSpeechRecognition,
  getTranscript: () => string,
  getFailure: () => Error | null,
  getEnded: () => boolean,
): Promise<string> {
  return new Promise((resolve, reject) => {
    const timeoutId = window.setTimeout(() => {
      recognition.abort();
      reject(new Error('内置语音识别超时。'));
    }, NATIVE_SPEECH_TIMEOUT_MS);

    recognition.onend = () => {
      window.clearTimeout(timeoutId);
      const failure = getFailure();
      if (failure) {
        reject(failure);
        return;
      }
      const transcript = getTranscript().trim();
      if (!transcript) {
        reject(new Error('内置语音未识别到内容。'));
        return;
      }
      resolve(transcript);
    };

    try {
      if (getEnded()) {
        recognition.onend?.();
      } else {
        recognition.stop();
      }
    } catch {
      window.clearTimeout(timeoutId);
      reject(new Error('内置语音识别停止失败。'));
    }
  });
}

function readTranscript(event: NativeSpeechRecognitionEvent): string {
  const firstResult = event.results[0];
  const firstAlternative = firstResult?.[0];
  return firstAlternative?.transcript || '';
}

function formatNativeSpeechError(error?: string): string {
  if (error === 'not-allowed' || error === 'service-not-allowed') {
    return '麦克风权限未开启或语音识别服务不可用。';
  }
  if (error === 'no-speech') {
    return '内置语音未识别到内容。';
  }
  if (error === 'aborted') {
    return '语音识别已取消。';
  }
  return '内置语音识别失败。';
}
