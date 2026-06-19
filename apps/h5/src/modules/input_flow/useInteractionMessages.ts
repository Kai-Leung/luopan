import { useCallback, useEffect, useRef, useState } from 'react';
import type { Dispatch, RefObject, SetStateAction } from 'react';
import {
  loadStoredMessages,
  MESSAGE_STORAGE_KEY,
} from './h5Interaction';
import type { InteractionMessage } from './h5Interaction';
import { safeTrySetItem } from '../../utils/browserSafe';

type UseInteractionMessagesOptions = {
  inputRef: RefObject<HTMLTextAreaElement | null>;
  setInputText: Dispatch<SetStateAction<string>>;
};

export function useInteractionMessages({
  inputRef,
  setInputText,
}: UseInteractionMessagesOptions) {
  const [messages, setMessages] = useState<InteractionMessage[]>(loadStoredMessages);
  const messageEndRef = useRef<HTMLDivElement>(null);

  const appendMessage = useCallback((message: Omit<InteractionMessage, 'id' | 'createdAt'>) => {
    const trimmed = message.content.trim();
    if (!trimmed) return;
    setMessages((previous) => [
      ...previous,
      {
        id: `${Date.now()}-${previous.length}`,
        ...message,
        content: trimmed,
        createdAt: new Date().toISOString(),
      },
    ]);
  }, []);

  const appendToCentralInput = useCallback((text: string) => {
    const normalized = text.trim();
    if (!normalized) return;
    setInputText((previous) => (previous.trim() ? `${previous.trim()}\n${normalized}` : normalized));
    inputRef.current?.focus();
  }, [inputRef, setInputText]);

  const clearMessages = useCallback(() => setMessages([]), []);

  useEffect(() => {
    const stored = safeTrySetItem(MESSAGE_STORAGE_KEY, JSON.stringify(messages));
    if (!stored) {
      const compactMessages = messages.map((message) => (
        message.type === 'image' ? { ...message, dataUrl: undefined } : message
      ));
      safeTrySetItem(MESSAGE_STORAGE_KEY, JSON.stringify(compactMessages));
    }
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages]);

  return {
    messages,
    setMessages,
    appendMessage,
    appendToCentralInput,
    clearMessages,
    messageEndRef,
  };
}
