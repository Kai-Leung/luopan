import React from 'react';

export function InteractionPromptDialog({
  prompt,
  value,
  onValueChange,
  onCancel,
  onSubmit,
}: {
  prompt: { title: string; placeholder: string } | null;
  value: string;
  onValueChange: (value: string) => void;
  onCancel: () => void;
  onSubmit: () => void;
}) {
  if (!prompt) return null;
  return (
    <div className="h5-interaction-dialog-mask" role="presentation" onClick={onCancel}>
      <section className="h5-interaction-dialog" role="dialog" aria-label={prompt.title} onClick={(event) => event.stopPropagation()}>
        <h3>{prompt.title}</h3>
        <textarea value={value} placeholder={prompt.placeholder} onChange={(event) => onValueChange(event.target.value)} autoFocus />
        <div className="h5-interaction-dialog-actions">
          <button type="button" onClick={onCancel}>取消</button>
          <button type="button" className="h5-interaction-dialog-submit" onClick={onSubmit}>提交</button>
        </div>
      </section>
    </div>
  );
}
