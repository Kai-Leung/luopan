import React from 'react';

export function MockToast({ message, visible }: { message: string; visible: boolean }) {
  if (!visible) return null;
  return (
    <div className="h5-toast">
      <div className="h5-toast-inner">{message}</div>
    </div>
  );
}
