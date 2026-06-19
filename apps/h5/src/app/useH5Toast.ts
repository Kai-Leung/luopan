import { useCallback, useEffect, useRef, useState } from 'react';
import { safeClearTimeout, safeSetTimeout } from '../utils/browserSafe';

export function useH5Toast() {
  const [toastMsg, setToastMsg] = useState('');
  const [toastVisible, setToastVisible] = useState(false);
  const toastTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const showToast = useCallback((message: string) => {
    safeClearTimeout(toastTimerRef.current);
    setToastMsg(message);
    setToastVisible(true);
    toastTimerRef.current = safeSetTimeout(() => setToastVisible(false), 3800);
  }, []);

  useEffect(() => () => {
    safeClearTimeout(toastTimerRef.current);
  }, []);

  return { toastMsg, toastVisible, showToast };
}
