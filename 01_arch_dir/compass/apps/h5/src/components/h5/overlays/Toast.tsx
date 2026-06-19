import React from 'react';

export function Toast({ message, visible }: { message: string; visible: boolean }) {
  if (!visible) return null;
  return (
    <div className="h5-toast" role="status" aria-live="polite">
      <div className="h5-toast-inner">{message}</div>
    </div>
  );
}
