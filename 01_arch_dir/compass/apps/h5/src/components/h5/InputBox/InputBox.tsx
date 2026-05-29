import React from 'react';
import type { RefObject } from 'react';
import type { InteractionAction } from '../../../modules/input_flow/h5Interaction';
import { EditIcon, PlusIcon, SearchIcon, SendArrowIcon, SparkleIcon, VoiceBarsIcon } from '../icons/H5Icons';

export function InputBox({
  inputRef,
  inputText,
  uploadOpen,
  pressingAction,
  onInputChange,
  onSubmit,
  onToggleUpload,
  onVoiceStart,
  onVoiceEnd,
}: {
  inputRef: RefObject<HTMLTextAreaElement | null>;
  inputText: string;
  uploadOpen: boolean;
  pressingAction: InteractionAction | null;
  onInputChange: (value: string) => void;
  onSubmit: (action?: InteractionAction) => void;
  onToggleUpload: () => void;
  onVoiceStart: (action: InteractionAction) => void;
  onVoiceEnd: (action: InteractionAction) => void;
}) {
  return (
    <>
      <section className="h5-input-section">
        <div className="h5-input-bar">
          <EditIcon />
          <textarea
            ref={inputRef}
            className="h5-input-control"
            value={inputText}
            placeholder="输入内容，或按住说话..."
            rows={1}
            onChange={(event) => onInputChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                onSubmit();
              }
            }}
          />
          <button className="h5-input-send" onClick={() => onSubmit()} disabled={!inputText.trim()} aria-label="发送输入内容" type="button">
            <SendArrowIcon />
          </button>
        </div>
        <button className={`h5-upload-btn ${uploadOpen ? 'h5-upload-btn-open' : ''}`} onClick={onToggleUpload} aria-label="打开上传选择">
          <PlusIcon />
        </button>
      </section>

      <section className="h5-bottom-actions">
        {(['查', '录入', '问'] as InteractionAction[]).map((action) => (
          <button
            className={`h5-action-card ${action === '查' ? 'h5-action-left' : action === '录入' ? 'h5-action-center' : 'h5-action-right'} ${pressingAction === action ? 'h5-action-pressing' : ''}`}
            aria-label={`按住语音${action}`}
            key={action}
            onPointerDown={() => onVoiceStart(action)}
            onPointerUp={() => onVoiceEnd(action)}
            onPointerCancel={() => onVoiceEnd(action)}
            onPointerLeave={() => onVoiceEnd(action)}
          >
            {action === '查' ? <SearchIcon /> : action === '录入' ? <VoiceBarsIcon /> : <SparkleIcon />}
          </button>
        ))}
      </section>
      {pressingAction ? <div className="h5-voice-hint">松开后转写</div> : null}
    </>
  );
}
